import argparse
import json
import warnings as python_warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

LIST_ROLES = {"main_regressors", "controls", "mechanisms", "moderators", "instruments", "fixed_effects", "descriptive_variables"}


def read_data(path, sheet=None):
    suffix = path.suffix.lower()
    if suffix in {".csv", ".txt"}:
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        # ``sheet_name=None`` returns a dictionary of DataFrames. The profiler
        # operates on one table, so default to the first worksheet.
        return pd.read_excel(path, sheet_name=0 if sheet is None else sheet)
    if suffix == ".dta":
        return pd.read_stata(path)
    raise SystemExit(f"unsupported file type: {suffix}")


def safe_float(value):
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value)
    return value


def column_profile(df):
    rows = []
    n = len(df)
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        unique = int(s.nunique(dropna=True))
        row = {
            "name": str(col),
            "dtype": str(s.dtype),
            "missing": missing,
            "missing_pct": round(missing / n, 4) if n else None,
            "unique": unique,
            "constant": unique <= 1,
        }
        if pd.api.types.is_numeric_dtype(s):
            desc = s.replace([np.inf, -np.inf], np.nan).dropna().describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
            for key in ["mean", "std", "min", "1%", "25%", "50%", "75%", "99%", "max"]:
                if key in desc:
                    row[key] = safe_float(desc[key])
            row["zero_count"] = int((s == 0).sum())
            row["negative_count"] = int((s < 0).sum())
        elif pd.api.types.is_datetime64_any_dtype(s):
            row["min"] = str(s.min()) if missing < n else None
            row["max"] = str(s.max()) if missing < n else None
        else:
            top = s.dropna().astype(str).value_counts().head(5)
            row["top_values"] = top.to_dict()
        rows.append(row)
    return rows


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def declared_regressors(roles):
    values = [*as_list(roles.get("treatment")), *as_list(roles.get("main_regressors"))]
    values.extend(as_list(roles.get("controls")))
    return list(dict.fromkeys(str(value) for value in values if value))


