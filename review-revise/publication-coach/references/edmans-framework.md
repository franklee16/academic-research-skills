# Edmans' Rejection Framework — Detailed Criteria

Based on "Learnings From 1,000 Rejections" by Alex Edmans (Review of Finance, 2023).
This reference contains the detailed diagnostic criteria for each dimension.

---

## Dimension 1: CONTRIBUTION (Weight: 50%)

The single biggest reason for rejection. A paper must not just be new — it must be
sufficiently new, sufficiently important, and sufficiently well-scoped.

### 1.1 Novelty (Is the result surprising?)

**Green flags:**
- The result challenges an established view or prior finding
- The result was not predictable from combining existing literature
- The paper identifies a new mechanism that changes interpretation of prior results
- A new dataset or setting that genuinely adds knowledge (not just geographic extension)

**Red flags:**
- The result is a "convex combination of results already known" — if X→Z and Z→Y are both known, X→Y is not surprising
- The paper extends a known result to a new country/industry/crisis without explaining why results would differ there
- The paper documents a result in a specific setting when the general result is already known
- The contribution is documenting a channel through which a known result operates, but the channel does not change the interpretation
- "Research by matrix" — finding an empty cell (X₂→Y₂) where X₁→Y₁, X₁→Y₂, X₂→Y₁ are already known, but the cell is empty because nobody found it interesting

**Diagnostic questions:**
- Would a reader Bayesian update after reading this paper? By how much?
- Could a reader have predicted this result before reading the paper?
- If the reader had 2 hours with the paper, would they learn something they couldn't have guessed?
- Does the paper pass the "social welfare" test — does the benefit of reading exceed the cost?

### 1.2 Importance (Does it matter?)

**Green flags:**
- The result would likely appear in a survey paper on the topic
- A policymaker or practitioner would change behavior based on the finding
- The effect size is first-order, not second-order

**Red flags:**
- X is "just another" determinant of Y among many already-known determinants
- The result is second-order relative to the main variables already studied
- The magnitude is economically small even if statistically significant
- Documenting channels that don't change interpretation of the main result ("Section 6.2 result")
- The result reinforces what we already know but doesn't change views

**Diagnostic questions:**
- Would a survey paper on determinants of Y mention X?
- Would a manager deciding Y pay attention to X?
- Is the result "the rabbit in a horse-and-rabbit stew"?

### 1.3 Journal Fit (Right audience?)

**Green flags:**
- Most references are from finance journals
- The paper studies finance outcomes (stock returns, dividend policy, leverage, compensation, firm value)
- A general finance reader would at least read the abstract

**Red flags:**
- The paper is really about accounting, operations research, organizational behavior, or macroeconomics
- Most references are from non-finance journals
- Most references are from field journals rather than general-interest journals
- The topic is so niche that "many readers might not know what X is"
- X is the "end goal" but finance journals have real/financial variables as the end goal

**Diagnostic questions:**
- What fraction of the bibliography is from finance journals?
- What fraction is from field journals vs. general-interest journals?
- Would a general finance reader read the abstract?
- Does the paper study finance outcomes or just use finance data?

### 1.4 Generalizability (External validity?)

**Green flags:**
- Large-sample, multi-country or multi-period evidence
- The setting has features that make results plausibly generalizable
- If a single event/case study, the paper focuses on the event itself rather than claiming general lessons

**Red flags:**
- Single-case study used to draw general conclusions about X→Y
- Results from one narrow setting with no argument for why they extend
- The paper's question is general but the setting is very specific

**Diagnostic questions:**
- Is the sample representative or idiosyncratic?
- Are there logical reasons the results would extend to other settings?
- If narrowed to the specific setting, would the contribution still be publishable?

### 1.5 Trade-Off Balance (Costs AND benefits?)

**Green flags:**
- The paper considers both costs and benefits of X
- If studying one side, the cost/benefit was not obvious
- The paper addresses whether X creates value overall, not just whether X increases Y

**Red flags:**
- The paper claims X "creates value" but only studies benefits, not costs
- The paper's question is about overall value creation but only documents one side
- The benefit documented is obvious/predictable, making the one-sided analysis insufficient

