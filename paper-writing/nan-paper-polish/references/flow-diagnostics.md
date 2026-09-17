# Flow and Cohesion diagnostics

Treat Flow as the reader's ability to traverse a coherent and cohesive argument with low avoidable inference cost. Run every applicable criterion below as an isolated pass under [diagnostic-protocols.md](diagnostic-protocols.md). Never diagnose Flow from an isolated sentence or equate Flow with adding transitions.

## Required context hierarchy

| Level | Input | Purpose |
|---|---|---|
| Manuscript | title, abstract, section order, research questions | global reader path |
| Section | all paragraph-function summaries | paragraph order and functional gaps |
| Paragraph group | previous/current/next paragraphs or summaries | paragraph relations |
| Full paragraph | every sentence in order | relations, topic chain, old--new progression |
| Local span | target plus neighbors and global registers | reference, term, topic/stress position |

## Global and section Flow

**Input window:** the manuscript outline and complete paragraph-function map for the section.

**Intermediate representation:** a reverse outline showing each unit's function, prerequisite, and consequence.

**Decision test:** flag repetition, loops, unexplained scope changes, a consequence before its premise, a section that does not support the research question, or an Introduction promise not answered in Results/Discussion.

**Repair boundary:** reorder or bridge only with logic already supported by the source. A missing premise is `QUERY`, not an invitation to invent a smooth bridge.

**Recheck:** read only the reverse outline, then inspect every changed boundary in full prose.

## Paragraph relation

**Input window:** the current paragraph, preceding and following paragraphs, and their function summaries.

**Intermediate representation:** label the relation to each neighbor, such as background--problem, problem--method, method--limitation, claim--evidence, result--interpretation, comparison, contrast, sequence, or qualification.

**Decision test:** distinguish:

1. a real relation that is already clear (`PASS`);
2. a real relation that is underexpressed (`ISSUE`);
3. wrong paragraph order (`ISSUE` or `QUERY` by risk);
4. a missing argumentative step (`QUERY` unless the source states it elsewhere);
5. no defensible relation (`ISSUE` for removal/move or `QUERY`).

**Repair boundary:** use a topic sentence, relation clause, supported bridge, local move, split, or merge according to the diagnosed cause. Do not add a connective before the real relation is known.

**Recheck:** relabel both boundaries after revision.

## Sentence relation

**Input window:** the complete paragraph plus adjacent paragraph-function summaries when the first or last sentence is involved.

**Intermediate representation:** label every adjacent sentence pair as continuation, contrast, cause, consequence, evidence, example, interpretation, condition, sequence, or another exact relation.

**Decision test:**

- relation true and recoverable: `PASS`;
- relation true but unreasonably implicit: `ISSUE`;
- connective asserts a false relation: `ISSUE`;
- relation depends on an unstated premise: `QUERY`;
- sentences serve incompatible paragraph functions: propose move/split or `QUERY`.

**Repair boundary:** state or restore the real relation. Never report only `flow is weak`; name the broken link and its reader cost.

**Recheck:** regenerate the complete sentence-relation map for the paragraph.

## Topic chain

**Input window:** complete paragraph; include the preceding paragraph topic for the first sentence.

**Intermediate representation:** list each sentence's grammatical subject and discourse topic using stable canonical terms.

**Decision test:** flag random shifts, unnecessary synonym variation, a new topic without setup, ambiguous pronouns, or a return to an earlier topic that forces rereading. Do not flag a topic shift that marks a justified rhetorical move.

**Repair boundary:** prefer a stable term, explicit referent, local reorder, or topic-preserving voice choice. Do not force identical subjects.

**Recheck:** read only the topic chain and then the full paragraph.

## Old--new progression

**Input window:** complete paragraph, with the prior paragraph's final established information when relevant.

**Intermediate representation:** mark familiar information at each sentence opening and emphasis-worthy new information near each ending. Link each new item to where it becomes given.

**Decision test:** flag an opening concept with no definition/setup, a sentence that does not inherit any established information, or an ending that cannot support the next sentence. Route abrupt first occurrences to `TERM-INTRODUCTION`.

