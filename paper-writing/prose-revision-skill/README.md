# Prose Revision Skill for Claude

A Claude Skill for revising draft prose — essays, papers, memos, reports — by
finding the best structure for the ideas the author already wants to express.
Its guiding principle is **idea flow before linguistic flow**.

## What It Does

This skill treats awkward writing as a symptom of structural problems, not just
bad phrasing, and fixes the structure before polishing the words. When active,
Claude will:

* **Diagnose idea flow before wording** — order, emphasis, and what each unit is
  trying to do come before sentence-level smoothing
* **Work at every level** — sentence, paragraph, section, and whole — fixing the
  larger structure (paragraph and section order) before rewriting inside paragraphs
* **Lead with the main claim** and push qualifications after the claim they modify,
  so the reader isn't kept waiting for the point
* **Stay conservative on content** — preserve the author's voice, substantive
  claims, and *claim strength* (no turning "suggests" into "shows")
* **Offer revised versions** distinguished by how much they restructure (light,
  moderate, or full rebuild), with a note on the tradeoff
* **Leave well enough alone** — if a draft already reads well, say so rather than
  manufacture edits

It is distinct from proofreading: this skill gets a rough draft's structure into
shape; proofreading is the later pass for typos and final copy-editing.

## Installation

1. Download this repository as a zip file (click **Code → Download ZIP** above)
2. In [claude.ai](https://claude.ai), go to **Customize → Skills**
3. Upload the zip file
4. Confirm the skill appears in your skills list and is toggled on

> **Requirement:** Code execution and file creation must be enabled in
> **Settings → Capabilities**.

## Usage

Just ask naturally:

* *"Revise this paragraph for flow"*
* *"Help me tighten this section — the argument feels tangled"*
* *"This draft reads awkwardly; can you restructure it?"*

Claude will detect the prose-revision context, load this skill automatically, and
diagnose structure before touching the wording. You do not need to give any
special instructions.

## File Structure

```
prose-revision-skill-ht-anthony-lee-zhang/
├── SKILL.md    # The skill: philosophy, workflow, output style, worked example
└── README.md   # This file
```

## Background

Builds on a prose-revision skill by Anthony Lee Zhang ("ht" = hat tip). The core
idea — that clear writing is first a matter of getting ideas into the right order,
and only then a matter of elegant sentences — draws on a long tradition of writing
advice that treats revision as structural work rather than surface polish.

## License

MIT — free to use, adapt, and share.
