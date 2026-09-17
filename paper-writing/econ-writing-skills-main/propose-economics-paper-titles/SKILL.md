---
name: propose-economics-paper-titles
description: Always invoke this skill for ANY request to write, propose, choose, rank, rewrite, compare, or audit an economics paper title—including 中文 requests for 论文标题, 英文标题, 标题候选, 推荐标题, or 备选标题. Invoke it when the user asks for one recommended English title plus alternatives from an empirical, theoretical, or structural economics manuscript, even if the skill is not named. It reads the paper body and treats every displayed title as a factual promise. Do not use for section, table, figure, news, or book titles.
---

# Propose Economics Paper Titles

Design accurate, distinctive, concise English titles that compress what the paper is and make an honest promise to the right reader. Generate diversity by changing information architecture, not by swapping synonyms in one template.

## Load the required knowledge

Before proposing, rewriting, or auditing titles, read all four references:

1. `references/evidence-protocol.md` — manuscript reading, evidence ledger, causal language, conflicts, and missing information.
2. `references/title-knowledge.md` — the complete guide-derived principles, rationales, title families, exceptions, and anti-patterns.
3. `references/composition-and-length.md` — candidate generation, ranking, promise audits, length, and paper-type adaptations.
4. `references/quality-and-sources.md` — final scoring, Top Five calibration, and provenance.

These references are mandatory. If the user supplies a journal style or title-length rule, follow it.

## Non-negotiable rules

- Read enough of the paper body to determine the central object, relationship or task, evidence strength, contribution, and necessary scope.
- Treat every content word as a promise the body must deliver.
- Never add causal language, a mechanism, a general scope, a result direction, a novelty claim, or a design label without support.
- Treat gerunds and nominalized actions as factual claims. `Reducing`, `Improving`, `Removing`, and similar openings presuppose the intervention changed that object; supportive or consistent-with mechanism evidence does not license them.
- Apply a closed-world paraphrase rule: a smoother title expression is eligible only if the source entails it without adding scope, causal force, mechanism status, measurement meaning, evaluation, or centrality.
- Do not promote a secondary heterogeneity result, discussion point, or future-research idea into the title.
- Do not use `first`, `new`, `novel`, `important`, or similar self-evaluation unless the narrow claim is explicitly defensible; usually show contribution through specifics instead.
- Accuracy outranks cleverness and brevity. Brevity outranks detail only when no necessary distinction is lost.
- Formal title candidates are English by default. Explain tradeoffs in the user's language when helpful.
- If a title centers a behavior, mechanism, or decision observed only inside an estimated structural model, include `model`, `structural`, or an equally explicit model marker in that same title. Do not let readers infer that the behavior was directly observed.
- Preserve exact geographic scope. Evidence from 17 U.S. states does not license `U.S. markets`, `the United States`, or national scope unless the manuscript establishes national coverage.
- Preserve institutional hierarchy as well as geography. A study of municipal procurement does not license the umbrella `public procurement`; a paper on one occupation does not license a labor-market title. Use the narrowest source-defined institution unless broader coverage is established.
- Treat relationship operators as claims. `versus`, `tradeoff`, `tension`, `offsetting`, and contrast punctuation require explicit opposing directions or a source-stated conflict; two mechanisms or margins are not opponents merely because both appear in the model.
- Build an authorized title vocabulary from the manuscript's exact central nouns and source-authorized equivalents before generation. Every substantive noun in every displayed title must come from that list. Do not replace `provider quality` or `service quality` with `workforce quality`, `human capital`, or another broader construct unless the body explicitly establishes equivalence.
- Do not modify the source manuscript unless explicitly asked.

A title that promises an unsupported effect, mechanism, scope, or contribution fails regardless of memorability.

## Determine the mode

- **candidates** — propose and rank new titles; this is the default.
- **rewrite** — improve an existing title without discarding useful supported elements automatically.
- **compare** — evaluate user-supplied candidates and recommend one.
- **audit** — test a title's accuracy, information density, distinctiveness, and consistency; do not replace it unless asked.

All modes require an evidence ledger and promise audit.

## Read the paper in two passes

1. Inventory files and versions; identify the paper type and locate the question, results, design or model, mechanism, scope, abstract, introduction, and conclusion.
2. Read the body evidence in depth, then use the abstract, introduction, and conclusion as consistency checks. A polished abstract is not sufficient authority if it overstates the body.

For long manuscripts, search to locate sections and then read enough context to understand what is central versus secondary.

## Build an internal title fact sheet

Follow `references/evidence-protocol.md`. Record:

- central research object and audience;
- central relationship, task, or economic mechanism;
- strongest supportable result or tension;
- evidence type and causal strength;
- model, measurement, or counterfactual identity when central;
- setting, population, period, industry, or institution only if it defines identification, interpretation, or external validity;
- genuine hook vocabulary already connected to the paper;
- claims and words that would overpromise;
- current title elements worth retaining;
- conflicts or unfinished results.

Before generating, freeze a primary-identity bundle: the first-order research object, primary outcome or task, evidence type, indispensable scope, and claim IDs. Label secondary, exploratory, robustness, mechanism-support, and future-only claims separately. Write one accurate, conservative thesis statement before compressing it. Keep the fact sheet internal unless the user asks for an audit.

Copy any manuscript-reported hierarchy (`primary`, `secondary`, `exploratory`, `robustness`) into `source_reported_status` and make it immutable. The Agent may classify status only when the source is silent. A large share, interesting decomposition, precision, preregistration, or narrative appeal cannot promote a source-reported secondary result. Every lexical form of such a claim enters `display_forbidden_terms` immediately.

