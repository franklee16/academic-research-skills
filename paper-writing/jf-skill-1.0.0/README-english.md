# JF Writing Style Guide — Quick Start

A Journal of Finance style reference for academic writing in financial economics. Distilled from 144 JF papers published between 2022 and 2025. Covers sentence templates, collocations, paragraph structures, and a polishing workflow. Works for both English-language editing and Chinese-to-English translation.

---

## How to Activate

Type any keyword below into the conversation to trigger the skill:

| Trigger | Example |
|---------|---------|
| `jf-skill` | `jf-skill help me polish this introduction` |
| `JF风格` | `JF风格，把这段结果翻译成英文` |
| `JF polish` | `jf polish my results section` |
| `JF translate` | `JF translate this abstract` |
| `JF style` | `apply JF style to my literature review` |

**What does NOT trigger the skill:** General grammar correction, style advice for non-finance journals, or purely structural feedback (those go through peer review).

---

## What Happens When You Use It

| You Say | The Skill Does | Reference Files Used |
|---------|----------------|---------------------|
| "polish introduction" | Matches JF opening sentences and paragraph structure | `sentence-templates.md` sections 1-5 |
| "polish results" | Applies the Claim-Evidence-Interpretation paragraph model | `sentence-templates.md` sections 9-11 + `paragraph-patterns.md` sections 29-33 |
| "translate abstract" | Chinese-to-English translation with JF phrase substitution and hedging calibration | `phrase-bank.md` |
| "check full-paper writing style" | Scans for AI fingerprints (three-tier defense), over-hedging, and unnatural collocations | All 5 reference files |
| "not sure how to start an introduction" | Offers 28 JF opening styles to choose from | `sentence-templates.md` section 1 |
| "polish conclusion" | Applies JF conclusion templates and implication cascade | `sentence-templates.md` section 15 |
| "rewrite a paragraph" | Matches the paragraph to one of 33 structural patterns | `paragraph-patterns.md` |

---

## Architecture

The skill uses a modular structure. The main file (`SKILL.md`) handles triggering, routing, and quality control. Examples, templates, and collocations live in the `references/` subdirectory and are loaded on demand.

```
jf-skill-1.0.0/
├── SKILL.md                          ← Main file (triggers, mode selection, quality standards)
└── references/
    ├── sentence-templates.md         ← 21 categories of sentence patterns, with full examples and citations
    ├── phrase-bank.md                ← Verb collocations, adjective pairs, hedging by confidence level, non-academic-to-JF substitutions
    ├── paragraph-patterns.md         ← 33 paragraph structures with variants and worked examples
    ├── meta-discourse.md             ← Templates for boundary setting, interpretive control, and layered analysis
    └── usage-guide.md                ← 8-step polishing workflow, appendix templates, 18 caveats (A-R, including the three-tier AI-defense system)
```

---

## Workflow

Every time the skill is activated, it follows these steps:

1. **Diagnose** — Which part of the paper is this (introduction, results, conclusion, etc.)? Does the user want polishing, translation, or drafting help?
2. **Load references** — Most tasks need only 1 or 2 reference files. Full-paper audits need all 5.
3. **Apply patterns** — Match JF sentence types, substitute phrases, calibrate hedging intensity.
4. **Polish** — Iterate, avoiding mechanical or rote substitution.
5. **AI-fingerprint check (three-tier)** — Tier 1: scan for 12 phrase-level markers (words like "notably," "potentially," "Furthermore," plus hedging phrases that GPTZero has learned to flag). Tier 2: 5 structural self-audit questions (paragraph template diversity, whether the Introduction follows a rigid four-part structure, parallel subsection formatting, expressions of uncertainty, and whether the Conclusion re-lists contributions). Tier 3: 5 quantitative metrics (sentence-length standard deviation, connector-word density, share of extreme-length paragraphs, count of uncertainty expressions, and dominant template share).

---

## Key Design Principles

**This is a reference book, not a recipe book.** Every sentence pattern, collocation, and paragraph structure in the skill is *descriptive* (this is what JF authors actually do), not *prescriptive* (this is what you must do). The goal is to help you diagnose what your text is missing and see how published JF papers handle similar situations — not to override your own judgment.

**No single paper uses all the patterns.** Real JF papers draw on only a small subset. If a paper uses more than five distinctive collocations ("shed new light on," "bridge different strands," "demystify," etc.), it starts to read like it was AI-generated.

**Hedging should match the strength of your evidence.** Vague claims get speculative language. Well-supported findings get confident language. Over-hedging damages credibility just as much as overclaiming.

**Journal conventions differ across outlets.** ALL CAPS openings, long enumerations, and "The remainder of the paper is organized as follows" are standard in JF. If you are submitting to the JPE, QJE, or Econometrica, check whether those conventions apply.

**AI detection is about structural symmetry, not word choice.** The right way to lower your AI-detection risk is not to swap out individual words. It is to break structural symmetry, inject uncertainty, and allow traces of imperfection. See `usage-guide.md`, Caveats M through R, for details.

---

## Data Source

All patterns are extracted sentence by sentence from 144 published Journal of Finance papers (2022–2025). Coverage includes asset pricing, corporate finance, banking, behavioral finance, household finance, international finance, and financial intermediation. Every example sentence is a direct quotation from a published JF article.

---

## Version History

**v3.1.0** (June 5, 2026) — Three-tier AI-fingerprint defense system: Step 5 expanded from a 7-item scan to 12 phrase-level markers + 5 structural audit questions + 5 quantitative metrics. Anti-patterns expanded from 8 to 15 (7 new entries on structural symmetry). Added Caveats M-R to `usage-guide.md` covering the symmetry problem, high-trigger patterns and their fixes, quantitative audit metrics, imperfect writing as a defense, section-specific risk tables, and a 2-minute pre-submission check. Principles adapted from the structure-randomizer and deep-humanize approaches.

**v3.0.0** (June 5, 2026) — Modular rewrite: split the ~2,000-line monolithic SKILL.md into an orchestrator plus 5 reference files.

---

## Acknowledgments

Inspired by the modular architecture of [academic-research-skills](https://github.com/Imbad0202/academic-research-skills). The v3.1 AI-detection defense system builds on principles from structure-randomizer (using structural variance to evade detection) and deep-humanize (statistical analysis of detection-model dimensions).
