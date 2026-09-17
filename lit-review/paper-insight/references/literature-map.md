# Literature Map

Use this reference when the user asks to connect papers, build related work, or understand how a paper sits in a field. When the user needs systematic literature expansion before mapping, read `citation-chaining.md` first.

## Relationship Types

- Foundational: introduces a task, theory, model family, dataset, or metric.
- Direct predecessor: closest prior method or most similar framing.
- Competitor: alternative method for the same problem.
- Extension: improves, scales, adapts, or generalizes a prior paper.
- Benchmark/dataset: supplies evaluation data or protocol.
- Survey/meta-analysis: organizes the field.
- Critique/negative result: questions assumptions, exposes failure modes, or reports weak reproduction.
- Application: applies the core method to a new domain.

## Search Path Labels

- Backward: found through target paper references.
- Forward: later work citing, extending, applying, or critiquing the target paper.
- Lateral: same task/problem, different method family or assumption.
- Benchmark: same dataset, metric, leaderboard, or SOTA comparison.
- Negative: reproduction failure, critique, contradiction, or limitation-focused source.

## Compact Graph Template

```text
[Target Paper]
  <- [Foundational Paper]: introduced [concept/dataset/method]
  <- [Direct Predecessor]: similar because [reason]
  <-> [Competing Method]: differs by [reason]
  -> [Extension]: builds on [component]
  x  [Critique]: challenges [assumption/result]
```

## Timeline Template

| Year | Paper | Role | Key contribution | Link to target paper |
|---:|---|---|---|---|
|  |  | foundational / predecessor / competitor / extension / critique |  |  |

## Inclusion Rules

- Include a paper only if it changes the interpretation of the target paper or the user's next decision.
- Prefer exact relationship labels over vague "related".
- If relationship is inferred from title/abstract only, mark it as tentative.
- For fast-moving areas, separate peer-reviewed work from preprints.

## Stopping Rules

Stop expanding when:

- The requested paper count, year range, or venue range is reached.
- New papers repeat the same method family without changing the synthesis.
- Candidate papers are only weakly related to the user's question.
- The user needs a decision now and additional search has low marginal value.
