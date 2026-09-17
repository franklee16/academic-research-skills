# JF Writing Style Guide: Essential Usage Guide

*Consolidated from the master SKILL.md (124 JF papers, 2022--2025, updated 2026-06-04).*

---

## Table of Contents

1. Polishing Workflow (8 Steps)
2. Appendix: Quick-Reference Templates
   - Introduction Template
   - Results Paragraph Template
   - Conclusion Template
   - Alternative Explanation Template
   - Concern-Response Pairing Template
   - Meta-Reflexive and Clarifying Templates
   - Hedging Calibration Table
3. Critical Caveats and Usage Notes
   - A: This Skill Is a Reference, Not a Recipe
   - B: Journal Specificity Warning
   - C: The ALL CAPS Trap
   - D: Variation Within a Single Paper
   - E: The "Battery of Robustness Checks" Concern
   - F: Contribution Inflation
   - G: The Peril of Overly Comprehensive Templates
   - H: Confidence Calibration for Contribution Claims
   - I: Reflection and Quality Audit
   - J: Em Dash Overuse Warning
   - K: "Potentially" and "Arguably" Dilution
   - L: AI-Fingerprint Warning: Quotation Marks and Dashes
   - M: The Symmetry Problem — Why Lexical Substitution Alone Fails
   - N: High-Trigger AI Patterns and Their Fixes (Finance-Specific)
   - O: Quantitative Self-Audit Metrics
   - P: Imperfect Writing as AI Defense
   - Q: Section-Specific AI Risks for Finance Papers
   - R: Two-Minute Pre-Submission Check

---

# 1. Polishing Workflow (8 Steps)

**Step 1: Diagnose** -- Which section are you writing? Match to Sections 1-21 of the master guide.

**Step 2: Draft using templates** -- Introductions: "A LARGE LITERATURE... Yet... In this paper, we..." (Sections 1-5). Consider alternative openings: historical arc, two-concurrent-trends, rhetorical-question-answer, concrete anecdote, historical legislation, challenge-conventional-view, functional-role, definition-then-importance, revolutionary-change, post-crisis-era, expectation-before-contradiction. Results: Claim-Evidence-Interpretation. Conclusions: punchline opening, summary, implications, numbered-specific-questions, bounded-effect.

**Step 3: Calibrate hedging** (Section 25 of master guide) -- Speculative: "may," "it is possible that." Well-supported: "we find that." JF convention: even strong claims use "suggest that" not "prove."

**Step 4: Add connectors** (Section 27 of master guide) -- However, Moreover, Thus, First... Second... Also: "A clarifying note about... is in order," "This evidence should not be construed as suggesting that," "To put the numbers in perspective."

**Step 5: Check collocations** (Sections 22-24 of master guide) -- Replace non-academic phrases (see Section 57 of master guide).

**Step 6: Structure paragraphs** (Sections 29-55 of master guide) -- Match paragraph type to writing function: Results (Claim-Evidence-Interpretation), Introductions (Gap-Fill, Broad-to-Narrow, Puzzle-Resolution, Middle-Way Compromise), Mechanisms (Competing-Mechanisms, Two-Effects, Layered-Explanation, Necessary-Interplay), Robustness (Concern-Response, Self-Critique-Defense, Meta-Reflexive), Discussion (Implication-Cascade, Generalizability, Dual-Interpretation, Theory-Testing, Indistinguishability-Then-Pivot), Data (Vivid-Data-Showcase, Taxonomy-Enumeration), Narrative (Peel-the-Onion, Parameter-Mapping, Intractability-Pivot, Results-Unification), New (Expectation-Then-Contradiction).

**Step 7: Write roadmap** (Section 16 of master guide) -- "The remainder of the paper is organized as follows."

**Step 8: Polish conclusion** (Section 15 of master guide) -- Consider punchline opening, findings summary, implication cascade, numbered-specific-questions, limits, and future work.

---

# 2. Appendix: Quick-Reference Templates

## Introduction Template

