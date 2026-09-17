import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from run_marker_line_spec import MarkerLineSpecError, bind_panel, execute_spec
from test_candidate_digitize_marker_line import BOUNDS, HEIGHT, INSIDE, OUTSIDE, SAMPLES, WIDTH, fixture


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_spec(source):
    confirmations = {
        "panel_roi": "verified",
        "plot_bounds": "verified",
        "x_axis": "verified",
        "y_axis": "verified",
        "axis_transform": "verified",
        "series_colors": "verified",
        "sample_positions": "verified",
        "compact_filled_marker_grammar": "verified",
        "reference_line_conflicts": "verified",
        "overlay_review": "verified",
        "anchor_residual_review": "verified",
    }
    return {
        "schema_version": 1,
        "status": "ready_for_assisted_extraction",
        "source": {
            "input_file": str(source),
            "sha256": sha256(source),
            "media_kind": "raster",
            "coordinate_space": "pixel",
            "measurement_space": "original_raster_pixels",
            "resampling_applied": False,
            "width": WIDTH,
            "height": HEIGHT,
        },
        "panels": [
            {
                "panel_id": "panel-a",
                "bounds": [10, 10, 290, 200],
                "bounds_verification": "verified",
                "plot_bounds": list(BOUNDS),
                "plot_bounds_verification": "verified",
                "chart_type": "marker_line",
                "coordinate_model": "cartesian_linear",
                "axes": [
                    {
                        "axis_id": "x",
                        "orientation": "x",
                        "scale": "linear",
                        "verification": "verified",
                        "anchors": [{"pixel": 40, "value": 0}, {"pixel": 260, "value": 10}],
                    },
                    {
                        "axis_id": "y",
                        "orientation": "y",
                        "scale": "linear",
                        "verification": "verified",
                        "anchors": [{"pixel": 180, "value": 0}, {"pixel": 30, "value": 15}],
                    },
                ],
                "series": [
                    {
                        "name": "curve",
                        "marker_colors_rgb": [list(OUTSIDE), list(INSIDE)],
                        "sample_values": SAMPLES,
                    }
                ],
                "reference_lines": [8],
                "extraction_parameters": {
                    "color_tolerance": 2,
                    "sample_radius": 7,
                    "marker_radius_min": 3,
                },
                "mark_grammars": ["curve", "marker", "reference_line"],
                "route": {
                    "route_id": "raster_marker_line_candidate",
                    "maturity": "candidate",
                    "implementation": "scripts/candidate_digitize_marker_line.py",
                },
                "required_confirmations": list(confirmations),
                "confirmations": confirmations,
            }
        ],
    }


class MarkerLineSpecRunnerTests(unittest.TestCase):
    def test_binds_verified_spec_and_refuses_identical_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.png"
            fixture().save(source)
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(make_spec(source), indent=2) + "\n", encoding="utf-8")
            output = execute_spec(spec_path, root / "runs")
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "candidate_extracted")
            self.assertTrue(manifest["numeric_output_authorized"])
            panel_dir = output / manifest["panels"][0]["relative_directory"]
            self.assertTrue((panel_dir / "data.csv").is_file())
            self.assertTrue((panel_dir / "overlay.png").is_file())
            with self.assertRaises(FileExistsError):
                execute_spec(spec_path, root / "runs")

    def test_rejects_unbound_route_and_invalid_colour(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source.png"
            fixture().save(source)
            spec = make_spec(source)
            spec["panels"][0]["route"]["route_id"] = "raster_line_color"
            with self.assertRaises(MarkerLineSpecError):
                bind_panel(spec["panels"][0], panel_index=0)
            spec["panels"][0]["route"]["route_id"] = "raster_marker_line_candidate"
            spec["panels"][0]["series"][0]["marker_colors_rgb"] = [[300, 0, 0]]
            with self.assertRaises(MarkerLineSpecError):
                bind_panel(spec["panels"][0], panel_index=0)

    def test_rejects_source_hash_mismatch_before_writing_a_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.png"
            fixture().save(source)
            spec = make_spec(source)
            spec["source"]["sha256"] = "0" * 64
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            with self.assertRaises(MarkerLineSpecError):
                execute_spec(spec_path, root / "runs")
            self.assertFalse((root / "runs").exists())


if __name__ == "__main__":
    unittest.main()
