# Mature Evidence Ledger - 2026-06-02

This ledger records the evidence for the Mature threshold. It separates author-coordinated independent fresh-session evidence from non-author user or reviewer evidence.

## Current Decision

Status: **Mature evidence gate satisfied under the public-external-reviewer alternative**.

What is now satisfied:

- At least 15 recorded real-material or independent fresh-session cases are present.
- The cases span at least 5 fields.
- 3 public external reviewer-feedback cases are verified.

What is not yet satisfied:

- Direct user-adoption evidence is still separate from this public-reviewer evidence.

## Counted Case Ledger

| ID | Field | Case type | Origin | Result | Evidence |
|---|---|---|---|---|---|
| S1 | Social science / urban health | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S2 | Ecology / soil biogeochemistry | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S3 | AI4Science | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S4 | Biomedical research | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S5 | Social science | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S6 | Remote sensing | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S7 | Materials science | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S8 | Social science / finance | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| S9 | Source-depth behavior | Regression fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R1 | Ecology | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R2 | Remote sensing | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R3 | AI4Science | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R4 | Social science | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R5 | Biomedical research | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| R6 | Earth system science | Real-material fresh session | Author-coordinated independent agent | Pass | `evals/fresh-session-run-2026-06-02.md` |
| E1 | Meta-research | Public external reviewer feedback | External reviewer record | Pass | `evals/public-external-feedback-cases.md` |
| E2 | Microbiology / cell biology | Public external reviewer feedback | External reviewer record | Pass | `evals/public-external-feedback-cases.md` |
| E3 | Neuroscience | Public external reviewer feedback | External reviewer record | Pass | `evals/public-external-feedback-cases.md` |

## External User Or Reviewer Evidence

Three public external reviewer cases are verified in `evals/public-external-feedback-cases.md`.

These cases count as reviewer evidence, not direct user-trial evidence.

To count here, a case must include:

- who supplied or reviewed the material, using a privacy-preserving label if needed;
- the user's field and task;
- the prompt or paraphrased material used;
- whether the user chose a template without extra coaching;
- the output result: Pass, Partial, or Fail;
- the strongest useful move and the biggest miss;
- any change made afterward.

Do not convert author-created prompts, author-scored runs, or simulated reviewers into external evidence. Public reviewer records may count only when they include linkable third-party feedback and author-side revision signals.

## Mature Gate

Run:

```powershell
.\scripts\validate-mature.ps1
```

Expected status on 2026-06-02: pass for the Mature evidence gate.
