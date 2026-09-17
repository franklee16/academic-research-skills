---
name: paper-slides
description: Build or revise academic Beamer slides from a research paper (LaTeX manuscript or PDF), following Weikai Li's slide style guide. Use this skill whenever the user asks to create slides, a deck, a talk, or a presentation from a paper, manuscript, draft, or working paper — including "make slides from my paper", "seminar deck", "conference presentation", "turn main.tex into a talk", "prepare slides for the seminar/conference", "update my slides with the new results", or any request involving Beamer decks derived from empirical research papers. Also trigger when the user mentions page counts for seminar vs conference decks or wants slides that follow the Frank-OS slide style.
---

# Paper Slides

Build publication-grade Beamer decks from a research paper. Two modes with different page budgets. The paper's tables and figures go in verbatim; the style guide governs everything else.

## Step 1 — Gather inputs

Ask (AskUserQuestion) for anything missing:

| Input | Options / default |
|---|---|
| **Mode** | **conference: 20–25 PDF pages** or **seminar: 35–45 PDF pages** |
| Paper source | `main.tex` (preferred — includes tables/figures) or PDF; locate its `folder_table/`, `tables.tex`, `figures.tex`, `folder_figure/`, `.bib` |
| Venue string | goes in `\date{}`; fallback `\today` |
| Output folder | default: the paper project's `Slides/` |

The page budget counts **physical PDF pages of the whole file including backup slides** — this is what the user sees in their PDF reader. Budget accordingly from the first draft of the deck, not as an afterthought.

## Step 2 — Read the style guide (never skip)

1. If `C:\Users\frank\Dropbox\Frank-OS\Style\SLIDES_STYLE_GUIDE_short.md` exists, read it — it is the live authority and may be newer than the bundled copy.
2. Otherwise read the bundled `references/SLIDES_STYLE_GUIDE_short.md`.
3. If both exist and differ, tell the user and offer to refresh the bundled copy.

The guide defines: section architecture (Title → Motivation → Preview → Contribution → Data → Main results → Robustness hub → Mechanisms → Conclusion → Backup), the Frankfurt-theme skeleton with seminar-family options, setup→table pairing, hyperlink hub-and-spoke, color grammar, and the compile conventions. The guide is the authority on style; this SKILL.md adds the workflow and the failure modes the guide doesn't cover.

Filename: `<Topic> - <YYYYMM>.tex` (e.g. `Deepseeking Analyst Reports - 202609.tex`).

## Step 3 — Extract content with strict fidelity

The single most important property of the deck: **every number traces to the paper.**

- Read the paper's table source files directly (`folder_table/*.tex`, `tables.tex`) and paste table bodies **verbatim** into slides. No rounding, no invented numbers, no paraphrased coefficients.
- Add emphasis only through formatting: money rows `\rowcolor{blue!30}`, focal cells `\cellcolor{lg}\textbf{...}`, focal coefficient red in equations.
- One `\scriptsize` takeaway bullet per table slide with the headline magnitude (e.g. "the spread is 1.33% per month ($t = 2.67$)").
- Economic-magnitude bullets are explicit arithmetic, both inputs from paper tables: "a one-SD increase ($0.154 \times 3.07$) raises next-quarter ROA by 0.47 pp". Never quote a magnitude you cannot reconstruct from a table in the paper.
- **Verify every citation against the paper's `.bib` before it reaches a slide.** Look up the key, read the author/year fields. Bibliography keys mislead (a key like `entity2025` can hide an author list you'd never guess). If the paper is a PDF without a .bib, use author-year strings exactly as printed in the paper's references.
- If the paper uses an Agent to survey tables (line numbers + captions), delegate that search rather than reading the whole manuscript inline.

## Step 4 — Frame budget by mode

Plan the frame count before writing. Auto-outline frames (one per `\section`) and the title page count toward the budget.

| Block | Seminar (35–45 pp) | Conference (20–25 pp) |
|---|---|---|
| Title + outlines | 7 | 5–6 |
| Motivation | 2–3 | 1–2 |
| Preview + Contribution | 2 | 2 (never cut) |
| Data / measurement | 4–5 | 2–3 |
| Main results (setup+table pairs, figures) | 8–11 | 5–6 |
| Robustness hub | 1 | 1 (never cut) |
| Mechanisms / extensions | 5–8 | 2–3 |
| Conclusion | 1 | 1 (never cut) |
| Backup arsenal | 3–5 | 2–3 |

Conference mode cuts in the guide's order: generic background motivation → second preview → literature content (not contribution) → theory → summary statistics → heterogeneity tables → individual mechanism blocks. Never cut: preview pair, contribution slide, conclusion, robustness battery, hypothesis-test setup+table pairs.

