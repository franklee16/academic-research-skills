import unittest

from figure_spec import (
    FigureSpecError,
    assert_valid_figure_spec,
    figure_spec_readiness,
    validate_figure_spec,
)


def base_spec():
    return {
        "schema_version": 1,
        "status": "ready_for_assisted_extraction",
        "source": {
            "media_kind": "raster",
            "coordinate_space": "pixel",
            "measurement_space": "original_raster_pixels",
            "resampling_applied": False,
            "width": 640,
            "height": 480,
            "sha256": "0" * 64,
        },
        "panels": [
            {
                "panel_id": "panel-a",
                "bounds": [20, 20, 620, 460],
                "bounds_verification": "verified",
                "plot_bounds": [40, 30, 610, 450],
                "plot_bounds_verification": "verified",
                "chart_type": "line",
                "coordinate_model": "cartesian_linear",
                "axes": [
                    {
                        "axis_id": "x",
                        "scale": "linear",
                        "verification": "verified",
                        "anchors": [{"pixel": 50, "value": 0}, {"pixel": 600, "value": 10}],
                    },
                    {
                        "axis_id": "y",
                        "scale": "linear",
                        "verification": "verified",
                        "anchors": [{"pixel": 440, "value": 0}, {"pixel": 40, "value": 100}],
                    },
                ],
                "mark_grammars": ["curve"],
                "route": {"route_id": "raster_line_color"},
                "required_confirmations": ["panel_roi", "plot_bounds", "x_axis", "y_axis"],
                "confirmations": {
                    "panel_roi": "verified",
                    "plot_bounds": "verified",
                    "x_axis": "verified",
                    "y_axis": "verified",
                },
            }
        ],
    }


class FigureSpecTests(unittest.TestCase):
    def test_accepts_verified_linear_axes_and_panel_bounds(self):
        spec = base_spec()
        self.assertEqual(validate_figure_spec(spec), [])
        assert_valid_figure_spec(spec)
        self.assertEqual(figure_spec_readiness(spec)["status"], "ready_for_assisted_extraction")

    def test_rejects_out_of_bounds_panel_and_duplicate_anchor_pixels(self):
        spec = base_spec()
        spec["panels"][0]["bounds"] = [-1, 20, 620, 500]
        spec["panels"][0]["axes"][0]["anchors"][1]["pixel"] = 50
        errors = validate_figure_spec(spec)
        self.assertTrue(any("bounds" in error for error in errors))
        self.assertTrue(any("anchor pixels" in error for error in errors))
        with self.assertRaises(FigureSpecError):
            assert_valid_figure_spec(spec)

    def test_distinguishes_raw_log_values_from_displayed_log_coordinates(self):
        raw_log = base_spec()
        raw_log["panels"][0]["coordinate_model"] = "cartesian_log_x"
        raw_log["panels"][0]["axes"][0]["scale"] = "log10"
        raw_log["panels"][0]["axes"][0]["anchors"] = [
            {"pixel": 50, "value": -10},
            {"pixel": 600, "value": -2},
        ]
        self.assertTrue(any("positive" in error for error in validate_figure_spec(raw_log)))

        displayed_log = base_spec()
        displayed_log["panels"][0]["coordinate_model"] = "cartesian_displayed_log_x"
        displayed_log["panels"][0]["axes"][0]["scale"] = "displayed_log10"
        displayed_log["panels"][0]["axes"][0]["anchors"] = [
            {"pixel": 50, "value": -10},
            {"pixel": 600, "value": -2},
        ]
        self.assertEqual(validate_figure_spec(displayed_log), [])

    def test_ready_status_rejects_an_unverified_required_confirmation(self):
        spec = base_spec()
        spec["panels"][0]["confirmations"]["x_axis"] = "proposed"
        errors = validate_figure_spec(spec)
        self.assertTrue(any("x_axis" in error and "must be verified" in error for error in errors))

    def test_rejects_resampled_raster_measurement_contract(self):
        spec = base_spec()
        spec["source"]["resampling_applied"] = True
        self.assertTrue(any("resampling_applied" in error for error in validate_figure_spec(spec)))


if __name__ == "__main__":
    unittest.main()
