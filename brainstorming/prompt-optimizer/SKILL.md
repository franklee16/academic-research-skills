---
name: prompt-optimizer
description: Transforms raw user requests into structured, outcome-focused prompts for Claude Cowork. Use when the user wants to optimize or rewrite a prompt for Cowork, needs help structuring a multi-step task for autonomous execution, or says things like "optimize this Cowork prompt", "rewrite for Cowork", or "make this a Cowork prompt". Outputs a single code block with the rewritten prompt following the GOAL/CONTEXT LOADING/IDENTITY/SUCCESS CRITERIA/INPUTS/CONSTRAINTS/CHECKPOINT RULE structure.
---

# Cowork Prompt Optimizer

Transform raw requests into structured prompts for Claude Cowork autonomous execution.

## Execution Model

Cowork is an agentic tool that executes multi-step tasks autonomously on local files and connected tools (Google Drive, Slack, Notion, Gmail, Calendar, Chrome). It has built-in skills for .docx, .xlsx, .pptx, and PDF creation. It works within an iClaude OS workspace containing workstation subfolders, each with CLAUDE.md (identity + workflow rules) and MEMORY.md (accumulated context).

**Key insight:** Clear goals and constraints outperform step-by-step instructions. Mistakes can be destructive, so high-risk tasks need checkpoints.

## Rewrite Principles (Priority Order)

1. **Goal over process** - State the end-state and deliverables. Do NOT include step-by-step instructions.
2. **Context loading** - Identify which workstation(s) and project subfolder(s) are relevant. Instruct Cowork to read CLAUDE.md, MEMORY.md, and Resources files before executing. Be specific.
3. **Concrete success criteria** - Every criterion must be verifiable (e.g., "under 2,000 words" not "high quality").
4. **Boundaries and constraints** - Define what to include, exclude, preserve, avoid. Err toward more guardrails.
5. **Failure handling** - Specify what to do if expected files are missing, formats are wrong, or a connector fails.
6. **Tool and connector naming** - Name specific tools so Cowork selects them correctly.

## Output Format

```
GOAL
[One sentence: the specific end-state]

CONTEXT LOADING
- [Which workstation CLAUDE.md + MEMORY.md to read]
- [Which project MEMORY.md to read, if applicable]
- [Which Resources files to scan for relevant reference material]

IDENTITY
[One sentence: which workstation voice/role Cowork should adopt, or "cross-workstation"]

SUCCESS CRITERIA
- [Verifiable outcome]
- [Verifiable outcome]
- [Verifiable outcome]

INPUTS
- [Folder paths, files, or connectors to use]

CONSTRAINTS
- [What to preserve, avoid, or not touch]
- [Scope limits and format requirements]
- [If X is missing or fails, do Y]

CHECKPOINT RULE
[When to pause for approval, calibrated to risk level]
```

## Risk Levels for Checkpoints

| Risk Level | Checkpoint Behavior |
|------------|---------------------|
| High | Pause before ANY action |
| Medium | Pause after plan |
| Low | Pause before delivering final output |

## Output Rules

- Output ONLY the rewritten prompt inside a single code block
- Mark any field the user must customize with `WARNING` and a brief note
- Keep total output under 200 words
- If the raw request is too vague to infer a workstation or context source, flag it with `WARNING` and suggest what context might be relevant
- Do NOT execute, answer, or comment on the request itself
