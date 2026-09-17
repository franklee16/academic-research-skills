---
name: review-paper-2
description: Adversarial paper review simulating a skeptical referee — checks identification, statistical claims, robustness, and presentation against real referee patterns
---

# Review Paper
*v1.1 — Pre-submission self-review combining econ-native evaluation with adversarial stress testing*

Simulate a rigorous peer review of an academic manuscript before submission. Combines economics-specific review criteria (identification strategy, econometric specification) with a Devil's Advocate stress test and editorial synthesis.

**Argument:** `$ARGUMENTS`
- Path to a paper file (`.pdf`, `.tex`, `.qmd`, `.md`, `.docx`)
- Or a project name (will look for the paper in the project's standard locations)

**Modes** (append to argument):
- `full` (default) — 3-pass review: Econ Referee + Devil's Advocate + Editorial Synthesis
- `quick` — Single-pass referee report only (skip DA and synthesis)
- `methodology` — Deep dive on identification and econometrics only
- `da-only` — Devil's Advocate stress test only (skip balanced review)

Example: `/review-paper ~/Dropbox/Github/bd-social-norms/paper/main.tex full`
Example: `/review-paper dep-dts quick`

---

## Instructions

### Step 0: Locate and Read the Paper

1. If `$ARGUMENTS` contains a file path, read that file directly
2. If `$ARGUMENTS` is a project name, check these locations in order:
   - `~/Dropbox/Github/[project]/paper/`
   - `~/Dropbox/Github/[project]/manuscript/`
   - `~/Dropbox/Github/[project]/draft/`
   - Glob for `*.tex`, `*.pdf`, `*.qmd`, `*.docx` in the project repo
3. For PDFs, read in chunks (5 pages at a time). For LaTeX, read the main file and any `\input{}` files.
4. Read the **full paper** end-to-end before starting any review pass.

Parse the mode from `$ARGUMENTS`. Default to `full` if not specified.

5. **Load the reference file** `review-paper-references/real-referee-patterns.md` via the Skill tool. This contains calibration patterns from real referee reports at top journals — use it to ground the review in how actual referees write and what they prioritize.

### Step 1: Econ Referee Pass

Think like a referee at a top-5 economics journal (AER, QJE, Econometrica, JPE, REStud). Evaluate across these 6 dimensions:

#### 1.1 Argument Structure
- Is the research question clearly stated and well-motivated?
- Does the introduction establish the question's importance in 2-3 paragraphs?
- Is the logical flow sound (question -> literature -> method -> results -> conclusion)?
- Are conclusions supported by the evidence presented?
- Are limitations acknowledged honestly?

#### 1.2 Identification Strategy
- Is the causal claim credible? What is the source of exogenous variation?
- Are the key identifying assumptions stated explicitly?
- Threats to identification: omitted variables, reverse causality, measurement error, selection, spillovers, SUTVA violations?
- For RCTs: randomization quality, compliance, attrition, balance, pre-analysis plan adherence?
- For quasi-experimental: parallel trends, exclusion restriction, first-stage strength, bandwidth sensitivity?
- Is the estimator appropriate for the research design (TWFE concerns with staggered adoption, etc.)?
- **Implementation fidelity** (for program evaluations): Was the program delivered as designed? Do deviations (delays, mistargeting, short duration) limit what the paper can claim? Is the paper evaluating the program-as-designed or program-as-implemented?

#### 1.3 Econometric Specification
- Standard errors: clustered at the right level? Robust? Few-cluster corrections needed?
- Functional form: appropriate? Sensitivity to alternatives?
- Sample selection: any concerns about conditioning on post-treatment variables?
- Multiple testing: how many hypotheses tested? Any corrections?
- Are point estimates economically meaningful (magnitude, not just statistical significance)?
- Heterogeneity analysis: pre-specified or exploratory? Appropriate corrections?
- Power: is the study adequately powered for the effects being detected (or not detected)? For null results, report MDEs — what effect sizes can be ruled out?
- **Mechanism evidence**: Does the paper provide *positive* evidence for the claimed mechanism, or only rule out alternatives? Suggest specific heterogeneity analyses that would discriminate between competing explanations.
- **Cost-benefit** (for interventions): Is return on investment discussed? Even back-of-envelope cost per unit of outcome is valuable.

#### 1.4 Literature Positioning & Framing
- Are the key papers in this area cited?
- Is prior work characterized accurately and fairly?
- Is the contribution clearly differentiated from existing work?
- Any missing citations a referee would flag?
- Is the paper positioned in the right literature (not just the convenient one)?
- **Framing breadth**: Could the paper be framed more broadly? Narrow framing undersells the contribution. Avoid "first paper to..." claims — they're debatable and shrink the scope. Help the author see the biggest defensible question their paper answers.
- Does the intro explain what the results *mean* for the existing literature, not just that the paper "contributes to" it?

#### 1.5 Writing Quality
- Clarity and concision (economics papers should be tight)
- Abstract effectively summarizes question, method, findings, and contribution
- Consistent notation throughout
- Tables and figures are self-contained (clear labels, notes, sources, sample sizes)
- Appropriate length for the contribution

#### 1.6 Presentation & Data Transparency
- Are summary statistics presented and discussed?
- Balance tables (for RCTs)? Do they show treatment and control means separately (not just the difference)? Randomization inference? Joint test?
- Are variable definitions clear and documented? For composite indices, are the components listed?
- Is the data section informative about sample construction?
- Are results presented clearly (coefficient, SE, significance, N)?
- Are all tables/figures referenced in the text?
- **Admin vs. self-reported data**: If both exist, are both shown? Are discrepancies discussed as a data quality signal?
- **Table parsimony**: Can ITT and IV be consolidated (one in main tables, one in appendix)? Can related tables be combined?
- **Self-reported outcomes**: Are table titles explicit when outcomes are self-reported?
- **Robustness to controls**: Is there an appendix showing results without baseline controls?
- **Displacement/GE effects**: For labor market papers, is this discussed alongside main results (not just in the conclusion)?

Rate each dimension 1-5 (1 = major problems, 5 = excellent).

Generate **3-5 referee objections** — the tough questions a top referee would ask. For each:
- State the objection clearly
- Explain why it could be fatal or damaging
- Suggest how the author could address it

**If mode = `quick` or `methodology`**: Write the review report (see output format below) and stop here. For `methodology`, focus only on dimensions 1.2 and 1.3.

---

### Step 2: Devil's Advocate Stress Test

*Skip if mode = `quick` or `methodology`.*

Switch perspective entirely. You are no longer a balanced reviewer — you are an adversarial critic whose job is to find every vulnerability. This is separate from Step 1; do not repeat the same points.

Run these 8 challenges:

#### 2.1 Core Thesis Challenge
Construct the **strongest possible argument against** the paper's main conclusion. Write 200-300 words making the case that the paper is wrong.

#### 2.2 Cherry-Picking Detection
- Are results selectively reported? Are there specifications that were likely run but not shown?
- Does the paper emphasize its strongest results while burying weaker ones?
- Is the sample definition suspiciously convenient for the results?

#### 2.3 Confirmation Bias Scan
- Does the paper only cite evidence supporting its hypothesis?
- Are contradictory findings from other studies discussed?
- Is the theoretical framework chosen because it predicts the "right" result?

#### 2.4 Logic Chain Validation
Trace the argument from assumptions through to conclusions. Identify any point where the chain breaks or requires an unstated leap.

#### 2.5 Overgeneralization Check
- Do the results generalize beyond the specific sample/context studied?
- Does the paper claim more generality than the evidence supports?
- External validity: would this hold in other countries/time periods/populations?

#### 2.6 Alternative Explanations
List 2-4 alternative explanations for the main results that are **not adequately ruled out**. For each, explain what additional evidence would distinguish the author's story from the alternative.

#### 2.7 Stakeholder Blind Spots
- Whose perspective is missing from the analysis?
- Are there distributional effects or welfare implications not discussed?
- Would practitioners/policymakers interpret these results differently than the authors intend?

#### 2.8 "So What?" Test
- If the results are exactly right, what changes? Who acts differently?
- Is the contribution incremental or transformative?
- Does the paper answer a question people are actually asking?

Classify each finding as:
- **CRITICAL**: Fatal flaw in core argument — cannot be rescued without fundamental revision
- **MAJOR**: Seriously undermines credibility but can be addressed with additional analysis/writing
- **MINOR**: Worth noting but does not affect core argument
- **OBSERVATION**: Not a defect, but an alternative perspective worth considering

**If mode = `da-only`**: Write the Devil's Advocate report and stop here.

---

### Step 3: Editorial Synthesis

*Only runs in `full` mode.*

Now step back and synthesize Steps 1 and 2 into an editorial decision. Think like an editor making a desk decision.

#### 3.1 Consensus Analysis
- Where do the referee evaluation and Devil's Advocate agree? (These are the strongest signals.)
- Where do they disagree? (The DA may have been too harsh, or the referee too generous.)
- Which DA findings are genuine threats vs. hypothetical concerns unlikely to bother a real reviewer?

#### 3.2 Decision
Based on the synthesis:
- **Strong Accept**: Excellent across all dimensions, DA found only minor/observation-level issues
- **Accept with Minor Revision**: Strong paper, 1-2 addressable issues, no DA critical findings
- **Revise and Resubmit**: Good potential, but 2+ major issues or 1 DA critical finding that can be addressed
- **Reject**: Fundamental identification/argument problems that cannot be fixed with revision

#### 3.3 Revision Roadmap
Organize all findings into a prioritized action list:
- **Priority 1 (Required)**: Must fix before submission — fatal or near-fatal issues
- **Priority 2 (Strongly Recommended)**: Will significantly strengthen the paper
- **Priority 3 (Nice to Have)**: Polish items, additional robustness checks, framing improvements

---

### Step 4: Write the Report

Save the full report to the working directory as `review_[sanitized_paper_name]_[YYYY-MM-DD].md`.

Tell the user the full path to the output file.

---

## Output Format

```markdown
# Manuscript Review: [Paper Title]

**Date:** [YYYY-MM-DD]
**Mode:** [full / quick / methodology / da-only]
**File reviewed:** [path to manuscript]
**Reviewer:** /review-paper skill v1.0

---

## Summary Assessment

**Overall recommendation:** [Strong Accept / Accept with Minor Revision / Revise and Resubmit / Reject]

[2-3 paragraph summary: main contribution, key strengths, and central concerns. Be direct.]

---

## Econ Referee Report

### Dimension Scores

| Dimension | Score (1-5) | Key Issue |
|-----------|:-----------:|-----------|
| Argument Structure | | |
| Identification Strategy | | |
| Econometric Specification | | |
| Literature Positioning | | |
| Writing Quality | | |
| Presentation & Data | | |
| **Overall** | **[avg]** | |

### Strengths

1. [Strength — be specific, cite sections/tables]
2. [...]
3. [...]

### Major Concerns

#### MC1: [Title]
- **Dimension:** [which of the 6]
- **Issue:** [specific description]
- **Suggestion:** [how to address it]
- **Location:** [section/page/table]

[Repeat for each major concern]

### Minor Concerns

#### mc1: [Title]
- **Issue:** [description]
- **Suggestion:** [fix]

[Repeat]

### Referee Objections

#### RO1: [The tough question]
**Why it matters:** [why this could be fatal or damaging]
**How to address it:** [suggested response or additional analysis]

[Repeat for 3-5 objections]

---

## Devil's Advocate Report

*(Only in `full` and `da-only` modes)*

### Strongest Counter-Argument
[200-300 words. The single best case that the paper's conclusion is wrong.]

### Critical Findings
[Any CRITICAL-severity issues. If none, state "No critical findings."]

### Major Findings
[MAJOR-severity issues with challenge number (2.1-2.8)]

### Minor Findings & Observations
[Brief list]

### Alternative Explanations Not Ruled Out
1. [Alternative — what evidence would distinguish it]
2. [...]

---

## Editorial Synthesis

*(Only in `full` mode)*

### Consensus Points
[Where referee and DA agree — these are the most important signals]

### Areas of Disagreement
[Where DA was harsher than the referee assessment warrants, or vice versa]

### Decision Rationale
[2-3 sentences explaining the recommendation]

### Revision Roadmap

#### Priority 1: Required Before Submission
- [ ] [Action item with specific guidance]
- [ ] [...]

#### Priority 2: Strongly Recommended
- [ ] [Action item]
- [ ] [...]

#### Priority 3: Nice to Have
- [ ] [Action item]
- [ ] [...]

---

## Specific Comments

[Section-by-section or line-by-line comments, if any. Include page/paragraph references.]
```

---

## Principles

- **Be constructive.** Every criticism comes with a suggestion. The goal is to make the paper better, not to tear it down.
- **Be specific.** Reference exact sections, equations, tables, page numbers.
- **Think like a top-5 referee.** What would make them recommend rejection? What would make them enthusiastic?
- **Distinguish fatal flaws from polish.** Not everything is equally important. Prioritize.
- **Acknowledge what's done well.** Good research deserves recognition. Acknowledge difficulty of execution: "Successful evaluations of government programs are very challenging."
- **Economics-specific lens.** Identification, not just "methodology." Economic significance, not just statistical significance. Credibility revolution standards.
- **Be honest about uncertainty.** If you're unsure whether data exists, say so: "I don't know if this data exists, but..."
- **Offer choices, not mandates.** For presentational suggestions, give the author latitude: "I would leave it to you to decide."
- **Framing advice is a gift.** When a paper is framed too narrowly, suggesting a broader frame helps the author — it's not a criticism.
- **Do NOT fabricate.** If you cannot read a section clearly, say so. Do not invent details about the paper.
- **Do NOT hallucinate citations.** If you suggest missing references, flag that the user should verify they exist.
