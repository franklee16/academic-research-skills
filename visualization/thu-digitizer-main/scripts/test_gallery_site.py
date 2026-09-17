import csv
import hashlib
import json
import math
import unittest
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"


class GallerySiteTests(unittest.TestCase):
    def test_requested_nature_case_json_does_not_expose_local_absolute_paths(self):
        for case_id in (
            "nature-70284-fig8a",
            "nature-36825-fig1b",
            "nature-40822-fig1f",
            "nature-20563-fig6f",
        ):
            case_root = GALLERY / "assets" / "cases" / case_id
            for path in case_root.glob("*.json"):
                with self.subTest(case=case_id, file=path.name):
                    self.assertNotRegex(path.read_text(encoding="utf-8"), r"(?<![A-Za-z])[A-Za-z]:[\\\\/]")

    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((GALLERY / "data" / "cases.json").read_text(encoding="utf-8"))
        cls.basics = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))

    def test_static_entrypoints_exist(self):
        for relative in [
            "index.html",
            "home.css",
            "home.js",
            "README.md",
            "ATTRIBUTION.md",
        ]:
            self.assertTrue((GALLERY / relative).is_file(), relative)
        for relative in [
            "capabilities.html",
            "styles.css",
            "app.js",
            "data/capabilities.json",
        ]:
            self.assertFalse((GALLERY / relative).exists(), relative)

    def test_every_recreated_image_uses_the_original_canvas_dimensions(self):
        for sample in self.basics["samples"]:
            with self.subTest(sample=sample["id"]):
                with Image.open(GALLERY / sample["assets"]["original"]) as original:
                    with Image.open(GALLERY / sample["assets"]["recreated"]) as recreated:
                        self.assertEqual(recreated.size, original.size)

    def test_first_line_case_uses_the_attached_image_and_semantic_extraction(self):
        sample = self.basics["samples"][0]
        self.assertEqual(sample["id"], "line")
        root = GALLERY / "assets" / "basics" / "line"
        original = root / "original.png"
        self.assertEqual(
            hashlib.sha256(original.read_bytes()).hexdigest(),
            "04efe900130ee60e291fdff77374c2283a16b0a0f0ae7a6568e6e3d134991d84",
        )

        with (root / "data.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        points = [row for row in rows if row["kind"] == "point"]
        self.assertEqual(len(points), 33)
        self.assertEqual(
            Counter(row["series"] for row in points),
            Counter({"biodiversity": 11, "context": 11, "economic_language": 11}),
        )
        self.assertTrue(all(row["pixel_x"] and row["pixel_y"] for row in points))
        self.assertTrue(all(row["value_status"] == "calibrated_original_pixel_sample" for row in points))
        context = [row for row in points if row["series"] == "context"]
        self.assertEqual(sum(row["error_status"] == "visible_endpoints_extracted" for row in context), 11)

        report = json.loads((root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(original.read_bytes()).hexdigest())
        self.assertEqual(report["visible_extraction"]["implementation"], "scripts/digitize_line_chart.py")
        self.assertEqual(report["coverage"], {"points_found": 33, "points_expected": 33, "error_bars_found": 11, "error_bars_expected": 11})
        self.assertEqual(report["validation"]["role"], "independent_synthetic_truth_validation_only")
        self.assertLess(report["validation"]["point_mae"], 0.35)
        self.assertTrue(sample["styleSpec"]["rasterEvidenceInteractive"])
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 600, "height": 400})

    def test_nature_56055_marker_line_case_publishes_full_original_pixel_evidence(self):
        case_id = "nature-56055-fig3c"
        sample = next(item for item in self.basics["samples"] if item["id"] == case_id)
        root = GALLERY / "assets" / "cases" / case_id
        original = root / "original.png"
        expected_sha256 = "fd5fe57633c5535eedd61619cd4d60c7ca5136a523f08655a4b8c19ad8cb0078"

        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), expected_sha256)
        self.assertEqual(sample["metrics"][0], {"value": "168 / 168", "label": "曲线标记覆盖"})
        self.assertTrue(sample["styleSpec"]["rasterEvidenceInteractive"])

        with (root / "data.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        curve_points = [row for row in rows if row["category"] == "visible curve marker"]
        curve_lines = [row for row in rows if row["category"] == "visible marker connection"]
        local_dots = [row for row in rows if row["series"].startswith("local dot field")]
        self.assertEqual(len(rows), 390)
        self.assertEqual(
            Counter(row["series"] for row in curve_points),
            Counter({"Spontaneous curvature": 56, "Surface reconstruction": 56, "Rigid": 56}),
        )
        self.assertEqual(len(curve_lines), 165)
        self.assertEqual(len(local_dots), 57)
        self.assertTrue(all(row["pixel_x"] and row["pixel_y"] for row in curve_points))
        self.assertTrue(all(row["confidence"] and row["value_uncertainty"] for row in curve_points))
        self.assertEqual(
            {row["value_status"] for row in curve_points},
            {"candidate_marker_centre_global_path_v0.2.0"},
        )

        report = json.loads((root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "visible_geometry_candidate")
        self.assertEqual(report["source"]["sha256"], expected_sha256)
        self.assertEqual((report["source"]["width"], report["source"]["height"]), (1495, 1278))
        self.assertEqual(report["source_data_role"], "not_used")
        self.assertFalse(report["primary_csv"]["source_data_used"])
        self.assertTrue(report["visible_extraction"]["numeric_output_authorized"])
        self.assertEqual(report["coverage"]["declared_curve_marker_slots"], 168)
        self.assertEqual(report["coverage"]["authorized_curve_markers"], 168)
        self.assertEqual(report["coverage"]["retained_local_dot_components"], 57)

        run_manifest = json.loads((root / "figure-spec-run-manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(run_manifest["numeric_output_authorized"])
        self.assertEqual({panel["panel_id"] for panel in run_manifest["panels"]}, {
            "spontaneous_curvature", "surface_reconstruction", "rigid",
        })
        self.assertTrue(all(panel["numeric_output_authorized"] for panel in run_manifest["panels"]))
        for panel in report["visible_extraction"]["panels"]:
            candidate = json.loads((root / panel["candidate_report"]).read_text(encoding="utf-8"))
            self.assertTrue(candidate["numeric_output_authorized"])
            self.assertEqual(candidate["series"][next(iter(candidate["series"]))]["summary"]["extracted"], 56)

        for path in root.rglob("*.json"):
            self.assertNotRegex(path.read_text(encoding="utf-8"), r"(?<![A-Za-z])[A-Za-z]:[\\\\/]", path.name)

        with Image.open(original) as source_image, Image.open(root / "recreated.png") as recreated:
            self.assertEqual(source_image.size, (1495, 1278))
            self.assertEqual(recreated.size, source_image.size)

    def test_nature_27341_upset_case_uses_validated_original_pixel_geometry(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "nature-27341-fig1")
        with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        totals = [row for row in rows if row["kind"] == "set_total"]
        intersections = [row for row in rows if row["kind"] == "intersection"]

        self.assertEqual(len(totals), 19)
        self.assertEqual(len(intersections), 30)
        self.assertEqual([int(row["count"]) for row in intersections], [
            998, 802, 684, 675, 500, 441, 287, 278, 229, 124, 117, 110, 110, 108, 83,
            71, 62, 41, 40, 40, 39, 38, 37, 28, 23, 21, 16, 9, 7, 4,
        ])
        self.assertEqual([row["members"] for row in intersections], [
            "Pa35T2", "Pa37T1;Pa37T2", "Pa36T1;Pa36T2", "Pa35T1",
            "Pa29T1;Pa29T2;Pa29T4", "Pa33T1;Pa33T2", "Pa30T1;Pa30T2", "Pa37T2",
            "Pa35T1;Pa35T2", "Pa33T2", "Pa31T2", "Pa31T1;Pa31T2", "Pa34T1;Pa34T2",
            "Pa26T1;Pa26T2", "Pa37T1", "Pa34T1", "Pa26T1", "Pa29T2", "Pa31T1",
            "Pa34T2", "Pa29T1;Pa29T2", "Pa33T1", "Pa26T2", "Pa29T4", "Pa30T2",
            "Pa30T1", "Pa29T1", "Pa29T2;Pa29T4", "Pa36T2", "Pa36T1",
        ])
        self.assertEqual(sum(int(row["member_count"]) for row in intersections), 42)

        expected_totals = {
            "Pa26T1": 170, "Pa26T2": 145, "Pa29T1": 555, "Pa29T2": 589, "Pa29T4": 537,
            "Pa30T1": 308, "Pa30T2": 310, "Pa31T1": 150, "Pa31T2": 227, "Pa33T1": 479,
            "Pa33T2": 565, "Pa34T1": 181, "Pa34T2": 150, "Pa35T1": 904, "Pa35T2": 1227,
            "Pa36T1": 688, "Pa36T2": 691, "Pa37T1": 885, "Pa37T2": 1080,
        }
        self.assertEqual({row["set"]: int(row["value"]) for row in totals}, expected_totals)
        for name, expected in expected_totals.items():
            derived = sum(int(row["count"]) for row in intersections if name in row["members"].split(";"))
            self.assertEqual(derived, expected, name)
        self.assertTrue(all(abs(float(row["pixel_error"])) <= 3 for row in totals))
        self.assertAlmostEqual(float(intersections[0]["pixel_x"]), 560.5)
        self.assertAlmostEqual(float(intersections[-1]["pixel_x"]), 1761.5)
        self.assertAlmostEqual(float(totals[0]["pixel_y"]), 1119.0)
        self.assertAlmostEqual(float(totals[-1]["pixel_y"]), 1499.0)

        report = json.loads((GALLERY / sample["assets"]["report"]).read_text(encoding="utf-8"))
        self.assertEqual(report["visible_extraction"]["algorithm_version"], "lattice-composite-original-pixel-v2")
        self.assertEqual(report["coverage"]["membership_grid_cells"], 570)
        self.assertEqual(report["coverage"]["active_membership_nodes"], 42)
        self.assertLess(report["validation"]["set_total_left_bar_max_abs_error"], 3)
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 1999, "height": 1579})
        self.assertEqual(sample["styleSpec"]["layout"]["left"], 519)
        self.assertEqual(sample["styleSpec"]["layout"]["right"], 1803)
        candidate = json.loads(
            (GALLERY / "assets" / "cases" / "nature-27341-fig1" / "lattice-candidate-report.json").read_text(encoding="utf-8")
        )
        self.assertTrue(candidate["numeric_output_authorized"])
        self.assertEqual(candidate["coordinate_provenance"]["measurement_space"], "original_raster_pixels")
        preflight = json.loads(
            (GALLERY / "assets" / "cases" / "nature-27341-fig1" / "preflight-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual(preflight["route_selection"]["primary"]["route_id"], "raster_lattice_composite_candidate")
        spec = json.loads(
            (GALLERY / "assets" / "cases" / "nature-27341-fig1" / "figure-spec.json").read_text(encoding="utf-8")
        )
        self.assertEqual(spec["source"]["measurement_space"], "original_raster_pixels")
        self.assertFalse(spec["source"]["resampling_applied"])

    def test_every_other_upset_case_is_original_pixel_extracted_and_source_validated(self):
        expected = {
            "nature-19006-fig2b": {"columns": 15, "rows": 4, "active": 32, "primary": 51},
            "nature-28348-fig7": {"columns": 12, "rows": 5, "active": 40, "primary": 57},
        }
        for case_id, counts in expected.items():
            with self.subTest(case=case_id):
                sample = next(item for item in self.basics["samples"] if item["id"] == case_id)
                root = GALLERY / "assets" / "cases" / case_id
                with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(len(rows), counts["primary"])
                self.assertEqual(sum(row["kind"] == "intersection" for row in rows), counts["columns"])
                self.assertEqual(sum(row["kind"] == "set_total" for row in rows), counts["rows"])
                self.assertEqual(sum(row["kind"] == "membership_cell" for row in rows), counts["active"])
                self.assertTrue(all(row["pixel_x"] and row["pixel_y"] for row in rows))

                report = json.loads((root / "report.json").read_text(encoding="utf-8"))
                self.assertEqual(report["status"], "visible_geometry_candidate")
                self.assertEqual(report["source_data_role"], "independent_validation_only")
                self.assertTrue(report["visible_extraction"]["numeric_output_authorized"])
                self.assertEqual(report["visible_extraction"]["algorithm_version"], "lattice-composite-original-pixel-v2")
                self.assertEqual(report["coverage"]["membership_grid_cells"], counts["columns"] * counts["rows"])
                self.assertEqual(report["coverage"]["active_membership_nodes"], counts["active"])
                self.assertEqual(report["coverage"]["ambiguous_membership_nodes"], 0)
                self.assertEqual(report["validation"]["source_mismatch_count"], 0)
                self.assertEqual(report["validation"]["official_source"]["status"], "validated")

                candidate = json.loads((root / "lattice-candidate-report.json").read_text(encoding="utf-8"))
                self.assertEqual(candidate["coordinate_provenance"]["measurement_space"], "original_raster_pixels")
                self.assertFalse(candidate["coordinate_provenance"]["resampling_applied"])
                with (root / "source-validation.csv").open(newline="", encoding="utf-8") as handle:
                    validation = list(csv.DictReader(handle))
                self.assertEqual(len(validation), counts["columns"])
                self.assertTrue(all(row["validation_status"] == "validated" for row in validation))
                preflight = json.loads((root / "preflight-report.json").read_text(encoding="utf-8"))
                self.assertEqual(preflight["route_selection"]["primary"]["route_id"], "raster_lattice_composite_candidate")

    def test_homepage_leads_with_image_extraction_only_chart_cases(self):
        samples = self.basics["samples"]
        self.assertEqual(
            [item["id"] for item in samples],
            [
                "line",
                "scatter",
                "nature-56055-fig3c",
                "dose-response",
                "bar",
                "bar-horizontal",
                "bar-stacked",
                "bar-percent-stacked",
                "pie",
                "nature-20563-fig6f",
                "histogram",
                "heatmap",
                "boxplot",
                "boxplot-horizontal",
                "forest",
                "nature-21043-fig6a",
                "nature-00142-fig3a",
                "nature-00142-fig4a",
                "nature-02571-fig1d",
                "nature-63786-fig1c",
                "nature-19006-fig2b",
                "nature-28348-fig7",
                "nature-27341-fig1",
                "nature-70099-fig5e",
                "nature-37200-fig8e",
                "nature-31408-fig2d",
                "nature-06199-fig1",
                "nature-60895-fig4c",
                "nature-51329-fig5a",
                "china-mining-gakedaban-dt-300m",
            ],
        )
        self.assertEqual(sum(item["status"] == "validated_local_stable" for item in samples), 3)
        self.assertEqual(sum(item["status"] == "candidate" for item in samples), 6)
        self.assertEqual(sum(item["status"] == "partial_visible" for item in samples), 4)
        self.assertEqual(sum(item["status"] == "low_confidence" for item in samples), 1)
        self.assertEqual(next(item for item in samples if item["id"] == "forest")["status"], "visible_geometry_extracted")
        self.assertFalse(any(item["status"] == "source_mapped" for item in samples))

        html = (GALLERY / "index.html").read_text(encoding="utf-8")
        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        self.assertIn("图表提取能力", html)
        self.assertIn("图形类型", html)
        self.assertNotIn('class="hero"', html)
        self.assertNotIn("FIGURE → DATA", html)
        self.assertNotIn('id="hero-title"', html)
        self.assertNotIn("capabilities.html", html)
        self.assertIn('fetch("data/basics.json")', script)
        for label in ["原图", "提取覆盖", "复现"]:
            self.assertIn(label, script)

    def test_requested_nature_bar_cases_replace_the_synthetic_examples(self):
        expected = {
            "bar-horizontal": {
                "figureUrl": "https://www.nature.com/articles/s41467-026-70284-8/figures/8",
                "rows": 16,
                "extracted": 13,
                "authorized": 13,
                "missing": 3,
                "canvas": (2001, 360),
                "report_status": "partial_visible",
            },
            "bar-stacked": {
                "figureUrl": "https://www.nature.com/articles/s41467-023-36825-1/figures/1",
                "rows": 33,
                "extracted": 29,
                "authorized": 0,
                "missing": 4,
                "canvas": (709, 600),
                "report_status": "low_confidence",
            },
        }
        for case_id, wanted in expected.items():
            with self.subTest(case=case_id):
                sample = next(item for item in self.basics["samples"] if item["id"] == case_id)
                self.assertEqual(sample["figureUrl"], wanted["figureUrl"])
                self.assertTrue(sample["styleSpec"]["rasterEvidenceInteractive"])
                self.assertEqual(
                    (sample["styleSpec"]["canvas"]["width"], sample["styleSpec"]["canvas"]["height"]),
                    wanted["canvas"],
                )
                root = (GALLERY / sample["assets"]["report"]).parent
                with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(len(rows), wanted["rows"])
                self.assertEqual(sum(row["numeric_use_allowed"] == "true" for row in rows), wanted["authorized"])
                self.assertEqual(sum(row["value_status"] != "not_extracted" for row in rows), wanted["extracted"])
                self.assertEqual(sum(row["value_status"] == "not_extracted" for row in rows), wanted["missing"])
                report = json.loads((root / "report.json").read_text(encoding="utf-8"))
                self.assertEqual(report["status"], wanted["report_status"])
                self.assertFalse(report["expected_detection_count_passed"])
                self.assertEqual(report["source_data_role"], "independent_validation_only")
                for name in ["preflight-report.json", "figure-spec.json", "source-validation.json", "SOURCES.md"]:
                    self.assertTrue((root / name).is_file(), f"{case_id}:{name}")

    def test_fig8e_uses_the_user_approved_raster_and_reviewed_36_point_case(self):
        sample = next(
            item for item in self.basics["samples"] if item["id"] == "nature-37200-fig8e"
        )
        self.assertEqual(
            {metric["label"]: metric["value"] for metric in sample["metrics"]},
            {"bars": "6", "point candidates": "36", "clean markers": "17"},
        )
        self.assertNotIn("?", sample["description"])
        self.assertNotIn("?", sample["styleSpec"]["note"])
        self.assertTrue(sample["styleSpec"]["rasterEvidenceInteractive"])

        root = (GALLERY / sample["assets"]["report"]).parent
        original = root / "original.png"
        expected_hash = "fcec6e33ba24cd5a8588ebdd04787aca74bf71a3f6955658ee3adcc24ec4e234"
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), expected_hash)
        for name in ("original.png", "overlay.png", "recreated.png"):
            with Image.open(root / name) as image:
                self.assertEqual(image.size, (1700, 581), name)

        with (root / "data.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 60)
        self.assertEqual(Counter(row["kind"] for row in rows), Counter({"point": 36, "line": 18, "rect": 6}))
        point_rows = [row for row in rows if row["kind"] == "point"]
        self.assertEqual(
            Counter((row["series"], row["category"]) for row in point_rows),
            Counter(
                {
                    ("E. coli B36", "-"): 6,
                    ("E. coli B36", "+"): 6,
                    ("S. aureus BPH2900", "-"): 6,
                    ("S. aureus BPH2900", "+"): 6,
                    ("S. pyogenes HKU419", "-"): 6,
                    ("S. pyogenes HKU419", "+"): 6,
                }
            ),
        )
        self.assertEqual(
            Counter(row["value_status"] for row in point_rows),
            Counter(
                {
                    "visible_marker_candidate": 17,
                    "error_line_overlap_candidate": 10,
                    "bar_outline_overlap_candidate": 7,
                    "merged_cluster_candidate": 2,
                }
            ),
        )
        self.assertEqual(sum(row["numeric_use_allowed"] == "true" for row in point_rows), 17)

        report = json.loads((root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "candidate_with_review_flags")
        self.assertEqual(report["extraction_strategy"], "hybrid")
        self.assertEqual(report["input"]["sha256"], expected_hash)
        self.assertEqual(report["point_candidates"], 36)
        self.assertEqual(report["primary_csv"]["rows"], 60)
        self.assertEqual(len(report["summary_consistency"]), 6)
        self.assertEqual(report["source_data_role"], "not_used")

    def test_fig4c_overlay_is_registered_to_the_cropped_original_pixels(self):
        sample = next(
            item for item in self.basics["samples"] if item["id"] == "nature-60895-fig4c"
        )
        root = (GALLERY / sample["assets"]["report"]).parent
        original_path = root / "original.png"
        self.assertEqual(
            hashlib.sha256(original_path.read_bytes()).hexdigest(),
            "128779e655ef28a2ff2e6a5ae4239976a8a2ea8df01315b19b09ced9e759f3fc",
        )

        with Image.open(original_path) as original, Image.open(root / "overlay.png") as overlay, Image.open(root / "recreated.png") as recreated:
            self.assertEqual(original.size, (1050, 650))
            self.assertEqual(overlay.size, original.size)
            self.assertEqual(recreated.size, original.size)
            self.assertIsNotNone(ImageChops.difference(original.convert("RGB"), overlay.convert("RGB")).getbbox())

            with (root / "data.csv").open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 22)
            self.assertEqual(
                Counter(row["value_status"] for row in rows),
                Counter({"visible_stacked_segment_candidate": 21, "border_occluded_stacked_segment_candidate": 1}),
            )
            for row in rows:
                x = int(row["pixel_x"])
                y = int(row["pixel_y"])
                width = int(row["width"])
                height = int(row["height"])
                bounds = (x, y, x + width, y + height)
                pixels = list(original.crop(bounds).get_flattened_data())
                if row["value_status"].startswith("border_occluded"):
                    self.assertEqual((row["series"], row["category"]), ("Downregulated", "Microglia"))
                elif row["series"] == "Upregulated":
                    support = sum(red > 220 and green < 100 and blue < 80 for red, green, blue in pixels)
                    self.assertGreaterEqual(support / len(pixels), 0.95, row["category"])
                else:
                    support = sum(blue > 180 and green > 100 and red < 80 for red, green, blue in pixels)
                    self.assertGreaterEqual(support / len(pixels), 0.95, row["category"])

                review_bounds = (max(0, x - 3), max(0, y - 3), min(original.width, x + width + 3), min(original.height, y + height + 3))
                self.assertIsNotNone(
                    ImageChops.difference(
                        original.crop(review_bounds).convert("RGB"),
                        overlay.crop(review_bounds).convert("RGB"),
                    ).getbbox(),
                    f"{row['series']}:{row['category']}",
                )

        report = json.loads((root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["input"]["crop"], [970, 0, 2020, 650])
        self.assertEqual(report["input"]["dimensions"], [2050, 2448])
        self.assertEqual(report["overlay_registration"]["coordinate_space"], "cropped original raster pixels")
        self.assertEqual(report["overlay_registration"]["max_registration_error_px"], 1)
        self.assertEqual(report["overlay_registration"]["review_status"], "passed")
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 1050, "height": 650})

    def test_requested_nature_donut_case_preserves_visible_labels_without_forcing_100(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "pie")
        self.assertEqual(
            sample["figureUrl"],
            "https://www.nature.com/articles/s41467-023-40822-9/figures/1",
        )
        self.assertEqual(sample["status"], "candidate")
        self.assertTrue(sample["styleSpec"]["rasterEvidenceInteractive"])
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 1025, "height": 215})
        root = (GALLERY / sample["assets"]["report"]).parent
        with (root / "data.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 18)
        self.assertEqual(Counter(row["category"] for row in rows), Counter({"Normal": 4, "AK": 5, "Primary": 4, "MET": 5}))
        self.assertTrue(all(row["value_status"] == "visible_printed_label" for row in rows))
        self.assertTrue(all(row["numeric_use_allowed"] == "true" for row in rows))
        sums = {
            group: round(sum(float(row["value"]) for row in rows if row["category"] == group), 1)
            for group in {row["category"] for row in rows}
        }
        self.assertEqual(sums, {"Normal": 97.5, "AK": 90.6, "Primary": 70.3, "MET": 73.6})
        report = json.loads((root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "candidate")
        self.assertEqual(report["visible_label_extraction"]["recovered_label_count"], 18)
        self.assertFalse(report["normalization_applied_to_primary_values"])
        self.assertEqual(report["shared_pie_route"], "raster_labelled_donut_candidate")
        self.assertTrue((root / "labelled-donut-config.json").is_file())
        self.assertEqual(report["source_data_role"], "independent_validation_only")
        for name in ["preflight-report.json", "figure-spec.json", "sector-geometry.csv", "candidate-report.json", "SOURCES.md"]:
            self.assertTrue((root / name).is_file(), name)

    def test_homepage_detail_has_scrollable_table_download_and_interactive_values(self):
        html = (GALLERY / "index.html").read_text(encoding="utf-8")
        css = (GALLERY / "home.css").read_text(encoding="utf-8")
        script = (GALLERY / "home.js").read_text(encoding="utf-8")

        for element_id in [
            "case-dialog",
            "detail-original-image",
            "detail-recreated-image",
            "original-source",
            "csv-download",
            "data-table-viewport",
            "interactive-chart",
            "chart-tooltip",
            "interactive-readout",
        ]:
            self.assertIn(f'id="{element_id}"', html)
        self.assertIn("拖动表格查看全部行列", html)
        self.assertIn("overflow: auto", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", css)
        self.assertIn(".comparison-panel {\n  display: grid;\n  grid-column: 1 / -1;\n  grid-row: 1;", css)
        self.assertIn("height: clamp(320px, 38vw, 520px)", css)
        self.assertIn('class="interactive-chart comparison-interactive"', html)
        self.assertIn('id="detail-recreated-image"', html)
        self.assertIn('data-recreation-view="interactive"', html)
        self.assertIn('>交互式图</button>', html)
        self.assertNotIn('data-recreation-view="interactive">数据</button>', html)
        self.assertIn("function setRecreationView(view)", script)
        self.assertIn('setRecreationView("recreated")', script)
        self.assertIn("function displayType(sample)", script)
        self.assertIn('class="type-group"', script)
        self.assertIn("type-group-grid", css)
        self.assertIn("function updateOriginalSource(sample)", script)
        self.assertIn("function applyComparisonAlignment(sample)", script)
        self.assertIn("detailOriginalImage.naturalWidth", script)
        self.assertIn(".case-summary {\n  grid-column: 1 / -1;\n  grid-row: 2;", css)
        self.assertIn(".data-panel {\n  grid-column: 1 / -1;\n  grid-row: 3;", css)
        for implementation in [
            "parseCsv",
            "renderTable",
            "renderInteractiveChart",
            "data-tooltip",
            "download",
        ]:
            self.assertIn(implementation, script)

    def test_gallery_uses_audience_facing_status_labels(self):
        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        self.assertIn("function publicStatusLabel(status)", script)
        self.assertIn("publicStatusLabel(sample.status)", script)
        self.assertNotIn("compactStatus(sample.statusLabel)", script)

    def test_paper_cases_have_brief_linked_original_source_metadata(self):
        paper_samples = [sample for sample in self.basics["samples"] if sample.get("articleUrl")]
        self.assertTrue(paper_samples)
        for sample in paper_samples:
            self.assertTrue(sample.get("journal"), sample["id"])
            self.assertTrue(sample.get("articleTitle"), sample["id"])
            self.assertTrue(sample.get("figure"), sample["id"])
            self.assertTrue(sample.get("figureUrl"), sample["id"])

    def test_style_backed_interactive_renderers_are_explicit(self):
        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        style_samples = [sample for sample in self.basics["samples"] if sample.get("styleSpec")]
        self.assertEqual(
            {sample["id"] for sample in style_samples},
            {
                "line",
                "dose-response",
                "bar",
                "heatmap",
                "boxplot",
                "nature-21043-fig6a",
                "nature-00142-fig3a",
                "nature-00142-fig4a",
                "nature-02571-fig1d",
                "nature-56055-fig3c",
                "nature-63786-fig1c",
                "nature-19006-fig2b",
                "nature-28348-fig7",
                "nature-27341-fig1",
                "scatter",
                "nature-70099-fig5e",
                "nature-37200-fig8e",
                "nature-31408-fig2d",
                "nature-06199-fig1",
                "nature-60895-fig4c",
                "bar-horizontal",
                "bar-stacked",
                "pie",
                "nature-20563-fig6f",
                "nature-51329-fig5a",
            },
        )
        renderers = {sample["styleSpec"]["renderer"] for sample in style_samples}
        self.assertEqual(
            renderers,
            {
                "paper-dose-response",
                "paper-dual-axis-bar-line",
                "paper-heatmap",
                "paper-boxplot",
                "paper-bubble-matrix",
                "paper-visible-bars",
                "paper-visible-upset",
                "paper-native-trace-line",
                "paper-native-geometry",
                "paper-polar-histogram",
            },
        )
        for sample in style_samples:
            spec = sample["styleSpec"]
            with self.subTest(sample=sample["id"]):
                self.assertIn(
                    spec["fidelity"],
                    {
                        "evidence_backed_style_reconstruction",
                        "visible_geometry_candidate",
                    },
                )
                self.assertTrue(spec["label"])
                self.assertTrue(spec["note"])
                self.assertIn("canvas", spec)
                self.assertIn(spec["renderer"], script)
        self.assertIn("interactiveChart.dataset.styleMode", script)
        self.assertIn('data-style-mode="evidence-backed"', (GALLERY / "home.css").read_text(encoding="utf-8"))

    def test_raster_evidence_interaction_reuses_the_exact_recreation_canvas(self):
        script = (GALLERY / "home.js").read_text(encoding="utf-8")
        css = (GALLERY / "home.css").read_text(encoding="utf-8")
        raster_cases = [
            sample
            for sample in self.basics["samples"]
            if sample.get("styleSpec", {}).get("rasterEvidenceInteractive")
        ]
        self.assertTrue(raster_cases)
        self.assertIn("function renderRasterEvidenceInteractive", script)
        self.assertIn("href: assetUrl(sample.assets.recreated)", script)
        self.assertIn("comparison-stage > .interactive-chart.comparison-interactive", css)
        self.assertIn("min-height: 0", css)
        for sample in raster_cases:
            with self.subTest(sample=sample["id"]):
                spec = sample["styleSpec"]
                self.assertIn("canvas", spec)
                with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                    headers = next(csv.reader(handle))
                self.assertIn("pixel_x", headers)
                self.assertIn("pixel_y", headers)
                with Image.open(GALLERY / sample["assets"]["recreated"]) as recreation:
                    self.assertEqual(recreation.size, (spec["canvas"]["width"], spec["canvas"]["height"]))

    def test_basic_samples_have_complete_triptychs_and_evidence(self):
        for sample in self.basics["samples"]:
            with self.subTest(sample=sample["id"]):
                for key in ["original", "overlay", "recreated", "data", "report"]:
                    asset = GALLERY / sample["assets"][key]
                    self.assertTrue(asset.is_file(), f"{sample['id']}:{key}")
                    self.assertGreater(asset.stat().st_size, 0, f"{sample['id']}:{key}")
                for key in ["original", "overlay", "recreated"]:
                    with Image.open(GALLERY / sample["assets"][key]) as image:
                        self.assertGreater(image.width, 350)
                        minimum_height = 200 if sample["id"] == "pie" else 250
                        self.assertGreater(image.height, minimum_height)
                with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                    self.assertGreater(len(list(csv.DictReader(handle))), 0)
                report = json.loads((GALLERY / sample["assets"]["report"]).read_text(encoding="utf-8"))
                self.assertEqual(report["schema_version"], 1)

    def test_second_scatter_case_uses_reviewed_eleven_point_candidate_evidence(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "scatter")
        case_root = GALLERY / "assets" / "cases" / "nature-09789-fig4a"
        with (case_root / "data.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        expected = {
            "P(Switch)": (0.088, 0.422),
            "Goalie Y position": (0.147, 0.132),
            "Shooter X position": (0.127, 0.181),
            "Shooter Y position": (0.108, 0.270),
            "Goalie Y velocity": (0.157, 0.132),
            "Shooter Y velocity": (0.125, 0.252),
            "Opponent identity": (0.170, 0.112),
            "Time since last change point": (0.114, 0.256),
            "Opponent experience": (0.186, 0.061),
            "Opponent action metric": (0.155, 0.233),
            "Permutations of all variables": (0.000, 0.000),
        }
        self.assertEqual(len(rows), 11)
        self.assertEqual({row["series"] for row in rows}, set(expected))
        self.assertTrue(all(row["kind"] == "point" for row in rows))
        self.assertTrue(all(row["value_status"] == "visible_marker_candidate" for row in rows))
        for row in rows:
            expected_x, expected_y = expected[row["series"]]
            self.assertAlmostEqual(float(row["x"]), expected_x, delta=0.0006)
            self.assertAlmostEqual(float(row["y"]), expected_y, delta=0.0006)
            self.assertTrue(row["x_uncertainty"])
            self.assertTrue(row["y_uncertainty"])
            self.assertTrue(row["confidence"])

        report = json.loads((case_root / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-09789-fig4a")
        self.assertEqual(report["extractor"], "candidate_compact_scatter_distance_peaks")
        self.assertEqual(report["status"], "candidate")
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["visible_marker_count"], 11)
        self.assertEqual(report["detection"]["accepted_peak_count"], 11)
        self.assertEqual(len(report["deterministic_run_id"]), 16)
        self.assertEqual(report["plot_bounds"], [172, 28, 711, 551])
        self.assertEqual(
            sorted(component["peak_count"] for component in report["components"] if component["peak_count"] > 1),
            [3, 3],
        )
        self.assertEqual(report["overlay_review"]["suppressed_peaks_reviewed"], 2)
        self.assertEqual(report["source_data_role"], "not_used")
        self.assertEqual(report["webplotdigitizer_comparison"], "not_compared")
        self.assertEqual(
            {item["series"] for item in report["semantic_mapping"]["mapping"]},
            set(expected),
        )
        self.assertTrue(
            all(item["association_residual_pixels"] <= 0.75 for item in report["semantic_mapping"]["mapping"])
        )

        digest = hashlib.sha256((case_root / "original.png").read_bytes()).hexdigest()
        self.assertEqual(digest, report["input"]["sha256"])
        for name in ("original.png", "overlay.png", "recreated.png"):
            with Image.open(case_root / name) as image:
                self.assertEqual(image.size, (1370, 650))

        point_metric = next(metric for metric in sample["metrics"] if metric["label"] == "点覆盖")
        self.assertEqual(point_metric["value"], "11 / 11")

    def test_natcom_fig5e_scatter_case_is_data_and_geometry_consistent(self):
        sample = next(
            item for item in self.basics["samples"] if item["id"] == "nature-70099-fig5e"
        )
        with (GALLERY / sample["assets"]["data"]).open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))

        points = [row for row in rows if row["kind"] == "point"]
        lines = [row for row in rows if row["kind"] == "line"]
        self.assertEqual(
            Counter(row["series"] for row in points),
            Counter({"Aβ42/Aβ40 ratio": 17, "MoCA": 16, "p-Tau-181": 15}),
        )
        self.assertEqual(len(lines), 3)
        self.assertTrue(
            all(
                row["value_status"] == "refit_from_extracted_visible_points"
                for row in lines
            )
        )
        self.assertTrue(
            all(
                row["fit_intercept"]
                and row["fit_slope"]
                and row["residual_sd"]
                and row["recomputed_r"]
                and row["annotated_r"]
                and row["annotated_p"]
                for row in lines
            )
        )

        expected_correlations = {
            "Aβ42/Aβ40 ratio": -0.57,
            "MoCA": -0.34,
            "p-Tau-181": 0.12,
        }
        for series, expected in expected_correlations.items():
            series_rows = [row for row in points if row["series"] == series]
            x_values = [float(row["x"]) for row in series_rows]
            y_values = [float(row["y"]) for row in series_rows]
            x_mean = sum(x_values) / len(x_values)
            y_mean = sum(y_values) / len(y_values)
            numerator = sum(
                (x - x_mean) * (y - y_mean)
                for x, y in zip(x_values, y_values)
            )
            denominator = math.sqrt(
                sum((x - x_mean) ** 2 for x in x_values)
                * sum((y - y_mean) ** 2 for y in y_values)
            )
            self.assertAlmostEqual(numerator / denominator, expected, delta=0.01)

        visible_points_metric = next(
            metric for metric in sample["metrics"] if metric["label"] == "visible points"
        )
        self.assertEqual(visible_points_metric["value"], "48")
        self.assertFalse(sample["styleSpec"].get("rasterEvidenceInteractive", False))

        report = json.loads(
            (GALLERY / sample["assets"]["report"]).read_text(encoding="utf-8")
        )
        self.assertEqual(report["visible_point_count"], 48)
        self.assertEqual(report["visible_points_by_panel"], [17, 16, 15])
        self.assertEqual(report["fit_representation"], "OLS refit from extracted visible points")
        self.assertEqual(report["ribbon_representation"], "fitted line ± residual SD")

    def test_bubble_matrix_uses_only_image_extracted_geometry(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "nature-21043-fig6a")
        root = GALLERY / sample["assets"]["data"]
        with root.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 208)
        self.assertEqual(len({(row["row"], row["column"]) for row in rows}), 208)
        self.assertEqual(sum(row["visible_marker"] == "true" for row in rows), 207)
        self.assertEqual(sum(row["visible_mark"] == "dot" for row in rows), 124)
        self.assertEqual(sum(row["visible_mark"] == "circle" for row in rows), 83)
        self.assertFalse({"mean", "p_value", "source_size_proxy", "source_status"}.intersection(rows[0]))
        for row in rows:
            if row["visible_marker"] == "true":
                self.assertTrue(row["visible_color"].startswith("#"))
                self.assertGreater(float(row["visible_radius_px"]), 0)
                self.assertIn(row["visible_geometry_status"], {"raster_detected_marker"})
        report = json.loads((GALLERY / sample["assets"]["report"]).read_text(encoding="utf-8"))
        self.assertEqual(report["coverage"]["categorical_grid_slots"], 208)
        self.assertEqual(report["coverage"]["visible_raster_markers"], 207)
        self.assertEqual(report["coverage"]["unmatched_grid_slots"], 1)
        self.assertEqual(report["pixel_extraction"]["unassigned_components"], 0)

    def test_vertical_boxplot_is_the_real_nature_medicine_case(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "boxplot")
        self.assertEqual(sample["status"], "candidate")
        self.assertEqual(
            sample["articleUrl"],
            "https://www.nature.com/articles/s41591-026-04303-y",
        )
        report = json.loads((GALLERY / sample["assets"]["report"]).read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-protaide-boxplot")
        self.assertEqual(report["stable_baseline"]["status"], "low_confidence")
        self.assertEqual(report["candidate_extraction"]["box_groups_extracted"], 20)
        self.assertEqual(report["candidate_extraction"]["box_groups_visible"], 20)
        self.assertEqual(report["candidate_extraction"]["visible_outliers_extracted"], 9)
        self.assertEqual(report["candidate_extraction"]["raster_coincident_medians"], 1)
        with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 20)
        self.assertEqual({row["panel"] for row in rows}, {"BCA", "AUC"})
        self.assertEqual({row["series"] for row in rows}, {"Retrain", "Finetune"})


    def test_first_bar_card_is_the_vector_pdf_transmission_case(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "bar")
        self.assertEqual(sample["status"], "partial_visible")
        self.assertEqual(
            sample["articleUrl"],
            "https://www.nature.com/articles/s41467-025-63143-5",
        )
        self.assertEqual(sample["styleSpec"]["renderer"], "paper-dual-axis-bar-line")
        self.assertEqual(sample["styleSpec"]["canvas"], {"width": 1756, "height": 828})
        report_path = GALLERY / sample["assets"]["report"]
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-63143-fig3")
        self.assertEqual(report["route"]["route_id"], "pdf_vector_assisted")
        self.assertEqual(report["visible_mark_counts"]["bars_accepted"], 22)
        self.assertEqual(report["visible_mark_counts"]["line_markers_accepted"], 22)
        self.assertFalse(report["public_gallery"]["source_data_used_by_renderer"])
        self.assertEqual(
            report["public_gallery"]["original_and_recreation_canvas"],
            [1756, 828],
        )
        case_root = report_path.parent
        for name in ["original.png", "overlay.png", "recreated.png", "data.csv", "figure-spec.json"]:
            self.assertTrue((case_root / name).is_file(), name)
            self.assertGreater((case_root / name).stat().st_size, 0, name)
        with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 22)
        self.assertEqual({row["panel_id"] for row in rows}, {"median_left", "mean_right"})
        self.assertEqual({row["year"] for row in rows}, {str(year) for year in range(2012, 2023)})
        self.assertTrue(all(row["bar_status"] == "vector_rectangle_extracted" for row in rows))
        self.assertTrue(all(row["line_status"] == "vector_marker_extracted" for row in rows))

    def test_dose_response_is_pdf_vector_extraction_with_separate_validation(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "dose-response")
        self.assertEqual(sample["status"], "candidate")
        self.assertEqual(
            sample["articleUrl"],
            "https://www.nature.com/articles/s41467-026-71361-8",
        )
        report_path = GALLERY / sample["assets"]["report"]
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-kahlous-dose-response")
        extraction = report["candidate_extraction"]
        self.assertEqual(extraction["route"], "verified_vector_pdf_geometry")
        self.assertEqual(extraction["summary"]["visible_marker_count"], 21)
        self.assertEqual(extraction["summary"]["main_marker_count"], 18)
        self.assertEqual(extraction["summary"]["vehicle_marker_count"], 3)
        self.assertEqual(extraction["summary"]["visible_error_bar_count"], 14)
        self.assertEqual(extraction["summary"]["traced_curve_count"], 3)
        validation = report["source_validation"]
        self.assertEqual(validation["source_matched_markers"], 18)
        self.assertEqual(validation["source_uncovered_vehicle_markers"], 3)
        self.assertEqual(validation["sem_occluded_by_marker"], 4)
        self.assertLess(validation["marker_mae"], 0.05)
        self.assertLess(validation["marker_max_absolute_error"], 0.1)
        self.assertLess(validation["visible_error_endpoint_mae"], 0.06)
        case_root = report_path.parent
        for name in [
            "source-article.pdf",
            "source-data.xlsx",
            "curves.csv",
            "source-validation.csv",
            "source-validation.png",
            "vector-inspection.json",
        ]:
            self.assertTrue((case_root / name).is_file(), name)
            self.assertGreater((case_root / name).stat().st_size, 0, name)
        with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 21)
        self.assertEqual({row["series"] for row in rows}, {"ADR", "NA", "DA"})
        self.assertFalse({"source_mean", "source_sem", "source_status", "marker_error"}.intersection(rows[0]))
        self.assertTrue(all(row["status"] == "vector_marker_extracted" for row in rows))

    def test_public_primary_data_never_contains_author_source_fields(self):
        banned_tokens = ("source", "author", "official")
        for sample in self.basics["samples"]:
            with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                headers = next(csv.reader(handle))
            with self.subTest(sample=sample["id"]):
                self.assertFalse(
                    [header for header in headers if any(token in header.lower() for token in banned_tokens)],
                    headers,
                )

    def test_heatmap_is_calibrated_and_validated_against_suppdata_8(self):
        sample = next(item for item in self.basics["samples"] if item["id"] == "heatmap")
        self.assertEqual(sample["status"], "candidate")
        self.assertEqual(
            sample["articleUrl"],
            "https://www.nature.com/articles/s41591-026-04303-y",
        )
        report_path = GALLERY / sample["assets"]["report"]
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["case_id"], "nature-protaide-heatmap")
        self.assertEqual(report["candidate_extraction"]["status"], "candidate")
        self.assertEqual(report["candidate_extraction"]["cell_count"], 672)
        validation = report["source_validation"]
        self.assertEqual(validation["matched_cells"], 672)
        self.assertEqual(validation["numeric_cells"], 578)
        self.assertEqual(validation["endpoint_censored_cells"], 94)
        self.assertLess(validation["numeric_mae"], 0.005)
        self.assertEqual(validation["significance"]["true_positive"], 456)
        self.assertEqual(validation["significance"]["false_positive"], 0)
        self.assertEqual(validation["significance"]["false_negative"], 1)
        case_root = report_path.parent
        for name in ["source-data.xlsx", "source-validation.csv", "source-validation.png"]:
            self.assertTrue((case_root / name).is_file(), name)
            self.assertGreater((case_root / name).stat().st_size, 0, name)
        with (GALLERY / sample["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 672)
        self.assertEqual({row["value_status"] for row in rows}, {"numeric", "clipped_high", "clipped_low"})

    def test_homepage_paper_cases_keep_article_provenance(self):
        self.assertEqual(len(self.basics["paperCases"]), 2)
        for case in self.basics["paperCases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["journal"], "Nature Communications")
                self.assertTrue(case["articleUrl"].startswith("https://www.nature.com/articles/"))
                for key in ["original", "overlay", "recreated", "data", "report"]:
                    self.assertTrue((GALLERY / case["assets"][key]).is_file())

    def test_manifest_has_three_complementary_cases(self):
        cases = self.manifest["cases"]
        self.assertEqual(len(cases), 3)
        self.assertEqual(
            {case["verification"] for case in cases},
            {
                "official_source_data_mapped",
                "visible_geometry_extracted",
                "partial_visible_geometry",
            },
        )

    def test_case_assets_and_external_metadata(self):
        for case in self.manifest["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["license"], "CC BY 4.0")
                self.assertTrue(case["articleUrl"].startswith("https://www.nature.com/articles/"))
                self.assertTrue(case["figureUrl"].endswith("/figures/2"))
                for key in ["original", "overlay", "recreated", "data", "report", "sourceData"]:
                    asset = GALLERY / case["assets"][key]
                    self.assertTrue(asset.is_file(), f"{case['id']}:{key}")
                    self.assertGreater(asset.stat().st_size, 0, f"{case['id']}:{key}")

                for key in ["original", "overlay", "recreated"]:
                    with Image.open(GALLERY / case["assets"][key]) as image:
                        self.assertGreater(image.width, 200)
                        self.assertGreater(image.height, 150)

    def test_reports_match_manifest_claims(self):
        for case in self.manifest["cases"]:
            report = json.loads((GALLERY / case["assets"]["report"]).read_text(encoding="utf-8"))
            with self.subTest(case=case["id"]):
                self.assertEqual(report["case_id"], case["id"])
                self.assertEqual(report["status"], case["verification"])
                self.assertIn("limitations", report)
                self.assertGreater(len(report["limitations"]), 0)

    def test_download_csvs_are_nonempty(self):
        for case in self.manifest["cases"]:
            with (GALLERY / case["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            with self.subTest(case=case["id"]):
                self.assertGreater(len(rows), 0)

    def test_borneo_axis_scope_is_explicit(self):
        case = next(item for item in self.manifest["cases"] if item["id"] == "nature-borneo-edge")
        report = json.loads((GALLERY / case["assets"]["report"]).read_text(encoding="utf-8"))
        with (GALLERY / case["assets"]["data"]).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(report["source_rows"], 71)
        self.assertEqual(report["panel_a_visible_rows"], 50)
        self.assertEqual(report["panel_a_out_of_range_rows"], 21)
        self.assertEqual(sum(row["panel_a_visible"] == "True" for row in rows), 50)

    def test_challenge_queue_assets_exist(self):
        self.assertGreater(len(self.manifest["challengeQueue"]), 0)
        for item in self.manifest["challengeQueue"]:
            self.assertTrue((GALLERY / item["image"]).is_file())
            self.assertEqual(item["status"], "challenge_queued")


if __name__ == "__main__":
    unittest.main()
