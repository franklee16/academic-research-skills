# Output contract

## Default conversational output

Answer directly in the Codex conversation unless the user asks for files or another format.

Provide two core elements:

1. **Clean revision**: place the complete revised passage or manuscript in a fenced `latex` block.
2. **Change explanations**: show the corresponding original text, revised text, concrete reason, and applicable diagnostic criterion or criteria for each substantive change.

Choose a readable structure that fits the length and task. Headings, tables, numbered records, Change IDs, severity labels, framework tags, and a separate diagnosis are optional rather than mandatory. Do not generate JSON, Markdown reports, DOCX, PDF, or other auxiliary files by default.

If the user specifies a different format or asks for only part of the default output, follow the user's instruction.

## Flexible change explanations

For each substantive change, preserve the following semantic mapping even when presentation varies:

- `Original`: the relevant source wording;
- `Revised`: the corresponding new wording;
- `Reason`: the specific problem and how the revision repairs it.
- `Criteria`: the criterion or criteria whose decision tests established the problem.

Keep presentation flexible; `Criteria` may appear as a short label or be integrated into the reason. Keep reasons concrete. Explain the affected topic chain, logical relation, agent/action, ambiguity, redundancy, claim strength, scope, evidence boundary, or consistency issue. Avoid generic explanations such as `improves flow`, `sounds more academic`, or `more concise` without identifying what changed.

Group repeated spelling, punctuation, grammar, or terminology edits when listing each instance would obscure the important revisions. Do not group changes with different reasons or different effects on meaning.

Mention author confirmation only for unresolved high-risk decisions. It may appear beside the relevant change or in a short final note; omit an empty confirmation section.

## LaTeX default

- Use a fenced `latex` block for the clean revision.
- Preserve existing LaTeX commands, citation keys, labels, equations, environments, and comments.
- For plain-text input, do not add a document preamble or unrelated scaffolding; present the revised prose in a LaTeX fence and escape characters only when needed for valid LaTeX.
- When the user requests DOCX, tracked changes, Markdown, plain text, JSON, a table, or another format, use that format instead.

### PDF-only routing

If a full manuscript is available only as PDF extraction and the original LaTeX commands and technical environments cannot be recovered reliably:

- deliver prioritized replacement passages or a section-by-section revision plan in LaTeX;
- retain exact PDF wording in each `Original` field and provide clean replacement prose in `Revised`;
- separate author queries from text that can be safely replaced;
- do not create a purported complete manuscript that substitutes comments such as `retain equation/table/prompt from source` for missing content;
- do not paraphrase equations, algorithms, prompts, code, or schemas as a way to fill extraction gaps.

An integrated clean manuscript requires the editable source or an explicit user request to reconstruct one from PDF with the associated limitations.

## Optional audit mode

Use the remaining schema only for long manuscripts, high-risk revisions, file-based workflows, or explicit requests for a formal audit trail. It is not a default user-facing format.

Preserve the source and write artifacts to new paths only when files are requested or materially useful for the requested scope.

## Internal ledger schema

Store a JSON object with this shape:

```json
{
  "title": "Revision report",
  "mode": "focused",
  "diagnosis": ["..."],
  "changes": [
    {
      "change_id": "CH-001",
      "location": {
        "section": "Introduction",
        "paragraph": 2,
        "sentence": 3
      },
      "change_type": "replace",
      "severity": "major",
      "original": "Exact source text.",
      "revised": "Exact revised text.",
      "reason": "Concrete explanation of the problem and repair.",
      "criteria": ["EVIDENCE-CLAIM", "HEDGING", "SCOPE"],
      "root_cause": "claim_exceeds_observational_evidence",
      "tags": ["HEDGE", "SCOPE"],
      "meaning_effect": "narrows_claim",
      "evidence_changed": false,
      "author_confirmation": true,
      "protected_change_authorized": false
    }
  ],
  "author_questions": ["..."]
}
```

### Audit-ledger fields

- `change_id`: unique `CH-###` identifier;
- `location`: string or object identifying section, paragraph, and sentence;
- `change_type`: `replace`, `delete`, `add`, `move`, `split`, `merge`, or `global`;
- `severity`: `minor`, `moderate`, or `major`;
- `original`: exact source excerpt;
- `revised`: exact revised excerpt;
- `reason`: specific rationale, not a generic phrase;
- `criteria`: one or more criterion IDs that established the defect;
- `root_cause`: the merged underlying defect addressed by the change;
- `tags`: one or more framework tags;
- `meaning_effect`: `none`, `clarifies`, `narrows_claim`, `strengthens_claim`, `changes_scope`, `structural`, or another explicit value;
- `author_confirmation`: Boolean.

