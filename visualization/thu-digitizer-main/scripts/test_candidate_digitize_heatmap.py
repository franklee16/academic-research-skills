import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from candidate_digitize_heatmap import extract_heatmap


class CalibratedHeatmapCandidateTests(unittest.TestCase):
    @staticmethod
    def _fixture(path: Path, *, ambiguous_cell: bool = False) -> None:
        image = Image.new("RGB", (230, 140), "white")
        draw = ImageDraw.Draw(image)
        palette = []
        for index in range(91):
            fraction = index / 90
            if fraction <= 0.5:
                local = fraction * 2
                start = np.asarray([180, 10, 40])
                end = np.asarray([220, 220, 220])
            else:
                local = (fraction - 0.5) * 2
                start = np.asarray([220, 220, 220])
                end = np.asarray([60, 80, 195])
            palette.append(tuple(np.rint(start + local * (end - start)).astype(int)))
        for offset, colour in enumerate(palette):
            draw.line((170, 20 + offset, 190, 20 + offset), fill=colour)

        x_boundaries = [20, 50, 80, 110, 140]
        y_boundaries = [20, 50, 80, 110]
        indices = [[0, 15, 30, 45], [60, 75, 90, 25], [55, 35, 10, 80]]
        significant = {(0, 1), (1, 3), (2, 0)}
        for row in range(3):
            for column in range(4):
                colour = palette[indices[row][column]]
                if ambiguous_cell and (row, column) == (1, 2):
                    colour = (0, 255, 0)
                draw.rectangle(
                    (
                        x_boundaries[column] + 1,
                        y_boundaries[row] + 1,
                        x_boundaries[column + 1] - 1,
                        y_boundaries[row + 1] - 1,
                    ),
                    fill=colour,
                )
                if (row, column) in significant:
                    x = (x_boundaries[column] + x_boundaries[column + 1]) // 2
                    y = (y_boundaries[row] + y_boundaries[row + 1]) // 2
                    draw.line((x - 5, y, x + 5, y), fill="white", width=2)
                    draw.line((x, y - 5, x, y + 5), fill="white", width=2)
                    draw.line((x - 4, y - 4, x + 4, y + 4), fill="white", width=1)
                    draw.line((x - 4, y + 4, x + 4, y - 4), fill="white", width=1)
        for x in x_boundaries:
            draw.line((x, 20, x, 110), fill="#464646")
        for y in y_boundaries:
            draw.line((20, y, 140, y), fill="#464646")
        image.save(path)

    @staticmethod
    def _extract(path: Path) -> dict:
        return extract_heatmap(
            path,
            grid_bounds=(20, 20, 140, 110),
            row_labels=["R1", "R2", "R3"],
            column_labels=["A", "B", "C", "D"],
            colorbar_bounds=(170, 20, 190, 110),
            colorbar_top_value=1.0,
            colorbar_bottom_value=-1.0,
            maximum_palette_distance=10,
        )

    def test_recovers_grid_values_endpoint_censoring_and_visible_marks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "heatmap.png"
            self._fixture(path)
            result = self._extract(path)

            self.assertEqual(result["status"], "candidate")
            self.assertEqual(result["cell_count"], 12)
            self.assertEqual(result["cells"][0]["value_status"], "clipped_high")
            self.assertEqual(result["cells"][6]["value_status"], "clipped_low")
            self.assertEqual(sum(cell["significant_visible"] for cell in result["cells"]), 3)
            self.assertAlmostEqual(result["cells"][1]["value"], 2 / 3, places=2)
            self.assertTrue(all(cell["palette_distance_rgb"] == 0 for cell in result["cells"]))

    def test_rejects_a_cell_colour_not_supported_by_the_colour_bar(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ambiguous.png"
            self._fixture(path, ambiguous_cell=True)
            result = self._extract(path)

            self.assertEqual(result["status"], "low_confidence")
            rejected = [cell for cell in result["cells"] if cell["status"] == "low_confidence"]
            self.assertEqual(len(rejected), 1)
            self.assertIn("too far", rejected[0]["reason"])


if __name__ == "__main__":
    unittest.main()
