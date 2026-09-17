---
name: dril-dataset-construction
description: >
  Implement the DRIL (Deep Research on a Loop) methodology to construct economic
  datasets from primary sources using AI agents. Use this skill whenever the user
  wants to build a dataset, construct panel data, collect cross-country or
  cross-sectional data, compile institutional or legal variables, automate
  research-assistant data collection, or create a codebook for systematic source
  coding. This includes tasks like "collect corporate tax rates by country,"
  "build a dataset on central bank independence," "code subnational borrowing
  rules," or "create a panel of regulatory indicators." Even if the user does
  not mention "DRIL" or "dataset construction" explicitly, use this skill when
  the task involves gathering structured data from scattered primary sources
  (laws, reports, filings, gazettes) across multiple units (countries, firms,
  years) with formal coding rules and documented evidence.
---

# DRIL Dataset Construction

This skill implements the **Deep Research on a Loop (DRIL)** methodology (Afonso et al., NBER w35188) for constructing structured datasets from primary sources using AI agents. DRIL separates research design from implementation, enforces a formal research instrument across all units, and produces auditable records with full citations.

## What DRIL Does

DRIL converts open-ended web research into standardized, auditable dataset construction. It targets problems where:
- Information exists in publicly accessible sources (legal texts, regulatory filings, government reports, policy documents)
- Variables can be formally defined in a codebook with coding rules
- The unit space is enumerable (e.g., 30 countries × 20 years)
- Auditability and traceability to primary evidence matter

## Architecture Overview

DRIL has three stages:

1. **Design Stage** (executed once): Produce a frozen research instrument, mapped unit space, and evidence policy
2. **Implementation Stage** (executed N times, once per unit): Run autonomous web research, code answers, and document evidence
3. **Verification Stage** (audit pass): Re-read cited sources and judge whether evidence supports recorded values

## Prerequisites

Before starting, the user should have:
- A clear research objective stated in natural language
- A rough sense of the target unit space (e.g., "OECD countries, 2010-2023")
- Familiarity with the domain to review the design agent's output

## Stage 1: Design

The design stage produces three artifacts that form the **frozen protocol**. Once finalized, they do not change during implementation.

### 1.1 Research Instrument (Codebook)

For each variable in the target dataset, the instrument specifies:

- **Question**: A precise question the agent must answer (e.g., "Does the subnational government have independent tax-setting authority?")
- **Value type**: Categorical with values {full, limited, none}, continuous with units, or other defined domain
- **Coding rules**: How to translate source material into the variable's value domain
- **Field kind**: Whether the variable produces a coded scalar, coded multivalue, narrative summary, extractive note, entity list, or tabular extract
- **Per-variable source overrides** (optional): When the default source hierarchy is inappropriate

Cross-cutting policies also govern:
- What to do when a literal match is absent
- How to document missing data
- When to add interpretive notes
- Under what conditions to flag items for follow-up
- How much source detail to retain

Read `references/codebook_template.yaml` for a complete template and example.

**Output**: `codebook.yaml`

### 1.2 Mapped Unit Space

Define the dimensions and their values:

- A dimension might be countries (ISO 3166-1 codes), years, policy domains, or any enumerable classification
- The mapped unit space is the Cartesian product (or defined subset) of these dimensions
- Each element is a **mapped unit** representing one row of the target dataset

**Output**: `units.csv` with one row per mapped unit (e.g., `country,year`)

### 1.3 Evidence Policy

The evidence policy governs how the implementation agent finds, evaluates, and documents sources. It has three components:

1. **Source-role hierarchy**: Priority ranking of source categories. For institutional/legal research: constitutional provisions > statutes > regulations > official guidance > academic syntheses. Can be global or overridden per variable.
2. **Citation contract**: Minimum documentation for any factual claim:
   - Verbatim excerpt from the source
   - Working URL + access date (web) or document name + page number (document)
   - Precise locator within the source (e.g., "Article 73, paragraph 2" or "Table 3.1, row for Argentina")
3. **Conflict resolution rules**: What to do when sources disagree — prefer more authoritative source, prefer more recent source, report both values, or flag for human review.

Read `references/evidence_policy_template.md` for a template.

**Output**: `evidence_policy.md`

### 1.4 Protocol Snapshot

Before implementation begins, save a frozen protocol that records:
- Research instrument version
- Evidence policy version
- Unit roster
- Operational parameters (model version, search parameters)

**Output**: `protocol_snapshot.json`

