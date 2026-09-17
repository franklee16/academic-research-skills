# Source Problem

Status: Pending / Confirmed / Blocked

Theoretical Grounding Workspace: `{workspace-root}/theoretical-groundings/{field-slug}/`

Grounding Folder: `groundings/{question-slug}/`

Source Research Question Workspace: `{workspace-root}/research-questions/{field-slug}/`

Source Problem Reality Check Workspace: `{workspace-root}/research-question-checks/{field-slug}/`

## Theoretical Grounding Source Gate

Use this checked problem for the current Theoretical Grounding Workflow: Yes / No

Reason this problem is being theoretically grounded now:

- {User request, fragile motivation, proposal framing need, theory need, or other reason}

## Source Card Metadata

| Field | Value | Source |
| --- | --- | --- |
| Short Name | {Short name} | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Research Question | {Question} | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Contribution Type | {Type} | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Card Decision | keep / needs more evidence / defer | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Evidence Sufficiency | Sufficient / Needs more evidence / Thin | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` |
| Source Candidate Angle | {Angle title} | `{workspace-root}/research-questions/{field-slug}/candidate_angles.md` |
| Source Research Opportunity Candidate | {Opportunity title} | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` |

## Source Problem Reality Check

| Field | Value | Source |
| --- | --- | --- |
| Check Folder | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/` |  |
| Problem Reality Check Report | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/problem_reality_check.md` |  |
| Problem Reality Verdict | problem-solid / needs-evidence / motivation-fragile / reject | `problem_reality_check.md` |
| Report Complete? | Yes / No | `problem_reality_check.md` |
| Interrogation Transcript | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/interrogation_transcript.md` |  |

## Problem Claim Being Grounded

{Problem claim from the Problem Reality Check Report}

## Unsafe Motivation Claims To Preserve

| Claim To Avoid | Safer Replacement | Why It Matters For Grounding |
| --- | --- | --- |
| {Unsafe claim} | {Safer replacement} | {How this constrains theory-backed framing} |

## Targeted Evidence Needs From Problem Reality Check

| Evidence Need | Why It Matters | Recommended Next Skill | Relevance To Theory |
| --- | --- | --- | --- |
| {Need, or None} | {Verdict impact} | {Skill or workflow} | {Whether theory can reframe it or must preserve it} |

## Local Context To Review

| Artifact | Path | Found? | Why It Matters |
| --- | --- | --- | --- |
| Research Question Card | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` | Yes / No | Source question and claims |
| Problem Reality Check Report | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/problem_reality_check.md` | Yes / No | Verdict, fragilities, unsafe claims |
| Interrogation Transcript | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/interrogation_transcript.md` | Yes / No | User-confirmed judgments |
| Research Question Summary | `{workspace-root}/research-questions/{field-slug}/research_question_cards.md` | Yes / No | Cross-card context |
| Candidate Angles | `{workspace-root}/research-questions/{field-slug}/candidate_angles.md` | Yes / No | Source angle and risks |
| Writing Intent | `{workspace-root}/research-questions/{field-slug}/writing_intent.md` | Yes / No | Target framing and constraints |
| Research Opportunities | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` | Yes / No | Source gap |
| Research Clusters | `{workspace-root}/field-maps/{field-slug}/research_clusters.md` | Yes / No | Field-level context |

## Verdict Handling Decision

| Problem Reality Verdict | Grounding Action |
| --- | --- |
| problem-solid | Continue to final grounding |
| needs-evidence | Continue, mark affected claims provisional |
| motivation-fragile | Continue, preserve unresolved fragilities |
| reject | Stop; do not create Theoretical Pillars |

Selected action for this run:

- {Action and rationale}

## Routing Decision

Theoretical Grounding Source Gate passed: Yes / No

Decision rationale:

- {Why this is exactly one checked Research Question Card, or what blocks the gate}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial source problem record | Created for Theoretical Grounding Workflow |
