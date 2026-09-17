# Compact filled scatter extraction

Use this low-freedom route only for Cartesian raster panels whose data marks are compact filled points of approximately one visible size. It recovers separable points and partially touching points with distinct distance-transform peaks. It does not recover hollow markers, size-encoded bubbles, dense swarms, perfect coincidences, fully occluded points, or hidden source rows.

## Mandatory procedure

1. Work from the original raster. Do not measure a chat preview, thumbnail, screenshot of an overlay, or rescaled copy.
2. Run `scripts/thu_digitizer.py inspect --chart-type scatter` and verify that the panel is Cartesian.
3. Verify the plot rectangle and at least two widely separated tick anchors on each axis. Use original-image pixel coordinates with `(0, 0)` at the upper-left.
4. Choose exactly one marker mode: `dark` for dark filled points on a lighter field, `light` for light filled points on a darker field, or `color` plus `--marker-color` for a distinct fill colour.
5. Run `scripts/candidate_digitize_scatter.py` once per panel. Do not write a replacement detector and do not pass an expected point count.
6. If Pearson's `R` is visibly printed, pass `--annotated-pearson-r`. The script must use it only after extraction as a validation gate.
7. Require `residual_audit.status: clear`. The relaxed negative-space pass may block authorization but must never add a point. Resolve a residual only by correcting visibly wrong configuration or adding a verified non-data exclusion, then rerun the primary detector.
8. Open the overlay at original resolution. Check every accepted ring, every component with `peak_count > 1`, every suppressed peak, and every magenta residual box.
9. Accept values only when `numeric_output_authorized` is true and the visual review agrees. Otherwise return the report's `low_confidence`/candidate evidence without claiming a complete extraction.

## Command

```powershell
python scripts\candidate_digitize_scatter.py `
  --input figure.png `
  --plot-bounds LEFT,TOP,RIGHT,BOTTOM `
  --x-anchor XPIXEL1,XVALUE1 --x-anchor XPIXEL2,XVALUE2 `
  --y-anchor YPIXEL1,YVALUE1 --y-anchor YPIXEL2,YVALUE2 `
  --marker-mode dark `
  --output-csv points.csv `
  --report scatter-report.json `
  --overlay scatter-overlay.png
```

For a distinct colour, replace `--marker-mode dark` with `--marker-mode color --marker-color '#RRGGBB'`. Add a verified `--exclude-region LEFT,TOP,RIGHT,BOTTOM` only for a compact legend or annotation that cannot be separated from markers by geometry. Never use exclusions merely to improve a count or correlation.

## Acceptance and refusal

- `candidate` plus `numeric_output_authorized: true`: retain CSV/report/overlay and complete the original-resolution review.
- `low_confidence`: do not override the refusal by visual narration or by changing thresholds until a desired count appears.
- `residual_audit.status: review_required`: do not promote residual peaks into the CSV. Correct a visibly wrong ROI, colour/polarity, or exclusion and rerun; otherwise retain the refusal.
- `validation.status: mismatch`: inspect calibration, ROI, marker grammar, multi-peak components, and suppressed peaks; do not tune points to the printed statistic.
- No printed statistic: accept only as reviewed visible geometry and state that no independent numeric annotation was available.

The report records input hash, algorithm version, deterministic run ID, calibration residuals, mask parameters, accepted/suppressed peaks, the relaxed residual audit, component peak counts, uncertainty, and limitations. These fields are the provenance contract; a prose summary is not a substitute.
