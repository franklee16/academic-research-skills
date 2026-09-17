# Empirical Methods For Finance

Use this for asset pricing, corporate finance, banking, household finance, market microstructure, and accounting-adjacent finance methods.

## Required Inputs

Ask for:

1. finance subfield;
2. data source and access status;
3. sample filters, time period, frequency, and unit;
4. timing of variables, returns, events, filings, or accounting data;
5. model or design;
6. benchmarks/factors;
7. inference plan;
8. main economic interpretation.

## Finance-Specific Checks

- look-ahead bias;
- survivorship bias;
- delisting returns;
- CRSP/Compustat/CCM link rules;
- event windows and announcement timing;
- restatements and point-in-time data;
- factor model choice;
- multiple testing and factor-mining;
- transaction costs and implementability;
- clustering and correlation structure;
- household finance survey weights, imputation, and participation margins.

## Copy-Ready Instruction

```text
Act as a finance empirical methods adviser.

First ask me for the subfield, data source, access status, sample filters, frequency, unit of observation, timing rules, model or design, benchmarks, and inference plan if I have not provided them.

Draft or audit the empirical methods section using only supplied facts. Do not invent data screens, factors, event windows, robustness checks, results, or citations.

For long output, first return proposed structure and assumptions and wait for confirmation.

Include data construction, timing, model/design, inference, finance-specific bias checks, economic interpretation limits, and what must be verified against code and data.
```
