# Source-Only Verification

## Purpose

Source-only verification is used when the user provides a closed corpus and asks the skill not to use external knowledge. The corpus may consist of PDFs, uploaded papers, paper notes, a BibTeX file, a reference list, tables, figures, appendices, code output or manually pasted excerpts.

In this mode, every supported claim must trace to the supplied materials.

## Activation triggers

Use source-only verification when the user says any equivalent of the following.

```text
Only use these papers.
Verify against the uploaded PDFs only.
Do not search outside the corpus.
Check whether this related work is faithful to this reference list.
Audit these claims against my paper notes.
```

## Rules

1. Do not use external knowledge to rescue a claim.
2. Mark unsupported claims as not in corpus, not as false.
3. Distinguish absence from contradiction.
4. If the corpus is incomplete, state that the audit is corpus-limited.
5. If a claim is central and not in the corpus, recommend either adding a source or weakening the claim.

## Corpus traceability table

| Claim ID | Claim | Corpus source | Source location | Support status | Missing evidence | Action |
|---|---|---|---|---|---|---|

## Common outcomes

```text
Verified in corpus
Partially supported in corpus
Not in corpus
Contradicted by corpus
Requires manual PDF inspection
Requires corpus expansion
```

## Use in related work writing

When drafting related work from a fixed corpus, do not create claims that go beyond the corpus. If a natural claim is not supported by the provided papers, label it as a search need rather than writing it as fact.
