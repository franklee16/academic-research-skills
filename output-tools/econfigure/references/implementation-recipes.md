# Figure Implementation Recipes

Use the project's existing software and dependency set. Do not install a plotting package without authorization. Keep all values derived from the underlying data or model objects; styling code must never contain hand-copied estimates.

## Reproducible build contract

- Separate data/model preparation from styling, but run both from one documented entry point.
- Save the tidy plotting dataset when it is a nontrivial transformation of model output. Include estimate, standard error or bounds, panel, series, order, units, and reference-category flags.
- Set category/factor ordering explicitly. Assert uniqueness of plot keys such as `(outcome, subgroup, event_time, estimator)`.
- Export with fixed width and height. Use vector PDF/SVG plus PNG preview. Never rely on an IDE window size.
- Put figure numbers/captions in LaTeX, Quarto, Word, or the journal production system rather than baking them into the art.
- If the target journal is named, check its current author guide before export and follow its required file type, color space, resolution, font, and accessibility/alt-text profile. Treat PNG as a review preview when the journal requires another production format such as TIFF or EPS.

## R: ggplot2

Use a compact project theme modeled on the sample set:

```r
econ_cols <- c(
  ink = "#231F20", blue = "#365AA4", bright_blue = "#008CC1",
  light_blue = "#7FBCE3", orange = "#F7901C", red = "#C93733",
  green = "#27994D", grid = "#C9CED1", ci = "#DEDEDE"
)

theme_econ <- function(base_size = 9, base_family = "sans") {
  ggplot2::theme_classic(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      plot.title.position = "plot",
      plot.title = ggplot2::element_text(size = base_size + 2, hjust = 0),
      plot.subtitle = ggplot2::element_text(size = base_size, hjust = 0),
      strip.background = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(size = base_size + 1, hjust = 0),
      panel.grid = ggplot2::element_blank(),
      legend.position = "top",
      legend.justification = "left",
      legend.title = ggplot2::element_blank(),
      axis.line = ggplot2::element_line(color = econ_cols["ink"], linewidth = .45),
      axis.ticks = ggplot2::element_line(color = econ_cols["ink"], linewidth = .4)
    )
}

theme_econ_ygrid <- function() {
  ggplot2::theme(
    panel.grid.major.y = ggplot2::element_line(color = econ_cols["grid"], linewidth = .18),
    panel.grid.major.x = ggplot2::element_blank(),
    panel.grid.minor = ggplot2::element_blank()
  )
}
```

Add `theme_econ_ygrid()` only for descriptive bars/time series that benefit from lookup gridlines. For event studies, use `geom_hline(yintercept = 0)`, a dashed `geom_vline()` at the treatment boundary, and `geom_errorbar()` or `geom_linerange()` for intervals. Encode estimators with both `scale_color_manual(values = c("Estimator A" = econ_cols[["blue"]], "Estimator B" = econ_cols[["orange"]]))` and `scale_shape_manual(values = c("Estimator A" = 16, "Estimator B" = 15))`; replace labels with the actual estimator names. Use `position_dodge()` only enough to prevent overlap. Explicitly insert or flag the omitted period rather than allowing a line to interpolate across it.

`ggplot2` line `linewidth` values are approximately millimeters, whereas `visual-system.md` specifies points. Useful mappings are `.50 mm ≈ 1.42 pt` for a focal line, `.32 mm ≈ 0.91 pt` for an interval/reference line, and `.18 mm ≈ 0.51 pt` for a light gridline. Inspect at final size rather than applying point values directly as `linewidth`.

For forests, create ordered label rows, use `geom_point()` plus `geom_errorbar(orientation = "y")` or `geom_segment()`, facet by outcome when units differ, and assemble aligned text columns with `patchwork`, `cowplot`, or a table grob already present in the project.

Export, for example:

```r
ggsave("output/figure_main.pdf", p, width = 6.6, height = 4.4, units = "in",
       device = grDevices::pdf, useDingbats = FALSE)
ggsave("output/figure_main.png", p, width = 6.6, height = 4.4, units = "in", dpi = 400, bg = "white")
```

Start with the generic `sans` family. Use a manuscript-specific font only after a probe render confirms that the selected device can resolve and embed it without warnings. Test the chosen PDF device rather than trusting `capabilities("cairo")`: Cairo may still fail because of a missing runtime library. On macOS, Quartz PDF is a useful fallback; otherwise use a tested base PDF device with fonts and symbols verified. After every export, assert that the target file exists and is nonempty, inspect warnings and embedded fonts (for example with `pdffonts`), verify PDF MediaBox and PNG pixel dimensions against the fixed canvas, and render the PDF back to an image for inspection.

