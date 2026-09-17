---
name: thu-digitizer
description: Extract and validate numeric data from chart images, PDF figures, and official source-data files locally and reproducibly, with calibrated axes, compact-scatter recovery plus residual audits, grouped/stacked bars, visible-label pie/donut validation, original-pixel aligned lattice composites such as UpSet plots, PDF vector inspection, line tracing, histograms, boxplots, error bars, CSV/JSON evidence, source-data cross-validation, and regression evaluation. Use when a user asks to recover or recreate chart data, extract scatter points, bars, printed pie/donut labels, or aligned memberships, check a PDF chart, assess digitization accuracy, validate against source data, or improve a chart-digitization workflow from corrected examples.
---

# THU Digitizer

Recover chart data without silently inventing values. Work locally unless the user explicitly approves a remote OCR or model service.

## Unified preflight router

For every new image or PDF, read [references/unified-routing.md](references/unified-routing.md) and run the unified preflight before choosing a family-specific extractor:

```powershell
& python scripts/thu_digitizer.py inspect `
  --input figure.png --chart-type histogram `
  --output-report preflight-report.json `
  --output-spec figure-spec.json
```

If the chart type is unknown, omit `--chart-type`; the router must return `needs_chart_type_confirmation` and must not authorize numeric extraction. Treat a supplied chart type, full-image panel, appearance estimate, coordinate model, or route as a proposal until its verification field is explicit. Validate a completed spec with `scripts/thu_digitizer.py validate-spec` before extraction.

The registry in `scripts/extractor_registry.py` is the single machine-readable map from chart types and input composition to stable, candidate, assisted, unsupported, and refusal routes. Registry presence is not proof of support. Never send an unknown, non-Cartesian, raster-only, or incompatible chart to a convenient XY/PDF extractor merely because it is available.

## Evidence-bound adaptive execution

Keep source identity, original-pixel measurement, calibrated coordinates, non-invention, ambiguity labels, and review evidence as hard requirements. Treat registered scripts as the default deterministic strategy, not as the only strategy that may emit candidate values. Read [references/adaptive-execution.md](references/adaptive-execution.md) before selecting the execution freedom.

Treat GPT-5.6 Sol and Terra as strong-model profiles when the runtime identifies the current model by either name. A strong profile may produce a separate `model_assisted_candidate` when a registered implementation is incompatible with the visible grammar, unstable under reasonable verified bounds, contradicted by its overlay, or returns `low_confidence`/`numeric_output_authorized: false`. Preserve every deterministic report unchanged; never rewrite a failed script result as successful. For weak or unidentified profiles, retain the registered deterministic or hybrid workflow.

For a weak or unidentified model, or after any missed/extra-mark correction, read [references/weak-model-execution.md](references/weak-model-execution.md). Enforce the inventory, locked-exclusion, registered-detector, family-completeness, and original-resolution review loop. Do not let model narration substitute for the coverage ledger or residual audit.

## Original-raster coordinate invariant

Measure every raster against the exact original file recorded by SHA-256, width, and height. Keep all pixel coordinates in `original_raster_pixels`. Never measure a chat preview, thumbnail, browser screenshot, resized copy, enlarged crop, overlay, or recreation; use enlargement only for review. Refuse a source-contract mismatch instead of estimating a scale factor. Preserve the original canvas dimensions in every recreation.

For repeated aligned layers such as top bars, row bars, a membership lattice, connectors, and categorical strips, read [references/original-pixel-lattice-composites.md](references/original-pixel-lattice-composites.md) and run the registered lattice-composite candidate. Never pass expected row, column, active-node, or intersection counts to detection.

## Binding research-quality baseline

Before designing, benchmarking, or promoting any new extractor, read [references/research-quality-baseline.md](references/research-quality-baseline.md). Its scope statements, comparative protocol, type-specific metrics, held-out robustness tests, evidence requirements, and promotion gates are mandatory. Do not call a benchmark-only route a supported extractor, and do not claim to exceed WebPlotDigitizer without its documented fair comparison.

## PDF-first routing (candidate / assisted)

When the source is a PDF, read [references/vector-pdf-chart-extraction.md](references/vector-pdf-chart-extraction.md) before digitizing. Inspect the requested page with `scripts/inspect_pdf_vectors.py` before rasterizing:

```powershell
& python scripts/inspect_pdf_vectors.py `
  --input paper.pdf --page 8 --output-report vector-inspection.json
```

