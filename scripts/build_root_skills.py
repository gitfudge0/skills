#!/usr/bin/env python3
"""Build self-contained public skills from the declared dependency graph."""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
MANIFEST = SOURCE / 'scripts/skill-manifest.json'

def closure(manifest, name):
    seen = set()
    def visit(root):
        if root in seen:
            return
        seen.add(root)
        for dependency in manifest['roots'][root]['roots']:
            visit(dependency)
    visit(name)
    return seen

def validate_manifest(manifest):
    for name, spec in manifest['roots'].items():
        assert (SOURCE / spec['source'] / 'SKILL.md').is_file(), name
        for dependency in spec['roots']:
            assert dependency in manifest['roots'], dependency
        for module in spec['modules']:
            assert manifest['modules'][module]['owner'] == name, module
    for name, spec in manifest['modules'].items():
        assert name in manifest['roots'][spec['owner']]['modules'], name
        assert (SOURCE / spec['source'] / spec.get('entry', 'guide.md')).is_file(), name
    for path in manifest['shared'] + manifest['helpers']:
        assert (SOURCE / path).exists(), path


def validate_source(manifest):
    """Verify fallback mappings before guides are copied into packages."""
    paths = [SOURCE / spec['source'] for spec in manifest['roots'].values()]
    paths += [SOURCE / spec['source'] for spec in manifest['modules'].values()]
    paths += [SOURCE / path for path in manifest['shared']]
    for directory in paths:
        for guide in directory.rglob('*.md'):
            for address in re.findall(r'(?:references/(?:modules|roots)/[\w-]+/guide\.md|shared/[\w/-]+\.md|shared/artifact_path\.py)', guide.read_text()):
                parts = address.split('/')
                if parts[:2] == ['references', 'roots']:
                    spec = manifest['roots'].get(parts[2])
                    target = SOURCE / spec['source'] / 'SKILL.md' if spec else None
                elif parts[:2] == ['references', 'modules']:
                    spec = manifest['modules'].get(parts[2])
                    target = SOURCE / spec['source'] / spec.get('entry', 'guide.md') if spec else None
                else:
                    target = SOURCE / address
                if target is None or not target.is_file():
                    raise ValueError(f'{guide.relative_to(SOURCE)}: invalid source fallback {address}')

def validate_package(package):
    """Check concrete package-root addresses and local Markdown links."""
    for guide in package.rglob('*.md'):
        text = guide.read_text()
        for address in re.findall(r'(?:references/(?:modules|roots)/[\w-]+/guide\.md|shared/[\w/-]+\.md|shared/artifact_path\.py)', text):
            if not (package / address).is_file():
                raise ValueError(f'{guide.relative_to(package)}: missing package address {address}')
        for address in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
            address = address.strip('<>').split('#', 1)[0]
            if not address or ':' in address or address.startswith('/') or any(c in address for c in (' ', '{', '$', '*')):
                continue
            if address == 'SKILL.md' or address.startswith(('references/modules/', 'references/roots/', 'shared/', 'shared/artifact_path.py')):
                target = package / address
            else:
                target = guide.parent / address
            if not target.exists():
                raise ValueError(f'{guide.relative_to(package)}: missing local link {address}')

def build(output):
    output = output.resolve()
    if output == SOURCE or output in SOURCE.parents:
        raise ValueError('Output must not be the source directory or its ancestor')
    manifest = json.loads(MANIFEST.read_text())
    validate_manifest(manifest)
    validate_source(manifest)
    output.mkdir(parents=True, exist_ok=True)
    names = [spec.get('package', 'fudge-' + name) for name, spec in manifest['roots'].items()]
    for name in names:
        target = output / name
        if target.exists() or target.is_symlink():
            if target.is_symlink() or not (target / '.fudge-build-generated').is_file():
                raise ValueError(f'Refusing to replace unmarked directory: {target}')
    # Retire only the former generated package, after validating new packages.
    retired = output / 'fudge-write'
    retire_write = (not retired.is_symlink() and retired.is_dir()
                    and (retired / '.fudge-build-generated').is_file())
    with tempfile.TemporaryDirectory(prefix='.fudge-stage.', dir=output) as stage:
        stage = Path(stage)
        for name, spec in manifest['roots'].items():
            package = stage / spec.get('package', 'fudge-' + name)
            shutil.copytree(SOURCE / spec['source'], package)
            included = closure(manifest, name)
            modules = set()
            for root in sorted(included):
                dependency = manifest['roots'][root]
                modules.update(dependency['modules'])
                if root != name:
                    destination = package / 'references/roots' / root
                    shutil.copytree(SOURCE / dependency['source'], destination)
                    (destination / 'SKILL.md').rename(destination / 'guide.md')
            for module in sorted(modules):
                module_spec = manifest['modules'][module]
                destination = package / 'references/modules' / module
                shutil.copytree(SOURCE / module_spec['source'], destination)
                entry = module_spec.get('entry', 'guide.md')
                if entry != 'guide.md':
                    (destination / entry).rename(destination / 'guide.md')
            for path in manifest['shared']:
                shutil.copytree(SOURCE / path, package / path)
            for path in manifest['helpers']:
                destination = package / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(SOURCE / path, destination)
            # Canonical routes to the primary root use its public entry rather
            # than creating a duplicate root guide inside its own package.
            for markdown in package.rglob('*.md'):
                markdown.write_text(markdown.read_text().replace(f'references/roots/{name}/guide.md', 'SKILL.md'))
            (package / '.fudge-package.json').write_text(json.dumps({'version': manifest['version'], 'root': name, 'roots': sorted(included), 'modules': sorted(modules)}, indent=2) + '\n')
            (package / '.fudge-build-generated').touch()
            validate_package(package)
        if retire_write:
            shutil.rmtree(retired)
        for name in names:
            destination = output / name
            if destination.exists():
                shutil.rmtree(destination)
            shutil.move(str(stage / name), destination)
    print(f'Built and validated {len(names)} public skills in {output}')

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: build_root_skills.py OUTPUT_DIR')
        build(Path(sys.argv[1]))
    except (ValueError, AssertionError, KeyError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
