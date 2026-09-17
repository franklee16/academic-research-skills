---
name: data-analysis-router
description: Multi-domain data analysis router for uploaded datasets, spreadsheets, CSV/XLSX files, business metric tables, or user questions that require selecting the right business analysis framework before producing insights, charts, recommendations, or a structured report. Use when Codex needs to inspect data fields, infer the business domain, profile one or more tables, choose among ecommerce, content operation, advertising, store operation, finance, user feedback, or general analysis frameworks, and explain the reasoning behind the selected framework.
---

# Data Analysis Router

## Overview

Use this skill to analyze business data by first identifying the likely domain, then applying the matching framework. Prefer explicit domain reasoning over jumping straight into calculations.

## Workflow

1. Inspect the user request, attached files, filenames, sheet names, field names, and visible sample rows.
2. If a dataset is available and profiling would help, run `scripts/profile_dataset.py` on all relevant `.csv` and `.xlsx` files.
3. Read `references/routing-rules.md` to choose the likely domain.
4. If one domain clearly matches, read only that domain reference plus `references/report-format.md`.
5. If multiple domains plausibly match, state the ambiguity, read the relevant domain references, and combine the frameworks.
6. If no domain is clear, read `references/general-analysis.md` and `references/report-format.md`.
7. Produce a structured report with domain judgment, evidence, metrics, findings, chart suggestions, action recommendations, and missing data.

## Dataset Profiling

Use the profiler when the user provides actual files or asks for analysis grounded in table structure:

```bash
python3 scripts/profile_dataset.py path/to/file.csv path/to/workbook.xlsx
```

The profiler supports multiple files, CSV files, and multi-sheet Excel workbooks without extra Python packages. Use its output to identify field types, candidate IDs, text columns, time columns, numeric metrics, sheet/table roles, and likely join keys. Do not treat inferred joins as proven relationships unless the data dictionary or user confirms them.

## Reference Selection

- `references/routing-rules.md`: Always read before selecting a domain unless the user explicitly specifies the domain.
- `references/general-analysis.md`: Read when no domain is clear or the user asks for generic exploratory analysis.
- `references/ecommerce.md`: Read for orders, products, users, traffic, GMV, refunds, conversion, repurchase, SKU, or marketplace/storefront data.
- `references/content-operation.md`: Read for posts, videos, notes, articles, exposure, likes, saves, comments, shares, followers, completion, or creator/account data.
- `references/advertising.md`: Read for campaigns, ad groups, creatives, spend, impressions, clicks, CTR, CVR, CPA, CPM, ROI, or ROAS.
- `references/store-operation.md`: Read for physical stores, branches, sales, traffic, members, shifts, table turnover, time periods, or offline retail/restaurant data.
- `references/finance.md`: Read for revenue, cost, gross profit, net profit, expenses, cash flow, budget, or P&L data.
- `references/user-feedback.md`: Read for reviews, ratings, complaints, support records, surveys, comments, sentiment, VOC, defects, or text feedback.
- `references/report-format.md`: Read before final reporting.

## Analysis Rules

- Separate observed facts from inferred business meaning.
- Name the selected framework and explain why it fits.
- When data is insufficient for a metric, say what fields are missing instead of inventing the metric.
- For multi-table data, identify each table's likely role before recommending joins or metrics.
- Prioritize decision-useful findings over exhaustive statistics.
- Include chart suggestions only when they match available fields.
- Flag conclusions that require more data, attribution logic, or business context.

## Output Requirements

Use the report structure from `references/report-format.md`. Keep the final answer concise when the user wants direction, and more detailed when the user asks for a full analysis report.
