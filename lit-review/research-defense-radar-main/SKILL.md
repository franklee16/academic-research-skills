---
name: research-defense-radar
description: Assess and monitor an ongoing research project's competitor landscape, novelty risk, and method/data opportunities from a proposal, paper, research question, data or method notes, or a suspected competing paper. Use for baseline competitor scans, paper-versus-project novelty comparisons, revision rescans, and recurring scholarly monitoring. Do not use for standalone paper summaries, narrative literature reviews, citation formatting, bibliography cleanup, or citation verification unless they are part of a project-specific novelty assessment.
license: MIT
compatibility: Requires web search and page retrieval for current literature verification. Scheduled-task support and durable writable storage are optional but required for unattended longitudinal monitoring.
---

# Research Defense Radar / 研究防御雷达

Build a decision-oriented map of literature that can pre-empt, narrow, support, falsify, or improve a research project. Treat the project—not a keyword list—as the unit of analysis.

Reply in the user's language. Preserve authoritative paper titles in their original language. If you provide a translated title, label it as an assistant translation rather than an official title. For a Chinese operating summary, read `SKILL.zh-CN.md`; this file remains authoritative if the two differ.

## Select one operating mode

Choose the smallest mode that answers the request:

1. **Known-paper comparison** — compare one or more supplied papers with the project. Do not run a full baseline unless the user asks or the comparison exposes a material gap.
2. **Baseline competitor map** — establish the first research fingerprint, search broadly, and produce a provisional novelty assessment.
3. **Project-revision refresh** — diff a revised project against its prior fingerprint, re-score known papers, and search only newly relevant threat surfaces before broadening.
4. **Incremental monitor** — use durable prior state and report only new or materially changed literature.
5. **Method/data discovery** — prioritize transferable measurement, data, identification, estimation, validation, and implementation practices; substantive-topic overlap is optional.

If a vague input leaves multiple materially different interpretations, ask only the questions that would change the search. Otherwise proceed with a partial fingerprint and label assumptions.

When the user supplies a full working-paper draft, distinguish access to the manuscript from public disclosure. If no stable public record establishes when the user's project or a comparison WP first became publicly accessible, ask for that earliest public date. Do not infer it from PDF metadata, a file-modification timestamp, a date printed inside a private draft, or private circulation.

## 1. Resolve inputs and state

Accept research questions, proposals, LaTeX, PDF, Word, slides, code, specifications, data dictionaries, referee responses, and chat notes. Read enough of the actual material to recover framing, data, methods, and claimed contributions.

Separate each fingerprint statement by provenance:

- **user-stated** — explicitly supplied by the user;
- **source-extracted** — directly supported by the project files;
- **agent-inferred** — a provisional interpretation that needs confirmation.

For local/project-backed work, copy `assets/RESEARCH_PROFILE_TEMPLATE.md` and `assets/RADAR_STATE_TEMPLATE.json` into a user-controlled project directory such as:

```text
research-radar/<project-slug>/
├── fingerprint.md
├── radar-state.json
├── observations.json
├── coverage.json
├── search-log.jsonl
└── alerts/
```

Never write project data into this installed skill directory. Skill upgrades may replace it, and private research material does not belong in a distributable package.

For web/cloud runs without a durable folder, use one of these patterns:

- schedule inside the ongoing research chat so prior context remains available;
- attach the fingerprint and state to an accessible project/task;
- store them in an explicitly authorized connected service; or
- embed a compact fingerprint plus known-paper registry in the scheduled prompt when the state is small.

If prior state is unavailable, run a fresh baseline and say so. Never call an item "new since last run" without readable prior state.

## 2. Build or update the research fingerprint

Use `assets/RESEARCH_PROFILE_TEMPLATE.md`. Capture:

- core research question and main claim;
- mechanisms and falsifiable predictions;
- population, setting, unit, geography, and period;
- data sources, granularity, linkage, and access constraints;
- key constructs, measures, and validation risks;
- identification and identifying assumptions;
- estimation, theory, simulation, ML/LLM, or data-engineering methods;
- primary and secondary contributions;
- known nearest papers and the user's current novelty claim;
- earliest public working-paper date, its stable record or user-stated provenance, and whether the project is not yet public;
- threat surfaces: combinations that would materially reduce novelty;
- search vocabulary and privacy-safe public query terms.

The default rubric is strongest for empirical economics, finance, management, and adjacent quantitative social science. For theory, experiments, computer science, life sciences, qualitative research, or humanities, read `references/DOMAIN_ADAPTATION.md` and mark inapplicable fields `NA` instead of forcing an empirical template.

