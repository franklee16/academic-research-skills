# Seminar & Conference Slide Style Guide — Weikai Li

**Short version — 2026-08-27.** Rule list distilled from the long guide. The full guide (`SLIDES_STYLE_GUIDE.md` long version) keeps the evidence and provenance; this file keeps what to *do*. Where the two disagree, the long version wins. Build order = §1 → §7; §8 is the skeleton.

**Index.** §1 architecture · §2 narrative · §3 flow · §4 writing · §5 visual · §6 lifecycle · §7 checklist · §8 skeleton.

---

## 1. Architecture

**Section sequence (canonical):** Title → Motivation (3–5 slides) → Preview (1–2) → Contribution (1, live, *after* preview) → (optional Institutional Background) → Data (2–7) → Main Results: sort/portfolio → puzzle-deepener → spec → table → robustness hub (4–6) → Mechanism/Alternatives (largest block; see §2) → (optional External Validity) → Conclusion (1 slide, 4–5 bullets) → Backup arsenal.

**Preview sits right after Motivation**, before data, methods, or literature. Headline number + t-stat + verdicts on competing explanations + pre-answer to the obvious objection.

**Contribution slide: 1 slide, live, after the preview.** Literature-only content gets commented out.

**Mechanism is the largest block.** Sizing rule: 1 overview slide + one setup+table pair per candidate channel + 1 pivotal-question slide for the rejected explanation. Minimum: not smaller than main-results block.

**Robustness: claimed, not shown.** One menu/hub slide with `\beamerbutton{here}` into backup. No robustness tables in main talk.

**Conclusion mirrors preview**, finding-first ("Contrary to [null], we find…"), 4–5 bullets, sign result → mechanism → boundary condition → implication. End cold — no thank-you, no Q&A slide.

**Backup after Conclusion**, reached by hyperlink not linear flow. Marked with `\section{Appendix}` (current flagship practice) or unsectioned (seminar family).

---

## 2. Narrative

**Openings: anchor in authority, land magnitude by slide 2–4.** Slide 2 = authority claim (received hypothesis, theory, literature gap). Magnitude ($, %, count) about *your market* by slides 2–4. Generic planet/background motivation is cut.

**Motivation sequencing:** market-not-planet → named-firm example as final move pre-killing confounds → worked numerical example for any constructed statistic.

**Front-loaded preview:** state the payoff, then earn it. Headline magnitude + t-stat + identification claim + mechanism verdicts + pre-answer to objection — all before Data.

**Results chain:** premise → effect → causality → mechanism → who → outcomes. Validate the measure first if you built one. Deepen the puzzle before regressing. Distinctness embedded in the main table, not asserted.

**Each setup slide names its predecessor's conclusion in its first bullet:** "Our evidence so far suggests…", "To test this, we run…".

---

## 3. Flow

**Setup → table pairing.** Footnotesize setup slide (hypothesis + proxies + equation with focal coefficient in red) → `\tiny` full-table slide. Title convention: exact repetition (flagship) or ", result" suffix (seminar family). Don't mix within one deck.

**Signposting is structural, not verbal.** No "so far / up next" transition slides. Orientation comes from the auto-Outline (seminar family) or the Frankfurt headline + preview (flagship). Branded coined term as through-line ("Low Carbon Alpha").

**Continuation conventions:** "(cont'd)" suffix for spills; verbatim repetition for 3+ slide runs; numbered sequences ("Alternative Explanation 1/2/3").

**Hyperlink navigation:** hub-and-spoke `\hypertarget` + `\hyperlink{...}{\beamerbutton{...}}`. Outbound reads "here". Inbound reads "main" or the origin slide's name. Idiom: `\hypertarget{name}{}` immediately after `\begin{frame}`, or inside the first `\begin{itemize}`. **After any cut, grep every `\hyperlink` argument against `\hypertarget` definitions** — orphan targets and dead links are the most common defect.

**Table walkthrough is pre-baked into formatting.** Money rows shaded `\rowcolor{blue!30}`, focal cells `\cellcolor{lg}`, dep-var labels in red, focal coefficients bold. Tables land whole — never reveal incrementally. `\pause` never on tables.

**Pacing:** `\pause` only on argument slides. Late decks reduce `\pause` and replace with `\vspace` spacing. Shrink-to-fit is the density response — content is never cut for the room, only the font.

---

## 4. Writing

**Frametitles: noun-phrase topic labels, never declarative claims.** Title Case. Question form reserved for the pivotal test or the big objection. Long titles: reword first; resize (`\large`/`\small`/`\normalsize` inside `\frametitle{}`) as fallback.

