"""Portable report examples retain contracts while sharing the plan runtime."""
import re
import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportExamplesTests(unittest.TestCase):
    def test_examples_pack_canonical_runtime_without_external_assets(self):
        for module in ('test-plan', 'decision-room'):
            with self.subTest(module=module), tempfile.TemporaryDirectory() as temp:
                source = ROOT / 'modules' / module / 'assets/example.src.html'
                text = source.read_text()
                self.assertIn('<doc-plan', text)
                self.assertNotIn('<doc-ask', text)
                output = Path(temp) / 'report.html'
                subprocess.run(['node', str(ROOT / 'plan/runtime/pack.mjs'), str(source), '-o', str(output)], check=True, capture_output=True)
                packed = output.read_text()
                self.assertIn((ROOT / 'plan/runtime/htmlplan.css').read_text().strip(), packed)
                self.assertIn((ROOT / 'plan/runtime/htmlplan.js').read_text().strip(), packed)
                self.assertNotRegex(packed, r'<(?:link|script)\b[^>]*(?:href|src)=')
                content = text[text.index('<doc-plan'):text.index('</doc-plan>') + len('</doc-plan>')]
                self.assertIn(content, packed)
                self.assertEqual(re.findall(r'<doc-claim\b[^>]*\bid="([^"]+)"', text), re.findall(r'<doc-claim\b[^>]*\bid="([^"]+)"', packed))

    def test_installed_packer_resolves_assets_without_source_tree(self):
        for module in ('test-plan', 'decision-room'):
            with self.subTest(module=module), tempfile.TemporaryDirectory() as temp:
                package = Path(temp)
                runtime = package / 'shared/report-deck/runtime'
                runtime.mkdir(parents=True)
                for name in ('htmlplan.css', 'htmlplan.js', 'pack.mjs'):
                    shutil.copyfile(ROOT / 'plan/runtime' / name, runtime / name)
                source = package / 'references/modules' / module / 'assets/example.src.html'
                source.parent.mkdir(parents=True)
                shutil.copyfile(ROOT / 'modules' / module / 'assets/example.src.html', source)
                output = package / 'portable.html'
                subprocess.run(['node', str(runtime / 'pack.mjs'), str(source), '-o', str(output)], check=True, capture_output=True)
                self.assertIn((runtime / 'htmlplan.css').read_text().strip(), output.read_text())
                self.assertIn((runtime / 'htmlplan.js').read_text().strip(), output.read_text())

    def test_case_results_and_limits_survive_packing(self):
        source = ROOT / 'modules/test-plan/assets/example.src.html'
        packed = ROOT / 'modules/test-plan/assets/example.html'
        for path in (source, packed):
            text = path.read_text()
            cases = re.findall(r'<doc-claim id="((?:R|U|I|E)\d+)">(.*?)</doc-claim>', text, re.S)
            self.assertEqual({key for key, _ in cases}, {'R1', 'R2', 'R3', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'I1', 'E1', 'E2', 'E3'})
            rows = dict(cases)
            self.assertIn('FAIL', rows['U2'])
            for case in ('E1', 'E2', 'E3'):
                self.assertIn('NOT RUN', rows[case])
                self.assertRegex(rows[case], r'NOT RUN — .+?</dd>')
            for _, content in cases:
                for field in ('Priority', 'Scenario', 'Expected', 'Execution', 'Evidence'):
                    self.assertIn(field, content)
            self.assertIn('id="gaps"', text)
            self.assertIn('id="out-of-scope"', text)
            self.assertIn('Fictional', text)

    def test_decision_recommendation_precedes_simulation(self):
        for name in ('example.src.html', 'example.html'):
            text = (ROOT / 'modules/decision-room/assets' / name).read_text()
            self.assertLess(text.index('id="recommendation"'), text.index('id="perspectives"'))
            for key in ('risks', 'conditions', 'out-of-scope', 'evidence'):
                self.assertIn(f'id="{key}"', text)
            self.assertIn('simulated', text.lower())
            self.assertIn('assumption', text.lower())


if __name__ == '__main__':
    unittest.main()