## Stage 2: Implementation

The implementation agent receives the frozen protocol and executes the instrument once per mapped unit. For each unit, the agent:

1. Formulates search queries based on the unit and the instrument's variables
2. Reads and evaluates sources according to the evidence policy's source hierarchy
3. Applies coding rules from the research instrument
4. Records structured evidence for each coded answer

### Required Output Per Unit

For each variable in the instrument, the agent produces:

- **Coded answer**: Following the specified value type and coding rules
- **Evidence item**: Linked to the answer, meeting the citation contract (verbatim quote, source locator, URL or page reference)
- **Uncertainty status**: One of {answered, not_found_after_search, not_applicable, proxy_used, inferred, conflict_unresolved}

Additionally, each unit record contains:
- **Source inventory**: All sources consulted, with their roles in the source hierarchy
- **Data gaps**: For any variable that could not be answered, a documented gap record with reason (not_found_after_search, not_applicable, unclear_definition, conflict_unresolved, out_of_scope)
- **Narrative notes**: Where the instrument specifies qualitative context is needed
- **Search logs**: Queries executed and results obtained

**Outputs**:
- `dataset.csv`: One row per mapped unit, one column per variable, plus uncertainty flags
- `evidence_records.json`: Structured evidence for each coded cell
- `gap_log.csv`: Documented data gaps
- `search_log.csv`: Search queries and results

### Operational Constraints

The implementation agent must:
- Stay within the scope of the approved design (no new variables, no broadening the unit space)
- Use the source-role hierarchy specified in the evidence policy
- Record uncertainty honestly rather than guessing
- Produce output conforming exactly to the structure derived from the research instrument
- Not silently produce null values — always document why data is missing

## Stage 3: Verification

The verification stage is a separate audit pass. A verification agent:

1. Reads the coded answers and their cited sources
2. Re-reads the source material (or accesses the URL/document)
3. Judges whether the recorded evidence supports the recorded value
4. Flags discrepancies for human review

This stage can run at any time after implementation completes, including after an initial release of the dataset. It is not optional for published datasets.

**Output**: `verification_report.md` with flagged items and adjudication notes

## Data Quality Mechanisms

Three mechanisms govern data quality throughout:

### Explicit Data Gaps
When information cannot be found, do not silently produce null. Create an explicit **data gap record** documenting what was searched for, what was found, and why the search was unsuccessful. Classify by reason: not_found_after_search, not_applicable, unclear_definition, conflict_unresolved, out_of_scope.

### Structured Uncertainty
Every observation carries a status indicator:
- **answered**: Coded with evidence
- **not_found_after_search**: No qualifying source located
- **not_applicable**: Variable does not apply to this unit
- **proxy_used**: Answer relies on a substitute measure
- **inferred**: Answer was derived rather than directly observed
- **conflict_unresolved**: Sources disagree and conflict was not adjudicated

### Append-Only Observation Ledger
When results are updated, the original observation is not overwritten. A new observation row is appended that supersedes the prior one. The current view reflects the latest observation, but the full history is preserved for audit.

## Output Assembly

At the end of a DRIL run, assemble all outputs into a reproducible package:

```
dril_run_YYYYMMDD/
├── protocol/
│   ├── codebook.yaml
│   ├── units.csv
│   ├── evidence_policy.md
│   └── protocol_snapshot.json
├── outputs/
│   ├── dataset.csv
│   ├── evidence_records.json
│   ├── gap_log.csv
│   └── search_log.csv
├── audit/
│   └── verification_report.md
└── README.md
```

Use `scripts/validate_codebook.py` to check that the codebook is well-formed before implementation. Use `scripts/assemble_dataset.py` to compile the final dataset from unit records.

## Important Notes

- DRIL does not eliminate the need for human judgment. It redirects human effort from collecting data to designing instruments and reviewing evidence.
- The research instrument is the authoritative specification. What it fails to specify, the agent cannot fill in with common sense.
- Design-stage corrections should trigger protocol versioning and re-execution, not silent edits.
- Every cell in the final dataset must be traceable to a specific passage in a specific source.

## When NOT to Use DRIL

Do not use this skill when:
- Data comes from a single structured database or API (use direct extraction instead)
- The research is exploratory and variables are not yet defined
- The unit space is open-ended ("find all countries that have this policy")
- Real-time data access, confidential information, or non-codifiable human judgment is required
- Volume matters more than traceability (e.g., sentiment scores for millions of posts)
