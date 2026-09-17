# Exhaustive checklist

Use this during the section-by-section sweep (Section 9 of the review). The point is comprehensiveness: every category here is a class of issue that could appear in a manuscript and shouldn't be missed. You will not flag every category in every paper — most papers won't have most of these problems. But you should *scan* for each category in each relevant section.

This is reference material, not a template. The output of the sweep is still prose-with-numbered-points organized by section, not a checklist.

## Cross-cutting: read for these throughout the entire manuscript

### Draft state and self-annotations

For pre-submission drafts, the manuscript itself contains signal about where the author is stuck. Read these as input, not as finished prose:

- Inline TODOs: `[TODO: ...]`, `[NOTE: ...]`, `[CONTENT: ...]`, `[REF]`, `[CITATION NEEDED]`. Note where they cluster — a section with five TODOs is a section the author hasn't worked out, regardless of what the existing prose says.
- Bracketed alternatives: `[X / Y / Z]` or "the firm [acquired / merged with / partnered with]". The author hasn't picked. If the choice is consequential, flag.
- Self-questions: `[is this still defensible?]`, `[do I need this hypothesis?]`. Address directly in the review — they're explicit asks.
- Tracked-changes density: heavy edits in one section but none in others tells you what's contested. Note the pattern and what it implies.
- Existing comments (if read from the docx XML): the author or coauthors flagging issues to themselves. These are the issues already known; don't pretend you discovered them, but do extend or sharpen them where useful.
- Placeholder count: "[Table 3 about here]" but the methods section describes only two tables — inconsistency.
- Section labels like "[draft]", "[skeleton]", "[needs work]" — preamble note, don't penalize.

The point is to distinguish *the author's known unfinished business* from *what the author thinks is finished but isn't*. The first gets a brief acknowledgment ("I see the discussion section is marked as draft; reviewing what's there"); the second is where the diagnostic actually lives.