Route as follows:

- `vector_paths_detected` or `mixed_vector_and_raster`: visually inspect the target panel, axes, and path geometry. Mixed content is expected; raster strips can coexist with vector points and curves.
- Verified vector markers + verified axes + excluded legend: use direct PDF-space marker centres and calibrated transforms. Keep original PDF coordinates, coordinate-derived values, display labels, calibration residuals, accepted/rejected path counts, and a centre-ring overlay.
- Any ambiguous marker, legend, panel, tick, or transform: use the calibrated raster workflow or return `low_confidence`/`not_extracted`.

This is a candidate assisted route, not a stable automatic extractor. It recovers visible plotted geometry only; never infer author raw observations, replicates, error bars, fit parameters, or hidden curve settings. For a log axis, calibrate `log10(value)` against PDF coordinates rather than applying a linear mapping. Label a newly fitted curve as a refit from extracted points, not the source author's fit.

## Official source-data validation

When an article provides an official XLSX, CSV, archive, or a user supplies ground-truth data, read [references/official-source-data-validation.md](references/official-source-data-validation.md) before comparing values. Source data becomes validation ground truth only after the panel-to-metric, unit, concentration, and summary-statistic mapping is verified.

- Keep the digitization output immutable; create a separate source-validation CSV, JSON summary, and identity plot or overlay.
- Map each visual panel explicitly to analyte/series, response metric, units, source columns, concentration transform, and displayed statistic. Matching an analyte name alone is not sufficient.
- Preserve raw source values and any unit normalization factor with its evidence. Never silently rescale a source column to force agreement with axis labels.
- Report paired coverage and statuses separately: `validated`, `partial_validated`, `metric_absent_in_source_workbook`, `source_unit_unresolved`, or `not_comparable`. Missing source coverage is not an extraction failure.
- Compare displayed summaries to corresponding source summaries, not individual replicates. A point-level match validates visible plotted values; it does not prove the authors' original fitting method or hidden parameters.

## Public gallery integrity

When publishing a gallery case, the primary CSV, static recreation, and
interactive recreation must be driven solely by image- or PDF-visible
extraction. Do not publish a “source-data mapping” as an extraction case, even
when a workbook makes the redraw look more faithful.

- Keep source workbooks, matched values, validation statistics, and identity
  plots in a separate validation asset. They may validate a digitization, but
  they must never be imported by the renderer or included in the downloadable
  extraction table.
- A visible mark that is occluded, fused, or not separable stays missing or
  `not_extracted`; never fill it from a source workbook.
- Preserve original and recreation canvases at identical dimensions. For an
  interactive recreation, use the original raster canvas/viewBox and retained
  plot bounds so axes can be compared directly side by side.
- Every hoverable mark must expose the exact primary-CSV fields that generated
  it. Decorative paths and labels must not block pointer events on data marks.
- Group gallery cards by broad extraction grammar only. A case may retain its
  concrete subtype (for example, scatter-line or dose-response curve) in its
  title, but not as a separate top-level capability claim.

### Dose-response curves from vector PDFs (candidate)

For concentration-response panels whose markers and paths remain vector objects, use `scripts/candidate_digitize_dose_response_pdf.py` through `extract_dose_response_pdf`. Supply a visually verified panel ROI, a verified main-plot ROI, two anchors for the displayed log-concentration coordinate, two y-axis anchors, and separate marker/curve vector colours for every series. Keep a vehicle/control point on a broken-axis segment distinct from the calibrated concentration axis; never assign it an invented molar concentration.

Recover marker centres, only those error-bar endpoints that remain visibly drawn outside the marker, and the authored curve path as separate products. Label the curve `curve_path_traced`: a PDF path is not evidence for the authors' 4PL parameters. If an official workbook provides mean, SD and N, validate point values against the displayed mean and visible intervals against `mean ± SD/sqrt(N)` in a separate CSV. Mark intervals hidden entirely by marker glyphs as `sem_occluded_by_marker`, not extraction failures, and mark missing vehicle rows as `vehicle_not_present_in_source_workbook`.

