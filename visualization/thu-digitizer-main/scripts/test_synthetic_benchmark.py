"""Regression check for the synthetic benchmark report visualisation."""
from __future__ import annotations

import tempfile
from pathlib import Path

from run_synthetic_benchmark import summary_plot


def main() -> None:
    # Thirty series-level rows collapse into ten case/method bars.
    rows = [
        {
            "case": f"case-{group // 2}",
            "family": f"family-{group // 2}",
            "method": f"method-{group % 2}",
            "normalized_score": 0.01 * (index + 1),
        }
        for group in range(10)
        for index in range(3)
    ]
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "summary.png"
        summary_plot(rows, output)
        assert output.exists() and output.stat().st_size > 1_000
    print("SUMMARY_AGGREGATION_TEST_OK")


if __name__ == "__main__":
    main()
