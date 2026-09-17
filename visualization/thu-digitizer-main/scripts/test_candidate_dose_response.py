import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

from candidate_digitize_dose_response_pdf import (  # noqa: E402
    LinearCalibration,
    SeriesSpec,
    extract_dose_response_pdf,
)


class DoseResponsePdfCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf = (
            ROOT
            / "gallery"
            / "assets"
            / "cases"
            / "nature-kahlous-dose-response"
            / "source-article.pdf"
        )
        cls.result = extract_dose_response_pdf(
            cls.pdf,
            page_number=7,
            panel_roi=(55.0, 178.0, 235.0, 310.0),
            main_plot_roi=(106.7, 213.8, 192.3, 280.8),
            x_calibration=LinearCalibration(116.836998, -10.0, 192.264999, -2.0),
            y_calibration=LinearCalibration(277.919006, 0.0, 222.200012, 100.0),
            series_specs=[
                SeriesSpec("ADR", "square", "#ffba12", "#ffba10"),
                SeriesSpec("NA", "triangle", "#748d8e", "#758c8e"),
                SeriesSpec("DA", "circle", "#48e99d", "#48ea9c"),
            ],
        )

    def test_real_panel_recovers_all_visible_marker_and_curve_geometry(self):
        self.assertEqual(
            self.result["summary"],
            {
                "visible_marker_count": 21,
                "main_marker_count": 18,
                "vehicle_marker_count": 3,
                "visible_error_bar_count": 14,
                "traced_curve_count": 3,
            },
        )
        self.assertEqual({point["series"] for point in self.result["points"]}, {"ADR", "NA", "DA"})
        self.assertTrue(all(curve["status"] == "curve_path_traced" for curve in self.result["curves"]))
        self.assertTrue(all(len(curve["points"]) > 200 for curve in self.result["curves"]))

    def test_log_coordinate_and_broken_vehicle_segment_stay_distinct(self):
        for series in {"ADR", "NA", "DA"}:
            points = [point for point in self.result["points"] if point["series"] == series]
            vehicle = [point for point in points if point["segment"] == "vehicle"]
            main = sorted(
                (point for point in points if point["segment"] == "main"),
                key=lambda point: point["log10_molar"],
            )
            self.assertEqual(len(vehicle), 1)
            self.assertIsNone(vehicle[0]["log10_molar"])
            self.assertEqual([round(point["log10_molar"]) for point in main], [-9, -8, -7, -6, -5, -4])
            self.assertTrue(all(point["status"] == "vector_marker_extracted" for point in points))


if __name__ == "__main__":
    unittest.main()
