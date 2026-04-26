---
name: consistency-checker
description: Systematic pre-submission consistency audit for academic manuscripts in accounting/finance. Performs exhaustive checks across 10 categories: cross-references (tables, figures, equations, citations), table/figure consistency, variable definitions, sample sizes, methodology alignment, structural formatting, cross-document coherence, and common pitfalls. TRIGGER when: submitting to journal, responding to R&R, finalizing working paper, user mentions "consistency check", "pre-submission", "audit paper", "check my manuscript", or asks to verify cross-references before submission.
---

# Comprehensive Academic Manuscript Consistency Audit

## Overview

You are acting as a meticulous academic referee, technical editor, and production manager combined. Your task is to perform an exhaustive, line-by-line consistency and accuracy audit of all provided documents (main paper, response letter, online appendix).

**Critical principles:**
- Do not summarize the paper
- Do not assume correctness
- Do not skip any section, table, figure, footnote, or appendix
- Treat this as formal pre-submission quality control

## Input

Accept these documents:
- **Main paper** (LaTeX source preferred, PDF accepted)
- **Online appendix** (optional)
- **Response letter** (optional, for R&R)

## Workflow

1. **Extract structured data** using bundled scripts (for LaTeX)
2. **Process systematically** through each of the 10 audit categories
3. **Document every issue** with exact location and severity
4. **Generate structured report** with summary table

---

## 10 Audit Categories

### 1. Cross-Reference and Citation Audit

#### 1a. In-text references to tables
- Verify every table referenced exists and points to correct table
- Verify every table is referenced at least once
- Check text descriptions match actual table content (variable, column, sign, magnitude, significance)
- Flag vague references ("as shown in the table above")

#### 1b. In-text references to figures
- Every figure referenced must exist
- Every figure must be referenced
- Descriptions must match figure content
- Check axis labels, legends match text claims

#### 1c. In-text references to equations
- Verify every equation number referenced exists
- Check equation descriptions match actual content

#### 1d. References to sections, appendices, footnotes
- Verify all section cross-references
- Verify all appendix references
- Verify all footnote references

#### 1e. Bibliographic references
- Every citation appears in reference list
- Every reference entry is cited (flag orphan references)
- Verify citation formatting consistency (author names, year, "et al." rules)
- Check for common errors (wrong year, misspelled names)
- Flag "forthcoming"/"working paper" references for verification

---

### 2. Table Audit (ALL tables without exception)

#### 2a. Internal consistency
- Column headers, row labels, panel headers are clear
- Numbers are plausible (percentages 0-100, correlations -1 to 1, R² 0-1, N positive integer)
- Observation counts consistent across panels and with text
- Significance stars defined and consistent across tables
- Standard errors/t-statistics correctly labeled and formatted
- Decimal places consistent

#### 2b. Numbering and ordering
- Sequential, unique, correct ordering (Table 1, 2, 3...)
- Appendix tables follow consistent scheme (A1, A2... or OA.1, OA.2...)
- Tables appear in order first referenced

#### 2c. Table notes and footnotes
- Every symbol/abbreviation explained in table note
- Notes don't contradict text or other tables
- Sample/period/methodology descriptions consistent with text

#### 2d. Alignment with text descriptions
- Every text claim about table: correct sign, magnitude, significance, column, panel
- "Significant at 1%" matches stars shown
- Direction claims (increases/decreases) are correct

---

### 3. Figure Audit (ALL figures without exception)

- Figure numbers sequential, unique, correctly ordered
- Every figure has title/caption matching content
- Axis labels present, legible, correctly described
- Legends match data series shown
- Text claims about figures visually consistent
- Figure notes complete and consistent with text

---

### 4. Variable Definitions and Labels

#### 4a. Variable inventory
- Compile complete list of all variables (text, tables, figures, appendices, footnotes)
- Record: name, definition location, all appearance locations

#### 4b. Consistency checks
- Each variable defined at least once clearly
- Variable names used identically across all sections (no silent renaming, pluralization changes, notation drift)
- Flag undefined variables or defined-but-unused variables
- Variable definitions table covers all regression variables

---

### 5. Sample and Data Consistency

- Sample period stated consistently throughout
- Sample size consistent (text says N=45,320, tables show same or explained subset)
- Subsample descriptions and sizes consistent
- Data source descriptions consistent (Compustat/CRSP/IBES)
- Sample filters described consistently, resulting sizes make sense

---

### 6. Methodology and Econometric Consistency

- Empirical model in text matches equation form
- Control variables in text match tables
- Fixed effects in text match table rows (Industry FE: Yes, Year FE: Yes)
- Standard error clustering stated consistently in table notes
- Robustness tests in text appear in tables and vice versa

---

### 7. Structural and Formatting Checks