### Optional integrity fields

- `evidence_changed`: Boolean, default false;
- `protected_change_authorized`: Boolean, default false;
- `related_changes`: list of Change IDs;
- `locations`: list for repeated global replacements;
- `agent_source`: role that proposed the change.
- `diagnostic_records`: source diagnostic record IDs merged into the change;
- `dependencies`: related criteria or changes that had to be resolved first.

`author_confirmation: true` means the decision is still unresolved and must appear in the author-confirmation queue. Set `protected_change_authorized: true` only after the user has explicitly authorized that protected-content change; once resolved, set `author_confirmation: false`. A pending confirmation is not authorization.

## Change types

### Replace

Provide the complete original and complete revised unit. Prefer a sentence or compact paragraph over isolated words when context affects the reason.

### Delete

Use the exact deleted source as `original` and `[deleted]` as `revised`. Explain why deletion does not remove evidence, scope, or a necessary logical step.

### Add

Use `[none]` as `original`. Distinguish a language-only bridge from a factual addition. Never insert a factual addition without source support or author confirmation.

### Move

Use the moved text in both `original` and `revised`, identify old and new locations, and explain the rhetorical or Flow reason.

### Split

Provide the full original sentence and all resulting sentences in `revised`.

### Merge

Provide all original sentences and the complete merged sentence.

### Global

Provide original form, standardized form, reason, and every affected location. Use only for genuinely identical mechanical or terminology changes.

## Optional formal record format

When a formal report is requested, a change may be rendered as:

```text
CH-014 | Introduction, paragraph 2, sentence 3 | Claim calibration

Original:
X causes a substantial improvement in Y.

Revised:
In this sample, X was associated with a substantial improvement in Y.

Reason:
The source uses causal language although the stated evidence supports an association. The revision restores evidential strength and scope.

Rules:
[EVIDENCE-CLAIM] [HEDGING] [SCOPE]

Meaning effect:
Narrows claim strength; data unchanged.

Author confirmation:
Required.
```

Use the user's language for field labels and reasons unless asked otherwise. Preserve the manuscript language inside Original and Revised. Do not impose this formal layout on the default conversational response.

## Grouping rules

- Record every substantive edit separately.
- Group multiple changes inside one sentence only when they share one coherent reason and the full sentence is shown before and after.
- Group identical spelling, punctuation, or terminology replacements only when every location is listed.
- Do not group unrelated edits under `improved clarity` or `improved flow`.
- State exactly which topic chain, logical relation, agent/action, claim force, or redundancy was repaired.
- Preserve every applicable criterion on the merged change; do not create separate user-facing changes for multiple criteria that share one root cause.

## Reason-quality rules

Reject generic reasons such as:

- `improve readability`;
- `make it academic`;
- `improve flow`;
- `grammar` without identifying the grammatical issue;
- `more concise` without identifying removed redundancy.

Prefer reasons such as:

- `Moves the previously introduced model into topic position so the sentence links to the prior finding.`
- `Restores the researcher as agent and converts the nominalization evaluation into the verb evaluated.`
- `Replaces causal causes with associated with because the described design is observational.`
- `Adds the summary noun discrepancy so this has one explicit antecedent.`

## Audit-mode validation rules

When audit mode is used:

- ensure every Change ID is unique;
- ensure every required field is present;
- ensure each non-add original excerpt occurs in the source;
- ensure each non-delete revised excerpt occurs in the clean revision;
- ensure every changed text span is covered by at least one ledger entry;
- reject unapproved number or LaTeX citation-key changes;
- ensure every `author_confirmation: true` item appears in the confirmation queue;
- ensure every applicable criterion coverage cell is `PASS`, corrected `ISSUE`, explicit `QUERY`, or `N/A`;
- ensure every changed span points to the diagnostic records and criteria that justified it;
- ensure no placeholder such as `[TODO]`, `[citation needed]`, or unsupported factual bridge remains in the clean revision;
- manually verify units, non-LaTeX citations, author attribution, technical terms, and formatting because the helper script does not fully validate them.
