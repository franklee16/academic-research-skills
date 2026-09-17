# Output Templates

Use these templates only when they fit the user's request. Keep outputs concise unless the user asks for full notes.

## Structured Reading Note

```text
Paper: [Title]
Authors / Year / Venue:
Link / DOI / arXiv:

One-sentence idea:
Problem:
Core method:
Key evidence:
Main findings:
Innovation:
Limitations:
Best related papers:
Relevance to the user's project:
Open questions:
```

## Innovation Assessment

```text
Claimed contribution:
Closest prior work:
Actual novelty:
Evidence supporting novelty:
Weak or missing evidence:
Novelty level: low / medium / high
Confidence: low / medium / high
What would strengthen the claim:
```

## Limitation-to-Direction Table

| Limitation or gap | Research direction | Why plausible | Minimal experiment | Cost | Risk | Priority |
|---|---|---|---|---|---|---|
|  |  |  |  | low/med/high | low/med/high | low/med/high |

## Related Work Table

| Paper | Year | Relationship | Key idea | Difference from target paper | Why it matters |
|---|---:|---|---|---|---|
|  |  | foundational / predecessor / competitor / extension / benchmark / critique |  |  |  |

## Research Direction Scoring

Score each from 1 to 5 unless the user requests another scale.

| Direction | Novelty | Feasibility | Impact | Cost | Risk | Project fit | Recommendation |
|---|---:|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  | pursue / pilot / defer / avoid |

Interpretation:

- Pursue: strong fit and clear verification path.
- Pilot: worth a small experiment before larger investment.
- Defer: interesting but currently too costly or under-supported.
- Avoid: low information gain, weak fit, or high risk with little upside.

## Paper Scorecard

| Dimension | Score | Rationale |
|---|---:|---|
| Novelty |  |  |
| Evidence |  |  |
| Reproducibility |  |  |
| Transferability |  |  |
| Risk |  |  |
| Reading Priority |  |  |

Decision: skim / read deeply / cite carefully / reproduce / build on / skip.

## Paper-to-Project Plan

| Paper component | Reusable unit | Target project location | Adaptation needed | Risk | Minimal verification |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Evidence Boundary Language

Use these labels when needed:

- Paper claim: the authors state this.
- Direct evidence: supported by reported experiment, table, figure, proof, or analysis.
- Inference: plausible interpretation based on the paper and related work.
- Speculation: hypothesis that requires new experiments.
- Unknown: cannot be determined from available sources.
