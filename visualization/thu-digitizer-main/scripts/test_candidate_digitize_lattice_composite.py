import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

try:
    from candidate_digitize_lattice_composite import extract_lattice_composite
    from source_coordinate_contract import raster_identity
except ImportError:  # pragma: no cover - package-style invocation
    from .candidate_digitize_lattice_composite import extract_lattice_composite
    from .source_coordinate_contract import raster_identity


ROOT = Path(__file__).resolve().parents[1]


def synthetic_fixture(path: Path):
    image = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(image)
    dark = (59, 59, 59)
    blue = (86, 180, 233)
    inactive = (233, 233, 233)
    xs = [320, 380, 440, 500, 560]
    ys = [360, 410, 460, 510]
    values = [80, 60, 40, 20, 10]
    memberships = [{"A", "D"}, {"B", "D"}, {"B"}, {"A"}, {"C"}]
    totals = {name: sum(value for value, members in zip(values, memberships) if name in members) for name in "ABCD"}
    baseline = 320
    for x, value in zip(xs, values):
        draw.rectangle((x - 7, baseline - value * 2, x + 7, baseline - 1), fill=dark)
    for y, name in zip(ys, "ABCD"):
        left = 250 - totals[name]
        draw.rectangle((left, y - 4, 249, y + 4), fill=blue)
    for x, members in zip(xs, memberships):
        for y, name in zip(ys, "ABCD"):
            colour = dark if name in members else inactive
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=colour)
    image.save(path)
    return values, totals


def synthetic_config(path: Path, values):
    return {
        "schema_version": 1,
        "source": raster_identity(path).as_dict(),
        "layers": {
            "column_bars": {
                "roi": [280, 100, 600, 330],
                "color": [59, 59, 59],
                "color_verification": "verified",
                "tolerance": 0,
                "width_range": [12, 18],
            },
            "row_bars": {
                "roi": [80, 330, 270, 540],
                "color": [86, 180, 233],
                "color_verification": "verified",
                "tolerance": 0,
                "height_range": [7, 11],
                "min_area": 40,
                "min_row_pixels": 4,
            },
            "membership": {
                "color": [59, 59, 59],
                "color_verification": "verified",
                "tolerance": 0,
                "patch_radius": 6,
                "active_fraction_min": 0.35,
                "inactive_fraction_max": 0.05,
            },
        },
        "semantics": {
            "verification": "verified",
            "column_ids": [f"I{index}" for index in range(1, 6)],
            "column_values": values,
            "row_ids": list("ABCD"),
            "row_types": ["T1", "T2", "T1", "T3"],
        },
        "validation": {
            "max_spacing_cv": 0.02,
            "row_value_axis": [{"pixel": 250, "value": 0}, {"pixel": 50, "value": 200}],
            "row_total_max_abs_error": 0.01,
            "top_value_max_abs_error": 0.01,
        },
    }


def multicolour_gapped_fixture(path: Path):
    image = Image.new("RGB", (680, 460), "white")
    draw = ImageDraw.Draw(image)
    dark = (65, 65, 65)
    row_colours = [(190, 99, 29), (101, 149, 47), (207, 65, 137)]
    xs = [330, 400, 470, 540]
    ys = [300, 350, 400]
    values = [80, 70, 60, 50]
    memberships = [{"A", "C"}, {"A", "B"}, {"B"}, {"A", "B", "C"}]
    baseline = 250
    tops = []
    for x, value in zip(xs, values):
        top = baseline - value * 2
        tops.append(top)
        draw.rectangle((x - 10, top, x + 10, baseline - 1), fill=dark)
    # Publication gridlines can split an otherwise continuous rendered bar.
    draw.rectangle((300, 198, 570, 201), fill=(204, 204, 204))
    for y, colour in zip(ys, row_colours):
        draw.rectangle((80, y - 7, 250, y + 7), fill=colour)
    for x, members in zip(xs, memberships):
        for y, row_id, colour in zip(ys, "ABC", row_colours):
            if row_id in members:
                draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=colour)
    image.save(path)
    return values, memberships, tops


