import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import run_scatter_benchmark as runner
except ImportError:  # pragma: no cover - package-style unittest invocation
    from . import run_scatter_benchmark as runner


class ScatterBenchmarkTests(unittest.TestCase):
    def test_writes_complete_evidence_and_passes_supported_variants(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "scatter_benchmark_report.json").read_text(encoding="utf-8")
            )

            self.assertEqual(stored, report)
            self.assertEqual(report["status"], "passed")
            self.assertGreaterEqual(len(report["variants"]), 5)
            supported = [
                variant
                for variant in report["variants"]
                if variant["expected_status"] == "candidate"
            ]
            for variant in supported:
                self.assertEqual(variant["status"], "passed")
                self.assertEqual(variant["metrics"]["precision"], 1.0)
                self.assertEqual(variant["metrics"]["recall"], 1.0)
                self.assertEqual(variant["metrics"]["f1"], 1.0)
                self.assertLessEqual(
                    variant["metrics"]["max_center_error_pixels"],
                    variant["center_error_limit_pixels"],
                )
                self.assertTrue((output_dir / variant["overlay"]).is_file())

            rejected = next(
                variant
                for variant in report["variants"]
                if variant["expected_status"] == "low_confidence"
            )
            self.assertEqual(rejected["status"], "rejected_as_expected")
            self.assertFalse(rejected["extraction"]["numeric_output_authorized"])
            self.assertEqual(rejected["extraction"]["points"], [])

            residual = next(
                variant
                for variant in report["variants"]
                if variant["expected_status"] == "low_confidence_residual"
            )
            self.assertEqual(residual["status"], "rejected_as_expected")
            self.assertFalse(residual["extraction"]["numeric_output_authorized"])
            self.assertEqual(
                residual["extraction"]["residual_audit"]["residual_candidate_count"],
                1,
            )

            with (output_dir / "scatter_benchmark_results.csv").open(
                encoding="utf-8", newline=""
            ) as source:
                rows = list(csv.DictReader(source))
            self.assertTrue(rows)
            self.assertTrue(all(row["image_sha256"] for row in rows))

    def test_refuses_to_overwrite_nonempty_evidence_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            sentinel = output_dir / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "refusing to overwrite"):
                runner.run_benchmark(output_dir)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_persists_evidence_before_quality_assertion(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(runner, "_failure_reason", return_value="forced failure"):
                with self.assertRaisesRegex(AssertionError, "forced failure"):
                    runner.run_benchmark(output_dir)
            report = json.loads(
                (output_dir / "scatter_benchmark_report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(report["status"], "failed")
            self.assertTrue((output_dir / "scatter_benchmark_results.csv").is_file())


if __name__ == "__main__":
    unittest.main()
