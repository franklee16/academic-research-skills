---
name: copyplot
description: Analyze a supplied scientific-figure image (PNG, JPEG, TIFF, or a rasterized figure), identify its chart type and visual grammar, infer axes and styling, and deliver a close Python/Matplotlib or Seaborn reproduction with synthetic or digitized example data stored in an Excel workbook whenever practical. Use for requests to imitate, reverse-engineer, redraw, reproduce, or learn from a paper figure such as line, scatter, bar, histogram, box, violin, heatmap, contour, error-bar, multi-panel, or mixed scientific plots.
---

# CopyPlot

Reconstruct a scientific figure as an editable, reproducible plotting project. Treat visual fidelity and scientific honesty as separate requirements: match the appearance closely, but never present inferred data as the source paper's original observations.

## Required inputs and defaults

- Require one readable source image. If it is not available locally, ask the user to attach it.
- Accept optional constraints such as preferred library, target journal size, font, DPI, or output folder.
- Default to Python with Matplotlib; add Seaborn only when it materially simplifies the plot. Use other plotting libraries only when the source clearly requires them.
- Default outputs to a new folder beside the input or in the current workspace. Never overwrite the source image.
- Use an `.xlsx` workbook for example data unless the dataset is too large or irregular; explain any fallback to CSV/NPZ.

## Workflow

### 1. Inspect the source

View the image at full resolution. If local, run:

```powershell
python scripts/analyze_image.py --input <image> --output <analysis.json>
```

Use the report as supporting evidence, not as a substitute for visual inspection. Read [references/figure-reconstruction-guide.md](references/figure-reconstruction-guide.md) when the chart is ambiguous, multi-panel, log-scaled, color-mapped, or requires data digitization.

Record:

- figure and panel dimensions, aspect ratios, margins, and panel labels;
- primary and secondary plot types, mark types, and likely plotting library;
- x/y limits, scale type, tick locations, tick-label format, axis labels, and units;
- background, spines, grid, colors, colormap, alpha, line styles, marker shapes, marker sizes, and approximate stroke widths;
- legend position, frame, order, columns, handle style, and typography;
- annotations, reference lines, error bars/bands, insets, and colorbars;
- confidence for every uncertain observation.

Do not invent unreadable text. Mark it as uncertain and use a visible placeholder in the first draft.

### 2. Classify the visual grammar

Name the figure at two levels:

1. **Family:** line, scatter, bar, distribution, matrix/heatmap, contour/surface, network, geographic, image/microscopy, or composite.
2. **Construction:** number of panels, layers, series, encodings, shared axes, transforms, and statistical summaries.

For mixed figures, describe every layer—for example, `scatter + fitted line + 95% confidence band`, not merely `scatter plot`.

### 3. Recover or synthesize data

Choose and disclose one mode:

- **Digitized approximation:** Calibrate pixels to axis coordinates and sample visible marks. Use only when the resolution and axes make recovery defensible.
- **Synthetic look-alike:** Generate data that reproduces the visible geometry, ranges, density, ordering, and summary statistics. This is the default when exact recovery is impossible.
- **User data:** Preserve supplied values and only reconstruct styling.

Store plotted values—not just summary parameters—in Excel. Put each logical table on its own sheet; keep error bounds, groups, facets, and annotations in explicit columns. Add a `README` sheet stating the source image, mode, assumptions, units, random seed, and which values are inferred.

To build a workbook from a compact JSON description, use:

```powershell
python scripts/make_example_workbook.py --spec <workbook-spec.json> --output <example_data.xlsx>
```

See [references/workbook-spec.md](references/workbook-spec.md) for the schema. Use a fixed random seed and write derived synthetic values to the workbook so the plot is deterministic.

### 4. Write the reproduction script

Create a self-contained `recreate_plot.py` that:

- resolves `example_data.xlsx` relative to `Path(__file__)`, not the current working directory;
- reads all plotted values from the workbook with `pandas.read_excel` or `openpyxl`;
- centralizes visual constants in a `STYLE` mapping and documents only non-obvious choices;
- sets the physical figure size in inches and saves at explicit DPI;
- uses explicit axis limits, ticks, formatters, z-order, clipping, and legend handles;
- embeds a known font only if licensed and supplied; otherwise chooses a close installed fallback;
- exports both a high-resolution PNG and a vector PDF or SVG when the plot primitives are vector-friendly;
- contains a `main()` function and runs successfully from any working directory.

Prefer public Matplotlib APIs. Avoid hard-coded pixel coordinates except for intentional figure-space annotations. For multi-panel figures, use `GridSpec` and explicit width/height ratios.

### 5. Render and compare

Run the script and inspect the rendered PNG. Then calculate coarse similarity diagnostics:

```powershell
python scripts/compare_images.py --reference <source-image> --candidate <rendered.png> --output-dir <qa-dir>
```

Inspect both the render and `difference.png`. Iterate on the largest mismatch first:

1. canvas and axes geometry;
2. axis limits, scales, and tick positions;
3. data geometry;
4. colors, widths, markers, and alpha;
5. text, legend, and annotations.

Treat similarity metrics as diagnostics only. A high pixel score can still hide incorrect axes or labels.

### 6. Validate the package

Before delivery:

- run `recreate_plot.py` in a clean output folder;
- verify the workbook opens and contains the exact values plotted;
- verify PNG plus PDF/SVG outputs exist and are non-empty;
- visually compare the final render with the source at the same aspect ratio;
- confirm the code contains no absolute machine-specific paths;
- state all approximations and unresolved ambiguities.

## Deliverables

Return a folder containing at minimum:

```text
recreated-figure/
|-- recreate_plot.py
|-- example_data.xlsx
|-- recreated_plot.png
|-- recreated_plot.pdf   # or .svg
|-- analysis.json
`-- qa/
    |-- comparison.json
    `-- difference.png
```

In the final response, identify the chart type, summarize the most important inferred style details, link every deliverable, give the exact run command, and distinguish recovered, supplied, and synthetic data.

## Boundaries

- A raster figure does not contain its original numerical dataset, font metadata, or plotting commands. Describe inferred values as approximations.
- Do not remove watermarks, ownership marks, or attribution from the source.
- Reproduce general scientific styling and geometry; warn before closely copying distinctive copyrighted illustrations, icons, or graphical abstracts.
- For microscopy, maps, molecular structures, Sankey diagrams, and network layouts, recreate the surrounding scientific chart when possible, but do not fabricate underlying scientific measurements or topology.
