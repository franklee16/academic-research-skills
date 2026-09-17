"""Contract checks for the visible-evidence China Mining isogram extraction."""

from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "outputs" / "china-mining-gakedaban-dt-300m"
EVIDENCE = CASE_ROOT / "visible-contour-extraction-v2-full-legend"


class ChinaMiningIsogramExtractionTests(unittest.TestCase):
    def test_visible_band_representation_is_complete_and_qualified(self) -> None:
        with (EVIDENCE / "visible_contour_bands.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 25)
        self.assertEqual(rows[0]["printed_legend_value_nT"], "20")
        self.assertEqual(rows[1]["printed_legend_value_nT"], "")
        self.assertEqual(rows[-1]["printed_legend_value_nT"], "500")
        self.assertTrue(all(row["band_semantics"].endswith("not_a_point_value_or_source_grid") for row in rows))

    def test_report_preserves_candidate_limits_and_same_canvas_views(self) -> None:
        summary = json.loads((EVIDENCE / "extraction_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["status"], "candidate_partial_visible")
        self.assertEqual(summary["visible_grammar"]["filled_colour_classes"], 25)
        self.assertTrue(summary["legend"]["candidate_class_index_is_not_physical_value"])
        self.assertIn("original gridded ΔT values", " ".join(summary["not_recovered"]))
        self.assertIn("map_only_recreation", summary["files"])
        with Image.open(CASE_ROOT / "source.jpg") as original, Image.open(EVIDENCE / "map_recreation.png") as recreation:
            self.assertEqual(original.size, recreation.size)
            # The legend is a visible figure layer and must not disappear from
            # the full-canvas recreation.  This pixel is inside its 260 nT
            # colour swatch and outside the reconstructed map polygon.
            self.assertEqual(original.convert("RGB").getpixel((1438, 676)), recreation.convert("RGB").getpixel((1438, 676)))
        with Image.open(EVIDENCE / "map_only_recreation.png") as map_only:
            self.assertEqual(map_only.size, recreation.size)

    def test_coordinate_fit_uses_only_visible_graticule_anchors(self) -> None:
        calibration = json.loads((EVIDENCE / "coordinate_calibration.json").read_text(encoding="utf-8"))
        self.assertLess(calibration["longitude"]["max_abs_anchor_residual_arcminute"], 0.01)
        self.assertLess(calibration["latitude"]["max_abs_anchor_residual_arcminute"], 0.01)
        self.assertIn("datum", " ".join(calibration["limitations"]).lower())


if __name__ == "__main__":
    unittest.main()
