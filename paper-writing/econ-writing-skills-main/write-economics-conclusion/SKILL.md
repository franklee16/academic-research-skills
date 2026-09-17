---
name: write-economics-conclusion
description: Always invoke this skill when the user wants a conclusion, concluding section, final paper section, paper ending, or 结论 for an economics manuscript—including requests to read an empirical, theoretical, or structural economics paper and write a ready-to-use English conclusion. Use it to draft, rewrite, shorten, audit, or fact-check the ending even when the user does not name the skill. It reads the paper body and uses only supported findings, mechanisms, boundaries, and implications. Do not use for general inference questions that do not request a manuscript section.
---

# Write an Economics Conclusion

Create the clean snapshot a reader should carry away from the paper: what the paper established, why it matters, and where the claim stops. Synthesize rather than repeat. Treat every extension beyond the results—mechanism, external validity, policy, and future work—as evidence-dependent.

## Load the required knowledge

Before drafting, rewriting, or auditing, read all four references:

1. `references/evidence-protocol.md` — manuscript reading, evidence ledger, causal language, conflicts, and missing information.
2. `references/conclusion-knowledge.md` — the complete guide-derived principles, rationales, conditions, and anti-patterns.
3. `references/composition-and-length.md` — module selection, natural order, transitions, paper-type branches, and elastic length.
4. `references/quality-and-sources.md` — final audit, scoring rules, Top Five calibration, and provenance.

These references are mandatory. Follow the target journal and any separate Discussion-section convention before applying default length guidance.

## Non-negotiable rules

- Base the conclusion on claims delivered by the manuscript body, not merely promised in the introduction.
- Never add a result, coefficient, mechanism, limitation, citation, counterfactual, future project, or policy claim that the supplied material does not support.
- Distinguish identified mechanisms, model-implied mechanisms, evidence consistent with a channel, suggestive evidence, and author speculation.
- Preserve mechanism strength exactly. If the source is only `consistent with`, supportive, or suggestive, do not write `principal/main channel`, `drives`, `explains`, `accounts for`, `operates through`, or a causal `because` unless separately supported.
- Map every explanatory clause, appositive, modifier, adjective, and comparison—not only the sentence's main result. A correct main clause does not license an unsupported `where`, `because`, `especially when`, or `reflecting` explanation.
- Match causal language to the design and external-validity language to the studied population, period, and institution.
- Use only the few numbers needed to preserve economic magnitude or a policy tradeoff; verify every component.
- Treat a number's denominator, baseline, comparison, and normalization as separate facts. Never infer `of baseline` or another denominator from nearby context.
- Preserve every uncertainty operator on a null result. `No detectable effect` may not become `no effect`, `unchanged`, `unaffected`, `without reducing/eroding/harming`, `preserved`, or `did not harm`; every restatement must carry its own detection and proxy qualifications.
- Treat `low-cost`, `large`, `substantial`, `modest`, `meaningful`, `efficient`, and similar evaluations as factual comparisons. Use them only with a reported benchmark or explicit source characterization.
- Apply a closed-world paraphrase rule: a smoother expression is eligible only if the source entails it without adding scope, causal force, mechanism status, measurement meaning, evaluation, or centrality.
- Do not convert a robustness exercise into a contribution or a caveat into proof that the concern is resolved.
- Keep the formal conclusion in English by default. Use the user's language for necessary questions or risk notes.
- Do not modify the source manuscript unless explicitly asked.

An unsupported core claim, incorrect number, causal upgrade, invented mechanism or limitation, or policy command beyond the evidence is a failed output regardless of style.

## Determine the mode

- **draft** — write a new conclusion from the completed body.
- **rewrite** — replace repetition, drift, or overclaiming while retaining supported content.
- **audit** — diagnose the existing conclusion; do not silently rewrite unless asked.
- **fact-check** — map conclusion claims to the manuscript and identify additions, omissions, and contradictions.

Every mode uses the evidence ledger and the same hard gates.

