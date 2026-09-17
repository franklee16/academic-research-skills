# Figures and Tables in Empirical Finance

## Table of Contents

1. [Tables](#tables)
2. [Figures](#figures)
3. [Captions](#captions)
4. [Finance-Specific Conventions](#finance-specific-conventions)

---

## Tables

### Formatting Rules

- Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`) -- never `\hline` or vertical rules
- Use `threeparttable` for tables with notes
- Report t-statistics in parentheses below coefficients, not p-values
- Significance stars: * p<0.10, ** p<0.05, *** p<0.01
- Consistent decimal places within a column
- Align numbers on the decimal point when possible

### Standard Finance Tables

| Table | Content | Standard Elements |
|-------|---------|-------------------|
| Table 1 | Summary statistics | Mean, SD, percentiles, N for all variables |
| Table 2 | Portfolio sorts | Returns/alphas by quintile, L/S spread, t-stats |
| Table 3 | Baseline regression | Coefficients, t-stats, R-squared, N, fixed effects |
| Table 4 | Heterogeneity / mechanism | Split by subgroups or interaction terms |
| Table 5 | Robustness | Alternative specifications, windows, controls |

### Table Notes

Every table must have notes. Include:
- What the table shows (one sentence)
- Variable definitions (if not obvious from headers)
- How standard errors are computed
- Significance level legend if using stars
- Sample size and period

**Example:**
> This table reports monthly returns (%) and alphas from portfolio sorts on DS Score. Quintile portfolios are formed monthly from April 2011 to December 2019. L/S is the long-short spread (Q5 - Q1). Alphas are estimated from the Fama-French five-factor model. t-statistics are in parentheses. Standard errors are Newey-West with 6 lags. * p<0.10, ** p<0.05, *** p<0.01.

### What Makes a Good Table

- **Self-contained**: A reader should understand the table from the caption and notes alone
- **Honest**: Report all specifications, not just the ones that work
- **Comparable**: Use the same sample and controls across specifications
- **Readable**: Do not cram too many panels or columns into one table

## Figures

### Creating Effective Figures

**Start with the question: What exactly should the reader take away from this figure?**

- Annotate graphs or emphasize the most important line/point
- Include axis titles and labels
- Font size for axis ticks and labels: at least as large as the paper text
- Use colorblind-friendly palettes
- Use vector formats (PDF) for line plots, not raster (PNG)

### Common Finance Figures

| Figure | Purpose | Best Format |
|--------|---------|-------------|
| Cumulative returns | Show portfolio performance over time | Line plot with two lines (L vs S) |
| Event study | Show dynamics around an event | Line plot with confidence bands |
| Coefficient plot | Show estimates across specifications | Dot-and-whisker plot |
| Bin scatter | Show binned relationship | Scatter with regression line |
| Histogram | Show distribution of key variable | Standard histogram with density |

### Color and Accessibility

- Default to colorblind-friendly palettes (viridis, Color Brewer)
- Use different line styles (solid, dashed, dotted) in addition to color
- Ensure figures work in grayscale (many referees print in B&W)
- For positive/negative data: use diverging color scales centered at zero

## Captions

**A good caption makes the figure/table self-contained.**

Include:
1. What is shown
2. The intended interpretation or takeaway
3. Key technical details (sample, units, methodology)

**Example caption:**
> Cumulative value-weighted returns of long-short portfolios sorted on DS Score. The long portfolio (Q5) buys stocks with the highest DS Score; the short portfolio (Q1) sells stocks with the lowest. The sample covers 3,799 A-share firms from April 2011 to December 2019. Cumulative VW return reaches 272% over the sample period.

### Figure Placement

- Put an eye-catching figure on the first page when possible
- Portfolio cumulative returns or main result visualization as Figure 1 is effective
- Place figures near the text that discusses them (inline, not float)

## Finance-Specific Conventions

### Portfolio Sort Tables

Standard layout:
- Rows: quintile portfolios (Q1 through Q5) and L/S spread
- Columns: raw return, CAPM alpha, FF3 alpha, FF5 alpha
- Each cell: point estimate with t-stat in parentheses below

### Regression Tables

Standard layout:
- Each column is a different specification
- Variables labeled in plain English, not code names
- Fixed effects indicated by "Yes" or "Firm FE", "Time FE"
- R-squared, N reported at bottom

### Return Attribution

When reporting portfolio returns:
- State whether returns are value-weighted (VW) or equal-weighted (EW)
- Report both raw returns and risk-adjusted alphas
- Report the factor model used for adjustment (CAPM, FF3, FF4, FF5)
- Annualize monthly returns when making comparisons: multiply by 12 for simple, compound for precise
