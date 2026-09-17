# journal-adapt skill

This folder contains the executable skill instructions for journal-adapt.

journal-adapt builds a **dynamic academic writing skill** from:

1. an optional static base writing skill,
2. a primary target-journal corpus,
3. optional field-top or topic-similar reference papers,
4. optional user/lab exemplars,
5. the manuscript section being revised.

The generated rules are reviewable before any manuscript revision starts.

---

## Install

For Claude Code:

```bash
mkdir -p ~/.claude/skills/journal-adapt
cp -R skill/* ~/.claude/skills/journal-adapt/
```

For Codex:

- If your Codex setup supports custom skills, install this folder as `journal-adapt`.
- If not, keep this repository open and ask Codex to follow `skill/SKILL.md` directly.

See `docs/INSTALLATION.md` for PDF conversion and MinerU troubleshooting. See `docs/STATIC_SKILL_RECOMMENDATIONS.md` for optional static base skill recommendations.

---

## Inputs

The skill will ask for:

1. target journal or writing destination,
2. primary corpus folder,
3. optional secondary corpus folder,
4. optional user/lab exemplar files,
5. optional base writing skill,
6. manuscript file,
7. sections to revise.

Markdown inputs work without MinerU. PDF inputs require a PDF-to-Markdown converter.

---

## Included Base Rules

```text
base_rules/
├── economics.md
├── ml_cv_nlp.md
├── cs_engineering.md
└── general_academic.md
```

You may replace these with any static writing skill or skip the base layer entirely.

---

## Output

The skill writes Markdown outputs next to the manuscript:

```text
[manuscript_name]_revised/
├── dynamic_writing_skill.md
├── style_profile.md
├── [section]_revised.md
├── [section]_revision_log.md
└── revision_summary.md
```

No facts, equations, citations, variables, or numerical claims should be changed unless the user explicitly approves that change.
