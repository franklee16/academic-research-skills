import json
import tempfile
import unittest
from pathlib import Path

from run_marker_line_benchmark import run_benchmark


class MarkerLineBenchmarkTests(unittest.TestCase):
    def test_candidate_passes_supported_and_refusal_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = run_benchmark(root)
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "passed")
            self.assertEqual(report["webplotdigitizer"]["status"], "not_compared")
            by_id = {item["case_id"]: item for item in report["cases"]}
            self.assertTrue(all(item["gate_passed"] for item in report["cases"]))
            self.assertGreater(by_id["same_colour_reference"]["stable_baseline"]["unsafe_reference_selections"], 0)
            self.assertLess(
                by_id["same_colour_reference"]["candidate"]["mae"],
                by_id["same_colour_reference"]["stable_baseline"]["mae"],
            )
            self.assertFalse(by_id["line_only_refusal"]["candidate"]["numeric_output_authorized"])
            with self.assertRaises(FileExistsError):
                run_benchmark(root)


if __name__ == "__main__":
    unittest.main()
