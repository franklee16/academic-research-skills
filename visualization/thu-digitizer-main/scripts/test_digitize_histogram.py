import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from digitize_histogram import extract_histogram


class ExtractHistogramTests(unittest.TestCase):
    def test_extracts_sorted_bin_edges_and_heights(self):
        image = np.full((80, 120, 3), 255, dtype=np.uint8)
        color = (0x1F, 0x77, 0xB4)
        image[50:70, 10:30] = color
        image[30:70, 35:55] = color
        image[45:70, 60:80] = color

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "histogram.png"
            Image.fromarray(image, mode="RGB").save(path)
            bins = extract_histogram(
                image_path=path,
                plot_bounds=(10, 10, 100, 70),
                x_axis=(10, 0.0, 100, 9.0),
                y_axis=(10, 12.0, 70, 0.0),
                bar_color="#1f77b4",
                tolerance=1,
                min_area=20,
            )

        self.assertEqual(len(bins), 3)
        self.assertEqual([bin_["height"] for bin_ in bins], [4.0, 8.0, 5.0])
        self.assertEqual([bin_["x_left"] for bin_ in bins], [0.0, 2.5, 5.0])
        self.assertEqual([bin_["x_right"] for bin_ in bins], [2.0, 4.5, 7.0])

    def test_uses_defaults_with_image_path_keyword(self):
        image = np.full((80, 120, 3), 255, dtype=np.uint8)
        image[50:54, 10:14] = (0x1F, 0x77, 0xB4)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "histogram.png"
            Image.fromarray(image, mode="RGB").save(path)
            bins = extract_histogram(
                image_path=path,
                plot_bounds=(10, 10, 100, 70),
                x_axis=(10, 0.0, 100, 9.0),
                y_axis=(10, 12.0, 70, 0.0),
                bar_color="#1f77b4",
            )

        self.assertEqual(len(bins), 1)

    def test_ignores_same_coloured_legend_swatch_outside_plot(self):
        image = np.full((80, 120, 3), 255, dtype=np.uint8)
        color = (0x1F, 0x77, 0xB4)
        image[30:70, 10:30] = color
        image[5:9, 105:118] = color

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "histogram.png"
            Image.fromarray(image, mode="RGB").save(path)
            bins = extract_histogram(
                image_path=path,
                plot_bounds=(10, 10, 100, 70),
                x_axis=(10, 0, 100, 9),
                y_axis=(10, 10, 70, 0),
                bar_color="#1f77b4",
                tolerance=1,
                min_area=12,
            )

        self.assertEqual(len(bins), 1)

    def test_returns_no_bins_when_colour_evidence_is_absent(self):
        image = np.full((80, 120, 3), 255, dtype=np.uint8)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "histogram.png"
            Image.fromarray(image, mode="RGB").save(path)
            bins = extract_histogram(
                image_path=path,
                plot_bounds=(10, 10, 100, 70),
                x_axis=(10, 0, 100, 9),
                y_axis=(10, 10, 70, 0),
                bar_color="#1f77b4",
                tolerance=1,
                min_area=12,
            )

        self.assertEqual(bins, [])


if __name__ == "__main__":
    unittest.main()