def top_correlations(df, columns, max_pairs=20):
    selected = [column for column in columns if column in df.columns]
    num = df[selected].select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan)
    if num.shape[1] < 2:
        return []
    corr = num.corr(numeric_only=True)
    pairs = []
    cols = list(corr.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            val = corr.loc[a, b]
            if pd.notna(val):
                pairs.append({"var1": str(a), "var2": str(b), "corr": float(val), "abs_corr": abs(float(val))})
    pairs.sort(key=lambda x: x["abs_corr"], reverse=True)
    return [{k: v for k, v in p.items() if k != "abs_corr"} for p in pairs[:max_pairs]]


def collinearity_diagnostics(df, roles):
    """Diagnose only agent-declared regressors, never IDs, time keys, or fixed effects."""
    excluded = {
        *as_list(roles.get("unit")),
        *as_list(roles.get("time")),
        *as_list(roles.get("cluster")),
        *as_list(roles.get("fixed_effects")),
    }
    requested = [column for column in declared_regressors(roles) if column not in excluded]
    missing = [column for column in requested if column not in df.columns]
    selected = [column for column in requested if column in df.columns]
    if not selected:
        return {
            "variables": [],
            "excluded_structural_variables": sorted(excluded),
            "status": "not_run",
            "reason": "Agent-declared treatment/main_regressors and controls are required.",
        }

    raw = df[selected].replace([np.inf, -np.inf], np.nan)
    design = pd.get_dummies(raw, columns=list(raw.select_dtypes(exclude=[np.number]).columns), drop_first=True, dtype=float)
    design = design.apply(pd.to_numeric, errors="coerce").dropna()
    varying = [column for column in design if design[column].nunique(dropna=True) > 1]
    design = design[varying]
    if design.empty:
        return {
            "variables": selected,
            "missing_variables": missing,
            "excluded_structural_variables": sorted(excluded),
            "status": "not_run",
            "reason": "No complete, varying regressor columns remain after encoding.",
        }

    standardized = (design - design.mean()) / design.std(ddof=0)
    standardized = standardized.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
    matrix = standardized.to_numpy(dtype=float)
    rank = int(np.linalg.matrix_rank(matrix))
    condition_number = float(np.linalg.cond(matrix)) if matrix.size else None
    if len(design) > 3:
        # Require the lower edge of an approximate Fisher-z confidence interval
        # to clear a practically strong |rho| floor of 0.70.
        threshold = float(
            min(0.95, np.tanh(np.arctanh(0.70) + 1.96 / np.sqrt(len(design) - 3)))
        )
    else:
        threshold = 0.95
    correlations = top_correlations(design, list(design.columns))
    flagged = [pair for pair in correlations if abs(pair["corr"]) >= threshold]

    vif_rows = []
    if design.shape[1] >= 2:
        values = np.column_stack([np.ones(len(design)), design.to_numpy(dtype=float)])
        for index, column in enumerate(design.columns):
            with python_warnings.catch_warnings():
                python_warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    vif = float(variance_inflation_factor(values, index + 1))
                except (ValueError, np.linalg.LinAlgError):
                    vif = float("inf")
            vif_rows.append({"variable": str(column), "vif": None if not np.isfinite(vif) else vif})

    warnings_out = []
    if flagged:
        warnings_out.append(
            f"{len(flagged)} regressor pair(s) exceed the sample-adaptive absolute-correlation threshold {threshold:.3f}."
        )
    high_vif = [row["variable"] for row in vif_rows if row["vif"] is None or row["vif"] >= 10]
    if high_vif:
        warnings_out.append(f"VIF is at least 10 or infinite for: {', '.join(high_vif)}.")
    if rank < design.shape[1]:
        warnings_out.append("The encoded regressor design matrix is rank deficient.")
    if condition_number is not None and condition_number >= 30:
        warnings_out.append(f"The standardized design-matrix condition number is high ({condition_number:.2f}).")

    return {
        "status": "ok",
        "variables": selected,
        "encoded_columns": [str(column) for column in design.columns],
        "missing_variables": missing,
        "excluded_structural_variables": sorted(excluded),
        "complete_observations": int(len(design)),
        "adaptive_correlation_threshold": threshold,
        "correlation_threshold_method": "95% Fisher-z lower bound above practical |rho| floor 0.70",
        "top_correlations": correlations,
        "flagged_correlations": flagged,
        "vif": vif_rows,
        "design_matrix_rank": rank,
        "design_matrix_columns": int(design.shape[1]),
        "condition_number_standardized": condition_number,
        "warnings": warnings_out,
    }


def panel_checks(df, roles):
    unit = roles.get("unit")
    time = roles.get("time")
    if not unit or not time or unit not in df.columns or time not in df.columns:
        return None
    key = df[[unit, time]]
    duplicate_count = int(key.duplicated().sum())
    counts = df.groupby(unit, dropna=False)[time].nunique(dropna=True)
    return {
        "unit": unit,
        "time": time,
        "n_units": int(df[unit].nunique(dropna=True)),
        "n_periods": int(df[time].nunique(dropna=True)),
        "duplicate_unit_time_rows": duplicate_count,
        "min_periods_per_unit": int(counts.min()) if len(counts) else 0,
        "median_periods_per_unit": safe_float(counts.median()) if len(counts) else None,
        "max_periods_per_unit": int(counts.max()) if len(counts) else 0,
        "balanced_candidate": bool(len(counts) and counts.min() == counts.max()),
    }


def load_roles(path):
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("roles JSON must be an object generated or reviewed by the agent.")
    roles = {k: v for k, v in data.items() if v is not None and v != []}
    for key in LIST_ROLES:
        if key in roles:
            roles[key] = as_list(roles[key])
    return roles


def warnings(df, profiles, roles, diagnostics):
    out = []
    for p in profiles:
        col_name = p["name"]
        if p["missing_pct"] and p["missing_pct"] > 0.2:
            out.append(f"{col_name}: missingness exceeds 20%; assess sample selection or imputation.")
        if p["constant"]:
            out.append(f"{col_name}: constant or nearly constant; not useful as a regressor in this sample.")
        if p.get("negative_count", 0) > 0 and any(token in col_name.lower() for token in ["price", "revenue", "sales", "asset", "population", "gdp"]):
            out.append(f"{col_name}: negative values in a variable that may be nonnegative by definition.")
        
        # Suggest log transformation for highly skewed positive continuous variables
        if col_name in df.columns and pd.api.types.is_numeric_dtype(df[col_name]):
            s = df[col_name].dropna()
            if len(s) > 30 and s.nunique() > 10 and (s > 0).all():
                try:
                    skew = s.skew()
                    if pd.notna(skew) and skew > 2.0:
                        out.append(f"{col_name}: highly skewed (skewness = {skew:.2f}) and positive; consider log transformation `log({col_name})` for elasticity interpretation or variance reduction.")
                except Exception:
                    pass

    out.extend(diagnostics.get("warnings", []))

    unit = roles.get("unit")
    time = roles.get("time")
    if unit and time and unit in df.columns and time in df.columns and df[[unit, time]].duplicated().any():
        out.append("Duplicate unit-time keys detected; aggregate or deduplicate before panel regression.")
    return out


def build_report(path, df, roles):
    profiles = column_profile(df)
    diagnostics = collinearity_diagnostics(df, roles)
    panel = panel_checks(df, roles)
    report = {
        "file": str(path),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "roles": roles,
        "analysis_roles": roles,
        "agent_role_decision_required": not bool(roles),
        "role_decision_policy": "An agent must assign semantic roles from the research question, variable names, values, units, timing, and codebook evidence; the profiler does not assign them by keyword.",
        "columns_profile": profiles,
        "top_correlations": diagnostics.get("top_correlations", []),
        "collinearity_diagnostics": diagnostics,
        "panel_checks": panel,
        "warnings": warnings(df, profiles, roles, diagnostics),
    }
    return report


def markdown_report(report):
    lines = [
        "# Econometric Dataset Profile",
        "",
        f"- File: `{report['file']}`",
        f"- Rows: {report['rows']}",
        f"- Columns: {report['columns']}",
        "",
        "## Agent-Decided Roles",
    ]
    if report["roles"]:
        for k, v in report["roles"].items():
            lines.append(f"- {k}: `{v}`")
    else:
        lines.append("- None supplied. The agent must inspect the column profile, variable names, observed values, research question, and any codebook before creating `roles.json`.")
    lines += ["", "## Data Quality Warnings"]
    for w in report["warnings"] or ["No automatic warnings. Still check economics-specific measurement issues."]:
        lines.append(f"- {w}")
    if report["panel_checks"]:
        p = report["panel_checks"]
        lines += [
            "",
            "## Panel Candidate Checks",
            f"- Unit key: `{p['unit']}`",
            f"- Time key: `{p['time']}`",
            f"- Units: {p['n_units']}",
            f"- Periods: {p['n_periods']}",
            f"- Duplicate unit-time rows: {p['duplicate_unit_time_rows']}",
            f"- Periods per unit: min {p['min_periods_per_unit']}, median {p['median_periods_per_unit']}, max {p['max_periods_per_unit']}",
            f"- Balanced candidate: {p['balanced_candidate']}",
        ]
    treatment = report["analysis_roles"].get("treatment")
    outcome = report["analysis_roles"].get("outcome")
    if treatment and outcome:
        lines += [
            "",
            "## Agent-Decided Causal Pathway Map",
            "",
            "```mermaid",
            "graph LR",
            f'    T["Treatment: {treatment}"] --> Y["Outcome: {outcome}"]',
        ]
        mechanism = report["analysis_roles"].get("mechanism")
        if mechanism:
            lines += [
                f'    M["Mechanism: {mechanism}"]',
                "    T --> M --> Y",
            ]
        instrument = report["analysis_roles"].get("instrument")
        if instrument:
            lines += [
                f'    Z["Instrument: {instrument}"]',
                "    Z --> T",
            ]
        lines.append("```")
    lines += ["", "## Column Profile"]
    for p in report["columns_profile"]:
        pct_val = p.get("missing_pct")
        pct_str = f"{pct_val:.1%}" if pct_val is not None else "0.0%"
        base = f"- `{p['name']}` ({p['dtype']}): missing {p['missing']} ({pct_str}), unique {p['unique']}"
        if "mean" in p and p["mean"] is not None:
            def fmt(value):
                return "n/a" if value is None or pd.isna(value) else f"{value:.4g}"

            base += (
                f", mean {fmt(p.get('mean'))}, sd {fmt(p.get('std'))}, "
                f"min {fmt(p.get('min'))}, max {fmt(p.get('max'))}"
            )
        lines.append(base)
    lines += ["", "## Top Numeric Correlations"]
    for pair in report["top_correlations"] or [{"var1": "n/a", "var2": "n/a", "corr": "n/a"}]:
        if pair["var1"] == "n/a":
            lines.append("- Not enough numeric columns.")
        else:
            lines.append(f"- `{pair['var1']}` vs `{pair['var2']}`: {pair['corr']:.3f}")
    diagnostics = report["collinearity_diagnostics"]
    lines += ["", "## Regressor Design Diagnostics", f"- Status: {diagnostics['status']}"]
    if diagnostics["status"] == "ok":
        lines += [
            f"- Regressors checked: {', '.join(diagnostics['variables'])}",
            f"- Structural variables excluded: {', '.join(diagnostics['excluded_structural_variables']) or 'none'}",
            f"- Sample-adaptive correlation threshold: {diagnostics['adaptive_correlation_threshold']:.3f}",
            f"- Design rank: {diagnostics['design_matrix_rank']} / {diagnostics['design_matrix_columns']}",
            f"- Standardized condition number: {diagnostics['condition_number_standardized']:.3f}",
        ]
        for row in diagnostics["vif"]:
            value = "infinite" if row["vif"] is None else f"{row['vif']:.3f}"
            lines.append(f"- VIF `{row['variable']}`: {value}")
    else:
        lines.append(f"- Reason: {diagnostics['reason']}")
    lines += [
        "",
        "## Econometric Next Step",
        "- Build a variable dictionary with economic role, unit, timing, transformation, and measurement risk.",
        "- Map the pathway from treatment/main regressor to outcome before interpreting correlations.",
        "- Confirm model-ready sample, fixed effects, clustering, and identifying variation before regression.",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Profile a CSV/XLSX/DTA dataset for econometric research planning.")
    parser.add_argument("data_file")
    parser.add_argument("--sheet")
    parser.add_argument("--roles-json", help="Agent-reviewed semantic roles JSON; roles are never assigned from column-name keywords.")
    parser.add_argument("--out", required=True, help="Markdown report path.")
    parser.add_argument("--json-out", help="Optional JSON report path.")
    args = parser.parse_args()

    path = Path(args.data_file)
    df = read_data(path, sheet=args.sheet)
    roles = load_roles(args.roles_json)
    report = build_report(path, df, roles)
    Path(args.out).write_text(markdown_report(report), encoding="utf-8")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
