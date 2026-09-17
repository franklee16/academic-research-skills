# Output and Evidence Schema

## Priority-paper fields

Every A/B/C/E priority paper should include:

| Field | Requirement |
|---|---|
| Paper | Original authoritative title and authors |
| Stable record | DOI and/or canonical URL |
| Lineage | Working-paper/preprint/conference/journal versions when relevant |
| Chronology | Earliest public date, current version date, current status |
| Priority relation | Pre-disclosure, same-day/unknown, or post-disclosure relative to the user's public WP cutoff |
| Evidence | `M`, `A`, or `F`, verification date, confidence |
| Classification | Primary A/B/C/D/E class plus optional secondary tags |
| Overlap | Applicable dimension factors and weighted score/range |
| Impact | High/medium/low threat or help, with affected contribution/design |
| Action | One feasible next step |
| Uncertainty | Missing evidence or unresolved interpretation |

## Overlap scoring

Default empirical weights:

| Dimension | Weight |
|---|---:|
| Core question | 20 |
| Mechanism/channel | 15 |
| Data/setting | 10 |
| Unit/linkage | 10 |
| Measurement/construct | 10 |
| Identification | 15 |
| Method/model | 5 |
| Outcome | 5 |
| Contribution claim | 10 |

Apply factors `0`, `0.25`, `0.50`, `0.75`, or `1.00`. Use `NA` when evidence is insufficient or a dimension is inapplicable. Do not silently rescale around unknown values. Report a range or withhold the total when missing critical evidence makes a point estimate misleading.

Do not calculate a numeric score from metadata-only (`M`) evidence. With abstract evidence (`A`), score only dimensions explicitly supported by the abstract and leave the rest `NA`.

Suggested interpretation when evidence is adequate:

- 80–100: near-direct overlap;
- 65–79: strong adjacent overlap;
- 45–64: meaningful overlap or high-value adjacent work;
- 25–44: supporting or methodological relevance;
- below 25: normally background unless uniquely useful.

The numeric range does not determine A/B/C/D/E. Classification follows contribution impact.

## Baseline report

### 1. Research Fingerprint

Concise fingerprint, primary/secondary contributions, provenance, and unresolved assumptions.

### 2. Executive verdict

State:

- what prior work already establishes;
- what remains provisionally distinct;
- the largest verified threat;
- the strongest surviving contribution;
- the most important coverage limitation.

### 3. Priority papers

Rank 3–10 papers by decision relevance, not score alone. Include the priority-paper fields above.

### 4. Competitor matrix

Compare the project with 3–8 nearest papers across question, mechanism, data, unit, measurement, identification, method, outcome, contribution, evidence level, and chronology.

### 5. Provisional novelty delta

Classify each project claim as:

- **No close prior identified — provisional**;
- **Narrow but defensible**;
- **Substantially pre-empted**;
- **Uncertain / insufficient coverage**.

Attach the papers and coverage evidence that justify each classification.

When the project WP is already public, base this novelty classification only on work first public before the verified/user-stated WP cutoff. Put same-day or unknown items in an uncertainty section. Put later papers in a separate `Post-disclosure convergence` section: they may affect citations or the current landscape but must not downgrade the project's public-time novelty or create a default differentiation requirement.

### 6. Method/data opportunities

For each useful paper, identify the transferable step, its assumptions, the weakness it addresses, and whether the user's current data make it feasible.

### 7. What to change now

Rank 1–5 concrete actions: cite, reposition, inspect full text, revise a claim, replicate, add a test, borrow a method, obtain data, or monitor.

### 8. Coverage and audit trail

Show search/cutoff dates, query families, completed and failed source families, evidence limitations, and likely blind spots.

## Incremental alert

Only emit a substantive alert for a new or materially changed item, a changed novelty classification, or degraded coverage that invalidates a quiet result.

```text
Research Defense Radar — Update

Top development: <one sentence>

| Paper | Class | Threat/help | Evidence | What changed | Affected part | Action |

Novelty delta: <only when changed>
Method/data lift: <only when actionable>
Coverage warning: <only when material>
Watch next: <optional>
```

When coverage completed and nothing material changed, use a one-line no-material-change result if the host cannot remain silent.
