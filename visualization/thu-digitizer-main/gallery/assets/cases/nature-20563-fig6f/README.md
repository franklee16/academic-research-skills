# Nature Communications 2021 Fig. 6f evidence package

Status: `candidate`.

`data.csv` is the primary image-derived extraction. It contains 30 visible
18-degree polar-histogram bins across the D = 30, 15, and 10 μm panels, with
the calibrated radial value, approximate raster uncertainty, and original-
raster chord endpoints. `recreated.png` and the interactive gallery view are
driven only by this CSV and retained calibration; neither imports the official
workbook.

The recoverable representation is the visible bin interval and outer radial
chord. The original force-vector observations and an author-side exact count
table are not recoverable from the raster. The radial axis has printed numeric
ticks but no explicit unit label, so the CSV uses
`displayed_histogram_count`.

The official caption says Source Data for panels c–f are provided, but the
downloaded workbook has `Figure 6d` and `Figure 6e` sheets and no verifiable
`Figure 6f` polar-bin table. The separate validation report therefore records
`metric_absent_in_source_workbook`; it never fills or changes the primary CSV.
