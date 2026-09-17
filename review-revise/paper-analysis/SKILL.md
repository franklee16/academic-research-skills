---
name: paper-analysis
description: >
  Critically read and analyze research papers using the 7-step Cornwell framework
  (Aerial View, Interrogation, Verdict). TRIGGER when: "analyze this paper", "critically read",
  "break down this paper", "what are the strengths and weaknesses", "evaluate this research",
  "read this paper critically", "seminar prep", "understand this paper", "paper analysis",
  "dissect this paper", "deep dive", "critical appraisal", or when user provides a DOI/URL/PDF
  with any analysis request. Also trigger for methodology quality, research gaps, alternative
  explanations, or confounding factors. NOT for formal journal peer review (use peer-review).
  NOT for finance editorial review (use paper-editor). NOT for multi-paper synthesis (use lit-review).
  This is for personal learning and deep critical reading for early-career researchers.
---

# Paper Analysis: 7-Step Critical Reading Framework

This skill applies Jacques Cornwell's 7-step framework (Nature Careers, 2026) for critically analyzing research papers. The framework is organized into three phases: Aerial View, Interrogation, and Verdict.

## Input Handling

The skill accepts input in two forms:

**URL/DOI detected** (input contains `doi.org`, `10.`, `http`, or a bare DOI pattern):
1. Use `firecrawl-scrape` or `WebFetch` to retrieve the paper
2. Extract title, abstract, figures, tables, and body text
3. If direct retrieval fails, use `mcp__tavily__tavily-search` to find a cached or linked version

**PDF path detected** (input ends with `.pdf` or is a file path):
1. Use the `pdf` skill to extract text from the PDF
2. Extract title from metadata, then body text section by section

**If ambiguous:** Ask the user to clarify whether they provided a URL/DOI or a local PDF path.

---

## Phase 1: The Aerial View (Steps 1-3)

Before diving into P values and complex methodology, understand the landscape of the paper.

### Step 1: Get a Broad Overview

Resist the urge to dive straight into dense methodology. Instead:

- Read the abstract thoroughly (1-2 passes)
- Review all figures and tables -- note their titles, axes, sample sizes
- Note the journal, publication year, author affiliations
- Form a first impression: Is this empirical, theoretical, review, or methods paper?

**Output for Step 1:** A 2-3 sentence "paper persona" describing what kind of paper this is.

### Step 2: Identify the Core Research Question

Every good piece of research hinges on a single, definable question. Although the title and abstract offer hints, the true research question is usually found at the end of the introduction.

- Find what specific hypothesis is being tested
- State it in one precise sentence
- Note whether it is descriptive, causal, predictive, or exploratory

**Output for Step 2:** The research question stated explicitly.

### Step 3: Map the Existing Knowledge Gap

Research doesn't happen in a vacuum; it builds on previous work. A critical reader should understand why the research is being conducted at that moment.

Ask yourself:
- What is already known about this topic?
- What piece of the puzzle is this paper trying to fill?
- Why does filling this gap matter?

Read the introduction to see how the authors frame the current state of the field.

**Output for Step 3:** A 2-3 sentence gap statement.

---

## Phase 2: The Interrogation (Steps 4-5)

Now roll up your sleeves and get into the details. Now that you understand what the authors are trying to achieve, evaluate how well they did it.

### Step 4: Assess the Methodology

This is often the most challenging yet most crucial step of critical appraisal. Compare the core research question (from Step 2) against the paper's methodology.

For each dimension below, rate as **Strong / Adequate / Weak / Unclear** and note specific concerns:

| Dimension | What to Assess |
|-----------|----------------|
| **Tools / Instruments** | Are measurement tools appropriate? Validated? Calibrated? |
| **Sample Size** | Large enough for the analysis type? Power calculation provided? |
| **Controls** | Appropriate control groups or conditions? Are confounders addressed? |
| **Data Quality / Access** | Can the data support the claims? Is there selection bias? |
| **Code Availability** | Is analysis code provided? Open source? Version-tracked? |
| **Reproducibility** | Could another researcher replicate key results from description alone? |

Key questions to ask:
- Did the authors use the right tools for the job?
- Is the sample size large enough to provide adequate statistical power?
- Did they use appropriate positive and negative controls?
- Are the raw data publicly accessible in repositories?
- Have the authors provided computational pipelines or scripts?

**Output for Step 4:** A methodology assessment table with ratings and notes.

### Step 5: Reach Your Own Conclusion

A common mistake is reading the authors' discussion section before looking at the data. The discussion is where the authors interpret their data, and they've had time to shape a narrative.

**Instructions:**
1. Skip or cover the discussion section
2. Go straight to the results section and figures
3. Look at the graphs, read the tables, check the error bars
4. Ask yourself: "What do these data show?"
5. Formulate your own conclusion solely based on the numbers and visual data