The Nature Communications Fig. 4d regression case can be rebuilt with:

```powershell
& python scripts/build_natcom_dose_response_case.py `
  --pdf article.pdf --source-data source-data.xlsx --output-dir evidence
```

This route remains candidate until additional marker styles, linear/log axis variants, raster-only inputs, multi-panel layouts, missing-curve/error-bar cases, held-out publications, and matched WebPlotDigitizer comparisons satisfy the binding promotion gates.

## Workflow

1. Run `scripts/thu_digitizer.py inspect` to record input composition and create a FigureSpec template. An unverified route proposal never authorizes values.
2. Confirm the panel, chart grammar, coordinate model, and recoverable representation. Refuse unknown or unsupported transforms.
3. Locate plot bounds and the required axis anchors. Use OCR only to propose labels; verify selected ticks against pixels or PDF geometry.
4. Select deterministic, hybrid, or strong-model-assisted execution using [references/adaptive-execution.md](references/adaptive-execution.md). Prefer verified direct vector centres and compatible registered extractors; do not force an incompatible family extractor or tune it toward an expected answer.
5. Treat points, curves, rectangles, boxes, colour cells, error bars, legends, and annotations as separate visible grammars before assembling chart semantics.
6. Run the family completeness check: require a clear residual audit for compact scatter, a declared-slot coverage ledger with standard reason codes for bars and visible labels, or complete active/inactive/ambiguous Cartesian-cell classification for aligned lattices. A completeness pass may block authorization; it must never add values.
7. Deliver the immutable CSV, JSON report, overlay, and (when requested) a recreation. State whether positions/curves are direct, traced, refitted, low-confidence, or unmeasured.
8. If official source data, ground truth, or user corrections are available, verify the semantic mapping and run a separate validation report. Never overwrite the original extraction with source-normalized values.

## Calibrated histogram extraction

The stable extractor supports color-distinct histogram bars with calibrated x/y axes. Use `scripts/digitize_histogram.py` through its `extract_histogram` API with explicit `plot_bounds`, two x-axis calibration points, two y-axis calibration points, and the bar color. Its result is calibrated bin edges and heights, not the original raw observations.

For local evidence, run the deterministic companion benchmark:

```powershell
& python scripts/run_histogram_benchmark.py --output-dir D:\Scratch\thu-digitizer-histogram-benchmark
```

It writes CSV, JSON, and overlay evidence for the clean PNG, low-resolution JPEG, and dark PNG fixtures. For a user chart, retain equivalent CSV, JSON, and overlay evidence alongside the calibrated extraction.

### Calibrated heatmaps (candidate)

For a rectangular heatmap with a readable continuous colour bar, use `scripts/candidate_digitize_heatmap.py` through `extract_heatmap`. Supply the verified grid bounds, ordered row/column labels, row and column counts implied by those labels, colour-bar bounds, and its two endpoint values. The route samples each cell away from borders, maps its modal fill colour to the nearest colour-bar row, and separately detects visibly rendered white significance marks.

Treat a cell matching the top or bottom colour-bar colour as interval-censored (`clipped_high` or `clipped_low`): the raster cannot distinguish the displayed endpoint from a source magnitude beyond it. Preserve the immutable colour-derived CSV before any official-source comparison. When an official workbook is available, validate it in a separate CSV/report and keep figure/source significance mismatches rather than rewriting the visible extraction.

The Nature Medicine Fig. 4c regression case and its independent SuppData 8 validation can be rebuilt with:

```powershell
& python scripts/build_natmed_heatmap_case.py `
  --input fig4-full.png --source-data supplementary-data.xlsx
```

This route remains candidate until clean, low-resolution/JPEG, dark/palette-shifted, missing-colour-bar, nonuniform-grid, and held-out publication cases meet the binding promotion gates.

### Research-grade raster trace candidate (continuity mode)

For a line, time-series, ROC/PR, survival, or fitted-curve panel whose visible
stroke is continuous enough to follow, use the continuity candidate in
`scripts/digitize_line_chart.py` rather than relying on one-pixel-per-sample
colour lookup:

