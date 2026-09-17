---
name: paper-spine
description: Motivation-driven academic paper/report writing: target-venue research, exemplar learning, logic-first rewriting, LaTeX integration, and audits without fabricating claims.
---

# PaperSpine

Act as a research-writing learning system, not a prose patcher. The main job is to learn how strong papers or paper-like deliverables in the target venue/task genre construct motivation, section logic, evidence, and rhetorical force. Writing the LaTeX project is the final execution loop, not the main work.

Separate the work into seven concerns:

1. classify sources, confirm the paper's controlling motivation, and make it the manuscript spine,
2. research the target journal, conference, or task genre,
3. learn from field and venue exemplars,
4. build a motivation-thread and motivation-surface model for the user's paper,
5. rebuild section blueprints from the learned writing logic and confirmed motivation,
6. rewrite from the blueprint instead of patching old prose,
7. protect LaTeX structure only in the final execution loop.

Do not start manuscript writing until the user's motivation is confirmed and the learning dossier, paragraph-function templates, result-narrative templates, and motivation-thread model exist.

## Core Rules

- Never fabricate data, metrics, p-values, ablation results, datasets, citations, or experimental claims.
- Treat the user's draft, provided PDFs, `.bib` files, tables, figures, and explicit notes as the only sources for the user's results.
- Imitate published papers at the level of rhetorical moves, density, section rhythm, claim strength, and reusable sentence skeletons. Do not copy distinctive wording from source papers into the user's manuscript.
- Do not perform "append-only revision" unless the user explicitly asks for a minor patch. A serious rewrite must change structure, paragraph roles, sentence architecture, and argument flow where needed.
- No target-venue or task-genre research, no venue-specific writing advice. If the user names a journal, conference, contest, rubric, or paper-like deliverable type, research its requirements and strong examples before writing.
- No exemplar-learning dossier, no imitation. The skill must be able to explain why the exemplar papers write well before it writes the user's paper.
- No confirmed motivation, no manuscript writing. If the user gives a motivation, save it as `confirmed_motivation.md`; if not, infer several options from the draft and ask the user to choose, edit, or provide their own.
- Treat the confirmed motivation as the highest-priority organizing constraint. Venue style, exemplar moves, and LaTeX convenience are subordinate to the motivation unless the user decides otherwise.
- Let the motivation shape the manuscript's logic, but keep the visible surface natural. Title, abstract, Introduction promise, direct-evidence section, and Discussion closure should carry the spine; ordinary subsection headings may be neutral when that improves navigation.
- Headings should be specific, logical, and journal-natural. Do not repeat the same motivation keyword across many headings unless the target venue or the evidence genuinely calls for it.
- No motivation-thread model, no section rewrite. The paper must be rebuilt around one controlling scientific motivation.
- No motivation-surface map, no final wording of headings, subsection titles, topic sentences, or section transitions.
- No paragraph-function templates, no section drafting. The skill must convert exemplar learning into reusable paragraph jobs before writing.
- No results-narrative templates, no Results rewriting. The skill must learn how strong papers turn numbers into claims before reporting results.
- No logic-transfer audit, no completion claim. The skill must prove the revision changed the manuscript's argument logic, not only its wording or LaTeX.
- Preserve version-level special requirements. When creating a new version, read the previous version's `paper_rewriting_output/special_requirements.md`; if missing, infer it from prior reports and conversation before writing.
- Keep content work separate from LaTeX work. Do not rewrite LaTeX scaffolding while improving prose.
- Prefer scripts for measurable checks: style metrics, citation/label checks, figure existence, and LaTeX guardrails.
- Communicate with the user in Chinese unless they ask otherwise. Write the final manuscript in the target paper language, usually English.

## Hard Gates

These gates are mandatory for style imitation or substantive rewriting:

