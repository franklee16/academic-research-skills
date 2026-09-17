import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from candidate_digitize_outline_boxplot import extract_outline_boxplots


class OutlineBoxplotCandidateTests(unittest.TestCase):
    @staticmethod
    def _draw_group(
        draw,
        *,
        center,
        q3,
        median,
        q1,
        upper,
        lower,
        fill,
        outlier=None,
        draw_median=True,
    ):
        line = "#464646"
        half = 11
        draw.rectangle((center - half, q3, center + half, q1), fill=fill, outline=line, width=2)
        if draw_median:
            draw.line((center - half, median, center + half, median), fill=line, width=2)
        draw.line((center, upper, center, q3), fill=line, width=2)
        draw.line((center - 6, upper, center + 6, upper), fill=line, width=2)
        draw.line((center, q1, center, lower), fill=line, width=2)
        draw.line((center - 6, lower, center + 6, lower), fill=line, width=2)
        if outlier is not None:
            draw.ellipse((center - 4, outlier - 4, center + 4, outlier + 4), outline=line, width=2)

    def test_recovers_paired_unfilled_and_split_fill_series_with_same_colour_outliers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paired.png"
            image = Image.new("RGB", (220, 190), "white")
            draw = ImageDraw.Draw(image)
            self._draw_group(
                draw,
                center=48,
                q3=62,
                median=78,
                q1=102,
                upper=43,
                lower=124,
                fill="white",
                outlier=143,
            )
            self._draw_group(
                draw,
                center=72,
                q3=55,
                median=70,
                q1=91,
                upper=38,
                lower=112,
                fill="#4685bd",
            )
            self._draw_group(
                draw,
                center=142,
                q3=72,
                median=88,
                q1=116,
                upper=50,
                lower=136,
                fill="white",
            )
            self._draw_group(
                draw,
                center=166,
                q3=64,
                median=83,
                q1=106,
                upper=46,
                lower=128,
                fill="#4685bd",
                outlier=149,
            )
            image.save(path)

            result = extract_outline_boxplots(
                path,
                plot_bounds=(20, 20, 200, 170),
                y_axis=(20, 1.0, 170, 0.0),
                line_color="#464646",
                filled_series={"Finetune": "#4685bd"},
                unfilled_series_label="Retrain",
                tolerance=4,
            )

            self.assertEqual(result["status"], "candidate")
            self.assertEqual(len(result["groups"]), 4)
            self.assertEqual(
                [group["series"] for group in result["groups"]],
                ["Retrain", "Finetune", "Retrain", "Finetune"],
            )
            self.assertTrue(all(group["status"] == "candidate" for group in result["groups"]))
            self.assertEqual(len(result["groups"][0]["outliers"]), 1)
            self.assertEqual(len(result["groups"][3]["outliers"]), 1)
            self.assertAlmostEqual(result["groups"][1]["median"], 2 / 3, places=2)

    def test_refuses_a_tall_box_with_no_internal_median(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing-median.png"
            image = Image.new("RGB", (150, 180), "white")
            draw = ImageDraw.Draw(image)
            self._draw_group(
                draw,
                center=48,
                q3=55,
                median=75,
                q1=105,
                upper=38,
                lower=125,
                fill="white",
                draw_median=False,
            )
            self._draw_group(
                draw,
                center=86,
                q3=62,
                median=80,
                q1=112,
                upper=44,
                lower=132,
                fill="#4685bd",
            )
            image.save(path)

            result = extract_outline_boxplots(
                path,
                plot_bounds=(20, 20, 125, 160),
                y_axis=(20, 1.0, 160, 0.0),
                line_color="#464646",
                filled_series={"Finetune": "#4685bd"},
                unfilled_series_label="Retrain",
                tolerance=4,
            )

            self.assertEqual(result["status"], "low_confidence")
            missing = next(group for group in result["groups"] if group["category_center_pixel"] == 48.0)
            self.assertEqual(missing["status"], "low_confidence")
            self.assertIn("no internal median", missing["reason"])


if __name__ == "__main__":
    unittest.main()
