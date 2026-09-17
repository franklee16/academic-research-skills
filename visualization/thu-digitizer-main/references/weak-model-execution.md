# Weak-model execution contract

Use this contract when the runtime model is weak, unidentified, or has already
missed/over-counted visible marks.  Reduce judgment by making the model a
configuration and review assistant around registered deterministic scripts.

## Mandatory five-stage loop

1. **Inventory the visible grammar.** Declare panels, category/series slots,
   label anchors, axes, legends, and visibly blank slots. Derive slots only from
   rendered structure; never pass an expected data-point, active-node, sector,
   or source-row count to a detector.
2. **Lock exclusions before detection.** Record every legend, annotation, inset,
   or decorative exclusion as original-pixel bounds with a visible reason. Do
   not add an exclusion after seeing an inconvenient candidate unless the
   original raster independently proves its non-data role.
3. **Run the registered primary detector.** Preserve the source hash, dimensions,
   exact parameters, deterministic run ID, CSV, report, and overlay. Do not
   replace a refusal with visual estimates.
4. **Run the family completeness check.** For scatter, require the relaxed
   negative-space residual audit to be `clear`. For declared bar/label slots,
   require a coverage ledger with a status and reason code for every slot; for
   an aligned lattice, require complete active/inactive/ambiguous cell
   classification. A residual pass may block authorization; it must never add
   values.
5. **Review at original resolution.** Check accepted geometry, ambiguity layers,
   residual candidates, and exclusions. Refine only visibly wrong bounds,
   calibration, colour, or grammar, then rerun from the original image.

## Standard reason codes

Use the codes implemented by `scripts/extraction_contract.py`:

| Code | Meaning |
|---|---|
| `visible_geometry_supported` | Original pixels uniquely support the mark. |
| `visible_label_verified` | Duplicate label transcriptions and independent geometry agree. |
| `no_supported_geometry` | No unique mark is supported in the declared slot. |
| `ambiguous_geometry` | Multiple plausible geometries or transcriptions remain. |
| `calibration_geometry_conflict` | Visible geometry conflicts with calibration or validation. |
| `occluded` / `fused` / `below_resolution` | The rendered image cannot uniquely separate the mark. |
| `not_drawn` | The declared structural slot is visibly blank, not a numeric zero. |
| `unsupported_route` | The chart grammar has no compatible registered route. |
| `detector_residual` | A second pass found unresolved marker-like evidence. |
| `source_contract_mismatch` | Hash or dimensions differ from the locked source. |

Do not collapse these codes into generic `not_extracted`. Keep a human-readable
detail beside the code.

## Multi-panel execution

- Create one FigureSpec panel and one extraction report per panel. Never reuse
  pixel calibration across panels merely because axes look alike.
- Keep a batch ledger with panel ID, route, source hash, declared slots,
  authorized slots, reason-code counts, overlay path, and status.
- Resume only missing/failed panels. Do not rerun successful panels with new
  thresholds selected from other panels' answers.
- Aggregate only authorized rows; retain every panel refusal in the final report.

## Blind forward testing

Test weak models on raw figures without expected counts or intended fixes. Score
configuration validity, mark precision/recall, unsafe false acceptance, correct
refusal, evidence completeness, elapsed time, and output determinism. Keep a
route candidate until synthetic, real-vector, held-out real-raster, and fair
comparison gates are satisfied.
