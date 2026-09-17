# Figure reconstruction guide

## Contents

1. Visual inventory
2. Plot taxonomy
3. Axis calibration
4. Style estimation
5. Data synthesis
6. Matplotlib implementation patterns
7. Quality assurance

## 1. Visual inventory

Start from the outside and move inward:

1. Canvas: pixel size, aspect ratio, white/colored/transparent background.
2. Layout: panel count, gutters, shared axes, inset axes, colorbars.
3. Axes: bounding boxes, spines, limits, scale, ticks, labels, units.
4. Marks: line, point, rectangle, polygon, raster cell, error bar, band.
5. Guides: grid, zero line, thresholds, fit lines, reference regions.
6. Text: title, panel tags, annotations, legend, statistical labels.
7. Rendering: antialiasing, transparency, raster/vector character.

Record observations with `high`, `medium`, or `low` confidence. Estimate dimensions in both image pixels and final physical units.

## 2. Plot taxonomy

| Visible evidence | Classify as | Typical implementation |
|---|---|---|
| Connected values with ordered x | line/time series | `Axes.plot`, `fill_between` |
| Unconnected markers | scatter | `Axes.scatter` |
| Marker plus whiskers | error-bar plot | `Axes.errorbar` |
| Rectangles from a baseline | bar/grouped/stacked bar | `Axes.bar`, `barh` |
| Adjacent bins | histogram | `Axes.hist` or precomputed bars |
| Median box, whiskers, fliers | boxplot | `Axes.boxplot` |
| Mirrored density | violin | `Axes.violinplot` or Seaborn |
| Colored matrix cells | heatmap | `imshow` or `pcolormesh` |
| Smooth filled isolines | filled contour | `contourf` |
| Levels without fill | contour | `contour` |
| Points plus fitted curve/band | regression composite | `scatter`, `plot`, `fill_between` |
| Multiple axes blocks | faceted/multi-panel | `GridSpec`, `subplots` |

Use a composite label when more than one row applies. Distinguish a heatmap from an image by looking for a colorbar, cell boundaries, regular axes, and discrete values.

## 3. Axis calibration

For a linear horizontal axis with plot pixels `p_left` and `p_right` and values `x_min`, `x_max`:

```text
x = x_min + (p_x - p_left) / (p_right - p_left) * (x_max - x_min)
```

For an image y coordinate measured downward:

```text
y = y_min + (p_bottom - p_y) / (p_bottom - p_top) * (y_max - y_min)
```

For log base 10, interpolate `log10(value)` rather than value. Infer a log scale from equal visual spacing of powers such as 0.1, 1, 10, 100 or from scientific tick formatting. Do not assume the visible curve is linear in data space.

Use at least two labeled ticks per axis; use three or more to detect nonlinear or broken axes. Flag axis breaks and categorical axes explicitly. Never digitize from a perspective-skewed photo without first rectifying it.

For scatter points, estimate marker centers rather than edges. For thick lines, sample the centerline. For error bars, store center, lower, and upper values in separate workbook columns.

## 4. Style estimation

### Geometry

Convert image proportions into figure settings:

- `figsize = (width_px / dpi, height_px / dpi)` for a chosen DPI.
- Estimate axes fractions from pixel bounding boxes and use `subplots_adjust` or `GridSpec`.
- Match whitespace before tuning data marks.

### Colors

Sample from the interior of marks, away from antialiased edges. Convert samples to hex and account for alpha compositing:

```text
observed = alpha * foreground + (1 - alpha) * background
```

When exact alpha is unknown, prefer the observed RGB with full opacity unless overlaps reveal transparency. For continuous maps, identify direction, endpoints, midpoint, and normalization (`linear`, `log`, `TwoSlopeNorm`, or bounded categories).

### Stroke and markers

At export DPI `d`, a raster width of `w_px` approximately corresponds to:

```text
linewidth_points = 72 * w_px / d
```

Antialiasing broadens edges, so start slightly below the raw estimate. Marker size in Matplotlib scatter is area in points squared; marker size in `plot` is diameter in points.

### Typography

Estimate hierarchy before exact font identity: font family class, weight, size ratios, math styling, capitalization, and alignment. Common scientific choices include Arial/Helvetica-like sans, Times-like serif, and Matplotlib DejaVu. Use a fallback rather than silently downloading a font.

### Legends

Match item order, number of columns, handle length, label spacing, border padding, frame visibility, face color, and anchor. Create proxy handles when the plotted artist produces the wrong legend symbol.

## 5. Data synthesis

Match visible structure without claiming recovery:

- Lines: anchor important extrema/crossings, interpolate, then add seeded noise at the visible frequency.
- Scatter: match marginal ranges, density, correlation, clusters, and outliers.
- Bars: match category order, baseline, magnitude ratios, groups, stacks, and visible errors.
- Histograms/densities: match modality, skew, tails, bin edges, and sample size only when stated.
- Heatmaps: match matrix shape, clusters/gradients, missing cells, normalization, and annotation precision.
- Box/violin: synthesize raw samples that yield similar quartiles/density; store both raw values and displayed summaries if the plot uses custom statistics.

Use NumPy's `default_rng(seed)` and record the seed. Once generated, write the realized values to Excel and have plotting code read them; do not regenerate on every run.

## 6. Matplotlib implementation patterns

- Apply `rc_context` so project styling does not leak into the user's global configuration.
- Set spine visibility and widths explicitly.
- Use `FixedLocator`/`FixedFormatter` when ticks must match exactly.
- Set `rasterized=True` only for dense artists inside vector output.
- Use `bbox_inches=None` when exact canvas size matters; tight cropping can change margins.
- Prefer `constrained_layout=False` plus explicit geometry for close reconstruction.
- For heatmaps, state `origin`, `extent`, `aspect`, interpolation, and normalization explicitly.
- For multi-panel figures, share axes only when the source does; hidden tick labels are not proof of shared limits.

## 7. Quality assurance

Review in this order:

1. Overlay or difference at identical pixel dimensions.
2. Compare panel and axes bounding boxes.
3. Check every printed tick, label, and legend entry semantically.
4. Check data landmarks: extrema, crossings, cluster centers, bar heights.
5. Check color samples and colormap endpoints.
6. Check thin details at 200–400% zoom.
7. Open the PDF/SVG to confirm vector output and font rendering.

Pixel comparisons are sensitive to fonts and antialiasing. Use them to localize differences, not to certify scientific equivalence.
