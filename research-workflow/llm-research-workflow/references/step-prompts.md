# Copy-Paste Prompt Templates for Each Workflow Step

These templates operationalize Ferrara (2026, Table 1) for empirical
economics and finance. They are written to be handed to any frontier LLM
(chat, agentic, or API system prompt) and are suitable for direct reuse in
teaching materials. Replace bracketed fields; delete inapplicable lines.

Read this file when the user asks for ready-made prompts, when producing
course handouts from the skill, or when Claude itself needs precise wording
for a step it is executing on the user's behalf.

---

## Step 1 — Task communication + option elicitation

```
I am an empirical researcher in [finance/economics]. I want to [extract /
classify / score / link / transcribe] the following from [data source]:
[precise definition of the target construct].

Research context: the resulting variable will be used to [research question /
regression role: outcome, treatment, control].

Here are [2-3] representative examples of the raw data:
[paste snippets — include at least one hard/ambiguous case]

Desired output: [schema, e.g., one row per document with fields X, Y, Z].
Corpus size: [N documents, approximate tokens each].
Constraints: [budget, language(s), data-sensitivity restrictions, deadline].

Propose at least four candidate methods for this task, including at least
one that does NOT use an LLM (e.g., dictionary, supervised classifier,
fuzzy matching, existing package). Do not recommend one yet — just lay out
the option set.
```

## Step 2 — Forced comparison

```
For each option you proposed: what are the relative pros and cons for MY
corpus specifically — expected accuracy, cost per 1,000 documents, speed,
reproducibility, and the failure modes most likely given [language / OCR
quality / domain vocabulary / class imbalance] in my data?

Which do you recommend, and what is the strongest argument AGAINST your
recommendation?
```

## Step 3 — Understanding the chosen method

```
Explain [chosen method] to me in detail, at a conceptual level, assuming I
am a trained empirical economist but not a machine-learning specialist.

Cover: how it works mechanically, what assumptions it makes, where it is
likely to fail on my data, and how I should describe it in the methods
section of a paper. I need to be able to defend this choice to a seminar
audience and a referee.
```

## Step 4 — Pilot implementation request

```
Write [Python/R] code implementing [method] on the attached PILOT sample of
[N] documents. Requirements:

- Structured output: every response must conform to this JSON schema:
  [schema]. Include an "uncertain" escape category.
- Pin the model version string [exact identifier] and set temperature to 0.
- Log every raw model response to disk before any parsing.
- Log per-document input and output token counts.
- Handle failures gracefully: retries with backoff, and resumability if the
  run is interrupted mid-corpus.
- Comment each section of the code so I can audit what it does.
```

## Step 5 — Implementation challenge

```
Before I run this: audit your own code.

1. Correctness — walk documents [A] and [B] through the pipeline by hand and
   show me the intermediate states. Does the prompt actually enforce the
   rubric I specified?
2. Efficiency — can this be batched, cached, or parallelized? Using the
   pilot token counts, project the total cost of the full corpus of [N]
   documents at current [model] prices.
3. Robustness — what happens on an empty document, a malformed file, a
   rate-limit error, or a response that violates the schema?

List what you would change, then produce the revised version.
```

## Step 6 — Output inspection

```
Attached is the pilot output. Review it critically:

- Does the label/score distribution look plausible? Any category near 0% or
  above 90% should be treated as a prompt bug until proven otherwise.
- Sample 10 justifications and check each against its source document: does
  the cited content actually appear there?
- Any format drift between early and late responses in the run?
- What should concern me that I have not asked about?

Note: do not compute or interpret agreement statistics on fewer than ~30
items — at small N they reflect sample size, not signal.
```

## Step 7 — Validation protocol

```
I have a hand-coded validation sample of [N] items coded by [who, how many
coders, agreement rate]. It is stratified to oversample [rare/hard
categories].

Design the validation: 
- Split it into a selection set (for choosing among candidate prompts/models)
  and a held-out set (for the final reported accuracy). Never report accuracy
  from the selection set.
- Compute precision and recall per category, not just overall accuracy —
  my category of interest occurs in roughly [x]% of documents.
- Reweight stratified results back to the corpus distribution for the
  headline figure.
- Report the comparison as a table I can adapt for the paper's appendix.
```

## Step 8 — Adversarial challenge (run this even when things look good)

```
Based on everything we have developed in this project: challenge it.

- Does the overall approach still make sense for the research question?
- Attack the measure: what is it actually capturing that is NOT [construct]?
  What correlated-but-distinct constructs could drive it (e.g., complexity,
  industry jargon, document length, speaker identity)?
- Attack the pipeline: where could systematic (non-classical) measurement
  error enter, and would it correlate with my regressors or outcome?
- What would a hostile referee at [target journal] say, and which of those
  criticisms can I preempt now — before the at-scale run — cheaply?

Do not soften this. I want the strongest version of each objection.
```

## Supplementary — content-vs-context check (GABRIEL-style)

Use after step 7 when the measure will enter a regression:

```
Take [n=50] documents from the pilot. Produce stripped versions with every
sentence/phrase carrying [construct] removed, then re-score the stripped
versions with the identical prompt and model. Report the score change per
document. If scores barely move, the model is inferring from context
(metadata, style, speaker) rather than reading content — the measure is not
capturing what it claims.
```