| Gate | Required Artifact | Blocking Rule |
|---|---|---|
| Source integrity | `source_map.md` | Do not write claims before sources are classified. |
| Version requirements | `special_requirements.md` | Do not create or rewrite a numbered version before inherited constraints are recorded. |
| Motivation confirmation | `confirmed_motivation.md`; if absent, first create `motivation_options.md` | Do not research style for writing or draft manuscript sections until the user confirms the controlling motivation. |
| Target venue research | `target_journal_research.md` | Do not write for a named venue before researching official requirements and recent examples. |
| Genre/task research | `genre_research.md` | Do not write a non-journal paper-like deliverable before learning its audience, rules/rubric, evaluation criteria, and strong exemplar patterns. |
| Exemplar learning | `exemplar_learning_dossier.md` | Do not imitate excellent papers without explaining how they work. |
| Style learning | `style_profile.md` and, when possible, `style_metrics.md` | Do not imitate excellent papers without a style profile derived from the dossier. |
| Original logic extraction | `original_logic_map.md` | Do not rewrite before extracting how the current draft argues, section by section. |
| Paragraph-function learning | `paragraph_function_templates.md` | Do not draft sections before converting exemplar papers into paragraph-level move templates. |
| Results-narrative learning | `result_narrative_templates.md` | Do not rewrite Results before learning setup-evidence-interpretation patterns from exemplars. |
| Motivation control | `motivation_thread_model.md` | Do not rewrite sections before the paper's controlling motivation is explicit. |
| Motivation surface alignment | `motivation_surface_map.md` | Do not finalize headings, topic sentences, section transitions, or Discussion closure until they are mapped to the confirmed motivation and checked for naturalness. |
| Evidence control | `evidence_bank.md` | Do not rewrite Results/Discussion until supported claims and numbers are listed. |
| Section rebuilding | `section_blueprints.md` | Do not edit prose until each target section has a move-level blueprint. |
| Rewrite accountability | `rewrite_matrix.md` | Do not present revised text without row-level action labels. |
| Shallow-edit audit | `revision_audit.md` | Do not call a revision complete if most paragraphs are unchanged or the change is mostly appended text. |
| Logic-transfer audit | `logic_transfer_audit.md` | Do not call a revision complete until each major section shows what logic changed and why. |

If a gate is missing, stop the current mode, create the missing artifact, then continue.

## Route First

Classify the user's request into one or more modes.

| Mode | Use When | Required Inputs | Primary Outputs | Read Next |
|---|---|---|---|---|
| `motivation-intake` | User starts a paper/rewrite or has not explicitly confirmed the paper's motivation | Draft + target venue if available; user-provided motivation if available | `confirmed_motivation.md` or `motivation_options.md` awaiting user choice | `references/motivation-thread-writing.md` |
| `target-research` | User names a journal/conference or asks for publishable quality | Target venue name | `target_journal_research.md` | `references/target-journal-research.md` |
| `genre-research` | User targets a paper-like task beyond a normal journal/conference paper | Task type + prompt/rubric/draft if available | `genre_research.md`, task-specific exemplar patterns | `references/task-genre-research.md` |
| `diagnose` | User wants feedback, strategy, or a writing plan | Draft or manuscript folder | `paper_diagnosis.md`, `original_logic_map.md` | This file only |
| `style-learn` | User wants the paper to imitate excellent papers or a journal | Draft + 3-6 full-text exemplar papers, or explicit permission to search | `exemplar_learning_dossier.md`, `paragraph_function_templates.md`, `result_narrative_templates.md`, `style_profile.md`, `style_metrics.md` | `references/exemplar-learning-dossier.md`, `references/style-learning-workflow.md`, `references/deep-imitation-protocol.md`, `references/logic-transfer-audit.md`, `references/deep-reading.md`, `references/journal-style-analysis.md` |
| `motivation-model` | User wants high-quality academic writing driven by motivation | Draft + evidence sources + exemplar learning dossier + `confirmed_motivation.md` | `motivation_thread_model.md`, `motivation_surface_map.md` | `references/motivation-thread-writing.md` |
| `rewrite` | User wants actual manuscript revision | Draft + `confirmed_motivation.md` + `target_journal_research.md` + `exemplar_learning_dossier.md` + `original_logic_map.md` + `paragraph_function_templates.md` + `motivation_thread_model.md` + `motivation_surface_map.md` | `evidence_bank.md`, `section_blueprints.md`, `rewrite_matrix.md`, revised draft, `revision_audit.md`, `logic_transfer_audit.md` | `references/deep-imitation-protocol.md`, `references/rewrite-matrix.md`, `references/motivation-thread-writing.md`, `references/logic-transfer-audit.md`, `references/round1-literature-revision.md`, `references/round2-journal-revision.md` |
| `latex` | User needs LaTeX conversion, template integration, compilation, or formatting repair | LaTeX project or target template | Clean `.tex`, compile report | `references/latex-source-control.md`, `references/round3-latex-polish.md`, `references/round4-template-integration.md` |
| `full-pipeline` | User explicitly asks for end-to-end paper improvement | Draft + target venue + exemplar papers + LaTeX/project files if applicable | All staged artifacts | All route references as needed |

