# pubfig Recipes

`pubfig` is the default engine for scientific figures.

## Core route

Typical minimal workflow:

```python
import pubfig as pf

fig = pf.line(data, x=x, series_names=["A", "B"])
pf.save_figure(fig, "figure1.pdf")
```

## Common figure families

| Need | Preferred `pubfig` functions |
|---|---|
| benchmark comparison | `bar_scatter`, `grouped_scatter`, `bar`, `line` |
| ablation | `bar_scatter`, `dumbbell`, `paired`, `bar` |
| distribution | `box`, `violin`, `raincloud`, `histogram`, `density`, `ecdf`, `qq` |
| relationship | `scatter`, `bubble`, `contour2d`, `hexbin` |
| trend | `line`, `area` |
| diagnostic / evaluation | `calibration`, `forest_plot`, `bland_altman`, `volcano`, `roc`, `pr_curve` |
| composition / hierarchy | `donut`, `upset`, `radial_hierarchy`, `circular_grouped_bar`, `circular_stacked_bar`, `stacked_ratio_barh` |
| matrix / map | `heatmap`, `corr_matrix`, `clustermap` |

## Export defaults

For a normal first pass:

```python
pf.save_figure(fig, "figure1.pdf")
```

For multiple formats:

```python
pf.batch_export(
    fig,
    "figure1",
    formats=("pdf", "svg", "png"),
    spec="nature",
    width="single",
    dpi=300,
)
```

## When to add export parameters

Only add more export controls when the task demands them:

- `spec` / `width` for venue-style export
- explicit SVG for vector-first downstream editing
- PNG for quick review or raster deliverables
- panel export when the user truly needs composite assembly
- `batch_export(...)` when the same figure needs several publication-style outputs

## Panel export branch

Use these only when multi-panel assembly is genuinely needed:

- `export_panel(...)`
- `export_panels(...)`

Do not default to panel export for single figures.

## Minimal recipe patterns

### Benchmark comparison

```python
fig = pf.grouped_scatter(values, category_names=category_names, group_names=model_names)
pf.save_figure(fig, "benchmark.pdf")
```

### Ablation

```python
fig = pf.dumbbell(baseline, improved, category_names=labels)
pf.save_figure(fig, "ablation.pdf")
```

### Calibration

```python
fig = pf.calibration(prob_true, prob_pred)
pf.save_figure(fig, "calibration.pdf")
```

### Forest plot

```python
fig = pf.forest_plot(effect, lower, upper, labels=labels, reference=1.0)
pf.save_figure(fig, "forest.pdf")
```

### Heatmap

```python
fig = pf.heatmap(matrix)
pf.save_figure(fig, "heatmap.pdf")
```
