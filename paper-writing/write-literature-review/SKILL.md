---
name: write-literature-review
description: Write or revise the literature review / related-literature section of an empirical paper (finance, economics, accounting), positioning the paper's contribution against prior work. Use whenever the user asks to write, draft, restructure, or fix a literature review section; organize a .bib file or pile of papers into themed synthesis; respond to reviewer complaints like "reads like a list," "missing literature," "weak positioning," or "insufficient contribution"; convert paper-by-paper paragraphs into critical synthesis; or plan how to frame the paper relative to 2-4 literature streams. Also trigger for "related literature," "literature review section," "positioning our contribution," and referee-report points about citations or novelty claims.
---

# Literature Review Section Writer

A literature review section is an argument for the paper's marginal contribution — a defensible map of the field, not a stack of paper summaries. Every subsection exists to establish what is known, what is contested, and what gap this paper fills. If a paragraph doesn't advance that argument, it doesn't belong.

Distinguish, in everything you write: established findings vs. authors' interpretations vs. field consensus vs. open controversy vs. this paper's inference. Readers (and referees) punish blurred versions of these.

Full rationale for each rule below lives in `references/source-principles.md` (distilled from Nature Reviews Bioengineering 2024 editorial and Dhillon 2022, FEBS Journal, adapted from standalone review articles to paper sections). Read it when an edge case isn't covered here.

## Inputs

Gather what's available: the paper draft or introduction, the paper set (.bib, PDF folder, annotated notes, or just author-year mentions), target journal, and expected section length.

Don't stall on missing inputs. State reasonable assumptions and produce a first version. Only ask the user about information that would change the framing itself — e.g., whether the paper's contribution claim is actually accurate, or which of two conflicting positioning angles is intended.

## Step 1 — Positioning gate

Before touching prose, output these five items:

1. **One-sentence paper statement**: "This paper [does X] using [data/method], showing [result]."
2. **Literature streams**: the 2–4 bodies of work this paper speaks to. Fewer, weighted, beats many shallow.
3. **State of each stream**: what is established, what is contested.
4. **The gap**: one sentence per stream — what the stream leaves unanswered that this paper answers.
5. **Space allocation**: how many paragraphs/words each stream gets, and which stream carries the main positioning weight.

If the map looks like a textbook chapter, keep narrowing until every stream directly serves the contribution claim.

## Step 2 — Evidence matrix

For each core paper, extract:

| Field | Content |
|---|---|
| Identity | Author, year, journal, citation key |
| Question | What the paper actually answers |
| Design | Method, data, sample, identification |
| Key finding | The result relevant to THIS paper's question |
| Strength/limit | Design advantage, or bias / external-validity boundary / measurement issue |
| Relation | To our paper: supports / contrasts / is extended by / is the closest competitor |
| Placement | Which stream subsection it lands in |

The "Relation" column is the point of the exercise. A matrix of what each paper did is a filing system; a matrix of how papers relate to each other and to ours is the raw material of synthesis. Also note paper-to-paper relations (agreements, conflicts, extensions) when you see them — those become paragraphs.

Papers in the .bib that don't earn a row relevant to the streams get cited elsewhere or not at all — cite to support specific claims, never for coverage.

## Step 3 — Argument-driven outline

Organize by theme or debate. Never chronologically, never paper-by-paper. Each subsection follows this chain:

**claim → key evidence → agreement/conflict among studies → why the conflict exists (setting, sample, measurement, identification assumptions) → the gap → how this paper differs**

The conflict-explanation step is where critical synthesis lives. If two streams disagree, diagnose the disagreement; if you can't, keep the uncertainty explicit rather than manufacturing a resolution.

Subsection headings should be specific and reveal content ("Institutional investors and carbon disclosure," not "Prior literature").

If 3+ closely related papers are method-comparable, plan one comparison table (question / data / method / finding / difference from this paper) — standard in finance and often stronger than another paragraph.

End the section with the handoff: what is established across streams, the gap, and the bridge to this paper's contribution. The final move answers "so what" — it does not speculate (that belongs in the paper's conclusion).

## Step 4 — Drafting rules

- **No laundry list.** The failure mode both source journals warn about most. Test: if a paragraph summarizes as "X found this; Y found that; Z found the other," rewrite it around a claim the paragraph defends. Selectivity is fine; comprehensive-but-shallow is not.
- **Cite originals.** For a specific finding, cite the paper that produced it, not a review that mentioned it. No ambiguity about who did the work.
- **Balance.** Present contrary evidence even when building toward your view. Discuss the closest competitor's paper honestly — referees know it.
- **Positioning move at the end of every thread.** Each subsection closes with how this paper differs, not with a summary of what was cited.
- **Reader-friendliness.** Define terms at first use. Minimal acronyms. Make transitions explicit — never assume the reader sees why you moved from one theme to the next. Specifics over generalities: data, sample period, identification strategy, magnitudes.
- **No fabricated citations.** Every citation must trace to a provided source (paper, .bib entry, or user-supplied note). If you're unsure a cited paper exists or says what's claimed, mark it `[UNVERIFIED]` for the user rather than writing it as fact.
- **No copied sentences.** Extract facts and relations, re-express. Text recycling from the user's own prior papers included.
- **Anti-slop writing.** Apply the deletion list from the global CLAUDE.md — no "delve," "pivotal," "underscore," rule-of-three emphasis, vague attributions ("studies show" without a name).
- **Layout choice.** Offer both layouts when drafting fresh: a dedicated "Related Literature" section after the introduction, or literature woven through the introduction (common at JF/JFE/RFS). Pick based on target journal convention; when unknown, default to dedicated section for papers with 3+ streams, woven for narrow positioning.

Match the paper's existing notation and citation style (natbib/biblatex, `\citet` vs `\citep` usage).

## Step 5 — Quality gate

Before delivering, score each item `PASS / REVISE / INSUFFICIENT EVIDENCE`:

1. **Positioning**: could a referee state this paper's contribution after reading the section alone?
2. **Organization**: thematic, not chronological or enumerative?
3. **Traceability**: does every important conclusion rest on a specific cited source?
4. **Balance**: are contrary findings and the closest competitor presented honestly?
5. **Laundry-list check**: does any paragraph fail the "X did this; Y did that" test?
6. **Positioning moves**: does every thread end with how this paper differs?
7. **Citations**: metadata verified against provided sources; unverifiable items flagged?

Nothing rated `INSUFFICIENT EVIDENCE` may be stated as established fact in the delivered draft.

## Delivery

Output in this order, showing only what the user asked for (run the upstream steps internally regardless):

1. Positioning gate (assumptions flagged)
2. Evidence matrix
3. Themed outline with argument chains
4. Drafted section (LaTeX or Markdown, matching the paper's format)
5. Comparison table plan, if applicable
6. Quality gate report
7. Flag list: unverified citations, papers missing from the matrix, streams the user may want to add

## Response to referee comments

When invoked with a referee report ("missing literature," "reads like a list," "contribution unclear"): classify each comment against the quality gate items, fix the section, and produce a change list mapping each comment to the specific revision — same discipline as the R&R protocol in the global rules.