```
[ALL CAPS HOOK -- broad claim or stylized fact].
[Alternative openings: Historical arc, Two-concurrent-trends, Rhetorical-question-answer,
 Concrete anecdote (specific date + named actors), Historical legislation,
 Challenge-conventional-view, Functional-role, Definition-then-importance,
 Revolutionary-change, Two-observations-enumeration, Post-crisis-era,
 or Expectation-before-contradiction].
[Context -- prior literature or real-world importance].
[PUZZLE or GAP -- "Yet/However, little is known about..." or "This leads to a puzzle..."
  or "These two facts point to an important gap: why...?"
  or Theory-supported-expectation-then-contradiction].
[THIS PAPER -- "In this paper, we [study/examine/investigate]..." or
  "This paper is devoted to establishing that..." or
  "We find a middle way between trade-offs in existing studies..." or
  "In this paper, we ask whether [phenomenon] also exists within [new domain]..."].
[RESEARCH IMPORTANCE (optional) -- "Studying such questions is important because..."].
[FINDINGS PREVIEW -- "We find that... Our results show that..."].
[CONTRIBUTION -- "Our paper contributes to the literature on..." or "We make [N] contributions."
  or "These findings are significant because they represent the first direct evidence that..."].
[ROADMAP -- "The remainder of the paper is organized as follows."].
```

## Results Paragraph Template

```
[TOPIC SENTENCE -- the claim].
[EVIDENCE -- "Table X presents the results. Column (1) shows that..."].
[COEFFICIENT INTERPRETATION].
[ECONOMIC MAGNITUDE -- "A one-standard-deviation increase in X is associated with Y% change"].
[Optional: "This relatively small average masks substantial heterogeneity..."].
[Optional: "The estimates are always negative but generally statistically insignificant"].
[CONSISTENCY -- "These results are consistent with..."].
```

## Conclusion Template

```
[PUNCHLINE (optional) -- "Cash flow matters."].
[RESTATE -- "In this paper, we [studied/examined]..."].
[SUMMARIZE FINDINGS -- "We find that..."].
[TAKEAWAY -- "Taken together, our results suggest that..."].
[IMPLICATIONS -- "An important implication... A related implication..."].
[LIMITATION -- "One caveat of our analysis is that..."].
[FUTURE WORK -- "We leave two questions for future research. First... Second..."].
```

## Alternative Explanation Template

```
[STATE -- "One potential concern is that..." or "A first-order concern is whether..."].
[TEST -- "To address this concern, we..."].
[RESULT -- "We find that..." / "The coefficient is insignificant"].
[REJECTION -- "Thus, this alternative explanation is unlikely to drive our results."].
```

## Concern-Response Pairing Template

```
[FRAMING -- "A simple comparison raises two main concerns."].
[CONCERN 1 -- "First, [concern]. We attempt to assuage this concern by [response]."].
[CONCERN 2 -- "Second, [concern]. We address this concern by [response]."].
```

## Meta-Reflexive and Clarifying Templates

```
Clarifying Note:
[SIGNAL -- "A clarifying note about [X] is in order."].
[CORRECTION -- "[X] is distinct from [Y]..."].
[CONTRIBUTION -- "Our contribution is to show that [actual claim]."].

Should Not Be Construed:
[FINDING -- "[Finding]."].
[NEGATION -- "This evidence should not be construed as suggesting that [extreme interpretation]."].
[BALANCED -- "A more balanced and measured interpretation is that [nuanced claim]."].

Dual Interpretation:
[FINDINGS -- "The findings can be interpreted in two ways."].
[INTERP A -- "First,..."].
[INTERP B -- "Alternatively,..."].
[BOTTOM LINE -- "Regardless, [what holds under either interpretation]."].

Middle Way:
[SETUP -- "We find a middle way between trade-offs in existing studies: [A] versus [B]."].
[POLE A -- "[Paper A] does [strength]... but [weakness]..."].
[POLE B -- "[Paper B] does [strength]... but [weakness]..."].
[SYNTHESIS -- The paper combines the strengths of both.].

Expectation-Then-Contradiction:
[INTUITION -- "One might expect that when [X], [Y] should improve."].
[THEORY SUPPORT -- "There are [N] compelling reasons from economic theory to support these expectations. First... Second..."].
[CONTRADICTION -- "Yet, research on '[Z]' suggests that [contrary evidence]."].

Necessary-Interplay:
[SINGLE NEGATION -- "It should be stressed that [X] alone cannot explain our results."].
[INTERPLAY -- "It is the interplay between [X] and [Y] that is necessary."].
[ELABORATION -- "[X] is present in standard settings. Yet... This is not necessarily true in our setting."].

Indistinguishability-Then-Pivot:
[ACKNOWLEDGMENT -- "The remaining two hypotheses, [A] and [B], are impossible to distinguish."].
[PIVOT -- "We can, however, ask whether [testable implication]."].
[RESULT -- Report findings on the testable implication.].
```

