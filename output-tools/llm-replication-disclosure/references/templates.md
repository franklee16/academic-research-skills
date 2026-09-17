# Templates for LLM-Assisted Replication Packages and Disclosure

Read this file when drafting disclosure text (Mode 2) or assembling a
package (Mode 3). Every bracketed field must come from the user's actual
records — never fill one with a plausible default. If a field is
unrecoverable, the template's honest-gap variants show how to say so.

---

## 1. Package directory structure

```
replication_package/
├── README.md                  # skeleton in section 2 below
├── prompts/
│   ├── final/                 # every prompt in final form: system prompts,
│   │                          #   rubrics, few-shot examples, vocab lists
│   ├── variants/              # robustness prompt variants, named by the
│   │                          #   table they produce (e.g., prompt_tableA7.txt)
│   └── project_log.md         # AGENTS.md / decision log if one exists
├── code/
│   ├── 01_preprocess/         # corpus restriction, pre-screens, snippets
│   ├── 02_model_calls/        # API/batch scripts + response parsers
│   ├── 03_analysis/           # measure -> every table and figure
│   └── environment/           # requirements.txt / renv.lock, hardware notes
├── raw_model_outputs/         # THE critical artifact: every raw response,
│                              #   organized by run, with run manifests
├── validation/
│   ├── validation_data.csv    # hand-coded labels
│   ├── coding_instructions.md # what the coders were told
│   └── holdout_ids.txt        # which items were held out from selection
├── data/
│   ├── final/                 # analysis datasets built from raw outputs
│   └── access_instructions.md # for restricted sources; NO licensed material
└── models/                    # only if fine-tuned/self-hosted: weights or
                               #   hub identifier + revision hash, FT data/code
```

## 2. README skeleton

```markdown
# Replication package for "[Paper title]"

## Overview
[1 paragraph: what the package reproduces; which results rely on
LLM-generated measures.]

## Requirements
- [Language + version]; install via [requirements file].
- Approximate total runtime: [X]; approximate API cost if re-running model
  calls: [$Y] at [date] prices.
- NOTE: re-running model calls is NOT required to reproduce the paper's
  numbers and is not guaranteed to return identical output (see
  "Reproducibility limits"). All reported results reproduce exactly from
  `raw_model_outputs/`.

## Model details
- Model: [exact versioned identifier], accessed [date range].
- Settings: temperature [t], [top-p / max tokens / seed / reasoning mode],
  output format: [JSON schema / forced choice].
- Data-sensitivity route: [enterprise zero-retention contract /
  self-hosted open-weight model (weights archived at ...) / public data].

## Order of execution
| Step | Script | Input | Output | Feeds |
|---|---|---|---|---|
| 1 | code/01_preprocess/... | raw corpus | screened corpus | Table 1, Fig 1 |
| 2 | code/02_model_calls/... | screened corpus | raw_model_outputs/ | — |
| 3 | code/03_analysis/... | raw outputs + validation | all tables/figures | Tables 2–6 |

## Script-to-exhibit mapping
[Every table and figure -> producing script -> output file.]

## Validation
[Sample size, coder description, inter-coder agreement, selection vs
held-out split, held-out precision/recall/accuracy.]

## Reproducibility limits
Model calls to hosted LLMs are not exactly reproducible (server-side
batching; possible model retirement). We compensate by archiving every raw
model response in `raw_model_outputs/`; all downstream results are
mechanically reproducible from these archives. [If self-hosted: weights and
decoding settings archived; identical output verified on our hardware, not
guaranteed across hardware.]
```

## 3. Methods / appendix paragraph (paper-facing)

Standard variant:

```
[Measure name] was constructed using [exact model identifier], accessed
between [start date] and [end date] via [the batch API / API / interface],
with temperature [t][, seed s,] and responses constrained to [format]. The
full prompt, including the classification rubric and [k] few-shot examples,
is reproduced in Appendix [X] and included in the replication package. We
validated the measure against [N] observations hand-coded by [description
of coders] following written instructions (Appendix [Y]); [n_sel] items
were used to select among candidate prompts and [n_holdout] were held out,
on which the final configuration achieved [precision/recall/accuracy
figures]. [Licensed data from vendor V were processed under an enterprise
agreement with zero data retention / All model inference was performed
locally on an open-weight model, so no licensed data left our environment.]
Because hosted model inference is not exactly reproducible and model
versions may be retired, the replication package archives every raw model
response; all results in the paper reproduce exactly from these archives.
```

Honest-gap variants (use, don't hide):

- Unknown access date: "accessed in [month-year]; exact dates were not
  logged."
- Selection/evaluation overlap discovered late: "an additional held-out
  sample of [n] items, coded after prompt selection, yields [figures]; the
  original combined-sample figure of [x] is reported for completeness."
- Raw outputs not archived for an early run: "outputs for [component] were
  regenerated on [date] with logging enabled; regenerated labels agree with
  the original analysis dataset for [x]% of items, and all reported results
  use the archived regenerated outputs."

## 4. Journal generative-AI disclosure statement

Before drafting, SEARCH the target journal's current policy — wording and
required granularity differ and change. Generic fallback covering the
common requirements:

```
Disclosure of generative AI use: Large language models were used in this
research as follows. (1) Data construction: [model + version] generated
[measure(s)] as described in Section [X] and Appendix [Y]; prompts, raw
model outputs, and validation data are included in the replication
package. (2) Code: portions of the analysis code were drafted with
[tool(s)] and were reviewed, tested, and are fully documented by the
authors. (3) Writing: [none / language editing only / specify]. The
authors take full responsibility for all content. No confidential or
licensed data were transmitted to third-party model providers [except
under the zero-data-retention enterprise agreement described in
Appendix Y].
```

## 5. Figure/table note fragment (for exhibits built on LLM output)

```
Notes: [Variable] classified by [exact model identifier] ([settings]),
accessed [date]. [Preprocessing summary: screening rule, snippet window.]
Validation against [N] hand-coded items: [held-out figures]. Prompts,
code, and raw model outputs are available in the replication package at
[DOI].
```

## 6. Mode 1 gap-report format

```
# Replication-readiness gap report — [project name], [date]

FATAL
- [ ] Raw model outputs: [status + evidence checked]

MAJOR
- [ ] Pinned model version + access dates: [...]
- [ ] Held-out validation accuracy: [...]
- [ ] Final-form prompts preserved: [...]

MINOR
- [ ] README / script-exhibit mapping: [...]
- [ ] Runtime and API-cost notes: [...]

Remediation plan (ordered by cost of delay): [...]
```
