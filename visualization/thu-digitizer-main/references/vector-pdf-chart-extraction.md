# Vector PDF chart route (candidate / assisted)

Use this route when a user supplies a PDF and needs a chart digitized, checked for vector content, or recreated. It improves fidelity when the visible plotted marks survive as PDF paths, but it is not a stable automatic extractor. Apply the research-quality baseline and return `partial_visible`, `low_confidence`, or `not_extracted` whenever panel assignment, transform, or mark identity is ambiguous.

## 1. Route before rasterizing

1. Preserve the original PDF and record its SHA-256.
2. Run `scripts/inspect_pdf_vectors.py` on the page containing the requested panel.
3. Treat `mixed_vector_and_raster` as normal: a figure can contain raster heatmaps/gradients while its axes, labels, points, lines, and legends remain vector paths.
4. Render a visual reference only after recording the page dimensions. Do not infer that a chart is raster merely because it includes embedded images.

Example:

```powershell
& python scripts/inspect_pdf_vectors.py `
  --input C:\paper.pdf --page 8 `
  --output-report C:\work\figure-5-vector-inspection.json
```

The inspector only routes work. It does not identify data marks or recover numerical values.

## 2. Direct vector recovery of visible scatter markers

Use direct path geometry only after visually verifying all of the following:

- The requested panel bounds in PDF points.
- A marker predicate: fill/stroke colour, path primitive, approximate marker size, and location inside the panel ROI.
- A separately excluded legend ROI. Legend dots can be geometrically identical to plotted points.
- At least two verified axis anchors per transform. For each panel, do not reuse a calibration from a neighboring panel unless their axes truly coincide.

For each accepted marker, record its PDF-space centre `(x_pt, y_pt)`, bounding box, matched drawing/path index if available, colour, panel identifier, and status `vector_marker_extracted`. Count the accepted markers and compare with the visible plot before converting coordinates. Produce an overlay that rings every accepted centre; visually check that no legend symbol is ringed and no visible data point is missed.

Use the actual vector coordinates for conversion, not just printed tick labels:

- Linear axis: fit `value = a * coordinate_pt + b` from two or more ticks and save residuals.
- Log axis: fit `log10(value) = a * coordinate_pt + b`, then convert with `value = 10 ** (...)`.
- Nonlinear, broken, categorical, or uncertain axes: stop and use a dedicated calibrated method rather than forcing either transform.

Printed concentration labels can be rounded; therefore a point's coordinate-derived x value can differ slightly from its display label. Keep both fields instead of silently replacing one with the other.

## 3. Curves, fit parameters, and recreation

A visible vector fit curve is a drawable object, not proof that the author-supplied parameters are embedded in the PDF. Keep these products distinct:

| Requested result | Permitted claim |
| --- | --- |
| Visible marker centres calibrated to axes | `vector_marker_extracted` for the plotted positions only |
| Curve traced from its vector path | `curve_path_traced`; not author parameters unless independently present |
| New 4PL / regression fit to extracted points | `refit_from_extracted_points`; state fitting method, bounds, R-squared, and point count |
| Recreated chart | State whether points, axes, and curves are direct or refitted; export an overlay/recreation for review |

Do not call a refitted curve the original author's curve. Do not claim raw observations, error bars, replicate counts, hidden smoothing settings, or fit parameters from marker centres alone.

For a compact dose-response recreation, retain the source's verified axis transform and plotting ranges, plot the directly recovered points, and label a new fit as `4PL refit`. Export a vector PDF plus a high-resolution PNG. If the user asks for an original-versus-recreated comparison, render the same panel crop from the source PDF next to the recreation and label which curves are refitted.

## 4. Evidence bundle and refusal rules

Save the input hash, page number, crop/ROI, vector-inspection report, calibration anchors and residuals, accepted/rejected path counts, CSV, JSON report, overlay, recreation, and explicit status. A vector route is stronger positional evidence than raster clicking, but it still recovers only what is visibly encoded in the PDF.

Return `partial_visible` when markers are exact but author raw data or fit parameters are absent. Return `low_confidence` or `not_extracted` when any marker-vs-legend separation, path-to-panel assignment, calibration anchor, or transform cannot be verified. Keep user PDFs out of the skill and benchmarks unless the user explicitly consents to retention.
