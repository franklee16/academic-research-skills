import unittest

from extraction_contract import build_coverage_ledger


class ExtractionContractTests(unittest.TestCase):
    def test_ledger_counts_only_declared_visual_slots(self):
        ledger = build_coverage_ledger(
            [
                {
                    "category": "A",
                    "series": "x",
                    "status": "extracted",
                    "reason_code": "visible_geometry_supported",
                    "numeric_output_authorized": True,
                },
                {
                    "category": "B",
                    "series": "x",
                    "status": "not_extracted",
                    "reason_code": "occluded",
                    "numeric_output_authorized": False,
                },
            ],
            slot_fields=("category", "series"),
        )
        self.assertFalse(ledger["expected_data_count_used"])
        self.assertEqual(ledger["declared_slot_count"], 2)
        self.assertEqual(ledger["authorized_slot_count"], 1)
        self.assertEqual(ledger["coverage_fraction"], 0.5)

    def test_duplicate_slots_are_refused(self):
        record = {
            "category": "A",
            "series": "x",
            "status": "extracted",
            "reason_code": "visible_geometry_supported",
        }
        with self.assertRaisesRegex(ValueError, "duplicate coverage slot"):
            build_coverage_ledger([record, record], slot_fields=("category", "series"))

    def test_non_extracted_slot_cannot_authorize_numeric_output(self):
        with self.assertRaisesRegex(ValueError, "cannot authorize"):
            build_coverage_ledger(
                [
                    {
                        "category": "A",
                        "series": "x",
                        "status": "not_extracted",
                        "reason_code": "below_resolution",
                        "numeric_output_authorized": True,
                    }
                ],
                slot_fields=("category", "series"),
            )


if __name__ == "__main__":
    unittest.main()