```powershell
& python scripts/digitize_line_chart.py `
  --input figure.png --output-csv extracted.csv --report extraction_report.json `
  --trace-mode continuity --plot-bounds 176,63,945,252 `
  --x-px-min 176 --x-value-min 0 --x-px-max 945 --x-value-max 850 `
  --y-px-min 63 --y-value-min 1.35 --y-px-max 252 --y-value-max 0.4 `
  --series curve=#141414 --sample-values 0,25,50,75,100
```

This route fits an affine calibration in transformed value space (including
`log10`), accepts additional tick anchors, scores anti-aliased colour softly,
and follows the lowest-cost continuous path across candidate runs. It records
coverage, jumps, support, per-sample pixel/value uncertainty, and explicit gap
statuses. A blank or occluded span remains missing; it is never interpolated to
make a complete table. Horizontal borders, gridlines, legends, crossings and
same-colour annotations still require a verified ROI and a series-level review.
The implementation is a candidate until the held-out raster benchmark and a
matched WebPlotDigitizer comparison pass the promotion gates; the legacy
`sample` mode remains available for backward-compatible runs.

## Calibrated boxplot extraction

The stable extractor supports colour-distinct, calibrated multi-group boxplots in vertical or horizontal layouts. Use `scripts/digitize_boxplot.py` through `extract_boxplots` with explicit `plot_bounds`, x/y calibration, `box_color`, `line_color`, `outlier_color`, and a verified orientation. It returns only the visible five-statistic summary (`q1`, `median`, `q3`, `lower_whisker`, `upper_whisker`) and visible outliers for each group; it does not recover raw samples.

Require distinct fill, line, and outlier colours. Refuse conservatively with `low_confidence` when a median, whisker cap/spine pairing, box fill, calibration, or a unique automatic orientation is not visibly supported.

For local evidence, run:

```powershell
& python scripts/run_boxplot_benchmark.py --output-dir D:\Scratch\thu-digitizer-boxplot-benchmark
```

The deterministic benchmark renders four groups in vertical and horizontal clean PNG, low-resolution JPEG, and dark PNG variants, plus a missing-median refusal case. It writes calibrated component evidence, CSV, JSON, and overlays before enforcing the quality gates.

### Paired outline boxplots (candidate)

For publication boxplots where one series is unfilled, a coloured fill is split by its median, and outlier rings share the structural line colour, use `scripts/candidate_digitize_outline_boxplot.py` through `extract_outline_boxplots`. This candidate detects repeated box-width stroke centres, validates ordered Q3/median/Q1 strokes against the two vertical box sides, pairs whisker caps with centre-spine evidence, classifies filled versus unfilled series by interior colour support, and detects hollow outlier rings outside the visible whiskers.

Keep this route separate from the stable fill-component extractor. Require a calibrated linear y-axis, retain every pixel coordinate and stroke-support diagnostic, and generate an overlay before accepting a group. Report a raster-unresolved whisker as coincident with the adjacent quartile only when the report preserves that flag. The output remains the visible five-number summary and visible outliers—not the underlying observations. Promote this route only after held-out publication figures and the binding comparative gates are complete.

The Nature Medicine Fig. 4b regression case can be rebuilt from a retained official image with:

```powershell
& python scripts/build_natmed_box_case.py --input fig4-full.png
```

## Deterministic sampled line extraction

Run the bundled script after axis calibration. Pixel coordinates use the original raster, with `(0, 0)` at the upper-left.

```powershell
& python scripts/digitize_line_chart.py `
  --input chart.png --output-csv extracted.csv --report extraction_report.json `
  --x-px-min 57 --x-value-min 2004 --x-px-max 363 --x-value-max 2014 `
  --y-px-min 1 --y-value-min 70 --y-px-max 297 --y-value-max 0 `
  --plot-bounds 44,1,375,297 `
  --sample-values 2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014 `
  --series 'biodiversity=#e2070b' `
  --series 'ecosystem_services=#bdbdbd' `
  --series 'economic_language=#0000dc' `
  --color-tolerance 28 --overlay extraction_overlay.png
```

Use `--error-color '#e6e6e6' --error-tolerance 12 --error-min-span 8` only after sampling the actual error-bar color. The report will mark a bar `not_extracted` if it lacks enough vertical evidence.

## Compact filled scatter extraction (candidate, low freedom)

