# Citation Verification

## Purpose

Mode E verifies whether references exist, whether their metadata are accurate, whether they are safe to cite, and whether they support the manuscript claims attached to them. It is a citation and evidence gate, not a general summary mode.

The mode is stricter than normal proofreading. It treats every literature claim, gap claim, novelty claim, theory claim, equilibrium claim, method claim, numerical claim, table claim and figure claim as something that must be traceable to a source, to the manuscript, to an appendix, to proof material, or to simulation output.

## Core principle

Do not verify while extracting. Do not extract while verifying.

Use two separate passes.

```text
Pass 1. Claim extraction only.
Pass 2. Evidence verification only.
```

This prevents the system from discovering new claims halfway through the audit and losing traceability.

## Scope options

Mode E can be run on different scopes.

```text
Full manuscript
Introduction only
Related work only
Discussion only
Limitations only
Reference list only
Tables and figures only
Appendix or online supplement only
Response letter only
Fixed source corpus only
```

If the user provides a fixed corpus, use source-only verification. Do not use external knowledge to silently support claims that are not in the corpus.

## Verification layers

### E0. Scope lock

Record the manuscript version, the sections being checked, the source corpus, and whether external search is allowed. If the user edits the manuscript after Pass 1, repeat Pass 1 for the edited sections.

### E1. Claim extraction

Extract all claims that need citation, source support, internal manuscript support, proof support, table support, figure support, or code support.

Use the claim extraction protocol in `references/23-claim-extraction-protocol.md`.

### E2. Metadata verification

Check each cited work.

```text
Author names
Year
Title
Journal or venue
Volume
Issue
Pages or article number
DOI
Publisher
Published version versus working paper version
Conference version versus journal version
```

Do not fabricate missing metadata. Mark it as unresolved.

### E3. Retraction and correction verification

Check for visible publication risks.

```text
Retraction
Expression of concern
Corrigendum
Publisher note
Withdrawn preprint
Superseded working paper
Duplicate publication risk
Hijacked journal risk
```

If the status cannot be confirmed, report the limitation rather than treating the citation as safe.

### E4. Venue identity and journal-level verification

Check whether the venue is what the manuscript implies it is. Use the embedded ABS AJG 2024 database when ABS 4*, 4 or 3 status matters.

Do not infer prestige from a journal name. Verify the venue identity.

### E5. Claim and citation support verification

For every extracted claim, decide whether the cited source supports the exact manuscript wording.

Use the evidence gate in `references/24-claim-citation-evidence-gate.md`.

The central question is simple. Does this source support this sentence at the strength used in the manuscript?

### E6. Numerical, table and figure verification

Check all numbers, units, signs, percentages, percentage points, parameter values, simulation statistics, table values, figure captions and claims about charts.

Use `references/25-numerical-and-table-verification.md`.

### E7. Source-only verification

When the user says to use only uploaded materials, fixed PDFs, a BibTeX file, a reference list, paper notes or a closed corpus, use source-only verification.

Use `references/26-source-only-verification.md`.

### E8. Final safety verdict

End every full Mode E audit with one of these verdicts.

```text
PASS
PASS WITH MINOR FIXES
MAJOR REPAIR REQUIRED
UNSAFE FOR SUBMISSION
```

## Academic status labels

Use these labels consistently.

| Status | Meaning |
|---|---|
| Verified | The source exists and clearly supports the claim. |
| Verified with rounding | The number is correctly rounded and the rounding does not alter interpretation. |
| Metadata verified only | The source exists, but full-text support has not been verified. |
| Partially supported | The source supports a weaker version of the claim. |
| Misleading | The source is used selectively or without an important boundary condition. |
| Overclaimed | The manuscript wording is stronger than the source allows. |
| Citation not found | The cited work could not be located. |
| Wrong version risk | A working paper, conference paper, accepted manuscript or journal version may differ. |
| Numerical error | A number, unit, sign, rounding, percentage, percentage point or magnitude is wrong. |
| Not in corpus | The claim is not traceable in source-only mode. |
| Contradicted | The source conflicts with the manuscript claim. |
| Manual check required | Paywall, scanned PDF, complex proof, formula, figure or table requires human inspection. |

## High-risk manuscript claims

Treat these as high risk by default.

```text
First paper to...
Few studies have...
No prior work examines...
The literature has primarily focused on...
This stream assumes...
Prior work shows that...
X always increases Y.
The effect is robust.
The numerical experiments validate...
The model proves empirical relevance.
The closest paper is different because...
```

Weaken unsupported claims rather than searching for a citation that merely appears convenient.

## Output table

| Claim ID | Manuscript claim | Location | Citation or evidence | Status | Risk | Required action |
|---|---|---|---|---|---|---|

## Strict rules

1. Never invent a source, DOI, page number, quote, proof result or data value.
2. Never treat simulation as real-world empirical evidence unless it uses observed data.
3. Never treat a citation as verified merely because the title sounds relevant.
4. Never hide uncertainty. Mark unresolved evidence explicitly.
5. If the manuscript wording is stronger than the source, recommend a weaker sentence.
