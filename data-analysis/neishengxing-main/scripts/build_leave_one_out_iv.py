#!/usr/bin/env python3
"""
Build leave-one-out peer instruments from a CSV file.

Example:
  python build_leave_one_out_iv.py data.csv --group village_id --vars pd digital_index --out loo_iv.csv

The script creates variables named loo_<var> for each requested variable:
  loo_x_i = (sum_group_x - x_i) / (n_group_nonmissing_x - 1)
"""

import argparse
from pathlib import Path
import pandas as pd


def build_loo(df: pd.DataFrame, group: str, variables: list[str]) -> pd.DataFrame:
    out = df.copy()
    for var in variables:
        if var not in out.columns:
            raise ValueError(f"Variable not found: {var}")
        counts = out.groupby(group)[var].transform(lambda s: s.notna().sum())
        sums = out.groupby(group)[var].transform("sum")
        denom = counts - out[var].notna().astype(int)
        numer = sums - out[var].fillna(0)
        loo = numer / denom
        loo = loo.where(denom > 0)
        out[f"loo_{var}"] = loo
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("--group", required=True, help="Group identifier, e.g. village_id")
    parser.add_argument("--vars", nargs="+", required=True, help="Variables to transform")
    parser.add_argument("--out", required=True, help="Output CSV path")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    if args.group not in df.columns:
        raise ValueError(f"Group variable not found: {args.group}")
    out = build_loo(df, args.group, args.vars)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)


if __name__ == "__main__":
    main()
