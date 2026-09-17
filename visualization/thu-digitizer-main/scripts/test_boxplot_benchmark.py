import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_boxplot_benchmark as runner


class BoxplotBenchmarkTests(unittest.TestCase):
    def test_persists_complete_vertical_and_horizontal_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "boxplot_report.json").read_text(encoding="utf-8")
            )
            with (output_dir / "boxplot_results.csv").open(
                encoding="utf-8", newline=""
            ) as source:
                rows = list(csv.DictReader(source))
            overlay_paths = [
                (output_dir / variant["overlay"]).is_file()
                for variant in report["variants"]
            ]

        self.assertEqual(report["family"], "boxplot")
        self.assertEqual(stored, report)
        self.assertEqual(
            {variant["name"] for variant in report["variants"]},
            {
                "vertical_clean",
                "vertical_lowres_jpeg",
                "vertical_dark",
                "horizontal_clean",
                "horizontal_lowres_jpeg",
                "horizontal_dark",
                "vertical_missing_median",
            },
        )
        successful = [
            variant for variant in report["variants"] if variant["status"] == "passed"
        ]
        self.assertEqual(len(successful), 6)
        self.assertTrue(
            all(
                variant["group_coverage"] == 1.0
                and variant["outlier_f1"] == 1.0
                and variant["summary_mae"] <= 0.25
                for variant in successful
            )
        )
        rejected = next(
            variant
            for variant in report["variants"]
            if variant["name"] == "vertical_missing_median"
        )
        self.assertEqual(rejected["status"], "rejected_as_expected")
        required_evidence = {
            "image_hash_sha256",
            "raster_dimensions",
            "plot_bounds",
            "x_axis",
            "y_axis",
            "colors",
            "tolerance",
            "groups",
            "group_matches",
            "outlier_matches",
            "summary_mae",
            "summary_p95_abs_error",
            "summary_max_abs_error",
            "outlier_precision",
            "outlier_recall",
            "outlier_f1",
            "overlay",
        }
        self.assertTrue(
            all(required_evidence.issubset(variant) for variant in report["variants"])
        )
        self.assertTrue(
            all(len(variant["image_hash_sha256"]) == 64 for variant in report["variants"])
        )
        self.assertTrue(
            all(len(variant["groups"]) == 4 for variant in report["variants"])
        )
        self.assertTrue(
            all(len(variant["group_matches"]) == 4 for variant in report["variants"])
        )
        self.assertTrue(all(overlay_paths))
        self.assertEqual(len(rows), 56)
        summary_rows = [row for row in rows if row["row_type"] == "summary"]
        outlier_rows = [row for row in rows if row["row_type"] == "outlier"]
        self.assertEqual(len(summary_rows), 28)
        self.assertEqual(len(outlier_rows), 28)
        self.assertTrue(
            all(
                row["plot_bounds"]
                and row["x_axis"]
                and row["y_axis"]
                and row["colors"]
                and row["image_hash_sha256"]
                for row in summary_rows
            )
        )

    def test_persists_failed_report_and_csv_before_an_empty_low_confidence_response_raises(self):
        empty_response = {
            "orientation": "vertical",
            "groups": [],
            "status": "low_confidence",
            "reason": "simulated missing evidence",
        }
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(runner, "extract_boxplots", return_value=empty_response):
                with self.assertRaisesRegex(AssertionError, "extractor status is low_confidence"):
                    runner.run_benchmark(output_dir)

            report_path = output_dir / "boxplot_report.json"
            csv_path = output_dir / "boxplot_results.csv"
            self.assertTrue(report_path.is_file())
            self.assertTrue(csv_path.is_file())
            stored = json.loads(report_path.read_text(encoding="utf-8"))
            with csv_path.open(encoding="utf-8", newline="") as source:
                rows = list(csv.DictReader(source))

        self.assertEqual(stored["status"], "failed")
        self.assertTrue(all(variant["status"] == "failed" for variant in stored["variants"]))
        self.assertEqual(len(rows), 56)

    def test_expected_rejection_persists_its_nonempty_diagnostic_reason(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            report = runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "boxplot_report.json").read_text(encoding="utf-8")
            )
            with (output_dir / "boxplot_results.csv").open(
                encoding="utf-8", newline=""
            ) as source:
                rows = list(csv.DictReader(source))

        rejected = next(
            variant
            for variant in report["variants"]
            if variant["name"] == "vertical_missing_median"
        )
        rejection_rows = [
            row for row in rows if row["variant"] == "vertical_missing_median"
        ]
        self.assertEqual(report, stored)
        self.assertEqual(report["rejection_reason"], "vertical_missing_median: missing median line")
        self.assertEqual(rejected["rejection_reason"], "missing median line")
        self.assertEqual(rejected["failure_reason"], "")
        self.assertTrue(rejection_rows)
        self.assertTrue(
            all(
                row["rejection_reason"] == "missing median line"
                and row["failure_reason"] == ""
                for row in rejection_rows
            )
        )

    def test_quality_gate_rejects_an_extra_extracted_group(self):
        real_extractor = runner.extract_boxplots

        def extract_with_extra_group(image_path, *args, **kwargs):
            result = real_extractor(image_path, *args, **kwargs)
            if Path(image_path).name == "vertical_clean.png":
                result = copy.deepcopy(result)
                result["groups"].append(copy.deepcopy(result["groups"][0]))
            return result

        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(
                runner, "extract_boxplots", side_effect=extract_with_extra_group
            ):
                with self.assertRaisesRegex(AssertionError, "extracted 5 groups"):
                    runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "boxplot_report.json").read_text(encoding="utf-8")
            )

        vertical_clean = next(
            variant for variant in stored["variants"] if variant["name"] == "vertical_clean"
        )
        self.assertEqual(vertical_clean["status"], "failed")
        self.assertEqual(vertical_clean["extracted_group_count"], 5)

    def test_quality_gate_rejects_an_extra_outlier_with_nonperfect_f1(self):
        real_extractor = runner.extract_boxplots

        def extract_with_extra_outlier(image_path, *args, **kwargs):
            result = real_extractor(image_path, *args, **kwargs)
            if Path(image_path).name == "vertical_clean.png":
                result = copy.deepcopy(result)
                result["groups"][0]["outliers"].append(
                    {"center_pixel": (0.0, 0.0), "value": 12.5}
                )
            return result

        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            with patch.object(
                runner, "extract_boxplots", side_effect=extract_with_extra_outlier
            ):
                with self.assertRaisesRegex(AssertionError, "outlier F1"):
                    runner.run_benchmark(output_dir)
            stored = json.loads(
                (output_dir / "boxplot_report.json").read_text(encoding="utf-8")
            )

        vertical_clean = next(
            variant for variant in stored["variants"] if variant["name"] == "vertical_clean"
        )
        self.assertEqual(vertical_clean["status"], "failed")
        self.assertLess(vertical_clean["outlier_f1"], 1.0)

    def test_refuses_a_nonempty_output_directory_without_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            sentinel = output_dir / "sentinel.txt"
            sentinel.write_text("preserve this evidence", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "non-empty"):
                runner.run_benchmark(output_dir)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve this evidence")
            self.assertEqual([path.name for path in output_dir.iterdir()], ["sentinel.txt"])


if __name__ == "__main__":
    unittest.main()
