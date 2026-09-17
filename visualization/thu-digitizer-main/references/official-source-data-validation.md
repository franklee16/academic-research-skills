# Official source-data validation

Use this procedure when a publication supplies an official XLSX, CSV, data archive, supplementary table, or user-provided ground-truth file. Its purpose is to validate a digitization of visible plotted values. It is not permission to infer unplotted raw observations, author fit parameters, or a metric that is absent from the source file.

## 1. Preserve provenance before interpreting values

Record the article or data URL, local file name, retrieval date, file hash when practical, workbook/sheet name, and the source range or columns used. Keep the downloaded source file unchanged.

Create a new validation artifact; never replace the original digitized CSV. The validation record should retain both sides of every comparison:

```text
panel_id, series_id, metric, displayed_statistic,
digitized_x, digitized_y,
source_x_raw, source_x_unit, source_x_normalized, source_x_scale_factor,
source_y_raw, source_y_normalized,
matched, validation_status, x_error, y_error, y_relative_error,
source_file, source_sheet, source_columns, mapping_evidence
```

Fields may be added for replicate count, confidence interval, PDF coordinates, or plot calibration residuals. Do not discard raw values after normalization.

## 2. Verify semantics before joining records

Build and save a mapping table for every panel or series:

| Plot property | Required source-data counterpart |
| --- | --- |
| panel and series | analyte, treatment, assay, or explicitly documented alias |
| y response | exact metric, channel, wavelength/ratio/difference, and units |
| x response | concentration/time/category, units, and any log transform |
| plotted point | mean, median, individual observation, fitted prediction, or another documented summary |
| uncertainty | SD, SEM, CI, range, or not plotted |

Do not map rows using an analyte name, worksheet position, or matching point count alone. Different panels can use the same analyte with different response channels; a source workbook can contain related but non-plotted metrics.

If the source contains repeated observations, compare the plotted point to the corresponding summary statistic only after the figure caption, methods, or source-data layout establishes the statistic. Record the replicate count and the aggregation calculation. Do not compare a plotted mean directly to one replicate.

## 3. Resolve units and axis transforms explicitly

Retain the raw source cell and declared unit. If a normalization is necessary, store the normalized value, scale factor, reason, and evidence from the axis labels, caption, source metadata, or a documented unit conversion.

- Never silently multiply or divide values merely to improve agreement.
- For logarithmic axes, fit/calibrate `log10(source_x_normalized)` against plot or PDF coordinates and assess residuals in log space.
- Check that the selected normalization yields a coherent axis mapping across all concentrations, not just a single endpoint.
- If the source header and plotted axis imply irreconcilable units, use `source_unit_unresolved` or `unit_or_metadata_mismatch`; do not choose a scale factor by guesswork.

Keep plot-display rounding distinct from coordinate-derived values and source values.

## 4. Match and compare conservatively

Join points using the verified panel/series/metric mapping plus concentration or category identity. On a numeric x axis, use calibrated x positions to help identify the matching source concentration only after unit/transform verification. Do not join by sorted row order alone.

Before calculating errors, verify the expected number of visible data points. Exclude or separately label legend symbols, decorative marks, rejected PDF paths, clipped points, and unmatched source rows.

Report at least:

- paired count and total visible digitized points;
- unmatched points and their reason;
- signed and absolute y error per point;
- per-panel MAE, RMSE, median absolute error, 95th-percentile absolute error when sample size permits, and maximum absolute error;
- x-axis error or log-axis calibration residual when x coordinates were digitized;
- an identity plot (`digitized` versus `source`) and/or an overlay replot.

Aggregate raw-unit y errors only for panels sharing the same response units. For heterogeneous response metrics, report per-panel errors and a clearly defined normalized error instead of one misleading aggregate.

## 5. Use coverage-aware statuses

Use a status per point or panel. Recommended values:

- `validated`: source mapping, units, displayed statistic, and matched value are verified.
- `partial_validated`: only a documented subset has a comparable source counterpart.
- `metric_absent_in_source_workbook`: the visible plot metric is not supplied, even if the analyte appears elsewhere.
- `source_unit_unresolved` or `unit_or_metadata_mismatch`: values exist but their scale cannot be justified.
- `not_comparable`: a source value is raw-only, a prediction, differently aggregated, or otherwise semantically mismatched.

Report coverage such as “42 of 56 visible points validated; 14 have a metric absent from the supplied workbook.” Do not classify missing or non-comparable source data as a failed digitization.

## 6. Keep curve claims separate from point validation

Agreement with source-derived points validates the extracted displayed points, subject to the mapping above. It does not establish that a reconstructed curve uses the authors' fit method, weights, constraints, or parameters.

When refitting a curve from extracted or source summaries, label it `refit_from_extracted_points` or `refit_from_source_summaries`. Compare to author parameters only when those parameters and the model are explicitly supplied. If authors report a goodness-of-fit statistic based on replicate-level data, do not expect it to equal a fit based on plotted means.

## 7. Deliver auditable, separate outputs

Deliver the untouched extraction, a source-validation CSV, a machine-readable JSON summary, and visual comparison evidence. The JSON summary should include source provenance, mapping assumptions, transformations, coverage/status counts, error metrics, and limitations.

Treat sensitive supplementary data according to the user's retention preference. A public URL is useful provenance, but do not embed proprietary source values in a reusable benchmark without consent.
