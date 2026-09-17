# Contributing To Good Story

`good-story` is meant to become a broadly usable research-writing product. Contributions should make it easier for researchers to find evidence-faithful stories across fields.

## Contribution Principles

1. Evidence integrity comes first.
2. A stronger story must not become a larger claim than the evidence supports.
3. Domain calibration packs are context, not skill boundaries.
4. Examples should teach a reusable move, not advertise a field.
5. New guidance should be testable with an evaluation scenario.

## What To Add

Good contributions include:

- a new before/after example;
- a field mini-case;
- a domain calibration pack;
- an overclaim or reviewer-resistance pattern;
- a source that contributes a reusable story move;
- an evaluation scenario that catches a real failure mode;
- a clearer Chinese or English user-facing explanation.

Avoid adding:

- generic writing advice that does not change story diagnosis;
- field-specific claims without evidence boundaries;
- long literature reviews;
- examples that require hidden background knowledge;
- style-only rewrites that do not diagnose the story.

## Adding A Field Calibration Pack

A calibration pack should help people in a field use the shared story logic well. It should not redefine what `good-story` is.

Use this structure:

```markdown
# Field Story Calibration

## When To Use

## Evidence Contract

## Common Story Types

## Reviewer Resistance

## Mini Cases

## What Not To Overclaim
```

Every mini case should include:

- loose material;
- weak story;
- better story;
- evidence standard;
- strongest supportable claim;
- main risk.

## Adding Examples

Add examples under `examples/`.

Each example should show:

`weak material -> diagnosis -> calibrated story -> why it works`

Keep examples compact. A user should understand the move in under two minutes.

## Adding Evaluation Scenarios

Add scenarios under `evals/scenarios.md` unless the suite becomes too large.

Each scenario needs:

- prompt;
- must-pass criteria;
- should-not criteria when useful.

Prefer scenarios that catch real failures:

- overclaiming;
- fake tension;
- lab chronology;
- wrong domain calibration;
- English labels in Chinese answers;
- hiding weak points.

## Adding Sources

Add a source only if it contributes at least one reusable story move or caution.

When adding a source:

1. Add it to `references/source-map.md`.
2. If it is user-visible, add it to README references.
3. Explain what the project uses from it.
4. Avoid citation padding.

## Required Checks

Before proposing a release or major documentation update, run:

```powershell
.\scripts\validate-product.ps1
```

Then manually review:

- README user entry;
- examples;
- evaluation scenarios;
- release checklist;
- Chinese user-facing wording.

## Release Labels

- **Draft:** core idea exists, but examples or evals are missing.
- **Beta:** README, skill logic, examples, and evals exist.
- **Release candidate:** eval scenarios pass and at least 5 unfamiliar real materials have been checked in fresh sessions.
- **Mature:** repeated use across fields shows stable story diagnosis, claim calibration, and language quality.
