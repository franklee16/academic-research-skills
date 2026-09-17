# Economy and consistency diagnostics

Run each criterion as an isolated pass under [diagnostic-protocols.md](diagnostic-protocols.md). These passes follow structure, Flow, and evidence decisions so they do not erase necessary repetition, qualifications, or reproducibility details.

## Redundancy

**Input window:** full paragraph for local redundancy; proposition summaries across a section or manuscript for repeated content.

**Intermediate representation:** reduce candidate spans to propositions, rhetorical functions, qualifications, evidence, and citations.

**Decision test:** flag only semantic duplication that adds no new evidence, scope, contrast, emphasis, or navigation. Keyword repetition and stable terminology are not redundancy.

**Repair boundary:** delete, merge, or shorten while preserving qualifications, reproducibility, citations, and deliberate reinforcement.

**Recheck:** compare propositions and run Flow/meaning checks across the deletion boundary.

## Shell phrases and metadiscourse

**Input window:** complete sentence and paragraph function.

**Intermediate representation:** identify framing phrases and whether they perform navigation, stance, scope, attribution, or no function.

**Decision test:** flag a phrase only when it contributes no necessary rhetorical or epistemic function. Do not remove `we argue`, `the results suggest`, or scope markers merely because they are metadiscourse.

**Repair boundary:** delete or replace only functionless wording.

**Recheck:** verify paragraph navigation, attribution, and claim force.

## Light verbs

**Input window:** complete sentence and terminology register.

**Intermediate representation:** identify light-verb constructions and candidate direct verbs.

**Decision test:** accept a direct verb only if it preserves technical meaning, aspect, tense, agency, and claim strength. A conventional disciplinary phrase may remain.

**Repair boundary:** change the construction, not the proposition.

**Recheck:** compare meaning and grammar in context.

## Terminology consistency

**Input window:** manuscript-wide term index, definitions, headings, figures/tables, and all variants.

**Intermediate representation:** record canonical term, first definition, allowed abbreviation, variants, locations, and whether variants encode real conceptual distinctions.

**Decision test:** flag accidental renaming, inconsistent capitalization/hyphenation, one label used for different concepts, or multiple labels for one concept. Do not standardize away meaningful distinctions.

**Repair boundary:** standardize only when identity is unambiguous; otherwise return `QUERY`.

**Recheck:** rescan every occurrence and linked caption/heading.

## Abbreviations

**Input window:** first occurrence and all uses across the manuscript.

**Intermediate representation:** record full form, abbreviation, first definition, redefinitions, and section-specific reset rules when supplied.

**Decision test:** flag undefined use, definition after use, repeated unnecessary definition, mismatched full form, inconsistent plural, or form drift.

**Repair boundary:** preserve domain conventions and user/venue rules.

**Recheck:** verify first use and every later occurrence.

## Tense

**Input window:** complete paragraph, section type, and the knowledge state or event type of each proposition.

**Intermediate representation:** classify propositions as completed study, ongoing research activity, current knowledge, procedure, observed result, or present interpretation.

**Decision test:** flag tense that mislocates the event/knowledge state or creates inconsistency among peer statements. Do not enforce one tense across an entire section mechanically.

**Repair boundary:** change tense only after identifying proposition type and attribution.

**Recheck:** verify temporal meaning, grammar, and cross-sentence consistency.

## Cross-references, numbering, and formatting

**Input window:** full source with labels, references, headings, equations, figures, tables, lists, citations, and numbering.

**Intermediate representation:** deterministic index of definitions and uses.

**Decision test:** flag missing targets, duplicated labels, stale numbering, broken hierarchy, inconsistent units/format, or references invalidated by a move. Do not alter values during language editing.

**Repair boundary:** repair only source-supported mechanics; protected content remains immutable.

**Recheck:** rescan after every structural change and compare protected tokens.

## Target style

**Input window:** explicit user instructions or an authoritative target-venue guide supplied or retrieved for the task, plus the relevant manuscript elements.

**Intermediate representation:** list only concrete applicable requirements.

**Decision test:** flag a violation only when a requirement is explicit and applicable. Do not invent a venue preference or impose a generic academic style.

**Repair boundary:** apply the requirement without changing evidence, meaning, or unsupported content.

**Recheck:** verify every listed requirement and record any conflict with research integrity or user constraints.

## Section-specific economy safeguards

- Do not delete Methods repetition required for reproducibility.
- Do not remove repeated technical terms merely to create lexical variety.
- Do not delete uncertainty or scope for concision.
- Do not merge Results and interpretation when section convention requires separation.
- Do not remove a citation or attribution while compressing literature synthesis.
