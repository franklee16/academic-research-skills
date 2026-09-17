import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from digitize_boxplot import extract_boxplots


class ExtractBoxplotTests(unittest.TestCase):
    def _extract(self, image: Image.Image, *, orientation: str = "vertical") -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vertical_boxplot.png"
            image.save(path)
            return extract_boxplots(
                image_path=path,
                plot_bounds=(10, 10, 110, 110),
                x_axis=(10, 0.0, 110, 10.0),
                y_axis=(10, 12.0, 110, 0.0),
                box_color="#6baed6",
                line_color="#111111",
                outlier_color="#d62728",
                orientation=orientation,
                tolerance=2,
                min_area=12,
            )

    def _extract_horizontal(self, image: Image.Image, *, orientation: str) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "horizontal_boxplot.png"
            image.save(path)
            return extract_boxplots(
                image_path=path,
                plot_bounds=(10, 10, 110, 110),
                x_axis=(10, 0.0, 110, 10.0),
                y_axis=(10, 12.0, 110, 0.0),
                box_color="#6baed6",
                line_color="#111111",
                outlier_color="#d62728",
                orientation=orientation,
                tolerance=2,
                min_area=12,
            )

    @staticmethod
    def _draw_horizontal_group(
        draw: ImageDraw.ImageDraw,
        *,
        left: int,
        top: int,
        right: int,
        bottom: int,
        median: int,
        lower_cap: int,
        upper_cap: int,
        cap_width: int = 1,
        outlier: tuple[int, int] | None = None,
    ) -> None:
        line = "#111111"
        category_center = (top + bottom) // 2
        draw.rectangle((left, top, right, bottom), fill="#6baed6")
        draw.line((median, top + 1, median, bottom - 1), fill=line)
        for offset in range(cap_width):
            draw.line((lower_cap + offset, top, lower_cap + offset, bottom), fill=line)
            draw.line((upper_cap + offset, top, upper_cap + offset, bottom), fill=line)
        draw.line((lower_cap + cap_width, category_center, left - 1, category_center), fill=line)
        draw.line((right + 1, category_center, upper_cap - 1, category_center), fill=line)
        if outlier is not None:
            x, y = outlier
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="#d62728")

    def test_extracts_two_vertical_groups_with_medians_and_outliers(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        box = "#6baed6"
        line = "#111111"
        outlier = "#d62728"

        # First group: blue fill maps to q3=7.8 and q1=4.2; median is 6.0.
        draw.rectangle((25, 45, 45, 75), fill=box)
        draw.line((26, 60, 44, 60), fill=line)
        draw.line((35, 35, 35, 44), fill=line)
        draw.line((25, 35, 45, 35), fill=line)
        draw.line((35, 76, 35, 85), fill=line)
        draw.line((25, 85, 45, 85), fill=line)
        draw.ellipse((33, 23, 37, 27), fill=outlier)

        # Second group: blue fill maps to q3=9.6 and q1=4.8; median is 7.2.
        draw.rectangle((65, 30, 85, 70), fill=box)
        draw.line((66, 50, 84, 50), fill=line)
        draw.line((75, 20, 75, 29), fill=line)
        draw.line((65, 20, 85, 20), fill=line)
        draw.line((75, 71, 75, 80), fill=line)
        draw.line((65, 80, 85, 80), fill=line)
        draw.ellipse((73, 88, 77, 92), fill=outlier)

        result = self._extract(image)

        groups = result["groups"]
        self.assertEqual([item["status"] for item in groups], ["extracted", "extracted"])
        self.assertEqual([round(item["median"], 3) for item in groups], [6.0, 7.2])
        self.assertEqual([len(item["outliers"]) for item in groups], [1, 1])
        self.assertLess(groups[0]["category_center_pixel"], groups[1]["category_center_pixel"])

        for group in groups:
            for statistic in ("q1", "median", "q3", "lower_whisker", "upper_whisker"):
                self.assertIn(statistic, group)
                self.assertIsInstance(group[statistic], (int, float))
            self.assertIn("box_bounds_pixel", group)

        self.assertEqual(groups[0]["box_bounds_pixel"], (25, 45, 45, 75))
        self.assertEqual(groups[1]["box_bounds_pixel"], (65, 30, 85, 70))
        self.assertEqual(
            [
                {
                    name: round(group[name], 3)
                    for name in ("q1", "median", "q3", "lower_whisker", "upper_whisker")
                }
                for group in groups
            ],
            [
                {
                    "q1": 4.2,
                    "median": 6.0,
                    "q3": 7.8,
                    "lower_whisker": 3.0,
                    "upper_whisker": 9.0,
                },
                {
                    "q1": 4.8,
                    "median": 7.2,
                    "q3": 9.6,
                    "lower_whisker": 3.6,
                    "upper_whisker": 10.8,
                },
            ],
        )
        self.assertEqual(groups[0]["outliers"][0]["center_pixel"], (35.0, 25.0))
        self.assertAlmostEqual(groups[0]["outliers"][0]["value"], 10.2)
        self.assertEqual(groups[1]["outliers"][0]["center_pixel"], (75.0, 90.0))
        self.assertAlmostEqual(groups[1]["outliers"][0]["value"], 2.4)

    def test_pairs_upper_cap_with_centred_whisker_spine(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((25, 45, 45, 75), fill="#6baed6")
        draw.line((26, 60, 44, 60), fill="#111111")
        draw.line((35, 35, 35, 44), fill="#111111")
        draw.line((25, 35, 45, 35), fill="#111111")
        draw.line((35, 76, 35, 85), fill="#111111")
        draw.line((25, 85, 45, 85), fill="#111111")
        draw.line((10, 20, 32, 20), fill="#111111")

        group = self._extract(image)["groups"][0]

        self.assertEqual(group["status"], "extracted")
        self.assertEqual(group["upper_whisker"], 9.0)

    def test_missing_median_is_low_confidence_without_a_value(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((25, 45, 45, 75), fill="#6baed6")
        draw.line((35, 35, 35, 44), fill="#111111")
        draw.line((25, 35, 45, 35), fill="#111111")
        draw.line((35, 76, 35, 85), fill="#111111")
        draw.line((25, 85, 45, 85), fill="#111111")

        group = self._extract(image)["groups"][0]

        self.assertEqual(group["status"], "low_confidence")
        self.assertIsNone(group["median"])
        self.assertIn("median", group["reason"])

    def test_ambiguous_centred_upper_caps_are_low_confidence(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((25, 45, 45, 75), fill="#6baed6")
        draw.line((26, 60, 44, 60), fill="#111111")
        draw.line((35, 20, 35, 44), fill="#111111")
        draw.line((25, 20, 45, 20), fill="#111111")
        draw.line((25, 35, 45, 35), fill="#111111")
        draw.line((35, 76, 35, 85), fill="#111111")
        draw.line((25, 85, 45, 85), fill="#111111")

        group = self._extract(image)["groups"][0]

        self.assertEqual(group["status"], "low_confidence")
        self.assertIsNone(group["upper_whisker"])
        self.assertRegex(group["reason"], r"upper whisker|ambigu")

    def test_boundary_adjacent_caps_without_spines_are_low_confidence(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((25, 45, 45, 75), fill="#6baed6")
        draw.line((26, 60, 44, 60), fill="#111111")
        draw.line((25, 44, 45, 44), fill="#111111")
        draw.line((25, 76, 45, 76), fill="#111111")

        group = self._extract(image)["groups"][0]

        self.assertEqual(group["status"], "low_confidence")
        self.assertIsNone(group["upper_whisker"])
        self.assertIsNone(group["lower_whisker"])

    def test_extracts_two_horizontal_groups_with_stats_and_outliers(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        self._draw_horizontal_group(
            draw,
            left=35,
            top=25,
            right=70,
            bottom=45,
            median=58,
            lower_cap=20,
            upper_cap=80,
            outlier=(15, 35),
        )
        self._draw_horizontal_group(
            draw,
            left=70,
            top=65,
            right=100,
            bottom=85,
            median=85,
            lower_cap=60,
            upper_cap=105,
            outlier=(108, 75),
        )

        result = self._extract_horizontal(image, orientation="horizontal")

        groups = result["groups"]
        self.assertEqual(result["orientation"], "horizontal")
        self.assertEqual([group["status"] for group in groups], ["extracted", "extracted"])
        self.assertEqual([round(group["median"], 3) for group in groups], [4.8, 7.5])
        self.assertLess(groups[0]["category_center_pixel"], groups[1]["category_center_pixel"])
        self.assertEqual(
            [
                {
                    name: round(group[name], 3)
                    for name in ("q1", "median", "q3", "lower_whisker", "upper_whisker")
                }
                for group in groups
            ],
            [
                {
                    "q1": 2.5,
                    "median": 4.8,
                    "q3": 6.0,
                    "lower_whisker": 1.0,
                    "upper_whisker": 7.0,
                },
                {
                    "q1": 6.0,
                    "median": 7.5,
                    "q3": 9.0,
                    "lower_whisker": 5.0,
                    "upper_whisker": 9.5,
                },
            ],
        )
        self.assertEqual(groups[0]["box_bounds_pixel"], (35, 25, 70, 45))
        self.assertEqual(groups[1]["box_bounds_pixel"], (70, 65, 100, 85))
        self.assertEqual(groups[0]["outliers"][0]["center_pixel"], (15.0, 35.0))
        self.assertAlmostEqual(groups[0]["outliers"][0]["value"], 0.5)
        self.assertEqual(groups[1]["outliers"][0]["center_pixel"], (108.0, 75.0))
        self.assertAlmostEqual(groups[1]["outliers"][0]["value"], 9.8)

    def test_auto_orientation_selects_a_unique_four_group_horizontal_layout(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        for top in (20, 42, 64, 86):
            self._draw_horizontal_group(
                draw,
                left=35,
                top=top,
                right=75,
                bottom=top + 10,
                median=55,
                lower_cap=20,
                upper_cap=90,
            )

        result = self._extract_horizontal(image, orientation="auto")

        self.assertEqual(result["orientation"], "horizontal")
        self.assertEqual([group["status"] for group in result["groups"]], ["extracted"] * 4)

    def test_auto_orientation_refuses_a_single_group_as_ambiguous(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        self._draw_horizontal_group(
            draw,
            left=35,
            top=45,
            right=75,
            bottom=65,
            median=55,
            lower_cap=20,
            upper_cap=90,
        )

        result = self._extract_horizontal(image, orientation="auto")

        self.assertEqual(result["orientation"], "unknown")
        self.assertEqual(result["status"], "low_confidence")
        self.assertIn("ambiguous_orientation", result["reason"])

    def test_auto_orientation_validates_two_vertical_groups_at_different_levels(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        line = "#111111"
        draw.rectangle((25, 70, 45, 90), fill="#6baed6")
        draw.line((26, 80, 44, 80), fill=line)
        draw.line((35, 60, 35, 69), fill=line)
        draw.line((25, 60, 45, 60), fill=line)
        draw.line((35, 91, 35, 100), fill=line)
        draw.line((25, 100, 45, 100), fill=line)

        draw.rectangle((65, 20, 85, 50), fill="#6baed6")
        draw.line((66, 35, 84, 35), fill=line)
        draw.line((75, 10, 75, 19), fill=line)
        draw.line((65, 10, 85, 10), fill=line)
        draw.line((75, 51, 75, 60), fill=line)
        draw.line((65, 60, 85, 60), fill=line)

        result = self._extract(image, orientation="auto")

        self.assertEqual(result["orientation"], "vertical")
        self.assertEqual([group["status"] for group in result["groups"]], ["extracted"] * 2)
        self.assertEqual([round(group["median"], 3) for group in result["groups"]], [3.6, 9.0])

    def test_extracts_horizontal_group_with_two_pixel_thick_caps(self):
        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        self._draw_horizontal_group(
            draw,
            left=35,
            top=45,
            right=70,
            bottom=65,
            median=58,
            lower_cap=20,
            upper_cap=80,
            cap_width=2,
        )

        result = self._extract_horizontal(image, orientation="horizontal")

        self.assertEqual(result["orientation"], "horizontal")
        self.assertEqual([group["status"] for group in result["groups"]], ["extracted"])


if __name__ == "__main__":
    unittest.main()