## Hedging Calibration

| Claim Strength | Typical Phrasing |
|---|---|
| Speculative | "It is possible that... / This could reflect... / We cannot rule out..." |
| Suggestive | "These results suggest that... / This finding is consistent with..." |
| Strong | "We find that... / Our results show that... / We establish that..." |
| Definitive | "We conclude that... / Taken together, the evidence indicates that..." |
| Model-based | "Our estimates imply that... / The model parameter estimates imply that..." |
| Null result | "The evidence does not support the hypothesis that... / an extremely tight interval around zero" |
| Mixed evidence | "Overall, the picture is mixed." |
| Interpretive boundary | "This evidence should not be construed as suggesting that..." |

---

# 3. Critical Caveats and Usage Notes

## A. This Skill Is a Reference, Not a Recipe

The patterns documented here are **descriptive** (what JF authors actually do), not **prescriptive** (what you must do). The skill catalogs the writing conventions of one specific journal. Using these templates mechanically will produce formulaic, voice-less prose. The goal is to internalize the patterns and deploy them flexibly, not to copy-paste.

**Key principle:** Use this skill to diagnose what is missing from your draft and to see how published authors handled a similar rhetorical situation. Never use it to replace your own judgment about what your paper needs.

## B. Journal Specificity Warning

Several conventions documented here are specific to the Journal of Finance and may be inappropriate for other journals:

- **ALL CAPS openings:** Common in JF but rare in many other top journals (e.g., JPE, QJE, Econometrica often use different conventions). Check your target journal's recent issues before adopting ALL CAPS.
- **"The remainder of the paper is organized as follows":** Nearly universal in JF but some journals prefer "The paper proceeds as follows" or omit the roadmap paragraph entirely.
- **Extensive verbal enumeration ("We present six findings. First... Second... Sixth...") :** JF allows long enumerations; some journals prefer tighter introductions with fewer enumerated items.

**Key principle:** Always check 3-5 recent papers in your target journal before finalizing your opening conventions.

## C. The ALL CAPS Trap

ALL CAPS openings in JF serve a specific function: they signal a broad, stylized fact or provocative question. Do NOT use ALL CAPS for:
- Narrow methodological statements
- Your own findings (these go in the abstract, not the opening sentence)
- Sentences that are not genuinely attention-grabbing

A poorly chosen ALL CAPS opening is worse than no ALL CAPS opening at all. If your opening fact is not genuinely surprising or important, use a different opening style.

## D. Variation Within a Single Paper

This skill documents many patterns, but a single paper should NOT use all of them. Overusing distinctive collocations like "shed new light on," "bridge different strands," "demystify," or "paint a more complete picture" in the same paper creates an impression of artificiality. Each paper typically uses only 2-4 of the more distinctive patterns.

**Key principle:** After drafting, scan for repeated distinctive phrases or patterns. If you find the same pattern appearing 3+ times, vary at least one of them.

## E. The "Battery of Robustness Checks" Concern

