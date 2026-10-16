import json
from html.parser import HTMLParser
import pathlib
import re
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'modules/gap-analysis/assets/report-template.html'


class ReportRows(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.rows = []
        self.cells = None
        self.cell = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.cells = []
        elif tag == 'td':
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'td':
            self.cells.append(' '.join(' '.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr':
            self.rows.append(self.cells)
            self.cells = None

    def row(self, identifier):
        return next(row for row in self.rows if row and row[0] == identifier)


def render(answers=None, gap_status="open", gap_fields=None):
    data = {'meta': {}, 'register': [{'id': 'GAP-1', 'claim': 'Missing contract', 'status': gap_status}],
            'questions': [{'id': 'Q-1', 'answerer': 'Vendor', 'question': 'Import supported?',
                           'links': ['GAP-1'], 'status': 'answered' if answers else 'open'}]}
    data['register'][0].update(gap_fields or {})
    data['register'].append({'id': 'GAP-2', 'claim': 'Unrelated resolved gap', 'status': 'closed'})
    if answers is not None:
        data['answers'] = answers
    script = re.search(r'<script>([\s\S]*?)</script>', TEMPLATE.read_text()).group(1)
    script = script.replace('__GAP_ANALYSIS_DATA__', json.dumps(data).replace('<', r'\u003c'))
    harness = "const nodes={};global.document={getElementById:id=>nodes[id]||(nodes[id]={})};\n"
    result = subprocess.run(['node', '-e', harness + script + '\nconsole.log(JSON.stringify(nodes));'],
                            text=True, capture_output=True, check=True)
    return json.loads(result.stdout)['app']['innerHTML']


class GapReportTests(unittest.TestCase):
    def test_native_runtime_packs_without_external_assets(self):
        source = TEMPLATE.read_text()
        self.assertIn('<doc-plan id="app"', source)
        self.assertIn('doc-claim id=', source)
        self.assertNotIn('<nav>', source)
        self.assertIn('htmlplan.js" defer', source)
        self.assertLess(source.index('htmlplan.js" defer'), source.index('const DATA'))
        payload = {'meta': {'project': '</script><img src=x>'}}
        source = source.replace('__GAP_ANALYSIS_DATA__',
                                json.dumps(payload).replace('<', r'\u003c'))
        source = source.replace('../../../plan/runtime/', str(ROOT / 'plan/runtime') + '/')
        with tempfile.TemporaryDirectory() as directory:
            src = pathlib.Path(directory) / 'gap.src.html'
            packed = pathlib.Path(directory) / 'gap.html'
            src.write_text(source)
            result = subprocess.run(['node', str(ROOT / 'plan/runtime/pack.mjs'), str(src),
                                     '-o', str(packed), '--artifact'],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html = packed.read_text()
            self.assertIn('data-htmlplan', html)
            self.assertNotRegex(html, r'<script[^>]+src=')
            self.assertNotRegex(html, r'<link[^>]+href=')
            self.assertIn(r'\u003c/script>', html)

    def test_closed_and_accepted_gaps_are_not_counted_as_open(self):
        for status in ["closed", "accepted"]:
            with self.subTest(status=status):
                self.assertIn("0 open items", render(gap_status=status))

    def test_machine_resolution_keeps_human_disposition_visible(self):
        html = render(gap_status="accepted", gap_fields={"basis_state": "changed",
                      "resolution": "proposed", "resolution_evidence": ["check:<contract>"]})
        for value in ["accepted", "basis changed", "resolution proposed", "check:&lt;contract&gt;"]:
            self.assertIn(value, html)

    def test_missing_answer_does_not_invent_one(self):
        html = render()
        self.assertIn('Import supported?', html)
        self.assertNotIn('Answer received', html)

    def test_answer_is_attributed_and_rendered_at_gap_and_question(self):
        html = render([{'id': 'Q-1', 'answer': 'Supported via SDK', 'answered_by': 'Vendor lead',
                        'date': '2026-10-16', 'evidence': ['sdk:p.3'], 'assessment': 'supported'}])
        self.assert_open_answer(html, ['Supported via SDK', 'Vendor lead', '2026-10-16',
                                       'sdk:p.3', 'supported'])

        # A closed target must fail even when report text still mentions open items.
        closed = html.replace('<span class="pill ">open</span>',
                              '<span class="pill ">closed</span>')
        with self.assertRaises(AssertionError):
            self.assert_open_answer(closed, ['Supported via SDK'])

        # Duplicate question evidence cannot conceal missing evidence at the gap.
        missing = re.sub(r'<tr\b[^>]*>[\s\S]*?</tr>',
                         lambda match: match[0].replace('Supported via SDK', '')
                         if '<span class="ref">GAP-1</span>' in match[0]
                         else match[0].replace('Supported via SDK',
                                               'Supported via SDK Supported via SDK'), html)
        self.assertEqual(missing.count('Supported via SDK'), 2)
        with self.assertRaises(AssertionError):
            self.assert_open_answer(missing, ['Supported via SDK'])

    def assert_open_answer(self, html, evidence):
        rows = ReportRows(html)
        gap = rows.row('GAP-1')
        self.assertEqual(gap[-1], 'unassigned open')
        self.assertEqual(rows.row('GAP-2')[-1], 'unassigned closed')
        for identifier in ['GAP-1', 'Q-1']:
            for value in evidence:
                self.assertIn(value, ' '.join(rows.row(identifier)), identifier)

    def test_conflicting_answer_stays_visible_and_escapes_markup(self):
        html = render([{'id': 'Q-1', 'answer': '<img src=x onerror=alert(1)>',
                        'answered_by': '<Vendor>', 'date': '2026-10-16',
                        'evidence': ['<sdk>'], 'assessment': 'conflicting',
                        'assessment_basis': 'Conflicts with signed agreement'}])
        self.assertIn('conflicting', html)
        self.assertIn('Conflicts with signed agreement', html)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', html)
        self.assertIn('&lt;Vendor&gt;', html)
        self.assertIn('&lt;sdk&gt;', html)
        self.assertNotIn('<img src=x', html)
        self.assert_open_answer(html, ['<img src=x onerror=alert(1)>', '<Vendor>',
                                       '2026-10-16', '<sdk>', 'conflicting',
                                       'Conflicts with signed agreement'])


if __name__ == '__main__':
    unittest.main()