If inputs are missing, ask only for the minimum blocker. For style imitation, prefer 3-6 local PDFs or extracted text files over broad web search. A small high-quality full-text corpus beats many shallow search results.

## Default Workflow

### 1. Intake and Source Map

Create `paper_rewriting_output/source_map.md` before major edits:

| Source | Path/URL | Role | Reliability | Notes |
|---|---|---|---|---|
| User draft | | user's claims/results | authoritative for this paper | |
| Reference paper | | style/structure only | do not borrow results | |
| Journal guideline | | formatting requirements | authoritative for format | |
| BibTeX | | citation keys | authoritative for keys | |

Also record:

- target venue,
- motivation status: user-confirmed, user-provided but needs confirmation, or absent,
- previous-version special requirements status,
- manuscript format: Word, Markdown, LaTeX, mixed,
- whether LaTeX already compiles,
- sections present/missing,
- figures/tables/bibliography paths,
- user priorities.

### 2. Confirm the Motivation

Create a confirmed motivation before any substantive paper writing, style imitation, or section blueprinting. The motivation is not a slogan; it is the paper's controlling reason for existing.

Use one of two paths:

**Path A: user provides the motivation.**

If the user gives a clear motivation and explicitly wants it used, save `paper_rewriting_output/confirmed_motivation.md`. If the motivation is broad, mixed, or tentative, restate it in 1-2 precise versions and ask the user to confirm before continuing.

**Path B: user does not provide the motivation.**

Infer 3-5 candidate motivations from the draft, target venue, figures, tables, and available evidence. Save them as `paper_rewriting_output/motivation_options.md`, then stop and ask the user to choose one, edit one, combine parts, or write their own.

`motivation_options.md` must include:

| Option | One-Sentence Motivation | Field Problem | Specific Gap | Design Response | Evidence Available | Fit To Target Venue | Main Risk | What This Choice Changes |
|---|---|---|---|---|---|---|---|---|

After the user confirms a choice, create `confirmed_motivation.md`:

| Field | Content |
|---|---|
| Source | user-provided / selected option / edited option |
| Confirmed motivation statement | |
| Red thread | |
| Prioritized claims | |
| Claims to avoid | |
| Section consequences | |

The confirmed motivation must decide what the Introduction builds toward, what Methods must justify, what Results must prove, and what Discussion must resolve. If two motivations compete, ask the user to choose the primary one and record the secondary one as a boundary, not a second spine.

Read `references/motivation-thread-writing.md` before creating candidate motivations or the confirmed motivation artifact.

For numbered versions such as V8, V9, or V10, also create `special_requirements.md` before rewriting. Read `references/version-requirements.md`. Requirements marked active must be inherited into the next version unless the user explicitly changes them.

### 3. Research the Target Venue Or Task Genre

If the user names a journal or conference, create `paper_rewriting_output/target_journal_research.md` before diagnosing or rewriting for that venue.

