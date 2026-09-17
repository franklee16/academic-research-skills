# Decisions Derived from the Supplied Samples

This reference records what to emulate and what not to copy literally. It is provenance for the defaults, not a requirement to reproduce every source's house style.

File links, versions, page systems, and SHA-256 checksums are recorded in [sample-manifest.md](sample-manifest.md). The skill remains usable when the raw library is absent because all operative rules are distilled here and in the visual system.

## Supplied color/style images

- `22011.png`: six aligned small-multiple line charts; bright blue (`#008CC1`) versus orange (`#F7901C`), redundant square/circle markers, common axes, and compact in-panel legends. Reuse the blue–orange pairing and panel consistency; prefer one shared legend when assembly permits.
- `22225.png`: a 2×2 coefficient/event-study composition using research blue (`#365AA4`) and diagnostic red (`#C93733`), with line type and marker shape also distinguishing series. Reuse the common treatment boundary and redundant encoding.
- `22319.png`: a vertically stacked time-series composition with directly annotated event lines in gray, red, and green, plus direct labels on the two outcome lines. Reuse restrained event annotation. Treat the dual axis as an exception, not a default.
- `22432.png`: a 2×2 monochrome treatment-effect layout with black estimates and light-gray uncertainty bands. Reuse this when color adds no information.
- `22836.png`: an aggregate panel above two subgroup panels and nested 90%/95% intervals. Reuse the hierarchy and the wider-gray/narrower-blue interval convention when both confidence levels matter.
- `23291.png`: an RD/binned-scatter design with blue binned points, separate black fits, and a strong cutoff line. Reuse the visual separation of data, fit, and cutoff.
- `23415.png`: ordered neutral-gray bars with black intervals, readable wrapped category labels, and direct numeric values. Reuse only for quantities with a meaningful zero; use dot-whiskers for regression coefficients.
- `23839.png`: two aligned interrupted-trend panels with blue observed points and red fitted segments. Reuse separate pre/post fits and the common intervention marker.
- `1-s2.0-S0304387822000815-gr4.jpg`: four aligned placebo-exposure coefficient panels, a visible zero line, and separation between the main estimate and shifted placebo estimates. Reuse the panel logic; strengthen text size and grayscale contrast in new work.

## Schwabish (2014), *An Economist's Guide to Visualizing Data*

The operative principles are: show the data, reduce clutter, and integrate text with the graph. Specific decisions adopted here include lighter gridlines than data, small multiples instead of spaghetti charts, direct or nearby labels, no 3-D effects, no ornamental gradients, and bar/slope alternatives to difficult pie comparisons. Color figures must still work in grayscale.

## `CLL_SNWT.pdf`

- Figure 2 uses four aligned event-study panels with a common reference structure and shared note.
- Figure 3 compresses many robustness checks into four side-by-side forest panels with specification labels at left.
- Table 1 groups summary statistics by data level and outcome family.
- Tables 2–3 use outcome spanners, numbered columns, coefficient/SE stacking, compact specification rows, and self-contained notes.

Adopt the event-study/forest organization and table-to-figure narrative. Increase final-size text and avoid overly small central plot regions.

## Kleven et al. (2021), *Does Biology Drive Child Penalties?*

- Figures 1–3 use vertically stacked event-study small multiples, shared event time, dark/light blue families, redundant open/filled markers, gray confidence bands, a labeled birth boundary, and direct long-run effect annotations.
- Figure 2 gives related mechanisms identical panel grammar, making cross-outcome reading fast.
- Table 1 compares three samples using P25/Mean/P75 rather than defaulting mechanically to mean/SD.
- Table 2 summarizes graphical results in conceptually defined short-run and long-run panels with identical outcome columns.

Adopt the stable grammar across related figures, the light/dark hierarchy, and the table that summarizes graphically defined estimands.

## Sha (2023), *The Political Impacts of Land Expropriation in China*

- Figure 4 pairs neutral placebo distributions with red actual-statistic lines and p-value annotations.
- Figures 5–6 use 2×2 and larger small-multiple event studies with treatment-period shading and redundant red/green encodings.
- Figure 7 combines descriptive bars across panels with related but distinct samples.
- Tables 6–9 use outcome/sample spanners, panel blocks, and lower specification/summary rows.

Adopt the placebo layout and multi-outcome panel organization. Do not rely on red/green alone, crowd stars into figures, or reproduce journal two-column constraints when a standalone full-width figure is available.

## Wang et al. (2023), *Building Tall, Falling Short*

- Figures 4–6 sequence distance-gradient evidence, event-study validation, and outcome spillovers. They distinguish groups with marker fill/color and state reference bins in the notes.
- Tables 2–8 use dependent-variable spanners, numbered models, panel families, specification blocks, joint-effect tests, observations, fit statistics, and detailed notes.

Adopt the evidence sequence and block organization. Do not copy the preprint watermark, tiny labels, crowded long notes, or inconsistent minor typography.
