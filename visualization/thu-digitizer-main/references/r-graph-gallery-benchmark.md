# R Graph Gallery-inspired benchmark

## Purpose and boundary

Use [The R Graph Gallery](https://r-graph-gallery.com/) as a coverage taxonomy and a source of public rendering patterns. Do not treat a gallery image as truth data. Generate all benchmark truth values locally with deterministic seeds, then render local variants with equivalent chart grammar.

Keep only the page URL, chart-family metadata, local generator version, seed, truth CSV/JSON, extraction result, metrics, and an overlay. Do not archive page images, scraped datasets, or copied source code unless the user separately approves the retention and terms have been checked.

## Initial representative set

| Priority | Family | Reference page | Truth to retain | Expected result |
| --- | --- | --- | --- | --- |
| P0 | Multi-series line and error bars | https://r-graph-gallery.com/line-chart-several-groups-ggplot2.html | x, y, error endpoints | Exact sampled coordinates and separately measured error endpoints |
| P0 | Scatter and bubble | https://r-graph-gallery.com/scatter-plot.html | x, y, marker area | Point centres; marker area only when visually separable |
| P0 | Grouped, stacked, and percent-stacked bars | https://r-graph-gallery.com/48-grouped-barplot-with-ggplot2 | category values and stack segments | Exact category values; percent stacks sum to 100 within tolerance |
| P0 | Histogram | https://r-graph-gallery.com/histogram.html | bin edges and counts/density | Bin edges and bar heights; not raw observations |
| P0 | Area and stacked area | https://r-graph-gallery.com/area-chart.html | x, series values, stack totals | Boundary traces and/or stack components |
| P0 | Heatmap | https://r-graph-gallery.com/heatmap.html | row/column grid and values | Cell grid and calibrated colour values where a readable colour bar exists |
| P0 | Box plot | https://r-graph-gallery.com/boxplot.html | quartiles, whiskers, outliers | Five-number summary and visible outliers; not latent samples |
| P1 | Density and violin | https://r-graph-gallery.com/density-plot.html | sampled curve or envelope | Rendered curve/envelope only; never claim recovery of raw samples |
| P1 | Pie and donut | https://r-graph-gallery.com/pie-plot.html | sector proportions | Sector angles/proportions and labels, if readable |
| P1 | Radar / polar bar | https://r-graph-gallery.com/spider-or-radar-chart.html | spokes and radii | Per-spoke values after radial calibration |
| P1 | Treemap | https://r-graph-gallery.com/treemap.html | leaf rectangles and weights | Visible leaf areas/labels; hierarchy only when encoded visibly |
| P2 | Maps, flows, networks, circle packing | https://r-graph-gallery.com/all-graphs | visible marks and labels | Structure or annotated geometry; never assume hidden topology/data |
| P2 | Word clouds and animation | https://r-graph-gallery.com/wordcloud.html | rendered words or frames | OCR/layout or per-frame marks; not source frequency without calibration |

## Local fixture matrix

For every family, generate at least these rendering variants from the same truth data:

1. Clean vector-like PNG with linear axes.
2. Small raster and JPEG compression.
3. Light/dark background, gridlines, legend inside/outside, and varied palettes.
4. Sparse and dense marks, overlapping series, rotated labels, and faceting where the family supports it.
5. A deliberately ambiguous case which must return `low_confidence` or `unsupported` rather than invented values.

Vary one factor at a time. Record the renderer/library version, image dimensions, font availability, random seed, and SHA-256 for every raster.

## Metrics and gates

- Coordinates/heights: MAE, median absolute error, 95th-percentile absolute error, and maximum error in native data units.
- Error bars: top/bottom endpoint error in pixels before axis mapping.
- Discrete objects: detection precision, recall, F1, category alignment, and component-to-truth matching rate.
- Proportions: absolute percentage-point error and stack-total constraint error.
- Curves/envelopes: x-aligned curve MAE and coverage; do not compare pointwise against unavailable raw samples.
- Calibration: axis-anchor residual in pixels and mapping residual in data units.

Set an explicit threshold per case. Promote a candidate extractor only when it improves its target family and does not regress any existing gated case. Keep unpromoted candidates outside stable scripts until the user approves promotion.

## Routing contract

Classify first, then dispatch to a dedicated extractor. Return `unsupported` or `low_confidence` for a family that lacks a validated route. The classifier is not permitted to route a pie, map, Sankey, violin, or heatmap through the line extractor merely because it finds a coloured contour.
