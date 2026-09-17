from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ScriptSmokeTests(unittest.TestCase):
    def test_latex_guard_passes_valid_fixture(self) -> None:
        result = run_script(
            "scripts/latex_guard.py",
            str(FIXTURES / "mini_paper.tex"),
            "--bib",
            str(FIXTURES / "references.bib"),
            "--markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Errors: 0", result.stdout)

    def test_style_metrics_reports_sections(self) -> None:
        result = run_script("scripts/style_metrics.py", str(FIXTURES / "mini_paper.tex"), "--markdown")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("# Style Metrics", result.stdout)
        self.assertIn("Introduction", result.stdout)

    def test_revision_audit_reports_similarity(self) -> None:
        result = run_script(
            "scripts/revision_audit.py",
            str(FIXTURES / "mini_paper.tex"),
            str(FIXTURES / "mini_paper_revised.tex"),
            "--markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("# Revision Audit", result.stdout)
        self.assertIn("Near-identical revised paragraphs", result.stdout)


if __name__ == "__main__":
    unittest.main()
