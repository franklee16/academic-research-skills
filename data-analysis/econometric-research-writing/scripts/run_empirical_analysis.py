#!/usr/bin/env python3
"""Run reproducible baseline, robustness, and event-study outputs from agent-decided roles."""

import argparse
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm

from profile_econ_dataset import as_list, collinearity_diagnostics, load_roles, read_data


def unique(values):
    return list(dict.fromkeys(value for value in values if value))


def main_regressors(roles):
    return unique([*as_list(roles.get("treatment")), *as_list(roles.get("main_regressors"))])


def required_columns(roles):
    return unique(
        [
            *as_list(roles.get("outcome")),
            *main_regressors(roles),
            *as_list(roles.get("controls")),
            *as_list(roles.get("fixed_effects")),
            *as_list(roles.get("cluster")),
            *as_list(roles.get("unit")),
            *as_list(roles.get("time")),
            *as_list(roles.get("event_time")),
        ]
    )


def validate_roles(df, roles):
    if not roles.get("outcome"):
        raise ValueError("roles.json must contain an agent-decided `outcome`.")
    if not main_regressors(roles):
        raise ValueError("roles.json must contain `treatment` or `main_regressors`.")
    missing = [column for column in required_columns(roles) if column not in df.columns]
    if missing:
        raise ValueError(f"roles.json references missing columns: {', '.join(missing)}")
    if len(as_list(roles["outcome"])) != 1:
        raise ValueError("This runner currently requires exactly one outcome per analysis.")


def markdown_table(frame):
    if frame.empty:
        return "_No rows._\n"
    display = frame.copy().fillna("")
    headers = [str(column).replace("|", "\\|") for column in display.columns]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in display.itertuples(index=False, name=None):
        values = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def focused_variables(df, roles):
    requested = unique(
        [
            *as_list(roles.get("descriptive_variables")),
            *as_list(roles.get("outcome")),
            *main_regressors(roles),
            *as_list(roles.get("controls")),
            *as_list(roles.get("mechanisms")),
            *as_list(roles.get("moderators")),
            *as_list(roles.get("instruments")),
        ]
    )
    return [column for column in requested if column in df.columns]


def descriptive_statistics(df, roles):
    rows = []
    for column in focused_variables(df, roles):
        original = df[column]
        is_numeric = pd.api.types.is_numeric_dtype(original)
        series = pd.to_numeric(original, errors="coerce").replace([np.inf, -np.inf], np.nan)
        valid = series.dropna()
        nonmissing = original.dropna()
        row = {
            "variable": column,
            "n": int(nonmissing.size),
            "missing": int(len(original) - nonmissing.size),
            "unique": int(nonmissing.nunique()),
            "mean": valid.mean() if is_numeric and not valid.empty else np.nan,
            "sd": valid.std() if is_numeric and valid.size > 1 else np.nan,
            "p25": valid.quantile(0.25) if is_numeric and not valid.empty else np.nan,
            "median": valid.median() if is_numeric and not valid.empty else np.nan,
            "p75": valid.quantile(0.75) if is_numeric and not valid.empty else np.nan,
            "min": valid.min() if is_numeric and not valid.empty else np.nan,
            "max": valid.max() if is_numeric and not valid.empty else np.nan,
        }
        rows.append(row)
    return pd.DataFrame(rows).round(6)


def encoded_terms(frame, columns, prefix):
    if not columns:
        return pd.DataFrame(index=frame.index), {}
    raw = frame[columns].copy()
    numeric = list(raw.select_dtypes(include=[np.number, "bool"]).columns)
    categorical = [column for column in columns if column not in numeric]
    parts = []
    roles = {}
    if numeric:
        numeric_frame = raw[numeric].apply(pd.to_numeric, errors="coerce").astype(float)
        numeric_frame.columns = [str(column) for column in numeric_frame.columns]
        parts.append(numeric_frame)
        roles.update({str(column): prefix for column in numeric_frame.columns})
    if categorical:
        dummies = pd.get_dummies(raw[categorical], prefix=[str(column) for column in categorical], drop_first=True, dtype=float)
        parts.append(dummies)
        roles.update({str(column): prefix for column in dummies.columns})
    result = pd.concat(parts, axis=1) if parts else pd.DataFrame(index=frame.index)
    return result, roles


