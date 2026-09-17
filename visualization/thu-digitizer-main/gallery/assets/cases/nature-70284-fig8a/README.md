# Nature Communications Figure 8a evidence bundle

Article DOI: `10.1038/s41467-026-70284-8`

Case status: `partial_visible`. The registered raster bar candidate extractor authorizes 13 of 16 visible bars (81.25%). The consolidated primary CSV leaves three rows blank and unauthorized:

- Temperature sensitivity: TreeBL to CropR
- Regional contribution: TreeBL to CropR
- Regional contribution: Shrub to CropR

The black bootstrap-interval strokes split pale fills into multiple components in the affected registered-detector invocations. No visual inference or source-data value was used to fill these rows.

## Core deliverables

- `original/41467_2026_70284_Fig8_HTML.png`: exact official raster used for measurement.
- `preflight-report.json` and `figure-spec.json`: unified preflight and verified panel/calibration record.
- `extraction/fig8a-primary.csv`: consolidated 16-row primary table; 13 authorized values and 3 blank rows.
- `extraction/fig8a-report.json`: case status, authorization scope, coverage, grammar, and limitations.
- `extraction/fig8a-overlay.png`: full-canvas review overlay; magenta bars and cyan intervals are authorized, orange marks are not authorized.
- `extraction/fig8a-recreation.png`: full-canvas pixel-space recreation from authorized rows only.
- `validation/source-validation.csv` and `validation/source-validation-report.json`: independent source-data validation record; 0 comparable pairs and no filling of the primary CSV.
- `provenance/SOURCES.md`, `provenance/source-record.json`, and `provenance/COMMANDS.md`: official URLs, hashes, rights, mappings, and command record.

The 15 per-color registered-extractor invocations and their CSV/report/overlay/recreation outputs remain intact under `extraction/`.

