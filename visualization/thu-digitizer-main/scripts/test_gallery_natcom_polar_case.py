import csv
import hashlib
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

from build_natcom_polar_histogram_case import sanitize_public_json


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
CASE_ID = "nature-20563-fig6f"
CASE_ROOT = GALLERY / "assets" / "cases" / CASE_ID


class NatureCommunicationsPolarCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basics = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
        cls.samples = [sample for sample in cls.basics["samples"] if sample["id"] == CASE_ID]
        with (CASE_ROOT / "data.csv").open(newline="", encoding="utf-8-sig") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_case_is_registered_once_with_polar_renderer(self):
        self.assertEqual(len(self.samples), 1)
        sample = self.samples[0]
        self.assertEqual(sample["status"], "candidate")
        self.assertEqual(sample["figure"], "Fig. 6f")
        self.assertEqual(sample["styleSpec"]["renderer"], "paper-polar-histogram")
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 1798, "height": 310})
        self.assertEqual(sample["metrics"][0], {"label": "可见扇区", "value": "30 / 30"})
        for relative in sample["assets"].values():
            self.assertTrue((GALLERY / relative).is_file(), relative)

    def test_csv_covers_every_visible_eighteen_degree_bin(self):
        self.assertEqual(len(self.rows), 30)
        grouped = defaultdict(list)
        for row in self.rows:
            grouped[row["panel_id"]].append(row)
            self.assertEqual(row["status"], "candidate")
            self.assertEqual(row["reason_code"], "visible_geometry_supported")
            self.assertGreater(float(row["radial_value"]), 0)
            self.assertGreater(float(row["radial_uncertainty_approx"]), 0)
            self.assertGreater(int(row["support_pixels"]), 0)
            for key in ("chord_x1_px", "chord_y1_px", "chord_x2_px", "chord_y2_px"):
                self.assertTrue(row[key])

        self.assertEqual(Counter(row["panel_id"] for row in self.rows), Counter(D30=10, D15=10, D10=10))
        expected_intervals = [(start, start + 18) for start in range(0, 180, 18)]
        for panel_id in ("D30", "D15", "D10"):
            intervals = sorted(
                (int(row["theta_start_deg"]), int(row["theta_end_deg"]))
                for row in grouped[panel_id]
            )
            self.assertEqual(intervals, expected_intervals)

    def test_recreation_and_review_crop_share_the_same_canvas(self):
        with Image.open(CASE_ROOT / "original.png") as original:
            self.assertEqual(original.size, (1798, 310))
        with Image.open(CASE_ROOT / "recreated.png") as recreated:
            self.assertEqual(recreated.size, (1798, 310))
        with Image.open(CASE_ROOT / "measurement-source.png") as measurement_source:
            self.assertEqual(measurement_source.size, (1798, 2550))

    def test_report_keeps_image_extraction_separate_from_source_validation(self):
        report = json.loads((CASE_ROOT / "report.json").read_text(encoding="utf-8"))
        public = report["public_gallery"]
        self.assertEqual(report["registered_route"], "unsupported_coordinate_route")
        self.assertFalse(report["numeric_output_authorized_by_registered_route"])
        self.assertEqual(report["source_validation"]["status"], "metric_absent_in_source_workbook")
        self.assertFalse(report["source_validation"]["figure_6f_sheet_present"])
        self.assertEqual(public["primary_csv_source"], "image_derived_only")
        self.assertTrue(public["source_validation_separate"])
        self.assertEqual(public["original_and_recreation_canvas"], [1798, 310])

    def test_manifest_hashes_every_published_evidence_asset(self):
        manifest = json.loads((CASE_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["case_id"], CASE_ID)
        self.assertEqual(manifest["row_count"], 30)
        for relative, expected_sha256 in manifest["assets"].items():
            path = CASE_ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_sha256, relative)

    def test_case_builder_redacts_source_directory_from_public_json(self):
        source = ROOT / "outputs" / "natcom-s41467-020-20563-9-fig6f"
        payload = {
            "input_file": str(source / "figure6-original.png"),
            "article_url": "https://www.nature.com/articles/s41467-020-20563-9",
        }
        sanitized = sanitize_public_json(payload, source)
        self.assertEqual(sanitized["input_file"], "figure6-original.png")
        self.assertEqual(sanitized["article_url"], payload["article_url"])

    def test_home_script_registers_the_interactive_renderer(self):
        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        self.assertIn('text.startsWith("\\uFEFF") ? text.slice(1) : text', script)
        self.assertIn("function renderPaperPolarHistogram(sample, table)", script)
        self.assertIn('"paper-polar-histogram": () => renderPaperPolarHistogram(sample, table)', script)


if __name__ == "__main__":
    unittest.main()
