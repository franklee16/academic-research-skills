# Chart Selection

## Task-to-chart mapping

| Communication task | Preferred forms | Notes |
|---|---|---|
| Benchmark comparison | grouped scatter, bar, companion table | use table when exact values matter most |
| Ablation | grouped comparison, dumbbell, compact table | keep the dimension count small |
| Calibration / evaluation | calibration, ROC, PR, Bland–Altman | choose what matches the evaluation claim |
| Distribution | box, violin, raincloud, histogram, density, ECDF, QQ | choose by whether shape or exact quantiles matter |
| Relationship | scatter, bubble, contour2d, hexbin | use hexbin/contour2d when overplotting is severe |
| Trend | line, area | line is usually the safer default |
| Diagnostic effect size | forest plot, volcano | match domain and inference style |
| Set/composition | UpSet, stacked ratio, donut, radial hierarchy | avoid decorative complexity unless it helps interpretation |
| Exact benchmark appendix | publication table | default to `pubtab` |

## Use X instead of Y

- Use **grouped scatter** or a **table** instead of a dense grouped bar when exact per-group values matter.
- Use **line** instead of bar for ordered progression over time or scale.
- Use **UpSet** instead of Venn-style thinking once the set count grows.
- Use **forest plot** instead of overloaded textual effect summaries.
- Use **table** instead of radar when precision and comparability matter more than shape.
- Use **hexbin** or **contour2d** instead of raw scatter when point overlap hides structure.
- Use **ECDF** when comparing cumulative distributions clearly is more important than showing a smoothed KDE.

## Anti-patterns

Avoid:

- pie/donut for exact quantitative comparison unless the composition story is primary and category count is small,
- radar for many categories or when axes are not semantically comparable,
- 3D effects,
- decorative color ramps without semantic purpose,
- overly dense legends that repeat axis information,
- mixed chart types that make the evidence harder to read,
- turning every result into a figure when a publication table would be cleaner.

## Selection heuristic

Ask in order:

1. What claim is the reader supposed to take away?
2. Does the reader need pattern perception or exact value lookup?
3. Are the groups ordered, categorical, repeated, hierarchical, or overlapping?
4. Is the result single-panel or likely part of a multi-panel figure?
5. Would a figure-only answer hide important exact values that should live in a table?
