# Synthetic benchmark suite

## Scope

`scripts/run_synthetic_benchmark.py` creates local, deterministic fixtures with known truth. The suite deliberately includes realistic raster effects: anti-aliased Matplotlib rendering, gridlines, labels, markers, pale error bars, low-resolution resizing, and JPEG compression. It does not contain user data and does not use remote services.

## Cases and comparisons

| Chart family | Cases | Candidate methods | Correct measurement primitive |
|---|---|---|---|
| Line | Clean and low-resolution/JPEG line plots | single column, local-window median, continuity-aware clustered trace | local color trace plus continuity |
| Scatter | Colored point groups | global color centroid, connected components | one component centroid per marker |
| Grouped bars | Filled bars by series | single center column, component bounds | top edge of the matched rectangle |
| Stacked bars | Filled segments by category | treating segment top as height, segment run height | each matched segment's vertical span |
| Histogram | Three local variants: clean PNG, low-resolution JPEG, dark PNG | color components + calibrated bin geometry | coverage/precision 1.0, MAE <= 0.25, zero unmatched/missing bins |
| Boxplot | Four groups in vertical/horizontal clean PNG, low-resolution JPEG, and dark PNG; missing-median refusal | colour fill components + paired line geometry + calibrated axes | visible five-statistic summaries and visible outliers; group coverage/F1 1.0 and MAE <= 0.25; conservative `low_confidence` refusal |

The runner reports MAE and coverage. It ranks methods only inside the same chart family after normalizing MAE by that family's y-range. Do not compare raw MAE across families.

## Candidate compact-scatter benchmark contract

`scripts/run_scatter_benchmark.py` exercises `candidate_digitize_scatter.py` on deterministic light-background dark markers over a pale band and fitted line, same-colour markers/line, light markers on a dark background, low-resolution JPEG, partially touching markers, thin axes/text distractors, a line/text-only refusal panel, and a low-contrast marker that is visible only to the relaxed residual pass. Every supported fixture must achieve point precision/recall/F1 of 1.0 within its declared pixel tolerance. The unsupported panel must return `low_confidence`, authorize no numeric output, and emit no point rows. The residual fixture must retain its primary candidates but authorize none until the exposed `detector_residual` is resolved. This is synthetic candidate evidence only; held-out real-vector, held-out real-raster, and fair WebPlotDigitizer gates remain open.

## Stable boxplot benchmark contract

`scripts/run_boxplot_benchmark.py` creates only deterministic local synthetic fixtures and records truth, image hash, calibrated plot bounds and axes, explicit colours, tolerance, group/component matches, outlier matches, diagnostics, CSV rows, and overlays before applying quality gates. The exact variants are `vertical_clean`, `vertical_lowres_jpeg`, `vertical_dark`, `horizontal_clean`, `horizontal_lowres_jpeg`, `horizontal_dark`, and `vertical_missing_median`.

Each success variant must recover four groups with `group_coverage == 1.0`, `outlier_f1 == 1.0`, and `summary_mae <= 0.25`. The missing-median variant must be `rejected_as_expected`, with `low_confidence`, no invented median, and a nonempty median diagnostic. JSON report equality and matching CSV evidence are regression-tested.

## Candidate dedicated bar benchmark contract

`scripts/run_bar_benchmark.py` exercises `candidate_digitize_bar_chart.py` on deterministic vertical and horizontal grouped bars, positive and negative values, visible error intervals, vertical stacks, horizontal 100% stacks on a dark background, a low-resolution JPEG, and an ambiguous duplicate-rectangle refusal case. Unit and retained real-raster regressions additionally cover thick verified error strokes that split a pale bar and percent stacks whose visible separator pixels reduce the unnormalized fill total.

Every supported fixture must recover every expected rectangle with precision/coverage/F1 of 1.0, value MAE no greater than 0.25, and maximum absolute error no greater than 0.6. Clean error-interval coverage must be 1.0 with no endpoint error above 2.5 px. The low-resolution JPEG may return `partial_visible`; it must retain rectangle coverage 1.0, extract at least 75% of error intervals, keep accepted endpoint error at or below 3 px, and leave unsupported intervals as `not_extracted`. The ambiguous case must return `low_confidence` without a numeric value.

This suite is candidate evidence only. It does not satisfy the real-vector, held-out real-raster, or fair WebPlotDigitizer comparison gates required for stable promotion.

## How to extend safely

1. Add a deterministic fixture and preserve its truth in the benchmark report.
2. Add a baseline and a candidate method that use the same calibration information.
3. Include stressors that are plausible in real screenshots, not only ideal vector-like drawings.
4. Promote a production extractor only when its relevant benchmark score improves without loss of coverage on existing fixtures.
5. Keep all user-supplied images out of this suite unless explicit retention permission is recorded.