For a Cartesian raster scatter panel with compact filled markers, read [references/compact-scatter-extraction.md](references/compact-scatter-extraction.md) and run `scripts/candidate_digitize_scatter.py` once per panel. Do not use `digitize_line_chart.py`, visual counting, or ad hoc connected components for this grammar. Supply verified plot bounds, at least two anchors per axis, and `dark`, `light`, or `color` marker mode. The candidate uses distance-transform peaks to split partially touching markers and excludes thin axes, curves, and text by compact-radius evidence.

```powershell
& python scripts/candidate_digitize_scatter.py `
  --input figure.png --plot-bounds LEFT,TOP,RIGHT,BOTTOM `
  --x-anchor XPIXEL1,XVALUE1 --x-anchor XPIXEL2,XVALUE2 `
  --y-anchor YPIXEL1,YVALUE1 --y-anchor YPIXEL2,YVALUE2 `
  --marker-mode dark `
  --output-csv points.csv --report scatter-report.json --overlay scatter-overlay.png
```

Open the overlay at original resolution. Accept candidate values only when the report says `numeric_output_authorized: true`, `residual_audit.status` is `clear`, every ring is centred on a visible marker, multi-peak components are plausible touching markers, and suppressed peaks are reviewed. A magenta residual box blocks authorization and is never promoted into the CSV; correct only visibly wrong configuration/exclusions and rerun. Treat script authorization as candidate-level evidence, not final acceptance: if the overlay contradicts the report or reasonable verified bounds produce an unstable point set, preserve that run as failed deterministic evidence and use the adaptive fallback policy. If the panel prints Pearson's `R`, pass `--annotated-pearson-r`; use it only as a validation gate, never as a target for adding or removing points. Do not pass an expected point count. Hollow markers, bubbles, dense swarms, and perfectly coincident or fully occluded points are outside this route.

## Aligned lattice composites (candidate, low freedom)

For an UpSet plot or another raster composite with repeated column bars, row bars, and a complete categorical membership grid, create a source-locked configuration and run the registered candidate:

```powershell
python scripts/candidate_digitize_lattice_composite.py init-config `
  --input figure.png --output lattice-config.json

python scripts/candidate_digitize_lattice_composite.py extract `
  --input figure.png --config lattice-config.json --output-dir evidence