"We perform a battery of robustness checks" is so common in JF that it has become nearly obligatory. However, the best JF papers go beyond this boilerplate by:
- Naming specific test types (falsification test, external validity test, placebo test)
- Explaining WHY each test matters for identification
- Using "concern-response pairing" (Section 48 of master guide) instead of a generic list

If your robustness section can be summarized as "we did a battery and everything is fine," you are not meeting JF standards for transparency.

## F. Contribution Inflation

The skill documents many contribution-framing verbs (demystify, bridge, augment, shed new light on, propose a proxy for). These are variants observed across 84 papers; no single paper uses more than 2-3 of them. Overclaiming contribution -- especially through primacy claims without adequate qualification -- is a common pitfall. "To the best of our knowledge" is the standard qualifier, but it should be used only when you have genuinely searched the literature.

## G. The Peril of Overly Comprehensive Templates

The appendix templates (Introduction Template, Results Paragraph Template, etc.) are emergency scaffolds for when you are stuck. They are NOT aspirational models of what a full paper should look like. Real JF papers vary considerably from these templates in detail, length, and structure. If your paper exactly matches every template, it will read as mechanical.

## H. Confidence Calibration for Contribution Claims

Several contribution patterns documented here carry unusually strong epistemic commitment: "That is exactly what we provide" (Section 5, item 24 in master guide), "The key theoretical result of our paper is that..." (Section 28 in master guide), and "represent the first direct evidence that..." (Section 5, item 21 in master guide). These are genuine JF patterns but are used by fewer than 5% of published papers. They require:

- **"Exactly what we provide"**: Only when the paper addresses every single item in a previously stated list of limitations. If even one item is not addressed, use a more qualified statement.
- **"The key theoretical result"**: Only when the paper has a single, clearly dominant theoretical contribution. Papers with multiple equally important results should not designate one as "the key."
- **"First direct evidence"**: Requires a genuine literature search confirming no prior direct test exists. If prior indirect or suggestive evidence exists, qualify as "the first direct test" rather than "the first evidence."

**Key principle:** When in doubt, use a more qualified formulation. Overclaiming is more damaging to credibility than underclaiming.

## I. Reflection and Quality Audit

The following issues were identified during a systematic self-review of the skill and corrected:

**1. Over-reliance on ALL CAPS openings:** The skill documents 26+ opening styles, but 12 of them use ALL CAPS. This overrepresents ALL CAPS relative to actual JF practice -- many JF papers (especially those in corporate finance and banking) use lowercase openings. The skill now explicitly notes this in Caveat C.

**2. Missing "negative result" templates:** JF papers increasingly publish papers whose main finding is a null or negative result (e.g., "the evidence does not support the hypothesis that..."). The skill had some coverage (Section 18 of master guide) but the templates in Section 57 did not include a Null Result template.

**3. "It turns out that" should be flagged as informal:** While "it turns out that" appears in published JF papers, it is more conversational than the skill's other phrases and could undermine the gravitas of a formal paper if overused. A usage note was added explicitly stating "Use sparingly for genuinely surprising connections."

**4. Some collocations are field-specific, not general JF:** Terms like "sufficient statistics" (public economics), "commitment device" (contract theory), and "generically optimal" (theory) are standard in their subfields but may be jarring if used in empirical corporate finance papers. Subfield labels were added to these terms in Sections 22-24 so users can assess relevance to their own paper.

**5. The Non-Academic to JF table (Section 57 of master guide) could encourage mechanical substitution:** If a user simply replaces "We can't answer X" with the JF alternative, the result may sound stilted. The table now comes with a stronger warning: "These are directional guides, not mechanical substitutions. Always adapt to your specific context -- the JF alternative may need modification to fit your sentence structure."

**6. The skill lacks a trigger condition:** Users need an easy way to invoke the skill. A trigger condition was added to the frontmatter: the skill should be activated when the user's prompt contains "jf-skill".

## J. Em Dash Overuse Warning