## 3. Search current literature

Before any novelty judgment, read `references/SEARCH_PLAYBOOK.md` and execute the relevant query families. Search the contribution space separately by question, mechanism, data/setting, measurement, identification, method, outcome, known-paper citation neighborhood, authors, and dangerous combinations.

Use multiple independent source families appropriate to the field. Treat working papers, preprints, job-market papers, conference drafts, accepted/forthcoming work, and online-first publications as potentially priority-relevant.

For each search run, record:

- search date and literature cutoff date;
- query family and privacy-safe query;
- source or index checked;
- coverage status: completed, partial, inaccessible, or not applicable;
- material access limitations and likely blind spots.

Do not paste confidential proposal passages, proprietary dataset names, or unpublished hypotheses into public search. Generalize them to the minimum conceptual query needed. If generalization would destroy the search value, show the proposed public query to the user before sending it.

## 4. Verify and deduplicate

Do not infer a paper's contribution from its title. Assign an evidence level:

- **M — Metadata only:** identity/status only; insufficient for substantive overlap claims.
- **A — Abstract verified:** supports a provisional description and overlap assessment.
- **F — Full text or detailed manuscript verified:** supports method, identification, mechanism, and contribution comparisons.

Every priority item needs a stable URL or DOI, evidence level, verification date, earliest public date and its provenance when available, current version/status, and confidence level. If the WP content is available but its public date is not, ask the user rather than treating the manuscript date as public chronology.

Track a paper lineage rather than counting NBER, SSRN, arXiv, conference, author-page, and journal versions as separate papers. Prefer DOI, then repository ID, then canonical URL, then normalized title plus author overlap. Note changed claims, samples, data, or methods across versions.

If local state is available, read `references/STATE_SCHEMA.md`, copy the observation and coverage templates, and use `scripts/update_radar_state.py` to merge verified observations deterministically. Read its `--help` output before use and prefer `--dry-run` before an in-place update.

## 5. Apply the public-working-paper priority cutoff

If the user's own WP is already public and its earliest public date is verified or user-stated, use that date as the priority cutoff:

- literature public **before** the project WP can pre-empt or narrow its public-time novelty and requires differentiation analysis;
- literature public **after** the project WP is post-disclosure convergence: it may matter for citation, monitoring, or method/data learning, but it does not negate the project's novelty at disclosure and does not, by default, require a new distinction;
- same-day or unknown timing remains uncertain until better chronology evidence is available.

Keep the public-time novelty verdict separate from the current literature landscape. If the project is not yet public, or its public date is unknown, do not apply this protection.

## 6. Classify relevance

Choose one primary class and optional secondary tags:

- **A — Direct competitor:** occupies substantially the same contribution space.
- **B — Potential threat:** pre-empts or narrows a novelty, mechanism, data, measurement, or design claim.
- **C — Method/data lift:** offers a transferable research step.
- **D — Supporting/positioning:** strengthens motivation, theory, interpretation, or external validity.
- **E — Contradictory/falsification evidence:** challenges a maintained assumption, expected sign, or mechanism.

Class A is not a mechanical keyword threshold. A paper may be a direct competitor with different data or methods if it makes substantially the same primary contribution. Conversely, shared keywords do not make a paper a threat.

## 7. Score overlap without false precision

Read `references/OUTPUT_SCHEMA.md`. Default empirical weights sum to 100:

- question 20;
- mechanism 15;
- data/setting 10;
- unit 10;
- measurement 10;
- identification 15;
- method/model 5;
- outcome 5;
- contribution claim 10.

Score each applicable dimension with anchored factors:

- 0 = none;
- 0.25 = weak;
- 0.50 = partial;
- 0.75 = strong;
- 1.00 = near-identical;
- NA = insufficient evidence or not applicable.

Calculate `sum(weight × factor)` and state any reweighting. Do not convert NA to zero. If critical fields are unknown, report a range or withhold the total and lower confidence.

Metadata-only evidence (`M`) cannot support a numeric overlap score. An abstract (`A`) can score only the dimensions the abstract actually establishes; leave the rest `NA`.

Report **threat/help level** separately from overlap:

- high — changes the primary contribution or a core design decision;
- medium — narrows a secondary contribution or requires a material robustness/repositioning step;
- low — useful context or a monitor-only item.

## 8. Explain decision impact

For every A/B/C/E priority item, state:

1. what the evidence actually establishes;
2. which fingerprint fields overlap;
3. what changes for the project;
4. one concrete researcher action;
5. what remains uncertain.

