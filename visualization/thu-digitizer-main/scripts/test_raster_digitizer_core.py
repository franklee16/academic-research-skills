import unittest

import numpy as np

from raster_digitizer_core import AxisCalibration, sample_traced_path, trace_colour_path


class RasterCoreTests(unittest.TestCase):
    def test_robust_calibration_downweights_bad_tick(self):
        calibration = AxisCalibration.fit(
            [(0, 0), (100, 10), (200, 20), (300, 45)],
        )
        self.assertAlmostEqual(calibration.value_at_pixel(250), 25.0, delta=0.25)
        self.assertGreater(calibration.residuals_pixels[-1], 100.0)
        self.assertLess(calibration.max_abs_residual_transformed, 20.0)

    def test_log10_calibration_maps_displayed_ticks(self):
        calibration = AxisCalibration.fit([(10, 1), (110, 100)], scale="log10")
        self.assertAlmostEqual(calibration.value_at_pixel(10), 1.0, places=6)
        self.assertAlmostEqual(calibration.value_at_pixel(60), 10.0, places=6)
        self.assertAlmostEqual(calibration.value_at_pixel(110), 100.0, places=6)
        self.assertGreater(calibration.uncertainty_at_pixel(60), 0.0)

    def test_continuity_trace_keeps_curve_after_a_blank_column(self):
        height, width = 80, 160
        image = np.full((height, width, 3), 255, dtype=np.uint8)
        target = np.asarray((35, 95, 190), dtype=np.uint8)
        truth = {}
        for x in range(10, 150):
            y = int(round(40 + 12 * np.sin(x / 18.0)))
            truth[x] = y
            if x not in {72, 73}:
                image[max(0, y - 1) : min(height, y + 2), x] = target

        trace = trace_colour_path(
            image,
            target=tuple(int(value) for value in target),
            plot_bounds=(10, 10, 149, 70),
            sigma=16,
            tolerance=20,
            score_threshold=0.25,
            smoothness=0.08,
            gap_penalty=0.75,
            max_step=5,
        )
        self.assertGreater(trace["coverage"], 0.9)
        self.assertEqual(trace["path"][72 - 10]["status"], "gap")
        observed = {
            item["x_pixel"]: item["y_pixel"]
            for item in trace["path"]
            if item["y_pixel"] is not None
        }
        errors = [abs(observed[x] - truth[x]) for x in observed if x in truth]
        self.assertLessEqual(float(np.percentile(errors, 95)), 2.0)

    def test_sampling_never_interpolates_missing_trace(self):
        trace = {
            "path": [
                {"x_pixel": 0, "y_pixel": 10, "support": 2, "uncertainty_px": 0.5},
                {"x_pixel": 1, "y_pixel": None, "support": 0, "uncertainty_px": None},
                {"x_pixel": 2, "y_pixel": 12, "support": 2, "uncertainty_px": 0.5},
            ]
        }
        x_axis = AxisCalibration.fit([(0, 0), (2, 2)])
        y_axis = AxisCalibration.fit([(0, 20), (20, 0)])
        sampled = sample_traced_path(
            trace,
            x_values=[1],
            x_axis=x_axis,
            y_axis=y_axis,
            sample_radius_px=0,
        )
        self.assertEqual(sampled[0]["status"], "not_extracted")
        self.assertIsNone(sampled[0]["y"])


if __name__ == "__main__":
    unittest.main()
