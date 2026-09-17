import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_histogram_benchmark as runner


class HistogramBenchmarkTests(unittest.TestCase):
    def test_writes_complete_report_for_all_histogram_variants(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "histogram_benchmark_report.json").read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(stored, report)
            self.assertEqual(report["family"], "histogram")
            self.assertEqual(len(report["variants"]), 3)
            for variant in report["variants"]:
                self.assertEqual(variant["coverage"], 1.0)
                self.assertLessEqual(variant["mae"], 0.25)
                self.assertTrue((output_dir / variant["overlay"]).is_file())

    def test_alignment_records_an_extra_in_plot_prediction(self):
        def bin_at(center, height):
            return {
                "x_left": center - 0.41,
                "x_right": center + 0.41,
                "height": height,
                "left_pixel": 10.0,
                "right_pixel": 20.0,
                "top_pixel": 30.0,
                "bottom_pixel": 40.0,
                "pixel_area": 100.0,
            }

        bins = [bin_at(center, height) for center, height in enumerate([3, 8, 5, 11, 6])]
        bins.append(bin_at(4, 9))

        alignment = runner._align_bins_by_center(bins)

        self.assertEqual(alignment["expected_bin_count"], 5)
        self.assertEqual(alignment["extracted_bin_count"], 6)
        self.assertEqual(alignment["matched_bin_count"], 5)
        self.assertEqual(alignment["unmatched_prediction_count"], 1)
        self.assertEqual(alignment["missing_truth_count"], 0)
        self.assertEqual(alignment["coverage"], 1.0)
        self.assertEqual(alignment["precision"], 5 / 6)

    def test_quality_gate_rejects_unmatched_prediction_at_low_mae(self):
        variant = {
            "name": "extra-bin.png",
            "coverage": 1.0,
            "mae": 0.1,
            "unmatched_prediction_count": 1,
            "missing_truth_count": 0,
        }

        with self.assertRaisesRegex(AssertionError, "unmatched prediction"):
            runner._assert_quality([variant])

    def test_writes_failure_evidence_before_raising_for_empty_extractions(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(runner, "extract_histogram", return_value=[]):
                with self.assertRaisesRegex(AssertionError, "coverage .* below 1.0"):
                    runner.run_benchmark(output_dir)

            report_path = output_dir / "histogram_benchmark_report.json"
            csv_path = output_dir / "histogram_benchmark_results.csv"
            self.assertTrue(report_path.is_file())
            self.assertTrue(csv_path.is_file())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "failed")
            self.assertIn("failure_reason", report)
            for variant in report["variants"]:
                self.assertEqual(variant["status"], "failed")
                self.assertEqual(variant["extracted_bin_count"], 0)
                self.assertEqual(variant["matched_bin_count"], 0)
                self.assertEqual(variant["unmatched_prediction_count"], 0)
                self.assertEqual(variant["missing_truth_count"], 5)

            with csv_path.open(encoding="utf-8", newline="") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(row["bin_x_left"] == "" for row in rows))
            self.assertTrue(all(row["status"] == "failed" for row in rows))

    def test_successful_report_records_calibration_and_bins_in_long_form_csv(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)

            expected_keys = {
                "raster_dimensions",
                "plot_bounds",
                "x_axis",
                "y_axis",
                "bar_color",
                "tolerance",
                "min_area",
                "bins",
            }
            self.assertTrue(
                all(expected_keys.issubset(variant) for variant in report["variants"])
            )
            self.assertTrue(all(variant["bins"] for variant in report["variants"]))

            with (output_dir / "histogram_benchmark_results.csv").open(
                encoding="utf-8", newline=""
            ) as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(
                len(rows), sum(len(variant["bins"]) for variant in report["variants"])
            )
            self.assertTrue(all(row["bin_x_left"] for row in rows))
            self.assertTrue(all(row["plot_bounds"] for row in rows))
            self.assertTrue(all(row["status"] == "passed" for row in rows))


if __name__ == "__main__":
    unittest.main()
