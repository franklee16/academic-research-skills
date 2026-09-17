import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from recreate_line_figure import RecreationSpecError, render_spec


def make_spec():
    return {
        "schema_version": 1,
        "canvas": {"width": 360, "height": 240, "background": "white"},
        "data_csv": "data.csv",
        "panels": [
            {
                "panel_id": "panel-a",
                "bounds_px": [45, 25, 335, 205],
                "xlim": [0, 4],
                "ylim": [0, 5],
                "x_ticks": [0, 1, 2, 3, 4],
                "y_ticks": [0, 1, 2, 3, 4, 5],
                "xlabel": "Distance",
                "ylabel": "Value",
                "spans": [{"x_min": 2, "x_max": 3, "color": "#d8eef8"}],
                "reference_lines": [{"y": 2.5, "color": "#3366ff", "dashes": [3, 3]}],
                "series": [
                    {
                        "x_column": "x",
                        "y_column": "value",
                        "label": "curve",
                        "color": "#2ba3ca",
                        "marker": "o",
                    }
                ],
                "decorations": [
                    {"type": "scatter", "points": [[1, 4], [2, 4]], "colors": ["#00aa88", "#66bbcc"], "size": 20},
                    {"type": "vline", "x": 1.5, "y_min": 3.5, "y_max": 4.5, "line_style": "--"},
                ],
                "legend": {"show": True, "loc": "upper left", "font_size": 7},
            }
        ],
        "figure_text": [{"x_px": 8, "y_px": 8, "text": "A", "font_size": 16, "font_weight": "bold"}],
    }


class RecreationRendererTests(unittest.TestCase):
    def test_exact_canvas_vector_outputs_and_immutable_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "data.csv").write_text("x,value\n0,1\n1,2\n2,3\n3,2\n4,1\n", encoding="utf-8")
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(make_spec()), encoding="utf-8")
            output = render_spec(spec_path, root / "runs")
            with Image.open(output / "recreated.png") as image:
                self.assertEqual(image.size, (360, 240))
            with Image.open(output / "recreated-3x.png") as image:
                self.assertEqual(image.size, (1080, 720))
            svg = (output / "recreated.svg").read_text(encoding="utf-8")
            self.assertIn('width="360px" height="240px"', svg)
            self.assertTrue((output / "recreated.pdf").is_file())
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["source_raster_embedded"])
            with self.assertRaises(FileExistsError):
                render_spec(spec_path, root / "runs")

    def test_missing_csv_column_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "data.csv").write_text("x,value\n0,1\n", encoding="utf-8")
            spec = make_spec()
            spec["panels"][0]["series"][0]["y_column"] = "missing"
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            with self.assertRaises(RecreationSpecError):
                render_spec(spec_path, root / "runs")


if __name__ == "__main__":
    unittest.main()