**Output for Step 5:** 2-3 sentences as your independent conclusion.

---

## Phase 3: The Verdict (Steps 6-7)

Bring your analysis face-to-face with the authors' narrative to see whether their conclusions hold up.

### Step 6: Reconcile Authors' Conclusion Against Your Own

Now read the authors' discussion and conclusion. Compare their interpretation of the data with the independent conclusion you formed in Step 5.

Ask yourself:
- Do their assertions align with the raw data?
- Are they overstating their findings?
- Is there a gap between your reading and theirs?

Rate alignment: **Strong / Partial / Weak / Contradictory**

**Output for Step 6:** A 2-3 sentence reconciliation assessment.

### Step 7: Consider Alternative Explanations or Confounding Factors

No study is perfect. Before finalizing your appraisal, play devil's advocate.

Ask yourself:
- What confounding variables were not addressed?
- Are there hidden factors that could have skewed the results?
- Do the authors acknowledge the limitations?
- Are the authors heavily funded by a company that benefits from positive results?
- Do they hold patents on the products studied?

**Output for Step 7:** A list of 3-5 alternative explanations or concerns.

---

## Output: Critical Summary Table

After completing all 7 steps, produce the following structured markdown table:

```markdown
# Critical Summary Table: [Paper Title]

**Authors:** [First Author et al.]
**Year / Journal:** [Year] / [Journal]
**Research Question:** [One sentence]
**Knowledge Gap:** [One sentence]

---

## Summary Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Overall Quality** | Strong / Adequate / Weak | [Brief justification] |
| **Methodological Rigor** | Strong / Adequate / Weak | [Specific concerns] |
| **Novelty / Contribution** | Strong / Adequate / Weak | [What is new] |
| **Clarity of Writing** | Strong / Adequate / Weak | [Organization, flow] |
| **Reproducibility** | Strong / Adequate / Weak | [Code, data access] |

---

## Phase 1: Aerial View

**Step 1 - Paper Overview:**
[2-3 sentence paper persona]

**Step 2 - Core Research Question:**
[One precise sentence]

**Step 3 - Knowledge Gap:**
[2-3 sentence gap statement]

---

## Phase 2: Interrogation

**Step 4 - Methodology Assessment:**

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Tools / Instruments** | Strong / Adequate / Weak / Unclear | [Notes] |
| **Sample Size** | Strong / Adequate / Weak / Unclear | [Notes] |
| **Controls** | Strong / Adequate / Weak / Unclear | [Notes] |
| **Data Quality / Access** | Strong / Adequate / Weak / Unclear | [Notes] |
| **Code Availability** | Strong / Adequate / Weak / Unclear | [Notes] |

**Step 5 - My Independent Conclusion:**
[2-3 sentences based solely on the data]

---

## Phase 3: Verdict

**Step 6 - Reconciliation:**

| Aspect | My Conclusion | Authors' Conclusion | Alignment |
|--------|---------------|-------------------|-----------|
| **Primary finding** | [2-3 sentences] | [2-3 sentences] | Strong / Partial / Weak / Contradictory |

**Step 7 - Alternative Explanations & Concerns:**
1. [Alternative explanation or confounding factor 1]
2. [Alternative explanation or confounding factor 2]
3. [Alternative explanation or confounding factor 3]
4. [Limitation not addressed]
5. [Funding / conflict of interest concern, if applicable]

---

## Strengths

- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

## Weaknesses

- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

---

## Quick Takeaway (for early-career researchers)

[2-3 sentences: What is the single most important thing to remember from this paper?
 What should a researcher take away?]
```

---

## Tips for Early-Career Researchers

1. **Time investment:** Deep analysis takes 1-2 hours per paper. Reserve this for high-impact papers that directly shape your research.

2. **AI usage:** This framework builds your own analytical skills. AI can help navigate literature broadly, but use this manual process to maintain your scientific intuition.

3. **Recording notes:** Record your thoughts in a notebook or reference management software. The act of writing reinforces learning.

4. **Practice:** With experience, you'll internalize these steps and perform them faster. Start with papers in your direct field.

5. **Compare with peers:** Discuss your analysis with colleagues or supervisors. Different backgrounds catch different issues.

---

## Differentiation from Other Skills

| Skill | Use When | Don't Use paper-analysis for |
|-------|----------|----------------------------|
| `peer-review` | Formal journal referee review | Personal learning |
| `paper-editor` | Finance paper editorial improvement | Other disciplines |
| `lit-review` | Synthesizing multiple papers | Single paper deep dive |
| `paper-taste` | Evaluating writing quality/style | Methodology critique |
