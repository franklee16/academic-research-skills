# General Analysis Framework

Use this framework when the data has no clear business domain, when the user asks for exploratory analysis, or when the dataset is too generic for a specialized module.

## Required Passes

1. Data overview: row count, column count, table/sheet roles, field types, and time range.
2. Data quality: missing values, duplicates, impossible values, outliers, inconsistent categories, and suspicious IDs.
3. Descriptive statistics: central tendency, distribution, top categories, and notable ranges.
4. Group comparison: compare key metrics across categories, segments, time periods, or entities.
5. Trend analysis: identify upward, downward, seasonal, cyclical, or volatile patterns.
6. Structure analysis: identify concentration, Pareto effects, contribution share, and long-tail patterns.
7. Correlation analysis: test relationships among numeric fields; avoid causal claims without evidence.
8. Exception analysis: isolate abnormal rows, periods, groups, or values and suggest possible causes.
9. Action recommendations: convert findings into next steps and validation needs.

## Metric Selection

- Choose one primary target metric when the user provides a goal.
- If no target is given, identify candidate target metrics from numeric fields and business language.
- Use time fields for trend charts and categorical fields for segmentation.
- For text fields, summarize themes, repeated phrases, and sentiment only if enough text exists.

## Chart Suggestions

- Time trend: line chart.
- Category comparison: bar chart.
- Composition: stacked bar or treemap.
- Contribution concentration: Pareto chart.
- Relationship between numeric fields: scatter plot.
- Distribution: histogram or box plot.
- Outliers: box plot plus filtered table.

## Cautions

- Do not overfit a business story to generic data.
- Do not imply causality from correlation.
- Do not calculate unavailable metrics; list missing fields instead.
