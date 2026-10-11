#!/usr/bin/env python3
"""Isolated installer behavior and package navigation checks."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parent.parent

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / 'repository'
        shutil.copytree(REPO, self.repo, ignore=shutil.ignore_patterns('.git', '.fudge-build', '__pycache__'))
        self.home = self.base / 'home'
        self.home.mkdir()
        self.skills = self.home / '.codex/skills'
        self.env = dict(os.environ, HOME=str(self.home))
    def tearDown(self):
        self.temp.cleanup()
    def run_install(self, *args, success=True):
        result = subprocess.run(['bash', str(self.repo / 'install.sh'), *args], env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result
    def test_defaults_and_standalone_navigation(self):
        self.run_install('install', '-a', 'codex')
        self.assertEqual({p.name for p in self.skills.iterdir()}, {'fudge-' + n for n in ['design', 'ux', 'ship', 'review', 'setup']} | {'fudge-plan'})
        spec = importlib.util.spec_from_file_location('builder', self.repo / 'scripts/build_root_skills.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        builder.validate_source(json.loads((self.repo / "scripts/skill-manifest.json").read_text()))
        for skill in self.skills.iterdir():
            builder.validate_package(skill)
            marker = json.loads((skill / '.fudge-package.json').read_text())
            self.assertFalse((skill / 'references/roots' / marker['root']).exists())
            self.assertEqual(len(list(skill.rglob('SKILL.md'))), 1)
            self.assertTrue((skill / 'shared/artifact_path.py').is_file())
        self.run_install('remove', '-a', 'codex', '--all', '-y')
        self.run_install('-a', 'codex', '--root', 'setup', '-y')
        self.assertEqual([p.name for p in self.skills.iterdir()], ['fudge-setup'])
    def test_removed_write_rejected_without_mutation(self):
        self.skills.mkdir(parents=True)
        old = self.skills / 'fudge-write'
        old.symlink_to(self.repo / 'fudge-write')
        for flag in ('--root', '--skill'):
            result = self.run_install('-a', 'codex', flag, 'fudge-write', '-y', success=False)
            self.assertIn('write has been removed', result.stderr)
            self.assertTrue(old.is_symlink())

    def test_write_retirement_all_hosts_and_package_closure(self):
        targets = ['.codex/skills', '.claude/skills', '.cursor/skills', '.config/opencode/skills']
        for target, mode in zip(targets, ['source', 'build', 'copy', 'foreign']):
            old = self.home / target / 'fudge-write'
            old.parent.mkdir(parents=True)
            if mode in ('source', 'build'):
                old.symlink_to(self.repo / ('fudge-write' if mode == 'source' else '.fudge-build/fudge-write'))
            else:
                old.mkdir()
                (old / ('manual.txt' if mode == 'foreign' else '.fudge-installer')).write_text('keep' if mode == 'foreign' else str(self.repo))
        self.run_install('-a', 'codex', '--root', 'setup', '-y')
        self.assertTrue((self.home / targets[0] / 'fudge-write').is_symlink())
        result = self.run_install('-a', 'codex', '-a', 'claude', '-a', 'cursor', '-a', 'opencode', '--all', '-y')
        manifest = json.loads((self.repo / 'scripts/skill-manifest.json').read_text())
        for index, target in enumerate(targets):
            directory = self.home / target
            old = directory / 'fudge-write'
            if index == 3:
                self.assertEqual((old / 'manual.txt').read_text(), 'keep')
            else:
                self.assertFalse(old.exists())
                self.assertFalse(old.is_symlink())
            for root in manifest['roots']:
                package = directory / ('fudge-' + root)
                metadata = json.loads((package / '.fudge-package.json').read_text())
                self.assertEqual(metadata['root'], root)
                for module in metadata['modules']:
                    self.assertTrue((package / 'references/modules' / module / 'guide.md').is_file())
            self.assertTrue((directory / 'fudge-ship/references/roots/setup/references/project-verification.md').is_file())
            self.assertTrue((directory / 'fudge-ship/references/modules/engineering/references/refactoring.md').is_file())
            self.assertTrue((directory / 'fudge-review/shared/test-effectiveness.md').is_file())
        self.assertIn('Installed 6 public skills for 4 agents', result.stdout)
        # Noninteractive default selection has the same retirement behavior.
        old = self.home / targets[0] / 'fudge-write'
        old.symlink_to(self.repo / 'fudge-write')
        self.run_install('-a', 'codex', '-y')
        self.assertFalse(old.exists() or old.is_symlink())

    def test_write_remove_all_owned_and_preserve_foreign(self):
        self.skills.mkdir(parents=True)
        old = self.skills / 'fudge-write'
        for mode in ('source', 'build', 'copy', 'foreign-link', 'foreign-copy'):
            if mode in ('source', 'build', 'foreign-link'):
                destination = self.base / 'foreign' if mode == 'foreign-link' else self.repo / ('fudge-write' if mode == 'source' else '.fudge-build/fudge-write')
                old.symlink_to(destination)
            else:
                old.mkdir()
                (old / '.fudge-installer').write_text(str(self.repo) if mode == 'copy' else str(self.base / 'elsewhere'))
            self.run_install('remove', '-a', 'codex', '--all', '-y')
            if mode.startswith('foreign'):
                self.assertTrue(old.exists() or old.is_symlink())
                if old.is_symlink():
                    old.unlink()
                else:
                    shutil.rmtree(old)
            else:
                self.assertFalse(old.exists() or old.is_symlink())

    def test_build_retires_only_marked_write_and_preserves_assets(self):
        output = self.base / 'build'
        output.mkdir()
        retired = output / 'fudge-write'
        retired.mkdir()
        (retired / '.fudge-build-generated').touch()
        unrelated = output / 'user-asset'
        unrelated.write_text('keep')
        def build():
            result = subprocess.run(['bash', str(self.repo / 'scripts/build-root-skills.sh'), str(output)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        build()
        self.assertFalse(retired.exists())
        self.assertEqual(unrelated.read_text(), 'keep')
        retired.mkdir()
        (retired / 'manual.txt').write_text('keep')
        build()
        self.assertEqual((retired / 'manual.txt').read_text(), 'keep')
        shutil.rmtree(retired)
        foreign = self.base / 'foreign-build'
        foreign.mkdir()
        (foreign / '.fudge-build-generated').touch()
        retired.symlink_to(foreign)
        build()
        self.assertTrue(retired.is_symlink())
        self.assertTrue((foreign / '.fudge-build-generated').exists())

    def test_ship_plan_packs_without_source_checkout(self):
        self.run_install('-a', 'codex', '--root', 'ship', '--copy', '-y')
        installed = self.skills / 'fudge-ship'
        self.assertEqual({p.name for p in self.skills.iterdir()}, {'fudge-ship'})
        marker = json.loads((installed / '.fudge-package.json').read_text())
        self.assertIn('plan', marker['modules'])
        module = installed / 'references/modules/plan'
        self.assertTrue((module / 'guide.md').is_file())
        self.assertFalse((module / 'SKILL.md').exists())
        for source in (self.repo / 'plan').rglob('*'):
            if source.is_file() and source.name != 'SKILL.md':
                self.assertEqual((module / source.relative_to(self.repo / 'plan')).read_bytes(), source.read_bytes())
        # A copied installation must work after the entire checkout disappears.
        shutil.rmtree(self.repo)
        if not shutil.which('node'):
            self.skipTest('Node.js is required to exercise the HTML packer')
        packed = self.base / 'standalone-plan.html'
        result = subprocess.run([
            'node', str(module / 'runtime/pack.mjs'),
            str(module / 'examples/sample-plan.html'),
            '--root', str(module), '-o', str(packed),
        ], cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        text = packed.read_text()
        self.assertIn('<style data-htmlplan>', text)
        self.assertIn('<script data-htmlplan>', text)
        self.assertNotIn('src="../runtime/htmlplan.js"', text)
        self.assertNotIn('href="../runtime/htmlplan.css"', text)

    def test_plan_standalone_update_remove_and_coexistence(self):
        for copy in (False, True):
            with self.subTest(copy=copy):
                args = ['-a', 'codex', '--skill', 'plan', '-y']
                if copy:
                    args.append('--copy')
                self.run_install(*args)
                installed = self.skills / 'fudge-plan'
                self.assertEqual({p.name for p in self.skills.iterdir()}, {'fudge-plan'})
                self.assertEqual(installed.is_symlink(), not copy)
                self.assertEqual(json.loads((installed / '.fudge-package.json').read_text())['root'], 'plan')
                for source in (self.repo / 'plan').rglob('*'):
                    if source.is_file():
                        self.assertEqual((installed / source.relative_to(self.repo / 'plan')).read_bytes(), source.read_bytes())
                source = self.repo / 'plan/SKILL.md'
                source.write_text(source.read_text() + '\nStandalone HTML update fixture.\n')
                self.run_install(*args)
                self.assertIn('Standalone HTML update fixture.', (installed / 'SKILL.md').read_text())
                self.run_install('-a', 'codex', '--root', 'ship', '-y')
                self.assertTrue((installed / 'SKILL.md').exists())
                self.assertTrue((self.skills / 'fudge-ship/references/modules/plan/guide.md').exists())
                listing = self.run_install('list', '-a', 'codex')
                self.assertIn('owned  fudge-plan', listing.stdout)
                self.run_install('remove', '-a', 'codex', '--root', 'plan', '-y')
                self.assertFalse(installed.exists())
                self.assertFalse(installed.is_symlink())
                self.assertTrue((self.skills / 'fudge-ship').exists())
                self.run_install('remove', '-a', 'codex', '--all', '-y')

    def test_plan_copy_packs_without_checkout(self):
        self.run_install('-a', 'codex', '--root', 'plan', '--copy', '-y')
        installed = self.skills / 'fudge-plan'
        shutil.rmtree(self.repo)
        if not shutil.which('node'):
            self.skipTest('Node.js is required to exercise the HTML packer')
        packed = self.base / 'standalone-plan.html'
        result = subprocess.run(['node', str(installed / 'runtime/pack.mjs'),
            str(installed / 'examples/sample-plan.html'), '--root', str(installed), '-o', str(packed)],
            cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('<script data-htmlplan>', packed.read_text())
        self.assertIn('<style data-htmlplan>', packed.read_text())

    def test_plan_foreign_and_legacy_ownership(self):
        self.skills.mkdir(parents=True)
        legacy = self.skills / 'html-plan'
        legacy.symlink_to(self.repo / 'html-plan')
        old_package = self.skills / 'fudge-html-plan'
        old_package.symlink_to(self.repo / '.fudge-build/fudge-html-plan')
        self.run_install('-a', 'codex', '--root', 'ship', '-y')
        self.assertTrue(legacy.is_symlink())
        self.assertTrue(old_package.is_symlink())
        foreign = self.skills / 'fudge-plan'
        foreign.symlink_to(self.base / 'missing')
        self.run_install('-a', 'codex', '--root', 'html-plan', '-y', success=False)
        self.assertTrue(foreign.is_symlink())
        self.assertTrue(legacy.is_symlink())
        self.assertTrue(old_package.is_symlink())
        foreign.unlink()
        self.run_install('-a', 'codex', '--root', 'html-plan', '-y')
        self.assertFalse(legacy.is_symlink())
        self.assertFalse(old_package.is_symlink())
        self.assertTrue(foreign.is_symlink())
        legacy.symlink_to(self.base / 'unrelated')
        old_package.mkdir()
        (old_package / 'manual.txt').write_text('keep')
        self.run_install('-a', 'codex', '--all', '-y')
        self.run_install('remove', '-a', 'codex', '--all', '-y')
        self.assertTrue(legacy.is_symlink())
        self.assertEqual((old_package / 'manual.txt').read_text(), 'keep')
        self.assertFalse(foreign.is_symlink())

    def test_plan_legacy_copy_and_selection_aliases(self):
        self.skills.mkdir(parents=True)
        for name in ('html-plan', 'fudge-html-plan'):
            with self.subTest(name=name):
                legacy = self.skills / name
                legacy.mkdir()
                (legacy / '.fudge-installer').write_text(str(self.repo) + '\n')
                self.run_install('-a', 'codex', '--skill', name, '--copy', '-y')
                self.assertFalse(legacy.exists())
                self.assertTrue((self.skills / 'fudge-plan/SKILL.md').is_file())
                self.run_install('remove', '-a', 'codex', '--root', name, '-y')
                self.assertFalse((self.skills / 'fudge-plan').exists())
                legacy.mkdir()
                (legacy / '.fudge-installer').write_text(str(self.repo) + '\n')
                self.run_install('remove', '-a', 'codex', '--root', 'plan', '-y')
                self.assertFalse(legacy.exists())

    def test_copy_update(self):
        self.run_install('-a', 'codex', '--root', 'setup', '--copy', '-y')
        installed = self.skills / 'fudge-setup'
        self.assertFalse(installed.is_symlink())
        (self.repo / 'fudge-setup/SKILL.md').write_text((self.repo / 'fudge-setup/SKILL.md').read_text() + '\nUpdate fixture.\n')
        self.run_install('-a', 'codex', '--root', 'setup', '--copy', '-y')
        self.assertIn('Update fixture.', (installed / 'SKILL.md').read_text())
    def test_migration_preserves_foreign_entries(self):
        self.skills.mkdir(parents=True)
        (self.skills / 'fudge-conventions').symlink_to(self.repo / 'fudge-conventions')
        old = self.skills / 'fudge-mindmap'
        old.mkdir()
        (old / '.fudge-installer').write_text(str(self.repo) + '\n')
        foreign = self.skills / 'fudge-ui-mock'
        foreign.mkdir()
        (foreign / 'manual.txt').write_text('keep')
        legacy_design = self.skills / 'fudge-design-system'
        legacy_design.symlink_to(self.repo / 'fudge-design-system')
        dangling = self.skills / 'fudge-delegate'
        dangling.symlink_to(self.base / 'unrelated-missing')
        self.run_install('-a', 'codex', '--root', 'conventions', '-y')
        self.assertFalse((self.skills / 'fudge-conventions').is_symlink())
        self.assertFalse(old.exists())
        self.assertEqual((foreign / 'manual.txt').read_text(), 'keep')
        self.assertTrue(dangling.is_symlink())
        self.assertTrue(legacy_design.is_symlink())
        result = self.run_install('-a', 'codex', '--root', 'design')
        self.assertIn(str(legacy_design), result.stdout)
        self.assertFalse(legacy_design.is_symlink())
        self.run_install('remove', '-a', 'codex', '--all', '-y')
        self.assertTrue(foreign.exists())
        self.assertTrue(dangling.is_symlink())
    def test_cleanup_is_scoped_to_selected_owner(self):
        self.skills.mkdir(parents=True)
        legacy = self.skills / 'fudge-ui-mock'
        legacy.symlink_to(self.repo / 'fudge-ui-mock')
        result = self.run_install('-a', 'codex', '--root', 'setup')
        self.assertTrue(legacy.is_symlink())
        self.assertNotIn(str(legacy), result.stdout)
        result = self.run_install('-a', 'codex', '--root', 'design')
        self.assertFalse(legacy.is_symlink())
        self.assertIn('Retired entries to remove:', result.stdout)
        self.assertIn(str(legacy), result.stdout)
    def test_nonterminal_remove_requires_yes(self):
        self.run_install('-a', 'codex', '--root', 'setup')
        self.run_install('remove', '-a', 'codex', '--all', success=False)
        self.assertTrue((self.skills / 'fudge-setup').is_symlink())
    def test_foreign_selected_root_is_protected(self):
        self.skills.mkdir(parents=True)
        foreign = self.skills / 'fudge-setup'
        foreign.symlink_to(self.base / 'missing')
        self.run_install('-a', 'codex', '--root', 'setup', '-y', success=False)
        self.assertTrue(foreign.is_symlink())
    def test_legacy_selection_and_removed_skill(self):
        self.run_install('-a', 'codex', '--no-roots', '--skill', 'ui-mock', '-y')
        self.assertEqual([p.name for p in self.skills.iterdir()], ['fudge-design'])
        result = self.run_install('-a', 'codex', '--skill', 'mindmap', '-y', success=False)
        self.assertIn('removed', result.stderr)
    def test_system_decomposition_migrates_into_ship(self):
        self.skills.mkdir(parents=True)
        legacy = self.skills / 'fudge-system-decomposition'
        legacy.symlink_to(self.repo / 'fudge-system-decomposition')
        self.run_install('-a', 'codex', '--root', 'setup', '-y')
        self.assertTrue(legacy.is_symlink())
        self.run_install('-a', 'codex', '--skill', 'system-decomposition', '-y')
        self.assertFalse(legacy.is_symlink())
        module = self.skills / 'fudge-ship/references/modules/system-decomposition'
        self.assertTrue((module / 'guide.md').is_file())
        self.assertTrue((module / 'references/lenses.md').is_file())
        self.assertFalse((module / 'SKILL.md').exists())
    def test_bad_navigation_and_unmarked_build_are_rejected(self):
        source = self.repo / 'fudge-setup/SKILL.md'
        source.write_text(source.read_text() + '\nRead `references/modules/missing/guide.md`.\n')
        self.run_install('-a', 'codex', '--root', 'setup', '-y', success=False)
        self.assertFalse(self.skills.exists())
        source.write_text(source.read_text().replace('\nRead `references/modules/missing/guide.md`.\n', ''))
        package = self.repo / '.fudge-build/fudge-setup'
        package.mkdir(parents=True)
        (package / 'manual.txt').write_text('keep')
        self.run_install('-a', 'codex', '--root', 'setup', '-y', success=False)
        self.assertEqual((package / 'manual.txt').read_text(), 'keep')

if __name__ == '__main__':
    unittest.main()