def build_design(frame, regressors, controls, fixed_effects):
    main_x, term_roles = encoded_terms(frame, regressors, "main")
    control_x, control_roles = encoded_terms(frame, controls, "control")
    term_roles.update(control_roles)
    x = pd.concat([main_x, control_x], axis=1)
    if fixed_effects:
        fe = pd.get_dummies(
            frame[fixed_effects].astype("category"),
            prefix=[f"FE:{column}" for column in fixed_effects],
            drop_first=True,
            dtype=float,
        )
        x = pd.concat([x, fe], axis=1)
        term_roles.update({str(column): "fixed_effect" for column in fe.columns})
    x = x.loc[:, ~x.columns.duplicated()].astype(float)
    varying = [column for column in x if x[column].nunique(dropna=True) > 1]
    x = sm.add_constant(x[varying], has_constant="add")
    term_roles["const"] = "intercept"
    return x, term_roles


def fit_model(df, outcome, regressors, controls=None, fixed_effects=None, cluster=None, covariance=None):
    controls = unique(controls or [])
    fixed_effects = unique(fixed_effects or [])
    needed = unique([outcome, *regressors, *controls, *fixed_effects, *as_list(cluster)])
    frame = df[needed].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if frame.empty:
        raise ValueError("No complete observations remain for the requested model.")
    y = pd.to_numeric(frame[outcome], errors="coerce")
    frame = frame.loc[y.notna()].copy()
    y = y.loc[y.notna()].astype(float)
    x, term_roles = build_design(frame, regressors, controls, fixed_effects)
    if np.linalg.matrix_rank(x.to_numpy(dtype=float)) < x.shape[1]:
        rank_status = "rank_deficient"
    else:
        rank_status = "full_rank"
    model = sm.OLS(y, x)
    cluster_column = as_list(cluster)[0] if cluster else None
    if covariance is None:
        covariance = "cluster" if cluster_column else "HC3"
    covariance = str(covariance).lower()
    if covariance == "cluster":
        if not cluster_column:
            raise ValueError("Cluster covariance requested without a `cluster` role.")
        groups = frame[cluster_column]
        n_clusters = int(groups.nunique(dropna=True))
        if n_clusters < 2:
            raise ValueError("Clustered standard errors require at least two clusters.")
        fitted = model.fit(cov_type="cluster", cov_kwds={"groups": groups, "use_correction": True})
    elif covariance in {"hc0", "hc1", "hc2", "hc3"}:
        covariance = covariance.upper()
        fitted = model.fit(cov_type=covariance)
    elif covariance == "nonrobust":
        fitted = model.fit()
    else:
        raise ValueError(f"Unsupported covariance type: {covariance}")
    return fitted, term_roles, {
        "nobs": int(fitted.nobs),
        "covariance": covariance,
        "cluster": cluster_column,
        "n_clusters": n_clusters if covariance == "cluster" else None,
        "fixed_effects": fixed_effects,
        "controls": controls,
        "rank_status": rank_status,
    }


def coefficient_rows(fitted, term_roles, model_name, metadata, include_fixed_effects=False):
    confidence = fitted.conf_int(alpha=0.05)
    rows = []
    for term in fitted.params.index:
        role = term_roles.get(str(term), "other")
        if role == "fixed_effect" and not include_fixed_effects:
            continue
        rows.append(
            {
                "model": model_name,
                "term": str(term),
                "role": role,
                "coefficient": float(fitted.params[term]),
                "std_error": float(fitted.bse[term]),
                "p_value": float(fitted.pvalues[term]),
                "ci_95_low": float(confidence.loc[term, 0]),
                "ci_95_high": float(confidence.loc[term, 1]),
                "n": metadata["nobs"],
                "covariance": metadata["covariance"],
                "cluster": metadata["cluster"] or "",
                "n_clusters": metadata["n_clusters"] or "",
                "fixed_effects": ", ".join(metadata["fixed_effects"]),
                "design_rank_status": metadata["rank_status"],
            }
        )
    return rows


