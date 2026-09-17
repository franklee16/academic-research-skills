# Compact marker-line candidate route

## Scope and non-scope

`scripts/candidate_digitize_marker_line.py` recovers the visible centres of
compact filled markers at verified sample positions on a calibrated linear
Cartesian panel. It supports multiple rasterized core colours for one semantic
series and same-colour reference lines. It does not recover unmarked curve
positions, hidden samples, raw observations, fit parameters, hollow markers,
or non-compact marker grammars.

This route is a candidate. The stable `raster_line_color` implementation and
`SKILL.md` are unchanged until benchmark evidence is reviewed and promotion is
explicitly approved.

## Failure addressed

The stable sample-mode route chooses one row cluster greedily. A same-colour
dashed reference line can therefore become the next selected cluster and keep
the trace latched to the reference line. Background alpha compositing can also
give one semantic marker series different exact core colours inside and outside
a shaded region. Finally, sample-mode values were mapped with a two-anchor
affine even after a multi-anchor `AxisCalibration` had been fitted.

The candidate instead:

1. Records every visible row candidate and its two-dimensional morphology.
2. Penalizes thin/low-fill line-like evidence and selects a second-order global
   path across all verified sample positions.
3. Accepts several verified colour templates per semantic series.
4. Uses the fitted `AxisCalibration` object for both pixel placement and value
   recovery.
5. Leaves review-required and missing values blank in the primary CSV.

## Executable FigureSpec binding

`scripts/run_marker_line_spec.py` validates the source SHA-256 and dimensions,
route ID, compact-marker grammar, verified x/y axes, sample positions, colour
templates, reference lines, and extraction parameters before calling the
candidate. A deterministic run identity includes the FigureSpec, runner,
extractor, and source hashes. A repeated identical run is refused rather than
overwriting evidence.

The candidate route ID is `raster_marker_line_candidate`. Required confirmation
names are recorded in `scripts/extractor_registry.py`.

## Evidence bundle

Every panel run contains:

- `configuration.json`: canonical bound parameters and calibration reports;
- `data.csv`: authorized numeric values only;
- `evidence.csv`: per-sample morphology, candidate value, confidence,
  uncertainty, status, and refusal reason;
- `overlay.png`: all row candidates and the selected marker centres;
- `report.json`: implementation/input hashes, run ID, complete candidate sets,
  summaries, and limitations.

Evidence directories are immutable. Failed or exploratory runs remain useful
negative evidence and must not be overwritten.

## Deterministic benchmark

Run:

```powershell
python scripts/run_marker_line_benchmark.py --output-root outputs/marker-line-evolution
```

The suite contains clean markers, same-colour reference-line conflicts,
background-dependent marker templates, and a line-only refusal panel. Synthetic
truth is used only after image extraction. The report also runs the stable
greedy selector with the same plot bounds, calibration, colour masks, sample
positions, and radius.

Current candidate gates require full coverage, MAE no greater than `0.05`, and
maximum error no greater than `0.11` data units for supported cases. The
line-only case must authorize no numeric output. WebPlotDigitizer is recorded as
`not_compared` when no matched assisted session is available.

## Recreation renderer

`scripts/recreate_line_figure.py` consumes extracted CSV data and a declarative
style spec. It writes an exact-size PNG, 3x PNG, vector SVG, PDF, and immutable
manifest. The source raster is not embedded. Supported elements include
multi-panel axes, shaded spans, reference lines, marker/line series, legends,
figure text, scatter decorations, and vertical decoration lines.

## Open promotion gates

- independent held-out real-raster cases;
- real-vector comparison where an original vector figure is available;
- fair matched WebPlotDigitizer comparison or a maintained `not_compared`
  reason;
- explicit user approval before changing the stable implementation or
  `SKILL.md`.
