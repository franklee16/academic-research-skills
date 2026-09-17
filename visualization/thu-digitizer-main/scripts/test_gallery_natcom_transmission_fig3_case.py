from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from build_natcom_transmission_fig3_gallery_case import (
    CANVAS,
    DEFAULT_SOURCE,
    PUBLIC_FIELDS,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
CASE_ROOT = GALLERY / "assets" / "cases" / "nature-63143-fig3"


class NatureTransmissionFig3GalleryCaseTests(unittest.TestCase):
    def test_public_bundle_is_complete_and_visible_geometry_only(self):
        report = json.loads((CASE_ROOT / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-63143-fig3")
        self.assertEqual(report["status"], "partial_visible")
        self.assertEqual(report["visible_mark_counts"]["bars_accepted"], 22)
        self.assertEqual(report["visible_mark_counts"]["line_markers_accepted"], 22)
        self.assertFalse(report["public_gallery"]["source_data_used_by_renderer"])
        self.assertEqual(report["public_gallery"]["primary_csv_fields"], PUBLIC_FIELDS)

        for name in ("original.png", "overlay.png", "recreated.png"):
            with Image.open(CASE_ROOT / name) as image:
                self.assertEqual(image.size, CANVAS, name)

        with (CASE_ROOT / "data.csv").open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            self.assertEqual(reader.fieldnames, PUBLIC_FIELDS)
        self.assertEqual(len(rows), 22)
        self.assertEqual({row["panel_id"] for row in rows}, {"median_left", "mean_right"})
        self.assertEqual(
            {(row["panel_id"], row["year"]) for row in rows},
            {
                (panel_id, str(year))
                for panel_id in ("median_left", "mean_right")
                for year in range(2012, 2023)
            },
        )
        self.assertTrue(all(row["bar_status"] == "vector_rectangle_extracted" for row in rows))
        self.assertTrue(all(row["line_status"] == "vector_marker_extracted" for row in rows))
        self.assertFalse(
            [field for field in PUBLIC_FIELDS if any(token in field.lower() for token in ("source", "author", "official"))]
        )

    def test_public_json_has_no_machine_absolute_paths(self):
        for name in ("report.json", "figure-spec.json", "manifest.json"):
            text = (CASE_ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn("F:\\", text, name)
            self.assertNotIn("C:\\", text, name)

    @unittest.skipUnless(
        DEFAULT_SOURCE.is_dir(),
        "retained local PDF evidence is not part of the public gallery checkout",
    )
    def test_builder_recreates_the_same_public_csv_and_canvases(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "case"
            sample = build(DEFAULT_SOURCE, target)
            self.assertEqual(sample["id"], "bar")
            self.assertEqual(sample["styleSpec"]["renderer"], "paper-dual-axis-bar-line")
            self.assertEqual(
                (target / "data.csv").read_bytes(),
                (CASE_ROOT / "data.csv").read_bytes(),
            )
            for name in ("original.png", "overlay.png", "recreated.png"):
                with Image.open(target / name) as image:
                    self.assertEqual(image.size, CANVAS, name)

    def test_gallery_slot_and_interactive_renderer_point_to_this_case(self):
        basics = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
        bar = next(sample for sample in basics["samples"] if sample["id"] == "bar")
        self.assertEqual(bar["assets"]["data"], "assets/cases/nature-63143-fig3/data.csv")
        self.assertEqual(bar["figure"], "Fig. 3")
        self.assertEqual(bar["styleSpec"]["renderer"], "paper-dual-axis-bar-line")

        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        self.assertIn("function renderPaperDualAxisBarLine", script)
        self.assertIn('"paper-dual-axis-bar-line": () => renderPaperDualAxisBarLine', script)
        self.assertIn("table.headers.map((field) => [field, row[field]])", script)
        self.assertIn('"pointer-events": "none"', script)


if __name__ == "__main__":
    unittest.main()
