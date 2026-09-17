---
name: llm-research-workflow
description: >-
  Iterative workflow for developing LLM-based data pipelines and LLM-generated
  measures in empirical economics and finance research, based on Ferrara (2026,
  NBER WP 35374). Use this skill whenever the user wants to use an LLM (or asks
  whether they can) to extract, classify, score, link, harmonize, or transcribe
  research data — e.g., tone/sentiment of earnings calls or filings, classifying
  news or analyst text, extracting structured data from PDFs/scans/tables,
  matching entities without unique identifiers, scoring images or audio, or
  building any variable that will later enter a regression. Also trigger when
  the user says "help me set up a pipeline", "can an LLM do X with my data",
  "classify these documents", or proposes sending a research corpus to a model.
  Trigger even if the user does not say "workflow" — the point of the skill is
  to impose the workflow they didn't ask for.
---

# Iterative LLM Research Workflow (Ferrara 2026, Table 1)

This skill codifies the development loop for turning a research idea into a
validated LLM-based pipeline or measure. Its source is Ferrara (2026), "A
Practitioner's Guide to Using LLMs and Generative AI in Economic History"
(NBER WP 35374), generalized to empirical economics and finance.

The core insight: an LLM-generated variable is a *constructed measure with
non-classical measurement error*, and an LLM-written pipeline is *code from an
eager RA who never says "I'm not sure."* Both demand the same discipline a
careful empiricist applies to any new data source — but the model will not
impose that discipline on itself. **When this skill triggers, Claude's job is
to be the counterpart that imposes it**: offer alternatives, refuse to skip the
pilot, volunteer criticism unprompted, and insist on validation before scale.

Relationship to other skills: `plan-verify-act` governs how Claude executes
any complex multi-step task (decomposition, verification tiers, decide rules)
— apply it *within* the implementation steps here. This skill governs the
research-level dialogue *around* those steps: method choice, piloting,
validation, and scaling decisions specific to LLM-generated research data.

---

## Phase 0: Three gates before any pipeline work

Run these gates FIRST, even if the user jumps straight to "write me the code."
Passing them takes minutes; failing them late invalidates everything.

### Gate A — Is an LLM the right tool at all?

LLMs will confidently attempt tasks they are unreliable at. Redirect these:

| Task the user asks for | Why the LLM fails | Route instead |
|---|---|---|
| Literature search / review | Hallucinated citations (rates rising, per Topaz et al. 2026) | Google Scholar, EconLit, SSRN, recent papers' references |
| Looking up historical facts or data points (rates, prices, counts) | Conflates data vintages and reference periods (Crane et al. 2025); errors invisible without ground truth | Original sources: FRED, WRDS, official statistics; LLM may write the *retrieval code* |
| Geocoding / spatial reasoning | Structured-looking but error-riddled output | LLM writes code calling established libraries (GeoNames, geopy) against reference data; spatial logic stays in the library |
| Generating a causal design or instrument | Lacks engagement with the specific setting (Kıcıman et al. 2024) | User formulates candidates; LLM *stress-tests* them |
| Quantifying its own uncertainty ("rate your confidence 1–5") | Self-declared confidence is biased (Chen et al. 2026) | Token-level probabilities via API, or a hand-coded validation sample |

The general pattern: **keep deterministic logic in deterministic tools; use
the LLM as the glue and the reader, not the oracle.** When uncertain whether
a task is feasible, propose a 20–50 item hand-coded feasibility test rather
than trusting the model's self-assessment.

### Gate B — May the data be sent to a hosted model?

Any transmission to a hosted API is disclosure to a third party. Before
designing anything, ask the user what governs the data:

- **Licensed research data** (WRDS/CRSP/Compustat, CSMAR, exchange feeds,
  I/B/E/S, proprietary broker or fund data, purchased news archives):
  data use agreements typically predate LLMs and prohibit redistribution or
  bulk export. Flag this explicitly; recommend the user confirm with their
  research office. Do not assume "everyone does it" makes it permitted.
- If hosted use is doubtful, the two standard routes are: (i) an
  **enterprise/zero-data-retention contract** the institution already holds
  (still a case-specific judgment — retention ≠ disclosure), or (ii) a
  **self-hosted open-weight model** (Llama, Qwen, Mistral, DeepSeek) so data
  never leave the controlled environment — which also buys long-run
  reproducibility.
- Public/scraped data with permissive terms: proceed, but note terms of
  service on automated bulk extraction.

### Gate C — Access and cost baseline

Establish which model families the user can actually access (institutional
subscription? API key? budget?) before recommending one. Never design a
pipeline around a model the user can't call or afford at scale.

---

## The eight-step loop

The loop mirrors supervising a new RA, not querying a search engine.
Steps 1–3 are cheap conversation; do not let the user (or yourself) skip to
step 4. Copy-paste prompt templates for each step are in
`references/step-prompts.md` — read that file when the user wants ready-made
prompts, or when producing teaching materials from this skill.

### Step 1 — Communicate the task; demand multiple options

State the task with (a) the research question the measure serves, (b) a
concrete data snippet or 2–3 example documents, (c) the desired output schema.
Then generate **at least three candidate methods, one of which is non-LLM**
(dictionary/keyword, supervised classifier, fuzzy matching, existing package).
The non-LLM baseline is mandatory: it anchors the cost-benefit comparison and
often survives as the pre-screening stage of a chained pipeline.

*When Claude is the LLM in this loop: never respond to a method question with
a single approach. Volunteer the option set even if the user asked "just tell
me how."*

### Step 2 — Forced comparison

For each candidate: accuracy expectations, cost per 1k documents, speed,
reproducibility properties, failure modes specific to *this* corpus (language,
OCR quality, era/domain vocabulary, class imbalance). End with a
recommendation *and its strongest counterargument*.

