#!/usr/bin/env python3
"""Keyboard wizard tests use a fake curses surface, never a user's skill home."""
import curses
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('install_ui', Path(__file__).resolve().parent.parent / 'scripts/install_ui.py')
UI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UI)

class Screen:
    def __init__(self, keys):
        self.keys = iter(keys)
        self.lines = []
    def keypad(self, enabled):
        pass
    def erase(self):
        pass
    def getmaxyx(self):
        return 30, 100
    def addnstr(self, row, col, text, width, attrs):
        self.lines.append(text[:width])
    def refresh(self):
        pass
    def getch(self):
        return next(self.keys)

class WizardTests(unittest.TestCase):
    def run_wizard(self, keys, retired=None, conflict=False):
        screen = Screen(keys)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            if conflict:
                (target / 'fudge-setup').mkdir()
            with patch.object(UI.curses, 'wrapper', side_effect=lambda action: action(screen)), patch.object(UI.curses, 'curs_set'):
                result = UI.choose(['codex', 'claude'], ['setup', 'design'], ['codex'], ['setup'], False, lambda agent: target, lambda path: False, retired or (lambda target, roots: []))
            return result, screen.lines
    def test_cancel_with_q_and_escape(self):
        self.assertIsNone(self.run_wizard([ord('q')])[0])
        self.assertIsNone(self.run_wizard([27])[0])
    def test_back_preserves_selections(self):
        result, lines = self.run_wizard([10, curses.KEY_DOWN, ord(' '), 27, 10, 10, curses.KEY_DOWN, ord(' '), 10, 10])
        self.assertEqual(result, (['codex'], ['setup', 'design'], True))
        self.assertIn('[x] design', lines)
    def test_review_lists_cleanup(self):
        result, lines = self.run_wizard([10, 10, 10, 10], lambda target, roots: [target / 'fudge-conventions'])
        self.assertEqual(result, (['codex'], ['setup'], False))
        self.assertIn('Retired entries to remove:', lines)
        self.assertTrue(any('fudge-conventions' in line for line in lines))
    def test_review_blocks_foreign_conflicts(self):
        result, lines = self.run_wizard([10, 10, 10, 10, ord('q')], conflict=True)
        self.assertIsNone(result)
        self.assertIn('Resolve or deselect conflicts before installing.', lines)
    def test_html_plan_review_uses_standalone_destination(self):
        screen = Screen([10, 10, 10, 10, ord('q')])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'fudge-plan').mkdir()
            with patch.object(UI.curses, 'wrapper', side_effect=lambda action: action(screen)), patch.object(UI.curses, 'curs_set'):
                result = UI.choose(['codex'], ['plan'], ['codex'], ['plan'], False,
                    lambda agent: target, lambda path: False, package_for=lambda root: 'fudge-plan')
        self.assertIsNone(result)
        self.assertTrue(any('conflict' in line.lower() and 'fudge:plan' in line for line in screen.lines))
        self.assertIn('Resolve or deselect conflicts before installing.', screen.lines)

    def test_terminal_support_and_fallback(self):
        with patch.object(UI.sys.stdin, 'isatty', return_value=True), patch.object(UI.sys.stdout, 'isatty', return_value=True), patch.object(UI.shutil, 'get_terminal_size', return_value=os.terminal_size((100, 30))), patch.dict(os.environ, TERM='xterm-256color'):
            self.assertTrue(UI.supported())
        with patch.object(UI.shutil, 'get_terminal_size', return_value=os.terminal_size((40, 20))):
            self.assertFalse(UI.supported())

if __name__ == '__main__':
    unittest.main()