**Bullets: full declarative sentences.** Top-level 10–25 words; sub-bullets 5–20 words, 2–4 per bullet. "We + present-tense verb" openers dominate. Fragments only as bold lead-ins (`**Ideal test**:`) or `\item[--]` citation sub-items. Concrete numbers inside bullets, always.

**Tense:** present tense uniformly for findings, design, literature, conclusion. Simple past only for institutional events.

**Color grammar (flagship standard):**

| Device | Meaning |
|---|---|
| `\textcolor{blue}` | Key concepts, coined terms, findings, discriminators |
| `\textcolor{red}` | The focal coefficient/variable — including inside equations |
| `\textbf` | Load-bearing word in finding sentences |
| `\underline` | Hypothesis names and structural labels |
| `\rowcolor{blue!30}` | Money row in tables |
| `\cellcolor{lg}` (periwinkle) / yellow `\cellcolor[rgb]{1,1,0}` | Focal cells / panel headers |

**Discipline:** blue never marks a variable, red never marks prose. Don't mix color grammar and bold-only grammar within one deck.

**Math density: one repeated equation skeleton per deck**, only LHS changing. Focal coefficient always red. Variables are Stata-style acronyms promoted to notation, with an on-slide glossary. Lag/lead timing explicit in subscripts; event windows in bracket notation.

---

## 5. Visual

**Theme:** `\usetheme{Frankfurt}` throughout. Two class options: `[10pt]` (seminar family) or `[presentation]` (Carbon flagship, 11pt). 4:3 — no `aspectratio`. Navigation symbols stripped.

**Title page:** bracket short forms `\title[short]{full}` and `\author[short]{names}`. `\inst{n}` institutes keyed to `\institute[]{}`. Short-author alphabetical in footline, not presenter-first. Venue string in `\date{}` for outbound decks.

**Tables: full pasted regression tables — never coefficient plots, never excerpts.** Booktabs three-line (`\toprule`/`\midrule`/`\bottomrule` + `\cmidrule`), no vertical rules. **t-statistics in parentheses** (not SEs), stars, dep-var headers bold italic. No captions — frametitle is the caption.

**Fit escalation order:** (1) shrink body font `\footnotesize`→`\scriptsize`→`\tiny` first; (2) tune `\setlength{\tabcolsep}` (start 0.05in); (3) `\begin{adjustbox}{width=1\textwidth}`; (4) negative `\vspace` as last resort.

**Layout norm: vertical stacking.** No `\begin{columns}` in body slides. Don't design multi-column body slides.

**Figures: pin width only, or add `keepaspectratio`.** Never pin both dimensions — squashes screenshots.

**Overlays:** `\pause` only — no `\only`, no `\onslide`, no handout variant.

---

## 6. Lifecycle

**Fork per venue; filename = topic + YYYYMM.** Style upgrades do not back-propagate across forks — decide deliberately whether to port.

**Never delete — comment out.** Superseded slides live in `\begin{comment}` blocks. The `.tex` is the talk's own revision history.

**Demote, don't discard.** Backup grows to ~14–15 slides then freezes as standing arsenal; main deck shrinks. ~25% of every late deck lives after Conclusion.

**Cut at slide granularity, not bullet granularity**, in this order: generic background motivation → second preview → literature content (not contribution) → theory sections → summary statistics → subsample/heterogeneity tables → individual mechanism blocks (only for shortest slots).

**What never gets cut:** the preview pair, the contribution taxonomy slide, the Conclusion, the numbered robustness battery, the hypothesis-test setup+table pairs.