def default_robustness_specs(roles):
    controls = as_list(roles.get("controls"))
    fixed_effects = as_list(roles.get("fixed_effects"))
    cluster = as_list(roles.get("cluster"))
    specs = [{"name": "Minimal", "controls": [], "fixed_effects": [], "covariance": "nonrobust"}]
    if controls:
        specs.append({"name": "With controls", "controls": controls, "fixed_effects": [], "covariance": "HC3"})
    specs.append(
        {
            "name": "Preferred",
            "controls": controls,
            "fixed_effects": fixed_effects,
            "covariance": "cluster" if cluster else "HC3",
        }
    )
    if cluster:
        specs.append({"name": "Preferred HC3", "controls": controls, "fixed_effects": fixed_effects, "covariance": "HC3"})
    deduplicated = []
    seen = set()
    for spec in specs:
        signature = (tuple(spec["controls"]), tuple(spec["fixed_effects"]), spec["covariance"])
        if signature not in seen:
            seen.add(signature)
            deduplicated.append(spec)
    return deduplicated


def run_robustness(df, roles):
    outcome = as_list(roles["outcome"])[0]
    regressors = main_regressors(roles)
    cluster = roles.get("cluster")
    specs = default_robustness_specs(roles) + as_list(roles.get("robustness_specs"))
    rows = []
    for spec in specs:
        sample = df.query(spec["sample_query"]) if spec.get("sample_query") else df
        fitted, term_roles, metadata = fit_model(
            sample,
            spec.get("outcome", outcome),
            as_list(spec.get("main_regressors")) or regressors,
            controls=as_list(spec.get("controls")),
            fixed_effects=as_list(spec.get("fixed_effects")),
            cluster=spec.get("cluster", cluster),
            covariance=spec.get("covariance"),
        )
        model_rows = coefficient_rows(fitted, term_roles, spec.get("name", "Robustness"), metadata)
        rows.extend(row for row in model_rows if row["role"] == "main")
    return pd.DataFrame(rows).round(6)


def event_periods(series, roles):
    numeric = pd.to_numeric(series, errors="coerce")
    observed = sorted({int(value) for value in numeric.dropna() if float(value).is_integer()})
    window = roles.get("event_window")
    if window:
        lower, upper = [int(value) for value in window]
        numeric = numeric.clip(lower=lower, upper=upper)
        observed = sorted({int(value) for value in numeric.dropna() if float(value).is_integer()})
    elif len(observed) > 15:
        numeric = numeric.clip(lower=-5, upper=5)
        observed = sorted({int(value) for value in numeric.dropna() if float(value).is_integer()})
    return numeric, observed


def run_event_study(df, roles, output_dir):
    event_time = roles.get("event_time")
    if not event_time:
        return None
    reference = int(roles.get("event_reference", -1))
    binned_event_time, periods = event_periods(df[event_time], roles)
    if reference not in periods:
        raise ValueError(f"Event-study reference period {reference} is not observed in the selected window.")
    work = df.copy()
    event_columns = []
    for period in periods:
        if period == reference:
            continue
        name = f"event_{period:+d}"
        work[name] = (binned_event_time == period).astype(float)
        event_columns.append(name)
    fitted, term_roles, metadata = fit_model(
        work,
        as_list(roles["outcome"])[0],
        event_columns,
        controls=as_list(roles.get("controls")),
        fixed_effects=as_list(roles.get("fixed_effects")),
        cluster=roles.get("cluster"),
    )
    rows = coefficient_rows(fitted, term_roles, "Event study", metadata)
    coefficient_map = {row["term"]: row for row in rows if row["role"] == "main"}
    plot_rows = []
    for period in periods:
        if period == reference:
            plot_rows.append({"event_time": period, "coefficient": 0.0, "std_error": 0.0, "ci_95_low": 0.0, "ci_95_high": 0.0, "reference": True})
        else:
            row = coefficient_map[f"event_{period:+d}"]
            plot_rows.append({"event_time": period, **{key: row[key] for key in ["coefficient", "std_error", "ci_95_low", "ci_95_high"]}, "reference": False})
    results = pd.DataFrame(plot_rows).round(6)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.errorbar(
        results["event_time"],
        results["coefficient"],
        yerr=[results["coefficient"] - results["ci_95_low"], results["ci_95_high"] - results["coefficient"]],
        fmt="o-",
        color="#1f4e79",
        ecolor="#6b7280",
        capsize=3,
        linewidth=1.2,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="#9a3412", linestyle="--", linewidth=0.9)
    ax.scatter([reference], [0], marker="s", color="black", zorder=4, label=f"Reference: {reference}")
    ax.set_xlabel("Event time")
    ax.set_ylabel(f"Coefficient on event-time indicator ({roles['outcome']})")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "event_study.png", dpi=300)
    fig.savefig(output_dir / "event_study.pdf")
    plt.close(fig)
    return results


