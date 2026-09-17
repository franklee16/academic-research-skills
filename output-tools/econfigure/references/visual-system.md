# Economics Figure Visual System

Use these defaults unless a journal template, established project style, or explicit user preference takes precedence. They distill the supplied figure images and the strongest layout choices in the supplied economics papers.

## Final-size canvas

Design at the dimensions in which the reader will see the figure; do not create a large plot and shrink it blindly.

| Target | Width | Typical height | Use |
|---|---:|---:|---|
| Single column | 3.2–3.5 in | 2.2–4.2 in | One simple plot, at most two short panels |
| Full page width | 6.4–7.0 in | 3.8–7.5 in | Event studies, forests, or 2–6 panels |
| Slide/standalone | 10–12 in | 5.6–7.0 in | Presentation only; increase all text proportionally |

Use a white background and generous outer whitespace. Keep plot regions aligned. Avoid decorative frames, drop shadows, gradients, textures, and 3-D effects.

Choose one delivery mode before laying out text:

- **Paper mode:** keep only panel headings and short annotations inside the art. Let LaTeX/Word supply the figure number, figure-level caption, notes, and source. Multi-panel, event-study, and forest figures normally use the full text width.
- **Standalone/slide mode:** add a concise descriptive title above the plot and put the unit in a subtitle or axis title. Scale type for viewing distance; do not also duplicate a manuscript caption inside the image.

## Typography

- Match the manuscript font when it is embedded and readable. Otherwise use a restrained sans serif such as Arial, Helvetica, or Source Sans for figures; use one family throughout.
- At final journal size, use approximately 10–11 pt for panel headings, 8.5–9.5 pt for axis titles, 8–9 pt for ticks and legends, and no less than 7.5 pt for annotations.
- Use sentence case. Prefer `Panel A. Outcome` or `Panel A: Outcome`, selected consistently across the paper. Place panel headings flush left above each plot.
- Write units once in the axis title or subtitle, not after every tick. Use real minus signs in rendered output and thousands separators where helpful.
- Spell out unfamiliar abbreviations inside the figure or caption. A figure should be interpretable without searching earlier pages.
- Keep figure numbers, the figure-level title, source, and long notes outside the plot image for journal manuscripts. Panel headings and short treatment-date labels belong inside the figure.

## Sample-derived palette

The supplied examples repeatedly use white, near-black, light gray, and one or two saturated accents. These are the default colors:

| Role | Hex | RGB | Use |
|---|---|---|---|
| Ink | `#231F20` | 35, 31, 32 | Text, axes, fitted lines |
| Research blue | `#365AA4` | 54, 90, 164 | Default estimate or focal series |
| Bright blue | `#008CC1` | 0, 140, 193 | Two-group line charts |
| Light blue | `#7FBCE3` | 127, 188, 227 | Context or comparison series |
| Orange | `#F7901C` | 247, 144, 28 | Second series paired with bright blue |
| Diagnostic red | `#C93733` | 201, 55, 51 | Cutoffs, warnings, or a contrasting fitted series |
| Green | `#27994D` | 39, 153, 77 | Third series or event annotation, with redundant encoding |
| Mid gray | `#92979D` | 146, 151, 157 | Secondary intervals and context points |
| CI gray | `#DEDEDE` | 222, 222, 222 | Confidence bands, usually 45–70% opacity |
| Grid gray | `#C9CED1` | 201, 206, 209 | Sparse major gridlines |
| Pale region | `#F1F2F3` | 241, 242, 243 | Treatment-period shading, sparingly |

Recommended combinations:

- One estimate: research blue, with dark or mid-gray confidence intervals.
- Two groups: bright blue plus orange, and also solid-circle versus dashed-square.
- Focal versus context: dark research blue plus light blue, and filled versus open markers.
- Diverging or diagnostic comparison: research blue plus diagnostic red. Do not imply good/bad unless the meaning warrants it.
- Three or four groups: research blue, orange, green, and diagnostic red, with distinct markers and line types. Direct-label whenever space permits.

Red and green from the sample set are not safe as color-only encodings. Whenever both appear, combine red solid circles with green dashed crosses/asterisks or another equally clear redundant distinction. Ensure all series remain separable in grayscale. Do not use rainbow palettes.

