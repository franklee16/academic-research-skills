---
name: write-economics-abstract
description: Always invoke this skill when the user wants an abstract or 摘要 for an economics research paper from a manuscript, completed paper body, model, data, or results—including requests to read an empirical, theoretical, or structural economics paper and write a ready-to-use English abstract. Use it to draft, rewrite, compress, audit, or fact-check an economics abstract even when the user does not name the skill. It reads the paper body and verifies every substantive claim. Do not use for generic summaries or non-research prose.
---

# Write an Economics Abstract

Produce a self-contained English abstract that lets a reader recover four things accurately: the research task, how the paper answers it, what it finds, and what the findings mean. Treat factual fidelity as a hard constraint and prose quality as an optimization within that constraint.

## Load the required knowledge

Before drafting, rewriting, or auditing, read all four references below. They are mandatory, not optional background:

1. `references/evidence-protocol.md` — manuscript reading, evidence ledger, causal language, conflicts, and missing information.
2. `references/abstract-knowledge.md` — the full guide-derived principles, rationales, exceptions, and anti-patterns.
3. `references/composition-and-length.md` — natural information order, paper-type adaptations, transitions, and elastic length.
4. `references/quality-and-sources.md` — final audit, scoring rules, Top Five calibration, and provenance.

Read the user's target-journal instructions first if supplied; a journal's hard limit overrides observed ranges.

## Non-negotiable rules

