#!/usr/bin/env python3
"""
Assemble a DRIL dataset from unit-level JSON records into a single CSV.

Assumes the following structure in the input directory:
    unit_records/
        argentina_2020.json
        argentina_2021.json
        ...

Each JSON file should contain:
    {
        "unit": {"country": "ARG", "year": 2020},
        "coded_answers": {"v01": "full", "v02": 1.23, ...},
        "uncertainty_status": {"v01": "answered", "v02": "answered", ...},
        "evidence_items": [...],
        "data_gaps": [...],
        "search_log": [...]
    }

Usage:
    python assemble_dataset.py unit_records/ --output dataset.csv
"""
import argparse
import csv
import json
import sys
from pathlib import Path


def assemble_dataset(records_dir: Path, output_path: Path) -> None:
    records = []
    for json_file in sorted(records_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        records.append(data)

    if not records:
        print(f"No JSON records found in {records_dir}")
        sys.exit(1)

    # Determine columns: unit dimensions + variable columns + uncertainty columns
    unit_keys = list(records[0]["unit"].keys())
    var_ids = sorted(records[0]["coded_answers"].keys())

    header = unit_keys + var_ids + [f"{v}_status" for v in var_ids]

    rows = []
    for rec in records:
        row = []
        for k in unit_keys:
            row.append(rec["unit"].get(k, ""))
        for v in var_ids:
            row.append(rec["coded_answers"].get(v, ""))
        for v in var_ids:
            row.append(rec.get("uncertainty_status", {}).get(v, ""))
        rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Assembled {len(rows)} rows into {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble DRIL unit records into a dataset CSV")
    parser.add_argument("records_dir", help="Directory containing unit JSON records")
    parser.add_argument("--output", "-o", default="dataset.csv", help="Output CSV path")
    args = parser.parse_args()

    records_dir = Path(args.records_dir)
    if not records_dir.is_dir():
        print(f"Error: {records_dir} is not a directory")
        return 1

    assemble_dataset(records_dir, Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