**Diagnostic questions:**
- Does the paper's stated question require showing both sides?
- If the paper only shows benefits (costs), are those benefits (costs) surprising enough on their own?
- Would a reader know whether X is desirable after reading the paper?

### 1.6 Hypothesis Clarity (Clear, directional, theory-grounded?)

**Green flags:**
- Clear directional hypothesis with theoretical backing
- Hypotheses that could be falsified
- Hypotheses formed before data analysis (credible pre-registration)
- Conflicting hypotheses (A predicts +, B predicts -) that the data can distinguish

**Red flags:**
- Hypothesis is so weak that even a strong correlation is likely spurious
- Arguments support the level of Y but the paper studies the efficiency of Y (or similar mismatch)
- Hypothesis concerns Y₁ but paper studies Y₂, where Y₁→Y₂ direction is ambiguous (complements vs. substitutes)
- "It's an empirical question" used as defense for unclear hypothesis
- No directional hypothesis — differences in either direction count as "victory"
- Kitchen-sink approach: regressing Y on every available X without hypotheses
- Cross-sectional tests without directional predictions

**Diagnostic questions:**
- Can you state the hypothesis in one sentence with a clear direction?
- Could the hypothesis have been reverse-engineered from the results?
- Would the opposite result also have been claimed as supporting the paper?
- Is there a theoretical reason for the specific direction predicted?

---

## Dimension 2: EXECUTION (Weight: 30%)

Execution issues are often paper-specific, but two recurring themes appeared.

### 2.1 Instrumental Variables Validity

**Green flags:**
- Instruments are clearly described and justified in the introduction, not buried
- The instrument satisfies both relevance and exclusion restriction with clear economic reasoning
- The paper explains the specific endogeneity problem before proposing the solution
- Instruments come from outside the system

**Red flags:**
- Instruments are mentioned in the introduction but not described (suspicious burial)
- Peer group averages used as instruments — nearly never valid (Gormley and Matsa, 2013)
- Lagged variables used as instruments — within the system, subject to same omitted variable and reverse causality concerns
- Statistical tests (overidentifying restrictions) used to "prove" validity — they cannot (Roberts and Whited, 2013)
- Paper justifies instrument by citing other papers that used it, even if those papers are unpublished or the methodology is now considered flawed
- Endogeneity addressed without first diagnosing what the specific problem is

**Diagnostic questions:**
- Does the paper explain its instruments in the introduction?
- Does the instrument come from outside the system?
- Is there a clear economic argument for why the exclusion restriction holds?
- Is the specific endogeneity concern diagnosed before solutions are proposed?
- Is there actually an endogeneity problem, or is IV used defensively?

### 2.2 Functional Form and Measurement

**Green flags:**
- Count variables used in levels or with appropriate models (Poisson, negative binomial)
- Economic significance reported alongside statistical significance
- Variable transformations have clear economic interpretations

**Red flags:**
- log(1 + x) transformation for count data with many zeros — coefficient is uninterpretable, results are sensitive to the arbitrary choice of adding 1 (see Cohn, Liu, and Wardlaw, 2022)
- Adding a constant before logging is arbitrary (could add 0.1 or 2 instead of 1)
- No economic significance reported

---

## Dimension 3: EXPOSITION (Weight: 20%)

Exposition alone rarely causes rejection, but it tips close decisions and slows review.

### 3.1 Clarity and Professionalism

**Green flags:**
- Paper is carefully proofread with no elementary errors
- Abstract contains a specific number of economic significance the reader can remember
- Introduction is self-contained: hypotheses, identification, data, results, economic significance
- Linear argument structure — one point at a time, not Hamlet-soliloquy back-and-forth
- Consistent formatting, bibliography style, table appearance

**Red flags:**
- Elementary typos and grammatical errors (signal carelessness in coding/proofs too)
- No economic significance in the abstract or introduction
- Introduction reads like a Hamlet soliloquy — starts with one point, flips to counterpoint, back and forth
- Literature review interleaved with contribution rather than separate
- Abstract page not labeled p1 (causes confusion in referee comments)
- Inconsistent bibliography formatting (some italics, some not)
- Tables/figures look sloppy