## Marks, lines, and uncertainty

- Primary data line: 1.2–1.6 pt. Secondary line: 0.9–1.2 pt. Reference line: 0.7–0.9 pt. Major grid: 0.35–0.55 pt.
- Point markers: about 4–5.5 pt at final size; smaller for dense scatterplots. Do not put markers on every observation of a high-frequency line.
- Whiskers: 0.8–1.0 pt with short caps. Draw a wider/lighter 95% interval behind a narrower/darker 90% interval when using nested intervals.
- Confidence bands: neutral gray or a low-opacity tint of the series color. The central estimate must remain clearly visible.
- Raw points should be lighter or smaller than fitted values. Avoid heavy outlines around every mark.

## Axes and scaffolding

- Keep the left and bottom axes in ink; remove the top and right spines unless a full box conveys a specific design used throughout the manuscript.
- Use a small number of major horizontal gridlines in grid gray for descriptive bars and long time series. Coefficient, event-study, and RD plots default to no grid or an extremely light horizontal grid. Usually omit vertical gridlines. If reference zero is substantively important, draw it slightly darker than the other gridlines but lighter than the data.
- Put tick labels horizontally whenever possible. Rotate time/category labels only when shortening, staggering, or changing orientation cannot solve the problem.
- Use meaningful tick intervals and consistent decimal precision. Avoid scientific notation for ordinary quantities.
- Add a vertical dashed line or pale region for an intervention/cutoff. Label the event directly and keep annotations from overlapping estimates.
- Do not force every plot to start at zero. Estimates and line charts may use a focused range; bars must start at zero.

## Legends and direct labels

Prefer direct labels at line ends or beside focal points. If a legend is necessary:

- place one shared legend above the panels, immediately below the title, or in genuine empty plot space;
- order entries in the same order readers encounter the lines or panels;
- reproduce color, marker, and line type in each key;
- use one row when it fits; avoid a large boxed legend floating far from the data.

Formal journal output defaults to a frameless legend. An unobtrusive thin border is acceptable only when a working-paper legend sits inside genuine empty plot space and the frame improves separation.

## Multi-panel arrangement

- Two panels: use 1×2 when labels remain readable; otherwise 2×1.
- Three panels: use 1×3 for short/wide plots or a centered top panel above two aligned lower panels when the first is the aggregate and the other two are subgroups.
- Four panels: use 2×2. Six panels: use 3×2 or 2×3 according to the aspect ratio and reading order. Seven related appendix panels may use a deliberate 4+3 layout with the final slot left blank; do not shrink all seven into one unreadable row.
- Keep panel widths, plot-region sizes, tick positions, and scales identical when comparison is intended.
- Repeat axis titles only when panels must stand alone; otherwise use shared outer titles. Do not delete tick labels if doing so makes values hard to retrieve.
- Use one shared legend and one shared note. Put aggregate/benchmark panels first, then mechanisms or subgroups in a pre-specified conceptual order.
- Do not arrange panels by statistical significance or leave an unexplained empty cell.

## Caption and note

A journal caption should state, as relevant:

1. what each panel and visual encoding represents;
2. sample, observation unit, period, and outcome units/transformation;
3. the estimand/model or equation reference;
4. omitted/reference category and any endpoint binning;
5. confidence level, standard-error method, clustering, weights, and bootstrap repetitions;
6. non-obvious data construction and the data source.

Keep interpretation in the surrounding prose. Do not turn the note into a miniature results section.

## Visual QA gate

Before delivery, confirm all of the following:

- every plotted number agrees with the source data/model object;
- labels, panel order, units, and reference periods are correct;
- no clipping, overlap, mojibake, or font substitution is visible in the rendered file;
- the focal data remain dominant at 100% and at the final printed size;
- multi-panel axes are aligned and comparable;
- color distinctions survive grayscale and a common color-vision simulation;
- PDF/SVG text is vector text where possible and fonts are embedded;
- the PNG has a white background and adequate effective resolution;
- the file contains no accidental title duplication, editor handles, watermark, or transparent artifacts.
- alt text exists for the production submission when required and accurately summarizes the figure without making unsupported inferential claims.