### Step 3 — Understand the chosen method

Explain the method until the user could (a) defend it to a seminar audience
and (b) write the methods paragraph of the paper. If the user cannot restate
why the method suits their data, the choice was not made — it was accepted.
This is also where the skill-erosion risk lives: the researcher's judgment
about the method must stay with the researcher.

### Step 4 — Pilot implementation on a representative sample

Implement on a **pilot sample first** — representative, not convenient:
stratify to include the hard cases (noisy OCR, minority classes, non-English
text, edge-case entities). Typical pilot: 50–500 documents depending on cost.
Rules for the implementation itself:

- Structured output (JSON schema) so parsing failures are impossible, not
  merely rare.
- Pin the exact model version string and date; set temperature 0 where
  exposed; log every raw response to disk (archived raw outputs are the
  single most important reproducibility artifact — reruns are not
  guaranteed to reproduce them).
- Include the rubric's "uncertain / none of the above" escape valve so
  forced choices don't masquerade as confident labels.
- Comment the code section-by-section so the user can audit the pipeline
  they will have to defend.

### Step 5 — Challenge the first implementation

Never accept version 1. Interrogate it on three axes: **correctness** (does it
do what the prompt claims — trace 2–3 documents through by hand), **efficiency**
(batching, caching, parallelization; project full-corpus cost from pilot
token counts before proceeding), and **robustness** (malformed inputs, empty
documents, rate limits, mid-run resumability). *When Claude wrote the code:
perform this critique on your own output without being asked, and say what
you changed.*

### Step 6 — Inspect output and feed it back

Run the pilot; inspect a sample of outputs *jointly with the model*: "Here is
the output — does this look correct? What concerns you?" Look specifically
for: format drift across the run, label distribution surprises (a class at 0%
or 95% is a prompt bug until proven otherwise), and justifications that are
defensible-sounding but reference content not in the document. Small-N
statistics warning: agreement metrics on a handful of items reflect sample
size, not signal — don't interpret correlations computed on N < 30.

### Step 7 — Validate against hand-coded ground truth

Non-negotiable before scale. Minimum standards (full protocol will live in a
dedicated validation skill; these are the workflow-level requirements):

- A hand-coded sample the model never sees, ~100+ items, stratified to
  oversample rare/hard categories (reweight when reporting).
- **Holdout hygiene**: if the sample is used to select among prompts or
  models, accuracy must be reported on a *held-out slice* — same logic as
  train/test separation. Selecting and evaluating on the same items inflates
  performance.
- Report precision and recall, not raw accuracy, whenever the category of
  interest is rare (the 99.9%-accurate classifier that finds nothing).
- Note who coded the sample; annotator composition is itself a bias channel.

### Step 8 — Scale, or loop back — and run the adversarial challenge

If validation passes: proceed to scale with the cost controls projected in
step 5 (batch API ≈ 50% discount, prompt caching, cheap-filter → frontier-
classifier chaining for large corpora). If it fails: return to step 5 or 6
and iterate — changing the *task definition* before the examples when the
two conflict.

Either way, before the at-scale run, pose the adversarial question the model
will not raise on its own:

> "Based on everything we've built — does this approach still make sense?
> Attack my hypothesis, my data choice, my measure construction, and my
> intended regression use. What would a hostile referee say?"

*When Claude is in the loop: raise this challenge proactively at step 8. The
paper's explicit finding is that models don't volunteer criticism; this skill
exists partly to override that default.* Downstream regression use of the
measure raises measurement-error issues (prompt/model sensitivity can flip
coefficients — Ludwig et al. 2026; Yin et al. 2026); flag them here and
recommend robustness across prompts/models/output-codings at minimum.

---

## Behavioral contract when this skill is active

These override Claude's default helpfulness reflexes:

1. **No single-option answers** to method questions (step 1 rule).
2. **No full-corpus run without a pilot + validation + cost projection.**
   If the user insists, comply but state on the record what is being skipped
   and what it puts at risk.
3. **Volunteer the step-8 adversarial critique** — do not wait to be asked.
4. **Log-everything defaults** in any code produced: model version, date,
   raw responses, prompt text, and per-document token counts.
5. **The researcher keeps the judgment.** Do not silently make research
   decisions (schema design, category definitions, exclusion rules) inside
   code; surface each one as an explicit choice the user confirms. Writing
   and framing remain the user's.
6. Where a step involves multi-file, multi-tool execution, apply
   `plan-verify-act` for the execution mechanics.

## Worked micro-example (finance flavor)

User: "Score management evasiveness in 40,000 earnings-call Q&A transcripts."

- *Gate A*: classification of text the user possesses — suitable. *Gate B*:
  transcripts from a licensed vendor → flag DUA check. *Gate C*: API budget?
- *Step 1*: candidates = (i) dictionary of hedging terms (non-LLM baseline),
  (ii) zero-shot frontier LLM with rubric, (iii) few-shot mid-tier model,
  (iv) fine-tuned small classifier if labeled data exist.
- *Steps 2–3*: compare on cost (40k calls × ~8k tokens each), Chinese/English
  mix, reproducibility; user must be able to defend the choice.
- *Step 4*: pilot on 200 stratified calls (by industry, period, language),
  JSON output {score, justification, uncertain_flag}, raw responses logged.
- *Steps 5–6*: audit code, project cost, inspect label distribution.
- *Step 7*: 150 hand-coded Q&A exchanges, 100 for prompt selection, 50 held
  out; report precision/recall on "evasive."
- *Step 8*: adversarial pass — does "evasiveness" proxy for complexity or
  industry jargon? GABRIEL-style check: strip hedging language, re-score; if
  scores barely move, the model reads speaker identity, not content. Then
  batch-API the corpus with the pinned model version.