**Diagnostic questions:**
- Can you state the paper's economic significance from memory after reading the abstract?
- Does the introduction contain all essential elements (hypotheses, ID, data, results, economic magnitude)?
- Is the argument linear or circular?
- Are there more than minor typos?

### 3.2 Length Discipline

**Green flags:**
- Introduction is 4-6 pages maximum
- The paper starts with context then goes immediately to the contribution
- Related literature discussed after the contribution, not before
- Few footnotes (aim for ≤1 per page)

**Red flags:**
- Introduction exceeds 6 pages (most max out at 6)
- Multiple pages spent motivating the importance of the topic (climate change, COVID, innovation) — any academic reader already knows
- Literature review starts before the paper's own contribution is explained
- Introduction goes back-and-forth between contribution and related literature
- Excessive footnotes (more than 1 per page average) — suggests hedging about what's central
- Total bibliography exceeds 5-6 pages for a standard empirical paper

**Diagnostic questions:**
- How long is the introduction? (Ideal: 4-6 pages)
- How many pages before the research question is stated?
- Is the contribution explained before the literature review?
- How many footnotes per page?

### 3.3 Citation Discipline

**Green flags:**
- Every cited paper is cited for a specific result or contribution, not institutional facts
- Bibliography is focused on directly relevant work
- Survey papers are cited for broad literature rather than listing many individual papers

**Red flags:**
- Papers cited for institutional facts they did not discover (e.g., "ESG has become more important (Edmans, 2023)" — that's a fact, not Edmans' contribution)
- Papers cited for using common methodologies (fixed effects, control variables) — anyone would use these
- Papers cited for well-known variables or datasets (Tobin's Q attributed to specific recent papers rather than Tobin)
- Papers mis-cited — credited for topics they don't actually study
- Vague connections to multiple literatures to appear broadly relevant ("we have implications for dividend policy" without saying what)
- Bibliography reads like a Masters thesis — citing many tangentially related papers

**Diagnostic questions:**
- For each citation: is the paper cited for a specific result it discovered, or for an institutional fact/methodology it used?
- Could the sentence stand without the citation? If yes, the citation may be unnecessary.
- Are there citations to papers in popular fields that are only tangentially related?
- Are any papers mis-cited (credited for something they don't study)?

---

## Scoring Rubric

Each sub-criterion is scored on a 1-5 scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | No concerns; this dimension is a strength of the paper |
| 4 | Good | Minor concerns that are easily addressed |
| 3 | Adequate | Moderate concerns; some revision needed |
| 2 | Weak | Significant concerns; major revision needed |
| 1 | Critical | Fundamental flaw; likely a desk-reject reason |

### Weighted Score Calculation

- **Contribution** (50%) = average of novelty, importance, journal fit, generalizability, trade-off balance, hypothesis clarity
- **Execution** (30%) = average of IV validity, functional form/measurement
- **Exposition** (20%) = average of clarity, length discipline, citation discipline
- **Overall** = 0.50 × Contribution + 0.30 × Execution + 0.20 × Exposition

### Overall Verdict Thresholds

| Overall Score | Verdict | Action |
|---------------|---------|--------|
| 4.0-5.0 | Publishable | Paper is competitive for top journals |
| 3.0-3.9 | Borderline | Could succeed with targeted improvements |
| 2.0-2.9 | Unlikely | Fundamental issues need addressing; consider lowering target journal |
| 1.0-1.9 | Not viable | Core contribution is insufficient; major rethink needed |

### Desk-Reject Flags

Any single sub-criterion scoring 1 automatically triggers a desk-reject warning,
regardless of the overall score. The most common desk-reject triggers are:
- Novelty = 1 (result is entirely predictable from prior literature)
- Importance = 1 (nobody would include this in a survey)
- Hypothesis clarity = 1 (no testable hypothesis)
- IV validity = 1 (fundamentally invalid instruments)
