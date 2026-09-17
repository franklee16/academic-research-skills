# Base Writing Rules: CS / Engineering

Version: 1.0
Scope: Computer science systems, software engineering, electrical engineering, robotics papers (IEEE, ACM, Springer)

---

## Core Principles

- Precision over accessibility. Vague claims are worse than no claims.
- System description must be complete enough to reimplement.
- Evaluation must be fair: compare against the strongest relevant baseline, not the weakest.
- Every design choice must be justified. "We chose X" is not justification; "We chose X because Y" is.

---

## Abstract

Structure (150–200 words): problem and context → gap or challenge → proposed system/approach → evaluation summary (with numbers) → main takeaway.
- State the specific problem, not the general field.
- Include at least one quantitative result.
- Name the system or method if it has a name.
- Avoid venue-specific jargon in abstract — it may be read outside the community.

---

## Introduction

Sequence: problem context → concrete challenge → why existing approaches fall short → your solution (overview) → contributions → paper organization.

- Contributions: numbered list, 3–4 items. Each item is a concrete, testable claim.
- "We design/build/implement/evaluate X" — concrete verbs, not "we explore/investigate/study."
- Problem statement must be specific: not "networking is important" but "existing protocols fail under condition X."

Do not:
- Begin with a generic statement about how important the field is.
- List more than 4 contributions.
- Claim novelty without stating what specifically has not been done before.

---

## Related Work

- Standalone section, after introduction.
- Group by approach: protocol-based, learning-based, hybrid, etc.
- For each group: describe the approach, state its limitation relative to your work.
- Be specific about limitations: "X cannot handle Y" not "X is insufficient."
- Do not use related work to criticize prior work — use it to position yours.

---

## System / Method Description

- Start with a high-level overview (one paragraph + one diagram) before details.
- Describe components in the order they execute or interact.
- API boundaries: define inputs, outputs, and assumptions for each component.
- Justify non-obvious decisions explicitly.
- Algorithms: use pseudocode for non-trivial procedures. Reference line numbers in text.
- Complexity: state time and space complexity for algorithmic contributions.

---

## Evaluation

Structure: evaluation goals → setup (hardware, datasets, metrics, baselines) → results → discussion of results.

- Baselines: compare against the most relevant current work, not outdated methods.
- Metrics: define each metric precisely. Explain why each metric matters for this problem.
- Statistical rigor: report mean and standard deviation across multiple runs.
- Microbenchmarks: test each claim separately. Aggregate results hide component performance.
- Negative results: if something did not work, say so and explain why.

Do not:
- Show only best-case results.
- Omit implementation details that affect reproducibility.
- Report latency without stating hardware configuration.

---

## Conclusion

- Restate problem and solution in 2 sentences.
- Key quantitative result in 1 sentence.
- Limitations: be honest about what the system does not handle.
- Future work: one or two specific directions, not a generic wishlist.

---

## Language

- Precise technical language. Prefer standard terminology over invented terms.
- Define every term on first use.
- Active voice: "The system processes", "We implement", "Algorithm 1 computes."
- Avoid anthropomorphizing systems: "the algorithm decides" → "the algorithm selects."
- Short sentences in evaluation sections — results must be scannable.

---

## Anti-Pattern List (always remove)

```
"Our system is highly efficient and scalable."  (without numbers)
"We propose a novel and robust framework..."
"Extensive experiments validate our approach."
"The system achieves excellent performance."
"As can be seen in Figure X..."  (let the figure speak)
"We believe our work will..."
"This is the first work to..."  (unless you can cite the search you did)
"Our approach is simple and easy to implement."
```