JF papers frequently use em dashes (--) for parenthetical explanations and definitions (e.g., "MULTIDIVISION FIRMS--THAT IS, FIRMS that operate two or more divisions--play an important role"). However, AI-assisted writing tends to overuse em dashes to the point where every paragraph contains one. In published JF papers, em dashes appear roughly once every 2-3 paragraphs in the introduction and virtually never in the results section. **Rule of thumb:** If your draft has more than one em dash per paragraph, reduce. Substitute commas, parentheses, or separate sentences where possible.

## K. "Potentially" and "Arguably" Dilution

The skill documents several hedging phrases using "potentially" and "arguably" (e.g., "a potentially more important reason," "arguably be discerned," "plausibly bound the magnitude"). These are genuine JF patterns but are used sparingly -- typically once per paper. When AI models deploy these hedges, they often scatter "potentially" throughout the text, making every claim sound uncertain. **Rule of thumb:** Use "potentially" or "arguably" at most once per section. If you find yourself hedging every claim, your argument lacks conviction; either strengthen the evidence or make a clear conditional claim instead.

## M. The Symmetry Problem: Why Lexical Substitution Alone Fails

AI detection tools (GPTZero, Turnitin, Originality.ai) do not primarily scan for specific words. They measure statistical patterns: sentence-length distributions, paragraph-structure entropy, transition density, and information-density variance. The fundamental AI fingerprint is **structural symmetry** — everything converging toward a mean.

A paper that fixes words but leaves structure intact will still be flagged. The correct defense operates at the structural level:

- **Sentence-length variance**: Human writing has multi-modal sentence-length distributions (5-word fragments coexist with 40-word technical sentences). AI produces a tight bell curve centered at 15-25 words. Target: standard deviation >25 words, ideally >40.
- **Paragraph-template entropy**: Humans vary paragraph structure unconsciously. AI defaults to claim→evidence→implication for nearly every paragraph. Detection algorithms measure template repetition; low entropy = flagged. Target: no single template in >70% of paragraphs.
- **Information-density fluctuation**: Human paragraphs range from 40% to 85% information density (some paragraphs are mostly transition/context, others are dense with technical content). AI paragraphs cluster at 65-75%. Target: at least 20% of paragraphs should be "low density" (transition, context, meta-commentary).
- **Transition imperfection**: Humans skip transitions, jump topics, leave logical gaps. AI writes seamless flow. Target: 2-4 deliberate "logic breaks" where a paragraph opens without any transition from the previous one.

**Why this matters for JF papers specifically**: Finance papers are template-heavy by convention (roadmap paragraphs, claim-evidence-implication results, concern-response robustness sections). This makes them MORE vulnerable to AI detection, not less — because the templates themselves resemble AI defaults. A JF paper that follows its own conventions too perfectly will read as AI-generated to both detection algorithms and experienced readers.

## N. High-Trigger AI Patterns and Their Fixes (Finance-Specific)

The following 5 patterns are high-confidence AI markers based on real detection feedback. Each comes with a fix that preserves the academic function while breaking the statistical signature.

### Pattern 1: The Clean Binary Contrast
**What triggers**: "This is not a quantitative error. It is a qualitative blind spot — the most severe type of problem." Precise opposition + escalating judgment + zero qualification. AI loves this structure.
**Fix**: Break into 2-3 sentences with concrete anchoring. Add a qualifier or specific example. "The issue isn't numerical imprecision — a factor-of-two error is within experimental tolerance. What matters is that the model claims something doesn't exist when it does. For [specific application], this qualitative failure matters more than any quantitative one."

### Pattern 2: The Rhetorical Question + Perfect Answer
**What triggers**: "What explains this pattern? The answer lies in how information propagates between markets." Question too well-formed, answer too immediate.
**Fix**: Either (a) open with an assertion instead, or (b) delay the answer by 2-3 sentences with context, caveats, or historical precedent. "The classification we propose hinges on information propagation — though mixed cases (part chain, part star) remain unclassified."

