# Method Candidate Library: {Short Name}

Status: Final / Provisional

Method Inspiration Workspace: `{workspace-root}/method-inspirations/{field-slug}/`

Inspiration Folder: `inspirations/{problem-slug}/`

Source Problem: `source_problem.md`

This library contains Candidate Methods for inspiration. It does not contain a Committed Method Design.

## Source Problem And Evidence Status

Source type: Research Question Card / Source Problem Brief

Problem statement:

- {Problem or research question}

Evidence status:

- sufficient / needs-evidence / thin / unknown

Problem Reality Verdict, if available:

- problem-solid / needs-evidence / motivation-fragile / reject / none

Provisional library: Yes / No

Reason:

- {Why final or provisional}

## Method Needs

| Method Need | Target Failure | Required Capability | Success Signal | Evidence Status |
| --- | --- | --- | --- | --- |
| MN-1 | {Failure} | {Capability} | {Signal} | supported / plausible / assumed / needs-evidence |

Method Needs confirmed or delegated: Yes / No

## Targeted Method Search Coverage

| Method Need | Same-Problem Coverage | Adjacent Coverage | Far-Analogy Coverage | Search Status | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| MN-1 | found / gap recorded | found / thin / missing | found / none found / missing | sufficient / needs-search | {Gap or None} |

## Selected Method Patterns

| Pattern | Method Need | Source Paper Type | Source Paper | Source URL | Transferable Unit | Evidence Strength | Assembly Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MP-1 | MN-1 | Same-Problem / Adjacent-Problem / Far-Analogy | {Paper} | {URL} | {Unit} | strong / moderate / weak / unknown | {Role} |

## Deferred And Rejected Patterns

| Pattern | Source Paper | Source URL | Disposition | Reason | Reconsider If |
| --- | --- | --- | --- | --- | --- |
| MP-2 | {Paper} | {URL} | deferred / rejected / needs search | {Reason} | {Condition} |

## Candidate Methods

### CM-1: {Candidate Method Name}

Method thesis:

- {Thesis}

Covered Method Needs:

- {Needs}

Inputs / modules / outputs:

- Inputs: {Inputs}
- Modules: {Modules}
- Outputs: {Outputs}

Training or inference flow:

1. {Step}
2. {Step}
3. {Step}

Source papers by role:

| Assembly Role | Pattern | Source Paper | Source URL |
| --- | --- | --- | --- |
| {Role} | MP-1 | {Paper} | {URL} |

Novelty hypothesis:

- {Hypothesis}

Weakest link:

- {Weakest link}

Feasibility:

- {Data, engineering, compute, or time feasibility}

Experiment implications:

- {Light downstream hint}

Status:

- promising / risky / too-expensive / needs-search

## Cross-Candidate Comparison

| Candidate Method | Main Strength | Main Weakness | Best Use Case | Main Follow-Up |
| --- | --- | --- | --- | --- |
| CM-1 | {Strength} | {Weakness} | {Use case} | experiment-design / research-framing / method-commitment / none |

## Downstream Routing Hints

These are hints only. Later workflows should use a Committed Method Design, not an uncommitted Candidate Method, as their main source.

| Follow-Up Need | Recommended Workflow | Trigger |
| --- | --- | --- |
| Turn inspiration into an owned method design | paper-reading-method-commitment | User is ready to commit after reflection |
| Design validation, baselines, and metrics | paper-reading-experiment-design | A Committed Method Design exists and claims need measurement |
| Clarify novelty | paper-reading-research-framing | Close-work risk remains high |
| Attack assumptions | paper-reading-experiment-design | Weak links need claim/evidence, baseline, or ablation pressure testing |

## Stop Condition Check

| Required Item | Met? | Notes |
| --- | --- | --- |
| Method Inspiration Source Gate passed | Yes / No |  |
| Method Need Decomposition confirmed or delegated | Yes / No |  |
| Targeted Method Search attempted or marked unavailable/deferred | Yes / No |  |
| Method Search Sufficiency checked | Yes / No |  |
| Method Patterns include source URLs | Yes / No |  |
| Transfer Mapping completed | Yes / No |  |
| Method Pattern Dispositions recorded | Yes / No |  |
| 3-5 Candidate Methods confirmed or delegated | Yes / No |  |
| Deferred and rejected patterns preserved | Yes / No |  |
| No Committed Method Design forced | Yes / No |  |

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Method Candidate Library | Created after Candidate Methods were confirmed or delegated |
