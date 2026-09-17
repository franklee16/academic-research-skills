# Source Card

Status: Pending / Confirmed

Problem Reality Check Workspace: `{workspace-root}/research-question-checks/{field-slug}/`

Check Folder: `checks/{question-slug}/`

Source Research Question Workspace: `{workspace-root}/research-questions/{field-slug}/`

Source Research Question Card: `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md`

## Source Card Gate

Use this card for the current Problem Reality Check: Yes / No

Reason this card is being checked now:

- {User request, fragile motivation, high-priority card, evidence concern, or other reason}

## Card Metadata

| Field | Value | Source |
| --- | --- | --- |
| Short Name | {Short name} | `cards/{question-slug}.md` |
| Research Question | {Question} | `cards/{question-slug}.md` |
| Contribution Type | {Type} | `cards/{question-slug}.md` |
| Card Decision | keep / needs more evidence / defer | `cards/{question-slug}.md` |
| Evidence Sufficiency | Sufficient / Needs more evidence / Thin | `cards/{question-slug}.md` |
| Source Candidate Angle | {Angle title} | `candidate_angles.md` |
| Source Research Opportunity Candidate | {Opportunity title} | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` |

## Linked Evidence Paths

| Evidence Item | Path | Evidence Role Claimed By Card | Found? | Notes |
| --- | --- | --- | --- | --- |
| {Paper or evidence title} | `{relative/path.md}` | {What the card says it supports} | Yes / No |  |

## Local Context To Review

| Artifact | Path | Found? | Why It Matters |
| --- | --- | --- | --- |
| Research Question Summary | `{workspace-root}/research-questions/{field-slug}/research_question_cards.md` | Yes / No | Card status and cross-card context |
| Candidate Angles | `{workspace-root}/research-questions/{field-slug}/candidate_angles.md` | Yes / No | Source angle and original risks |
| Writing Intent | `{workspace-root}/research-questions/{field-slug}/writing_intent.md` | Yes / No | Motivation fit and target framing |
| Research Opportunities | `{workspace-root}/field-maps/{field-slug}/research_opportunities.md` | Yes / No | Source problem gap |
| Research Clusters | `{workspace-root}/field-maps/{field-slug}/research_clusters.md` | Yes / No | Field-level grounding |

## Routing Decision

Source Card Gate passed: Yes / No

Decision rationale:

- {Why this is exactly one identifiable Research Question Card, or what blocks the gate}
