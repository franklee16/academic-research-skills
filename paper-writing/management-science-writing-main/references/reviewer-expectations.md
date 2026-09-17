# Reviewer Expectations for MS&E Journals

This reference covers what reviewers look for at each journal, common criticisms in review reports, and how to preempt and address them. Understanding reviewer psychology is as important as getting the math right.

---

## 1. Universal Expectations (All Journals)

Every reviewer at every MS&E journal evaluates papers on these dimensions:

| Dimension | Weight | Key Question |
|-----------|--------|-------------|
| **Contribution** | 30% | What is new? Is it significant enough? |
| **Rigor** | 25% | Are the model, proofs, and experiments correct? |
| **Relevance** | 20% | Does this matter for management practice or theory? |
| **Clarity** | 15% | Is the paper well-written and easy to follow? |
| **Positioning** | 10% | Is the paper properly situated in the literature? |

---

## 2. Journal-Specific Reviewer Priorities

### Management Science (MS)

**Reviewers are asked**: "Is this paper of sufficiently broad interest to the *Management Science* readership?"

**What they REALLY look for**:
1. **The "aha" moment**: Does the paper contain a surprising, counterintuitive, or elegant result?
2. **Generality**: Does the insight apply beyond the specific context studied?
3. **Brevity of insight**: Can the main result be explained in 2-3 sentences to a non-specialist?
4. **Contribution over technique**: A new problem with a simple method beats a known problem with a fancy method.

**Red flags for MS reviewers**:
- "This could have been a field journal paper"
- "The model is technically correct but the insight is incremental"
- "After 35 pages, I'm not sure what the manager should do differently"
- "The motivating story does not match the modeled reality"

**Typical scorecard**:
- Overall: Reject / Major Revision / Minor Revision / Accept
- Contribution: 1 (weak) to 5 (outstanding)
- Technical quality: 1 to 5
- Managerial relevance: 1 to 5
- Writing quality: 1 to 5

---

### Operations Research (OR)

**Reviewers are asked**: "Is the methodological contribution significant?"