- Ground every substantive statement in the supplied paper body or in a fact the user explicitly confirms.
- Never invent a contribution, result, coefficient, unit, sample, mechanism, robustness result, welfare claim, or policy implication.
- Do not upgrade association to causation, suggestive evidence to an established mechanism, or an author interpretation to a demonstrated fact.
- Verify each number with its direction, unit, baseline, estimand, population, and time horizon.
- For experiments and quasi-experiments, lock distinct design roles: assignment/randomization unit, treatment recipient, delivery actor, observation unit, and analysis unit. Never say the randomized unit `received` a treatment delivered to people or firms within it; express assignment and receipt in separate clauses when roles differ.
- Preserve the exact measured outcome and proxy status. Do not replace a price, index, proxy, score, ratio, or accounting measure with a broader construct such as cost, welfare, quality, productivity, or efficiency unless the manuscript establishes equivalence.
- Apply a closed-world paraphrase rule: a smoother expression is eligible only if the source entails it without adding scope, causal force, mechanism status, measurement meaning, evaluation, or centrality.
- Copy constructed sample and eligibility definitions into a locked phrase bank before drafting. Preserve their defining condition, place, lookback window, and event; do not replace them with category labels such as `new`, `incumbent`, `local`, `eligible`, or `inactive` unless the manuscript itself proves that equivalence.
- Lock the complete outcome tuple as well: outcome/proxy + population/subgroup + unit + comparison + horizon. Every repetition—including the closing synthesis—must preserve all scope-bearing members. `Mean exam scores among new providers` may not become `mean exam scores` or a general claim about service quality.
- For structural selection, preparation, equilibrium, or decomposition results, preserve each component's reported direction and relation. Do not assert that one channel `dominates`, `offsets`, `outweighs`, or is stronger than another unless the manuscript explicitly reports that comparison. An ambiguous net sign remains ambiguous even if a particular estimated counterfactual has a sign.
- Treat `modest`, `large`, `small`, `meaningful`, `important`, `broad`, and similar evaluations as claims. Omit them unless the manuscript provides or explicitly states the comparison basis.
- For `consistent-with`, supportive, or suggestive mechanisms, use only a noncausal evidence form (`patterns are consistent with X`, `evidence is suggestive of X`, or the manuscript's weaker wording). Do not combine a hedge with `drove`, `explains`, `operates through`, `because`, `by reducing`, or another causal predicate.
- Lock the identified treatment as the causal subject of every effect and implication sentence, including the final sentence. When alerts are randomized but information frictions are only a candidate mechanism, write `timely alerts increased participation`; never write `reducing information frictions expanded/can expand participation` or substitute the channel for the treatment.
- Treat “first,” “novel,” “new,” and “fills a gap” as factual claims requiring explicit, supportable scope.
- Use the old abstract and introduction as orientation and consistency checks, not as the final authority over results.
- Keep the formal abstract in English by default. Communicate necessary questions or risks in the user's language.
- Do not modify the user's manuscript unless the user explicitly asks for file edits.

Any unsupported core fact, incorrect number, causal overstatement, or invented mechanism is a failed output regardless of fluency.

## Determine the mode

Infer the narrowest mode that satisfies the request:

- **draft** — write a new abstract from the paper body.
- **rewrite** — improve an existing abstract while preserving only claims supported by the body.
- **audit** — diagnose accuracy, structure, information selection, and style; do not silently replace the abstract unless asked.
- **fact-check** — map substantive abstract claims to manuscript evidence and flag unsupported or conflicting claims.

All modes use the same evidence ledger. “Polish” never authorizes factual drift.

## Read the manuscript in two passes

1. Inventory files, versions, and sections. Identify the research type: causal empirical, associational/descriptive, measurement, structural/quantitative, theory, historical, or mixed.
2. Read the relevant body in depth: model or design; data and sample; main results; mechanisms; heterogeneity and null results; robustness and limits; welfare, theory, or policy analysis. Then check the introduction and existing abstract against what the body actually delivers.

For long projects, use search to locate candidate sections, but read enough surrounding text to interpret estimates and qualifications. Do not compose from keyword snippets.

## Build an internal abstract evidence ledger

Follow `references/evidence-protocol.md`. At minimum record:

- research question, tension, and paper type;
- data, setting, sample, and period;
- identification variation, measurement solution, model mechanism, or counterfactual logic;
- primary finding(s), exact magnitudes, units, and comparisons;
- mechanism evidence level;
- important null, reversal, heterogeneity, or boundary result;
- supported theory, welfare, policy, or real-world implication;
- what the paper does not establish;
- conflicts or missing facts.

Create a sentence plan in which each proposed substantive sentence points to ledger claim IDs. Keep the ledger internal in draft/rewrite mode unless the user asks to see it.

## Handle missing or conflicting information

Ask one concise question only when a missing or conflicting fact would change the abstract's central claim—for example, the main effect's direction, the estimand, or whether the design is causal. Do not ask about optional stylistic preferences if a sensible default exists.

If the gap is non-blocking, omit the unsupported item. If the user requests a provisional draft despite a blocking gap, label it outside the abstract as provisional and use only supported facts. Never place invented filler or unresolved placeholders inside a purportedly final abstract.

## Compose by function, not by template

Use the default information flow as a reasoning scaffold:

1. establish the question, tension, task, or headline result;
2. explain how the paper answers it and why the claim is credible or interpretable;
3. present the primary findings, prioritizing economic magnitude or meaningful comparisons;
4. add only a central mechanism, contrast, null, heterogeneity, or boundary result;
5. close the argument with the strongest supported implication, qualification, or synthesis.

Do not force one function per sentence. Merge, split, or reorder functions when the paper type requires it. A result-first abstract can work; an information-dense “We develop…” or “This paper provides…” opening can work. Empty self-reference and generic importance claims cannot.

Apply the paper-type branches in `references/composition-and-length.md`. In particular, do not force theory or structural papers into an empirical identification template.

## Draft and compress

- Make the findings the center of gravity.
- Prefer interpretable magnitude, units, and comparison over “statistically significant.”
- Include a null or countervailing result when it defines the contribution's boundary.
- Mention methods only to establish credibility, interpretation, or the economic object being recovered.
- Avoid citations, footnotes, table or section references, undefined abbreviations, robustness lists, and empty process sentences.
- Deliver the formal abstract as exactly one uninterrupted prose paragraph unless the user or target outlet explicitly requires another format. Multiple paragraphs are a delivery failure, not a response to paper complexity.
- Do not wrap the abstract in quotation marks, a block quote, a code fence, or an `Abstract:` label unless explicitly requested. The prose must be directly pasteable into a manuscript.
- Without explicit user or journal authorization, do not deliver more than 200 words. If a draft exceeds 200 words, rebuild it around the Tier 1 spine in `references/composition-and-length.md`, recount, and revise before delivery.
- For a structural or quantitative paper, retain the economic tradeoff, minimum model logic, principal counterfactual, and one essential model-dependence or boundary. Do not let accounting components, implementation costs, decompositions, or an explanation of why quantities cannot be combined displace that spine.
- Remove any sentence whose deletion does not change a reader's understanding of the question, credibility, findings, or closure.

## Run the double audit

Before delivery:

1. **Output → ledger:** trace every substantive claim, result noun, number, causal verb, mechanism, and implication to support; reject a synonym that broadens the measured object.
2. **Ledger → output:** ensure the central question, credibility source or model logic, primary finding, and essential boundary are not omitted.
3. Check independent self-sufficiency, information order, word count, natural academic English, and consistency with the body.
4. Run `scripts/validate_output.py`, or perform its exact mechanical checks manually if execution is unavailable. Resolve every hard-format failure.
5. If the draft exceeds 200 words, perform a second compression pass and validate again. Paper complexity alone does not waive this pass.
6. Run a delivery-surface check: exactly one paragraph; no outer quotation marks, heading, block quote, code fence, commentary, or blank-line break; direct natural economic wording rather than compressed abstractions.
7. Apply the hard gates and rubric in `references/quality-and-sources.md`.
8. Compare every sample-definition phrase word-for-word with the locked phrase bank. Then scan each weak-mechanism sentence for causal predicates; a hedge elsewhere in the sentence does not license one.
9. Build a list of every quantitative or closing claim's scope tokens (population, subgroup, proxy, place, horizon). Reject the draft if any repeated claim omits one or if the closing sentence generalizes beyond them.
10. Parse each design sentence as subject–verb–object. Confirm the subject's role licenses that verb: assignment units are assigned, recipients receive, delivery actors deliver, and analysis units are analyzed. Reject any role substitution.
11. Parse every effect or implication sentence, especially the close, as causal subject → predicate → outcome. The causal subject must equal `identified_treatment` (or be explicitly model-implied). If it equals `mechanism_candidate`, reject. A weak mechanism may appear only in a separate controlled sentence with no effect predicate.
12. For a structural mechanism/decomposition sentence, map component → object → direction → relative strength → source. Any blank is `not established`, not an invitation to infer. Reject `dominates`, `offsets`, `outweighs`, and ranked-channel language unless the relative-strength cell is explicit.

Revise until the output passes both audits.

Do not acknowledge a failed hard gate and continue. Revise, omit the item, or ask a blocking question before delivery; fluency and completeness cannot compensate.

## Deliver the result

For **draft** or **rewrite**, default to:

1. the directly pasteable English abstract only—one paragraph, no heading, no enclosing quotation marks, no code fence;
2. a short Chinese note only if a material ambiguity, omission, or factual risk remains.

Do not narrate the workflow or display the evidence ledger, sentence plan, reference-reading process, or intermediate reasoning in draft/rewrite mode. Build them privately and deliver the artifact. This output boundary is mandatory even when the ledger is useful internally.

For **audit**, provide a concise diagnosis organized by factual fidelity, missing/overweighted information, structure, length, and language. Rewrite only if requested.

For **fact-check**, show claim-to-source mappings, conflicts, and proposed corrections. Do not expose hidden chain-of-thought; show only useful evidence locations and conclusions.
