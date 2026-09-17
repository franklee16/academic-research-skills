# Introduction Runtime Core

Read this file completely on every invocation. It is the execution kernel for turning a user's paper materials into an honest and persuasive economics introduction. Detailed references remain normative and supply fuller rationales, exceptions, examples, and repair methods; load them through `SKILL.md` only when the current task presents their issue.

## 1. Keep the introduction's reader purpose fixed

An introduction helps a time-constrained economist answer five questions: What is the economic problem? What exactly does the paper ask? What is its answer? Why should that answer be believed or interpreted as claimed? How does it change verified prior understanding?

Use an inverted information hierarchy: identify the paper early, then earn and refine the answer. Unless a verified fact or debate genuinely needs more setup, the reader should know this paper's bounded question, basic approach, and central answer by the end of the second paragraph. More complete literature comparison normally follows that capsule. This is a functional principle, not a universal paragraph count. A compelling opening, method discussion, result sequence, contribution passage, and roadmap are tools, not compulsory blocks. Every paragraph must move the reader through the paper's question–answer–credibility–meaning chain.

## 2. Establish a closed evidence universe

Before drafting, privately list the files, versions, sections, references, notes, user confirmations, and journal rules that may support the response. The current paper body is the principal authority for what this paper does and finds. Existing introductions, abstracts, conclusions, titles, slides, and author notes are claims to verify unless the user confirms them. A bibliography entry proves only that a work is listed, not that it supports a particular claim.

For long documents, search to locate relevant sections, then read enough surrounding prose, tables, notes, propositions, and appendices to understand estimands, assumptions, hierarchy, and qualifications. Never compose from isolated keyword hits.

Every externally testable clause needs a source owner. This includes hooks, institutional background, compound nouns, transitions, evaluative modifiers, explanatory clauses, intuition, contribution comparisons, and closing synthesis. Source silence means `not established`. General knowledge, disciplinary convention, and a plausible completion of a familiar model do not enter the evidence universe unless the user authorizes outside research and it is actually verified.

Keep source ownership exact:

- the body controls this paper's setting, data, design or model, findings, mechanisms, and scope;
- each cited work controls only its own verified attributes and claims;
- a journal rule controls format, not scientific facts;
- one study cannot lend its assignment unit, setting, treatment, result, or contribution to another;
- a finite literature packet cannot establish the global absence of other work.

## 3. Cold-classify before loading examples

Using only the current user's materials, privately record:

- request mode and required visible output;
- current manuscript version and unresolved conflicts;
- central economic object and bounded question;
- headline claim type: causal, descriptive, theoretical, measured, structurally estimated, counterfactual, historical, or mixed;
- primary paper type and any inferential layer needed for the headline answer;
- credibility burden;
- whether the output requires citations, a gap, novelty, contributions, or literature relationships;
- evidence completeness and readiness.

Set `input_granularity` separately from readiness:

- **full** when readable manuscript sections provide the reasoning, result hierarchy, qualifications, author explanations, and surrounding context behind the claims;
- **sparse** when the authoritative material is only an abstract, compact fact packet, author note, table, or local excerpt without its supporting exposition;
- **mixed** when some claim owners are available in full and others only as summaries or titles.

Do not infer granularity from token count, attachment count, or whether the paper is short. Sparse can still be Ready. In a mixed packet, apply sparse constraints only to the claims whose owners lack supporting context. If fuller material becomes available, reclassify those claims and use the normal path. Read `sparse-packet-protocol.md` before type patterns whenever `input_granularity` is sparse or mixed.

Also record a `risk_profile` using only categories that are actually present: citation/source ownership; causal or mechanism identity; model ontology or authorized intuition; observed, latent, estimated, or counterfactual object identity; selection or method-role interpretation; sparse positioning; version conflict; and risk-note surface. Route the evidence protocol sections from this profile in addition to the universal draft/rewrite sections required by `SKILL.md`.

Freeze this snapshot before reading paper-type examples, calibration sources, eval cases, or historical failures. Those materials may suggest expression and audit risks; they may never fill an unknown field, supply a mechanism, or change readiness without support in the current paper.

