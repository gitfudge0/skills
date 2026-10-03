#!/usr/bin/env python3
"""Resolve or reserve a Fudge artifact directory without modifying product files."""
import argparse
import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path


def git(cwd, *args):
    result = subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def branch_key(branch):
    # Encoding is injective: slash and hyphen cannot collapse into the same key.
    encoded = base64.urlsafe_b64encode(branch.encode()).decode().rstrip('=')
    readable = re.sub(r'[^a-zA-Z0-9._-]+', '-', branch).strip('.-')[:36] or 'branch'
    # Very long branch names use a digest to stay within filesystem limits.
    identity = encoded if len(encoded) <= 120 else hashlib.sha256(branch.encode()).hexdigest()
    return readable + '--' + identity


def resolve(cwd, skill, output=None, branch=None, name='run', create=False, exclude=False):
    cwd = Path(cwd).resolve()
    if not cwd.is_dir():
        raise ValueError('cwd must be an existing directory')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', skill):
        raise ValueError('skill must be a single safe path component')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', name):
        raise ValueError('name must be a single safe path component')
    top = git(cwd, 'rev-parse', '--show-toplevel')
    root = Path(top) if top else cwd
    default = output is None
    if output is not None:
        chosen = Path(output).expanduser()
        chosen = chosen if chosen.is_absolute() else cwd / chosen
        # A dangling symlink occupies the caller's exact destination too.
        # Check the original leaf before resolve() can redirect creation.
        if create and (chosen.exists() or chosen.is_symlink()):
            raise FileExistsError('explicit output exists; choose an unused path or resume it explicitly')
        chosen = chosen.resolve()
        if create and (chosen.exists() or chosen.is_symlink()):
            raise FileExistsError('explicit output exists; choose an unused path or resume it explicitly')
    else:
        identity = branch or git(cwd, 'branch', '--show-current')
        if top and not identity:
            identity = 'detached-' + (git(cwd, 'rev-parse', 'HEAD') or 'unknown')
        parent = root / '.fudge'
        if top:
            parent /= branch_key(identity)
        parent /= skill
        chosen = parent / name
        suffix = 2
        while True:
            if create:
                try:
                    chosen.mkdir(parents=True, exist_ok=False)
                    break
                except FileExistsError:
                    pass
            elif not chosen.exists():
                break
            chosen = parent / f'{name}-{suffix}'
            suffix += 1
    if create and not default:
        chosen.mkdir(parents=True, exist_ok=False)
    # Exclusion is optional and only applies to default artifacts in this worktree.
    if exclude and default and top and create:
        exclude_path = git(cwd, 'rev-parse', '--git-path', 'info/exclude')
        if exclude_path:
            path = Path(exclude_path)
            path = path if path.is_absolute() else cwd / path
            path.parent.mkdir(parents=True, exist_ok=True)
            old = path.read_text() if path.exists() else ''
            if '.fudge/' not in old.splitlines():
                with path.open('a') as stream:
                    stream.write(('' if not old or old.endswith('\n') else '\n') + '.fudge/\n')
    return {'path': str(chosen), 'root': str(root), 'git': bool(top), 'default': default, 'created': create}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd', default='.')
    parser.add_argument('--skill', required=True)
    parser.add_argument('--output')
    parser.add_argument('--branch', help='PR head branch override')
    parser.add_argument('--name', default='run')
    parser.add_argument('--mkdir', action='store_true', help='reserve a unique directory')
    parser.add_argument('--exclude', action='store_true', help='exclude default in-repo artifacts after creation')
    args = parser.parse_args()
    try:
        print(json.dumps(resolve(args.cwd, args.skill, args.output, args.branch, args.name, args.mkdir, args.exclude)))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
