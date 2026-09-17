# Nature Communications 2023 Fig. 1f evidence package

Status: `partial_visible`.

`data.csv` is the primary extraction: 18 percentages explicitly printed next
to four donut charts (Normal 4, AK 5, Primary 4, MET 5).  It does not contain
values filled from a workbook.  The printed group sums are 97.5, 90.6, 70.3,
and 73.6, so they must not be silently forced to 100.  A pie renderer may
normalize each group's visible values for sector angles while retaining the
original labels.

`sector-geometry.csv` is separate validation-only evidence from annular colour
sampling on the official 2050 x 1399 raster.  The route is case-local because
the shared registry marks pie/donut unsupported.  `report.json` records the
scope, hash, deterministic run, geometry comparison, and non-recoverable
quantities.  `overlay.png` and `recreated.png` have the same dimensions as
`panel-original.png`.

The Figure 1 caption states that Source Data are provided for panels b and e,
not f.  Supplementary Data File 6 is retained only as related provenance; it
has not been used to complete or overwrite the visible labels.

Rebuild:

```powershell
python -X utf8 candidate_digitize_donut_case.py `
  --input figure1-original.png --output-dir .
python -X utf8 -m unittest test_candidate_digitize_donut_case.py -v
```
