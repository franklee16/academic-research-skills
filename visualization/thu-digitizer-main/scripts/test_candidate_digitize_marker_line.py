import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from candidate_digitize_marker_line import extract_marker_line, write_evidence_bundle
from raster_digitizer_core import AxisCalibration


WIDTH, HEIGHT = 300, 220
BOUNDS = (30, 20, 270, 190)
SAMPLES = list(range(11))
VALUES = [4, 5, 6, 7, 9, 11, 12, 10, 7, 5, 4]
OUTSIDE = (251, 129, 119)
INSIDE = (252, 106, 98)


def calibrations():
    return (
        AxisCalibration.fit([(40, 0), (260, 10)], scale="linear"),
        AxisCalibration.fit([(180, 0), (30, 15)], scale="linear"),
    )


def fixture(*, markers=True, shaded=True):
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    x_axis, y_axis = calibrations()
    shade_left = 150
    if shaded:
        draw.rectangle((shade_left, BOUNDS[1], BOUNDS[2], BOUNDS[3]), fill=(245, 235, 235))
    points = [
        (round(x_axis.pixel_at_value(x)), round(y_axis.pixel_at_value(y)))
        for x, y in zip(SAMPLES, VALUES)
    ]
    for first, second in zip(points, points[1:]):
        colour = INSIDE if (first[0] + second[0]) / 2 >= shade_left and shaded else OUTSIDE
        draw.line((*first, *second), fill=colour, width=1)
    reference_y = round(y_axis.pixel_at_value(8))
    for left in range(BOUNDS[0], BOUNDS[2] + 1, 10):
        colour = INSIDE if left >= shade_left and shaded else OUTSIDE
        draw.line((left, reference_y, min(left + 5, BOUNDS[2]), reference_y), fill=colour, width=1)
    if markers:
        for x_pixel, y_pixel in points:
            colour = INSIDE if x_pixel >= shade_left and shaded else OUTSIDE
            draw.ellipse((x_pixel - 4, y_pixel - 4, x_pixel + 4, y_pixel + 4), fill=colour)
    return image


class MarkerLineCandidateTests(unittest.TestCase):
    def test_global_path_prefers_compact_markers_over_same_colour_reference_dashes(self):
        image = fixture()
        x_axis, y_axis = calibrations()
        result = extract_marker_line(
            np.asarray(image),
            plot_bounds=BOUNDS,
            x_axis=x_axis,
            y_axis=y_axis,
            sample_values=SAMPLES,
            series=[("curve", [OUTSIDE, INSIDE])],
            color_tolerance=2,
            sample_radius=7,
            marker_radius_min=3,
            reference_lines=[8],
        )
        observations = result["series"]["curve"]["observations"]
        self.assertTrue(result["numeric_output_authorized"])
        self.assertTrue(all(item["status"] == "extracted" for item in observations))
        self.assertLessEqual(
            max(abs(item["value"] - truth) for item, truth in zip(observations, VALUES)),
            0.11,
        )
        self.assertTrue(any(len(candidates) > 1 for candidates in result["series"]["curve"]["candidate_sets"]))

    def test_background_dependent_marker_templates_are_bound_to_one_series(self):
        image = fixture()
        x_axis, y_axis = calibrations()
        result = extract_marker_line(
            np.asarray(image),
            plot_bounds=BOUNDS,
            x_axis=x_axis,
            y_axis=y_axis,
            sample_values=SAMPLES,
            series=[("curve", [OUTSIDE, INSIDE])],
            color_tolerance=2,
            sample_radius=7,
            marker_radius_min=3,
            reference_lines=[8],
        )
        dominant = [item["dominant_template_index"] for item in result["series"]["curve"]["observations"]]
        self.assertIn(0, dominant)
        self.assertIn(1, dominant)

    def test_line_only_panel_refuses_numeric_output(self):
        image = fixture(markers=False, shaded=False)
        x_axis, y_axis = calibrations()
        result = extract_marker_line(
            np.asarray(image),
            plot_bounds=BOUNDS,
            x_axis=x_axis,
            y_axis=y_axis,
            sample_values=SAMPLES,
            series=[("curve", [OUTSIDE])],
            color_tolerance=2,
            sample_radius=7,
            marker_radius_min=3,
            reference_lines=[8],
        )
        self.assertFalse(result["numeric_output_authorized"])
        self.assertEqual(result["status"], "low_confidence")
        self.assertTrue(all(item["value"] is None for item in result["series"]["curve"]["observations"]))

    def test_evidence_directory_is_immutable_and_reports_implementation_hash(self):
        image = fixture()
        x_axis, y_axis = calibrations()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "fixture.png"
            image.save(source)
            arguments = dict(
                input_path=source,
                output_root=root / "runs",
                plot_bounds=BOUNDS,
                x_axis=x_axis,
                y_axis=y_axis,
                sample_values=SAMPLES,
                series=[("curve", [OUTSIDE, INSIDE])],
                color_tolerance=2,
                sample_radius=7,
                marker_radius_min=3,
                reference_lines=[8],
                transition_weight=0.08,
                curvature_weight=0.03,
                confidence_threshold=0.55,
            )
            output = write_evidence_bundle(**arguments)
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(len(report["implementation_sha256"]), 64)
            self.assertTrue((output / "data.csv").is_file())
            self.assertTrue((output / "evidence.csv").is_file())
            self.assertTrue((output / "overlay.png").is_file())
            with self.assertRaises(FileExistsError):
                write_evidence_bundle(**arguments)


if __name__ == "__main__":
    unittest.main()
