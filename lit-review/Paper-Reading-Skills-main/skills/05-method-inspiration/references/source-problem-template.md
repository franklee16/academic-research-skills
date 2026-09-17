# Source Problem

Status: Pending / Confirmed / Blocked

Method Inspiration Workspace: `{workspace-root}/method-inspirations/{field-slug}/`

Inspiration Folder: `inspirations/{problem-slug}/`

## Method Inspiration Source Gate

Use this source for the current Method Inspiration Workflow: Yes / No

Source type: Research Question Card / Source Problem Brief

Reason method inspiration is being run now:

- {User request, method-design stage, proposal need, or other reason}

Candidate Methods from this source should be marked provisional: Yes / No

## Source Metadata

| Field | Value | Source |
| --- | --- | --- |
| Short Name | {Short name} | `{path or user-provided brief}` |
| Problem Statement Or Research Question | {Problem or question} | `{path or brief}` |
| Contribution Type | {Type, if available} | `{path or brief}` |
| Source Decision | keep / needs more evidence / defer / brief-only | `{path or brief}` |
| Evidence Status | sufficient / needs-evidence / thin / unknown | `{path or brief}` |
| Target Failure | {Failure the method should address} | `{path or brief}` |
| Intended Intervention Point | {Where the method may intervene} | `{path or brief}` |
| Constraints | {Data, compute, deployment, interpretability, time, or other constraints} | `{path or brief}` |
| Non-Goals | {What the method should not try to solve} | `{path or brief}` |

## Source Research Question Card

Use when the source type is Research Question Card.

| Field | Value |
| --- | --- |
| Source Research Question Workspace | `{workspace-root}/research-questions/{field-slug}/` |
| Source Card Path | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Source Candidate Angle | `{workspace-root}/research-questions/{field-slug}/candidate_angles.md` |
| Source Research Opportunity | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` |

## Source Problem Brief

Use when no Research Question Card exists yet.

### Brief

{User-provided or agent-drafted source problem brief}

### Brief Completeness

| Required Field | Present? | Notes |
| --- | --- | --- |
| Target problem | Yes / No |  |
| Failure scenario | Yes / No |  |
| Intended intervention point | Yes / No |  |
| Constraints | Yes / No |  |
| Non-goals | Yes / No |  |
| Evidence status | Yes / No |  |

## Problem Reality Check Context

| Field | Value | Source |
| --- | --- | --- |
| Problem Reality Check Report | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/problem_reality_check.md` / None |  |
| Problem Reality Verdict | problem-solid / needs-evidence / motivation-fragile / reject / none |  |
| Unsafe Motivation Claims | {Summary or None} | `problem_reality_check.md` |
| Targeted Evidence Needs | {Summary or None} | `problem_reality_check.md` |

## Local Context To Review

| Artifact | Path | Found? | Why It Matters |
| --- | --- | --- | --- |
| Research Question Card | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` | Yes / No / N/A | Source question and method-relevant claims |
| Research Question Summary | `{workspace-root}/research-questions/{field-slug}/research_question_cards.md` | Yes / No / N/A | Card status and cross-card context |
| Candidate Angles | `{workspace-root}/research-questions/{field-slug}/candidate_angles.md` | Yes / No / N/A | Original contribution route and risks |
| Writing Intent | `{workspace-root}/research-questions/{field-slug}/writing_intent.md` | Yes / No / N/A | Practical constraints and priority |
| Problem Reality Check Report | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/problem_reality_check.md` | Yes / No / N/A | Verdict and fragilities |
| Research Opportunities | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` | Yes / No / N/A | Source gap |
| Research Clusters | `{workspace-root}/field-maps/{field-slug}/research_clusters.md` | Yes / No / N/A | Field-level context |

## Routing Decision

Method Inspiration Source Gate passed: Yes / No

Decision rationale:

- {Why this is exactly one identifiable source problem, or what blocks the gate}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial source problem record | Created for Method Inspiration Workflow |