Recommended actions must respect the user's data, access, ethical, time, and design constraints. Label aspirational ideas that require unavailable data.

## 9. Produce the report

Follow `references/OUTPUT_SCHEMA.md`. Lead with the primary contribution at risk, not a bibliography. Include:

- compact fingerprint and provenance;
- executive verdict with coverage limits;
- 3–10 priority papers ranked by decision relevance;
- competitor/threat matrix;
- provisional novelty delta;
- priority chronology showing pre-disclosure, same-day/unknown, and post-disclosure work separately when the project WP is public;
- method/data opportunities;
- 1–5 actions to take now;
- search coverage and audit trail;
- broader reading appendix only when useful.

Use these novelty labels:

- **No close prior identified — provisional**;
- **Narrow but defensible**;
- **Substantially pre-empted**;
- **Uncertain / insufficient coverage**.

Never label a claim "safe." Never claim "first" or "no one has studied this" from a search result. Use bounded language such as: "No close prior was identified as of DATE within the sources and queries listed below."

Do not downgrade a public-time novelty label because of a paper first made public after the user's verified WP cutoff. Label it `post-disclosure convergence` and keep it outside the differentiation requirement unless the user explicitly asks for current-market positioning.

## 10. Create monitoring only after a successful manual run

After a reviewed baseline or historical calibration run, offer recurring monitoring. Do not silently create a scheduled task.

Default proposal when the user gives no schedule: Monday at 09:00 in the user's local timezone. Use the platform-specific prompt in `references/AUTOMATION.md` and explicitly invoke this skill instead of relying on automatic matching.

The scheduled task must identify:

- timezone and cadence;
- mode and project/fingerprint identity;
- durable state location or same-chat context;
- source scope and privacy-safe query policy;
- what counts as a material change;
- behavior when state, web access, or a source is unavailable;
- delivery language and destination.

Review the first few scheduled runs. Update an existing monitor after a project revision instead of creating an overlapping second monitor, unless the user explicitly wants separate monitoring.

## 11. Incremental-run rules

For each run:

1. Load the current fingerprint and prior registry.
2. Search recent work plus a small evergreen backfill.
3. Check known competitors for substantive revisions.
4. Verify and merge lineages.
5. Compare against prior state.
6. Report only new or materially changed A/B/C/E items and exceptional D items.
7. Persist the run record even when there is no material alert; advance the successful-scan clock only when required coverage completed.

If all required source families completed and nothing material changed, return the platform's quiet/no-change result. If coverage degraded, report the coverage failure rather than "nothing found."

## Gotchas

- A missing prior registry turns an incremental scan into a new baseline.
- An inaccessible abstract supports identity/status, not a substantive novelty judgment.
- Publication date, online-first date, revision date, and earliest public working-paper date are different clocks.
- A full WP manuscript proves content access, not public availability; ask for the earliest public date when no stable record verifies it.
- A post-disclosure paper can converge strongly with the project but cannot pre-empt the project's public-time priority.
- A high overlap score can still be helpful rather than threatening; explain contribution impact.
- A direct competitor can use different terminology; citation neighborhoods and author pages matter.
- Installing a skill does not create a schedule or grant web/storage permissions.
- A local path is useless to a web/cloud schedule unless that surface can access the same project or connector.
- Quiet alerts require completed coverage, not merely zero search results.

## Bundled resources

- `SKILL.zh-CN.md` — Chinese operating summary.
- `assets/RESEARCH_PROFILE_TEMPLATE.md` — fingerprint template to copy into user storage.
- `assets/RADAR_STATE_TEMPLATE.json` — durable registry template to copy into user storage.
- `assets/OBSERVATION_TEMPLATE.json` — verified paper-observation template.
- `assets/COVERAGE_TEMPLATE.json` and `assets/SEARCH_LOG_TEMPLATE.jsonl` — coverage and query-audit templates.
- `references/SEARCH_PLAYBOOK.md` — queries, sources, coverage, and stopping rules.
- `references/OUTPUT_SCHEMA.md` — evidence, scoring, report, and alert schemas.
- `references/DOMAIN_ADAPTATION.md` — non-default field adaptations.
- `references/STATE_SCHEMA.md` — state clocks, WP priority cutoff, lineage, migration, and merge protocol.
- `references/AUTOMATION.md` — cross-platform scheduling guidance and prompts.
- `references/INSTALL.md` — ChatGPT/Codex and Claude installation paths.
- `scripts/update_radar_state.py` — standard-library state validation and deterministic merge.
