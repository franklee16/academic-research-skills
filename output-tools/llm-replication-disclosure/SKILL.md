---
name: llm-replication-disclosure
description: >-
  Replication-package assembly and disclosure checklist for research that uses
  LLM-generated data, measures, or code, based on Table A.3 and Sections
  3.3.2-3.3.3 of Ferrara (2026, NBER WP 35374). Use this skill whenever the
  user is preparing a replication package, responding to a journal data
  editor, writing a generative-AI disclosure statement, drafting the methods
  or appendix section describing LLM use, submitting or revising a paper that
  used any LLM anywhere in the pipeline, or asks "what do I need to report /
  archive / disclose" about AI-assisted work. Also trigger proactively at the
  END of any project where Claude helped build an LLM pipeline — packaging
  requirements are cheapest to satisfy during the work, not after — and
  whenever the user mentions journal submission, data editors, replication
  files, ICPSR/openICPSR/Zenodo deposits, or reproducibility of model output.
---

# Replication Packages and Disclosure for LLM-Assisted Research

This skill codifies what must go into the paper, the appendix, and the
replication package when a study relies on LLM-generated data, measures, or
code. Source: Ferrara (2026), NBER WP 35374, Table A.3 and Sections
3.3.2–3.3.3, generalized to empirical economics and finance.

**The governing principle:** a reader should be able to see exactly what the
model was asked, what it answered, and how well it performed — *even though
rerunning the model is not guaranteed to reproduce the outputs.* LLM work has
two reproducibility problems conventional empirical work does not, and the
whole checklist is built around compensating for them:

1. **Run-to-run nondeterminism.** Temperature 0 is not a random seed. Hosted
   inference batches requests across users, and floating-point arithmetic is
   not associative — summation order can flip a token, and one flipped token
   diverges the rest. Even APIs exposing a seed parameter cannot control
   server-side batching. Outputs get *close to* reproducible, never fully.
2. **Model deprecation and silent drift.** The model behind an API name can
   be retrained or retired without notice. A pinned, dated identifier (e.g.,
   a versioned model string) survives only until the vendor retires it.

The compensating strategy is therefore **archive-first**: since the model
call cannot be guaranteed to rerun identically, archive everything the call
consumed and produced, so every *downstream* number is mechanically
replicable from the archive alone.

Relationship to other skills: `llm-research-workflow` governs the development
loop that *produces* the pipeline; this skill governs what survives into the
paper and the package. If that skill's logging defaults were followed
(raw outputs, versions, token counts logged from day one), assembly here is
mostly collation. `plan-verify-act` applies to the mechanics of assembling
and verifying the package itself.

---

## Three modes of use

Identify which the user needs and say so; they have different outputs.

**Mode 1 — Audit.** The user has an existing project. Walk the checklist
below against what actually exists on disk and produce a **gap report**:
each item marked present / absent / partially present, with severity.
Severity tiers: *fatal* (archived raw model outputs missing — downstream
results cannot be verified), *major* (no held-out validation accuracy; no
pinned model version; prompts not preserved in final form), *minor*
(README gaps, missing runtime notes). Never paper over a fatal gap; if raw
outputs were not logged, the honest remedies are re-running the pipeline
with logging on (results may shift — that shift is itself reportable) or
disclosing the limitation explicitly.

**Mode 2 — Draft disclosure text.** Generate the paper-facing text: the
methods/appendix paragraph, figure/table notes, and the journal disclosure
statement. Templates are in `references/templates.md` — read that file
before drafting. Two hard rules: (a) **never fabricate or guess settings
the user did not record** — if the temperature, version string, or access
date is unknown, ask, and if genuinely unrecoverable, the disclosure must
say so rather than assert a plausible value; (b) check the **target
journal's current generative-AI policy by web search** before finalizing —
these policies are in flux across AEA journals, JF/JFE/RFS, Management
Science, and data-editor guidance, and training-data knowledge of them
should be presumed stale.

**Mode 3 — Assemble the package.** Build the directory structure, README,
and manifests from the project's existing files. Structure and README
skeleton are in `references/templates.md`. Ask before moving or rewriting
any of the user's existing files; stage a copy rather than reorganizing
originals in place.

---

## The checklist (Table A.3, generalized)

Work through all five panels. Items marked ★ are the ones data editors and
referees most commonly find missing.

### Panel 1 — Paper and appendix

- ★ Exact model identifier(s) — the full versioned string, not the family
  name ("the model" or even "GPT-4o" is insufficient; the dated version
  string is the unit of reproducibility) — and date(s) of access.
- Settings that affect output: temperature, top-p, max output tokens, seed
  (if used), reasoning/thinking mode on or off, and the output format
  (JSON schema, forced choice, free text).