The file must include:

- official article type and length requirements,
- required section order and abstract headings,
- data/software availability requirements,
- AI-use disclosure requirements,
- figure/table expectations,
- 5-10 recent relevant papers from the venue,
- a judgement of whether the user's paper fits the venue and article type.

Use web search for current official requirements. Use recent venue papers as style examples, not as fact sources for the user's results. Read `references/target-journal-research.md`.

If the user names a paper-like task type beyond normal journal/conference writing, create `paper_rewriting_output/genre_research.md` before writing. Read `references/task-genre-research.md`. Learn the audience, evaluation criteria, required sections, exemplar move sequence, evidence conventions, and output constraints. Examples include modeling-contest papers, technical reports, thesis/proposal-style reports, review-style reports, white papers, and grant-like narratives. Do not force all of them into the journal-paper template.

### 4. Diagnose Before Rewriting

Extract the manuscript's current argument:

- one-sentence contribution,
- one-sentence red thread,
- section roles,
- major claims and their evidence,
- missing or weak links between Introduction, Methods, Results, and Discussion,
- numbers that need traceability.

Save the result as `paper_rewriting_output/paper_diagnosis.md`.

Then create `paper_rewriting_output/original_logic_map.md`. This is not a prose summary; it is the baseline argument map that later revisions must improve:

| Section | Current Paragraph/Unit | Current Rhetorical Job | Evidence Used | Logic Defect | Keep/Move/Delete/Rebuild |
|---|---|---|---|---|---|

The map must answer:

- what problem the current paper appears to solve,
- where the motivation chain breaks,
- which paragraphs report facts without explaining why they matter,
- which Results paragraphs only report metrics,
- which claims lack evidence or overstate the evidence,
- which LaTeX/formula/figure units should be preserved without prose imitation.

### 5. Learn Why Good Papers Work

When the task involves imitation, produce `exemplar_learning_dossier.md` before `style_profile.md`. The dossier must explain how the exemplar papers write, not just summarize what they studied.

For each exemplar and for each major section, identify:

- the motivation problem it constructs,
- the paragraph-level move sequence,
- how the final paragraph of the Introduction sets up Results,
- how Methods justifies design choices,
- how Results moves from metric reporting to interpretation,
- how Discussion resolves the original motivation and states limitations.

Then produce `style_profile.md`. It must contain:

- corpus list and why each paper was selected,
- section move sequence,
- section length/paragraph/sentence metrics,
- opening and closing patterns,
- claim strength rules,
- citation density and placement,
- terminology and collocation preferences,
- figure/table presentation conventions,
- sentence skeletons with slots,
- forbidden habits for this target style.

Use `scripts/style_metrics.py` on extracted text, Markdown, or LaTeX sources when possible:

```bash
python scripts/style_metrics.py <paper-or-folder> --markdown > style_metrics.md
```

Then interpret the metrics with `references/style-learning-workflow.md`. Do not rely on memory or vibes.

Also create two transfer artifacts before writing:

`paper_rewriting_output/paragraph_function_templates.md`

| Section | Paragraph Slot | Exemplar Move | Reader Question Answered | Required Inputs From Our Paper | Sentence-Level Pattern |
|---|---:|---|---|---|---|

`paper_rewriting_output/result_narrative_templates.md`

| Result Type | Setup Move | Evidence Move | Comparison Move | Interpretation Move | Transition Move | Claim-Strength Limit |
|---|---|---|---|---|---|---|

These files are the bridge from "we learned papers" to "we can write our paper." If they are generic enough to fit any topic, they are incomplete.

### 6. Build the Motivation Thread

Create `motivation_thread_model.md` from `confirmed_motivation.md`, not from general model preference:

| Element | Content | Evidence | Where It Must Appear |
|---|---|---|---|
| Field problem | | | Introduction P1-P2 |
| Specific gap | | | Introduction P3-P4 |
| Design response | | | Introduction, Methods |
| Main evidence | | | Results |
| Interpretation | | | Discussion |
| Limitation | | | Discussion |