### Pattern 3: The Symmetric Threshold Description
**What triggers**: "Below α≈0.3, nothing happens. Above that threshold, the effect increases roughly linearly." Two perfectly symmetric sentences describing two sides of a threshold.
**Fix**: Detail only the empirically rich side. Mention the other side in a subordinate clause. "The onset is near α≈0.3. Growth beyond that point is roughly linear with coupling, reaching [value] at α=1.5."

### Pattern 4: The Equal-Length Symmetric List
**What triggers**: Three (or N) items, each described in structurally identical sentences of similar length. Detection tools compute cosine similarity across items; >0.9 = flagged.
**Fix**: Deliberately unequal treatment. Make the focal case 3 sentences long and the peripheral case 1 sentence. Vary openings: one starts with a citation, another with a result, a third with a caveat. "While evidence for [A] is limited to [specific context]... [B], by contrast, appears robust across [broad range], as shown by [citation] and confirmed in our Table [X]. [C] we note only briefly, since it follows from [B] under [condition]."

### Pattern 5: The Three-Beat Summary (Evaluate → Enumerate → Declare)
**What triggers**: "The result is strikingly general. It holds for all N, all T, all specifications. Any observed effect is necessarily a beyond-standard-model phenomenon." Three sentences, each doing exactly one job: evaluation, scope, significance. AI's default conclusion cadence.
**Fix**: (a) Replace "all X, all Y, all Z" with the single most surprising member of the set or "regardless of parameters." (b) Merge evaluation and significance into one sentence. (c) Add a caveat that breaks the perfect arc. "This holds regardless of parameter choices — including, for instance, [surprising edge case]. What this means is [significance], though we caution that [boundary condition]."

## O. Quantitative Self-Audit Metrics

Before submitting, compute these five numbers. If any fails its threshold, revise the text — not by swapping words, but by restructuring paragraphs.

| # | Metric | How to Compute | Threshold | If Failing |
|---|--------|---------------|-----------|------------|
| 1 | Sentence-length standard deviation | Extract all sentences; count words per sentence; compute population std dev | >25 words | Inject 2-3 extremely short sentences (≤8 words) and 2-3 long sentences (≥30 words) into the section with the tightest sentence-length band |
| 2 | Connector density | Count occurrences of however/therefore/thus/hence/moreover/furthermore/additionally/consequently/accordingly; divide by total words × 1000 | <4 per 1000 words | Delete the weakest 50% of connectors; replace with implicit transitions or em-dash insertions |
| 3 | Extreme-paragraph fraction | Count paragraphs with ≤3 sentences; count paragraphs with ≥8 sentences; sum both; divide by total paragraph count | >20% | Split one long uniform paragraph into 1-sentence transition + remaining body; merge two short uniform paragraphs into one varied paragraph |
| 4 | Uncertainty expression count | Count sentences that admit doubt, limitation, surprise, or agnosticism (any phrasing) | ≥3 in the paper, across ≥2 different rhetorical subtypes | Add one data-level caveat ("sample size limits..."), one mechanism-level doubt ("we cannot explain why..."), one scope-level boundary ("whether this holds beyond... we have not tested") |
| 5 | Template dominance ratio | Classify each paragraph into its primary structural template (claim-evidence, gap-fill, causal-chain, abrupt-end, etc.); compute share of most common template | <70% | Identify 2-3 paragraphs where the dominant template can be replaced: change a claim-evidence paragraph to evidence-first; change a gap-fill paragraph to abrupt-end |

**Important**: These metrics are diagnostic, not aspirational. A paper that deliberately targets the threshold values will overcorrect and look artificial. The goal is to catch papers that have drifted too far toward AI-default values and nudge them back into the human range.

## P. Imperfect Writing as AI Defense

Counterintuitively, some forms of "bad" writing are protective against AI detection:

