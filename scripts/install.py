#!/usr/bin/env python3
"""Install public skills, migrating only entries owned by this checkout."""
import argparse
import json
import os
import shutil
import subprocess
import sys
from install_ui import choose as keyboard_choose, supported as keyboard_supported
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
BUILD = SOURCE / '.fudge-build'
MANIFEST = json.loads((SOURCE / 'scripts/skill-manifest.json').read_text())
ROOTS = list(MANIFEST['roots'])
PACKAGES = {name: spec.get('package', 'fudge-' + name) for name, spec in MANIFEST['roots'].items()}
ALIASES = {name: spec['owner'] for name, spec in MANIFEST['modules'].items() if name not in ROOTS}
ALIASES.update({'conventions': 'setup', 'delegate': 'ship', 'unslop': 'ship', 'report-deck': 'design'})
RETIRED = set(ALIASES) | {'mindmap'}
LEGACY = {'html-plan': 'html-plan'}
AGENTS = {'claude': '.claude/skills', 'codex': '.codex/skills', 'cursor': '.cursor/skills', 'opencode': '.config/opencode/skills'}

def owned(path):
    if path.name not in set(PACKAGES.values()) | set(LEGACY) | {'fudge-' + name for name in RETIRED}:
        return False
    if path.is_symlink():
        # Compare literal targets, including dangling old source links. Never resolve
        # an arbitrary link and mistake someone else's directory for our install.
        return os.readlink(path) in {str(SOURCE / path.name), str(BUILD / path.name)}
    marker = path / '.fudge-installer'
    return path.is_dir() and marker.is_file() and marker.read_text().strip() == str(SOURCE)

def retired_for(target, roots):
    legacy = [target / name for name, root in LEGACY.items() if root in roots and owned(target / name)]
    return legacy + [target / ('fudge-' + name) for name in sorted(RETIRED)
            if (name == 'mindmap' or ALIASES.get(name) in roots)
            and owned(target / ('fudge-' + name))]


def erase(path):
    if not owned(path):
        raise ValueError(f'Destination changed or is not installer-owned: {path}')
    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)

def select(title, choices, defaults):
    print(title)
    for index, name in enumerate(choices, 1):
        print(f'  [{"x" if name in defaults else " "}] {index} {name}')
    answer = input('Enter keeps defaults; numbers select; a selects all; n selects none; q cancels: ').strip()
    if answer.lower() == 'q':
        raise KeyboardInterrupt
    if not answer:
        return list(defaults)
    if answer.lower() == 'a':
        return list(choices)
    if answer.lower() == 'n':
        return []
    result = []
    for token in answer.replace(',', ' ').split():
        if not token.isdigit() or not 1 <= int(token) <= len(choices):
            raise ValueError(f'Invalid selection: {token}')
        name = choices[int(token) - 1]
        if name not in result:
            result.append(name)
    return result