Create a `display_forbidden_terms` list from every secondary, exploratory, robustness, mechanism-support, and future-only claim. No content word naming those claims may appear anywhere in a displayed title—not even as a coordinate noun or subtitle—unless the source itself classifies that claim as part of the primary identity. Do not promote status during title generation.

For each candidate, record the grammatical-head claim IDs and require every head to belong to the frozen primary spine with `status: central`. A subtitle or rationale cannot rescue a secondary head.

## Handle incomplete evidence

If the central result is unfinished or causal status is unclear, provide conservative topic/task titles and explain briefly that result-based or causal titles should wait. Ask a question only when resolving the issue would materially change the recommended title.

Never fill missing information with a familiar “X and Y: Evidence from Z” template.

## Generate genuinely different candidates

Freeze one primary paper spine before generating titles. Candidate diversity may vary architecture, emphasis, rhythm, design visibility, or scope visibility, but it may not replace that spine with a secondary outcome, subgroup, mechanism-support result, or exploratory claim.

In candidates mode, generate 8–12 working titles across only the families genuinely licensed by the paper:

- concise topic or concept;
- topic plus core relationship or outcome domain;
- core contrast or tension;
- broad concept plus precise subtitle;
- design or setting subtitle when it carries identification or scope information;
- model, measurement, or theory–evidence task;
- result-oriented title only when the result is central, robust, and safe to advertise;
- question title only when both answers are plausible, the tension is real, and the paper clearly answers it.

Do not generate a question or colon title merely to fill a category. Do not count near-duplicate wordings as diversity.

## Audit every candidate as a contract

For each working title, ask:

1. Does the body deliver every noun, modifier, causal term, mechanism, and scope cue?
2. Is the title centered on the paper's first-order contribution rather than an attractive side result?
3. Does `impact`, `effect`, or another causal term match the design?
4. Does a country, industry, period, or institution add identification or scope information?
5. If using `Evidence from`, would deleting the phrase lose real design or boundary information?
6. If using a colon, is the first half memorable and the second half more precise rather than repetitive?
7. Does a hook illuminate the research object rather than create journalistic mystery?
8. Can any word be removed without losing truth, distinction, or readability?

Reject rather than merely down-rank any candidate that fails truth or first-order centrality. Audit the grammatical center, not only individual words: a title can contain only true words and still fail by making a secondary outcome its identity. Apply this identical gate to the recommendation and every strong alternative.

## Rank and compress

Rank survivors in this order:

1. truth and scope fidelity;
2. fit with the paper's central contribution;
3. distinctiveness and search usefulness;
4. information density;
5. natural rhythm and memorability;
6. length.

Use `references/composition-and-length.md` for elastic ranges. The observed Top Five titles are calibration, not a template: the sample's many colon titles do not create a colon preference, and its absence of question titles does not ban questions.

## Run the final audit

- Compare the top titles with the manuscript body, abstract, introduction opening, and conclusion takeaway.
- Check that causal strength and scope remain consistent across all of them.
- Confirm no candidate uses a contribution claim supported only by the literature review or author aspiration.
- Optionally run `scripts/validate_output.py` for counts and lexical warnings. It cannot validate meaning.
- Apply the hard gates and rubric in `references/quality-and-sources.md`.

## Deliver the result

Re-run the complete promise and centrality audit on every title that will be shown. The recommendation and every strong alternative share exactly the same hard gates. `Interesting`, `more accessible`, and `adds variety` are not exceptions. If only one or two titles survive, present fewer rather than weaken the gate. Never show a title and then explain that it overweights a secondary result.

Immediately before delivery, perform a literal forbidden-term scan on the final shortlist. If a rationale would describe a displayed term as `secondary`, `exploratory`, `supportive`, or `not the main outcome`, delete that title. Do not repair it in prose.

Run the same scan on the recommendation and rationale. If either calls a source-reported secondary claim `primary`, `first-order`, `central`, or part of the paper identity, the entire shortlist fails and must be regenerated from the immutable primary set. Candidate-count requirements do not authorize status changes.

Run a noun-by-noun authorized-vocabulary scan after rendering. A fluent synonym absent from `authorized_title_terms` is a failure, not a stylistic improvement. Delete and regenerate that candidate using the manuscript's own economic object.

Run an operator audit too. Map every `versus`, `tradeoff`, contrast, question premise, and directional juxtaposition to an explicit relational claim ID. If selection and preparation are not reported as opposite-signed, use neutral `and` or omit the comparison. Map every institutional umbrella to `exact_institutional_scope`; reject `public` when only `municipal` is supported.

Unless the user requests a single final title, return:

1. **Recommended title** — one English title.
2. **Strong alternatives** — normally two to three English titles with genuinely different information structures. When the user explicitly requests three or four alternatives, generate at least three passing variants by changing architecture, rhythm, design visibility, model visibility, or exact scope while preserving the same primary claim set. Never use a secondary claim merely to fill the count; if three truthful variants genuinely cannot be formed, return fewer and state that constraint briefly.
3. **Why this one** — a brief explanation in the user's language, including the main tradeoff.

Do not display the full title fact sheet, all working candidates, promise-audit table, reference-reading process, or intermediate reasoning unless the user explicitly requests an audit. Build them privately and present only the useful shortlist and concise rationale.

If the user asks for title candidates only, omit explanations. In audit mode, diagnose first and propose replacements only when requested.

Do not acknowledge a failed hard gate and continue. Revise or remove the title; fluency, variety, and completeness cannot compensate.
