"""Focused contract checks for the China Mining filled-contour gallery case."""

from __future__ import annotations

import csv
import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
CASE_ID = "china-mining-gakedaban-dt-300m"


class ChinaMiningContourGalleryCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        basics = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
        self.sample = next(sample for sample in basics["samples"] if sample["id"] == CASE_ID)
        self.case_root = GALLERY / "assets" / "cases" / CASE_ID

    def test_case_declares_visible_only_contour_scope(self) -> None:
        self.assertEqual(self.sample["status"], "partial_visible")
        self.assertIn("等值线", self.sample["title"])
        self.assertEqual(self.sample["journal"], "China Mining Magazine")
        self.assertIn("原始磁测站点", self.sample["metricNote"])

    def test_assets_keep_one_source_canvas_and_full_legend_recreation(self) -> None:
        with Image.open(self.case_root / "original.jpg") as original:
            source_size = original.size
            source_hash = hashlib.sha256((self.case_root / "original.jpg").read_bytes()).hexdigest()
        self.assertEqual(source_size, (1575, 1246))
        self.assertEqual(source_hash, "487510a87cdb1438b1fa6fe4ee950597afa59f9e43160a3a729987ba60e924c3")
        for name in ("overlay.png", "recreated.png", "map-only-recreation.png"):
            with Image.open(self.case_root / name) as image:
                self.assertEqual(image.size, source_size, name)
        with Image.open(self.case_root / "original.jpg") as original:
            legend_pixel = original.convert("RGB").getpixel((1438, 676))
        for name in ("recreated.png", "overlay.png"):
            with Image.open(self.case_root / name) as image:
                self.assertEqual(legend_pixel, image.convert("RGB").getpixel((1438, 676)), name)

    def test_primary_csv_and_report_keep_legend_provenance_and_candidate_limits(self) -> None:
        with (self.case_root / "data.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 25)
        self.assertEqual(sum(row["value_status"] == "printed_legend_label" for row in rows), 13)
        self.assertEqual(sum(row["value_status"] == "derived_between_adjacent_printed_legend_labels" for row in rows), 12)
        self.assertTrue(all(row["band_semantics"].endswith("not_a_point_value_or_source_grid") for row in rows))

        report = json.loads((self.case_root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "partial_visible")
        self.assertEqual(report["registered_route_status"], "candidate_only")
        self.assertFalse(report["numeric_output_authorized_by_registered_route"])
        self.assertEqual(report["counts"]["visible_colour_classes"], 25)
        self.assertTrue((self.case_root / report["outputs"]["visible_band_grid"]).is_file())
        self.assertIn("original gridded", " ".join(report["limitations"]).lower())
        for path in self.case_root.glob("*.json"):
            self.assertNotRegex(path.read_text(encoding="utf-8"), r"(?<![A-Za-z])[A-Za-z]:[\\/]")


if __name__ == "__main__":
    unittest.main()
