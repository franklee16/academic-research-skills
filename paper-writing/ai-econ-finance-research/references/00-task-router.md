# Task Router And Project Setup

Use this reference when the user is unsure where to begin or wants to use the skill in a real research project.

## First Classification

Ask for only what is missing:

1. research stage: idea, literature, data, coding, methods, writing, revision, presentation, teaching, or replication;
2. field: economics, finance, or both;
3. output wanted: questions, checklist, prose, code, slide plan, agent setup, or resource list;
4. material status: public, licensed, restricted, confidential, unpublished, coauthored, student-related, or unknown;
5. tool mode: chat, project, coding agent, GitHub workflow, or unknown.

## Route

| If the user wants... | Load |
| --- | --- |
| concepts and risks | `01-handbook-core-concepts.md` |
| a copy-ready instruction | `02-skills-index.md` |
| literature review | `03-literature-review.md` |
| writing, revision, referee response | `04-writing-revision-referee.md` |
| economics empirical methods | `05-empirical-methods-economics.md` |
| finance empirical methods | `06-empirical-methods-finance.md` |
| code, data, tables, figures | `07-coding-data-stata-r-python.md` |
| Git, GitHub, agents, collaboration | `08-agentic-workflows-git-github.md` |
| datasets, household finance, Nordic data | `09-datasets-access-confidentiality.md` |
| slides, talk practice, teaching | `10-slides-teaching-websites.md` |
| verification, disclosure | `11-verification-disclosure.md` |
| examples and failures | `12-examples-failure-cases.md` |
| Chinese workflow | `13-chinese-router.md` |

## Step-By-Step Research Project Setup

Guide the user through this sequence:

1. Create one AI project/workspace for the paper.
2. Paste `SKILL.md` into project instructions.
3. Add only the reference files needed for the current research stage.
4. Add safe project materials: abstract, outline, public links, non-confidential notes, data dictionary, toy data, or code snippets.
5. Do not upload restricted data, licensed extracts, private coauthor notes, referee material, student data, raw microdata, or proprietary information unless rules and consent allow it.
6. Ask the AI to classify the task and missing inputs.
7. Confirm structure before long output.
8. Verify output.
9. Record accepted use in `AI-USE-LOG.md`.
10. If files or code are changed, inspect diff, run checks, commit, and push.

## Default Output Contract

End every serious response with:

```text
What I produced:
What I did not change:
What you must verify:
Questions for you:
```