The model must include the one-sentence red thread and the Introduction-to-Discussion resolution map. Read `references/motivation-thread-writing.md`.

Also create `motivation_surface_map.md` so the motivation appears in the manuscript's reader-visible layer:

| Surface Element | Current Wording | Motivation Role | Proposed Wording/Strategy | Venue Constraint | Status |
|---|---|---|---|---|---|
| Title/subtitle | | | | | |
| Abstract opening | | | | | |
| Abstract closing | | | | | |
| Introduction topic sentences | | | | | |
| Methods subsection headings/openings | | | | | |
| Results subsection headings/openings | | | | | |
| Figure/table callouts | | | | | |
| Discussion opening/closing | | | | | |

Use this map to decide where to state the motivation explicitly and where to express it through causal structure, contrast, section order, or reader-friendly headings. Avoid repetitive slogan-like wording.

### 7. Build Evidence and Section Blueprints

Before rewriting, create `evidence_bank.md`:

| Claim/Result | Source | Allowed Strength | Can Appear In | Notes |
|---|---|---|---|---|

For Results and Discussion, every claim must map to the user's draft, figures, tables, logs, or explicit notes. Exemplar papers can provide structure only.

Then create `section_blueprints.md`:

| Section | Motivation Job | Target Move Sequence | Heading/Surface Decision | Paragraph Plan | Corpus Pattern | Evidence Inputs | Required Deletions/Merges/Splits |
|---|---|---|---|---|---|---|---|

The blueprint must be written from the confirmed motivation, motivation surface map, style profile, paragraph-function templates, result-narrative templates, original logic map, and evidence bank. It must state how the new section logic differs from the original section logic and how each section advances the motivation. Do not build blueprints by lightly editing the original paragraphs.

### 8. Rewrite With a Matrix

Before changing prose, create `rewrite_matrix.md`:

| Section | Original Unit | Motivation Link | Action | Intended Move | Evidence Source | Model Pattern | Target Length | Logic Change | Rewrite Decision |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- One paragraph should usually perform one rhetorical move.
- One paragraph must also perform one motivation job: establish need, sharpen gap, justify design, test promise, interpret evidence, qualify limits, or close significance.
- Each rewritten paragraph must map to either a user-provided claim/result or a structural/style pattern from the corpus.
- Each rewritten paragraph must also map back to `original_logic_map.md` so the revision can show whether it rebuilt, moved, merged, deleted, or preserved the old logic.
- Subsection headings should name the logical job of the section in natural journal language. Use explicit motivation words only at strategic anchor points; otherwise let the opening sentence or transition carry the motivation.
- Every number in the rewritten text needs a source.
- Preserve the paper's scientific meaning unless the user explicitly asks for speculative restructuring.
- Use action labels: `REWRITE`, `SPLIT`, `MERGE`, `DELETE`, `MOVE`, `ADD`, or `KEEP`.
- `KEEP` is allowed only for technically dense text that already matches the style profile. Justify every `KEEP`.
- `ADD` cannot be the dominant action. If the plan mainly adds paragraphs after existing paragraphs, stop and rebuild the section.

Use `references/rewrite-matrix.md` for detailed paragraph-level procedure.

### 9. Rewrite From Blueprint, Not By Patching

For substantive revision, do not open the old paragraph and "improve it sentence by sentence." Use this order:

1. Read the original section and extract claims/evidence into notes.
2. Close the original section as prose source; keep only notes, citations, numbers, and figure references.
3. Write the target section from `section_blueprints.md`.
4. Reinsert required LaTeX commands, citations, labels, and figure/table references.
5. Run a shallow-edit audit:

```bash
python scripts/revision_audit.py <original-file> <revised-file> --markdown > paper_rewriting_output/revision_audit.md
```

If many paragraphs remain near-identical or most changes are additions, revise again.

