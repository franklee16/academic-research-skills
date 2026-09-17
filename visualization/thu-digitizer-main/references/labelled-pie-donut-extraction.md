# Visible-label pie and donut extraction

Use `scripts/candidate_digitize_labelled_donut.py` only when numeric labels are
explicitly printed and can be mapped to visibly distinct sector colours. The
recoverable primary representation is the printed label, not an angle-derived
percentage and not underlying source observations.

## Configuration contract

Provide a JSON configuration containing:

- `source_contract.sha256` and `source_contract.dimensions` when known;
- inclusive original-pixel `panel_bounds`;
- a named `palette` of `#RRGGBB` colours;
- one or more groups with a verified centre and annular radial band;
- each visible label's series, original-pixel anchor, `transcription_a`, and
  `transcription_b`;
- optional sampling and validation tolerances under `parameters`.

Do not provide an expected sector count, expected group total, source workbook
row count, or an inferred value for an unlabeled sector.

```powershell
python scripts/candidate_digitize_labelled_donut.py `
  --input figure.png --config donut-config.json `
  --output-csv labels.csv --geometry-csv sector-geometry.csv `
  --report donut-report.json --overlay donut-overlay.png
```

## Authorization logic

The route authorizes a label only when both transcriptions parse as the same
number, the named colour forms one supported annular sector, and the label's
within-group normalized share agrees with independently sampled geometry within
the configured tolerance. Geometry is validation-only: it can reject a label
but can never supply, replace, round, or normalize a primary value.

Keep printed group sums exactly as observed. A sum below or above 100 is not an
error by itself. Report unmatched transcription, absent geometry, multi-run
geometry, or label/geometry disagreement per record with a standard reason
code. Preserve rejected records in the report and primary CSV with blank numeric
output.

This is an assisted candidate route. OCR discovery, unlabeled-sector recovery,
3D pies, exploded/overlapping sectors, gradients, photographs, and inaccessible
original rasters remain unsupported.