def multicolour_gapped_config(path: Path, values):
    row_colours = [[190, 99, 29], [101, 149, 47], [207, 65, 137]]
    return {
        "schema_version": 1,
        "source": raster_identity(path).as_dict(),
        "layers": {
            "column_bars": {
                "roi": [290, 70, 580, 260],
                "color": [65, 65, 65],
                "color_verification": "verified",
                "tolerance": 0,
                "width_range": [18, 24],
                "max_vertical_gap_px": 5,
                "min_vertical_row_fraction": 0.7,
            },
            "row_bars": {
                "roi": [60, 280, 270, 420],
                "colors": row_colours,
                "color_verification": "verified",
                "tolerance": 0,
                "height_range": [13, 17],
                "min_area": 100,
                "min_row_pixels": 20,
            },
            "membership": {
                "colors": row_colours,
                "color_verification": "verified",
                "tolerance": 0,
                "patch_radius": 9,
                "active_fraction_min": 0.45,
                "inactive_fraction_max": 0.02,
            },
        },
        "semantics": {
            "verification": "verified",
            "column_ids": ["I1", "I2", "I3", "I4"],
            "column_values": values,
            "row_ids": list("ABC"),
            "row_types": [],
        },
        "validation": {
            "max_spacing_cv": 0.02,
            "row_value_axis": [],
            "top_value_max_abs_error": 0.01,
        },
    }