Use three private readiness outcomes. **Ready** means the question, answer, credibility, primary findings, boundaries, and requested positioning are sufficiently supported. **Conservative-ready** means the paper can be introduced honestly but a material gap, priority, or positioning claim must be omitted or narrowed. **Blocked** means a missing fact or conflict changes the central question, principal answer, treatment or model identity, main result, or a positioning claim the user expressly requires. Do not block merely because optional intuition, mechanisms, heterogeneity, policy content, roadmap, target length, or global novelty evidence is absent.

These are control states, never manuscript content. Do not print them or narrate the process in a draft or rewrite.

Maintain a private `loaded_sections` register keyed by file and section. Read each selected section once. Add a section only when a newly discovered risk requires it; final auditing does not justify re-reading an already loaded type or literature resource.

## 4. Build a minimal manuscript fact ledger

For every claim likely to appear, privately record:

| Field | Meaning |
|---|---|
| source owner and location | Exact section, table, proposition, note, or user confirmation |
| authorized claim | The smallest proposition actually supported |
| semantic role and object identity | Context, treatment, outcome, proxy, latent object, parameter, model result, counterfactual, mechanism, or contribution |
| inferential status | Causal, associational, descriptive, model-implied, simulated, suggestive, or not established |
| scope | Unit, population, setting, baseline, horizon, and comparison |
| source hierarchy | Primary, secondary, exploratory, robustness, limitation, or other label only when the source itself uses or clearly establishes it |
| allowed wording | Strongest accurate phrasing |
| introduction priority | Core, boundary-changing, useful, or omit |
| conflict or missing evidence | What would need resolution |

Lock identities across the whole introduction. A bundled treatment remains the causal subject; a separately unidentified mechanism cannot replace it in the question, answer, implication, or contribution. A latent construct is not an observed proxy, a realized outcome is not an estimated parameter, and a model counterfactual is not a reduced-form effect. Preserve direction, magnitude, unit, denominator, sample, time horizon, comparison basis, uncertainty, and result hierarchy.

Re-lock the exact noun and scope every time a result is restated. An earlier qualification does not travel automatically: a null in an observed test subsample cannot later become a result about learning; realized output per megawatt cannot later become latent project quality; a structurally estimated or counterfactual object cannot later become an observed effect. Prefer the manuscript's exact term over a broader synonym.

Record a reported result separately from its explanation. Mark any explanation as proved, model-implied, source-stated but suggestive, or absent. A result alone never licenses an intuitive `because`, behavioral chain, crowd-out story, institutional purpose, or proof sketch. A method name licenses accurate naming, not an unreported statement about why it identifies the effect, what a fixed effect absorbs, or which variation remains.

A request to explain intuition does not expand the evidence universe. If the materials give only a proposition, estimate, pretrend, or mechanism-consistent pattern, report its result and stated conditions without inventing a named force, dominance relation, selector type, fixed-effect role, purpose, proof logic, or behavioral step. Ask for the author's intuition only when it is indispensable; otherwise write a precise shorter account.

If any of these identities are difficult, load the relevant sections of `evidence-and-positioning-protocol.md` before writing.

## 5. Build literature evidence only when needed

When citations or positioning enter the task, create a private literature ledger for each relationship:

`citation identity → source availability and version → exact prior-work claim → comparison axis → comparison universe → relation to this paper → strongest licensed wording → unresolved support issue`

Then test each contribution through both sides:

`what this paper delivers → which verified work it is compared with → the exact dimension of difference → why that difference matters → where the body delivers it`

If either side lacks evidence, retreat to a concrete description of this paper's question, data, design, model, measurement, or finding. Do not replace evidence with `first`, `only`, `novel`, `little is known`, `fills a gap`, claims that other models cannot generate a result, or an invented literature consensus. Be generous to prior work and specific about differences. Literature paragraphs should explain relations, not inventory authors.

Load `literature-positioning-and-contributions.md` whenever a nontrivial gap, novelty, contribution, or citation relationship will appear. Load the relevant evidence protocol sections when source versions, quoted claims, or comparison ownership are uncertain.

## 6. Freeze a conservative spine

Introduction functions are selection obligations, not permission to complete missing premises. If the sources do not authorize a motivating fact, method role, mechanism, intuition, literature relation, implication, or transition premise, realize that function through a narrower supported statement or omit it. Never invent a bridge merely because the composition plan contains tension, credibility, meaning, or positioning.

Write one private sentence containing the bounded question, headline answer, and strongest supportable credibility identity. The opening, results, contribution, and closing must preserve that same subject and claim type.

