# Mode Router

## Purpose

Classify the user's request before doing literature work. Do not default to writing a related work section. Most literature tasks are decision tasks, not writing tasks.

## Mode triggers

Mode 0 is for strategic choices before a project starts. Use it for decisions about whether to enter a field, whether a topic is too crowded, whether to aim for a top journal, or whether the user should build a working paper first.

Mode A is for exploration. The user has keywords, a broad field, or a vague curiosity but no concrete mechanism or research question.

Mode B is for idea validation. The user has a rough mechanism, model, setting, proposition, algorithm or claim, and wants to know whether it is worth doing.

Mode C is for project foundation. The research question has been selected and needs a defensible literature tree, critical discussion and predecessor map.

Mode D is for manuscript support. The user is drafting introduction, related work, discussion, limitations, reviewer response or contribution language.

Mode E is for citation verification. The user needs pre-submission checking of reference existence, metadata, retraction status and whether each cited paper supports the sentence that cites it.

Mode F is for rolling updates. Use it when the paper framing changes, a project resumes after a pause, or a new submission cycle begins.

Mode G is for reviewer attack and literature defence. Use it when the user wants missing-citation risks, closest-predecessor attacks, or referee-style objections.

Mode H is for journal-specific positioning. Use it when the same paper may be framed for different disciplinary communities, such as management, economics, finance, marketing, operations, information systems, computer science, engineering, public policy, health, education, social science or interdisciplinary outlets.

Mode I is for systematic survey or review paper work. Use it when the user needs search protocol, inclusion and exclusion criteria, screening records and coding schemes.

Mode J is for theory-only gap viability. Use it when the user has no real data and wants to know whether a gap can be attacked with formal modelling, proofs, simulation or numerical experiments.

## Multi-mode requests

If the request clearly requires several modes, do not ask for unnecessary clarification. Run a bundled workflow.

Common bundles include these.

```text
A plus B, for exploration that rapidly validates candidate ideas.
B plus J, for a pure theory idea under no-data constraints.
C plus D, for project foundation and manuscript drafting.
D plus E, for related work writing and citation checking.
F plus G, for resubmission or revision defence.
H plus D, for target-journal rewriting.
```

## Minimum output by mode

Mode 0 must produce a strategic verdict.
Mode A must produce candidate topic clusters and reading priorities.
Mode B must produce collision risk, framework-difference test and ROI verdict.
Mode C must produce literature tree and critical gap matrix.
Mode D must produce manuscript-ready material or a source pack.
Mode E must produce a verification table and unresolved-risk list.
Mode F must produce new-paper risk and old-claim revision needs.
Mode G must produce reviewer attacks and defence strategy.
Mode H must produce target-journal literature priorities.
Mode I must produce a search protocol.
Mode J must produce no-data viability and evidence substitutes.


## Mode E evidence-gate expansion

Mode E must use a two-pass protocol when checking manuscript claims.

```text
Pass 1 extracts claims only.
Pass 2 verifies extracted claims only.
```

For Mode E, activate Citation Verification Agent, Claim Extraction Agent, Evidence Gate Agent, Numerical and Table Verification Agent, Source-Only Verification Agent when a fixed corpus is provided, Red Team Literature Reviewer Agent for high-risk gap or novelty claims, and Integration Editor Agent.

Mode E must end with one of these verdicts.

```text
PASS
PASS WITH MINOR FIXES
MAJOR REPAIR REQUIRED
UNSAFE FOR SUBMISSION
```