class LatticeCompositeCandidateTests(unittest.TestCase):
    def test_synthetic_geometry_is_complete_and_independently_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "synthetic.png"
            values, totals = synthetic_fixture(image_path)
            report = extract_lattice_composite(image_path, synthetic_config(image_path, values))
        self.assertEqual(report["status"], "candidate")
        self.assertTrue(report["geometry_output_authorized"])
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_count"], 5)
        self.assertEqual(report["geometry"]["row_count"], 4)
        self.assertEqual(report["geometry"]["cell_count"], 20)
        self.assertEqual(report["geometry"]["active_cell_count"], 7)
        self.assertEqual(report["geometry"]["ambiguous_cell_count"], 0)
        self.assertEqual({row["row_id"]: int(row["derived_total"]) for row in report["row_bars"]}, totals)
        self.assertLess(report["validation"]["row_totals_vs_bars"]["max_abs_error"], 0.01)

    def test_resized_copy_is_rejected_before_measurement(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / "original.png"
            resized = Path(directory) / "resized.png"
            values, _ = synthetic_fixture(original)
            with Image.open(original) as image:
                image.resize((400, 300)).save(resized)
            config = synthetic_config(original, values)
            with self.assertRaisesRegex(ValueError, "original-raster contract"):
                extract_lattice_composite(resized, config)

    def test_multicolour_layers_and_gridline_split_bars_are_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "multicolour-gapped.png"
            values, memberships, tops = multicolour_gapped_fixture(image_path)
            report = extract_lattice_composite(
                image_path,
                multicolour_gapped_config(image_path, values),
            )
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_count"], 4)
        self.assertEqual(report["geometry"]["row_count"], 3)
        self.assertEqual(report["geometry"]["active_cell_count"], sum(map(len, memberships)))
        self.assertEqual(report["geometry"]["ambiguous_cell_count"], 0)
        self.assertEqual([bar["top_px"] for bar in report["column_bars"]], tops)
        self.assertLess(report["validation"]["top_bars_vs_values"]["max_abs_error"], 0.01)

    def test_membership_glyphs_can_supply_complete_column_guides(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "membership-guides.png"
            values, _ = synthetic_fixture(image_path)
            config = synthetic_config(image_path, values)
            config["layers"]["column_bars"] = {
                "role": "membership_guides",
                "roi": [280, 354, 600, 367],
                "colors": [[59, 59, 59], [233, 233, 233]],
                "color_verification": "verified",
                "tolerance": 0,
                "width_range": [9, 13],
            }
            config["validation"]["top_value_max_abs_error"] = None
            report = extract_lattice_composite(image_path, config)
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_guide_role"], "membership_guides")
        self.assertEqual(report["geometry"]["column_count"], 5)
        self.assertEqual(report["geometry"]["active_cell_count"], 7)
        self.assertEqual(
            report["validation"]["top_bars_vs_values"]["status"],
            "not_applicable_membership_derived_column_guides",
        )

    def test_real_upset_regression_detects_geometry_without_expected_counts(self):
        image_path = ROOT / "gallery" / "assets" / "cases" / "nature-27341-fig1" / "original.png"
        row_ids = [
            "Pa26T1", "Pa26T2", "Pa29T1", "Pa29T2", "Pa29T4", "Pa30T1", "Pa30T2",
            "Pa31T1", "Pa31T2", "Pa33T1", "Pa33T2", "Pa34T1", "Pa34T2", "Pa35T1",
            "Pa35T2", "Pa36T1", "Pa36T2", "Pa37T1", "Pa37T2",
        ]
        config = {
            "schema_version": 1,
            "source": raster_identity(image_path).as_dict(),
            "layers": {
                "column_bars": {"roi_fraction": [0.25, 0.05, 0.92, 0.70], "color": [59, 59, 59], "color_verification": "verified", "tolerance": 0, "width_range": [20, 30]},
                "row_bars": {"roi_fraction": [0, 0.65, 0.25, 0.98], "color": [86, 180, 233], "color_verification": "verified", "tolerance": 0, "height_range": [5, 20], "min_area": 300, "min_row_pixels": 5},
                "membership": {"color": [59, 59, 59], "color_verification": "verified", "tolerance": 0, "patch_radius": 7, "active_fraction_min": 0.4, "inactive_fraction_max": 0.05},
            },
            "semantics": {
                "verification": "verified",
                "column_ids": [f"I{index:02d}" for index in range(1, 31)],
                "column_values": [998, 802, 684, 675, 500, 441, 287, 278, 229, 124, 117, 110, 110, 108, 83, 71, 62, 41, 40, 40, 39, 38, 37, 28, 23, 21, 16, 9, 7, 4],
                "row_ids": row_ids,
                "row_types": ["LCNEC", "LUAD", "LCNEC", "LUSC", "NSCLC-NOS", "LCNEC", "LUAD", "SCLC", "LUAD", "LCNEC", "LUSC", "LCNEC", "LUAD", "SCLC", "LUAD", "SCLC", "LUSC", "LUAD", "LCNEC"],
            },
            "validation": {
                "max_spacing_cv": 0.02,
                "row_value_axis": [
                    {"pixel": 31.5, "value": 1250}, {"pixel": 105, "value": 1000},
                    {"pixel": 178.5, "value": 750}, {"pixel": 252, "value": 500},
                    {"pixel": 325.5, "value": 250}, {"pixel": 399, "value": 0},
                ],
                "row_bar_edge_offset_px": 1,
                "row_total_max_abs_error": 3,
                "top_value_max_abs_error": 1,
            },
        }
        report = extract_lattice_composite(image_path, config)
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_count"], 30)
        self.assertEqual(report["geometry"]["row_count"], 19)
        self.assertEqual(report["geometry"]["cell_count"], 570)
        self.assertEqual(report["geometry"]["active_cell_count"], 42)
        self.assertEqual(report["geometry"]["ambiguous_cell_count"], 0)
        self.assertAlmostEqual(report["column_bars"][0]["pixel_x"], 560.5)
        self.assertAlmostEqual(report["row_bars"][0]["pixel_y"], 1119.0)

    def test_real_four_set_upset_uses_pixels_before_source_validation(self):
        root = ROOT / "gallery" / "assets" / "cases" / "nature-19006-fig2b"
        config = json.loads((root / "lattice-config.json").read_text(encoding="utf-8"))
        report = extract_lattice_composite(root / "original.png", config)
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_count"], 15)
        self.assertEqual(report["geometry"]["row_count"], 4)
        self.assertEqual(report["geometry"]["cell_count"], 60)
        self.assertEqual(report["geometry"]["active_cell_count"], 32)
        self.assertEqual(report["geometry"]["ambiguous_cell_count"], 0)
        self.assertEqual(report["geometry"]["row_guide_role"], "membership_guides")
        self.assertEqual(
            [bar["members"] for bar in report["column_bars"][:4]],
            [
                ["FunC-2", "FunC-4", "FunC-3", "FunC-1"],
                ["FunC-1"],
                ["FunC-3"],
                ["FunC-4", "FunC-3", "FunC-1"],
            ],
        )
        self.assertLess(report["validation"]["top_bars_vs_values"]["max_abs_error"], 4)

    def test_real_multicolour_upset_recovers_every_membership_node(self):
        root = ROOT / "gallery" / "assets" / "cases" / "nature-28348-fig7"
        config = json.loads((root / "lattice-config.json").read_text(encoding="utf-8"))
        report = extract_lattice_composite(root / "original.png", config)
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(report["geometry"]["column_count"], 12)
        self.assertEqual(report["geometry"]["row_count"], 5)
        self.assertEqual(report["geometry"]["cell_count"], 60)
        self.assertEqual(report["geometry"]["active_cell_count"], 40)
        self.assertEqual(report["geometry"]["ambiguous_cell_count"], 0)
        self.assertEqual(report["geometry"]["column_guide_role"], "membership_guides")
        self.assertEqual(
            {row["row_id"]: int(row["derived_total"]) for row in report["row_bars"]},
            {
                "Direct Match": 8786,
                "Non-Synon": 8767,
                "Position-Specific": 6251,
                "Diagnosis Match": 6219,
                "AMP Tier I": 3797,
            },
        )
        self.assertEqual(
            report["validation"]["top_bars_vs_values"]["status"],
            "not_applicable_membership_derived_column_guides",
        )


if __name__ == "__main__":
    unittest.main()
