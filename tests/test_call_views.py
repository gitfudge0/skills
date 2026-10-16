"""Exercise the dependency-free call-tree runtime through Node."""
from pathlib import Path
import shutil
import subprocess
import unittest


class CallViewsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'Node.js is required')
    def test_call_views(self):
        result = subprocess.run(['node', str(Path(__file__).with_name('call_views.cjs'))],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
