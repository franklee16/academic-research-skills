# PaperSpine

PaperSpine is a motivation-driven `SKILL.md` package for academic papers and paper-like writing tasks. It can be used with Codex-style skill folders and Claude Code skill folders. It is designed as a research-writing learning system rather than a prose polisher: it first studies the target venue or task genre, learns from strong exemplars, confirms the controlling motivation, builds section-level blueprints, and only then rewrites or integrates the manuscript.

In short: PaperSpine helps a manuscript grow around its central spine: motivation, evidence, section logic, and revision accountability.

## What It Does

- Confirms the paper's controlling motivation before substantive writing.
- Researches target journals, conferences, or paper-like task genres.
- Learns rhetorical structure from strong exemplar papers or reports.
- Builds traceable artifacts such as `confirmed_motivation.md`, `style_profile.md`, `section_blueprints.md`, `rewrite_matrix.md`, and `logic_transfer_audit.md`.
- Preserves version-specific requirements through `special_requirements.md`.
- Guards LaTeX projects against broken citations, labels, figures, and environments.
- Audits revisions for shallow editing and addition-heavy rewrites.

## Install

Install the whole folder, not only `SKILL.md`. PaperSpine uses `references/` and `scripts/` as part of the skill.

### Codex

Clone or copy this repository into your Codex skills directory as `paper-spine`:

```bash
git clone https://github.com/WUBING2023/PaperSpine.git "$CODEX_HOME/skills/paper-spine"
```

Then invoke it with `$paper-spine`:

```text
Use $paper-spine to diagnose and rewrite my manuscript for a target journal.
```

### Claude Code

For a personal skill available across projects, clone or copy this repository to:

```text
~/.claude/skills/paper-spine/SKILL.md
```

For a project-only skill, put it under the project:

```text
<project>/.claude/skills/paper-spine/SKILL.md
```

Example:

```bash
git clone https://github.com/WUBING2023/PaperSpine.git ~/.claude/skills/paper-spine
```

In Claude Code, the skill directory name becomes the slash command:

```text
/paper-spine
```

Claude Code may also invoke the skill automatically when your request matches the `description` in `SKILL.md`.

### Claude.ai

Zip the `paper-spine` folder itself, with `SKILL.md` directly inside that folder, then upload it through Claude's Skills settings. Keep the folder structure intact so `references/` and `scripts/` remain available.

## Quick Start

```text
Use $paper-spine to diagnose and rewrite my manuscript for a target journal.
```

For Claude Code, use:

```text
/paper-spine
```

## Typical Workflow

1. Create `source_map.md` to classify the draft, data, figures, references, and exemplar sources.
2. Carry forward `special_requirements.md` when making numbered versions such as V8, V9, or V10.
3. Confirm the motivation in `confirmed_motivation.md`, or create `motivation_options.md` for user selection.
4. Research the target venue or task genre.
5. Learn from exemplar papers or reports.
6. Build the motivation thread, evidence bank, section blueprints, and rewrite matrix.
7. Rewrite from the blueprint, not by appending sentences to old paragraphs.
8. Run revision, logic-transfer, and LaTeX integrity audits.

## Scripts

All scripts use only the Python standard library.

```bash
python scripts/style_metrics.py path/to/paper.tex --markdown
python scripts/revision_audit.py original.tex revised.tex --markdown
python scripts/latex_guard.py main.tex --bib references.bib --markdown
```

## Repository Hygiene

This repository should contain only the reusable skill. Do not commit user manuscripts, generated paper versions, local `paper_rewriting_output/` folders, compiled PDFs, or temporary one-off generation scripts.

## Privacy And Integrity

The skill is designed to keep user data separate from exemplar papers. Exemplar papers may teach structure and rhetorical moves, but their scientific results must not be copied into the user's manuscript. The skill also forbids fabricating data, citations, metrics, p-values, or experimental claims.
