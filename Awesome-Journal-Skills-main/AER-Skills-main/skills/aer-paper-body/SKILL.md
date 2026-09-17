---
name: aer-paper-body
description: Use when drafting or revising the body sections of an AER, AER:Insights, or AEJ manuscript — institutional background, data, empirical strategy, results, mechanisms, and conclusion. Covers equation conventions, results-paragraph narration, magnitude interpretation, and back-of-envelope policy calculations. Apply after the empirics are stable and before or alongside aer-introduction.
---

# AER Paper Body

## Overview

The introduction decides whether the editor sends the paper out; the **body
sections decide what the referees write**. Referees spend most of their time in
Data, Empirical Strategy, and Results — checking whether the estimand is
defined, the assumption is stated, the magnitudes are interpreted, and the
prose matches the tables. This skill covers everything between the
introduction and the bibliography.

Write the body **before** polishing the introduction. The introduction
summarizes a paper that already exists; drafting it first produces promises
the body then fails to keep.

## When to Use

- The empirics are stable (after `aer-identification` and `aer-robustness`)
  and the manuscript needs full section drafts
- A results section reads like a table walk-through ("Column 1 shows...
  Column 2 shows...") and needs narration surgery
- A referee or editor said the paper is "hard to follow," "under-interpreted,"
  or "reads like a report"
- Coefficients are reported but never converted into economic magnitudes
- The conclusion restates the abstract and needs to do real work

## Canonical Section Architecture

A full-length empirical AER paper, after the unlabeled introduction:

```
I.   Background  (or: Institutional Setting; Policy Context)
II.  Data        (sources, sample construction, measurement, summary stats)
III. Empirical Strategy   (estimand, equation, identifying assumption, inference)
IV.  Results     (main estimates, dynamics, robustness pointers)
V.   Mechanisms  (or: Heterogeneity and Mechanisms; Interpretation)
VI.  Conclusion
```

Variants:

- A **conceptual framework** section, when used, goes between Background and
  Data (or replaces Background for theory-led papers).
- *AER: Insights* compresses to roughly: Data and Design → Results →
  Discussion. Same disciplines, fewer headings.
- Structural papers insert Model and Estimation sections; the rules below
  about defining notation and stating assumptions apply with more force, not
  less.

One ordering rule binds everywhere: **every term, dataset, and design feature
is defined before first use**. Referees read linearly on the first pass.

## Section I — Background / Institutional Setting

Purpose: give the reader exactly the institutional detail needed to (a)
understand where the identifying variation comes from and (b) believe the
identifying assumption. Nothing else.

- Lead with the institution or policy, not the literature. History belongs
  here only if it explains the variation.
- State **who is treated, when, by what rule, and who decided**. The
  assignment rule is the soul of the design; if it is discretionary, say so
  and explain how the design handles it.
- Length: 1.5-3 typeset pages. If it runs longer, the surplus is almost
  always literature review in disguise — cut it or move it to the intro's
  antecedents paragraph.
- Every institutional claim gets a citation to a primary source (statute,
  agency document, administrative report) — not to another economics paper
  that also cites it secondhand.

Failure modes: a Wikipedia-style policy history; background that never
mentions the variation the design uses; institutional facts stated from
memory without a source.

## Optional Section — Conceptual Framework

Include a framework section only if it does at least one of:

1. **Generates a testable prediction** the empirics then test (especially a
   sign or heterogeneity prediction that distinguishes mechanisms)
2. **Defines the estimand's welfare interpretation** (maps a reduced-form
   coefficient into a sufficient statistic)
3. **Disciplines magnitudes** (tells the reader what effect size theory
   permits)

Rules:

- Keep it **stylized**: two-period, two-type, linear where possible. Push
  derivations to the appendix; state propositions and intuition in the text.
- End the section with an explicit bridge: "The framework yields two
  predictions we take to the data: first ...; second ...". Each prediction
  must reappear, by name, in Results or Mechanisms.
- Do not bolt on a model that merely re-derives "demand slopes down."
  Referees treat decorative theory as padding and will say so.

## Section II — Data

Referees check this section against the replication package line by line.
Structure it in four blocks:

### A. Sources

For each dataset: name, producer, access mode, years covered, unit of
observation, and a citation. If access is restricted, say how it was obtained
(this also feeds `aer-replication`).

### B. Sample construction

The single most under-written block in rejected papers. Report the funnel
explicitly, with counts:

> "The raw file contains 48,212 establishments. We drop establishments with
> fewer than five employees (6,103), those never observed before treatment
> (2,914), and those with missing wage data in more than two years (1,371),
> leaving an analysis sample of 37,824."

Every drop needs a rationale. If a restriction is consequential, flag that
the robustness section relaxes it. The funnel counts must match the
replication package exactly — `aer-consistency` will audit this.

### C. Variable definitions and measurement

- Define the outcome and treatment precisely, with units, in prose (the full
  variable table can live in the appendix).
