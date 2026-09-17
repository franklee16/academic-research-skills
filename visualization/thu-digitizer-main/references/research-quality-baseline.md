# Research quality baseline for chart digitization

## Status and use

Use this as the binding minimum standard before designing, benchmarking, or promoting a new THU Digitizer capability. It records what is recoverable from a rendered chart, how to compare an improvement fairly, and which evidence is required before claiming accuracy.

Do not interpret a chart image as its hidden source data. Return only visually supported quantities. For example, a boxplot supports visible summary statistics and visible fliers, not its raw sample; a violin or dense swarm may support a contour or separable visible points, not a complete observation table.

Read this file together with [report-and-evolution.md](report-and-evolution.md) and [benchmark-suite.md](benchmark-suite.md). A new candidate that fails any applicable gate below must remain experimental or return `low_confidence`/`not_extracted`.

## Research sources

| Source | Durable lesson for this skill |
|---|---|
| [WebPlotDigitizer documentation](https://automeris.io/docs/digitize/) | Reliable raster digitization is an assisted workflow: select an axis type, calibrate it, constrain a region of interest, identify colour, run a type-specific extractor, and manually correct when needed. It supports linear, log, and date axes and recommends widely separated calibration anchors. |
| [PlotExtract](https://arxiv.org/html/2503.12326v1) | Pair numerical matching with precision/recall and a complementary interpolated-curve comparison. Allow refusal and compare a replot with the source, but do not treat image resemblance as sole numeric proof. |
| [Yang, He, and Zhang (2025)](https://www.sciencedirect.com/science/article/pii/S1524070325000062) | Complex line charts require separate treatment of chart elements, text, and intersecting curves. Its headline extraction percentage is not a portable target because its public abstract does not define an error tolerance or split sufficient for a fair cross-tool comparison. |
| [ChartDetective](https://damienmasson.com/pdfs/chartdetective.pdf) | Prefer an original vector representation when PDF/SVG marks and transforms exist. Its reported vector-chart comparison is promising, but it is a context-specific study rather than proof of universal superiority over raster tools. |
| [ICDAR chart competition tasks](https://chartinfo.github.io/tasks.html) and [series metric](https://chartinfo.github.io/metrics/metric.pdf) | Evaluate chart classification, text, axis analysis, legend association, and raw-data recovery as separate layers as well as end-to-end. Use data-type-specific metrics for continuous curves, point sets, discrete values, and boxplots. |
| [ExChart](https://exchart.github.io/) | Use AI as a staged assistant: understand coordinates, interpret marks, then recover values; retain human verification because a model can recover table structure while still missing precise numbers. |

## Scope statement

The stable skill currently provides dedicated extractors for calibrated colour-distinct lines, histograms, and vertical/horizontal boxplots. Compact filled raster scatter points have a deterministic candidate with synthetic evidence, a blocking low-contrast residual audit, and retained real-case regression evidence, but it is not promoted as a universal or stable point detector. Repeated aligned lattice composites have a source-locked deterministic candidate with synthetic and retained UpSet regression evidence; irregular matrices and ambiguous cells remain outside that route. Grouped and stacked bars also remain candidate/benchmark routes. Visible-label pie/donut extraction is an assisted candidate limited to duplicate label transcription plus independent annular-geometry validation; it does not infer unlabeled sectors. Do not describe a benchmark or candidate route as supported universal automation.

## Priority order

Prioritize a family only when its data representation, confidence model, and benchmark can be stated precisely.

| Priority | Families and required distinction |
|---|---|
| P0 | Vertical/horizontal simple, grouped, stacked, 100% stacked, and negative bar charts; error bars; multi-line/step/marker charts including crossings; scatter, bubble, and colour-distinct jitter/strip points; boxplots with visible overlay points. |
| P1 | Area and stacked-area charts, interval/forest plots, waterfall charts, heatmaps with calibrated colour bars, pie/donut, and radar. |
| P2 | Polar, ternary, map, contour, network, Sankey, treemap, and animation. Add a coordinate-specific parser and benchmark; never force them through XY calibration. |
| Restricted | Violin, density, dense swarm, and overplotted marks. Extract only an explicitly defined visible representation; do not claim hidden observations or an exact sample count. |

Implement the next missing P0 dedicated extractor before expanding into P1/P2: grouped/stacked bars first, then complex line handling and visible point overlays for boxplots.

## How to exceed WebPlotDigitizer responsibly

Do not claim to exceed WebPlotDigitizer from a single image, an easier synthetic fixture, or a different error definition. For every P0 capability, compare at least:

1. Current stable THU Digitizer.
2. Candidate THU Digitizer.
3. WebPlotDigitizer assisted mode and, when applicable, its configured automatic mode.

Use identical input files, calibration assumptions, ground truth, evaluation tolerance, and declared human intervention. Record elapsed time, number of user confirmations/corrections, refusal rate, and all numeric metrics. If a WebPlotDigitizer comparison is unavailable, state `not_compared` rather than implying superiority.

Pursue superiority through these verifiable properties:

- Parse PDF/SVG vector marks, transforms, text, and layers before rasterizing. Fall back to raster geometry only when vector structure is absent or unusable.
- Separate chart type, panel/ROI, axis transform, OCR/tick association, legend/series association, mark segmentation, coordinate recovery, and validation. Do not use one opaque image-to-CSV step as the sole evidence.
- Let a vision model propose type, ROI, OCR, colours, and extraction route. Under [adaptive-execution.md](adaptive-execution.md), a local strong-model profile may also emit candidate pixel geometry and calibrated values when a deterministic route is incompatible or contradicted by its overlay. Accept those values only after original-pixel, geometric, calibration, ambiguity, and overlay checks, and label them `model_assisted_candidate`. Remote model use needs explicit user approval.
- Generate an evidence bundle: input hash, dimensions, crop/ROI, calibration anchors and transform, matching records, CSV, JSON, overlay, recreation, confidence, and rejection reasons. For deterministic runs, also retain masks/components, software version, and run identifier; for model-assisted runs, retain the runtime model name/profile, strategy reason, and per-mark evidence/status.
- Prefer selective automation: request confirmation or refuse when transform type, tick association, series identity, or visible mark geometry is ambiguous.

## Required benchmark protocol

### Test strata

Maintain all three strata for every promoted family:

1. **Deterministic synthetic truth:** known values and controlled style factors.
2. **Real vector truth:** figures rendered from retained source data or extractable PDF/SVG objects.
3. **Real raster truth:** held-out published or consented figures with source data where possible; otherwise independently double-annotated ground truth and disagreement records.

Split train, tuning, and final test by renderer/template/source document, not merely by image. Do not tune on the final test set. Use clean, low-resolution, JPEG, dark/light, colour-shifted, anti-aliased, legend-overlap, occlusion, crossing, and unsupported-transform conditions where applicable.

Report macro averages by chart family and condition, plus the complete per-case results. Never average raw MAE across families with different data ranges.

### Numeric and structural metrics

| Layer | Minimum metrics |
|---|---|
| Chart classification | Per-class precision, recall, F1, macro-F1, and unknown-chart false-positive rate. |
| Text, tick, and legend | Text-box IoU, normalized character error rate, tick detection/association F1, parsed-value accuracy, legend-to-series macro-F1. |
| Calibration | Anchor pixel error, transform selection accuracy, tick-fit residual, and data-space normalized error from calibration alone. |
| Discrete marks | One-to-one optimal matching; precision, recall, F1, x/y normalized MAE, P95 absolute error, and maximum absolute error. |
| Continuous curves | Pointwise normalized MAE/RMSE/P95 plus interpolation/integral error, endpoint error, and missing-span rate. |
| Bars and histograms | Category/series matching F1, top/edge/segment-boundary normalized errors, bin-edge error, height error, unmatched/missing mark counts. |
| Boxplots | Separate Q1, median, Q3, lower-whisker, upper-whisker MAE/P95/max; visible-flier F1; no raw-sample metric. |
| Confidence and refusal | Risk-coverage curve, error among high-confidence outputs, expected calibration error or Brier score when probabilities exist, correct-refusal rate, and unsafe false-accept rate. |
| Reproducibility and usability | Re-run output equality or hash stability, complete evidence-bundle rate, elapsed time, and human confirmations/corrections. |

Normalize coordinate errors by the relevant x/y axis range and state the tolerance used for a match. Include 95% bootstrap confidence intervals for family-level comparisons and paired confidence intervals or paired tests for stable-versus-candidate/WPD comparisons.

## Promotion gates

Before any stable promotion, all applicable requirements must hold:

1. Define the recoverable representation and explicit non-recoverable quantities before code is written.
2. Add a deterministic failing test, then the minimum implementation, then a regression test for every discovered error mode.
3. Preserve evidence before quality assertions; never overwrite a non-empty evidence directory.
4. Pass all existing stable tests and all new family tests.
5. Meet declared numeric, structural, confidence, robustness, and reproducibility gates on held-out cases; report failures rather than omitting them.
6. Demonstrate no regression against stable on every existing family and condition.
7. For P0 work, run the fair WebPlotDigitizer comparison or record why it is `not_compared`.
8. Present raw evidence, caveats, and exact supported scope to the user; obtain explicit promotion approval.

## Claim discipline

Use `validated_local_stable` only for a family that has a dedicated stable extractor, tests, fresh evidence, and an approved manifest entry. Use `candidate`, `benchmark_only`, `partial_visible`, or `low_confidence` for everything else. Never describe an internal benchmark, visual similarity, model narration, or a single corrected image as a production capability.
