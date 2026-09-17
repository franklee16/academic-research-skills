# Evidence Protocol for Manuscript-Grounded Writing

This protocol is a hard gate. Use it in candidates, rewrite, compare, and audit modes. It converts a manuscript into a traceable set of claims before title generation.

## 1. Establish the evidence universe

Inventory every supplied manuscript file and identify versions. Read the body as the principal evidence source. Treat the introduction, current abstract, conclusion, title, slides, and user notes as claims to verify unless the user explicitly confirms them.

For a long manuscript, first map sections and then read the full local context of relevant passages. Search helps locate evidence; it does not replace interpretation.

## 2. Classify the paper

Choose one or more: causal empirical; associational or descriptive; measurement; structural or quantitative; theoretical; historical; mixed. The classification controls whether causal, design, model, measurement, historical, or counterfactual language belongs in the title.

## 3. Build the title claim ledger

For every possible title promise, record:

| Field | Meaning |
|---|---|
| `claim_id` | Stable short ID |
| `claim_type` | object, relationship, result, mechanism, design, model, setting, scope, contribution, hook |
| `exact_claim` | Conservative statement the body supports |
| `source_file` | Source manuscript file |
| `source_location` | Section, page, table, figure, theorem, or paragraph |
| `support_level` | explicit, strongly implied, author interpretation, absent, conflicting |
| `status` | central, secondary, robustness, exploratory, future only |
| `causal_status` | causal, associational, descriptive, theoretical, model-implied, unclear |
| `scope` | Population, place, institution, period, outcome, horizon |
| `mechanism_level` | identified, model-implied, direct test, consistent-with, suggestive, speculative |
| `allowed_wording` | Strongest safe title wording |
| `title_priority` | essential, useful, optional, exclude |
| `conflict_or_gap` | What remains unresolved |
| `primary_identity_membership` | yes/no |
| `eligible_as_title_center` | yes/no |
| `eligible_as_modifier_only` | yes/no |
| `exclusion_reason` | Why a supported claim cannot define a title |
| `primary_spine_claim_ids` | Claim IDs that must remain the title's grammatical and conceptual center |
| `grammatical_head_claim_ids` | Claim IDs expressed by the title's head noun phrase or main predicate |
| `head_status_check` | Whether every grammatical head belongs to the frozen primary spine |
| `forbidden_broadenings` | Unsupported synonyms, gerund claims, mechanism upgrades, and broader promises |
| `coordinated_head_claim_ids` | Claim IDs for every noun sharing coordinate title-center status |
| `display_eligible` | yes only when all grammatical and coordinated heads are central primary-spine claims |
| `observability` | directly observed, measured proxy, model-implied, counterfactual, or unobserved |
| `required_title_marker` | model/structural/counterfactual/scope marker required to prevent a false observational promise |
| `exact_geographic_scope` | Exact states, regions, institutions, or countries supported by the body |
| `source_reported_status` | Immutable primary, secondary, exploratory, robustness, or unspecified status stated by the manuscript |
| `status_authority` | source when reported; agent classification only when source is silent |
| `authorized_title_terms` | Exact manuscript nouns and explicitly equivalent terms allowed in displayed titles |
| `forbidden_object_substitutions` | Smooth but materially different umbrella terms for the outcome, population, market, or contribution |
| `exact_institutional_scope` | Exact municipal, state, occupational, industry, program, or market level supported by the body |
| `relational_operator` | and, versus, tradeoff, tension, contrast, directional, or question premise |
| `operator_support_claim_ids` | Explicit claims licensing opposition, direction, or tension; empty forbids the operator |

Keep the ledger internal unless the user asks for an audit.

Support is necessary but not sufficient. A secondary, robustness, exploratory, mechanism-support, or future-only claim defaults to `eligible_as_title_center: no`. It may appear only as a subordinate modifier when necessary for truthful distinction and when it does not redefine the paper.

For the delivered shortlist, use a stricter default: claims with those statuses are `display_forbidden` everywhere, including coordinate noun phrases and subtitles. Relax this only when the manuscript—not the title generator's interest judgment—explicitly includes the claim in the primary paper identity. Freeze status before candidate generation and never promote a claim merely to create variety.

Source-reported hierarchy overrides all Agent judgments. If the manuscript labels a result secondary, every faithful synonym and umbrella form for that result is display-forbidden. Its magnitude, explanatory share, statistical strength, or preregistration does not change the status. Do not reinterpret `72 percent of additional bids came from ...` as making entrant composition a primary outcome when the source identifies that analysis as secondary.

## 4. Calibrate title language

