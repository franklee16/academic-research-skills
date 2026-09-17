import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_bar_benchmark as runner


class BarBenchmarkTests(unittest.TestCase):
    def test_writes_complete_evidence_for_all_candidate_variants(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "bar_benchmark_report.json").read_text(encoding="utf-8")
            )

            self.assertEqual(stored, report)
            self.assertEqual(report["status"], "passed")
            self.assertEqual(len(report["variants"]), 6)
            successes = [
                variant
                for variant in report["variants"]
                if variant["expected_status"] != "low_confidence"
            ]
            for variant in successes:
                self.assertEqual(variant["metrics"]["coverage"], 1.0)
                self.assertEqual(variant["metrics"]["precision"], 1.0)
                self.assertLessEqual(variant["metrics"]["mae"], 0.25)
                self.assertTrue((output_dir / variant["overlay"]).is_file())
                self.assertTrue((output_dir / variant["recreation"]).is_file())

            lowres = next(
                variant
                for variant in report["variants"]
                if variant["name"] == "grouped_vertical_lowres_jpeg"
            )
            self.assertEqual(lowres["status"], "partial_visible")
            self.assertGreaterEqual(lowres["metrics"]["error_bar_coverage"], 0.75)
            self.assertLessEqual(lowres["metrics"]["error_endpoint_max_px"], 3.0)

            ambiguous = next(
                variant
                for variant in report["variants"]
                if variant["expected_status"] == "low_confidence"
            )
            self.assertEqual(ambiguous["benchmark_status"], "rejected_as_expected")
            self.assertTrue(
                all(mark.get("value") is None for mark in ambiguous["extraction"]["marks"])
            )

            with (output_dir / "bar_benchmark_results.csv").open(
                encoding="utf-8", newline=""
            ) as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(
                len(rows),
                sum(len(variant["extraction"]["marks"]) for variant in report["variants"]),
            )
            self.assertTrue(all(row["image_hash_sha256"] for row in rows))
            self.assertTrue(all(row["plot_bounds"] for row in rows))

    def test_refuses_to_overwrite_a_nonempty_evidence_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            sentinel = output_dir / "keep.txt"
            sentinel.write_text("do not overwrite", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "refusing to overwrite"):
                runner.run_benchmark(output_dir)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "do not overwrite")
            self.assertEqual(list(output_dir.iterdir()), [sentinel])

    def test_failure_evidence_is_persisted_before_quality_assertion(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(runner, "_failure_reason", return_value="forced failure"):
                with self.assertRaisesRegex(AssertionError, "forced failure"):
                    runner.run_benchmark(output_dir)

            report_path = output_dir / "bar_benchmark_report.json"
            csv_path = output_dir / "bar_benchmark_results.csv"
            self.assertTrue(report_path.is_file())
            self.assertTrue(csv_path.is_file())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "failed")
            self.assertTrue(all(variant["benchmark_status"] == "failed" for variant in report["variants"]))

    def test_ambiguous_gate_rejects_a_numeric_value(self):
        variant = {
            "name": "unsafe-ambiguous",
            "status": "low_confidence",
            "expected_status": "low_confidence",
            "extraction": {"marks": [{"value": 4.0}]},
        }

        self.assertIn("emitted a value", runner._failure_reason(variant))


if __name__ == "__main__":
    unittest.main()
