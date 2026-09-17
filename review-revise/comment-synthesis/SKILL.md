---
name: comments-synthesis
description: Consolidate feedback from multiple discussants, referees, and commentators on a research paper into one unified revision plan. Use this skill WHENERVER a user has gathered comments, discussion decks, referee reports, or reviewer feedback from more than one source on a paper and wants them synthesized — for example "synthesize the comments", "consolidate the discussant feedback", "what are the common comments across referees", "build a revision plan from the discussion decks", "combine the discussant comments", "summarize the referee reports", or when a Comments/ or quality_reports/ folder contains multiple discussion PDFs/PPTX/DOCX files for one paper. Also trigger when the user says they got discussant comments at a conference, an R&R with referee reports, or workshop feedback and wants it pulled together. Do not trigger for a single comment or a single referee report — this is specifically for cross-source synthesis (2+ sources).
---

# Discussant & Referee Comment Synthesis

## What this skill does

A paper usually collects feedback from several independent readers — conference discussants, journal referees, workshop attendees, co-authors. Each speaks from a different angle, but the same handful of concerns recur. The value of synthesizing them is **convergence detection**: an issue raised by 4 independent readers is a publication-blocking threat; one raised by a single reader is a useful refinement. This skill turns a folder of heterogeneous comment files into one revision plan that makes the convergence visible.

The output is a single Markdown report with three parts:
1. **Common comments** — raised by ≥2 sources, each with concern, attribution, and a concrete *how to address*.
2. **Idiosyncratic comments** — raised by one source, each with the same structure.
3. **Prioritized roadmap** — Must-do / Should-do / Minor, ranked by convergence and severity.

## When to use

Trigger when the user has **two or more** independent comment sources for one paper and wants them consolidated. Typical settings:
- A conference circuit: discussant decks (PPTX/PDF) from ARCS, FMA, CAAA, CICF, All-Ohio, etc.
- A journal R&R: multiple referee reports plus a discussant or two.
- Workshop / co-author round of comments (often DOCX or email text).

If there is only one source, do not run this skill — just summarize that one document directly.

## Inputs

Look for source files in these locations, in order:
1. The project's `Comments/` folder (primary — discussant decks, workshop notes).
2. The project's `quality_reports/` folder (referee reports, editorial reviews, internal evaluations).

Supported formats: `.pdf`, `.pptx`, `.docx`, `.txt`, `.md`. Read every source file directly — do **not** rely on prior syntheses or summary files that may already exist in those folders, because they may be stale or partial. (If prior syntheses exist, note them; you will offer to clean them up at the end.)

## Workflow

### Step 1 — Inventory the sources

List every comment file found. For each, determine the **commentator, affiliation, venue, and date** — this metadata is almost always on slide 1 / page 1 / the letterhead. Build a sources table up front so the reader can see the corpus at a glance:

```
| # | Commentator | Affiliation | Venue / Date | File |
|---|-------------|-------------|--------------|------|
```

If you cannot identify the commentator for a file, say so rather than inventing one.

### Step 2 — Extract the substantive comments from each source

Read each source in full and pull out the actual comments. Use the bundled extraction helper when a file is a binary format (see `scripts/extract_sources.py` below). For each source, capture:
- The concern in the commentator's own framing (one or two sentences).
- Any specific numbers, tables, coefficient values, or paper sections they cite (e.g. "β(PSL on males) ≈ +0.153", "Table 7", "Section 4.4"). These anchors are what make the synthesis actionable.
- Any suggested test or fix the commentator themselves proposed.

Keep author responses / rebuttals (common in workshop DOCX notes) paired with the comment that triggered them — they are useful context for writing the *how to address*.

### Step 3 — Cluster thematically and count convergence

Group comments by underlying issue, not by surface phrasing. Two discussants who say "the magnitude seems large" and "is 37% plausible?" are raising the same issue. After clustering, count how many distinct sources raised each issue. This count is the priority signal — record it on every common-comment entry.

The bar for **Common** is ≥2 independent sources. Everything else is **Idiosyncratic**.

Watch for comments that *sound* the same but are actually different (e.g. "brokerages already had PSL" vs. "analyst location is measured with error" — both are about treatment validity but have distinct fixes). Split them.

### Step 4 — Write each comment entry

For every comment, common or idiosyncratic, use this shape:

```
### [Short label] — raised by N sources   (or: — single source, [Name])

**The concern.** One or two sentences stating the issue in plain language,
in the commentators' framing. Include any numbers/tables they cited.

**Who raised it.** [Source #, Source #, ...] — name them explicitly.

**How to address.** Concrete, paper-specific actions. Tie each action to a
specific test, table, section, or data source when possible. Prefer 2–4
bulleted actions over a vague paragraph.
```

