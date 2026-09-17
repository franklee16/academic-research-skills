import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from candidate_digitize_split_fill_boxplot import extract_split_fill_boxplots
from digitize_boxplot import extract_boxplots


class SplitFillBoxplotCandidateTests(unittest.TestCase):
    def test_candidate_merges_fill_split_by_median_without_changing_stable_route(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "split-fill.png"
            image = Image.new("RGB", (220, 180), "white")
            draw = ImageDraw.Draw(image)
            for center, top, median, bottom, upper, lower in [
                (70, 60, 80, 100, 40, 125),
                (150, 48, 72, 94, 30, 118),
            ]:
                draw.rectangle((center - 20, top, center + 20, bottom), fill="#4685bd", outline="#464646", width=2)
                draw.line((center - 19, median, center + 19, median), fill="#464646", width=2)
                draw.line((center, upper, center, top), fill="#464646", width=2)
                draw.line((center - 10, upper, center + 10, upper), fill="#464646", width=2)
                draw.line((center, bottom, center, lower), fill="#464646", width=2)
                draw.line((center - 10, lower, center + 10, lower), fill="#464646", width=2)
            image.save(path)

            common = {
                "plot_bounds": (20, 20, 200, 160),
                "x_axis": (20.0, 0.0, 200.0, 2.0),
                "y_axis": (20.0, 10.0, 160.0, 0.0),
                "box_color": "#4685bd",
                "line_color": "#464646",
            }
            stable = extract_boxplots(
                path,
                **common,
                outlier_color="#ff00ff",
                orientation="vertical",
                tolerance=8.0,
                min_area=8,
            )
            candidate = extract_split_fill_boxplots(
                path,
                **common,
                tolerance=8.0,
                min_fragment_area=8,
                maximum_median_gap=4,
            )

            self.assertEqual(stable["status"], "low_confidence")
            self.assertEqual(candidate["status"], "candidate")
            self.assertEqual(candidate["fragment_count"], 4)
            self.assertEqual(candidate["merged_box_count"], 2)
            self.assertEqual(len(candidate["groups"]), 2)
            self.assertTrue(all(group["status"] == "extracted" for group in candidate["groups"]))
            self.assertEqual(candidate["outlier_status"], "not_extracted")


if __name__ == "__main__":
    unittest.main()
