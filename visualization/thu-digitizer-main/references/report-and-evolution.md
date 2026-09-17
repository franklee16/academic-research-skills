# Report and evolution protocol

## Required extraction evidence

Keep these artefacts together for every extraction:

- Input-file hash and raster dimensions.
- Execution strategy. For deterministic runs, keep the registered implementation name, algorithm version, run ID, and complete parameters. For model-assisted runs, keep the runtime model name/profile, strategy reason, per-mark evidence/status, and references to preserved deterministic comparison reports.
- Plot bounds and two calibration anchors per linear axis.
- CSV values, JSON report, and an overlay or reproduction.
- Per-series sample coverage and confidence.
- Error-bar pixel endpoints, values, and status (`extracted` or `not_extracted`).
- The applicable completeness evidence: a declared-slot coverage ledger with standard reason codes, a compact-scatter residual audit, or an explicit reason that neither applies.

Do not call an estimate an extraction when it lacks pixel evidence. `not_extracted` is a valid and preferred result.

## Benchmark case format

Keep a small manifest outside the skill or in a consented project directory. Store synthetic cases by default. For a user-owned image, retain the image only with explicit permission; otherwise retain its SHA-256 hash, calibration, correction CSV, and non-sensitive feature notes.

```json
{
  "schema_version": 1,
  "cases": [
    {
      "id": "synthetic-line-001",
      "kind": "synthetic",
      "truth_csv": "truth.csv",
      "required_metrics": {"max_mae": 0.5, "max_error_bar_endpoint_px": 1}
    }
  ]
}
```

Measure numeric-series MAE with `scripts/evaluate_digitization.py`. Measure error-bar endpoints separately in pixel space before mapping them to data units. Do not use a visual match or image similarity score as the sole gate.

## Promotion loop

1. Read [research-quality-baseline.md](research-quality-baseline.md) and define the visible, recoverable representation and its non-recoverable limits.
2. Save the failed input hash, current output, correction, and a concise failure label.
3. Write a candidate algorithm/configuration change outside the stable path.
4. Run the current and candidate versions on every benchmark case, including the baseline's applicable held-out robustness conditions.
5. Promote only if the relevant numeric, structural, confidence, and reproducibility metrics improve without an existing regression. For P0 work, also record the fair WebPlotDigitizer comparison or `not_compared` reason.
6. Present the evidence and obtain user approval before changing `SKILL.md` or stable scripts.
7. Record the version identifier and preserve the prior stable files for rollback.

Never auto-promote a rule from a single image. Do not send benchmark images or corrections to remote services unless the user explicitly authorizes it.
