---
name: "jf-writing-style-guide"
description: "JF writing style reference for polishing academic prose and Chinese-to-English translation in Journal of Finance style. Triggers on: JF风格, JF润色, jf-skill, JF写作, JF polish, JF translate. v3.1 adds three-tier AI-fingerprint defense."
metadata:
  version: "3.1.0"
  last_updated: "2026-06-05"
  status: active
  task_type: open-ended
  related_skills: []
---

# JF Writing Style Guide v3.1

Reference for writing and polishing academic finance prose in the Journal of Finance style. Extracted from 144 JF papers (2022--2025). Use for: drafting new sections, polishing drafts, Chinese-to-English translation.

**v3.1** adds a three-tier AI-fingerprint defense (phrase scan, structural audit, quantitative verification), expanded anti-patterns covering structural symmetry, and a comprehensive detection-defense reference (Caveats M-R). Principles adapted from the structure-randomizer and deep-humanize skills.

---

## Quick Start

**Minimal invocation:**
```
jf-skill 请帮我润色这段引言
JF风格 把这段中文摘要翻译成英文
jf-skill polish my results section
```

**Execution flow:**
1. **Diagnose** — Which section of the paper? (Introduction, Results, Conclusion, etc.)
2. **Load references** — Read the relevant reference file(s) for that section
3. **Apply patterns** — Match templates, calibrate hedging, check collocations
4. **Polish** — Iterate, avoiding mechanical substitution
5. **Verify** — Run AI-fingerprint check

---

## Trigger Conditions

### Trigger Keywords

**中文:** JF风格, JF润色, jf-skill, JF写作, JF翻译, JF句型, JF句式, JF用语

**English:** jf-skill, JF polish, JF translate, JF style, JF writing

### When NOT to Use

| Scenario | Use Instead |
|----------|-------------|
| General academic writing (not finance) | General style guide |
| Writing for other journals (JPE, QJE, RFS) | Check target journal conventions |
| Pure grammar/typo fixing | Direct editing |
| Content/structure feedback | Peer review workflow |

---

## Mode Selection

| User Need | Mode | What to Load |
|-----------|------|-------------|
| "润色引言" / "polish introduction" | Introduction polish | `references/sentence-templates.md` §1-5 |
| "润色结果" / "polish results" | Results polish | `references/sentence-templates.md` §9-11; `references/paragraph-patterns.md` §29-33 |
| "翻译摘要" / "translate abstract" | Translation + polish | `references/phrase-bank.md`; `references/usage-guide.md` §Non-Academic table |
| "检查全文写作风格" / "full paper audit" | Full audit | All reference files; focus on AI-fingerprint markers |
| "不知道怎么开头" / "help me open" | Opening brainstorm | `references/sentence-templates.md` §1 |
| "润色结论" / "polish conclusion" | Conclusion polish | `references/sentence-templates.md` §15 |
| "改写段落" / "rewrite paragraph" | Paragraph restructure | `references/paragraph-patterns.md` |

---

## Reference Files Index

| File | Content | When to Load |
|------|---------|-------------|
| `references/sentence-templates.md` | Part A: Opening patterns, research questions, puzzles, gaps, contributions, findings, data, hypotheses, results reporting, economic magnitude, robustness, mechanisms, alternative explanations, limitations, conclusions, roadmaps, identification framing, null results, policy implications | Any section-level writing |
| `references/meta-discourse.md` | Clarifying notes, boundary-setting, interpretive control, layered analysis, narrative scaffolding | When results need careful framing; when preempting misinterpretations |
| `references/phrase-bank.md` | Verb collocations, adjective pairs, adverb combinations, hedging phrases (by certainty level), certainty phrases, logical connectors, model description patterns, non-academic-to-JF alternatives | All polishing and translation |
| `references/paragraph-patterns.md` | 30+ paragraph-level patterns: Claim-Evidence-Interpretation, Gap-Fill, Broad-to-Narrow, Alternative-Explanation, Puzzle-Resolution, Competing-Mechanisms, and more | When structuring or restructuring paragraphs |
| `references/usage-guide.md` | 8-step polishing workflow, appendix quick-reference templates, hedging calibration table, critical caveats A-R (ALL CAPS trap, contribution inflation, AI-fingerprint warnings, em dash overuse, "potentially" dilution, symmetry problem, high-trigger AI patterns, quantitative audit metrics, imperfect writing as defense, section-specific risks, 2-minute pre-submission check) | Before finalizing any polished output |