The *how to address* is the heart of the report. Good guidance:
- Name the specific empirical test, robustness check, or section rewrite.
- Cite the data source or method (e.g. "wild-cluster bootstrap at the policy-jurisdiction level", "BLS National Compensation Survey", "Wald test H₀: β₁ + β₂ = 0").
- When commentators disagree on the fix, present the alternatives and say which is preferred and why.
- Distinguish "reframe the narrative" changes from "run new analysis" changes — they have very different costs.

### Step 5 — Build the prioritized roadmap

Aggregate everything into Must-do / Should-do / Minor tiers. Rank within tier by convergence count (for common comments) and by whether the comment threatens the paper's core identification (a mechanism objection from 5 readers outranks a wording quibble from 2). Cross-reference each roadmap item back to the comment labels (e.g. "(see Item A, N)") so the reader can trace a roadmap action to the full discussion.

### Step 6 — Write the report

Write a single Markdown file. Default name and location: `Comments/Comments_Synthesis_and_Revision_Plan.md` (or the project's equivalent comments folder). Overwrite only if the user confirms; otherwise version the filename.

The report should open with a one-paragraph "convergence reading" — the 2–3 issues that every reader hit, which are the biggest threats to acceptance. This is the single most useful sentence in the document; write it carefully.

Follow the user's writing rules: no em dashes (use commas, colons, parentheses); English for academic output unless the user writes in another language.

### Step 7 — Cleanup (ask first)

Prior syntheses or partial summary files in the source folders are now redundant once the unified report exists. **Identify them explicitly and ask the user before deleting anything.** Never delete source files (the original decks, reports, notes) — only prior syntheses the user confirms are superseded. Deletion is destructive; the user's confirmation rule applies in full.

## Principles that matter

- **Attribution is the whole point.** Every comment must tag which source(s) raised it. A synthesis that merges everything into anonymous bullet points has destroyed the only information that makes cross-source synthesis valuable. When in doubt, over-attribute.
- **Convergence counting drives priority.** An issue raised by 5 independent readers is almost certainly real and blocking. Treat the count as a first-class signal, displayed in the heading.
- **Read sources fresh.** Do not trust prior summary files. They drift, they miss idiosyncratic comments, and they can propagate errors. Go back to the originals.
- **Keep the commentators' anchors.** Coefficients, table numbers, section references — these are what let the author act immediately instead of re-reading the deck.
- **The how-to-address must be concrete.** "Discuss the mechanism more" is useless. "Add a brokerage-size cross-section to separate the access channel from the public-health channel (smaller brokerages should respond more if access/stigma is the mechanism)" is useful.
- **Respect scope.** If the user scoped the synthesis to one folder (e.g. "just the Comments folder"), honor that and flag anything outside the scope rather than silently expanding.

## Bundled helper: extracting text from PDF / PPTX / DOCX

Comment files arrive in binary formats. Use `scripts/extract_sources.py` to dump plain text per file so you can read everything without fighting each format separately:

```bash
python scripts/extract_sources.py <folder-with-comment-files> <output-folder>
```

It tries `markitdown` first (handles most formats well), then falls back to `pypdf`/`pdfplumber` for PDFs, `python-pptx` for PPTX, and `python-docx` for DOCX. One `.txt` is written per source file into the output folder; read those.

If extraction fails on a scanned/image PDF, fall back to OCR (`pytesseract` or `easyocr`), per the user's global PDF-extraction rules. For Asian-language PDFs, prefer `python-docx`-via-markitdown over image-based APIs.

## Output template

```markdown
# Synthesis of Discussant & Commentator Feedback — [Paper short title]

**Paper:** [full title]
**Authors:** [authors]
**Compiled:** [date]

[One-paragraph convergence reading: the 2–3 universal issues.]

## Sources Synthesized
[table]

## Part 1 — Common Comments (raised by ≥2 sources)
### A. [Issue] — raised by N sources
**The concern.** ...
**Who raised it.** ...
**How to address.** ...

## Part 2 — Idiosyncratic Comments (single source)
### From [Commentator] ([venue])
- [Comment]. → *Action:* ...

## Part 3 — Prioritized Revision Roadmap
**Must-do (core identification):**
1. [Action] (Item A)
...
**Should-do:**
...
**Minor / hygiene:**
...
```

## Adapting to other fields

This skill was written around an empirical finance/economics paper, but the workflow is field-agnostic. The only thing that changes across fields is the *content* of the how-to-address actions (which tests to run, which methods to cite). Keep the structure — sources table, common/idiosyncratic split, convergence counting, prioritized roadmap — constant. If the paper is in a different field (marketing, accounting, public policy, sociology), use that field's methodological vocabulary for the actions and do not impose econometrics-specific fixes.
