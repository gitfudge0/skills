#!/usr/bin/env python3
"""Convert tests/evals/scenarios.json into `claude plugin eval` suites.

Each selected public root becomes a minimal plugin wrapper:

    <out>/<package>/.claude-plugin/plugin.json
    <out>/<package>/skills/<package>/      copy of .fudge-build/<package>
    <out>/<package>/evals/<case>/case.yaml one case per scenario

case.yaml is written as JSON, which is valid YAML. Each invariant becomes one
LLM grader over the run trace. The scenario fixture is supplied to the agent as
an appended system prompt; cases with a `fixture_id` also get a scaffold script
that generates the isolated ship fixture repository (it runs only with
`claude plugin eval --scaffold`).
"""
import argparse
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCENARIOS = REPO / 'tests/evals/scenarios.json'
MANIFEST = REPO / 'scripts/skill-manifest.json'
FIXTURES = REPO / 'tests/evals/ship_fixtures.py'
MARKER = '.fudge-evals-generated'
TOOLS = ['Read', 'Glob', 'Grep', 'Skill', 'Bash', 'Edit', 'Write']

FIXTURE_NOTE = (
    'Evaluation fixture. The following describes the workspace and environment for this task. '
    'Where something it describes is not present in the working directory, treat the description '
    'as the real situation: say what you would inspect and do, and never invent command output, '
    'file contents or results.\n\nFixture: {fixture}'
)
GRADER = (
    'Scenario fixture: {fixture}\n'
    'User prompt: {prompt}\n\n'
    'Pass only if the transcript shows this behavior: {invariant}\n\n'
    'Judge observable actions (tool calls, edits, posts) and the final output, not wording. '
    'If the fixture was only described rather than present, accept clearly stated intended actions '
    'that satisfy the behavior, but fail any invented results or any forbidden action actually taken.'
)
SCAFFOLD = '''#!/usr/bin/env bash
# Generated: creates the isolated "{fixture_id}" ship fixture in the run's working directory.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tree="$(mktemp -d)/tree"
python3 "$here/ship_fixtures.py" create --output "$tree" >/dev/null
cp -R "$tree/{fixture_id}/." .
'''


def slug(text, words=6):
    parts = re.findall(r'[a-z0-9]+', text.lower())[:words]
    return '-'.join(parts) or 'case'


def case_names(cases):
    names, used = [], set()
    for index, case in enumerate(cases, 1):
        name = case.get('id') or f"{case['root']}-{index:02d}-{slug(case['prompt'])}"
        base, n = name, 2
        while name in used:
            name, n = f'{base}-{n}', n + 1
        used.add(name)
        names.append(name)
    return names


def to_case_yaml(name, case, args):
    tags = [case['root'], case.get('source', 'scenario')]
    if case.get('fixture_id'):
        tags.append('fixture-' + case['fixture_id'])
    fixture = case.get('fixture', '')
    if case.get('fixture_id'):
        fixture = (f"The working directory holds the generated '{case['fixture_id']}' fixture repository "
                   '(present only when the suite runs with --scaffold).')
    execution = {
        'prompt': case['prompt'],
        'max_turns': args.max_turns,
        'timeout_seconds': args.timeout,
        'allowed_tools': TOOLS,
    }
    if fixture:
        execution['append_system_prompt'] = FIXTURE_NOTE.format(fixture=fixture)
    document = {
        'schema_version': '1.0',
        'name': name,
        'description': (case.get('lesson') or fixture)[:500],
        'tags': tags,
        'execution': execution,
        'graders': [
            {
                'type': 'llm',
                'name': f'invariant-{number:02d}',
                'focus': 'trace',
                'criteria': GRADER.format(fixture=fixture, prompt=case['prompt'], invariant=invariant),
            }
            for number, invariant in enumerate(case['invariants'], 1)
        ],
        'expected_outcome': '; '.join(case['invariants']),
    }
    if args.runs:
        document['runs'] = args.runs
    if case.get('fixture_id'):
        document['context'] = {'scaffold_script': 'scaffold.sh'}
    return document


# Mirrors the case.yaml schema accepted by `claude plugin eval` (schema 1.x), which
# has no dry-run mode: generated cases are checked here instead of by running them.
CASE_KEYS = {'schema_version', 'name', 'description', 'tags', 'plugins', 'context', 'execution', 'runs', 'graders', 'expected_outcome'}
EXECUTION_KEYS = {'prompt', 'max_turns', 'timeout_seconds', 'model', 'allowed_tools', 'artifact_publish',
                  'growthbook_overrides', 'append_system_prompt', 'env'}
CONTEXT_KEYS = {'scaffold_script', 'history_file', 'add_dirs'}
GRADER_KEYS = {'llm': {'type', 'name', 'criteria', 'focus', 'weight', 'arm'}}
FOCUS = {'trace', 'last_message', 'files', 'mock_calls'}