- **Redundancy**: Humans repeat themselves in slightly different words. AI is efficient. Allow 1-2 sentences per section that restate a point already made, using different phrasing.
- **Asymmetric treatment**: Humans don't give equal space to equal topics. A Results section with three findings might have one finding spanning 3 paragraphs and another finding covered in 2 sentences. This is correct — it signals judgment about relative importance.
- **Incomplete enumeration**: Humans say "temperatures" when AI says "temperatures, spacings, densities, and spectral functions." Deliberately use summary terms instead of exhaustive lists — at least in the body text (exhaustive lists belong in tables and the Appendix).
- **Occasional abruptness**: A paragraph that ends without a summary sentence. A section that opens without a transition from the previous section. A claim stated without the usual "We find that" preamble. These imperfections are human.
- **Genuine uncertainty**: AI papers sound confident about everything. Human papers have moments of honest doubt. "We do not yet have a clean explanation for..." is more protective against detection than any synonym substitution.

**Rule**: Target 2-4 deliberate "imperfections" per 5000 words. More than that reads as sloppy; fewer than that reads as AI.

## Q. Section-Specific AI Risks for Finance Papers

Different sections have different AI fingerprint risks. Here are the highest-risk locations and what to check:

| Section | Highest AI Risk | Fix |
|---------|----------------|-----|
| **Introduction** | Territory→Gap→Answer→Roadmap four-segment symmetry; roadmap paragraph with "First... Second... Third... Fourth..." | Delete or compress roadmap to one sentence; merge territory and gap into one paragraph; make answer segment 3-4 sentences, not a full preview |
| **Literature Review** | "Our paper contributes to three strands..." followed by equal-length summaries of each strand | Make strand treatments deliberately unequal; the paper's core strand gets 2 paragraphs, peripheral strands get 2 sentences each |
| **Results (subsections)** | Each subsection uses the identical reporting template (topic sentence → table reference → coefficient → economic magnitude → consistency check) | Vary subsection openings: one opens with the result, another with the intuition, a third with a counterintuitive finding. Allow subsection lengths to vary by factor of 3 |
| **Robustness** | "Battery of robustness checks" + generic list of tests + "results are robust" | Name specific test types (falsification, placebo, external validity); explain WHY each matters; allow one test to show mixed results |
| **Discussion** | Perfect coverage of "significance → limitations → future work" + "Not X but Y" binary contrasts | Open with a concrete experimental scenario, not an abstract evaluation; include at least one speculative connection to an adjacent field; use at least two different types of uncertainty language |
| **Conclusion** | Numbered re-listing of contributions matching the Introduction's preview | One paragraph: core insight (1 sentence) + implication (1 sentence) + open question or concrete prediction (1 sentence) |
| **Abstract** | "We find that... We show that... We document that..." uniform sentence openings | Vary sentence openings; include one sentence that admits a boundary condition or limitation |

## R. Two-Minute Pre-Submission Check

If you have no time for a full audit, check only these five highest-leverage positions (they contribute the most to detection scores):

1. **Introduction's last paragraph** — Is it a mechanical "This paper makes three contributions..." list? If yes, rewrite.
2. **Discussion's first paragraph** — Does it open with a clean binary contrast ("Not X, but Y") or a rhetorical question? If yes, restructure.
3. **Discussion's last paragraph** — Does it end with "We leave this for future work" or "Further investigation is warranted"? If yes, replace with a specific open question.
4. **Conclusion** — Is it a numbered re-listing of contributions? If yes, compress to 3 sentences.
5. **The longest Results subsection** — Does it follow the standard claim→evidence→interpretation template for every paragraph? If yes, vary the structure of at least one paragraph.

---

*Consolidated from the JF Writing Style Guide master SKILL.md (124 Journal of Finance papers, 2022--2025). Caveats A-I added 2026-06-03 following critical self-reflection on the skill's scope and potential for misuse. Caveats J-L added 2026-06-04 following Round 4 quality review and AI-fingerprint testing. Caveats M-R added 2026-06-05: three-tier AI detection defense (phrase scan, structural audit, quantitative verification), high-trigger patterns with finance-specific fixes, imperfect-writing-as-defense principle, section-specific risk table, and 2-minute pre-submission check. Principles adapted from structure-randomizer (structural variance as detection countermeasure) and deep-humanize (detection models' statistical dimensions).*
