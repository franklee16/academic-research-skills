# SciFigureHub coverage and challenge protocol

## Scope

Use [SciFigureHub Gallery](https://uu543493-83c1-74a94416.nma1.seetacloud.com:8448/) as a taxonomy of real scientific-panel stressors and as a source of public panel/detail URLs. It is not numeric ground truth for THU Digitizer.

The catalogue snapshot inspected on 2026-07-20 contained 8,385 panels in 31 labelled subtypes, 8,328 review-passed reproductions, five subject groups, and a mean gallery quality score of 9.0/10. Computed image complexity ranged from 8.45 to 97.7 (median 45.07); 776 panels were above 70. These scores assess the gallery reproduction workflow. They do not measure digitization error.

Do not commit downloaded target images, article figures, or copied reproduction code to this repository. Retain metadata, URLs, hashes, and locally generated fixtures only unless the user separately approves retention and the applicable terms have been checked. Nature/Springer article panels may remain copyrighted even when their URLs are public.

## Why catalogue labels are not extraction truth

Visual inspection confirmed two routing hazards:

1. A high-complexity `bar` example is primarily a photograph with a small bar-chart inset. Panel segmentation and inset detection must precede bar extraction.
2. A `scatter` example contains three atomistic structure renderings with colour-encoded spheres, not Cartesian scatter axes. Catalogue subtype is a discovery hint, never permission to run an XY extractor.

Other inspected panels combine multiple coordinate systems or mark grammars: horizontal positive/negative bars with error intervals, 100%-stacked faceted bars, boxplots with raw points and significance brackets, annotated/missing-cell heatmaps, a dual-triangle matrix with two colour scales and size encoding, a projected 3D multi-line plot, and a spike raster above an analogue EMG trace.

## Recoverable-representation contract

| Gallery subtype | Count | Visibly recoverable representation | Explicitly not recoverable from the raster alone | Route |
| --- | ---: | --- | --- | --- |
| `bar` | 647 | Rectangle endpoint relative to a verified baseline; visible error interval separately | Hidden samples; SD/SEM/CI semantics | P0 candidate |
| `grouped_bar` | 798 | Category/series rectangles, signed values, visible intervals | Group identity without verified category/legend association | P0 candidate |
| `stacked_bar` | 234 | Segment boundaries and signed segment spans; visible total constraint | Occluded/zero segments; latent composition | P0 candidate |
| `histogram` | 190 | Bin edges and heights | Original observations | Stable, restricted styles |
| `box` | 637 | Five-number summary and visible outliers | Raw sample; hidden or fused points | Stable summary; overlay candidate |
| `line` | 235 | Visible sampled curve or visible markers | Hidden interpolation/model parameters | Stable, colour-distinct linear route |
| `multi_line` | 1,340 | One visible trace per verified series, including missing spans | Unresolvable crossings/occluded spans; 3D values without projection calibration | P0 complex-line candidate |
| `time_series` | 309 | Visible traces or event coordinates per verified track | Sampling rate and latent events without scale evidence | P0/P1 by grammar |
| `learning_curve` | 2 | Visible train/test traces and markers, including inset as a separate panel | Model state or unseen epochs | P0 complex-line candidate |
| `calibration_curve` | 1 | Visible predicted/observed curve coordinates and reference line | Calibration model internals | P0 complex-line candidate |
| `roc_curve` | 42 | Visible FPR/TPR curve samples; printed AUC only via verified text | Thresholds not drawn; underlying predictions | P0 complex-line candidate |
| `pr_curve` | 5 | Visible precision/recall curve samples | Thresholds and class observations | P0 complex-line candidate |
| `survival_curve` | 92 | Kaplan-Meier step geometry and visible censor marks | Patient-level times, risk sets not printed | P1 step-curve route |
| `dose_response` | 87 | Visible points, curve, and error intervals with log/linear calibration | Original replicates; source fit parameters unless printed and verified | P0 nonlinear-axis route |
| `scatter` | 727 | Visible point centres after XY verification | Occluded points; non-Cartesian atom positions mislabelled as scatter | Stable, colour-distinct limited route |
| `scatter_with_fit` | 487 | Visible points and a separately labelled visible fitted curve | Source regression parameters or residuals | P0 composite route |
| `dot_plot` | 363 | Visible point centres; size/colour only with verified legends | Fused points and hidden counts | P0 point route |
| `bubble_plot` | 60 | Point centres, visible marker area, and calibrated colour | Hidden points; numeric size/colour without readable legends | P0 point-plus-legend route |
| `umap_tsne_pca` | 252 | Visible embedding coordinates in plot units and visible clusters | Original high-dimensional distances/features | P1 embedding route |
| `volcano_plot` | 114 | Visible point centres, thresholds, and labels | Source p-values/fold changes for occluded points | P0 dense-point route |
| `density` | 108 | Rendered density curve or filled envelope | Raw observations and exact bandwidth | Restricted visible-envelope route |
| `violin` | 213 | Visible violin envelope plus independently visible summary marks | Raw observations or exact sample count | Restricted visible-envelope route |
| `heatmap` | 716 | Row/column grid, missing-cell mask, and colour-calibrated values | Values without a readable scale; hidden annotations | P1 grid route |
| `confusion_matrix` | 40 | Grid, class labels, printed values or colour-calibrated cells | Counts/proportions when neither text nor scale is available | P1 grid/OCR route |
| `matrix_plot` | 15 | Cell position, visible glyph size/colour, symbols, and triangle identity | Exact correlations without calibrated legends | P1 multi-encoding grid route |
| `forest_plot` | 46 | Point estimates and visible interval endpoints by row | Study weights/model semantics not visibly encoded | P1 interval route |
| `geospatial_map` | 242 | Visible georeferenced cells/points after projection or control-point calibration | Source rasters, vector topology, values without colour scale | P2 geospatial route |
| `network_plot` | 22 | Visible node centres, drawn edges, labels, and visible attributes | Hidden edges, direction, weights, or layout-generating graph | P2 graph route |
| `sankey_alluvial` | 10 | Visible nodes, ribbon boundaries, and relative widths | Hidden flow table or exact values without calibration | P2 flow route |
| `table_like` | 55 | Visible cell text/glyphs and categorical tracks | Underlying database/schema not printed | P2 OCR/table route |
| `other_data_display` | 296 | Only a grammar declared after panel-specific classification | Any structure inferred from the fallback label | Unknown/refuse by default |

## Required architecture

Treat complex-panel digitization as four separately auditable layers:

1. **Panel parser:** split figures, facets, insets, photos, legends, colour bars, annotations, and plot regions. A subtype label never bypasses this stage.
2. **Coordinate model:** select Cartesian linear/log/date, categorical, polar, ternary, projected 3D, geospatial, matrix/grid, graph, flow, or event-raster coordinates. Refuse an unsupported transform.
3. **Mark grammar:** dispatch rectangles, curve traces, points/bubbles, intervals, boxes, cells/glyphs, envelopes, nodes/edges, ribbons, text, or events to dedicated extractors.
4. **Evidence and semantics:** associate axes, categories, series, legends, and units; preserve masks/components, calibration residuals, CSV/JSON, overlay, confidence, and refusal reasons.

This separation is the main path beyond WebPlotDigitizer: broader automation must still end in locally verified geometry, not an opaque image-to-table guess.

## Benchmark use

- `target.png` and target PDFs are **challenge-only** unless independent numeric truth is available. Use them to test routing, panel splitting, refusal, and visual overlays.
- A gallery `reproduce_panel.py` may document an attempted reconstruction, but its values are not automatically the source article's truth. It can seed a separate locally rendered fixture only after provenance is recorded.
- Split held-out cases by DOI, renderer/template, and source document. Do not tune on another panel from the same figure and call it held out.
- Maintain deterministic local truth for every promoted extractor. Add real vector truth and consented/official source-data truth before promotion.
- Record WebPlotDigitizer as `not_compared` until the same inputs, calibration, intervention count, tolerance, and output representation have actually been compared.

## Initial inspected challenge cases

The machine-readable records live in `scifigurehub-manifest.json`. The first eight cases target failure modes rather than easy exemplars:

- Horizontal grouped bars with negative values, error bars, multiple stages, an inset, and dense labels.
- Faceted 100%-stacked bars with a long hierarchical legend.
- Grouped boxplots with visible points, significance brackets, sample counts, and a clipped neighbouring panel.
- Block-structured heatmap with missing cells, nested headers, text/symbol overlays, and multiple legends.
- 34×34 dual-triangle matrix with two colour scales, size encoding, and significance stars.
- Projected 3D multi-line plot with backdrop planes and endpoint annotations.
- Spike-event raster plus a continuous EMG trace and shaded time windows.
- A catalogue false-positive `scatter` example consisting of atomistic sphere renderings.

## Delivery phases

1. **Assisted parity:** manual/verified ROI, linear/log/date/category calibration, colour/series selection, line/scatter, simple/grouped/stacked/percent/negative bars, histograms, boxes, and evidence bundles.
2. **Complex statistical panels:** facets/insets, crossings and occlusion, overlaid points, forest/survival/dose-response, heatmaps/matrices, legends and OCR association.
3. **Non-Cartesian science graphics:** polar/ternary, projected 3D, geospatial maps, networks, Sankey/alluvial, and event rasters, each with a coordinate-specific contract and benchmark.

Promotion remains governed by `research-quality-baseline.md`: the current bar work is a candidate until real-vector/real-raster strata, fair WebPlotDigitizer comparison, no-regression evidence, and user approval are complete.