---

## Core Workflow

### Step 1: Diagnose the Context
Identify what section of the paper the text belongs to, what rhetorical function it serves, and what the user is asking for (polish existing, translate, draft new, restructure).

### Step 2: Load Relevant References
Based on the diagnosis, read the appropriate reference files. Most tasks need only 1--2 references. A full paper audit needs all 5.

### Step 3: Apply Patterns, Not Templates
The patterns in the references are **descriptive** (what JF authors actually do), not **prescriptive** (what you must do). Adapt them to the user's specific argument and evidence. Never copy-paste template sentences verbatim.

### Step 4: Calibrate Hedging
Match claim strength to evidence strength. See the hedging calibration table in `references/usage-guide.md`.
- Speculative: "It is possible that..." / "We cannot rule out..."
- Suggestive: "These results suggest that..." / "This finding is consistent with..."
- Strong: "We find that..." / "Our results show that..."
- Definitive: "We conclude that..." / "Taken together, the evidence indicates that..."

### Step 5: Three-Tier AI-Fingerprint Defense

AI text is statistically detectable: low structural variance, seamless transitions, zero admissions of uncertainty, flat information density. The correct defense is not lexical substitution but structural randomization — break symmetries, inject imperfection, vary every pattern that AI defaults to a mean. The three tiers below escalate from surface markers through structural diagnostics to quantitative thresholds.

---

#### Tier 1: Phrase-Level Scan (12 Markers)

Scan the full text. If any marker hits its threshold, fix mechanically.

| # | Marker | Threshold | Fix |
|---|--------|-----------|-----|
| 1 | "notably" / "importantly" as sentence starters | ≤1 per section | Delete or move mid-sentence |
| 2 | Double quotation marks around technical terms for emphasis | 0 (JF: quotes ONLY for direct quotations or coined terms) | Remove quotes |
| 3 | Em dashes as sentence connectors | 0 (JF: only for parenthetical insertions) | Replace with period or semicolon |
| 4 | "This is because" | ≤1 per paper | "The reason is that..." or state explanation directly |
| 5 | Triple-dot ellipses (...) in body text | 0 (only in direct quotations) | Remove |
| 6 | "potentially" / "arguably" | ≤1 per section | Delete; if claim is uncertain, restate as conditional |
| 7 | Em dashes | ≤1 per paragraph | Reduce; JF average is 1 per 2-3 paragraphs in intro, near-zero in results |
| 8 | Furthermore / Moreover / Additionally / It is worth noting / In conclusion / To summarize | 0 per paper | Delete entirely; these are AI-default connectors that never appear in JF |
| 9 | "shed new light on" / "bridge different strands" / "demystify" / "paint a more complete picture" | ≤2 DISTINCTIVE collocations per paper | If 3+ appear, keep the best 2, rephrase others |
| 10 | "Not X, but Y" or "Not X; it is Y" binary contrast | ≤1 per paper | Break into 2-3 sentences with concrete context |
| 11 | "We hope this work will..." / "We leave this for future work" / "Further investigation is warranted" / "It remains an open question whether..." / "We should be candid about..." | 0 per paper | These 5 hedging phrases are learned by GPTZero; use a specific forward pointer instead ("The next step is to test whether...") |
| 12 | ALL CAPS applied to the paper's own findings | 0 (ALL CAPS only for stylized facts/puzzles) | Move findings to abstract; keep ALL CAPS for genuine broad facts |

---

#### Tier 2: Structural Self-Audit (5 Diagnostic Questions)

Read the full text and answer honestly. "Yes" to 3+ questions means structural rewrite is needed before submission.

1. **How many distinct paragraph templates appear? Does any single template appear more than twice?** If most paragraphs follow claim→evidence→implication, the paper has a structural AI fingerprint. At least 30% of paragraphs should deviate from the dominant template.

2. **Is the Introduction the standard territory→gap→answer→roadmap four-segment structure?** If yes: delete or compress the roadmap to one sentence. Consider merging territory and gap into one paragraph. Let the answer segment be 3-4 sentences, not a full preview of all findings.

3. **Do parallel subsections (e.g., three Results subsections) use the same reporting template?** If yes: vary their structures deliberately. One opens with the result; another opens with the intuition; a third opens with an unexpected finding. Make their lengths unequal — allow one subsection to be 1 paragraph while another is 3.

