---
name: hbs-case-writer
description: Create Harvard Business School-style case studies on financial market events, products, or investment decisions. Use when the user wants to write a teaching case about a financial event, market phenomenon, investment product, or corporate decision. Triggers on requests like "write a case about X", "create an HBS case on Y", or "develop a teaching case for Z". Outputs immersive, decision-focused narratives with supporting exhibits and teaching notes.
---

# HBS Case Writer

Write Harvard Business School-style teaching cases on financial market events and investment decisions.

## Case Structure

Every case follows this architecture:

1. **Title & Header** — Case title, protagonist name/role, date, institution
2. **Opening Hook** — Start at the decision moment; protagonist faces a choice
3. **Background** — Industry context, market conditions, relevant history
4. **The Situation** — Specific events, data, and stakeholders involved
5. **Analysis Framework** — Information the reader needs to analyze (not the analysis itself)
6. **The Decision** — End with open questions; NO resolution

## Writing Principles

### Narrative Style
- Third-person limited (follow the protagonist)
- Present tense throughout
- Objective, journalistic tone — no judgments or conclusions
- Let facts and data tell the story
- Quote real sources when available

### What Makes It a Case (Not an Article)
- Ends with a decision point, never a resolution
- Presents conflicting information or trade-offs
- Reader must analyze, not just absorb
- Avoid teaching explicitly — immerse the reader instead
- Include just enough context; let exhibits carry data

### The Protagonist
- Name a specific person or team facing the decision
- Give them a role, organization, and stakes
- Show their thought process through action, not introspection
- They don't have to be heroic — real people with real constraints

## Data & Exhibits

### Required Elements
- Financial data tables (performance, valuations, market data)
- Charts where visual data tells the story better
- Timeline of key events
- Competitive landscape or peer comparisons

### Exhibit Standards
- Source all data (Bloomberg, SEC filings, company reports, etc.)
- Use clean, professional formatting
- Exhibit titles should be descriptive
- Number exhibits sequentially

## Figure Generation

Use the plotting script to create professional figures:

```bash
python scripts/case_plots.py
```

### Available Plot Types

| Function | Use Case | Example |
|----------|----------|---------|
| `plot_time_series` | Trends over time | Stock prices, deposits, rates |
| `plot_bar_chart` | Comparisons | Revenue by segment, market share |
| `plot_stacked_bar` | Composition | Asset allocation, cost breakdown |
| `plot_pie_chart` | Proportions | Deposit composition, market share |
| `plot_dual_axis` | Two metrics | Price and volume, rates and deposits |
| `plot_comparison_bars` | Peer comparison | SVB vs competitors |

### Figure Style

All figures use professional HBS-style formatting:
- Clean white background with subtle grid
- Bold titles and axis labels
- Professional color palette
- High DPI (300) for print quality
- No top/right spines

### Creating Figures

When writing a case, generate figures by:

1. **Identify key data** — What numbers tell the story?
2. **Choose plot type** — Time series for trends, bars for comparisons, pie for proportions
3. **Run the script** — Modify `case_plots.py` with your data
4. **Save to case folder** — Output to `{case_folder}/figures/`

### Example: SVB Case Figures

```python
# Figure 1: Deposit Growth
plot_time_series(
    dates=dates,
    values=deposits,
    title='SVB Total Deposits (2018-2022)',
    ylabel='Deposits ($ Billions)',
    filename='exhibit_deposits.png',
    show_values=True
)

# Figure 2: Uninsured Deposits
plot_pie_chart(
    labels=['Uninsured (>$250K)', 'Insured (<$250K)'],
    values=[94, 6],
    title='SVB Deposit Insurance Status',
    filename='exhibit_uninsured.png',
    colors=['#d62728', '#2ca02c']
)
```

## Financial Data Collection

When building a case, gather:

1. **Market Data** — Prices, volumes, volatility, correlations (Yahoo Finance, FRED, Bloomberg)
2. **Company Data** — Financial statements, SEC filings, earnings calls, investor presentations
3. **News & Analysis** — WSJ, FT, Bloomberg, CNBC coverage of the event
4. **Academic Context** — Relevant research papers on the topic
5. **Regulatory Context** — SEC actions, Fed statements, regulatory changes

Use web search tools to find current data. Document all sources for exhibits.

## Output Format

### Case Document
```
[Title]

[Protagonist Name] stared at [the screen/report/data]...

[Background sections]

[The Decision Point]

Exhibits follow on separate pages.
```

### Teaching Note (Optional)
Create when the case is complete:
- Learning objectives (2-4 specific takeaways)
- Discussion questions (3-5 questions to guide class)
- Suggested teaching plan (how to structure the discussion)
- Key analysis points (what students should identify)

## Workflow

When given a financial event/product:

1. **Research Phase**
   - Identify the key decision and protagonist
   - Gather market data, news, and financials
   - Find academic or analytical context

2. **Outline Phase**
   - Map the narrative arc
   - Identify required exhibits
   - Determine the decision point

3. **Writing Phase**
   - Draft sections in order (hook → background → situation → decision)
   - Create exhibits with sourced data
   - Write teaching note if requested

4. **Review Phase**
   - Check against HBS style principles
   - Verify all data is sourced
   - Ensure decision point is clear and unresolved

## References

- [hbs-patterns.md](references/hbs-patterns.md) — Detailed patterns from real HBS cases
- [financial-data-sources.md](references/financial-data-sources.md) — Where to find financial data