## Read the paper in two passes

1. Inventory the manuscript, versions, and whether Conclusion and Discussion are separate.
2. Read the research question, model or identification, main results, mechanisms, heterogeneity and nulls, robustness, limitations, external validity, welfare or policy analysis, and future directions. Then compare the introduction's promises and any existing abstract/conclusion with the delivered evidence.

For long papers, locate relevant sections with search and then read their full argumentative context. Do not construct the ending from isolated phrases.

## Build an internal conclusion evidence ledger

Follow `references/evidence-protocol.md`. Record:

- one central takeaway and the small set of findings needed to support it;
- the research setting, method, or model detail needed to re-anchor the reader;
- exact result status and any economically useful magnitude;
- mechanism evidence level and alternative channels;
- heterogeneity, nulls, countervailing effects, and boundary conditions;
- specific limitations and what each limitation changes;
- robustness responses without claiming they eliminate all threats;
- supported theory, welfare, policy, historical, or real-world implications;
- future questions explicitly stated by the manuscript or mechanically tied to a documented boundary without adding a new horizon, mechanism, outcome, or threat;
- relevant citations already present in the manuscript;
- conflicts, missing facts, and claims the paper does not establish.

Choose a takeaway sentence and a paragraph-function plan before writing. Bind every substantive proposition—including subordinate clauses, comparative adjectives, mechanism labels, and numerical denominators—to claim IDs. Unsupported connective interpretation makes the sentence ineligible even when its main clause is supported. Keep the full ledger internal in draft/rewrite mode unless requested.

## Handle missing or conflicting information

Ask a concise question only if a conflict changes the central conclusion, causal status, principal magnitude, or policy interpretation. Otherwise omit unsupported optional material and proceed conservatively.

Do not invent a limitation because “good conclusions admit limitations.” Do not invent a policy paragraph because “conclusions need implications.” Do not invent future research to fill a slot. If a requested conclusion would be materially misleading without absent facts, say so and request the narrow information needed.

## Select modules before composing

The only universal module is a distilled answer anchored in the research task. Select the smallest sufficient set from:

- distilled main findings;
- mechanism or economic intuition;
- heterogeneity, nulls, and conditions;
- a specific limitation and the manuscript's response;
- external-validity calibration;
- theory, welfare, policy, historical, or real-world implications;
- future research that grows from an identified boundary;
- a brief literature or institutional connection when it performs real interpretive work.

Do not mechanically include every module. Use the decision rules in `references/composition-and-length.md`.

## Compose a natural ending

Use this default logic when it fits:

1. re-anchor the research question, setting, or framework and state the distilled answer;
2. synthesize the selected findings rather than replaying tables or the abstract;
3. explain why the pattern arises or where it holds, using evidence-calibrated mechanism language;
4. attach a limitation or external-validity boundary to the claim it qualifies;
5. derive a restrained implication; include a future question only when the manuscript supplies it or every premise is already documented;
6. end on the most important accurate departure impression.

Allow modules to merge or move next to the claims they qualify. A theory conclusion may organize broad lessons and parameter conditions; a structural conclusion may center counterfactual tradeoffs; a historical conclusion may return to narrative and contemporary relevance; a discussion-style conclusion may be longer because it must resolve policy or identification debates.

## Write with vulnerable confidence