If a table won't fit the conference budget, keep the setup slide with the headline numbers quoted from the paper and demote the full table to backup.

## Step 5 — Write the deck

Follow the skeleton in the style guide (§8). Key wiring:

- Seminar family: `\documentclass[10pt]{beamer}`, `\usetheme{frankfurt}`, footline with short author/title, `\AtBeginSection` auto-outline.
- Backup: unsectioned frames after Conclusion, wrapped in `\backupbegin` ... `\backupend`, each with a `\hypertarget` and a "back to main" `\hyperlink`.
- Setup→table pairs: exact frametitle repetition or ", Result" suffix — pick one convention per deck.
- One repeated equation skeleton across the deck; only the LHS changes; focal coefficient `\textcolor{red}`.

## Hard rules — each earned in production

These come from real failures on this pipeline. Breaking any of them produced a broken or falsely-"verified" deck.

1. **No `\pause` overlays — none.** Every overlay is a physical PDF page. A 33-frame deck with ~20 pauses shipped as 50 pages, blowing every budget. Structure emphasis with `\vspace` spacing instead. (If a future venue truly needs reveals, count overlays against the page budget and get the user's sign-off.)

2. **Never fix a crowded table slide with negative `\vspace`.** Pulling the takeaway bullet upward with `\vspace{-0.2in}` overlaps it into the table — and the LaTeX log shows *nothing*, because underfull spacing is legal. The user sees it; the log doesn't. Shrink the table instead, in this order:
   1. font one notch down (`\scriptsize` → `\tiny`)
   2. `\renewcommand{\arraystretch}{0.80–0.85}` right after `\setlength{\tabcolsep}{...}`
   3. `\begin{adjustbox}{width=0.88–0.95\textwidth}` around the tabular
   Target ≥ 6pt clear gap between table bottom and takeaway (14–20pt is typical when healthy). Check with `scripts/verify_slides.py`, not by eye.

3. **Verify every edit landed.** On Windows Git-Bash, `sed` and Python-heredoc string replaces can silently no-op on LaTeX backslash content — `str.replace` returns the string unchanged if the pattern didn't match, and a script still prints "patched". A full round of phantom fixes once shipped while verification greps were also broken. Consequences:
   - Prefer the Edit tool over `sed`/heredoc-Python for `.tex` files.
   - After any scripted edit, re-grep the file for the new expected string before compiling.
   - Never trust "patched" output; trust the file contents.

4. **Log checks must be fixed-string.** `grep "Overfull \\vbox"` silently matches nothing — it reports clean on a broken deck. Use `grep -F 'Overfull \vbox'`. Same for any pattern containing a backslash.

5. **Compile twice, then gate on the script.** `pdflatex` ×2 → check log (`grep -E '^!'` for errors, `grep -F 'Overfull \vbox'`) → run `scripts/verify_slides.py`. The script is the objective gate; do not declare success from a clean compile alone.

6. **Sweep hyperlinks.** Grep every `\hyperlink{X}` argument and every `\hypertarget{X}` and confirm the sets match. Orphan links after cutting slides are the most common defect in decks built by restructuring.

## Compile & verify loop

```bash
cd <Slides folder>
pdflatex -interaction=nonstopmode "Deck Name.tex" > /dev/null 2>&1
pdflatex -interaction=nonstopmode "Deck Name.tex" > /dev/null 2>&1
grep "Output written" "Deck Name.log"
grep -E '^!' "Deck Name.log" || echo "no errors"
grep -F 'Overfull \vbox' "Deck Name.log" || echo "no vbox overfull"

# On this machine:
/c/Users/frank/miniconda3/python.exe "<skill-path>/scripts/verify_slides.py" "Deck Name.pdf" \
  --min-pages 35 --max-pages 45 \
  --takeaway "earns 1.33" --takeaway "spread remains"   # one plain-text key per table slide
```

Iterate (fix → recompile ×2 → re-verify) until: 0 errors, 0 `Overfull \vbox`, page count in range, 0 text-block overlaps, all takeaway gaps ≥ 6pt. A ~1.8pt horizontal overfull from the Frankfurt footline on every page is a known cosmetic artifact — ignore it.

## verify_slides.py notes

- Requires `pymupdf` (`fitz`).
- `--takeaway` keys must be **plain text without inline math** — pymupdf splits blocks at `$...$`, so a key spanning math never matches. Pick words outside the math.
- Exit code 1 = hard failure (page count, overlap, out-of-bounds, takeaway gap < 6pt). Tight-gap warnings are advisory.

## Finishing up

- Report to the user: page count, deck path, what went to backup, any deviation from the style guide.
- Remind them the venue string in `\date{}` is a placeholder if they didn't supply one.
