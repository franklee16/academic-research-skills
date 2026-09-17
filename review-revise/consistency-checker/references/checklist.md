# Consistency Check Quick Reference

## Pre-Submission Checklist

Use this checklist for a quick scan before running the full audit.

### 🔴 Critical Checks (Must Pass)

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | All `\ref{}` point to existing `\label{}` | Run `crossref_validator.py` |
| 2 | All `\cite{}` keys in bibliography | Run `crossref_validator.py --bib file.bib` |
| 3 | Table numbers sequential (1, 2, 3...) | Scan for gaps |
| 4 | Figure numbers sequential | Scan for gaps |
| 5 | N values in tables match text claims | Manual check |
| 6 | Significance stars defined in table notes | Check first table |
| 7 | Every table/figure referenced in text | Search "Table" and "Figure" |

### 🟡 Important Checks (Should Pass)

| # | Check | Common Issues |
|---|-------|---------------|
| 8 | Variable names consistent throughout | ROA vs Roa vs roa |
| 9 | Sample period stated consistently | "1990-2020" vs "1990 to 2020" |
| 10 | Control variables match text/tables | Text lists SIZE, table shows Size |
| 11 | Fixed effects match text/tables | "Industry FE" vs "Industry Fixed Effects" |
| 12 | Section numbers sequential | No gaps after reordering |
| 13 | Footnote numbers sequential | Check after deletions |

### 🟢 Polish Checks (Nice to Have)

| # | Check | What to Look For |
|---|-------|------------------|
| 14 | Decimal places consistent | 0.034 vs 0.0341 |
| 15 | Parentheses/brackets closed | Matching pairs |
| 16 | Abbreviations consistent | "e.g.," vs "for example" |
| 17 | Citation format consistent | et al. rules, ampersand vs "and" |

---

## Common Pitfalls

These errors occur frequently in accounting/finance papers:

### Off-by-One Table References
- **Cause:** Reordering tables during revision
- **Fix:** Search "Table X" and verify each reference

### Copy-Paste Errors
- **Cause:** Copying paragraph from Table 2 description to Table 3
- **Symptom:** Numbers don't match the actual table
- **Fix:** Read each table description against actual table

### Mismatched Significance
- **Cause:** Updating results but not text
- **Symptom:** Text says "significant at 1%" but table shows *
- **Fix:** Check every significance claim against table stars

### Orphan References
- **Cause:** Deleting citations but not bibliography entries
- **Symptom:** Bibliography has entries never cited
- **Fix:** Run crossref_validator.py

### Sample Size Mismatches
- **Cause:** Different subsample restrictions
- **Symptom:** Subsamples don't sum to total N
- **Fix:** Verify N values across all tables

---

## Script Commands

```bash
# Extract structured data from LaTeX
python scripts/latex_extractor.py main.tex --appendix appendix.tex -o extracted.json

# Validate cross-references
python scripts/crossref_validator.py main.tex --bib references.bib -o validation.json
```

---

## Output Interpretation

### Severity Levels

| Icon | Level | Meaning |
|------|-------|---------|
| 🔴 | Major | Factual error, contradiction, or missing element |
| 🟡 | Medium | Ambiguity or inconsistency that could confuse readers |
| 🟢 | Minor | Typo, formatting issue, or stylistic irregular |

### Priority Order

1. Fix all 🔴 Major issues before submission
2. Address 🟡 Medium issues if time permits
3. 🟢 Minor issues are optional polish

---

## Quick Verification Steps

1. **Run extraction script:** Get structured data
2. **Run validation script:** Find broken references
3. **Manual table check:** Verify N values and significance
4. **Read section by section:** Check variable naming
5. **Cross-document check:** If appendix/response letter exists

---

## Accounting/Finance Specific Checks

| Term | Correct Usage | Common Errors |
|------|---------------|---------------|
| Earnings management | "earnings management" | ❌ "earnings manipulation" |
| Accruals | "accruals" (plural) | ❌ "accrual" (when referring to concept) |
| Discretionary accruals | "discretionary" | ❌ "non-discretionary" (check context) |
| Return vs Returns | Consistent throughout | ❌ Mixed usage |
| ROA/ROE | Define once, use consistently | ❌ ROA, Roa, roa mixed |