- ★ Validation reporting: sample size, who hand-coded it and how (number of
  coders, instructions, inter-coder agreement), and accuracy on the
  **held-out** portion — never on items used to select prompts or models.
  Precision and recall, not raw accuracy, for rare categories.
- How sensitive/licensed data were handled: the route that made
  transmission permissible (enterprise zero-data-retention contract,
  self-hosted open-weight model, or public data). For finance data this
  means naming the treatment of WRDS/CRSP/Compustat, CSMAR, I/B/E/S,
  exchange, or vendor-licensed text under their DUAs.
- Which parts of the analysis and code were LLM-assisted, at the
  granularity the target journal's policy requires.

### Panel 2 — Prompts

- ★ Full text of every prompt **in its final form**: system prompts,
  classification rubrics (including the "uncertain / none of the above"
  category), few-shot examples, and any domain-vocabulary lists.
- Prompt variants used for robustness checks, clearly mapped to which
  robustness table they produced.
- The project log / AGENTS.md if one coordinated the work — it documents
  decisions that never made it into code.

### Panel 3 — Code

- Pre-processing code: corpus restriction, keyword/fuzzy pre-screens,
  snippet windows, stop-word removal — every step between raw source and
  what the model actually saw. (Reviewers reconstruct measures from here;
  an undocumented pre-screen is an undocumented sample-selection rule.)
- API-call or batch-submission scripts, including the parser that turns raw
  responses into the analysis dataset.
- Analysis code from LLM-generated measure to every table and figure.
- Software environment: language and package versions (requirements file),
  hardware notes where relevant (GPU use, local model serving stack).
- ★ README with execution order, approximate runtimes and API costs, and an
  explicit mapping from scripts and output files to the paper's tables and
  figures.

### Panel 4 — Data and model outputs

- ★★ **The archived raw model outputs for every call used in the paper.**
  This is the single most important item in the package. Reruns are not
  guaranteed to reproduce them; the archive is what makes every downstream
  result mechanically replicable.
- The hand-coded validation data together with the coding instructions
  given to the coders.
- The final analysis datasets built from the raw outputs.
- For restricted source data: access instructions in place of the data.
  **Never include licensed material in the package** — including it is a
  DUA violation dressed up as transparency.
- For fine-tuned or self-hosted models: the weights or a durable pointer to
  the archived version (e.g., a model-hub identifier with revision hash),
  plus the fine-tuning data and code where licensing allows.

### Panel 5 — Final check

- A reader **without access to the model vendor** can reproduce every number
  in the paper from the archived files alone. This is the acceptance test
  for the whole package; run it mentally file by file, or better, actually
  re-execute the downstream chain from archived outputs in a clean
  environment.
- A note states which steps cannot be rerun exactly (model nondeterminism,
  deprecation) and what is archived to compensate. Data editors currently
  tolerate this residual as an acknowledged imperfection — but only when it
  is acknowledged.

---

## Behavioral rules when this skill is active

1. **Archive-first triage.** In Mode 1, check Panel 4's raw-output item
   before anything else; its absence changes the advice for every other
   panel.
2. **No invented metadata.** Version strings, dates, temperatures, and
   accuracy figures come from the user's records or from re-derivation —
   never from plausible-sounding defaults. A disclosure statement with a
   guessed setting is worse than one with an honest gap.
3. **Search the target journal's current AI policy** before finalizing any
   disclosure text; do not rely on remembered policy.
4. **Ask before reorganizing.** Package assembly touches the user's project
   files; propose the structure, get confirmation, then stage copies.
5. **Timing nudge.** If this skill triggers mid-project rather than at
   submission, say so explicitly: turning on raw-response logging and
   version pinning *now* costs nothing; reconstructing them later may be
   impossible. Cross-reference `llm-research-workflow` step 4 defaults.

## Worked micro-example (finance flavor)

User: "My paper scoring 10-K risk-factor novelty with an LLM got an R&R at
a top journal; the data editor wants the replication package."

- Mode 1 audit first. Findings: raw responses were logged (✓, fatal risk
  cleared); model string recorded but access dates missing (major — recover
  from API billing logs); validation sample exists but the same 150 items
  were used to pick the prompt and report accuracy (major — hold-out
  violation; remedy: hand-code a fresh 50-item held-out slice and report
  that figure, disclosing the change).
- Mode 3: stage `package/` with `prompts/`, `code/{preprocess,api,analysis}`,
  `raw_outputs/`, `validation/`, `data_access.md` (EDGAR is public — include;
  the licensed analyst-report robustness corpus — access instructions only),
  README with script→table mapping and the ~$740 batch-API cost note.
- Mode 2: draft the appendix paragraph and the journal's AI-disclosure form
  after searching the journal's current policy; the nondeterminism note
  states that reruns may differ and that archived outputs reproduce all
  reported numbers exactly.