### Numerical and factual consistency
- Sample sizes (N, n) reported in abstract, methods, tables, robustness checks — do they match?
- Time periods reported in abstract, intro, methods, tables — do they match?
- Counts of variables, hypotheses, robustness checks — match between text and tables?
- Means, standard deviations, correlations — does anything look suspicious or contradict elsewhere?
- Effect sizes interpreted in text — are they consistent with what's in the tables?
- Percentage changes calculated from log-transformed coefficients — done correctly?
- Citations to specific page numbers — are page references plausible (don't fabricate verification, but flag obvious mismatches like "Smith (2010, p.847)" for a 6-page paper)?

### Citation hygiene

The detailed reference handling lives in the section-specific "References" subsection below — including the bidirectional consistency check (every in-text citation appears in references and vice versa), citation density assessment, and the opt-in style audit.

Cross-cutting citation issues to scan for during the read of the body text:

- Citations to specific page numbers — are page references plausible (don't fabricate verification, but flag obvious mismatches like "Smith (2010, p.847)" for a 6-page paper)?
- Citation drift across sections: the same work cited differently in different sections (Smith 2010 in intro, Smith et al. 2010 in discussion).
- Heavy clustering of same-author citations in one paragraph (suggests over-reliance or reviewer-identification risk).
- Citations to fields the paper isn't actually engaging with (kitchen-sink positioning).
- Foundational citations missing for the literatures the paper engages — flag *streams of work* the paper underweights, not specific titles unless certain.

### Conceptual drift
- Does the paper's core construct change meaning across sections? (Common: introduction defines X loosely, methods operationalize X narrowly, discussion claims about X loosely again.)
- Does terminology shift inconsistently? (E.g., a broad umbrella term in the introduction becomes a narrow setting-specific term in the methods, then reverts to the umbrella term in the discussion — flag.)
- Does the paper drift between "association," "effect," "impact," "drives," "causes" in ways that imply different causal claims?

### Hedge language and overclaiming
- "Significant" used where "statistically valid evidence for an effect" is meant.
- Causal language ("X causes Y," "X drives Y") where the design supports only association.
- "Demonstrate" or "establish" used where evidence is suggestive, not probative.
- "First" or "novel" claims — verify (loosely) whether plausible to claim, or whether the literature has prior versions.
- Practical implications overstated relative to effect sizes.

### Prose register
- Active vs. passive voice consistency
- Consistent verb tense (literature in past, current contribution in present is the convention)
- Sentence-level redundancy ("In the context of," "It should be noted that," "It is important to recognize")
- Paragraph-level redundancy (does each paragraph add something, or is paragraph 3 saying what paragraph 1 said with different words?)

## Section-specific scans

### Title
- Does it convey the paper's contribution, or just its topic?
- Is it specific enough to be discoverable, or generic ("A Study of X and Y")?
- Does it overstate (e.g., "How X Causes Y" for a correlational study)?
- Length: top journals lean toward 7–12 word titles.

### Abstract
- Word count appropriate for the target journal (usually 150–250).
- Does it state the contribution, the design, the finding, the implication?
- Are there incomplete sentences or grammatical errors? (This is a serious flag — abstracts get more scrutiny than any other section.)
- Does it overstate findings relative to what's in the results?
- Does it match what the intro says the paper does?

### Introduction
- Is there a clear motivating puzzle, tension, or unsolved problem? Or just an observation that "research has not examined X"?
- Is the gap *theoretical* (something prior accounts can't explain) or *empirical* (no one has measured X) or *contextual* (no one has tested X in setting Y)? The first is strongest, the third is weakest.
- Does the introduction "sell" the paper or summarize it? (Top journals expect selling.)
- Is the contribution articulated in terms of *what's added or changed* in the literature, not just what the paper does?
- Does it foreshadow findings without requiring readers to slog through theory to see whether it's worth their time?
- Length: top journals tend to run 4–8 pages of introduction; longer often signals positioning insecurity.
- Are there unnecessary repetitions of motivation that should be moved to or trimmed from later sections?

### Theory / conceptual development
- Are constructs sharply defined? Where? (First mention, or buried in methods?)
- Are construct definitions consistent with how prior literature uses them, or do they break from convention without justification?
- Is the theory *derived* (hypotheses follow logically from a set of premises) or *assembled* (hypotheses listed, then prior literature cited as support after)?
- Are mechanisms specified or just named? "X reduces Y because of Z" — is Z actually explained, or just labeled?
- Are alternative theoretical accounts engaged, or dismissed/ignored?
- Are boundary conditions specified, or left implicit?
- Does the theory section motivate the paper *again* — and if so, can that be cut?
- Does it review literature exhaustively (bad — looks like a lit review chapter) or selectively (good — engages only what matters)?

### Hypotheses / propositions
- Does each hypothesis follow from the theory, or is it asserted with citations?
- Are hypotheses *diagnostic* — would different theories predict different outcomes — or consistent with many accounts?
- Are some hypotheses obvious (i.e., "X is positively related to Y" where the only theoretical surprise would be a null)? Flag and consider whether they're necessary.
- Does H2 follow from the *same* logic as H1, or does it require additional theoretical scaffolding?
- Interaction hypotheses: is the moderator's mechanism specified, or just predicted to "amplify" or "attenuate"?
- Are there too many hypotheses for the conceptual depth? (5+ hypotheses for a paper without a clear unifying mechanism is a flag.)

### Methods
- Sample: how was it constructed? Inclusion/exclusion criteria specified? Selection bias addressed?
- Is the sample size justified, or just reported?
- Variable construction: is each measure defined, sourced, and validated? Are multi-item measures' alphas reported?
- Are control variables justified theoretically, or kitchen-sinked?
- Identification strategy: explicit, or implicit?
- Robustness checks: do they address the most plausible alternative explanations, or are they deck-stacking?
- Is the analytical approach appropriate to the structure of the data (clustered errors, fixed effects, etc.)?
- Are deviations from prior literature in measurement or method explained?
- Replicability: could a reader reproduce the analysis from what's described?

### Results / findings
- Are tables labeled clearly?
- Do table footnotes match what's reported?
- Are coefficients reported with appropriate precision (too many decimals is amateurish; too few hides effect sizes)?
- Do results in text match results in tables?
- Are significance stars consistent with reported p-values or standard errors?
- Are interactions interpreted at meaningful values (not just at the mean)?
- Are effect sizes interpreted in substantive terms, or only in standardized coefficients?
- For null results: are they discussed, or buried?
- For supported hypotheses: is the magnitude actually meaningful, or just statistically detectable?

### Discussion
- Does it overclaim relative to results? (Most common discussion problem.)
- Does it engage with the most plausible alternative explanations, or sidestep them?
- Are limitations discussed, or only token-listed?
- Does the practical implications section connect to the actual findings, or pivot to general managerial advice?
- Does it gesture at future research in ways that are concrete, or generic?
- Length: discussions in top journals are usually substantial (4–8 pages); under 2 pages signals underdeveloped framing.
- Does the discussion repeat what was already said in the intro? (Bad — discussion should *advance* the paper's argument given the findings.)

### References

**Default scan (always done):**

- Bidirectional consistency check: every (Author, Year) cited in the body should appear in the reference list, and every entry in the reference list should be cited somewhere in the body. Do this systematically — extract the in-text citations and the reference list, compare them, and report any in-text citations missing from references and any orphaned reference entries. This catches real authorial errors (citations dropped during edits, late additions not yet in references) and is high-signal.
- Citation density: too few (suggests poor positioning) or too many (suggests citation dump)?
- Self-citation balance: heavy self-citation flags reviewer-identification risk and substantive over-reliance on the authors' own prior work.
- Are foundational citations missing for the literatures the paper engages? Flag *streams of work* the paper underweights, not specific titles unless certain.
- Recency: papers in top journals usually cite work from the past 5 years for the central conversation. If the most recent citations are 10+ years old, flag positioning concern.
- Reference list completeness at a glance: are obvious fields missing across multiple entries (e.g., several entries with no year, no journal, no page numbers)? Flag systemic gaps but don't go entry-by-entry unless the user asks.

**Style audit (opt-in only):** A full per-entry reference style audit is *not done by default*. It's tedious, produces long noisy output, and only the user knows the target journal's exact requirements. Trigger it only when the user asks: "check my references," "audit my reference list," "do a reference style pass," "check for APA compliance," or similar.

When the user requests an audit, ask once: "Which style should I check against — APA 7th, or a specific journal's style (AMJ, ASQ, AMR, SMJ, Organization Science, JOM, JIBS, etc.)?" If the user already specified the target journal earlier in the conversation, use that journal's style without asking again. If they say "APA," use APA 7th unmodified. If they name a journal, use the major management journal conventions catalogued below as a starting point, and explicitly note any conventions you're uncertain about so the user can verify.

**Major management journal style notes** (for opt-in audit):

| Journal | Reference style basis | Notable deviations from APA 7th |
|---|---|---|
| AMJ | APA-derived | Uses ampersand (&); volume italicized; DOIs preferred; year in parentheses |
| ASQ | APA | Adopted APA style for citations and references in January 2025; house styles change, so check the journal's current author guidelines rather than assuming |
| AMR | APA-derived | Similar to AMJ; ampersand; volume italicized |
| SMJ | Modified APA | Ampersand; DOI required for online-first; specific journal abbreviation conventions |
| Organization Science | INFORMS style | Numbered references in some journals; check current author guidelines |
| JOM | APA 7th | Largely standard APA |
| JIBS | APA-derived | Specific format for non-English language sources |
| Research Policy | Elsevier/Harvard | Substantially different — author-year inline, specific punctuation |
| Strategic Organization | APA-derived | Similar to SMJ |

For any journal not listed, default to APA 7th and flag in the review that the user should verify against the journal's current author guidelines, since style requirements change.

**APA 7th checkpoints (when audit is requested):**

For each reference entry, scan for:

- *Author formatting*: Last name, F. M. (initials with periods and spaces); ampersand before final author; up to 20 authors listed before "..."; exact comma placement.
- *Year*: in parentheses after authors, period after closing paren; for in-press, "(in press)"; for no-date sources, "(n.d.)".
- *Article title*: sentence case (only first word, proper nouns, and word after colon capitalized); no quotation marks; period at end.
- *Journal title*: italicized, title case, no abbreviation unless the journal explicitly abbreviates.
- *Volume*: italicized number; issue in parentheses (not italicized) only if each issue starts at page 1; comma after.
- *Page range*: en-dash (–), not hyphen; no "pp."; period at end before DOI.
- *DOI*: full URL form (https://doi.org/...) for APA 7th; not just the bare DOI string; no period after.
- *Books*: publisher name only (no city as of APA 7th); edition in parentheses if not first.
- *Chapter in edited volume*: "In F. M. Editor (Ed.),"; book title italicized; pages in parentheses without "pp."
- *Hanging indent*: every entry should use a hanging indent; flag if formatting suggests this is missing.
- *Alphabetization*: by first author last name; multi-author entries by first author then year then second author; same-author same-year disambiguated with a, b, c.

**In-text citation formatting (when audit is requested):**

- Parenthetical: (Author, Year) for one author; (Author1 & Author2, Year) for two; (Author1 et al., Year) for three or more on first and subsequent mentions in APA 7th.
- Narrative: Author (Year) for one; Author and Author (Year) for two; Author et al. (Year) for three or more.
- Multiple citations in same parenthesis: alphabetical, semicolon-separated.
- Page numbers for direct quotes: (Author, Year, p. 47) or (Author, Year, pp. 47–49).
- "et al." formatting: italicized in some style guides, plain in APA — APA 7th is plain.

**Watch out for these cross-cutting style errors regardless of journal:**

- Inconsistent capitalization (sentence case in one entry, title case in another)
- Inconsistent journal name formatting (full name then abbreviated then full again)
- Mixed "&" and "and" in author lists
- Missing volume or issue numbers
- Hyphens used where en-dashes belong (page ranges)
- DOI sometimes present, sometimes absent — flag the inconsistency
- Working papers, dissertations, and book chapters with different formatting conventions inconsistently applied

When reporting style issues, group them: report "12 entries missing DOIs," "5 entries with title case article titles, the rest sentence case," "3 entries with hyphens instead of en-dashes in page ranges" — not 20 separate flags. The user wants the pattern, not a per-entry list.

### Tables

If rendered:
- Variables labeled clearly, not in code-name shorthand (e.g., "ln_emp" should be "Log(Employees)" in the published version).
- Do column headers indicate the model spec?
- Are control variables included or suppressed? (Suppression is common but should be flagged in notes.)
- Are observations and clusters reported in every table?
- Do robustness check tables follow the same column structure as the main table for easy comparison?
- Are correlations reported with sample size?
- Do interaction terms appear in tables, or only in text?
- Do reported coefficients in text match those in tables?
- Are significance stars consistent with reported p-values or standard errors?
- Are Ns consistent across tables, and consistent with text?

If placeholder ([Table N about here]) with no caption:
- Does the methods section describe what should be in this table?
- Does the results text reference findings that imply what the table will show?
- Is the placeholder count consistent with what the methods describe?
- Note as missing; don't critique content that doesn't exist.

If caption-only or skeleton (variable list, no estimates yet):
- Evaluate the caption: is it informative enough to know what's intended?
- Are the variables listed the right ones for the analysis the methods describe?
- Is the model count plausible (e.g., methods says "robustness checks" but no robustness columns are listed)?

### Figures

If rendered:
- Are axes labeled with units?
- Are confidence intervals or standard errors shown?
- Are figure captions informative without requiring the reader to find the figure in the text?
- For interaction plots: are values used for the moderator labeled (e.g., "low = -1 SD")?
- Does each figure earn its space, or is it summarizing a table that's already in the paper?
- Are colors readable in greyscale (top journals often print greyscale)?
- Do the figure's claims match the table results they're visualizing?

If placeholder or absent:
- If a caption exists, evaluate the caption — does it describe a figure that would actually convey the intended point?
- If the prose around a placeholder describes "as Figure 2 shows...", note that the claim depends on a figure that doesn't yet exist; flag the load-bearing nature.
- Don't critique content that doesn't exist.

## Field-specific scans

### Empirical strategy / management papers
- Endogeneity: panel structure exploited? Instruments justified? Selection on observables vs. unobservables?
- Within-firm vs. between-firm variation: which identifies the result? Is it the right one for the theory?
- Does the paper test the theorized mechanism, or only an outcome consistent with the mechanism?
- Mediation analyses: are they done correctly (modern conventions, not Baron & Kenny)?

### OB / micro papers
- Common method bias: addressed?
- Measurement invariance for cross-group comparisons?
- Random effects for nested data structure?
- Are effect sizes reported in standardized form (Cohen's d, η²) where appropriate?
- Were measures pre-registered or developed post-hoc?

### Qualitative papers
- Case selection logic: theoretical sampling justified?
- Data structure (Gioia et al. or equivalent) used appropriately, not as decoration?
- Are quotes representative or cherry-picked?
- Negative cases discussed?
- Member checks, triangulation, or other validity moves reported?

### Theory papers
- Scope conditions specified?
- Boundary conditions vs. moderators distinguished?
- Propositions diagnostic, or definitional?
- Engagement with empirical literature: does the theory address known findings, or hand-wave them?
- Is the theory falsifiable in principle?

### Mixed-methods papers
- Are the qual and quant components actually integrated, or just sequential?
- Does each component address what it's good at, or are they redundant?
- Does the paper claim more than either component alone could support?

## When to break the format

If the paper has a single dominant problem that makes everything else moot — e.g., the construct is fundamentally mismeasured such that no result in the paper means what it claims to mean — say so up front and let everything downstream inherit that framing. Don't pretend the section-by-section sweep matters when the paper needs to be rebuilt. The verdict in Section 1 should reflect this; the rest of the review then says "given this framing problem, here's what the paper currently is and what could survive a rewrite."
