# Scatter points over pastel bars

Use this reference when coloured dots/strip points are overlaid on a bar, especially when the point colour also appears in the bar border. Recover only uniquely supported visible centres; this route does not recover hidden raw observations.

## Marker-core segmentation

1. Work in the original raster and save its hash, dimensions, group ROI, calibration, and sampled RGB/HSV values.
2. Sample a solid marker-core pixel and a pastel-fill interior pixel separately. A hue-only mask is insufficient when both share a hue.
3. Build a marker-core mask from colour distance plus saturation/value checks. Keep the tolerance and sampled colours in the report.
4. Score compact local shapes with a disc/circle template or an equivalent blob test. A bar edge is horizontal or vertical evidence, not by itself a marker.
5. Fit the bar fill and outline geometry independently. Preserve, rather than erase, candidates touching that geometry for review.
6. Create nearest-neighbour enlarged crops for audit. Enlargement only exposes source pixels; it cannot resolve two markers that the source raster has merged.

## Output contract

| Status | Meaning | May appear in an accepted point table? |
|---|---|---|
| `visible_marker_candidate` | A locally compact marker core has original-pixel support and is not geometrically confounded with a bar edge. | Yes, labelled as a visible candidate. |
| `bar_outline_overlap_candidate` | A compact marker-like core touches a calibrated bar border. | No; keep in the review layer. |
| `merged_cluster_candidate` | More than one marker could explain the same connected pixel region. | No; keep as a cluster/region, not invented centres. |
| `not_extracted` | The raster does not support a unique centre or value. | No. |

Every candidate needs its data value, pixel centre, marker-colour evidence, shape-support score, crop/ROI, status, and overlay. Category-jitter x is useful for group assignment, not a continuous measurement unless calibrated as one.

## Decision rule

- A compact core away from bar geometry can become `visible_marker_candidate`.
- A core intersecting a bar edge becomes `bar_outline_overlap_candidate`, even when it looks plausible after magnification.
- A fused blob with multiple compatible decompositions becomes `merged_cluster_candidate`; report its visible region and uncertainty, not a guessed sample count or a table of guessed coordinates.
- If a dark outline cannot be distinguished from a marker or calibration is uncertain, return `not_extracted` for that quantity.

Do not infer a sample count from another panel, bar height, alpha darkness, group totals, or expected cohort size. Do not convert a replot that looks plausible into numeric evidence.

## Required validation before promotion

Add synthetic truth cases that separately cover: isolated points above a pastel bar; points inside the fill; points on a horizontal/vertical border; touching pairs; dense fused clusters; low-resolution/JPEG variants. Use one-to-one point matching and report precision, recall, normalized x/y MAE, P95 error, false acceptance of edge geometry, correct-refusal rate for fused clusters, and deterministic output equality. A candidate becomes stable only after the binding baseline's held-out and regression gates pass.
