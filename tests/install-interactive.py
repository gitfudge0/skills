#!/usr/bin/env python3
"""Black-box keyboard checks for the installer's terminal picker."""

import fcntl
import os
from pathlib import Path
import pty
import re
import select
import struct
import subprocess
import tempfile
import termios
import time
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "install.sh"
ANSI = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")


class InstallerTTY:
    def __init__(self, home, args=(), columns=100):
        self.master, self.slave = pty.openpty()
        fcntl.ioctl(self.slave, termios.TIOCSWINSZ, struct.pack("HHHH", 30, columns, 0, 0))
        self.initial_termios = termios.tcgetattr(self.master)
        self.output = bytearray()
        env = os.environ.copy()
        env.update(HOME=str(home), TERM="xterm-256color")
        self.process = subprocess.Popen(
            ["bash", str(INSTALLER), *args],
            stdin=self.slave,
            stdout=self.slave,
            stderr=self.slave,
            cwd=INSTALLER.parent,
            env=env,
            start_new_session=True,
        )

    def text(self):
        return ANSI.sub("", self.output.decode("utf-8", errors="replace"))

    def read_until(self, predicate, timeout=8, since=0):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            recent = ANSI.sub("", self.output[since:].decode("utf-8", errors="replace"))
            if predicate(recent):
                return
            ready, _, _ = select.select([self.master], [], [], 0.1)
            if ready:
                try:
                    self.output.extend(os.read(self.master, 65536))
                except OSError:
                    pass
            if self.process.poll() is not None and not ready:
                break
        raise AssertionError("Installer did not reach expected screen.\n" + self.text()[-2000:])

    def send(self, keys):
        os.write(self.master, keys.encode("utf-8"))

    def mark(self):
        return len(self.output)

    def finish(self, timeout=10):
        deadline = time.monotonic() + timeout
        while self.process.poll() is None and time.monotonic() < deadline:
            ready, _, _ = select.select([self.master], [], [], 0.1)
            if ready:
                try:
                    self.output.extend(os.read(self.master, 65536))
                except OSError:
                    pass
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=2)
            raise AssertionError("Installer did not exit.\n" + self.text()[-2000:])
        code = self.process.returncode
        while select.select([self.master], [], [], 0)[0]:
            try:
                chunk = os.read(self.master, 65536)
            except OSError:
                break
            if not chunk:
                break
            self.output.extend(chunk)
        if code != 0:
            raise AssertionError(f"Installer exited {code}.\n" + self.text()[-2000:])
        if termios.tcgetattr(self.master) != self.initial_termios:
            raise AssertionError("Installer did not restore terminal settings")

    def close(self):
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=2)
        os.close(self.master)
        os.close(self.slave)


class InteractiveInstallTest(unittest.TestCase):
    def setUp(self):
        self.temp_home = tempfile.TemporaryDirectory(prefix="fudge-install-pty-")
        self.home = Path(self.temp_home.name)
        self.addCleanup(self.temp_home.cleanup)

    def start(self, *args):
        self.tty = InstallerTTY(self.home, args)
        self.addCleanup(self.tty.close)
        self.tty.read_until(
            lambda screen: "optional" in screen.lower() and "codex" in screen.lower()
        )

    def installed(self):
        skills = self.home / ".codex" / "skills"
        return {path.name for path in skills.iterdir()} if skills.exists() else set()

    def confirm(self):
        marker = self.tty.mark()
        self.tty.send("\r")  # Review the current selection on the same screen.
        self.tty.read_until(lambda screen: "Confirm installation" in screen, since=marker)
        self.tty.send("\r")  # Confirm installation.
        self.tty.finish()

    def test_defaults_install_only_three_roots(self):
        self.start()
        self.confirm()
        self.assertEqual(
            self.installed(), {"fudge-design", "fudge-ship", "fudge-review"}
        )
        for name in self.installed():
            self.assertTrue((self.home / ".codex" / "skills" / name).is_symlink())

    def test_search_and_select_one_optional_skill(self):
        self.start()
        marker = self.tty.mark()
        self.tty.send("/")
        self.tty.read_until(lambda screen: "Search optional skills" in screen, since=marker)
        marker = self.tty.mark()
        self.tty.send("ui-mock")
        self.tty.read_until(lambda screen: "ui-mock" in screen.lower(), since=marker)
        marker = self.tty.mark()
        self.tty.send("\r")  # Leave search with its filtered result focused.
        self.tty.read_until(lambda screen: "1 match" in screen.lower(), since=marker)
        marker = self.tty.mark()
        self.tty.send(" ")
        self.tty.read_until(lambda screen: "4 skill(s)" in screen.lower(), since=marker)
        self.confirm()
        self.assertEqual(
            self.installed(),
            {"fudge-design", "fudge-ship", "fudge-review", "fudge-ui-mock"},
        )

    def test_escape_cancels_and_restores_terminal(self):
        self.start()
        self.tty.send("\x1b")
        self.tty.finish()
        self.assertEqual(self.installed(), set())
        self.assertFalse((self.home / ".codex").exists())

    def test_claude_copy_preselection(self):
        self.start("-a", "claude", "--copy")
        self.confirm()
        skills = self.home / ".claude" / "skills"
        self.assertEqual(
            {path.name for path in skills.iterdir()},
            {"fudge-design", "fudge-ship", "fudge-review"},
        )
        for name in ("fudge-design", "fudge-ship", "fudge-review"):
            entry = skills / name
            self.assertTrue(entry.is_dir())
            self.assertFalse(entry.is_symlink())
            self.assertTrue((entry / ".fudge-installer").is_file())
        self.assertFalse((self.home / ".codex").exists())

    def test_wide_sections_share_a_row_and_narrow_sections_stack(self):
        def initial_rows(columns):
            tty = InstallerTTY(self.home, columns=columns)
            try:
                tty.read_until(
                    lambda screen: "AGENTS" in screen
                    and "CORE SKILLS" in screen
                    and "OPTIONAL" in screen
                )
                rows = tty.text().splitlines()
                tty.send("\x1b")
                tty.finish()
                return rows
            finally:
                tty.close()

        wide = initial_rows(100)
        narrow = initial_rows(70)
        self.assertTrue(any("AGENTS" in row and "CORE SKILLS" in row for row in wide))
        self.assertTrue(any("AGENTS" in row for row in narrow))
        self.assertTrue(any("CORE SKILLS" in row for row in narrow))
        self.assertFalse(any("AGENTS" in row and "CORE SKILLS" in row for row in narrow))


if __name__ == "__main__":
    unittest.main()