**What they REALLY look for**:
1. **Proof novelty**: Does the paper introduce a new proof technique or analytical framework?
2. **Technical difficulty**: Is solving this problem mathematically non-trivial?
3. **Generality of method**: Can the method be applied to other problems?
4. **Correctness**: Are all proofs complete and correct? (Proof errors are the #1 rejection reason)

**Red flags for OR reviewers**:
- "The proof is essentially a modification of [existing technique]"
- "The result follows directly from applying [known theorem]"
- "The computational experiments are too limited to validate the method"

---

### MSOM

**Reviewers are asked**: "Does this paper advance our understanding of how operations ARE actually managed?"

**What they REALLY look for**:
1. **Empirical grounding**: Is there real data? Is it used well?
2. **Behavioral realism**: Do the model assumptions reflect how people/organizations actually behave?
3. **Managerial specificity**: Are the implications concrete enough for a practitioner to act on?
4. **Causal identification** (for empirical papers): Are the causal claims credible?

**Red flags for MSOM reviewers**:
- "The empirical component is cosmetic — the paper is essentially analytical"
- "The data does not actually support the causal claim"
- "The managerial implications are generic and could apply to any OM paper"

---

### POM

**Reviewers are asked**: "Does this paper contribute to production and operations management?"

**What they REALLY look for**:
1. **Topic fit**: Is this a POM-relevant problem? (production, supply chain, service ops, sustainability)
2. **Practical relevance**: Would a production/operations manager care about this?
3. **Timeliness**: Is this addressing a current challenge in industry?
4. **Methodological soundness**: Appropriate methods, correctly applied

---

### EJOR

**Reviewers are asked**: "Does this paper contribute to operational research?"

**What they REALLY look for**:
1. **Computational thoroughness**: Extensive numerical testing with multiple benchmark sets
2. **Methodological clarity**: The method should be reproducible from the description
3. **Practical connection**: Even theory papers should mention potential applications
4. **European OR sensibility**: More tolerant of heuristic/metaheuristic methods; values real applications

**Red flags for EJOR reviewers**:
- "The computational experiments are insufficient to demonstrate the method's effectiveness"
- "The paper does not compare against the state-of-the-art"
- "The contribution over existing methods is not clearly demonstrated"

---

### OMEGA

**Reviewers are asked**: "Is this paper concise AND impactful?"

**What they REALLY look for**:
1. **Brevity**: Is the paper under 6000 words? If not, why not?
2. **Direct applicability**: Can a manager read this and change their practice tomorrow?
3. **Data-driven**: The best OMEGA papers use real data to tell a compelling story
4. **No padding**: Every paragraph must earn its place

**Red flags for OMEGA reviewers**:
- "This paper is too long for its contribution"
- "The managerial recommendations are too generic"
- "The literature review is excessive"

---

### C&IE

**Reviewers are asked**: "Does the computational method advance industrial engineering?"

**What they REALLY look for**:
1. **Algorithmic novelty**: Is the proposed method genuinely new or a minor tweak?
2. **Computational validation**: Extensive experiments on standard benchmarks
3. **Statistical rigor**: Proper experimental design with statistical testing
4. **Applicability**: Is there a clear industrial engineering application?

---

## 3. The Review Report Structure

Understanding how reviewers write their reports helps you preempt their concerns.

### Typical Review Structure

```
1. Summary (1 paragraph)
   - Restate what the paper does
   - Overall assessment (positive/negative)

2. Major Comments (3-6 items)
   - Contribution concerns
   - Model/technical issues
   - Methodology questions
   - Results interpretation issues
   - Missing literature

3. Minor Comments (5-15 items)
   - Typos
   - Notation issues
   - Presentation suggestions
   - Additional experiments
   - Clarification requests
```

### Common Reviewer Phrases (and What They Mean)

| Reviewer Says | Actually Means |
|---------------|---------------|
| "The contribution is incremental" | The gap between your paper and existing literature is too small |
| "The assumptions are restrictive" | You haven't defended your assumptions or shown what happens when relaxed |
| "The managerial insights are generic" | You haven't translated your math into concrete actions |
| "The paper is difficult to follow" | Poor structure, unclear notation, missing signposting |
| "The numerical experiments are limited" | Too few instances, no sensitivity analysis, no statistical tests |
| "The paper does not fit this journal" | Wrong methodology-contribution profile for this venue |
| "This is more suitable for [Journal X]" | See above; also, your paper is too narrow/applied/theoretical for this journal |

---

## 4. Preempting Common Criticisms

### "The contribution is incremental"

**Preemption strategy**:
1. Build an explicit **gap table** in the introduction comparing your paper to 8-12 key references across 5-8 dimensions
2. Clearly mark which cells represent your contribution
3. State: "While prior work has studied X, Y, and Z separately, we are the first to consider them jointly and characterize the resulting interaction effect."

### "The assumptions are restrictive"

**Preemption strategy**:
1. Defend each assumption: "This assumption is consistent with industry practice because..."
2. Relax at least one assumption as an extension: "In the Online Supplement, we show that relaxing Assumption 3 does not change the qualitative results."
3. Acknowledge limitations: "We maintain Assumption 2 for analytical tractability; extending our analysis to relax this assumption is an important direction for future work."

### "The managerial insights are generic"

**Preemption strategy**:
1. Use the SAR framework (Setting → Analytical finding → Recommendation)
2. Make each insight specific and actionable
3. Connect to real companies or industries
4. Number insights for clarity

---

## 5. Rebuttal Strategies

### Structure of a Rebuttal Letter

```
Dear Editor,

We thank the reviewers for their careful reading and constructive comments.
We have revised the manuscript to address all concerns. Below, we respond 
to each comment. Reviewer comments are in italics; our responses follow.

[Point-by-point responses]

We believe the revised manuscript is substantially improved and hope it
is now suitable for publication.

Sincerely,
The Authors
```

### Rebuttal Principles

1. **Be gracious**: Thank the reviewer even for harsh comments. Never argue.
2. **Be specific**: "We have added X on page Y" — not "We addressed this."
3. **Show the change**: Quote the added/modified text in the response.
4. **Pick your battles**: If a reviewer asks for an infeasible analysis, explain why it's infeasible AND propose an alternative.
5. **If you disagree, explain why respectfully**: "We respectfully note that [evidence]. However, we have added a discussion of this limitation on page Z."
6. **Track changes**: Use a marked-up version or color-coded responses. Make it easy for the reviewer to see what changed.

### When a Reviewer Is Wrong

If a reviewer makes a factual error:
1. Do not say "The reviewer is wrong."
2. Say: "We appreciate the reviewer raising this point. To clarify, [polite correction with evidence]. We have revised the text on page X to prevent this misunderstanding."

---

## 6. Self-Review Checklist (Before Submission)

Review your own paper as if you were a reviewer:

### Contribution
- [ ] Can I state the single main contribution in one sentence?
- [ ] Would a colleague in my subfield say "I wish I had thought of that"?
- [ ] Is the contribution clearly labeled in the introduction?

### Technical Quality
- [ ] Have I verified every proof? (Better: has a colleague verified them?)
- [ ] Are all equations numbered and correctly referenced?
- [ ] Do the numerical experiments support (not just illustrate) the analytical results?

### Managerial Relevance
- [ ] Can a non-academic manager understand at least one insight from this paper?
- [ ] Are the managerial insights specific and actionable?
- [ ] Is the motivating problem real? (Cite an industry source)

### Positioning
- [ ] Have I cited the most relevant papers from the target journal?
- [ ] Is the literature review organized by stream, not paper-by-paper?
- [ ] Does the gap table clearly show my contribution?

### Presentation
- [ ] Is the abstract within the journal's word limit?
- [ ] Is the notation table complete and accurate?
- [ ] Are all figures and tables referenced in the text?
- [ ] Are all citations verified (not hallucinated)?
