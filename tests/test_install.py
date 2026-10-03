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
        self.base = Path(self.temp.name)
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
        self.assertEqual({p.name for p in self.skills.iterdir()}, {'fudge-' + n for n in ['design', 'ux', 'ship', 'review', 'setup']})
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