4. **Are there at least 2 explicit admissions of uncertainty, surprise, or limitation?** If no: add them. Human authors express doubt. Use "We do not yet have a clean explanation for..." or "This was not what we expected" or "Whether this holds beyond [boundary] we have not tested." Distribute uncertainty across different rhetorical types: data-level, mechanism-level, scope-level, and implicit (not using the word "uncertain").

5. **Does the Conclusion recapitulate contributions one by one (numbered re-listing of what the Introduction already promised)?** If yes: rewrite as 1 paragraph stating the core insight (1 sentence) + implication (1 sentence) + open question or concrete prediction (1 sentence). Never restate the contribution checklist.

---

#### Tier 3: Quantitative Verification (5 Metrics)

Compute these metrics on the final text. If any fails, return to the draft.

| Metric | Threshold | Why |
|--------|-----------|-----|
| Sentence length standard deviation | >25 (target >40) | AI produces 15-25 word sentences in a tight bell curve; human writing is multi-modal with ≤8 and ≥35 word sentences coexisting |
| Connector density (however/therefore/thus/hence) | <4 per 1000 words | AI over-uses logical glue; human academic writing relies on implicit transitions |
| Extreme-length paragraph fraction | ≥20% of paragraphs ≤3 sentences or ≥8 sentences | AI defaults to uniform 4-6 sentence paragraphs; humans write 1-sentence transition paragraphs and 10-sentence technical deep-dives |
| Uncertainty expression count | ≥3 distinct admissions of uncertainty per paper | Distributions across at least 2 different rhetorical subtypes (data-level, mechanism-level, scope-level) |
| Dominant template share | No single paragraph template used in >70% of paragraphs | If claim-evidence-implication appears in >70% of paragraphs, the AI default structure dominates |

**Metric calculation reference:**
- Sentence length std dev: Extract all sentences, count words, compute std. If <25, deliberately inject 2-3 extremely short (≤8 word) sentences and 2-3 long (≥30 word) sentences into the densest section.
- Connector density: Grep for "however|therefore|thus|hence|moreover|furthermore|additionally|consequently|accordingly". Divide count by total word count × 1000.
- Extreme paragraph fraction: Count paragraphs with ≤3 sentences; count paragraphs with ≥8 sentences; sum and divide by total paragraph count.

---

## Quality Standards

1. ⚠️ **IRON RULE**: Do not produce sentences a JF editor would flag as AI-generated. Run the fingerprint check every time.
2. ⚠️ **IRON RULE**: Match hedging to evidence strength. Overclaiming damages credibility more than underclaiming.
3. **One paper, not all patterns.** Overusing distinctive collocations ("shed new light on," "bridge different strands," "demystify") in the same paper creates artificiality. Each paper typically uses only 2--4 distinctive patterns.
4. **Journal specificity.** ALL CAPS openings, extensive enumeration, and roadmap paragraphs are JF conventions. Check target journal if not submitting to JF.
5. **Contribution restraint.** "To the best of our knowledge" requires a genuine literature search. "First direct evidence" is used by <5% of published papers.

---