## Stata

Prefer native `twoway`, `graph combine`, and existing project packages. User-written commands such as `coefplot` or `event_plot` are useful only when already installed or when installation is authorized.

Core styling options:

```stata
graphregion(color(white)) plotregion(color(white))
ylabel(, angle(horizontal) nogrid)
xlabel(, nogrid)
yline(0, lcolor("146 151 157") lwidth(vthin))
legend(region(lcolor(none)) rows(1))
```

For a descriptive chart that benefits from horizontal lookup lines, replace `nogrid` in `ylabel()` with `grid glcolor("201 206 209") glwidth(vthin)`. Keep coefficient, event-study, and RD plots gridless by default.

If the Stata version accepts hex colors, use the palette hex codes. Otherwise use the RGB triplets in `visual-system.md`, quoted as `"R G B"`.

- Event study: overlay `rcap ci_lo ci_hi event_time, lcolor("146 151 157")` with `scatter estimate event_time, mcolor("54 90 164") msymbol(O)`; add the treatment boundary using `xline()` and label endpoint bins explicitly.
- Two estimators: offset x positions by a small documented amount and distinguish both marker symbol and color.
- Forest: use a numeric row index, `rcap`/`rspike` for intervals, `scatter` for estimates, and `ylabel()` for readable subgroup labels. Add interaction p-values in a separate aligned text element or in the manuscript table, not as stars on points.
- Panels: export individual graphs at identical dimensions and combine them with shared margins; suppress repeated legends and axis titles deliberately.

Use `graph export ..., replace` only for an explicitly targeted output file. Prefer PDF for manuscript art and a high-resolution PNG for review.

## Python: matplotlib/seaborn

Set style locally rather than modifying a user's global configuration:

```python
from matplotlib import rc_context
import matplotlib.pyplot as plt

ECON_RC = {
    "figure.facecolor": "white", "axes.facecolor": "white",
    "font.family": "sans-serif", "font.size": 9,
    "axes.edgecolor": "#231F20", "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "xtick.color": "#231F20", "ytick.color": "#231F20",
    "legend.frameon": False, "pdf.fonttype": 42, "ps.fonttype": 42,
}

with rc_context(ECON_RC):
    fig, ax = plt.subplots(figsize=(6.6, 4.4), constrained_layout=True)
    # draw data with a higher z-order than grid/reference lines
    fig.savefig("output/figure_main.pdf")
    fig.savefig("output/figure_main.png", dpi=400, facecolor="white")
    plt.close(fig)
```

Define reusable encodings such as `COLORS = {"Estimator A": "#365AA4", "Estimator B": "#F7901C"}` and `MARKERS = {"Estimator A": "o", "Estimator B": "s"}`, replacing the labels with actual estimator names. Use `ax.errorbar()` for dot-whisker plots, `fill_between()` for bands, and `sharex`/`sharey` for comparable panels. Add `ax.grid(axis="y", color="#C9CED1", linewidth=0.5, zorder=0)` only for descriptive plots that need lookup lines. For complex panel layouts, use `GridSpec` and one figure-level legend. Do not call `tight_layout()` after manually positioned annotations without visually checking the result.

## LaTeX assembly

- Use `graphicx` and size figures by manuscript width, such as `width=\linewidth`; do not scale a low-resolution raster upward.
- Use `subcaption` only when panels are separate files or need cross-references. If panel letters are already inside the combined art, do not add a second set.
- Keep `\caption{}` and `\label{}` outside the image. Put the label immediately after the caption.
- Avoid `\resizebox` as a substitute for designing at the correct dimensions.

## Programmatic checks

Where the language permits, assert that interval bounds are ordered, event times are unique within series, reference coefficients equal the documented convention, and plotted row counts match the intended sample. Require the point estimate to lie inside the interval only for interval methods where that is an invariant, such as a conventional symmetric Wald interval; percentile/BCa bootstrap, inverted tests, profile, Fieller, or disjoint confidence sets need method-specific validation. Render the final PDF to an image before declaring success. Verify that `≤`, `≥`, minus signs, non-Latin labels, and math symbols survive the selected font/device; use an explicit ASCII fallback only when the target system cannot render them reliably.