- State supported findings clearly; do not hide behind vague caution.
- Use calibrated verbs such as `shows`, `suggests`, `points to`, or `is consistent with` according to evidence strength.
- Separate treatment effects from mechanism interpretations in different sentences. The grammatical subject of an identified-effect sentence must be the randomized/identified intervention—not an inferred friction or channel. A supportive channel may appear only afterward as `patterns are consistent with X` (or weaker); never as `evidence shows that reducing X caused Y`.
- For structural selection or decomposition results, reproduce each reported margin and direction independently. Never infer entrant ability from preparation costs, or vice versa, unless the model result explicitly signs that relationship. Call components `offsetting` only when their reported contributions have opposite signs; same-direction components are reinforcing or simply separate.
- Prefer a neutral exact quantity to an unsupported evaluation: `$3.40 per successful notification` is evidence; `a low-cost notification` is a separate claim.
- Begin from the manuscript's supported setting or research problem, not an invented field-wide prevalence claim. `In many markets`, `widely`, `common`, `often`, and similar contextual generalizations require explicit manuscript support and scope.
- Run a literal evaluation-word scan before delivery. Delete `modest`, `large`, `small`, `meaningful`, `important`, `low-cost`, `cost-effective`, and equivalents unless the ledger records the source benchmark or explicit author evaluation.
- Exclude exploratory heterogeneity by default when it competes with the central finding, is weakly estimated, or requires speculative explanation.
- Explain a limitation's consequence instead of writing “this study has limitations.”
- Preserve one or two decision-relevant quantities when they sharpen the takeaway.
- Allow necessary citations already supported by the manuscript; unlike an abstract, a conclusion may cite literature or policy facts. Do not add unverified references.
- Avoid a new literature review, full method recap, result inventory, generic future-work list, policy manifesto, or new empirical claim.
- Use new synthesis language rather than copying the abstract or introduction.

## Run the double audit

1. **Output → ledger:** decompose every sentence into micro-claims—main clause, mechanism verb, explanatory subordinate clause, evaluative modifier, number, unit, denominator, scope, and qualification—and trace each independently.
2. **Ledger → output:** confirm that the central takeaway and essential boundary are present and that the first-order result has not been displaced by secondary discussion.
3. Compare the conclusion against the title, abstract, introduction promises, main results, and mechanism evidence.
4. Apply the deletion test: if removing a sentence does not change the reader's core understanding, cut or compress it.
5. Optionally run `scripts/validate_output.py` for mechanical warnings. It cannot validate semantic truth.
6. Apply `references/quality-and-sources.md` and revise until all hard gates pass.

Check explicitly that no `consistent-with` source has become a ranked channel, no explanatory clause invents a reason for heterogeneity, no adjective evaluates magnitude or cost without a benchmark, and every number preserves the exact reported denominator—including its absence.

For every mechanism paragraph, underline the subject of each effect sentence privately. If the subject is a latent friction/channel rather than the identified treatment or modeled object, rewrite. Then scan weak-mechanism sentences for `drove`, `explains`, `accounts for`, `operates through`, `mediates`, `because`, and `by reducing`; these verbs are forbidden above their evidence level.

Audit the first and last sentences as standalone claims. Every prevalence statement, contextual generalization, evaluative adjective, and broad paper-level implication must have its own ledger row; delete it if absent.

Audit future-work clauses as new claims, not harmless suggestions. Do not invent a longer follow-up, cumulative effect, persistence concern, delayed response, new outcome, or new mechanism from silence about time. If the source does not document the premise, delete the future sentence and do not backfill the module.

For every structural decomposition sentence, create a mini-table of component, object changed, direction, conditioning statement, and source wording. Compose only from filled cells. Delete causal connectors or selection stories not stated in the source, and verify that `offsetting` maps to opposite signs.

Audit repeated claims independently: a null-result or proxy qualification must travel with the claim every time it is restated, including the final sentence.

Do not acknowledge a failed hard gate and continue. Revise, omit the item, or ask a blocking question before delivery; fluency and completeness cannot compensate.

## Deliver the result

For **draft** or **rewrite**, return the English conclusion, followed only when needed by a short Chinese risk or confirmation note.

Do not narrate the workflow or display the evidence ledger, paragraph plan, reference-reading process, or intermediate reasoning in draft/rewrite mode. Build them privately and deliver the artifact.

For **audit**, report factual drift, missing or overemphasized information, module selection, sequence, length, and language. Rewrite only if requested.

For **fact-check**, show useful claim-to-source mappings and corrections without exposing hidden chain-of-thought.