**Repair boundary:** reorder sentences or clauses, replace an ambiguous reference, or introduce a source-supported concept before use.

**Recheck:** regenerate the old--new map for all affected sentences.

## Reference resolution

**Input window:** complete paragraph and the previous paragraph when needed.

**Intermediate representation:** for every potentially ambiguous `it`, `this`, `these`, `which`, `former/latter`, generic `method/framework/result`, and numbered pointer, list all grammatically and semantically plausible antecedents.

**Decision test:**

- exactly one recoverable antecedent: `PASS`;
- two or more plausible antecedents: `ISSUE`;
- no recoverable antecedent: semantic gap or `QUERY`;
- reference to a proposition: test whether an exact summary noun is required.

**Repair boundary:** use the exact noun or `this/these + summary noun` only when ambiguity is real. Do not replace clear pronouns mechanically.

**Recheck:** resolve every reference in the revised paragraph without consulting the original.

## Terminology introduction

**Input window:** manuscript-wide first-occurrence index; for each candidate, the first-occurrence paragraph, the previous paragraph, later role, and any available definition.

**Intermediate representation:** record first occurrence, definition/inference path, canonical form, later use, and whether the term's role is established.

**Decision test:** classify as naturally introduced, undefined acronym, abrupt proper term, premature concept, unclear role, inconsistent first definition, or `QUERY` for missing author knowledge.

**Repair boundary:** define from source material, connect to an established concept, delay the term, or ask the author. Never invent a definition.

**Recheck:** verify first occurrence, definition, canonical form, and every later use.

## Topic position

**Input window:** complete paragraph, not the target sentence alone.

**Intermediate representation:** identify the paragraph's current story and the topic/grammatical subject of each sentence.

**Decision test:** flag a sentence opening only when it foregrounds incidental or wholly new information and thereby breaks the established story. A deliberate shift with a clear function is valid.

**Repair boundary:** move the established topic or backward link into the opening, or choose a voice that preserves continuity. Do not force one subject throughout.

**Recheck:** regenerate the topic chain and confirm that agency and meaning remain correct.

## Stress position

**Input window:** target sentence, preceding and following sentences, and paragraph function.

**Intermediate representation:** identify intended emphasis, new information, natural closure position, and what the next sentence develops.

**Decision test:** flag an important finding buried mid-sentence, incidental details stealing closure, or a sentence ending that sets up the wrong next topic. Do not move required conditions away from the proposition they limit.

**Repair boundary:** reorder clauses or relocate incidental material without changing scope, qualification, or technical meaning.

**Recheck:** confirm the intended emphasis, old--new progression, rhythm, and next-sentence link.

## Transitions

**Input window:** the full adjacent sentences or paragraphs.

**Intermediate representation:** infer the real relation while temporarily ignoring the existing connective, then compare the connective's semantics with that relation.

**Decision test:** classify as accurate, missing but needed, false, redundant, or masking a missing premise.

**Repair boundary:** add, replace, or remove a transition only after validating the relation. A missing premise is `QUERY`.

**Recheck:** ensure the connective remains true when the surrounding propositions are read literally.

## Parallelism

**Input window:** the complete list or set of peer objectives, steps, results, comparisons, or limitations.

**Intermediate representation:** extract the syntactic frame and logical level of each peer item.

**Decision test:** flag inconsistent structure only when it obscures equivalence, hierarchy, comparison basis, or sequence.

**Repair boundary:** align structure without altering technical roles or falsely making non-peer items equivalent.

**Recheck:** read the frames without content, then verify content and meaning.

## Flow repair order

Prefer the repair that matches the root cause:

1. explicit referent;
2. stable terminology;
3. local old--new or topic reorder;
4. accurate relation clause or connective;
5. short bridge supported by existing text;
6. sentence or paragraph move;
7. author query for a missing premise or ambiguous meaning.

This is a diagnostic order, not a requirement to keep edits small. Make every connected change needed for a complete repair.

## Required Flow recheck

After any structural or local prose edit, rerun the affected paragraph-function map, paragraph relations, sentence relations, topic chain, old--new map, reference register, terminology-introduction register, topic position, and stress position. A sound reverse outline alone does not establish sentence-level Flow.