## Anti-Patterns

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **Mechanical template substitution** | Produces formulaic, voice-less prose | Adapt patterns to the specific argument; vary sentence structure |
| 2 | **Over-hedging every claim** | Makes the paper sound uncertain about everything | Reserve hedging for genuinely uncertain claims; use confident phrasing for well-supported findings |
| 3 | **ALL CAPS for narrow/obvious claims** | Weakens the impact of the opening; looks pretentious | ALL CAPS only for broad, genuinely striking stylized facts |
| 4 | **"Battery of robustness checks" without specifics** | Boilerplate that signals laziness | Name specific test types (falsification, placebo, external validity); explain WHY each matters |
| 5 | **Using 5+ distinctive collocations in one paper** | Reads as AI-generated or trying too hard | Limit to 2--4 distinctive patterns per paper |
| 6 | **"We contribute to three strands..." without differentiation** | Formulaic and forgettable | Explain what is NEW about each contribution, not just that it exists |
| 7 | **ALL CAPS for your own findings** | Findings go in the abstract, not as ALL CAPS opening | ALL CAPS openings are for stylized facts/puzzles, not your results |
| 8 | **Mechanical translation word-by-word** | Produces unnatural English that no JF author would write | Translate the meaning and rhetorical function, not the words; then apply JF patterns |
| 9 | **"Not X, but Y" binary contrasts** | AI's favorite clean structure: precise opposition with zero hesitation. GPTZero recognizes this as a high-confidence pattern. | Break into 2-3 sentences with concrete context. For example: "BM's problem isn't numerical imprecision — factor-of-2 errors are acceptable experimentally. The deeper issue is that it claims something doesn't exist, when it does. In device design, this existence-blindness outweighs any numerical error." |
| 10 | **Rhetorical question immediately self-answered** | "What distinguishes these three regimes? The answer lies in..." — AI's default explanatory opener. Question too precise, answer too immediate. | Either (a) open with assertion instead of question, or (b) delay the answer by 2-3 sentences with a caveat or historical context first. |
| 11 | **Symmetric parallel lists (equal-length items)** | "Star: [description+conclusion]. Cyclic: [description+conclusion]. Chain: [description+conclusion]." Detection algorithms measure cosine similarity across list items; equal structure = >0.9 similarity → flagged. | Make list items deliberately unequal: one item 1 sentence, another 3 sentences; one opens with a citation, another opens with a result. Allow the paper's focal case to be detailed while others are briefly noted. |
| 12 | **"Below X, Y happens. Above X, Z happens" symmetric threshold** | AI's default template for describing phase transitions or regime changes. Two perfectly symmetric sentences. | Break symmetry — detail only the empirically rich side. Mention the other side in a half-sentence or parenthetical. |
| 13 | **Evaluation → Exhaustive list → Significance (three-beat summary)** | "The result is strikingly general. It holds for all N, all temperatures, all spacings, and all spectral densities. Any nonzero ergotropy is necessarily a beyond-BM effect." AI's perfect three-part cadence: evaluate, enumerate, declare significance. | (a) Replace "all X, all Y, all Z" with "regardless of parameters" or the single most surprising member of the set. (b) Merge evaluation and significance into one sentence. (c) Or reverse order: significance first, then scope. |
| 14 | **Every paragraph follows the same structural template** | If all paragraphs are claim→evidence→implication, detection algorithms measure low structural entropy → flagged. Humans vary paragraph structure unconsciously. | Target: no single template appears in >70% of paragraphs. At least 30% of paragraphs should deviate from the dominant template. Deliberately use abrupt-end, evidence-first, or causal-chain structures for some paragraphs. |
| 15 | **Perfect transitions between every section and paragraph** | AI writes seamless logical flow. Humans skip transitions, jump topics, leave gaps. Zero logical breaks = AI fingerprint. | Deliberately insert 2-4 "logic breaks" in the paper where the next paragraph opens without any transitional sentence from the previous one. Distribute across section boundaries. |

---

## Caveats

Before every use, keep these in mind:

1. **This is a reference, not a recipe.** The patterns are what JF authors actually do; your paper has its own voice and argument. Use the skill to diagnose what's missing, not to replace your judgment.

2. **Variation matters.** A paper that uses every pattern from this skill will read as mechanical. Each real JF paper deploys only a subset.

3. **Check your target journal.** ALL CAPS openings, extensive enumeration, and "The remainder of the paper is organized as follows" are common in JF but may be inappropriate for JPE, QJE, or Econometrica.

4. **The best JF writing is invisible.** The goal is not to show off how many templates you've mastered — it's to make your argument clear, precise, and persuasive.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.1.0 | 2026-06-05 | Three-tier AI-fingerprint defense: upgraded Step 5 from 7-item scan to 12-marker phrase scan + 5-question structural audit + 5-metric quantitative verification. Expanded anti-patterns from 8 to 15 entries (symmetry patterns 9-15 from structure-randomizer/deep-humanize). Added Caveats M-R to usage-guide.md covering: symmetry problem, high-trigger patterns with fixes, quantitative audit metrics, imperfect writing as defense, section-specific risks, 2-minute pre-submission check. |
| 3.0.0 | 2026-06-05 | Ground-up modular rewrite. Split ~2000-line monolithic SKILL.md into orchestrator + 5 reference files. Added trigger conditions table, mode selection guide, anti-patterns table, AI-fingerprint quality standards. |
| 2.x | 2026-06-04 | Round 4 additions (Sections 62-90), AI-fingerprint warnings, caveats J-L |
| 2.x | 2026-06-03 | Round 3 quality audit, caveats A-I |
| 1.x | 2026-05 | Initial creation from 124 JF papers |

---

*Synthesized from 144 Journal of Finance papers (2022--2025). All examples verbatim from published JF articles.*