- Discuss measurement error where a referee would: self-reported outcomes,
  imputation, top-coding, deflators (name the index and base year).
- State the level of aggregation and why it matches the design.

### D. Summary statistics

Narrate Table 1 — do not re-read it aloud. The paragraph answers three
questions: Is the sample representative of the population the question is
about? Are treatment and comparison groups comparable pre-treatment? Are
there features (skewness, mass points, attrition) that shape specification
choices? Two to four facts, each tied to a design decision.

## Section III — Empirical Strategy

The section referees read most carefully. Four mandatory components, in
order: **estimand → equation → identifying assumption → inference**.

### Estimand first

One sentence, before any equation: "Our object of interest is the average
effect of [treatment] on [outcome] among [population], [horizon]." If the
design recovers a local effect (LATE, effects at the cutoff, ATT for
switchers), say so here, not in the conclusion's limitations paragraph.

### Equation conventions

```latex
Y_{ict} = \beta\, D_{ct} + \alpha_c + \gamma_t + X_{ict}'\delta + \varepsilon_{ict}
```

- **Define every symbol** in the sentence immediately following the equation,
  including subscripts: "where $Y_{ict}$ is log earnings of worker $i$ in
  county $c$ in year $t$; $D_{ct}$ indicates ...; $\alpha_c$ and $\gamma_t$
  are county and year fixed effects."
- Subscript order is consistent across all equations and matches the tables.
- Number every displayed equation; refer to them as "equation (1)."
- State which coefficient is the object of interest and what variation
  identifies it after controls and fixed effects absorb the rest: "β is
  identified from within-county changes in $D_{ct}$ around the staggered
  adoption dates."
- For modern DiD estimators, write the ATT(g,t) estimand and aggregation
  explicitly rather than pretending the design is equation-(1) TWFE — the
  estimator choice itself comes from `aer-identification`.

### Identifying assumption

State it formally **and** in words, then preview the evidence:

> "Identification requires that, absent the reform, treated and not-yet-
> treated counties would have followed parallel wage trends (Assumption 1).
> Three pieces of evidence support this: the event-study coefficients in
> Figure 2 are flat pre-treatment (joint test p = 0.71); ..."

The triplet "assumption — threat — evidence" is the unit of writing here.
Name the two or three most plausible violations a referee will raise and
point to where each is addressed.

### Inference

One short paragraph: clustering level and why it matches the design's level
of variation, number of clusters, and any small-cluster correction (wild
cluster bootstrap) or design-specific inference (AR confidence sets,
randomization inference, permutation p-values). Never leave inference to the
table notes alone.

## Section IV — Results

### The narration discipline

One paragraph per claim — not per table. Each results paragraph has a fixed
internal anatomy:

1. **Finding first.** The opening sentence states the economic finding with
   its magnitude — not the table's existence. Write "The reform raises
   earnings by 4.2 percent (Table 3, column 4)," never "Table 3 presents the
   results of estimating equation (1)."
2. **Evidence.** Walk the reader through where the number comes from and how
   it moves across specifications: "The estimate is stable as we add county
   trends (columns 2-3) and shrinks only modestly with matched-pair fixed
   effects (column 4)."
3. **Interpretation.** Convert the coefficient into economic units and
   benchmark it (rules below).

Column-by-column narration without a finding-first sentence is the most
reliable marker of a weak results section.

### Magnitude interpretation rules

Every headline coefficient gets all three conversions:

1. **Native units.** Log-outcome coefficients are *log points*: β = 0.042 is
   "4.2 log points," or exactly 100·(e^0.042 − 1) = 4.3 percent. Use the
   exact conversion whenever |β| > 0.10; below that, log points ≈ percent is
   acceptable if labeled. Never confuse **percent** with **percentage
   points**: a 2pp rise from a 10 percent base is a 20 percent increase —
   write whichever the sentence means.
2. **Relative to the sample.** Express the effect against the dependent
   variable's mean (or SD, for index outcomes): "4.3 percent of the sample
   mean, or 0.11 standard deviations."
3. **Relative to the literature or a policy lever.** "Roughly half the
   effect of an additional year of schooling in this population" or "the
   equivalent of moving a county from the 25th to the 40th percentile of the
   broadband distribution."

For binary outcomes, report the baseline rate next to every marginal effect.
For elasticities, state both numerator and denominator changes. If the
implied magnitude is implausibly large, say so and investigate **before** a
referee does — implausible magnitudes draw harsher reports than honest nulls.

### Precision language

- "Statistically significant at the 5 percent level" — never "almost
  significant," "marginally insignificant," or significance implied by stars
  alone.
- For null results: report the CI and what it rules out — "the 95 percent
  confidence interval excludes effects larger than 1.8 percent, one-quarter
  of the effect in [antecedent]." Distinguish a precise zero from an
  uninformative one.
