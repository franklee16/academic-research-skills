# Sentence clarity diagnostics

Run each criterion as an isolated pass under [diagnostic-protocols.md](diagnostic-protocols.md). Retain local context so sentence edits do not damage topic continuity, agency, claim strength, or technical terminology.

## Agent--action

**Input window:** target sentence plus the surrounding paragraph.

**Intermediate representation:** identify semantic agent, action, affected object, grammatical subject, and main verb.

**Decision test:** flag an empty abstract subject, hidden agent that readers need, weak verb that obscures the principal action, or grammatical structure that assigns the action to the wrong entity.

**Repair boundary:** restore a concrete subject or verb only when agency is known. Do not invent an agent or replace a standard technical nominal.

**Recheck:** compare agent, action, attribution, and paragraph topic before and after.

## Nominalization

**Input window:** complete sentence and terminology register.

**Intermediate representation:** list nominalized actions, their governing verbs, possible agents, and whether the noun is an established technical construct.

**Decision test:** flag a nominalization only when it hides agency/action, creates a weak light-verb phrase, or adds syntactic load. Preserve technical terms and nouns that serve topic continuity.

**Repair boundary:** convert to a verb when meaning, tense, and disciplinary usage remain intact.

**Recheck:** verify agent, action, topic position, and technical term preservation.

## Subject--verb distance

**Input window:** complete sentence.

**Intermediate representation:** mark main subject, main verb, intervening clauses/phrases, and any competing possible subject.

**Decision test:** do not use a word-count threshold alone. Flag only when the interruption creates a likely misparse, delays the main action unreasonably, or separates a subject from its correct verb.

**Repair boundary:** move an interruption, split the sentence, or restate the subject without losing qualifications.

**Recheck:** read the sentence for one-pass parsing and confirm that moved material still limits the correct proposition.

## Voice

**Input window:** complete paragraph plus attribution requirements.

**Intermediate representation:** record paragraph topic, known agent, action, and whether agency or process continuity matters more.

**Decision test:** choose passive when it preserves the established topic or the agent is irrelevant/unknown; choose active when agency, responsibility, or analytical choice matters. Voice is not a general quality score.

**Repair boundary:** change voice only when the current choice causes an agency, continuity, or ambiguity defect.

**Recheck:** rerun topic position, attribution, and meaning-integrity checks.

## Noun strings

**Input window:** target sentence, terminology register, and nearby definitions.

**Intermediate representation:** identify consecutive noun modifiers and generate plausible attachment structures.

**Decision test:** flag when two or more interpretations remain plausible, component relationships are unclear, or a nonstandard compound masks the head noun. Preserve established compounds.

**Repair boundary:** unpack with prepositions, clauses, or defined compounds. Use `QUERY` when the intended relation is uncertain.

**Recheck:** ensure the revised relation matches the definition and terminology elsewhere.

## Sentence load and boundaries

**Input window:** target sentence and adjacent sentences.

**Intermediate representation:** enumerate propositions and rhetorical tasks: result, evidence, comparison, interpretation, mechanism, condition, limitation, or implication.

**Decision test:** split when independent tasks obscure their relations or overload one grammatical frame; merge only when fragments repeat context or falsely separate one proposition. Sentence length alone is not a defect.

**Repair boundary:** make relation and claim strength explicit across the new boundaries. Preserve citations and qualifiers with the propositions they support.

**Recheck:** rerun sentence relation, Hedging, reference, and stress-position checks.

## Ambiguity and modifier attachment

**Input window:** complete sentence plus necessary referents.

**Intermediate representation:** list plausible readings for modifiers, coordination, scope, negation, comparison, and pronoun attachment.

**Decision test:** flag when more than one reading is grammatically and contextually plausible or when the intended scope requires rereading.

**Repair boundary:** move or expand the modifier, repeat a noun, or split the clause. Use `QUERY` if author intent is not recoverable.

**Recheck:** confirm one intended reading without changing scientific scope.

## Grammar and punctuation

**Input window:** target sentence plus adjacent sentence when agreement, tense, reference, or punctuation depends on context.

**Intermediate representation:** identify the precise rule or grammatical relation involved.

**Decision test:** check agreement, articles, countability, tense consistency, comparison form, modifier attachment, parallel construction, fragments, run-ons, and punctuation function. Do not combine this pass with general rewriting.

**Repair boundary:** change only the grammatical construction and any connected tokens required for correctness.

**Recheck:** verify grammaticality, meaning, LaTeX integrity, and surrounding Flow.

## Read-aloud symptom pass

Use reading aloud or text-to-speech only as a symptom detector for unnatural pauses, excessive interruption, repeated rhythm, reference ambiguity, or sentence load. Route every symptom to the applicable criterion above; `sounds awkward` is not itself a sufficient diagnosis.
