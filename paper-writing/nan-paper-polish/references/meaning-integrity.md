# Meaning integrity

## Protected content

Treat these as immutable unless the user explicitly authorizes a change:

- numbers, signs, units, equations, table and figure values;
- sample size, population, time, place, and study design;
- variable and construct definitions;
- statistical direction, significance, interval, and uncertainty;
- correlation, association, prediction, contribution, and causation distinctions;
- modal force, scope, conditions, exceptions, and limitations;
- citations, citation keys, quotations, and attribution;
- domain terms, abbreviations, labels, and proper names;
- equations, algorithms, code, prompts, JSON/schema, templates, and other executable or reproducibility artifacts;
- research questions, hypotheses, findings, and stated contributions.

Never invent evidence, data, citations, methods, mechanisms, findings, gaps, contributions, or limitations.

Do not use a hedge to launder an unsupported proposition. When the supplied manuscript gives no basis for a factual or practical claim, adding `may` is insufficient; convert the claim into an explicit evidence gap or author question, or omit it pending confirmation.

## Risk levels

### Level A: apply and record

- spelling, punctuation, agreement, and obvious grammar;
- formatting normalization;
- unambiguous terminology consistency;
- redundant wording whose removal cannot change scope or force.

### Level B: revise conservatively and flag for review

- sentence splitting or merging;
- active/passive change;
- sentence reordering within a paragraph;
- local Flow repair;
- nominalization changes;
- hedge calibration that preserves the existing evidential level.

### Level C: require author confirmation

- substantive deletion or factual addition;
- paragraph or section relocation that changes emphasis or argument;
- causal, certainty, scope, generalization, or recommendation change;
- new, removed, or replaced citation;
- interpretation of contradictory data;
- unsupported bridge logic;
- ambiguous technical terminology;
- any modification to a protected number, formula, definition, or result.

When confirmation is unavailable, preserve the source in the clean candidate and put the item in the author-confirmation queue. A separate conservative alternative may be offered when useful, but must not silently replace a central novelty, design, contribution, method, or interpretation claim. If the manuscript itself conclusively establishes the mismatch, apply a proportionate and complete evidence-preserving correction and explain it.

## Claim-strength register

Classify important claims before editing:

1. `observation`: directly reported data or result;
2. `association`: statistical or empirical relationship without causal warrant;
3. `interpretation`: inference supported by results;
4. `mechanism`: proposed explanation not directly tested;
5. `extrapolation`: claim beyond the observed sample, condition, or period.

Do not promote a claim to a stronger class through language editing. Record any deliberate narrowing or strengthening in `meaning_effect`.

## Integrity checks

- Compare all number and unit tokens before and after.
- Compare LaTeX citation keys and cross-reference labels.
- Check that every changed technical term is deliberate and globally consistent.
- Check Abstract, Results, Discussion, and Conclusion for the same result stated at different strengths.
- Check that `no evidence was found` has not become `there is no effect`.
- Check that `associated with` has not become `caused`, `affected`, or `led to` without support.
- Check that a hedge has not been removed merely to sound confident.
- Check that a limitation has not disappeared from the sentence whose claim it constrains.
- Check that a passive-to-active edit has not invented an agent.
- Check that a bridge sentence does not add an unstated premise.
- Check that no prompt, code, schema, equation, algorithm, or reproducibility artifact changed as a side effect of prose polishing.

## Attribution rules

- Preserve who performed an action, proposed an idea, or reported a finding.
- Use author-prominent phrasing when agency or scholarly disagreement matters.
- Use information-prominent phrasing when the topic or knowledge state matters.
- Never make a cited author's claim appear to be the present author's claim.
- Never turn a literature consensus into a universal fact without evidence.
