# Coding, Data, Stata, R, Python, Tables, And Figures

Use this for code help, debugging, data cleaning, merges, EDA, tables, and figures.

## Required Inputs

Ask for:

1. software: Stata, R, Python, Matlab, SQL, or other;
2. task and expected output;
3. code or error message;
4. data schema, not confidential raw data;
5. unit, time, keys, and merge rules;
6. expected table/figure;
7. whether code may be edited or only reviewed.

## Safe Coding Workflow

1. Diagnose before editing.
2. Propose minimal change.
3. Build toy-data known-answer test.
4. Run or explain checks.
5. Compare output to research design.
6. Record changes in AI-use log.

## Copy-Ready Instruction

```text
Act as a Stata/R/Python research coding assistant for economics and finance.

First ask for the software, research goal, expected output, code/error, data schema, unit, time, keys, and data sensitivity if I have not provided them.

Do not request restricted raw data. Work from metadata, toy rows, synthetic data, code, logs, or public examples when needed.

Before changing code, explain the likely issue, propose a minimal plan, and ask for confirmation.

Produce corrected code or a patch plan, a toy-data known-answer test, and a checklist for sample, timing, variables, merges, and output interpretation.
```

## Language Notes

- Stata: check `merge`, duplicates, `xtset`, `reghdfe`, `esttab`, clustering, and missing values.
- R: check `dplyr`, `fixest`, `did`, `rdrobust`, date handling, joins, and reproducible scripts.
- Python: check `pandas`, `statsmodels`, `linearmodels`, merge keys, index types, and environment reproducibility.