### 10. Audit Logic Transfer

Before calling the manuscript improved, create `paper_rewriting_output/logic_transfer_audit.md`. Read `references/logic-transfer-audit.md`.

The audit must compare the original draft, the learning artifacts, and the revised manuscript:

| Section | Original Logic | Learned Target Logic | Revised Logic | Evidence of Transfer | Verdict |
|---|---|---|---|---|---|

It must answer, section by section:

- Did the Abstract now state the real motivation, gap, response, evidence, and significance?
- Did the Introduction change from background accumulation to necessity construction?
- Did Methods explain design rationale rather than only list components?
- Did each Results subsection test one promise from the Introduction?
- Did Discussion resolve the Introduction's motivation and state limitations?
- Which original paragraphs were merely polished rather than logically rebuilt, and why was that acceptable?

If the audit finds that the revision mostly changed wording, added sentences after old paragraphs, or preserved the old section logic, return to `section_blueprints.md` and rewrite again before LaTeX polishing.

### 11. Final LaTeX Execution Loop

If the draft is LaTeX, do a guard pass before content revision and a compile/guard pass after content revision:

```bash
python scripts/latex_guard.py path/to/main.tex --bib path/to/references.bib --markdown
```

Prefer editing prose inside the existing LaTeX project instead of converting Markdown back to LaTeX. Preserve:

- preamble,
- `\newcommand` and custom macros,
- labels,
- citation commands,
- figure/table floats,
- equations,
- bibliography commands.

Use `references/latex-source-control.md` for the LaTeX-safe workflow.

Only this stage should focus on the LaTeX project. Earlier stages may inspect `.tex` files for evidence, but the main work is learning and planning.

## Deep Reading Policy

Do not deep-read every paper by default. Use tiers:

| Tier | Count | Purpose | Output |
|---|---:|---|---|
| Quick scan | 5-15 | decide relevance and avoid bad exemplars | `literature_survey.md` |
| Style corpus | 3-6 | learn how excellent papers write | `style_profile.md` |
| Full deep reading | 1-3 | understand field logic and reusable moves | `deep_reading_3_papers.md` |

Read `references/deep-reading.md` only when full deep reading is needed. Read `references/journal-style-analysis.md` when the user targets a specific journal or conference.

## Revision Rounds

Use rounds as checkpoints, not bureaucracy.

| Round | Purpose | Output |
|---|---|---|
| R0 Diagnosis | understand current argument and risks | `paper_diagnosis.md` |
| R1 Structural Rewrite | improve motivation thread, move order, evidence placement | `revision_1_structure.md` |
| R2 Style Conformity | apply journal/exemplar style profile | `revision_2_style.md` |
| R3 Language Polish | native academic English without changing claims | `revision_3_polished.*` |
| R4 LaTeX Integration | compile, guard, verify content | `.tex`, PDF, `latex_report.md` |

For R1 details, read `references/round1-literature-revision.md`. For R2 details, read `references/round2-journal-revision.md`. For language and LaTeX details, read `references/round3-latex-polish.md` and `references/round4-template-integration.md`.

## Validation Gates

Before presenting a revised manuscript, produce short validation notes:

### Scientific Integrity

- confirmed motivation exists before substantive writing,
- every section blueprint and rewritten major section points back to the confirmed motivation,
- headings, subsection openings, topic sentences, and Discussion closure are aligned with `motivation_surface_map.md` without sounding forced,
- all numbers traced,
- no invented citations,
- no borrowed results from exemplar papers,
- speculative claims marked as author decisions.

### Style Fit

- style profile applied section by section,
- paragraph-function templates applied to every rewritten major section,
- Results narrative templates applied to every rewritten Results subsection,
- paragraph lengths and section proportions are close enough to corpus targets,
- claim strength matches the venue,
- terminology is consistent.

### Logic Transfer

