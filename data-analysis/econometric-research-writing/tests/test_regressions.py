from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SKILL_ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


profiler = load_script("profile_econ_dataset", "profile_econ_dataset.py")
renderer = load_script("render_validate_docx", "render_validate_docx.py")
runner = load_script("run_empirical_analysis", "run_empirical_analysis.py")


class ProfilerRegressionTests(unittest.TestCase):
    def test_single_row_formats_missing_standard_deviation(self):
        frame = pd.DataFrame({"value": [1.0]})
        report = profiler.build_report(Path("single.csv"), frame, {})
        markdown = profiler.markdown_report(report)
        self.assertIn("sd n/a", markdown)

    def test_xlsx_without_sheet_uses_first_worksheet(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.xlsx"
            with pd.ExcelWriter(path) as writer:
                pd.DataFrame({"first": [1]}).to_excel(
                    writer, sheet_name="first_sheet", index=False
                )
                pd.DataFrame({"second": [2]}).to_excel(
                    writer, sheet_name="second_sheet", index=False
                )
            loaded = profiler.read_data(path)
            self.assertIsInstance(loaded, pd.DataFrame)
            self.assertEqual(list(loaded.columns), ["first"])

    def test_semantic_roles_are_not_assigned_from_column_names(self):
        frame = pd.DataFrame({"firm_id": [1, 2], "year": [2020, 2021], "revenue": [3.0, 4.0]})
        report = profiler.build_report(Path("sample.csv"), frame, {})
        self.assertEqual(report["analysis_roles"], {})
        self.assertTrue(report["agent_role_decision_required"])

    def test_collinearity_uses_declared_regressors_and_excludes_keys(self):
        frame = pd.DataFrame(
            {
                "firm_id": np.arange(40),
                "year": np.arange(2000, 2040),
                "treatment": np.linspace(0, 1, 40),
                "control": np.linspace(0, 2, 40),
            }
        )
        roles = {
            "treatment": "treatment",
            "controls": ["control"],
            "unit": "firm_id",
            "time": "year",
            "fixed_effects": ["year"],
        }
        diagnostics = profiler.collinearity_diagnostics(frame, roles)
        self.assertEqual(diagnostics["variables"], ["treatment", "control"])
        self.assertNotIn("firm_id", diagnostics["encoded_columns"])
        self.assertNotIn("year", diagnostics["encoded_columns"])
        self.assertLess(diagnostics["design_matrix_rank"], diagnostics["design_matrix_columns"])
        self.assertTrue(diagnostics["vif"])


class EmpiricalAnalysisTests(unittest.TestCase):
    def test_full_analysis_writes_tables_clustered_results_and_event_figure(self):
        rng = np.random.default_rng(7)
        rows = []
        for firm in range(12):
            treatment_year = 3 + firm % 3
            firm_effect = firm / 10
            for year in range(8):
                event_time = year - treatment_year
                treatment = int(event_time >= 0)
                control = rng.normal()
                outcome = firm_effect + 0.15 * year + 1.2 * treatment + 0.25 * control + rng.normal(scale=0.1)
                rows.append(
                    {
                        "firm_id": firm,
                        "year": year,
                        "event_time": event_time,
                        "treatment": treatment,
                        "control": control,
                        "outcome": outcome,
                    }
                )
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            data_path = tmpdir / "panel.csv"
            roles_path = tmpdir / "roles.json"
            output_dir = tmpdir / "results"
            pd.DataFrame(rows).to_csv(data_path, index=False)
            roles_path.write_text(
                json.dumps(
                    {
                        "outcome": "outcome",
                        "treatment": "treatment",
                        "controls": ["control"],
                        "unit": "firm_id",
                        "time": "year",
                        "fixed_effects": ["firm_id", "year"],
                        "cluster": "firm_id",
                        "event_time": "event_time",
                        "event_reference": -1,
                        "event_window": [-3, 3],
                    }
                ),
                encoding="utf-8",
            )
            runner.run_analysis(data_path, roles_path, output_dir)
            expected = {
                "descriptive_statistics.csv",
                "baseline_results.csv",
                "robustness_results.csv",
                "design_diagnostics.json",
                "event_study_results.csv",
                "event_study.png",
                "event_study.pdf",
                "analysis_manifest.json",
            }
            self.assertTrue(expected.issubset({path.name for path in output_dir.iterdir()}))
            baseline = pd.read_csv(output_dir / "baseline_results.csv")
            self.assertEqual(set(baseline["covariance"]), {"cluster"})
            self.assertEqual(set(baseline["cluster"]), {"firm_id"})
            robustness = pd.read_csv(output_dir / "robustness_results.csv")
            self.assertIn("Preferred", set(robustness["model"]))
            self.assertIn("Preferred HC3", set(robustness["model"]))


class RendererRegressionTests(unittest.TestCase):
    def test_missing_renderer_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            argv = [
                "render_validate_docx.py",
                str(Path(tmp) / "paper.docx"),
                "--output-dir",
                str(Path(tmp) / "rendered"),
            ]
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                renderer, "find_renderer", return_value=None
            ):
                with self.assertRaises(SystemExit) as caught:
                    renderer.main()
            self.assertNotEqual(caught.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
