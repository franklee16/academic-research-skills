# Table Implementation Recipes

Use the project's existing software and packages. Do not install an export package without authorization. Generate every cell from data/model objects, not from copied console output.

## Shared data contract

For a complex table, create a tidy intermediate result with fields such as:

`model_id`, `column_order`, `panel`, `outcome`, `term`, `term_order`, `estimate`, `std_error`, `conf_low`, `conf_high`, `p_value`, `nobs`, `n_clusters`, `covariance_type`, `cluster_variable`, `small_sample_correction`, `reference_distribution`, `reference_df`, `statistic`, `stat_value`, and specification flags.

Preserve full precision. Apply labels, rounding, stars, and blank/missing conventions only in the final formatting layer. Assert that the composite result key `(model_id, panel, term[, contrast_id])` is unique, that `model_id` maps one-to-one to `column_order`, and that all intended columns are present.

## LaTeX

Prefer `booktabs` plus `threeparttable`; use `dcolumn`, a correctly configured `siunitx`, or an equivalent method for decimal alignment that has been compiled with the chosen star macro. The following fragment uses `dcolumn` and therefore requires `\usepackage{booktabs,threeparttable,dcolumn}` plus `\newcommand{\sym}[1]{\rlap{\textsuperscript{#1}}}` in the manuscript preamble.

```latex
\begin{table}[!htbp]\centering
\caption{Informative table title}\label{tab:main}
\begin{threeparttable}
\begin{tabular}{l*{4}{D{.}{.}{3}}}
\toprule
& \multicolumn{2}{c}{Outcome family A}
& \multicolumn{2}{c}{Outcome family B} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
& \multicolumn{1}{c}{(1)} & \multicolumn{1}{c}{(2)}
& \multicolumn{1}{c}{(3)} & \multicolumn{1}{c}{(4)} \\
\midrule
% generated numeric cells may append zero-width stars, e.g. \sym{***}
\midrule
Observations & {} & {} & {} & {} \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]\footnotesize
\item \textit{Notes:} Generated note text.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

The placeholder skeleton illustrates hierarchy only; the build code must populate values directly. Put text cells under `\multicolumn{1}{c}{...}` when they occupy a numeric `D` column. The `D{.}{.}{3}` argument means three decimal places; it is not a `siunitx` format string. Compile-test negative values, parentheses rows, blank cells, and the longest star marker; reserve enough intercolumn space that zero-width stars do not collide. Avoid `\resizebox` until semantic splitting, shorter headers, `tabular*`, or landscape has been considered. Compile in the actual manuscript and inspect the log for overfull boxes and undefined references.

## R

Use stored model objects with an existing package such as `modelsummary`, `fixest::etable`, `broom`, `tinytable`, `gt`, or `kableExtra` when already available.

With `modelsummary`, define explicitly:

- a named model list in column order;
- `coef_map` for readable labels and row order;
- `gof_map` for observations, clusters, and the correct fit statistics;
- `stars` and numeric formatting;
- custom rows for controls, fixed effects, sample, tests, and diagnostics;
- spanners/panels in the chosen output backend.

Do not use regex-only term selection if it might silently include the wrong interaction. Inspect `broom::tidy()` or `coef()` names first. For `fixest::etable`, use `dict`, `keep`/`order`, `fitstat`, `group`, `headers`, and `notes` deliberately; ensure the displayed SE type matches the fitted call or explicit `vcov` argument.

For descriptive tables, compute summaries from one grouped pipeline so `N`, weights, missing-value rules, quantiles, and units are consistent. Do not mix summaries copied from separate commands.

## Stata

Prefer native `collect` for a dependency-free workflow or existing `eststo`/`esttab` when already installed.

With `esttab`/`estout`:

1. store each model with a meaningful name in the intended column order;
2. add specification facts and diagnostics programmatically using `estadd` or returned scalars;
3. use `keep()` and `order()` with exact coefficient names;
4. set coefficient/SE formats and stars once;
5. generate `mgroups()`, `mtitles()`, `stats()`, and notes from macros rather than editing the `.tex` file by hand.

Illustrative structure:

```stata
eststo clear
quietly regress outcome treatment controls, vce(cluster county_id)
eststo m1
estadd local county_fe "No"
estadd local year_fe "No"
estadd scalar n_clusters = e(N_clust)

quietly reghdfe outcome treatment controls, absorb(county_id year) vce(cluster county_id)
eststo m2
estadd local county_fe "Yes"
estadd local year_fe "Yes"
estadd scalar n_clusters = e(N_clust)

esttab m1 m2 using "output/table_main.tex", replace booktabs fragment ///
    keep(treatment) order(treatment) b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    stats(county_fe year_fe N n_clusters r2_a, ///
          labels("County FE" "Year FE" "Observations" "County clusters" "Adjusted R-squared"))
```

Adapt commands to packages already present; do not substitute `regress` for the user's estimator. Confirm the command actually stores `e(N_clust)` before adding it, and select the correct overall or within fit statistic for absorbed-effects models. After export, inspect the `.tex` for escaped labels and compile it. Native `collect` users should define dimensions, labels, styles, stars, and notes in code and save the collection for reproducibility.

## Python

Extract from `statsmodels`, `linearmodels`, or the project's estimator objects into a tidy `pandas` DataFrame. Do not parse a rendered text summary when attributes such as `params`, `bse`, `pvalues`, `conf_int`, `nobs`, and covariance metadata are available.

- Join columns by explicit term keys and preserve the requested order.
- Build coefficient and SE display rows only after numerical checks.
- Use `Styler`, `DataFrame.to_latex`, `summary_col`, or a project template as appropriate, but verify multi-index spanners and escaping.
- Record covariance type and cluster metadata separately; do not infer them from the presence of different SE values.
- For nonlinear transformations or linear combinations, use the estimator-supported covariance/test API rather than transforming only the point estimate. Use the delta method for regular smooth transformations when appropriate; allow transformed endpoints, bootstrap, simulation, profile/Fieller methods, or test inversion when the estimand and model require them, and label the method accurately.

## Word, spreadsheet, and HTML output

- Deliver an editable table, not an embedded image.
- Preserve semantic merges only for header spanners; avoid merged body cells.
- Set explicit column widths and repeat header rows across pages in Word.
- Use black rules and white cells; disable zebra striping unless the user requests a non-journal presentation.
- In spreadsheets, keep full-precision source values on a hidden/documented data sheet or in the build input and use a separate presentation sheet. Do not make the styled cells the sole analytical record.

## Render-and-verify loop

1. Generate the table from a clean analytical session.
2. Compare extracted values to the model objects programmatically.
3. Render LaTeX/Word/HTML in the target page geometry.
4. Inspect at final size for rule placement, wrapping, decimal alignment, font substitution, and note fit.
5. Regenerate after fixes; never patch exported numbers by hand.
