import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

try:
    from candidate_digitize_scatter import extract_scatter_points
except ImportError:  # pragma: no cover - package-style unittest invocation
    from .candidate_digitize_scatter import extract_scatter_points


ROOT = Path(__file__).resolve().parents[1]


def _fixture(path: Path, *, include_points: bool = True) -> tuple[Path, list[tuple[int, int]]]:
    image = Image.new("RGB", (210, 150), "white")
    draw = ImageDraw.Draw(image)
    plot = (20, 18, 190, 128)
    draw.line((20, 18, 20, 128), fill="#222222", width=2)
    draw.line((20, 128, 190, 128), fill="#222222", width=2)
    draw.polygon(
        [(24, 52), (186, 76), (186, 105), (24, 83)],
        fill="#dbe8f3",
    )
    draw.line((24, 67, 186, 91), fill="#0058a2", width=3)
    # Text-like and tick-like dark strokes must not become points.
    draw.line((32, 29, 75, 29), fill="#222222", width=2)
    draw.line((32, 29, 32, 35), fill="#222222", width=2)
    for x in (55, 100, 145):
        draw.line((x, 125, x, 132), fill="#222222", width=2)

    centers = [(48, 57), (78, 79), (88, 79), (124, 49), (158, 101)]
    if include_points:
        for x, y in centers:
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#282829")
    image.save(path)
    return path, centers


class CandidateScatterExtractorTests(unittest.TestCase):
    def test_splits_touching_dark_markers_without_detecting_axes_band_or_line(self):
        with tempfile.TemporaryDirectory() as temporary:
            image_path, truth = _fixture(Path(temporary) / "scatter.png")
            report = extract_scatter_points(
                image_path,
                plot_bounds=(20, 18, 190, 128),
                x_anchors=[(20.0, 0.0), (190.0, 10.0)],
                y_anchors=[(18.0, 10.0), (128.0, 0.0)],
                marker_mode="dark",
                dark_threshold=105,
                min_radius=3.0,
                max_radius=8.0,
            )

        self.assertEqual(report["status"], "candidate")
        self.assertTrue(report["numeric_output_authorized"])
        self.assertEqual(len(report["points"]), len(truth))
        observed = [(point["pixel_x"], point["pixel_y"]) for point in report["points"]]
        for expected_x, expected_y in truth:
            self.assertTrue(
                any(
                    abs(observed_x - expected_x) <= 1.0
                    and abs(observed_y - expected_y) <= 1.0
                    for observed_x, observed_y in observed
                )
            )
        self.assertTrue(
            any(component["peak_count"] == 2 for component in report["components"])
        )

    def test_refuses_line_and_text_only_panel(self):
        with tempfile.TemporaryDirectory() as temporary:
            image_path, _ = _fixture(
                Path(temporary) / "scatter-without-points.png",
                include_points=False,
            )
            report = extract_scatter_points(
                image_path,
                plot_bounds=(20, 18, 190, 128),
                x_anchors=[(20.0, 0.0), (190.0, 10.0)],
                y_anchors=[(18.0, 10.0), (128.0, 0.0)],
                marker_mode="dark",
                dark_threshold=105,
                min_radius=3.0,
                max_radius=8.0,
            )

        self.assertEqual(report["status"], "low_confidence")
        self.assertFalse(report["numeric_output_authorized"])
        self.assertEqual(report["points"], [])

    def test_relaxed_residual_audit_blocks_a_low_contrast_marker_without_adding_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            image_path, truth = _fixture(Path(temporary) / "scatter.png")
            with Image.open(image_path) as source:
                image = source.convert("RGB")
            draw = ImageDraw.Draw(image)
            draw.ellipse((172, 37, 182, 47), fill="#777777")
            image.save(image_path)
            report = extract_scatter_points(
                image_path,
                plot_bounds=(20, 18, 190, 128),
                x_anchors=[(20.0, 0.0), (190.0, 10.0)],
                y_anchors=[(18.0, 10.0), (128.0, 0.0)],
                marker_mode="dark",
                dark_threshold=105,
                min_radius=3.0,
                max_radius=8.0,
            )

        self.assertEqual(len(report["points"]), len(truth))
        self.assertEqual(report["status"], "low_confidence")
        self.assertFalse(report["numeric_output_authorized"])
        self.assertEqual(report["residual_audit"]["status"], "review_required")
        self.assertEqual(report["residual_audit"]["residual_candidate_count"], 1)
        self.assertEqual(
            report["residual_audit"]["candidates"][0]["reason_code"],
            "detector_residual",
        )

    def test_annotated_correlation_is_validation_only_and_blocks_mismatch(self):
        with tempfile.TemporaryDirectory() as temporary:
            image_path, _ = _fixture(Path(temporary) / "scatter.png")
            report = extract_scatter_points(
                image_path,
                plot_bounds=(20, 18, 190, 128),
                x_anchors=[(20.0, 0.0), (190.0, 10.0)],
                y_anchors=[(18.0, 10.0), (128.0, 0.0)],
                marker_mode="dark",
                dark_threshold=105,
                min_radius=3.0,
                max_radius=8.0,
                annotated_pearson_r=-0.99,
                pearson_tolerance=0.01,
            )

        self.assertEqual(report["status"], "low_confidence")
        self.assertFalse(report["numeric_output_authorized"])
        self.assertEqual(len(report["points"]), 5)
        self.assertEqual(report["validation"]["status"], "mismatch")
        self.assertIn("never used to add, remove, or move points", report["validation"]["role"])

    def test_real_fig5e_panels_recover_visible_points_without_expected_count_input(self):
        image_path = (
            ROOT
            / "gallery"
            / "assets"
            / "cases"
            / "nature-70099-fig5e"
            / "original.png"
        )
        panels = (
            ((106, 91, 340, 304), [(150.5, 0.04), (321.5, 0.10)], -0.57, 17),
            ((403, 91, 638, 304), [(424.0, 10.0), (627.0, 30.0)], -0.34, 16),
            ((700, 91, 936, 304), [(736.5, 50.0), (898.5, 200.0)], 0.12, 15),
        )
        for bounds, x_anchors, annotated_r, expected_visible_count in panels:
            with self.subTest(bounds=bounds):
                report = extract_scatter_points(
                    image_path,
                    plot_bounds=bounds,
                    x_anchors=x_anchors,
                    y_anchors=[(100.5, 3.0), (293.5, 1.0)],
                    marker_mode="dark",
                    annotated_pearson_r=annotated_r,
                )
                self.assertEqual(report["status"], "candidate")
                self.assertTrue(report["numeric_output_authorized"])
                self.assertEqual(len(report["points"]), expected_visible_count)
                self.assertEqual(report["validation"]["status"], "matched")
                self.assertLess(report["validation"]["absolute_difference"], 0.01)


if __name__ == "__main__":
    unittest.main()
