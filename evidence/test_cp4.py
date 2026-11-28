"""Offline checks for provenance, denominators and impact; mutate only temp copies."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import verify


class CP4EvidenceTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        self.folder = self.root / 'evidence/cp4'
        shutil.copytree(verify.E / 'cp4', self.folder)
        manifest = json.loads((self.folder / 'cp3-snapshot.json').read_text(encoding='utf-8'))
        for relative in manifest['files']:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(verify.ROOT / relative, target)

    def change(self, name, mutate):
        path = self.folder / name
        value = json.loads(path.read_text(encoding='utf-8'))
        mutate(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def test_saved_evidence_and_base_impact_validate(self):
        result = verify.validate_cp4(self.root)
        self.assertEqual(result['cp3_snapshot_files_unchanged'], 10)
        self.assertEqual(result['supplemental_counts']['user_posts'], 4)
        self.assertEqual(result['human_confirmed_count'], 0)
        self.assertEqual(result['base_sessions_per_month_estimated'], 36)
        self.assertEqual(result['base_loss_minutes_estimated'], 540)

    def test_changing_a_frozen_snapshot_is_rejected(self):
        path = self.root / 'evidence/public-reviews/reviews.csv'
        path.write_bytes(path.read_bytes().replace(b'RV001', b'RV999', 1))
        with self.assertRaisesRegex(AssertionError, 'snapshot changed'):
            verify.validate_cp4(self.root)

    def test_excerpt_change_without_updated_provenance_is_rejected(self):
        self.change('supplemental-sources.json', lambda value: value['records'][0].update(excerpt='Changed quote.'))
        with self.assertRaises(AssertionError):
            verify.validate_cp4(self.root)

    def test_publisher_reports_cannot_inflate_the_user_post_denominator(self):
        self.change('supplemental-sources.json', lambda value: value['counts'].update(user_posts=6))
        with self.assertRaisesRegex(AssertionError, 'denominators'):
            verify.validate_cp4(self.root)

    def test_human_count_requires_row_level_records(self):
        self.change('label-audit.json', lambda value: value.update(human_confirmed_count=150))
        with self.assertRaisesRegex(AssertionError, 'Human count'):
            verify.validate_cp4(self.root)

    def test_total_customers_cannot_replace_assistant_users(self):
        self.change('cost-handoff.json', lambda value: value['users'].update(base=100))
        with self.assertRaises(AssertionError):
            verify.validate_cp4(self.root)

    def test_wrong_turn_weighting_and_unsupported_savings_are_rejected(self):
        for change in ({'turns_per_assistant_user_month': 1.8}, {'observed_savings_minutes': 540}):
            with self.subTest(change=change):
                path = self.folder / 'cost-handoff.json'
                original = path.read_bytes()
                self.change(path.name, lambda value: value.update(change))
                with self.assertRaises(AssertionError):
                    verify.validate_cp4(self.root)
                path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