Plan with this default dependency graph:

`specific tension or obstacle → bounded question → early paper-and-answer capsule → credibility architecture → ordered findings → changed understanding and necessary boundary → verified positioning → optional roadmap`

This graph is not a paragraph template. Merge, split, integrate, preview, or reorder functions when the reader's dependency changes. Literature can appear early to establish a verified debate or measurement obstacle. A setting can open the paper when it creates the design. A theoretical paper can open with an economic possibility rather than an external trend. A result can open the paper when it defines the puzzle.

The early capsule is a preview, not a first full results section. Normally state the headline answer and at most the one magnitude needed to identify it; reserve qualifications and connected results for the later result story. Do not report the same exact magnitude twice. Give the primary answer the greatest weight. Include a secondary result, mechanism, heterogeneity pattern, null, robustness exercise, cost, or limitation only when removing it would change the reader's understanding of the main answer, credibility, or indispensable boundary. Accuracy is necessary but not sufficient for introduction eligibility.

If the packet supplies no verified broad fact, controversy, theoretical benchmark, or literature tension, start directly with the paper-specific variation, measured contrast, economic possibility, or research task. A plain supported opening is stronger than a vivid invented one.

Use a roadmap only when the supplied paper or user provides the actual section numbers and responsibilities. Never infer a conventional Section 2–6 sequence from the model or empirical content. Sparse evidence should produce the minimum complete introduction—often only a few paragraphs—not generic background, repeated cautions, or invented measurement detail added to imitate a calibration length.

## 7. Draft with calibrated freedom

Keep factual atoms low-freedom and rhetoric high-freedom. Exact objects, numbers, estimands, samples, causal status, model primitives, mechanisms, cited claims, and contribution axes stay fixed. Syntax, transitions, rhythm, local order, and paragraph count may vary.

Make credibility intelligible rather than listing methods. Explain only the source-supported role of the design, archival construction, measurement solution, model discipline, or identifying variation. For mixed papers, preserve every inferential layer: descriptive evidence, reduced-form effects, structural estimates, model-implied mechanisms, and policy counterfactuals do not merge merely for narrative smoothness.

State one indispensable limitation next to the claim it qualifies and then move on. Do not repeat noncausal status, model dependence, selection, mechanism uncertainty, or incomplete literature coverage until the introduction reads like an audit. Use evaluative terms such as large, important, efficient, robust, stable, or policy-attractive only when a verified benchmark supports them.

Let length respond to the argument. Expand only when the reader needs more setting, credibility, model logic, connected findings, or verified literature positioning to understand the answer. Compress generic importance claims, repeated results, routine robustness, unverified novelty, citation lists, and redundant roadmaps. Target-journal rules and explicit user constraints prevail.

## 8. Run three private audits

Before delivery, check in both directions:

1. **Output to evidence:** every substantive span, number, causal verb, mechanism, contextual fact, citation, evaluation, gap, novelty statement, and comparison has the correct source owner and semantic role.
2. **Evidence to output:** the question, answer, credibility, primary findings, interpretation-changing boundary, and defensible positioning have not been displaced by a more dramatic secondary detail.
3. **Introduction to body:** every advertised finding and contribution maps to a body location; the introduction promises nothing the paper does not deliver.

Then apply two global tests. First, after the opening movement, could an economist accurately retell the paper's specific question, answer, and credibility rather than only its broad topic? Second, do the opening question, answer, contribution passage, and closing still use the same treatment, object, scope, and inferential status?

Perform a deletion pass after those tests. If the main result or the same limitation appears more than once, each later occurrence must add indispensable credibility, scope, or interpretation; otherwise delete it. A verified literature claim may establish an opening tension or a later contribution comparison, but do not narrate the same paper-level facts in both places merely to lengthen the introduction.

For draft or rewrite, keep all of this private. Compose `formal_prose` and, only when materially needed, a `risk_note` containing only the missing source, affected claim category, and exact evidence status. Summarize categories; never quote, number, or rebut the user's unsupported requests one by one. Serialize them once into a single `delivery_buffer`: English prose first, then at most one blank line and one or two short, unlabelled sentences in the user's language. Read `final-delivery-gate.md` last and apply it to the exact buffer. Any revision requires a fresh full pass. Return the buffer once; emit nothing before or after it.
