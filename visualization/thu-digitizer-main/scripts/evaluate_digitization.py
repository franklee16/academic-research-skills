"""Compare digitized CSV output with a trusted CSV and enforce an MAE gate."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def normalized_key(value: str) -> str:
    """Keep text keys intact while treating 0 and 0.0 as the same numeric key."""
    try:
        return f"number:{float(value):.12g}"
    except ValueError:
        return f"text:{value}"


def sort_key(value: str) -> tuple[int, float | str]:
    if value.startswith("number:"):
        return 0, float(value.removeprefix("number:"))
    return 1, value.removeprefix("text:")


def read_rows(path: Path, key: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or key not in reader.fieldnames:
            raise ValueError(f"{path} must contain key column {key!r}")
        rows = list(reader)
    lookup = {normalized_key(row[key]): row for row in rows}
    if len(lookup) != len(rows):
        raise ValueError(f"{path} has duplicate key values in {key!r}")
    return list(reader.fieldnames), lookup


def number(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth", required=True, type=Path)
    parser.add_argument("--prediction", required=True, type=Path)
    parser.add_argument("--key", default="x")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--max-mae", type=float)
    args = parser.parse_args()
    truth_fields, truth = read_rows(args.truth, args.key)
    prediction_fields, prediction = read_rows(args.prediction, args.key)
    fields = [field for field in truth_fields if field in prediction_fields and field not in {args.key, "x_pixel"}]
    if not fields:
        raise SystemExit("no shared value columns to evaluate")
    shared_keys = sorted(set(truth).intersection(prediction), key=sort_key)
    if not shared_keys:
        raise SystemExit("truth and prediction have no shared keys")

    metrics: dict[str, Any] = {}
    failures: list[str] = []
    for field in fields:
        errors: list[float] = []
        missing = 0
        for key in shared_keys:
            expected = number(truth[key].get(field))
            observed = number(prediction[key].get(field))
            if expected is None or observed is None:
                missing += 1
                continue
            errors.append(abs(observed - expected))
        if not errors:
            metrics[field] = {"count": 0, "missing_or_non_numeric": missing, "mae": None, "rmse": None, "max_abs_error": None}
            failures.append(f"{field}: no comparable numeric values")
            continue
        mae = sum(errors) / len(errors)
        metrics[field] = {
            "count": len(errors),
            "missing_or_non_numeric": missing,
            "mae": mae,
            "rmse": math.sqrt(sum(error * error for error in errors) / len(errors)),
            "max_abs_error": max(errors),
        }
        if args.max_mae is not None and mae > args.max_mae:
            failures.append(f"{field}: MAE {mae:.6g} exceeds {args.max_mae:.6g}")

    report = {
        "schema_version": 1,
        "truth_file": args.truth.name,
        "prediction_file": args.prediction.name,
        "key": args.key,
        "shared_rows": len(shared_keys),
        "metrics": metrics,
        "passed_max_mae": not failures,
        "failures": failures,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REPORT={args.report}")
    for field, metric in metrics.items():
        print(f"{field}: MAE={metric['mae']} count={metric['count']}")
    if failures:
        raise SystemExit("; ".join(failures))


if __name__ == "__main__":
    main()
