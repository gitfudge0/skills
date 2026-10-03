#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HELPER = Path(__file__).resolve().parent.parent / 'shared/artifact_path.py'

class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.repo.mkdir()
    def tearDown(self):
        self.temp.cleanup()
    def git(self, *args, cwd=None):
        return subprocess.run(['git', '-C', str(cwd or self.repo), *args], capture_output=True, text=True, check=True).stdout.strip()
    def init_git(self):
        self.git('init', '-q')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test', 'commit', '--allow-empty', '-qm', 'fixture')
    def resolve(self, *args, cwd=None, success=True):
        result = subprocess.run(['python3', str(HELPER), '--cwd', str(cwd or self.repo), '--skill', 'ship', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return json.loads(result.stdout) if success else result
    def test_branch_identity_and_unique_reservation(self):
        self.init_git()
        first = self.resolve('--branch', 'feature/a', '--name', 'test', '--mkdir')
        second = self.resolve('--branch', 'feature-a', '--name', 'test', '--mkdir')
        third = self.resolve('--branch', 'feature/a', '--name', 'test', '--mkdir')
        self.assertNotEqual(first['path'], second['path'])
        self.assertEqual(Path(third['path']).name, 'test-2')
        self.assertTrue(Path(first['path']).is_dir())
    def test_explicit_exact_destination_and_existing_refusal(self):
        destination = self.repo / 'requested'
        result = self.resolve('--output', 'requested', '--mkdir')
        self.assertEqual(result['path'], str(destination))
        self.assertFalse(result['default'])
        self.resolve('--output', 'requested', '--mkdir', success=False)
        self.assertTrue(destination.is_dir())
    def test_explicit_dangling_link_refused(self):
        destination = self.repo / 'requested'
        target = self.base / 'missing-target'
        destination.symlink_to(target)
        self.resolve('--output', str(destination), '--mkdir', success=False)
        self.assertTrue(destination.is_symlink())
        self.assertFalse(target.exists())
    def test_non_git_default(self):
        result = self.resolve('--name', 'check', '--mkdir', '--exclude')
        self.assertEqual(result['path'], str(self.repo / '.fudge/ship/check'))
        self.assertFalse(result['git'])
        self.assertFalse((self.repo / '.git').exists())
    def test_worktree_and_external_exclusion(self):
        self.init_git()
        worktree = self.base / 'worktree'
        self.git('worktree', 'add', '-qb', 'fixture-worktree', str(worktree))
        self.assertTrue((worktree / '.git').is_file())
        nested = worktree / 'nested'
        nested.mkdir()
        result = self.resolve('--mkdir', '--exclude', cwd=nested)
        self.assertEqual(result['root'], str(worktree))
        self.assertTrue(Path(result['path']).is_relative_to(worktree))
        exclude = Path(self.git('rev-parse', '--git-path', 'info/exclude', cwd=worktree))
        if not exclude.is_absolute():
            exclude = worktree / exclude
        self.assertIn('.fudge/', exclude.read_text().splitlines())
        before = exclude.read_text()
        external = self.base / 'external'
        self.resolve('--output', str(external), '--mkdir', '--exclude', cwd=nested)
        self.assertEqual(exclude.read_text(), before)
        self.assertFalse((worktree / '.gitignore').exists())

if __name__ == '__main__':
    unittest.main()
