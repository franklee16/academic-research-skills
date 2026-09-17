# Source Research Question Checks

Status: Draft / Confirmed

Theoretical Grounding Workspace: `{workspace-root}/theoretical-groundings/{field-slug}/`

Source Research Question Workspace: `{workspace-root}/research-questions/{field-slug}/`

Source Problem Reality Check Workspace: `{workspace-root}/research-question-checks/{field-slug}/`

## Source Workspaces

| Artifact | Path | Found? | Notes |
| --- | --- | --- | --- |
| Research Question Workspace | `{workspace-root}/research-questions/{field-slug}/` | Yes / No |  |
| Research Question Cards Summary | `{workspace-root}/research-questions/{field-slug}/research_question_cards.md` | Yes / No |  |
| Problem Reality Check Workspace | `{workspace-root}/research-question-checks/{field-slug}/` | Yes / No |  |
| Problem Reality Check Summary | `{workspace-root}/research-question-checks/{field-slug}/problem_reality_checks.md` | Yes / No |  |
| Source Field Map Workspace | `{workspace-root}/field-maps/{field-slug}/` | Yes / No |  |

## Checked Research Question Cards Available For Grounding

The Theoretical Grounding Workflow may ground exactly one checked card per run.

| Card | Research Question Card | Problem Reality Verdict | Check Report | Check Complete? | Eligible For Grounding? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| {Short Name} | `{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md` | problem-solid / needs-evidence / motivation-fragile / reject | `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/problem_reality_check.md` | Yes / No | Yes / No | {Reason} |

## Routing Notes

- {Which checked card was selected, or why selection is blocked}
- {Any missing source artifact}
- {Any verdict-specific handling that matters before grounding}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial source check summary | Created for Theoretical Grounding Workspace |
