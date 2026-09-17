---
name: autonomous-qa-loop
description: Create neutral autonomous QA-loop prompts for fresh, independent, history-free agents reviewing complex code changes, with module-level parallel review packets and broad reporting of plausible concerns. Use when the user says QA loop, autonomous QA loop, automated QA loop, independent review, fresh agent review, parallel QA agents, vibe coding QA, subagent review, reviewer prompt, audit agent, or asks to repeatedly find bugs without leading the reviewer toward suspected issues, prior conclusions, or existing debugging context.
---

# Autonomous QA Loop

Use this skill to draft a neutral prompt for a fresh independent QA agent. The
purpose is to keep each review pass free of prior debugging context, suspected
bugs, expected conclusions, and implementation bias.

This is useful when ordinary self-checks plateau: the same agent can find some
issues, but later passes often inherit the same assumptions. A fresh,
history-free reviewer can surface different defects when given only the
original goal, concrete artifacts, and authoritative context.

Use the prompt as part of a loop. For broad scopes, split the target into
module-level review packets and send each packet to a separate fresh agent in
parallel. Triage the combined findings in the main thread, fix only confirmed
issues, then start another fresh-agent pass with newly generated neutral
prompt(s). Repeat until independent passes stop surfacing meaningful defects or
concerns.

## Hard Format

The review prompt must contain exactly these four English top-level sections,
in this order:

```text
Background
Goal (Original Request)
Review Target
Relevant Context Documents
```

Do not add other top-level sections. Do not add sections such as `Known Issues`,
`Focus Areas`, `Expected Findings`, `Suggested Checks`, `My Diagnosis`, or
similar leading guidance.

## Neutrality Rules

- Keep the prompt neutral. Do not disclose suspected bugs, intended fixes,
  expected conclusions, or prior reviewer opinions.
- Describe the original user/business requirement in `Goal (Original Request)`; do not
  rewrite it as the implementation's intended behavior unless that came from the
  original requirement.
- Put raw artifacts in `Review Target`: changed files, diffs, commits, output paths,
  test logs, or commands that define what should be reviewed.
- Put context sources in `Relevant Context Documents`: authoritative docs, schemas, project
  plans, and files the reviewer may read.
- If some old documents, old code paths, archived branches, or stale generated
  outputs are obsolete, state that fact in `Background`.
- If some scope must not be reopened, state it in `Background`. Examples: do not
  revisit model-training policy, do not redesign portfolio logic, do not review
  deprecated V1/V2/V3 paths.
- For broad reviews, split the target into neutral module-level prompts when
  possible. Each prompt must remain self-contained and use the same four-section
  structure.
- Ask reviewers to report concrete defects and plausible concerns. They should
  include evidence, uncertainty, and reproduction or verification hints when
  available. They should not suppress suspicious findings merely because they
  are not fully proven. The main thread decides whether each item is truly a
  bug.

## Section Content

`Background` must explain the current facts the reviewer should accept before
starting:

- Current source of truth for facts, docs, data, and code.
- Which historical docs/code/output paths are deprecated or out of scope.
- Which scope boundaries are fixed and must not be re-litigated.
- Any environment constraints that matter for interpreting the review object.

`Goal (Original Request)` must preserve the user's original request:

- Quote or paraphrase the original requirement faithfully.
- Include acceptance criteria only when they came from the original request or
  an authoritative current doc.
- Do not include implementation diagnosis.

`Review Target` must identify the concrete artifacts to inspect:

- File paths, commit IDs, diff ranges, output directories, generated reports,
  or test commands.
- Prefer exact paths and raw evidence over summaries.
- Include enough artifacts for review, but do not include expected issues.
- For large scopes, keep each prompt focused on one module, subsystem, workflow,
  or test surface so multiple fresh reviewers can work in parallel.

`Relevant Context Documents` must list documents the reviewer may use:

- Current authoritative context docs.
- Current schemas, enums, interfaces, or design notes needed to judge the change.
- Explicit notes when a listed document supersedes older material.

## Template

Use this exact skeleton and fill only what is known:

```text
Background
<Current source-of-truth facts. State deprecated/out-of-scope docs or code.
State fixed boundaries that the reviewer must not reopen.>

Goal (Original Request)
<The original user requirement, as neutrally and faithfully as possible.>

Review Target
<Concrete artifacts to review: files, diffs, commits, outputs, commands, logs.
Ask the reviewer to report concrete defects and plausible concerns with
evidence, uncertainty, and verification hints when available.>

Relevant Context Documents
<Authoritative docs and context files the reviewer may read.>
```

## QA Loop

After a reviewer completes one pass:

1. Triage all reported defects, plausible concerns, and risk signals in the
   main thread.
2. Fix only issues confirmed by the main thread.
3. Do not reuse a reviewer's conversation as context for the next reviewer.
4. Generate new neutral prompt(s) with the same four-section structure.
5. Split broad scopes into module-level prompts and run fresh reviewers in
   parallel when possible.
6. Repeat until fresh reviewers stop surfacing meaningful defects or concerns.

## Final Check

Before sending the review prompt, verify:

- It has exactly four top-level sections.
- It does not mention known issues, suspected bugs, expected findings, or focus
  areas outside the four required sections.
- `Background` states source-of-truth, deprecated material, and non-reopenable scope.
- `Review Target` is artifact-based and reviewable without hidden conversation
  context.
