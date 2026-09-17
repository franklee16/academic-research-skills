"""Focused contract checks for the Nature Communications Fig. 5a gallery case."""

from __future__ import annotations

import csv
import json
import unittest
from collections import Counter
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
GALLERY = REPO_ROOT / "gallery"
CASE_ID = "nature-51329-fig5a"


class NatureCommunicationsSpatialPointCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        basics = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
        self.sample = next(sample for sample in basics["samples"] if sample["id"] == CASE_ID)
        self.case_root = GALLERY / "assets" / "cases" / CASE_ID

    def test_case_is_explicitly_a_partial_visible_spatial_point_map(self) -> None:
        self.assertEqual(self.sample["status"], "partial_visible")
        self.assertIn("空间点位图", self.sample["title"])
        self.assertEqual(self.sample["figure"], "Fig. 5a")
        self.assertTrue(self.sample["styleSpec"]["rasterEvidenceInteractive"])
        self.assertEqual(self.sample["styleSpec"]["canvas"], {"width": 1834, "height": 550})

    def test_primary_csv_is_only_visible_vector_point_evidence(self) -> None:
        with (self.case_root / "data.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 3850)
        self.assertEqual(Counter(row["set"] for row in rows), {
            "region_map": 426,
            "map_11": 496,
            "map_12": 496,
            "map_13": 496,
            "map_14": 496,
            "map_21": 360,
            "map_22": 360,
            "map_23": 360,
            "map_24": 360,
        })
        self.assertEqual({row["visible_status"] for row in rows}, {"vector_marker_extracted"})
        self.assertEqual({row["numeric_use_allowed"] for row in rows}, {"false"})
        self.assertEqual(
            Counter(row["value_status"] for row in rows)["colourbar_calibrated_visible_approximation"],
            3424,
        )

    def test_triptych_and_report_preserve_the_candidate_limit(self) -> None:
        for name in ("original.png", "overlay.png", "recreated.png"):
            with Image.open(self.case_root / name) as image:
                self.assertEqual(image.size, (1834, 550))
        report = json.loads((self.case_root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "partial_visible")
        self.assertEqual(report["registered_route"], "unknown_refuse")
        self.assertFalse(report["numeric_output_authorized_by_registered_route"])
        self.assertEqual(report["counts"]["primary_csv_rows"], 3850)
        self.assertIn("no contour lines or filled contour bands", " ".join(report["limitations"]).lower())


if __name__ == "__main__":
    unittest.main()
