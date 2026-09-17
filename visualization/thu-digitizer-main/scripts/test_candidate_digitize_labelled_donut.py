import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from candidate_digitize_labelled_donut import extract_labelled_donuts


ROOT = Path(__file__).resolve().parents[1]


def fixture(path: Path) -> Path:
    image = Image.new("RGB", (240, 240), "white")
    draw = ImageDraw.Draw(image)
    draw.pieslice((40, 40, 200, 200), -90, 54, fill="#d62728")
    draw.pieslice((40, 40, 200, 200), 54, 270, fill="#1f77b4")
    draw.ellipse((90, 90, 150, 150), fill="white")
    image.save(path)
    return path


def config(first="20", second="30"):
    return {
        "schema_version": 1,
        "panel_bounds": [0, 0, 239, 239],
        "palette": {"red": "#d62728", "blue": "#1f77b4"},
        "groups": [
            {
                "name": "A",
                "center": [120, 120],
                "radial_band": [45, 70],
                "labels": [
                    {
                        "series": "red",
                        "anchor": [185, 60],
                        "transcription_a": first,
                        "transcription_b": first,
                    },
                    {
                        "series": "blue",
                        "anchor": [30, 160],
                        "transcription_a": second,
                        "transcription_b": second,
                    },
                ],
            }
        ],
        "parameters": {"maximum_geometry_error_pp": 3.0},
    }


class CandidateLabelledDonutTests(unittest.TestCase):
    def test_visible_values_are_authorized_without_forcing_sum_to_100(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture(Path(directory) / "donut.png")
            report = extract_labelled_donuts(path, config())

        self.assertEqual(report["status"], "candidate")
        self.assertTrue(report["numeric_output_authorized"])
        self.assertFalse(report["primary_values_normalized_or_forced_to_100"])
        self.assertEqual(
            sum(record["displayed_value_percent"] for record in report["records"]),
            50.0,
        )
        self.assertTrue(all(record["numeric_output_authorized"] for record in report["records"]))

    def test_disagreeing_transcriptions_are_not_authorized(self):
        broken = config()
        broken["groups"][0]["labels"][0]["transcription_b"] = "21"
        with tempfile.TemporaryDirectory() as directory:
            path = fixture(Path(directory) / "donut.png")
            report = extract_labelled_donuts(path, broken)

        first = report["records"][0]
        self.assertEqual(first["status"], "low_confidence")
        self.assertEqual(first["reason_code"], "ambiguous_geometry")
        self.assertFalse(first["numeric_output_authorized"])

    def test_real_fig1f_case_generalizes_from_case_local_configuration(self):
        case_root = ROOT / "gallery" / "assets" / "cases" / "nature-40822-fig1f"
        module_path = case_root / "candidate_digitize_donut_case.py"
        spec = importlib.util.spec_from_file_location("fig1f_case", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        shared_config = {
            "schema_version": 1,
            "source_contract": {
                "sha256": module.EXPECTED_SOURCE_SHA256,
                "dimensions": list(module.EXPECTED_SOURCE_SIZE),
            },
            "panel_bounds": [
                module.PANEL_BOX[0],
                module.PANEL_BOX[1],
                module.PANEL_BOX[2] - 1,
                module.PANEL_BOX[3] - 1,
            ],
            "palette": {name: value["hex"] for name, value in module.PALETTE.items()},
            "groups": [
                {
                    "name": group,
                    "center": list(meta["center"]),
                    "radial_band": list(meta["radial_band"]),
                    "labels": [
                        {
                            "series": cell_type,
                            "anchor": list(anchor),
                            "transcription_a": f"{value:.1f}",
                            "transcription_b": f"{value:.1f}",
                        }
                        for label_group, cell_type, value, anchor in module.VISIBLE_LABELS
                        if label_group == group
                    ],
                }
                for group, meta in module.DONUTS.items()
            ],
            "parameters": {
                "angle_samples": 7200,
                "color_tolerance": 20.0,
                "minimum_sector_share_percent": 0.5,
                "maximum_geometry_error_pp": 2.0,
            },
        }
        report = extract_labelled_donuts(
            case_root / "measurement-source.png", shared_config
        )

        self.assertEqual(report["status"], "candidate")
        self.assertEqual(report["coverage_ledger"]["authorized_slot_count"], 18)
        self.assertLessEqual(
            report["geometry_validation"]["maximum_absolute_error_pp"], 2.0
        )


if __name__ == "__main__":
    unittest.main()
