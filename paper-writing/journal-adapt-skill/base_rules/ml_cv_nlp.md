# Base Writing Rules: ML / CV / NLP

Version: 1.0
Scope: Machine learning, computer vision, natural language processing papers (NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP)

---

## Core Principles

- Claim must be supported by experiment. Never state a claim without pointing to the evidence.
- Reproducibility matters. State enough implementation detail for replication.
- Comparison with baselines is mandatory. Results without context are meaningless.
- Simplicity signals confidence. Overcomplicated presentation hides weak contributions.

---

## Abstract

Structure (150–250 words): problem → limitation of prior work → proposed method → key results (with numbers) → significance.
- Include at least one concrete metric result (e.g., "achieves 87.3% accuracy on X benchmark").
- Name the method or model if it has a name.
- Do not use "novel", "innovative", "state-of-the-art" as self-descriptions.
- Past tense for experiments, present tense for claims about the method.

---

## Introduction

Sequence: problem motivation → limitations of existing approaches → your approach (high-level) → contributions (bulleted list) → paper structure.

- Motivation must connect to a real problem, not just a benchmark gap.
- Contribution list: 3 items maximum. Each item is one concrete, verifiable claim.
- Contributions stated as facts, not intentions: "We propose X that achieves Y" not "We aim to address Z."
- Related work: either standalone section after intro, or integrated — pick one, be consistent.

Do not:
- Open with "Deep learning has revolutionized..."
- List 5+ contributions — weakens all of them.
- Promise results you do not deliver by end of paper.

---

## Related Work

- Organize by approach or technique, not chronologically.
- For each group of related work: what they do, what they cannot do, how yours differs.
- Do not dismiss prior work. Show you understand it fully before noting limitations.
- Citation density: cite the most relevant 3–5 papers per claim, not 10+.

---

## Method

- Describe the intuition before the formalism.
- One figure showing the overall architecture or pipeline is expected.
- Define all notation before first use. Maintain notation consistency throughout.
- Algorithm pseudocode: use standard formatting; number all lines; reference line numbers in text.
- Justify non-obvious design choices: "We use X instead of Y because..."

---

## Experiments

Structure: experimental setup → main results → ablation studies → analysis.

- Setup: dataset(s), evaluation metrics, baselines, implementation details (optimizer, LR, hardware, seeds).
- Main results: table with all baselines. Bold your best result. Note statistical significance if applicable.
- Ablation: remove one component at a time. Each ablation tests one design decision.
- Analysis: what do the numbers actually mean? Where does the method fail?

Do not:
- Report only accuracy — include relevant secondary metrics.
- Cherry-pick qualitative examples without quantitative support.
- Omit hyperparameter settings — this blocks reproducibility.

---

## Conclusion

- Summarize contribution in 2–3 sentences.
- Honest limitations: what the method cannot handle, what assumptions it relies on.
- Future work: one specific direction, not a wishlist.

---

## Language

- Active voice: "We propose", "We show", "Our model achieves."
- Present tense for method descriptions and established facts.
- Past tense for specific experimental results.
- Technical terms: define on first use, then use consistently.
- Equations: introduce in words before displaying. Number only if referenced later.

---

## Anti-Pattern List (always remove)

```
"We propose a novel..."
"To the best of our knowledge, this is the first..."
"State-of-the-art performance"  (as self-description before results)
"Our method is simple yet effective."
"Extensive experiments demonstrate..."
"It is worth noting that..."
"We leave X for future work." (without a specific direction)
"As shown in Figure X, our method clearly outperforms..."  (let numbers speak)
```