```

Fill only visibly verified ROIs, one colour or a verified colour list per layer, rendered-size ranges, support thresholds, labels, printed values, and optional independent axis anchors. Prefer actual row/column bars as guides; when bars are separate from the matrix or subpixel, a complete repeated glyph row/column may be declared `membership_guides`, with the role recorded and inapplicable value-bar geometry validation disabled. The implementation must derive guide centres before consulting semantic array lengths and must classify every row-by-column cell as `active`, `inactive`, or `ambiguous`. Accept numeric output only when `numeric_output_authorized: true`, the source identity matches, every configured validation passes, and no cell is ambiguous. Never select guide roles or tune thresholds from expected counts. Keep this route `candidate`; it recovers visible aligned geometry and verified printed values, not hidden records or occluded memberships.

### Assisted grouped and stacked bars (candidate)

Use `scripts/candidate_digitize_bar_chart.py` for colour-distinct vertical or horizontal simple/grouped bars and visible stacked segments after verifying the plot bounds, linear value-axis anchors, category centres, layout, baseline, and one colour per series. The output is visible rectangle geometry and calibrated endpoints, not the records summarized by each bar.

When a legend or decorative swatch shares a series colour inside the plot ROI, pass one or more visually verified `exclude_regions` (CLI: `--exclude-region left,top,right,bottom`). The report must retain every excluded component and the exclusion rectangles. Never use exclusion regions merely to remove inconvenient candidate bars, and refuse when a legend cannot be separated from plotted geometry.

The Nature Communications Fig. 2b regression case can be rebuilt with `scripts/build_natcom_grouped_bar_case.py`. Its primary 32-row CSV is raster-derived; retained PDF rectangles are an independent vector validation and do not overwrite raster values. This route remains candidate until additional held-out real-raster cases and the binding WebPlotDigitizer comparison gates are complete.

The bar candidate also bridges one- to two-pixel value-axis gaps caused by
anti-aliasing or gridlines, prefers the uniquely baseline-connected rectangle
when a legend swatch shares a fill colour, and labels a bar whose baseline is
covered by an in-plot overlay as `occluded_by_overlay`. When a verified
separately coloured error/interval stroke cuts through a pale bar, the route may
use cross-axis-dilated error-colour evidence to reconnect topology across the
stroke. This does not add fill or change the outer measured endpoints; require
`verified_occluder_bridging.occluder_role` to remain
`topology_only_not_numeric_fill`.

For a percent stack, retain each visible segment span without normalization.
An expected-total shortfall is separator-consistent only when the measured
internal pixel/value gaps account for it and no gap exceeds the configured
stack-gap tolerance. Keep `values_normalized_or_completed: false`; a large gap,
top shortfall, missing segment, or unexplained total mismatch remains
`low_confidence`.

## Visible-label pie and donut extraction (assisted candidate)

For a pie/donut whose numeric values are explicitly printed and visibly mapped
to distinct sector colours, read [references/labelled-pie-donut-extraction.md](references/labelled-pie-donut-extraction.md) and run `scripts/candidate_digitize_labelled_donut.py`. Supply the original-raster contract, panel bounds, group centres, annular bands, named palette, label anchors, and two transcriptions of every declared visible label.

Authorize only matching transcriptions that pass independent annular-geometry
validation. Preserve the printed value and printed group sum even when they do
not equal 100. Geometry is validation-only and must never supply or normalize a
primary label. Unlabeled sectors, angle-only estimates, source observations,
exploded/3D pies, gradients, and overlapping sectors remain unsupported.

## Scatter overlays on pastel bars

Use this route for jitter/strip points drawn over pastel bars, especially when a bar outline has the same hue as its points.
Read [references/scatter-overlay-points.md](references/scatter-overlay-points.md) before extracting this chart family or changing its candidate implementation.

1. Crop each category at original resolution; make a nearest-neighbour enlarged crop for pixel review. Nearest-neighbour enlargement is evidence review, not new image information.
2. Sample the interior of a dark, saturated marker and the interior of the pastel bar separately: distinguish the darker marker core from the pastel bar fill. Do not use same-hue connected components alone: they merge points, fills, and outlines.
3. Detect compact, marker-shaped cores (for example, a small circular-template support score) and reject linear horizontal/vertical evidence that is consistent with a bar edge.
4. Calibrate the bar rectangle separately. Keep any point centre that shares its pixels with a bar edge as `bar_outline_overlap_candidate`; do not silently accept it or discard it.
5. Return two layers: `visible_marker_candidate` for a locally supported centre, and a candidate/ambiguity layer for bar-edge conflicts or merged marker clusters. Record the original-pixel support score, marker colour, crop, and overlay.
6. Do not emit an estimated raw-sample table for a merged cluster. A marker count, centre, or value is recoverable only when the original pixels support its unique separation; report `partial_visible` or `not_extracted` otherwise.

Treat a colour template, a local-shape test, and bar geometry as complementary evidence. Re-run the existing scatter benchmark plus a synthetic pastel-bar-with-overlay case before promoting any implementation change; this procedure alone is a candidate workflow, not a stable extractor.

## Quality gates

- Require two verified ticks per axis. For nonlinear axes, stop and use a calibrated transform; do not apply a linear mapping.
- For PDF vectors, require visual path-to-panel and marker-to-data verification, exclude legend marks, retain PDF-space centres, and make an overlay before accepting a coordinate-derived value.
- For source-data validation, require an explicit panel-to-metric/unit/statistic mapping. Do not match records merely by analyte name, worksheet row, or sorted position.
- Retain raw source values, source units, normalized values, every scale factor, and the evidence for that transform. If the units or metric are unresolved, return a non-comparable status rather than silently choosing a conversion.
- State paired count over total visible points, unmatched reasons, and per-panel errors. Aggregate direct-unit errors only when the compared response metrics share units; otherwise prefer normalized errors or panel-level summaries.
- Keep display labels and coordinate-derived values as separate fields when rounding or plotting transforms make them differ.
- Keep series colors distinct from gridlines, fills, and error bars. Sample a representative interior pixel, not an anti-aliased edge.
- Treat a value as missing when no color evidence is found. Never interpolate merely to make a CSV look complete.
- For scatter points over bars, expose the unresolved-candidate layer rather than converting edge conflicts or fused blobs into accepted points.
- For an aligned lattice, classify every Cartesian cell and refuse numeric output when any cell is ambiguous. Never tune geometry from supplied semantic labels, printed totals, or expected counts.
- Require standard `reason_code` values and a declared-slot `coverage_ledger` for bar and visible-label extractors. Use the lattice route's complete Cartesian-cell classification as its equivalent completeness evidence. Do not use an external expected data count to make either structure complete.
- For labelled pie/donut output, require matching duplicate transcriptions and validation-only sector geometry; never force displayed values to total 100.
- Reject any raster measurement whose input hash or dimensions differ from its original-pixel source contract.
- Treat error bars as separate geometry. Report their endpoints in both pixels and data units.
- Generate a recreation or overlay for visual review. Image similarity alone never proves numeric correctness.

Read [references/report-and-evolution.md](references/report-and-evolution.md) and [references/research-quality-baseline.md](references/research-quality-baseline.md) before adding a corrected case or changing extraction logic.

## Synthetic benchmark

Run `scripts/run_synthetic_benchmark.py --output-dir D:\Scratch\thu-digitizer-benchmark` before promoting an extraction change. It generates only local, deterministic charts and truth data for clean/low-resolution lines, scatter plots, grouped bars, and stacked bars. Compare the method report rather than choosing one universal technique:

- Trace a color-distinct line with local evidence, the legacy continuity method,
  and the shared `raster_core_continuity` candidate (soft colour evidence,
  path continuity, and explicit gaps).
- Recover separable coloured scatter points from connected-component centroids, and benchmark compact/touching filled markers plus the low-contrast residual-refusal case separately with `scripts/run_scatter_benchmark.py`.
- Recover grouped bars from component bounds.
- Recover stacked bars from each segment's run height, never from its top edge alone.

Read [references/benchmark-suite.md](references/benchmark-suite.md) before interpreting or expanding this suite.

The grouped/stacked-bar routes in this synthetic runner are benchmarks, not dedicated stable user-facing extractors. Do not claim automated bar support until a dedicated extractor meets the binding research-quality baseline.

## Gallery-inspired benchmark expansion

Use the R Graph Gallery as a public taxonomy and rendering-pattern reference, not as a source of truth data. Read [references/r-graph-gallery-benchmark.md](references/r-graph-gallery-benchmark.md) before adding its representative families. Generate fresh local data and renderings; retain only page URLs and family metadata unless the user separately approves keeping downloaded site assets or source code.

Begin with exact-value families (line/scatter, bars, histogram, area, heatmap, box plot). For density/violin, unlabeled pie/donut, general polar, treemap, maps, networks, Sankey, word clouds, and animation, state the recoverable representation explicitly; a raster cannot generally recover the original raw observations or hidden graph structure. Use the assisted labelled pie/donut route only for explicitly printed values with independent visible-sector validation.

## Controlled evolution

Keep the stable skill code unchanged during normal extraction. Record a candidate improvement only when a correction identifies a reproducible failure mode. Compare the candidate against the current implementation on all benchmark cases; promote it only after it improves the relevant metric without regressions and after user approval. Keep sensitive source images outside the skill by default.

## Limits of v0.1

The bundled executables support calibrated colour-distinct lines plus pale error bars, a continuity-aware raster line candidate, a candidate compact filled-scatter route with distance-peak splitting and a blocking residual audit, a candidate original-pixel aligned-lattice route, grouped/stacked bar candidates with verified-occluder topology bridging, an assisted visible-label pie/donut candidate, calibrated histograms, colour-distinct vertical or horizontal boxplots, and PDF vector inspection. The compact-scatter route is not a universal point detector: hollow markers, bubbles, dense swarms, perfect coincidences, and occluded marks remain unsupported or `not_extracted`. The pie/donut route does not discover OCR labels or infer unlabeled sectors. The lattice route does not cover irregular matrices, merged or occluded cells, or unverified semantic text. Direct PDF marker recovery and source-data validation are assisted workflows. Histogram output is limited to visible bin edges/heights and boxplot output to visible summaries/outliers. For bars, OCR-heavy images, nonlinear or unsupported coordinates, overlapping series, or unverified vector paths, retain the same evidence/refusal gates and do not claim stable automation without dedicated held-out evidence.