def write_frame(frame, stem, output_dir, title, note, source="Computed from the input dataset using the recorded agent-reviewed specification."):
    frame.to_csv(output_dir / f"{stem}.csv", index=False)
    markdown = f"# {title}\n\n{markdown_table(frame)}\nNotes: {note}\n\nSource: {source}\n"
    (output_dir / f"{stem}.md").write_text(markdown, encoding="utf-8")


def run_analysis(data_path, roles_path, output_dir, sheet=None):
    df = read_data(Path(data_path), sheet=sheet)
    roles = load_roles(roles_path)
    validate_roles(df, roles)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    descriptive = descriptive_statistics(df, roles)
    write_frame(descriptive, "descriptive_statistics", output_dir, "Table 1. Descriptive Statistics", "Variables are selected from agent-decided economic roles; missing values are reported explicitly.")

    outcome = as_list(roles["outcome"])[0]
    regressors = main_regressors(roles)
    fitted, term_roles, metadata = fit_model(
        df,
        outcome,
        regressors,
        controls=as_list(roles.get("controls")),
        fixed_effects=as_list(roles.get("fixed_effects")),
        cluster=roles.get("cluster"),
    )
    baseline = pd.DataFrame(coefficient_rows(fitted, term_roles, "Baseline", metadata)).round(6)
    write_frame(baseline, "baseline_results", output_dir, "Table 2. Baseline Estimates", "Fixed-effect coefficients are absorbed from the displayed table. The covariance estimator and clustering variable are reported in the table.")

    robustness = run_robustness(df, roles)
    write_frame(robustness, "robustness_results", output_dir, "Table 3. Robustness Results", "Rows report the main regressor across minimal, controlled, preferred, and alternative-inference specifications.")

    diagnostics = collinearity_diagnostics(df, roles)
    (output_dir / "design_diagnostics.json").write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False), encoding="utf-8")
    diagnostics_lines = ["# Design-Matrix Diagnostics", "", f"- Status: {diagnostics['status']}"]
    for warning in diagnostics.get("warnings", []):
        diagnostics_lines.append(f"- Warning: {warning}")
    if diagnostics["status"] == "ok":
        diagnostics_lines.extend(
            [
                f"- Variables: {', '.join(diagnostics['variables'])}",
                f"- Excluded structural variables: {', '.join(diagnostics['excluded_structural_variables']) or 'none'}",
                f"- Adaptive correlation threshold: {diagnostics['adaptive_correlation_threshold']:.3f}",
                f"- Design rank: {diagnostics['design_matrix_rank']} / {diagnostics['design_matrix_columns']}",
                f"- Standardized condition number: {diagnostics['condition_number_standardized']:.3f}",
                "",
                "## Variance Inflation Factors",
                "",
                markdown_table(pd.DataFrame(diagnostics["vif"]).round(6)),
            ]
        )
    (output_dir / "design_diagnostics.md").write_text("\n".join(diagnostics_lines) + "\n", encoding="utf-8")

    event_results = run_event_study(df, roles, output_dir)
    if event_results is not None:
        write_frame(event_results, "event_study_results", output_dir, "Figure 1 Data. Event-Study Estimates", "The omitted reference period is set to zero. The figure displays 95% confidence intervals.")

    outputs = sorted(path.name for path in output_dir.iterdir() if path.is_file())
    manifest = {
        "input_data": str(data_path),
        "roles_file": str(roles_path),
        "agent_decided_roles": roles,
        "package_versions": {"python": platform.python_version(), "pandas": pd.__version__, "statsmodels": statsmodels.__version__},
        "outputs": outputs,
    }
    (output_dir / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_dir


def main():
    parser = argparse.ArgumentParser(description="Generate descriptive statistics, baseline and robustness regressions, clustered inference, and an optional event-study figure.")
    parser.add_argument("data_file")
    parser.add_argument("--roles-json", required=True, help="Agent-decided variable roles and empirical specification.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--sheet")
    args = parser.parse_args()
    output_dir = run_analysis(args.data_file, args.roles_json, args.output_dir, sheet=args.sheet)
    print(output_dir)


if __name__ == "__main__":
    main()