- Use `impact`, `effect`, or another causal construction only when the design supports it for the advertised scope.
- In associational work, name the objects or relationship without implying causation.
- In structural work, distinguish the model, estimated object, and counterfactual task.
- In theory, advertise the economic environment, mechanism, or proposition rather than empirical validation the paper lacks.
- In historical work, retain the period or institution when it defines the contribution or scope.

Do not let causal wording in an old title override the body.

Preserve the manuscript's technical nouns and classifications. Do not replace `output per employee` with `productivity`, `linked firm-worker panel` with `matched employer-employee data`, or an eligibility threshold with an unreported label such as `mid-sized` unless the manuscript establishes that equivalence. A smoother synonym is unacceptable when it changes the economic object, sample, design, or contribution.

Apply a closed-world paraphrase rule: a title may promise only the exact object, relationship, scope, causal status, mechanism level, and centrality licensed by the ledger. Treat gerunds and action nouns as factual promises. `Reducing Information Frictions` claims that the paper establishes a reduction; it is not a neutral topic label. If the body only offers evidence consistent with an information-friction channel, use an object/task formulation or omit the channel.

## 5. Calibrate mechanisms and contribution

Do not put a mechanism in the title unless it is central and supported at a level that can survive the compression. Never turn suggestive evidence or author speculation into a title fact.

`First`, `new`, `novel`, `unique`, and broad contribution labels require explicit, narrowly scoped support. Prefer showing contribution through concrete nouns: the object, design, model, measurement target, contrast, or setting.

## 6. Decide whether scope belongs

A place, country, industry, institution, or period earns title space when it:

- supplies distinctive identifying variation;
- defines the population to which the claim applies;
- is the substantive object of the paper;
- makes an otherwise generic title meaningfully distinctive.

It does not earn space merely because the data came from there.

## 7. Resolve conflicts and unfinished evidence

Do not choose silently between conflicting result directions, causal claims, or manuscript versions. Ask only if the resolution would change the recommended title. Otherwise provide conservative object/task titles and explain that result-based wording should wait.

Never use an unfinished result, a future direction, or “not reported” information as a title promise.

## 8. Audit title promises

Map every content word in a candidate to one or more claim IDs. Reject the title if it introduces:

- an unsupported causal effect;
- an untested mechanism;
- a broader population or period than the evidence;
- an unsupported novelty claim;
- a secondary or robustness finding as the main identity;
- a design label the paper does not use or justify;
- a hook unrelated to the actual research object.
- an unreported qualitative label or terminology substitution that changes the economic object, sample, design, or contribution.

Critical factual failures cannot be offset by clever wording.

Audit the grammatical and conceptual center of each title, not only its words. A title can contain only true terms yet fail by making a secondary outcome its main noun phrase.

Freeze the primary identity before generating candidates. For every displayed candidate, record its grammatical head claim IDs and reject it unless those heads are members of `primary_spine_claim_ids`. A secondary result may not become the center merely to diversify the shortlist.

Run a literal token/concept scan against all `display_forbidden` claims. If any displayed title contains one, discard the title. When fewer candidates survive than requested, return fewer.

Treat every noun in a coordinated list as a co-head. In a form such as `Information, Entry, and Prices`, all three nouns occupy title-center status. Build a hidden candidate table containing candidate, grammatical/coordinated heads, claim IDs, statuses, and `display_eligible`; render only rows marked yes, with no free-form override for variety.

Observability is part of the title promise. A title that foregrounds preparation, effort, latent types, or another model-only decision must say `model`, `structural`, or an equally clear marker in that title. A rationale cannot supply the missing marker. Likewise, copy exact geographic scope into the ledger: a multi-state sample is not a national market, and `U.S.` cannot replace `17 U.S. states` when the distinction matters.

Generate substantive nouns only from `authorized_title_terms`. Authorize a synonym only after confirming bidirectional substantive equivalence for the manuscript's estimand and contribution. `Provider quality` or `service quality` does not entail `workforce quality`; the latter changes the unit and economic object. Map every noun in the final shortlist to its authorized source term and reject unmapped nouns.

Scope umbrellas require evidence: municipal procurement is a subset of public procurement but does not license a public-procurement-wide title. Copy `exact_institutional_scope` unless the body establishes the broader level. Likewise, `versus`, `tradeoff`, `tension`, and similar operators assert opposition. Permit them only when `operator_support_claim_ids` contains explicit opposite-signed or source-stated conflict evidence. Coexistence of selection and preparation is not opposition.

When a requested count requires additional candidates, vary only title architecture using primary heads: topic; question; design-visible subtitle; model-visible subtitle; exact setting; or result wording whose full qualification survives. Re-run all gates on each. Candidate-count pressure never promotes a secondary claim.