**`\backupbegin`/`\backupend`:** either invoke them (so backup frames don't inflate `\inserttotalframenumber`) or drop them entirely. Don't define-but-never-call.

---

## 7. New-deck checklist

Build in this order. Decide family at step 1 (seminar: `[10pt]` + footline + auto-outline; flagship: `[presentation]` + color grammar + no outline).

1. Instantiate skeleton (§8). Filename `<Topic> - <YYYYMM>.tex`. Venue string in `\date{}`.
2. Title page: bracket short forms, `\inst{}` institutes, alphabetical short-author.
3. Motivation: 3–5 slides, market-specific. Anchor slide 2 in authority; magnitude by slides 2–4; end with named-firm example.
4. Hypothesis as causal chain in plain bullets.
5. Preview right after Motivation: headline number + t-stat + verdicts + pre-answer to objection.
6. Contribution slide after preview. Literature-only content commented out.
7. Data: sources → sample restrictions with counts → "Measuring X" with toy example → optional descriptive distribution for constructed measure → summary stats in backup.
8. Main results as setup→table pairs. Sort/portfolio first, puzzle-deepener, FM spec (one repeated equation skeleton, focal coefficient red), `\tiny` booktabs table, money row `\rowcolor{blue!30}`, one takeaway bullet with economic magnitude and arithmetic.
9. Robustness as hub: one slide, numbered items, each `\beamerbutton{here}` into backup.
10. Mechanism as largest block: overview + discriminative prediction + setup+table pair per channel + pivotal question-titled slide for rejected explanation.
11. Conclusion mirrors preview, finding-first, 4–5 bullets.
12. Backup arsenal: numbered Robustness battery, subsample/heterogeneity tables, summary stats — every one a `\hypertarget` with "back to main".
13. **Sweep pass:** grep every `\hyperlink` against `\hypertarget`; de-duplicate `\label`s; frametitle rule (reword first, resize fallback); copyedit; fix figure aspect ratios.

---

## 8. Skeleton

```latex
\PassOptionsToPackage{table}{xcolor}
\documentclass[10pt]{beamer}                  % seminar family; flagship line uses [presentation]
\usepackage{amsmath}
\usepackage{sansmathaccent}
\usepackage{tabularx,rotating}
\usepackage{booktabs}
\usepackage{subfigure}
\usepackage{pgfpages}
\usepackage{multirow}
\usetheme{frankfurt}
\usepackage{longtable}
\usepackage{comment}
\usepackage{textcomp}
\usepackage{supertabular}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{adjustbox}
\usepackage[utf8]{inputenc}
\usepackage{newunicodechar}
\usepackage{colortbl,xcolor}                  % for color grammar (flagship)
\definecolor{lg}{rgb}{0.8,0.8,1.0}            % periwinkle for \cellcolor{lg}
\newcommand{\hlabel}{\phantomsection\label}
\hypersetup{colorlinks}
\pdfmapfile{+sansmathaccent.map}
\setbeamertemplate{navigation symbols}{}

\defbeamertemplate*{footline}{shadow theme}
{\leavevmode
  \hbox{\begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm
      plus1fil,rightskip=.3cm]{author in head/foot}
      \usebeamerfont{author in head/foot}\hfill\insertshortauthor
    \end{beamercolorbox}
    \begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm,rightskip=.3cm
      plus1fil]{title in head/foot}
      \usebeamerfont{title in head/foot}\insertshorttitle\hfill\insertframenumber\,/\,\inserttotalframenumber
  \end{beamercolorbox}}
  \vskip0pt
}

\newcommand{\backupbegin}{
  \newcounter{framenumberappendix}
  \setcounter{framenumberappendix}{\value{framenumber}}
}
\newcommand{\backupend}{
  \addtocounter{framenumberappendix}{-\value{framenumber}}
  \addtocounter{framenumber}{\value{framenumberappendix}}
}
\newcommand{\nologo}{\setbeamertemplate{logo}{}}

\title[Short Title]{Full Paper Title}
\author[Cui, Li and Zhang]
{Chenyu Cui\inst{1} \and Frank Weikai Li\inst{2} \and Xinyi Zhang\inst{3}}

\institute[]{
  \inst{1} University of International Business and Economics
  \and \inst{2} Singapore Management University
  \and \inst{3} Sun Yat-sen University
}
\date{2022 Research in Behavioral Finance Conference}   % venue string; \today is fallback

\begin{document}
\frame[plain]{\titlepage}

% --- Auto-outline (seminar family only; flagship line comments this out) ---
\AtBeginSection[]
{
  \begin{frame}
    \frametitle{Outline}
    \tableofcontents[currentsection]
  \end{frame}
}

\section{Motivation}
\begin{frame}
  \frametitle{Motivation}
  % 3-5 bullets at \footnotesize; \pause between argument blocks
\end{frame}

% --- Setup -> table pair (exact title repetition; seminar family appends ", result") ---
% Spec slide: \footnotesize bullets + repeated equation with focal coefficient red
% Table slide: same frametitle, \tiny first, booktabs, money row \rowcolor{blue!30},
% focal cells \cellcolor{lg}, one \scriptsize takeaway bullet with magnitude.

% --- Hyperlink hub idiom (outbound "here", inbound "back to main") ---
\begin{frame}
  \frametitle{Robustness Checks}
  \begin{itemize}\hypertarget{robustness}{}\footnotesize
    \item We conduct a battery of robustness tests:
    \item[--] Robustness 1: ... (\hyperlink{robust1}{\beamerbutton{here}})
    \item[--] Robustness 2: ... (\hyperlink{robust2}{\beamerbutton{here}})
  \end{itemize}
\end{frame}

% --- Backup arsenal ---
\section{Appendix}
\backupbegin
\begin{frame}\hypertarget{robust1}{}
  \frametitle{Robustness 1: Scope 2 Emission}
  \tiny
  % table
  \begin{itemize}\footnotesize
    \item Finding restated (back to \hyperlink{robustness}{\beamerbutton{main}})
  \end{itemize}
\end{frame}
\backupend

\end{document}
```
