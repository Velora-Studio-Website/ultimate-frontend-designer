"""Regression probes for the embedded evidence record utility, using disposable files."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ui_craft_review',
    ROOT / 'skills/ultimate-frontend-designer/extensions/ui-craft/scripts/review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / 'observed.txt'
        self.file.write_text('revision 1', encoding='utf-8')
        self.context = dict(revision='r1', target='fixture', method='unit-probe',
                            state='default', viewport='360x800', expected='same file', actual='same file')
        self.data = dict(schemaVersion=1, scope='review', revision='r1', findings=[],
            checks=[dict(id=n, required=True, status='pass', note='fixture only',
                         context=self.context.copy(), evidence=[review.evidence(self.root, self.file)])
                    for n in review.SCOPES['review']])

    def test_control_and_changed_evidence(self):
        self.assertEqual(review.validate(self.data, self.root), [])
        self.file.write_text('revision 2', encoding='utf-8')
        self.assertTrue(review.validate(self.data, self.root))

    def test_duplicate_keys_and_boolean_version(self):
        path = self.root / 'ambiguous.json'
        path.write_text('{"status":"fail","status":"pass"}', encoding='utf-8')
        with self.assertRaises(ValueError):
            review.read(path)
        self.data['schemaVersion'] = True
        self.assertTrue(review.validate(self.data, self.root))

    def test_visual_cannot_be_excluded(self):
        self.data['checks'][0].update(status='not_applicable', scope_basis='out of scope')
        self.assertTrue(review.validate(self.data, self.root))

    def test_revision_and_missing_scope_check(self):
        self.data['checks'][0]['context']['revision'] = 'r0'
        self.assertTrue(review.validate(self.data, self.root))
        self.data['checks'].pop()
        self.assertTrue(review.validate(self.data, self.root))

    def test_retained_nonblocking_finding_evidence_is_checked(self):
        self.data['findings'] = [dict(id='f1', blocking=False, status='resolved',
            description='spacing', recheck_evidence=[dict(path='observed.txt', sha256='wrong')])]
        self.assertTrue(review.validate(self.data, self.root))

    def test_scope_escape_is_rejected(self):
        with tempfile.NamedTemporaryFile() as outside:
            with self.assertRaises(ValueError):
                review.evidence(self.root, Path(outside.name))

    def test_unresolved_blocker_prevents_acceptance(self):
        self.data['findings'] = [dict(id='f1', blocking=True, status='open', description='broken focus')]
        self.assertTrue(review.validate(self.data, self.root))


if __name__ == '__main__':
    unittest.main()