def main():
    parser = argparse.ArgumentParser(description='Install public Fudge skills. Specialists are bundled internal modules.')
    parser.add_argument('command', nargs='?', choices=['install', 'list', 'remove'], default='install')
    parser.add_argument('-a', '--agent', action='append', choices=AGENTS, default=[])
    parser.add_argument('--root', action='append', default=[], help=', '.join(ROOTS) + ' (conventions is a migration alias)')
    parser.add_argument('--skill', action='append', default=[], help='public skill or legacy name; legacy modules select their owning root')
    parser.add_argument('--all', action='store_true', help='select all public roots; remove all owned entries')
    parser.add_argument('--no-roots', action='store_true', help='legacy flag, accepted only with --skill')
    parser.add_argument('--copy', action='store_true')
    parser.add_argument('-y', action='store_true', help='apply without terminal confirmation')
    args = parser.parse_args()
    if args.all and (args.root or args.skill or args.no_roots):
        raise ValueError('--all cannot be combined with selections')
    if args.no_roots and (args.root or not args.skill):
        raise ValueError('--no-roots is supported only with legacy --skill selections; modules now install through their owning root')
    roots = []
    for name in args.root + args.skill:
        name = name.removeprefix('fudge-')
        if name == 'mindmap':
            raise ValueError('mindmap has been removed; it has no replacement public skill')
        root = ALIASES.get(name, name)
        if root not in ROOTS:
            raise ValueError(f'Unknown skill: {name}')
        if root != name:
            print(f'Migration: {name} → fudge:{root}')
        if root not in roots:
            roots.append(root)
    interactive = sys.stdin.isatty() and not args.y
    agents = list(dict.fromkeys(args.agent))
    keyboard_confirmed = False
    if args.command == 'install':
        if interactive and not args.all and keyboard_supported():
            selection = keyboard_choose(list(AGENTS), ROOTS, agents or ['codex'], roots or ROOTS, args.copy, lambda agent: Path.home() / AGENTS[agent], owned, retired_for, package_for=lambda root: PACKAGES[root])
            if selection is None:
                print('Aborted.')
                return
            agents, roots, args.copy = selection
            keyboard_confirmed = True
        if not agents:
            if not interactive:
                raise ValueError('Specify at least one target agent with -a for a non-interactive install')
            agents = select('Choose target agents:', list(AGENTS), ['codex'])
        if not roots:
            roots = select('Choose public skills:', ROOTS, ROOTS) if interactive and not args.all else ROOTS[:]
        if not agents or not roots:
            print('Nothing selected.')
            return
        if interactive and not keyboard_confirmed and not args.copy:
            args.copy = input('Install method: symlink [Enter] or copy [c]: ').lower() == 'c'
    else:
        agents = agents or list(AGENTS)
    targets = [Path.home() / AGENTS[name] for name in agents]
    if args.command == 'list':
        for name, target in zip(agents, targets):
            print(f'{name} ({target}):')
            if target.is_dir():
                for entry in sorted(target.iterdir()):
                    print(f'  {"owned" if owned(entry) else "foreign"}  {entry.name}')
        return
    if args.command == 'remove':
        candidates = [entry for target in targets if target.is_dir() for entry in sorted(target.iterdir()) if owned(entry)]
        if roots:
            candidates = [entry for entry in candidates if LEGACY.get(entry.name, ALIASES.get(entry.name.removeprefix('fudge-'), entry.name.removeprefix('fudge-'))) in roots]
        elif not args.all:
            if not candidates:
                print('No installer-owned skills found.')
                return
            if not interactive:
                raise ValueError('Remove requires --all or an explicit --root selection')
            chosen = select('Choose installs to remove:', [str(p) for p in candidates], [])
            candidates = [p for p in candidates if str(p) in chosen]
    else:
        candidates = [target / PACKAGES[root] for target in targets for root in roots]
        conflicts = [p for p in candidates if (p.exists() or p.is_symlink()) and not owned(p)]
        if conflicts:
            raise ValueError('Existing installs not owned by this installer:\n  ' + '\n  '.join(map(str, conflicts)))
    cleanup = [path for target in targets for path in retired_for(target, roots)] if args.command == 'install' else []
    print(f'Ready to {args.command}:')
    for path in candidates:
        print(f'  {path}')
    if cleanup:
        print('Retired entries to remove:')
        for path in cleanup:
            print(f'  {path}')
    if not args.y and not keyboard_confirmed and (interactive or args.command == 'remove'):
        if not interactive:
            raise ValueError('Confirmation requires a terminal; pass -y')
        if input('Proceed? [y/N] ').lower() != 'y':
            print('Aborted.')
            return
    if args.command == 'remove':
        for path in candidates:
            erase(path)
        print(f'Removed {len(candidates)} installer-owned skills.')
        return
    subprocess.run(['bash', str(SOURCE / 'scripts/build-root-skills.sh'), str(BUILD)], check=True)
    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        for root in roots:
            path = target / PACKAGES[root]
            if path.exists() or path.is_symlink():
                erase(path)
            source = BUILD / path.name
            if args.copy:
                shutil.copytree(source, path)
                (path / '.fudge-installer').write_text(str(SOURCE) + '\n')
            else:
                path.symlink_to(source, target_is_directory=True)
    for path in cleanup:
        erase(path)
        print(f'Migrated retired entry: {path}')
    print(f'Installed {len(roots)} public skills for {len(targets)} agents.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(130)
    except (ValueError, OSError, subprocess.CalledProcessError, EOFError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
