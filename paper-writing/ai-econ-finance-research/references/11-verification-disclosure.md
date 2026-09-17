# Verification, Reproducibility, And Disclosure

Use this whenever an AI output might enter research notes, code, slides, papers, or replies.

## Verification Methods

| Output | Check |
| --- | --- |
| citation | DOI, journal page, author/year/title, source supports claim |
| literature claim | claim-source bank and closest-paper check |
| code | toy-data known-answer test and real-output audit |
| coefficient | sign, unit, magnitude, sample, timing, denominator |
| method prose | compare to code, data construction, estimand, inference |
| proof/model | algebra, limiting cases, equilibrium logic, assumptions |
| data access | provider terms, institution rules, confidentiality |
| slides | claim-to-evidence mapping and public-sharing permission |

## Copy-Ready Instruction

```text
Act as a verification and AI-use disclosure assistant for economics and finance research.

First ask what output needs verification, how it will be used, and what original sources, code, data, tables, policies, or materials are available.

Classify the output type. Identify the main risks. Give the minimum verification method. State acceptance, revision, or rejection criteria. Draft an AI-use log entry and disclosure note if needed.

Do not claim something is verified unless the relevant source, code, data, or policy has been checked.
```

## AI-Use Log Fields

- date;
- tool/model if known;
- task;
- inputs used;
- output accepted;
- human edits;
- files changed;
- checks run;
- remaining uncertainty;
- commit hash if relevant.
