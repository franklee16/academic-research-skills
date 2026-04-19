# Visualization & Output in Stata

Publication-quality tables, coefficient plots, and figures. All code tested on Stata 15+.

---

## 1. Regression Tables with esttab

### Basic Table

```stata
* Run and store models
quietly reg price mpg
estimates store m1

quietly reg price mpg weight
estimates store m2

quietly reg price mpg weight foreign
estimates store m3

* Basic table
esttab m1 m2 m3, se star(* 0.10 ** 0.05 *** 0.01)
```

### Publication-Ready Table

```stata
esttab m1 m2 m3, ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("Model 1" "Model 2" "Model 3") ///
    title("Price Regressions") ///
    keep(mpg weight foreign) ///
    order(foreign mpg weight)
```

### Export to File

```stata
* Text file
esttab m1 m2 m3 using "table1.txt", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("Model 1" "Model 2" "Model 3")

* LaTeX
esttab m1 m2 m3 using "table1.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    booktabs label

* RTF (Word-compatible)
esttab m1 m2 m3 using "table1.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01)
```

### Common esttab Options

| Option | Description |
|--------|-------------|
| `se` | Show standard errors |
| `t` | Show t-statistics |
| `p` | Show p-values |
| `ci` | Show confidence intervals |
| `star(...)` | Define significance stars |
| `mtitle(...)` | Column titles |
| `title(...)` | Table title |
| `keep(...)` | Variables to show |
| `drop(...)` | Variables to hide |
| `order(...)` | Variable order |
| `label` | Use variable labels |
| `booktabs` | LaTeX booktabs format |
| `replace` | Overwrite existing file |

---

## 2. Coefficient Plots

### Basic Coefficient Plot

```stata
* After running regression
reg price mpg weight foreign i.rep78

* Plot coefficients
coefplot, drop(_cons) xline(0) ///
    title("Coefficient Plot")

graph export "coefplot.png", replace
```

### Multiple Model Comparison

```stata
* Store multiple models first
quietly reg price mpg
estimates store m1

quietly reg price mpg weight
estimates store m2

quietly reg price mpg weight foreign
estimates store m3

* Compare in single plot
coefplot m1 m2 m3, drop(_cons) xline(0) ///
    legend(order(2 "Model 1" 4 "Model 2" 6 "Model 3"))

graph export "coefplot_comparison.png", replace
```

### Vertical Coefficient Plot

```stata
coefplot m3, drop(_cons) vertical ///
    yline(0, lpattern(dash)) ///
    title("Vertical Coefficient Plot")
```

### Event Study Style Plot

```stata
* After event study regression with lead/lag dummies
coefplot, keep(lead_* lag_*) vertical ///
    yline(0, lpattern(dash)) ///
    xline(0.5, lpattern(dash) lcolor(red)) ///
    xlabel(, angle(45)) ///
    xtitle("Event Time") ytitle("Effect")
```

### Customizing coefplot

```stata
coefplot m1 m2, drop(_cons) xline(0) ///
    ciopts(recast(rcap)) ///              // Cap ends on CI
    msymbol(D) ///                         // Diamond markers
    mcolor(navy) ///                       // Marker color
    levels(95 90) ///                      // Multiple CI levels
    legend(order(1 "95% CI" 2 "90% CI"))
```

---

## 3. Summary Statistics

### Basic Summary

```stata
summarize price mpg weight

* Detailed with percentiles
summarize price, detail
```

### tabstat (Formatted)

```stata
* Multiple statistics
tabstat price mpg weight, stat(mean sd min max n) columns(statistics)

* By group
tabstat price mpg weight, by(foreign) stat(mean sd n)
```

### Summary Table with estpost

```stata
* Summary statistics table
estpost summarize price mpg weight
esttab, cells("mean(fmt(2)) sd(fmt(2)) min max count") nomtitle nonumber

* Export to file
esttab using "summary_stats.tex", replace ///
    cells("mean(fmt(2)) sd(fmt(2)) min max count") ///
    nomtitle nonumber booktabs
```