- The text quotes point estimates and standard errors exactly as the table
  shows them. Paraphrased or re-rounded numbers are how text-table
  inconsistencies (and referee distrust) start.

### Back-of-envelope policy calculation

High-impact AER results sections close with one disciplined aggregate
calculation: state every input and its source, multiply through in one
visible chain, and round honestly.

> "The point estimate implies that the \$4.5 billion program raised annual
> earnings by \$310 per covered worker (0.042 × \$7,400 baseline ×
> coverage). Against a per-worker cost of \$240, the implied first-year
> benefit-cost ratio is 1.3, before any productivity spillovers."

One calculation, in the text, with inputs traceable — not a cascade of
unsourced multiplications. If the calculation deserves more than a
paragraph, it becomes its own short section (as in the broadband example's
benefit-cost section).

### Robustness pointers

The main results section cites robustness, it does not contain it: one
paragraph summarizing the battery from `aer-robustness` ("The estimate is
stable across [clustering, sample, specification] variants; Section [V] /
Appendix [B] reports the full set") plus the single most important check
shown inline.

## Section V — Mechanisms

Organize by **candidate explanation**, not by table:

1. Open by naming the two or three channels consistent with the main result,
   including the ones you will rule out.
2. For the favored channel: present the theory-predicted heterogeneity and
   auxiliary outcomes ("if the channel is skill-biased adoption, effects
   should concentrate in tradeable services — they do, Table 5").
3. For each alternative: state the sharpest version of the referee's
   objection, then the evidence against it. Steelman first, then answer.
4. Close with calibrated language: "the evidence is most consistent with
   [channel]" — not "we prove the mechanism is [channel]." Mechanism evidence
   is consistency evidence; only the main effect carries design-based
   identification (see `aer-identification` on this distinction).

## Section VI — Conclusion

The conclusion is **short** (half a page to one page) and does four things:

1. Restate the question and the headline magnitude in fresh words — do not
   copy abstract sentences (`aer-consistency` flags verbatim duplication).
2. State the external-validity boundary honestly: what population, period,
   and policy margin the estimate speaks to, and the compliers/locality
   caveat if the design implies one.
3. Draw the policy or theory implication the evidence actually supports —
   one step beyond the results, never three.
4. At most two sentences on open questions — specific ones this paper makes
   answerable, not "more research is needed."

No new results, no new citations, no new caveats that belong in Results.

## Cross-Section Consistency Rules

- The introduction's promises (contributions, magnitudes, evidence list) map
  one-to-one onto body sections; nothing promised is undelivered and nothing
  major appears unannounced.
- Numbers, sample sizes, and specification labels match the tables exactly,
  everywhere — `aer-consistency` audits this before submission.
- Tense: present for what the paper does and finds ("we estimate," "the
  effect is"); past for data collection and historical events.
- Prose style follows `docs/style-guide.md` — finding-first sentences, no
  filler transitions, no AI-pattern tics.

## Common Failure Modes

- A results section that narrates tables instead of findings
- Coefficients never converted out of log points; magnitudes never
  benchmarked
- The estimand defined nowhere; "the effect" means three populations in
  three sections
- Sample funnel absent, so the referee reconstructs (and mistrusts) the Ns
- Mechanisms section organized as "more regressions" with no candidate
  channels named
- A two-page conclusion introducing limitations the results section hid
- Institutional background with no source for any factual claim

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the
relevant resource:

- Worked results-section narration (same fictional paper as the intro
  example): `examples/results-section-example.md`
- Sentence- and paragraph-level prose rules: `docs/style-guide.md`
- Estimator, diagnostic, and citation defaults for Section III:
  `docs/methods-reference.md`
- Model introduction the body must stay consistent with:
  `examples/intro-example.md`
- Code that should produce every number quoted in Results:
  `templates/stata/`, `templates/r/`, or `templates/python/`

## Handoff

```text
SECTIONS DRAFTED: <Background | Framework | Data | Strategy | Results | Mechanisms | Conclusion>
ESTIMAND STATED: <yes / no — sentence>
SAMPLE FUNNEL REPORTED: <yes / no>
HEADLINE MAGNITUDE CONVERSIONS: <log-points / percent / vs-mean / vs-literature>
BACK-OF-ENVELOPE CALCULATION: <present / not applicable>
MECHANISM CHANNELS: <favored + ruled-out list>
NEXT SKILL: <aer-introduction | aer-tables-figures | aer-consistency>
```

## Anti-Patterns

- Writing the introduction first and forcing the body to keep its promises
- "Table 4 shows the results. Column 1 reports... Column 2 reports..." — a
  reader gains nothing the table did not already give
- Reporting a 0.31 log-point effect as "31 percent" (it is 36 percent)
- A "conceptual framework" added after the results to decorate them, making
  no prediction the paper tests
- Mechanisms claimed with the same confidence as the identified main effect
- Conclusion paragraphs recycled verbatim into the abstract and introduction
