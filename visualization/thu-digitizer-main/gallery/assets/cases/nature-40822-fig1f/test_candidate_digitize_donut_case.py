import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


MODULE_PATH = Path(__file__).with_name("candidate_digitize_donut_case.py")
SPEC = importlib.util.spec_from_file_location("candidate_donut", MODULE_PATH)
candidate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(candidate)


class AnnularGeometryCandidateTests(unittest.TestCase):
    def _fixture(self, values, names):
        image = Image.new("RGB", (240, 240), "white")
        draw = ImageDraw.Draw(image)
        total = sum(values)
        angle = -90.0
        for value, name in zip(values, names):
            extent = 360.0 * value / total
            draw.pieslice(
                (40, 40, 200, 200),
                angle,
                angle + extent,
                fill=candidate.PALETTE[name]["rgb"],
                outline="white",
                width=2,
            )
            angle += extent
        draw.ellipse((92, 92, 148, 148), fill="white")
        return np.asarray(image)

    def test_recovers_normalized_sector_geometry_without_expected_count(self):
        names = ["TSK", "Tumor_KC_Basal", "Normal_KC_Diff"]
        truth = [20.0, 30.0, 50.0]
        rgb = self._fixture(truth, names)
        result = candidate.sample_annular_geometry(
            rgb, (120, 120), (55, 72), angle_samples=7200, tolerance=8.0
        )
        recovered = {row["cell_type"]: row["geometry_share_percent"] for row in result["sectors"]}
        self.assertEqual(set(recovered), set(names))
        self.assertGreater(result["accepted_classified_coverage"], 0.95)
        for name, expected in zip(names, truth):
            self.assertLess(abs(recovered[name] - expected), 0.8)

    def test_blank_ring_refuses_geometry_instead_of_inventing_sectors(self):
        rgb = np.full((240, 240, 3), 255, dtype=np.uint8)
        result = candidate.sample_annular_geometry(
            rgb, (120, 120), (55, 72), angle_samples=3600, tolerance=8.0
        )
        self.assertEqual(result["status"], "no_classifiable_sector")
        self.assertEqual(result["sectors"], [])
        self.assertEqual(result["accepted_classified_coverage"], 0.0)

    def test_run_identifier_is_deterministic(self):
        params = {"centres": [[1, 2]], "tolerance": 20}
        one = candidate.stable_run_id("abc", params)
        two = candidate.stable_run_id("abc", params)
        self.assertEqual(one, two)


if __name__ == "__main__":
    unittest.main()
