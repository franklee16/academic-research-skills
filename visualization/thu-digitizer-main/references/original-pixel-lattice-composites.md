# Original-pixel layered lattice composites

Use this candidate for raster figures made from repeated aligned layers, such as top bars, row bars, a dot/membership lattice, connectors, and categorical strips. UpSet is one instance of this grammar; the detector is not tied to sample names, row counts, column counts, or a fixed canvas.

## Source-coordinate invariant

Measure only the exact file named in the source contract. Run `init-config` on the original raster; it records SHA-256, width, height, `original_raster_pixels`, and `resampling_applied: false`.

Do not measure a chat preview, thumbnail, browser screenshot, enlarged crop, resized image, or overlay. Nearest-neighbour enlargement is review-only. If the configured hash or dimensions differ from the input, stop; do not repair the mismatch with a scale factor.

Every accepted geometry row must retain original `pixel_x`/`pixel_y` coordinates. A recreation must use the original canvas dimensions.

## Low-freedom workflow

Create a source-locked template:

```powershell
python scripts/candidate_digitize_lattice_composite.py init-config `
  --input figure.png --output lattice-config.json
```

Fill only visibly verified configuration:

- original-pixel or fractional ROIs for the column-bar and row-bar layers;
- one verified interior RGB colour (`color`) or a verified list (`colors`) and
  tolerances for column bars, row bars, and nodes;
- plausible rendered bar width/height ranges;
- optional `max_vertical_gap_px` and `min_vertical_row_fraction` when a visibly
  verified gridline splits otherwise continuous column bars;
- node patch radius plus non-overlapping active/inactive support thresholds;
- optional verified row/column labels and visibly printed column values;
- optional row-value axis anchors for independent bar-length validation.

Mark every configured colour and supplied semantic table `verified`. Do not supply an expected detected row count, column count, or active-node count. Semantic array lengths may validate detected geometry after detection; they must never change thresholds or create missing marks.

Normally keep `column_bars.role: column_bar` and `row_bars.role: row_bar`. If
the corresponding value bars are separate from the matrix or some printed
values render below one pixel, a complete repeated glyph row or column may be
used only as `role: membership_guides`. The detector must recover those guide
centres from pixel components before consulting labels or values, record the
guide role in the report, and treat value-bar geometry validation as not
applicable for that axis. Do not choose a guide role to force an expected grid
size.

Run the registered implementation:

```powershell
python scripts/candidate_digitize_lattice_composite.py extract `
  --input figure.png --config lattice-config.json --output-dir evidence
```

The evidence directory must be absent or empty. The script refuses to overwrite existing evidence.

## Completeness contract

Derive row and column centres independently from repeated bar or verified
membership-guide geometry. Classify every Cartesian row-by-column cell as:

- `active`: foreground support is at or above the verified active threshold;
- `inactive`: support is at or below the verified inactive threshold;
- `ambiguous`: support lies between the thresholds.

Never convert `ambiguous` using an expected count, correlation, row total, neighbouring pattern, or source workbook. Numeric authorization requires zero ambiguous cells, regular row/column spacing, verified visible semantic values, and every configured independent validation gate to pass.

When printed column values are verified, derive each row total from active memberships. When a row-value axis is configured, validate those totals independently against row-bar edge geometry. Keep the axis edge offset explicit; anti-aliased fills may place the first full-colour pixel beside the intended edge.

## Evidence and limits

Retain `geometry.csv`, `report.json`, `overlay.png`, deterministic run ID, complete config, input identity, all cell support fractions, spacing diagnostics, and validation errors. Review the overlay at original resolution.

This route recovers visible aligned geometry and verified printed values only. It does not recover hidden records, occluded nodes, unprinted intersections, connector meaning, or unverified OCR text. Keep it `candidate` until synthetic, vector-backed, and held-out raster strata satisfy the research-quality promotion gates.