- original logic map exists,
- revised section logic differs from the original where the original was weak,
- each major revised section names the learned target pattern it follows,
- each major revised section names the motivation job it performs,
- Introduction promises match Results tests,
- Discussion resolves the Introduction rather than repeating Results,
- shallow-edit audit and logic-transfer audit agree that changes are substantive.

### LaTeX Integrity

- `scripts/latex_guard.py` run if LaTeX exists,
- compile attempted when a TeX engine is available,
- unresolved citations/labels/figures listed,
- content not silently dropped.

## Output Directory

Create outputs under `paper_rewriting_output/` unless the user asks otherwise:

| File | Purpose |
|---|---|
| `source_map.md` | source roles and reliability |
| `special_requirements.md` | inherited and newly added version-level constraints that later versions must read first |
| `motivation_options.md` | candidate controlling motivations when the user has not provided one |
| `confirmed_motivation.md` | user-confirmed controlling motivation, red thread, claim boundaries, and section consequences |
| `target_journal_research.md` | official venue requirements and recent-paper style survey |
| `genre_research.md` | task audience, rubric/evaluation criteria, exemplar structure, evidence conventions, and writing strategy |
| `paper_diagnosis.md` | current manuscript diagnosis |
| `original_logic_map.md` | baseline map of current argument logic and defects |
| `exemplar_learning_dossier.md` | explanation of how good papers construct motivation and sections |
| `paragraph_function_templates.md` | learned paragraph jobs that will guide section drafting |
| `result_narrative_templates.md` | learned Results patterns for setup, evidence, interpretation, and transition |
| `style_metrics.md` | script-generated style measurements |
| `style_profile.md` | learned style rules |
| `motivation_thread_model.md` | controlling motivation and section resolution map |
| `motivation_surface_map.md` | motivation alignment for title/subtitle, headings, topic sentences, transitions, callouts, and closure |
| `evidence_bank.md` | allowed claims and numbers |
| `section_blueprints.md` | target move-level section plans |
| `rewrite_matrix.md` | paragraph-level rewrite plan |
| `revision_audit.md` | unchanged-paragraph and addition-heavy audit |
| `logic_transfer_audit.md` | logic-level comparison of original, learned target pattern, and revised manuscript |
| `latex_report.md` | LaTeX guard/compile notes |
| `research_report.md` | final trace of changes and remaining author tasks |

## Red Flags

Stop and verify when:

- a number has no source,
- a numbered version is being created and `special_requirements.md` from the prior version was not checked,
- the paper's controlling motivation has not been confirmed by the user,
- multiple motivations are being mixed without the user choosing a primary one,
- the Introduction, Results, and Discussion imply different motivations,
- subsection headings repeat the same motivation keyword so often that the structure feels forced,
- a paragraph cannot name its motivation job,
- Results subsection titles do not map to Introduction promises,
- the user named a target venue and `target_journal_research.md` is missing,
- the user named a non-journal paper-like task and `genre_research.md` is missing,
- the skill begins writing before `exemplar_learning_dossier.md` exists,
- the skill begins writing before `original_logic_map.md` exists,
- the skill begins writing before `paragraph_function_templates.md` exists,
- Results rewriting begins before `result_narrative_templates.md` exists,
- a rewrite uses a reference paper's result as if it were the user's result,
- the style profile has not been created but style imitation has begun,
- the evidence bank has not been created but Results/Discussion rewriting has begun,
- the section blueprint has not been created but prose editing has begun,
- a section is rewritten without a matrix row,
- a rewrite mostly preserves original paragraph order and adds sentences after them,
- a rewrite matrix contains mostly `KEEP` or `ADD`,
- `logic_transfer_audit.md` cannot explain how the revision changed the section's reasoning,
- the Results still report metrics without stating what Introduction promise each result tests,
- the Discussion does not explicitly close the main motivation thread,
- LaTeX commands are being rewritten during language polishing,
- compilation fixes are consuming more time than content quality work,
- the user's LaTeX project did not compile before revision.

When a red flag appears, report it and switch to the smallest corrective action.
