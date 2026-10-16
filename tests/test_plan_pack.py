"""Exercise plan guidance warnings through the public packer CLI."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PACK = Path(__file__).resolve().parents[1] / 'plan/runtime/pack.mjs'


@unittest.skipUnless(shutil.which('node'), 'Node.js is required')
class PlanPackTests(unittest.TestCase):
    def lint(self, prose='', decisions=0, title='Scheduling Messages in PostBox'):
        asks = ''.join(f'<doc-ask id="q{i}"><p>Keep this choice?</p><label><input type="radio" name="q{i}" value="yes" checked>Yes</label></doc-ask>' for i in range(decisions))
        page = f'<!doctype html><html><meta charset="utf-8"><link rel="stylesheet" href="htmlplan.css"><script src="htmlplan.js" defer></script><title>Message Plan</title><body><h1>{title}</h1><main><doc-plan><doc-claim><p>{prose or "Users can schedule messages."}</p><doc-mock frame="none" w="440"><template>Schedule</template></doc-mock>{asks}</doc-claim><doc-claim aux="scope"><p>Normal sending stays unchanged.</p><ul><li>Normal send</li></ul></doc-claim></doc-plan></main></body></html>'
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'plan.html'
            source.write_text(page)
            result = subprocess.run(['node', str(PACK), str(source), '--lint-only'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_decision_warning_starts_at_six(self):
        for count in (0, 1, 5):
            with self.subTest(count=count):
                self.assertNotIn('decisions —', self.lint(decisions=count))
        self.assertIn('6 decisions —', self.lint(decisions=6))

    def test_uncertainty_and_recommendation_are_not_rewritten(self):
        output = self.lint('The user might retry. The app should retain input. It may fail.')
        self.assertNotIn('ASD-STE100', output)
        self.assertNotIn('"might" → "can"', output)
        self.assertNotIn('"should" → "must"', output)

    def test_title_budget_matches_guidance(self):
        for title in ('Messages', 'Scheduling All Delayed Messages in the PostBox Client'):
            with self.subTest(title=title):
                self.assertIn('3 to 7 words', self.lint(title=title))

    def test_plain_language_advice_remains_available_for_prose(self):
        self.assertIn('Plain language: consider "utilize"', self.lint('Users utilize the calendar.'))

    def test_quoted_and_code_text_do_not_trigger_plain_language_advice(self):
        output = self.lint('<doc-quote>We utilize the system.</doc-quote><code>utilize()</code>')
        self.assertNotIn('"utilize"', output)


if __name__ == '__main__':
    unittest.main()