### Balance Table

```stata
* By treatment group
bysort treatment: summarize y x1 x2

* Or use tabstat
tabstat y x1 x2, by(treatment) stat(mean sd n) nototal
```

---

## 4. Basic Graphs

### Scatter Plot with Fit Line

```stata
twoway (scatter y x) (lfit y x), ///
    title("Scatter with Linear Fit") ///
    xtitle("X Variable") ytitle("Y Variable") ///
    legend(off)

graph export "scatter.png", replace
```

### Binned Scatter (binscatter)

```stata
* Install: ssc install binscatter
binscatter y x, controls(z1 z2) ///
    title("Binned Scatter") ///
    xtitle("X") ytitle("Y | Controls")
```

### Time Series

```stata
twoway line y year, ///
    title("Outcome Over Time") ///
    xtitle("Year") ytitle("Outcome")

* Multiple series
twoway (line y1 year) (line y2 year), ///
    legend(order(1 "Series 1" 2 "Series 2"))
```

### Histogram

```stata
histogram y, frequency ///
    title("Distribution of Y") ///
    xtitle("Y") ytitle("Frequency")
```

### Kernel Density

```stata
kdensity y, ///
    title("Density of Y") ///
    xtitle("Y") ytitle("Density")

* By group
twoway (kdensity y if treat==0) (kdensity y if treat==1), ///
    legend(order(1 "Control" 2 "Treatment"))
```

---

## 5. Graph Formatting

### Publication Scheme

```stata
* Set clean scheme
set scheme s1mono  // Black and white
set scheme s1color // Color version

* Or use custom
ssc install grstyle, replace
ssc install palettes, replace
ssc install colrspace, replace

grstyle init
grstyle set plain
grstyle set legend 6, nobox
grstyle set color navy maroon forest_green
```

### Common Graph Options

```stata
twoway ..., ///
    title("Main Title") ///
    subtitle("Subtitle") ///
    xtitle("X Axis Label") ///
    ytitle("Y Axis Label") ///
    xlabel(0(10)100) ///           // X ticks at 0,10,20,...,100
    ylabel(, angle(horizontal)) /// // Horizontal Y labels
    legend(order(1 "First" 2 "Second") pos(6)) /// // Bottom legend
    note("Note: Sample description") ///
    graphregion(color(white)) ///  // White background
    plotregion(margin(zero))       // No margins
```

### Export Formats

```stata
* PNG (web/slides)
graph export "figure.png", replace width(2400)

* PDF (publication)
graph export "figure.pdf", replace

* EPS (LaTeX)
graph export "figure.eps", replace
```

### Combine Multiple Graphs

```stata
* Create individual graphs
twoway scatter y1 x, name(g1, replace) title("Panel A")
twoway scatter y2 x, name(g2, replace) title("Panel B")

* Combine
graph combine g1 g2, rows(1) ///
    title("Combined Figure")

graph export "combined.png", replace
```

---

## 6. RD Plots (Stata 16+)

```stata
* Using rdplot (requires rdrobust package)
rdplot y running_var, c(0) ///
    graph_options(title("RD Plot") ///
                  xtitle("Running Variable") ///
                  ytitle("Outcome"))
```

---

## Quick Reference

### Table Output Commands

| Command | Purpose |
|---------|---------|
| `esttab` | Regression tables |
| `estpost` | Post results for tables |
| `tabstat` | Summary statistics |
| `tabout` | Cross-tabulations |

### Graph Commands

| Command | Purpose |
|---------|---------|
| `coefplot` | Coefficient plots |
| `binscatter` | Binned scatter plots |
| `twoway` | General 2D graphs |
| `histogram` | Histograms |
| `kdensity` | Kernel density |
| `graph combine` | Multi-panel figures |

### Export Checklist

- [ ] Use vector format (PDF/EPS) for line plots
- [ ] Use 300+ DPI for raster images
- [ ] Include informative axis labels
- [ ] Add reference lines where appropriate
- [ ] Use consistent color scheme
- [ ] Match journal font requirements