def check_case(path):
    """Return schema problems for one generated case.yaml."""
    problems = []
    def need(condition, message):
        if not condition:
            problems.append(f'{path}: {message}')
    try:
        case = json.loads(path.read_text())
    except ValueError as error:
        return [f'{path}: not parseable: {error}']
    need(isinstance(case, dict), 'must be an object')
    if problems:
        return problems
    need(set(case) <= CASE_KEYS, f'unknown keys {sorted(set(case) - CASE_KEYS)}')
    need(str(case.get('schema_version', '')).split('.')[0] == '1', 'schema_version must be 1.x')
    need(isinstance(case.get('name'), str) and case['name'] == path.parent.name, 'name must match its directory')
    need(all(isinstance(t, str) for t in case.get('tags', [])), 'tags must be strings')
    execution = case.get('execution', {})
    need(set(execution) <= EXECUTION_KEYS, f'unknown execution keys {sorted(set(execution) - EXECUTION_KEYS)}')
    need(isinstance(execution.get('prompt'), str) and execution['prompt'].strip(), 'execution.prompt is required')
    need(1 <= execution.get('max_turns', 10) <= 200, 'max_turns must be 1..200')
    need(1 <= execution.get('timeout_seconds', 300) <= 3600, 'timeout_seconds must be 1..3600')
    need(1 <= case.get('runs', 3) <= 50, 'runs must be 1..50')
    context = case.get('context', {})
    need(set(context) <= CONTEXT_KEYS, f'unknown context keys {sorted(set(context) - CONTEXT_KEYS)}')
    if 'scaffold_script' in context:
        need((path.parent / context['scaffold_script']).is_file(), 'scaffold_script is missing')
    graders = case.get('graders', [])
    need(isinstance(graders, list) and graders, 'at least one grader is required')
    names = [g.get('name') for g in graders]
    need(len(names) == len(set(names)), 'grader names must be unique')
    for grader in graders:
        keys = GRADER_KEYS.get(grader.get('type'))
        need(keys is not None, f'unsupported grader type {grader.get("type")!r}')
        if keys:
            need(set(grader) <= keys, f'unknown grader keys {sorted(set(grader) - keys)}')
            need(isinstance(grader.get('criteria'), str) and grader['criteria'].strip(), 'llm grader needs criteria')
            need(grader.get('focus', 'last_message') in FOCUS, 'invalid grader focus')
    return problems


def check_wrapper(wrapper):
    problems = []
    manifest = wrapper / '.claude-plugin/plugin.json'
    if not manifest.is_file():
        problems.append(f'{manifest}: missing')
    skills = list((wrapper / 'skills').glob('*/SKILL.md'))
    if len(skills) != 1:
        problems.append(f'{wrapper}/skills: expected exactly one SKILL.md, found {len(skills)}')
    cases = sorted((wrapper / 'evals').glob('*/case.yaml'))
    if not cases:
        problems.append(f'{wrapper}/evals: no cases')
    for case in cases:
        problems += check_case(case)
    return problems, len(cases)


def reset(directory):
    if directory.is_symlink() or (directory.exists() and not (directory / MARKER).is_file()):
        raise ValueError(f'Refusing to replace unmarked directory: {directory}')
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)
    (directory / MARKER).touch()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', type=Path, default=REPO / '.fudge-evals')
    parser.add_argument('--build', type=Path, default=REPO / '.fudge-build')
    parser.add_argument('--root', action='append', default=[], help='public root to include (repeatable; default all)')
    parser.add_argument('--case', default='*', help='case-name glob')
    parser.add_argument('--runs', type=int, help='runs per case written into case.yaml (default: eval default)')
    parser.add_argument('--max-turns', type=int, default=40)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--check', type=Path, nargs='+', metavar='WRAPPER', help='only check already generated wrappers')
    args = parser.parse_args()

    if args.check:
        problems = []
        for wrapper in args.check:
            found, count = check_wrapper(wrapper)
            problems += found
            print(f'{wrapper}\t{count} case(s)\t{"OK" if not found else "FAIL"}')
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1 if problems else 0

    manifest = json.loads(MANIFEST.read_text())
    cases = json.loads(SCENARIOS.read_text())['cases']
    unknown = sorted({c['root'] for c in cases} - set(manifest['roots']))
    if unknown:
        raise ValueError(f'scenarios.json uses unknown roots: {unknown}')
    for root in args.root:
        if root not in manifest['roots']:
            raise ValueError(f'unknown root {root!r}; choose from {", ".join(manifest["roots"])}')

    selected = {}
    for name, case in zip(case_names(cases), cases):
        if args.root and case['root'] not in args.root:
            continue
        if not fnmatch.fnmatchcase(name, args.case):
            continue
        selected.setdefault(case['root'], []).append((name, case))
    if not selected:
        raise ValueError('no scenarios match the root/case filters')

    packages = {root: manifest['roots'][root].get('package', 'fudge-' + root) for root in selected}
    missing = [str(args.build / p) for p in packages.values() if not (args.build / p / 'SKILL.md').is_file()]
    if missing:
        raise ValueError(f'missing built packages {missing}; build first: bash scripts/build-root-skills.sh {args.build}')
    args.out.mkdir(parents=True, exist_ok=True)
    for root, entries in selected.items():
        package = packages[root]
        source = args.build / package
        wrapper = args.out / package
        reset(wrapper)
        (wrapper / '.claude-plugin').mkdir()
        (wrapper / '.claude-plugin/plugin.json').write_text(json.dumps({
            'name': package,
            'version': '0.0.0',
            'description': f'Evaluation wrapper for the {package} skill package (generated).',
            'author': {'name': 'fudge skills'},
        }, indent=2) + '\n')
        shutil.copytree(source, wrapper / 'skills' / package, ignore=shutil.ignore_patterns('.fudge-build-generated'))
        for name, case in entries:
            directory = wrapper / 'evals' / name
            directory.mkdir(parents=True)
            (directory / 'case.yaml').write_text(json.dumps(to_case_yaml(name, case, args), indent=2, ensure_ascii=False) + '\n')
            if case.get('fixture_id'):
                shutil.copy2(FIXTURES, directory / 'ship_fixtures.py')
                script = directory / 'scaffold.sh'
                script.write_text(SCAFFOLD.format(fixture_id=case['fixture_id']))
                script.chmod(0o755)
        problems, _ = check_wrapper(wrapper)
        if problems:
            raise ValueError('generated suite failed schema checks:\n' + '\n'.join(problems))
        print(f'{wrapper}\t{len(entries)}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