#### 7a. Section and heading structure
- Section numbering sequential (no gaps, duplicates)
- Roadmap paragraph matches actual structure

#### 7b. Footnotes and endnotes
- Footnote numbers sequential and unique
- Footnotes don't contain information belonging in main text
- Footnotes don't contradict main text

#### 7c. Formatting consistency
- Consistent fonts, bold, italics, spacing
- Consistent number formatting (thousands separator, decimal separator)
- Consistent abbreviations (e.g., vs. for example)
- All parentheticals, quotation marks, brackets properly closed

---

### 8. Cross-Document Consistency (CRITICAL)

Applies when multiple documents provided.

#### 8a. Main paper ↔ Online appendix
- Every reference to appendix points to existing element
- Every appendix element referenced from main paper
- Variable definitions, sample descriptions consistent
- Results discussed in both are consistent

#### 8b. Main paper ↔ Response letter
- Changes promised in response letter reflected in paper
- References to tables/figures/sections in response letter are correct
- Flag unfulfilled promises
- New analyses properly integrated

#### 8c. Online appendix ↔ Response letter
- New appendix items referenced in response letter exist

---

### 9. Language and Clarity Checks (Accounting/Finance Specific)

- Correct terminology (earnings management vs. manipulation, accruals vs. accrual)
- Consistent accounting standards references (IFRS vs. IAS, ASC 606 vs. revenue standard)
- Flag overstated claims (causality when method supports only association)
- Hedging language consistency for similar results

---

### 10. Common Pitfalls Checklist

Specifically check these frequently occurring errors:

- **Off-by-one table references** (very common after reordering)
- **Copy-paste errors** (paragraph describes Table 3 but copied from Table 2)
- **Mismatched significance levels** (text says 1%, stars show 5%)
- **Sample sizes don't add up** (subsamples should sum to full sample)
- **Control variables mismatch** (text lists controls not in table, or vice versa)
- **Inconsistent rounding** (0.034 in text, 0.0341 in table)
- **Orphan references** (cited but not in bibliography, or in bibliography but never cited)
- **Mismatched citation formats**
- **Tables without clearly stated dependent variable**
- **Appendix numbering scheme mismatch** (Table A3 in text, Table A.3 in appendix)

---

## Output Format

### Section-by-Section Report

Organize findings by the 10 categories above. Within each section:

```
**Issue Found:**
- Location: [page, section, table/figure number, column/row]
- Quoted text/element: "..."
- Problem: [precise explanation]
- Severity: [🔴 Major / 🟡 Medium / 🟢 Minor]

**If no issues in category:**
"✓ Checked — no issues detected."
```

### Severity Guidelines

| Severity | Criteria |
|----------|----------|
| 🔴 Major | Factual errors, contradictions, wrong references, missing elements |
| 🟡 Medium | Ambiguities, inconsistencies that could confuse readers |
| 🟢 Minor | Typos, formatting inconsistencies, stylistic irregularities |

### Summary Table

At the end, provide:

| Issue # | Location | Category | Severity | Description |
|---------|----------|----------|----------|-------------|
| 1 | Table 3, Col 2 | Table Audit | 🔴 Major | N=15,432 implausible for sample size stated in text (45,320) |
| 2 | p.12, ln.4 | Citations | 🟡 Medium | Smith (2020) cited but not in bibliography |
| ... | ... | ... | ... | ... |

Sort by severity (Major first), then by location.

---

## Using Extraction Scripts

For LaTeX manuscripts, run the bundled extraction scripts first:

```bash
python scripts/latex_extractor.py <main.tex> [--appendix appendix.tex]
python scripts/crossref_validator.py <main.tex> <references.bib>
```

This produces structured JSON with:
- All `\label{}` and `\ref{}` pairs
- Table environments and content
- Figure environments
- Citation keys
- Section structure

Use this data to ground your audit in precise extraction.

---

## Accounting/Finance Terminology Reference

| Check | Correct Usage | Common Errors |
|-------|---------------|---------------|
| Earnings management | "earnings management" | ❌ "earnings manipulation" (different connotation) |
| Accruals | "accruals" (plural) | ❌ "accrual" (singular when referring to the concept) |
| Discretionary | "discretionary accruals" | ❌ "non-discretionary" (check context) |
| IFRS/IAS | Consistent usage throughout | ❌ Mixing IFRS and IAS without clarification |
| Return vs. Returns | Consistent throughout paper | ❌ "Return" in one section, "Returns" in another |
| ROA/ROE | Define at first use, use consistently | ❌ ROA, Roa, roa in same paper |

---

## Final Instructions

Work slowly and carefully. Go through every single element. Precision and completeness are more important than speed. When in doubt, flag it for author verification.
