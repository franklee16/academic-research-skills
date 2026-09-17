---
name: "jf-writing-style-guide"
description: "JF writing style reference for polishing academic prose and Chinese-to-English translation in Journal of Finance style. Triggers on: JF风格, JF润色, jf-skill, JF写作, JF polish, JF translate."
metadata:
  version: "3.0.0"
  last_updated: "2026-06-05"
  status: active
  task_type: open-ended
  related_skills: []
---

# JF Writing Style Guide v3.0

Reference for writing and polishing academic finance prose in the Journal of Finance style. Extracted from 144 JF papers (2022--2025). Use for: drafting new sections, polishing drafts, Chinese-to-English translation.

**v3.0** is a ground-up rewrite of the original ~2000-line monolithic SKILL.md. All reference material is now inline in this single file — no external references directory needed.

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
2. **Locate section** — Jump to the relevant inline section (sentence templates, paragraph patterns, phrase bank, meta-discourse, or usage guide)
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
| "润色引言" / "polish introduction" | Introduction polish | Sentence templates §1-5 (inline) |
| "润色结果" / "polish results" | Results polish | Sentence templates §9-11; Paragraph patterns §29-33 (inline) |
| "翻译摘要" / "translate abstract" | Translation + polish | Phrase bank; Usage guide Non-Academic table (inline) |
| "检查全文写作风格" / "full paper audit" | Full audit | All inline sections; focus on AI-fingerprint markers |
| "不知道怎么开头" / "help me open" | Opening brainstorm | Sentence templates §1 (inline) |
| "润色结论" / "polish conclusion" | Conclusion polish | Sentence templates §15 (inline) |
| "改写段落" / "rewrite paragraph" | Paragraph restructure | Paragraph patterns (inline) |

---

## Inline Reference Sections

All reference material is included inline below — no files to load separately.
See the following sections within this document:

| Section | Content | When to Reference |
|---------|---------|-------------------|
| Sentence Templates (below) | Opening patterns, research questions, puzzles, gaps, contributions, findings, data, hypotheses, results reporting, economic magnitude, robustness, mechanisms, alternative explanations, limitations, conclusions, roadmaps, identification framing, null results, policy implications | Any section-level writing |
| Meta-Discourse (below) | Clarifying notes, boundary-setting, interpretive control, layered analysis, narrative scaffolding | When results need careful framing; when preempting misinterpretations |
| Phrase Bank (below) | Verb collocations, adjective pairs, adverb combinations, hedging phrases (by certainty level), certainty phrases, logical connectors, model description patterns, non-academic-to-JF alternatives | All polishing and translation |
| Paragraph Patterns (below) | 30+ paragraph-level patterns: Claim-Evidence-Interpretation, Gap-Fill, Broad-to-Narrow, Alternative-Explanation, Puzzle-Resolution, Competing-Mechanisms, and more | When structuring or restructuring paragraphs |
| Usage Guide (below) | 8-step polishing workflow, appendix quick-reference templates, hedging calibration table, critical caveats (ALL CAPS trap, contribution inflation, AI-fingerprint warnings, em dash overuse, "potentially" dilution) | Before finalizing any polished output |

---

## Core Workflow

### Step 1: Diagnose the Context
Identify what section of the paper the text belongs to, what rhetorical function it serves, and what the user is asking for (polish existing, translate, draft new, restructure).

### Step 2: Load Relevant References
Based on the diagnosis, jump to the appropriate inline reference section below. Most tasks need only 1--2 sections (e.g., sentence templates + phrase bank). A full paper audit needs all 5.

### Step 3: Apply Patterns, Not Templates
The patterns in the references are **descriptive** (what JF authors actually do), not **prescriptive** (what you must do). Adapt them to the user's specific argument and evidence. Never copy-paste template sentences verbatim.

### Step 4: Calibrate Hedging
Match claim strength to evidence strength. See the hedging calibration table in the Usage Guide section below.
- Speculative: "It is possible that..." / "We cannot rule out..."
- Suggestive: "These results suggest that..." / "This finding is consistent with..."
- Strong: "We find that..." / "Our results show that..."
- Definitive: "We conclude that..." / "Taken together, the evidence indicates that..."

### Step 5: Run AI-Fingerprint Check
After polishing, scan for these markers that NEVER appear in published JF papers:
1. **"notably" / "importantly"** as sentence starters — use at most once per section
2. **Double quotation marks** around technical terms for emphasis — JF uses quotes ONLY for direct quotations or coined terms
3. **Em dashes as sentence connectors** — JF uses em dashes for parenthetical insertions only, not as sentence joiners
4. **"This is because"** — JF prefers "The reason is that..." or stating the explanation directly
5. **Triple-dot ellipses** in body text — these appear only in direct quotations
6. **"potentially" / "arguably"** appearing more than once per section
7. **Em dashes more than once per paragraph**

If any of these appear more than twice in the entire paper, the text likely reads as AI-generated to an experienced academic reader.

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
| 3.0.0 | 2026-06-05 | Ground-up rewrite. Consolidated into single-file monolithic format with all reference material inline. Added trigger conditions table, mode selection guide, anti-patterns table, AI-fingerprint quality standards. |
| 2.x | 2026-06-04 | Round 4 additions (Sections 62-90), AI-fingerprint warnings, caveats J-L |
| 2.x | 2026-06-03 | Round 3 quality audit, caveats A-I |
| 1.x | 2026-05 | Initial creation from 124 JF papers |

---

*Synthesized from 144 Journal of Finance papers (2022--2025). All examples verbatim from published JF articles.*

---

# JF Writing Style Guide — Sentence-Level Templates

*A comprehensive reference of academic writing patterns extracted from 124 published Journal of Finance papers (2022--2025). Organized by writing function -- find the section that matches what you are trying to accomplish.*

---

# PART A: SENTENCE-LEVEL TEMPLATES

---

## 1. Opening Your Paper (First Sentences of Introduction)

**Standard ALL CAPS Openings:**

1. "ARE GERMANS MORE TRUSTWORTHY THAN the French? It turns out that the answer varies greatly depending on whom you ask." (Pursiainen, "Cultural Biases in Equity Analysis")

2. "A LARGE LITERATURE DOCUMENTS THAT the health of the banking sector is important for nonfinancial firm outcomes such as investment and employment." (Chu, "Loan Covenant")

3. "THE DIFFICULTIES THE CANONICAL CONSUMPTION-based asset pricing model faces in matching key empirical moments in both the time series and the cross section have sparked a large theoretical literature." (Bansal, Miller, Song, Yaron, "Long-Run Risk")

4. "Whether and to what extent decision-makers take sunk costs into account is a long-standing question in economics, finance, and psychology." (Guenzel, "In Too Deep")

5. "A central question in the design of executive compensation contracts is whether managers should be rewarded for observable shocks that are beyond the managers' control." (Chen et al., "Are CEOs Rewarded for Luck?")

6. "DOES INTERNET USE SPUR A 'democratization of finance' (Shiller (2007)), meaning improved portfolio choices by households, or does it amplify behavioral biases?" (Broadband Internet)

7. "A CENTRAL ISSUE IN THE STUDY of macroeconomic stability is the predictability of financial crises. An important line of thought holds that crises are largely unpredictable." (Greenwood et al., "Predictable Financial Crises")

8. "THE CRYPTOCURRENCY MARKET HAS EXPERIENCED rapid growth. This market allows companies to raise money without engaging with venture capitalists and to be traded without being listed on stock exchanges." (Liu, Tsyvinski, Wu, "Common Risk Factors in Cryptocurrency")

9. "THE TRADITIONAL ROLE OF LIFE insurers is to insure idiosyncratic risk through products such as life annuities, life insurance, and health insurance." (Koijen and Yogo, "The Fragility of Market Risk Insurance")

10. "A GROWING LITERATURE DOCUMENTS THAT the real values of long-term financial assets—including the stock market, a perpetual asset that endures indefinitely—fluctuate sharply in response to the actions and announcements of central banks. But this leads to a puzzle." (Bianchi, Lettau, Ludvigson, "Monetary Policy and Asset Valuation")

11. "THE TEXTBOOK EXPLANATION FOR WHY some assets have higher expected returns than others involves 'extending the principles behind fire and casualty insurance to investment portfolios (Cochrane (1999)).'" (Chinco, Hartzmark, Sussman, "A New Test of Risk Factor Relevance")

12. "A LARGE AND EXPANDING LITERATURE explores the relation between stock returns and the business cycle. The traditional view is that stocks are rationally priced to immediately reflect investors' expectations about future economic activity." (Gomez-Cram, "Late to Recessions")

**Alternative Opening Styles:**

13. **Rhetorical-Question-Answer:** "DO FINANCIAL CRISES FAN THE FLAMES of fanaticism? Many political commentators and journalists think so." (Doerr et al., "Financial Crisis and Populism") — Poses a provocative YES/NO question in ALL CAPS, then immediately answers with what "many" believe before proceeding to the evidence.

14. **Two-Concurrent-Trends Hook:** "TWO PHENOMENA IMPACTED THE U.S. economy in the years preceding the Great Recession. One is the dramatic rise in household debt from 2000 to 2007. The other is an unprecedented increase in import competition triggered by the expansion of China... We hypothesize that these two occurrences are linked." (Import Competition and Household Debt) — Introduces two parallel empirical trends as stylized facts, then conjectures they are causally connected. Distinct from puzzle or gap openings.

15. **Historical Arc Opening:** "Over the past half-century, investor trading has changed significantly. Decades ago, retail investors traded via phone only during market hours, paying heavy commissions to do so. The 1990s brought about online trading and significantly lower commissions. More recently, the fintech brokerage Robinhood brought about even more changes..." (Barber et al., "Attention-Induced Trading") — A three-stage historical progression (past, intermediate, contemporary) that grounds the paper's relevance in technological or institutional change. Useful for papers studying recent phenomena.

16. **"Witnessed" + Enumerated Trends:** "THE RECENT ERA OF GLOBALIZATION witnessed (i) increased correlation of stock market returns across countries... and (ii) greater cross-country trade integration as firms' production chains spread across the world." (Stock Market Spillovers via Global Production Network) — Uses "witnessed" as an active verb within an ALL CAPS opening, then enumerates parallel trends that set up the research question.

17. **Characterizing-a-Challenge Opening:** "CHARACTERIZING THE MACROECONOMIC FUNDAMENTALS DRIVING the real and nominal yield curves in a unified framework has been a long-standing challenge for macroeconomists and financial economists." (Risk-Sharing and the Term Structure) — Names a specific intellectual challenge and the fields for whom it has been a challenge. Useful for cross-field papers that bridge subdisciplines.

18. **Concrete-Anecdote Opening:** "ON NOVEMBER 26, 2012, THE analyst following the common stock of Bank of America (BAC) at Guggenheim Securities made a tactical trading call suggesting that investors sell BAC over the next three months based on his expectation of the impact on BAC of the U.S. economy being pushed over fiscal cliffs. At the same time, the analyst reiterated his buy recommendation on BAC over a 12-month period based on his long-term investment thesis." (Are Analyst Short-Term Trade Ideas Valuable?) — A journalistic opening dropping the reader into a specific date, named analyst, named brokerage, and specific ticker. This concrete microcosm is then used to motivate the broader research question. Distinct from historical arc because it zooms into one moment rather than tracing a trend.

19. **Historical-Legislation Opening:** "THE 2000 REGULATION FAIR DISCLOSURE ('Reg FD') and the 2003 Global Analyst Research Settlement ('Global Settlement') are two of the most significant regulatory actions designed to protect retail investors in the past few decades." (Non-Deal Roadshows) — Opens with specific regulatory actions and their dates, framing the paper's importance through legal/regulatory change rather than broad stylized facts. Useful for papers evaluating a specific regulation's effects.

20. **Challenge-Conventional-View Opening:** "A LONG-STANDING VIEW IN FINANCIAL ECONOMICS is that banks specialize in lending to industries in which they have a comparative advantage. In this paper, we challenge this view..." (Paravisini et al., "Specialization in Bank Lending") — States an established conventional view in ALL CAPS, then immediately challenges it. Distinct from puzzle openings because it names the specific view being overturned rather than setting up a tension.

21. **Functional-Role Opening:** "THE MAIN ROLE OF PRIMARY FINANCIAL MARKETS is to channel resources to firms with worthwhile projects." (Axelson and Makarov, "Informational Black Holes") — Opens by defining the core function or purpose of the institution/market under study. The rest of the paper then shows how this function is undermined. Useful for papers studying market failures or institutional breakdowns.

22. **Definition-Then-Importance Opening:** "MOMENTUM, THE TENDENCY FOR ASSETS that have earned above-average returns in the past to continue to outperform in the future, is one of the most pervasive and widely studied financial market anomalies." (Heston et al., "Option Momentum") — Defines the key concept in an appositive clause, then asserts its importance. Useful when the concept may be unfamiliar to some readers or when a precise definition sets up the extension.

23. **Revolutionary-Change Opening:** "THE ADVENT OF ZERO-COMMISSION TRADING in stocks and options has revolutionized retail brokerage services in the United States." (Bryzgalova, Pavlova, and Sikorskaya, "Retail Trading in Options") — Opens with a technological or regulatory disruption that has transformed an industry. Useful for papers studying the consequences of recent structural change.

24. **Two-Observations-Enumeration Opening:** "IN THE LAST DECADE OR SO, two observations have come to the forefront of the empirical asset pricing literature. First, thanks to the factor zoo phenomenon, in the near future we might have as many empirically 'priced' sources of risk as stock returns. Second, the so-called weak factors..." (Bryzgalova, Huang, and Julliard, "Bayesian Solutions for the Factor Zoo") — Enumerates two parallel empirical observations that jointly motivate the paper. Distinct from two-concurrent-trends because it lists abstract observations rather than concrete trends.

25. **Post-Crisis-Era Opening:** "SINCE THE GREAT RECESSION, CENTRAL BANKS around the world have employed large-scale asset purchases as an essential tool in a rapidly evolving policy landscape." (Corhay et al., "Discount Rates, Debt Maturity, and the Fiscal Theory") — Grounds the paper's relevance in a specific post-crisis policy environment. Useful for papers studying the consequences of crisis-era policy innovations.

26. **Expectation-Before-Contradiction Opening:** "One might expect that when a larger number of experts are active in the market in which a firm seeks financing, investment decisions should improve and the cost of capital for the firm should go down. There are two compelling reasons from economic theory to support these expectations. First... Second... Yet, research on 'investment cycles' suggests that increasing the size of financial markets may not always be socially useful." (Axelson and Makarov, "Informational Black Holes") — First builds up the intuitive expectation with theoretical support, then introduces the contradictory evidence. A three-part structure: intuition, theoretical support, contradiction. More elaborate than a simple puzzle.

27. **Open-Question-Periodically-Gains-Relevance Opening:** "Whether to tax financial transactions or not remains an important open question for public economics that periodically gains broad relevance after periods of economic turmoil." (Optimal Financial Transaction Taxes) — Describes a recurring policy/academic debate where the question "periodically gains broad relevance" after crises, creating a more dynamic sense of importance than simply calling it "important." Useful for papers on topics that resurface cyclically.

28. **High-Level-Conceptual-Framing Opening:** "At a high level, disruption captures the idea that some shocks, such as regulation or a new technology, affect incumbent firms in an industry differently than new entrants." (Disruption and Credit Markets) — Uses "At a high level, X captures the idea that..." to provide an intuitive, bird's-eye definition of a key concept before diving into technical detail. Useful for papers introducing a conceptual framework or novel taxonomy.

---

## 2. Stating Your Research Question / Motivation

**Examples:**

1. "In this paper, we examine the canonical case of a radical government coming to power: Hitler and his Nazi party in 1930s Germany." (Doerr et al., "Financial Crisis and Populism")

2. "In this paper, we quantify the contribution of the zombie credit channel to Europe's disinflationary episode after its sovereign debt crisis." ("Zombie Credit and (Dis-)Inflation")

3. "This paper examines whether executives receive compensation for windfall gains that are unrelated to their efforts." (Chen et al., "Are CEOs Rewarded for Luck?")

4. "In this paper, we study the role of cultural biases in analysts' stock recommendations in Europe." (Pursiainen, "Cultural Biases in Equity Analysis")

5. "We study the effects of the rollout of high-speed broadband internet on the stock market participation and portfolio choices of individual investors in Norway in the 2000s." (Broadband Internet)

6. "In this paper, we estimate the probability of financial crises as a function of past credit and asset price growth." (Greenwood et al., "Predictable Financial Crises")

7. "In this paper, we address this question, by exploiting a new rule that requires U.S. publicly traded companies to report the ratio between CEO pay and median worker pay for the first time in 2018." (Pan et al., "Pay Ratio Disclosure")

8. "I find that returns are predictably negative for several months after the onset of recessions, becoming high only thereafter." (Gomez-Cram, "Late to Recessions")

9. "In this paper, we present new empirical evidence consistent with this hypothesis, and a new theoretical explanation consistent with the evidence." (Bianchi et al., "Monetary Policy and Asset Valuation")

10. **Stronger Agency Variant:** "This paper is devoted to establishing that part of this relation is causal and understanding why exposure to FC loans increased support for the populist far right." (Doerr et al., "Financial Crisis and Populism") — Stronger than "we examine," signaling a clear causal mission.

11. **Testing-by-Negation:** "In this paper, we test this proposition not by inferring beliefs from reported beliefs or asset prices, but by showing that investors adjust their portfolios differently in response to the same public event and by ruling out the main nonbelief channels." (Belief Disagreement and Portfolio Choice) — Structures the approach by first stating what you do NOT do, then affirming what you DO. Creates contrastive emphasis on methodological improvement.

12. **Goal-Qualifying Variant:** "We investigate the differences in the pricing of SPX and VIX options in this paper with a primary view toward understanding the factors that drive differences..." (The Price of Higher Order Catastrophe Insurance) — "with a primary view toward understanding" frames the purpose as directional/aspirational, not definitive.

13. **Premise-Statement Opening:** "Our analysis builds on the premise that the value created by a fund ultimately depends on (i) skill... and (ii) scalability..." (Skill, Scale, and Value Creation in the Mutual Fund Industry) — States a core premise before describing the analysis. The paper commits to a foundational idea upfront, and everything that follows is built on that premise. Distinct from standard "we study" because it foregrounds the theoretical logic.

14. **Process-Oriented Opening:** "We begin our analysis by showing that stock borrowing fees are related to option prices through a version of the put-call parity relation augmented to include the borrowing fee." (Is There a Risk Premium in the Stock Lending Market?) — Narrates the analytical journey step by step. Distinct from "In this paper, we..." because it foregrounds the process rather than the destination.

15. **Essential-Idea Statement:** "The essential idea underlying our paper is that a more sophisticated statistical technology... produces predictions with greater variance than a more primitive technology." (Predictably Unequal? The Effects of Machine Learning on Credit Markets) — States the paper's core insight explicitly and directly, functioning as an "elevator pitch" for the paper's theoretical mechanism. More pointed than standard contribution statements.

16. **Middle-Way Positioning:** "We find a middle way between trade-offs in existing studies: clean identification versus a real-world setting and important experiences." (Fully Closed) — Frames the paper as occupying the Goldilocks middle ground between two opposing methodological poles.

17. **Extension-to-New-Domain Question:** "In this paper, we ask whether [phenomenon] also exists within [new domain]." (Heston et al., "Option Momentum") — States that a well-documented phenomenon in one market/asset class may extend to another. The word "also" signals that the paper is testing generalizability rather than proposing something entirely new.

18. **Research-Importance Justification:** "Studying such questions is important because..." (Schilling, "Optimal Forbearance") — Explicitly justifies the research question's importance after posing it. Distinct from contributions (Section 5) because it precedes the contribution statement and motivates the question itself.

19. **Focusing-on-X-Also-Allows Contribution:** "Focusing on the demand side also allows us to explain cross-sectional variation in the sign and magnitude of the basis across equity indices." (Beyond Basis Basics) — After stating the paper's primary focus, appends an "also allows us to" additional contribution. A two-move structure that packages a secondary result as a natural byproduct of the primary research design.

20. **Cannot-Speak-to-X-but-Provides-Y Contribution:** "Although this study is unable to speak to the effect of these restrictions on the abusive practices they target, it provides causal empirical evidence on the effects of this legislation on both mainstream and alternative credit markets." (Less Mainstream Credit) — First acknowledges what the paper cannot answer, then immediately pivots to what it does provide. An elegant limitation-then-contribution combination that manages expectations while asserting value.

---

## 3. Setting Up a Puzzle or Tension

**Examples:**

1. "But this leads to a puzzle. Asset pricing (AP) theories can generally rationalize such large responses only if market participants believe that something related to monetary policy will have a long-lasting effect on real variables. Yet the notion that monetary policy shocks could have long-lived effects on real variables is contravened by both foundational New Keynesian macro theories and prior empirical evidence." (Bianchi et al., "Monetary Policy and Asset Valuation")

2. "From a market participant perspective, this pattern suggests that the investor can profit by selling at the start of recessions and then increasing risk-taking several months later. From a risk-based perspective, the empirical pattern in Figure 1 presents a puzzle because it is hard to explain negative average excess returns within any rational equilibrium model." (Gomez-Cram, "Late to Recessions")

3. "It is possible, however, that financial markets do not recognize income inequality as an important concern. In this case, the market response to pay ratio disclosure would depend on what, if anything, markets infer from the newly disclosed pay ratios." (Pan et al., "Pay Ratio Disclosure")

4. "A potential concern with this argument is that the variation in correlations that we examine is economically meaningful because the relative risk aversion of gamma = 100 is too high." (Chinco et al., "A New Test of Risk Factor Relevance")

5. **Frictionless-Benchmark Puzzle:** "In a frictionless world, collateral quality need not have any predictable relation to margin, spread, or maturity. In contrast, the data clearly show that all three terms rise as collateral quality drops." (Loan Terms and Collateral) — Establishes the null prediction of frictionless theory, then immediately shows the data contradicts it. A powerful structure for papers testing market imperfections.

6. **Unsatisfactory Closure:** "While this literature safely rejects the null hypothesis that firms are not financially constrained, it provides little guidance on the economic importance of financial constraints that derive from their 'well-identified' estimates." (Quantifying Reduced-Form Evidence on Collateral Constraints) — Praises the literature for succeeding on one dimension (rejection), then pivots to the limitation (no quantification). Useful for bridging reduced-form and structural approaches.

7. **Unsurprising-But-Not-Necessary:** "While it is unsurprising that riskier collateral is associated with higher margin requirements, it is not theoretically necessary that loans against riskier collateral be riskier or have a substantially higher spread." (Loan Terms and Collateral) — Concedes one finding is expected, then separates it from a distinct question that is NOT theoretically determined.

8. **Surprising-Neglect Gap:** "Given the close relationship between market liquidity and asset pricing, it is somewhat surprising that the effect of the parallel trading environment on asset prices has received little attention." (Asset Pricing with Cohort-Based Trading in MBS Markets) — Adds the author's evaluative judgment to standard gap identification.

9. **Contrasting-Facts-Puzzle:** "Yet, at the start of the financial panic in 2008, only 10% of bank loans had remaining maturity of less than one year and the typical firm did not face the prospect of a bank loan maturing until 2011. These observations point to an important gap in our understanding of the transmission of bank health: why do shocks to lenders affect their existing corporate borrowers despite the prevalence of long-term credit?" (The Loan Covenant Channel) — Juxtaposes two directly contradictory facts and crystallizes the research question FROM the tension. Distinct from standard gap statements because the gap is a logical contradiction between two stylized facts, not an absence in prior literature.

10. **Testing-Implications-of-Prior-Theory:** "An implication of the Engelberg, Reed, and Ringgenberg (2018) analysis is that short sellers should receive a risk premium... A second implication... is that the returns to short-selling... should also reflect a premium... We test these predictions and find that the evidence does not support them." (Is There a Risk Premium in the Stock Lending Market?) — The entire paper is structured around deriving and testing logical implications of ONE specific prior theory. Distinct from puzzle statements because it takes an existing theoretical claim seriously and empirically stress-tests it.

11. **Resolves-Famous-Puzzle:** "This characterization of momentum resolves the perennial question about covariances and momentum (Cochrane (2011, p. 1075)): '...why should all the momentum stocks then rise and fall together the next month, just as if they are exposed to a pervasive, systematic risk?'" (Factor Momentum and the Momentum Factor) — The paper's central finding is framed as directly answering a well-known puzzle posed by a prominent scholar. Cites the exact words of the puzzle-poser.

12. **Theory-Supported-Expectation-Then-Contradiction:** "One might expect that [X] should [expected outcome]. There are two compelling reasons from economic theory to support these expectations. First... Second... Yet, research on 'Y' suggests that [contradictory evidence]." (Axelson and Makarov, "Informational Black Holes") — A three-part structure: (1) intuitive expectation, (2) theoretical support enumerated, (3) contradiction from evidence. More elaborate than a simple puzzle because it builds up the theoretical case before undermining it.

13. **Sharp-Contradiction-with-Theory Puzzle:** "With perfect capital markets, there is no role for CLOs, or securitization more broadly, because economic agents can costlessly transform cash flows. Therefore, CLOs exist because of market imperfections." (CLO Performance) — Starts from a frictionless benchmark where the studied object should not exist, then immediately affirms it does, converting existence itself into a puzzle about which imperfections drive it.

14. **At-First-Glance-Surprising Puzzle:** "Finally, at first glance, it might be surprising that the major risk factors all share the common economic feature of investing in firms with a short cash-flow duration. We argue, however, that this commonality is intuitive." (Duration-Driven Returns) — Poses a surprise, then resolves it by providing the unifying logic. The "at first glance" framing acknowledges the surprise is superficial and the resolution is the contribution.

---

## 4. Identifying Gaps in the Literature

**Examples:**

1. "What has been missing from the literature on the real effects of financial crises is a clear link between financial distress and broad-based radicalization of the electorate." (Doerr et al., "Financial Crisis and Populism")

2. "Despite a large body of work on bank lending, little is known about how the distance between lenders and borrowers varies over the business cycle." (Granja, Leuz, Rajan, "Distant Lending")

3. "While a large literature has examined the determinants of CEO compensation, much less is known about how the demands of the CEO position affect managers' personal well-being." (Guenzel, Hamilton, Malmendier, "CEO Stress, Aging, and Death")

4. "However, evidence on the effect of transparency with respect to gender pay disparities on employee and firm outcomes is limited." (Bennedsen et al., "Gender Pay Gap")

5. "Much less is known, however, about whether rare disaster risk helps explain the cross section of stock returns." (Hirshleifer, Mai, Pukthuanthong, "War Discourse")

6. "Notwithstanding this evidence, however, precise estimates of the probability of a financial crisis following credit and asset price booms remain unavailable. More importantly, how high the probability of a crisis should be permitted to climb before prompting preemptive policy action remains an open question." (Greenwood et al., "Predictable Financial Crises")

7. "While previous empirical and theoretical research assumes (implicitly) that equity holders price all leverage-related risks equally, we investigate the possibility that shareholders demand different risk premia for short-term compared to long-term leverage." (Friewald, Nagler, Wagner, "Debt Refinancing and Equity Returns")

8. **Volume-Contrast Gap:** "While there are countless studies of equity options market data, relatively few papers study VIX options." (The Price of Higher Order Catastrophe Insurance) — Frames the gap through volume of existing research ("countless" vs. "relatively few").

9. **Logical-Necessity Gap:** "By definition, the connection between borrowing and lending and the term structure cannot be made in a representative agent setup and thus departing from such a paradigm is essential." (Risk-Sharing and the Term Structure) — A "by definition" argument that shows the gap is logically built into the standard framework.

10. **Prevailing-Assumption Gap:** "The assumption among advocates of automatic enrollment has been that the incremental retirement plan contributions... are financed largely by decreased consumption... However, no evidence to date rules out alternative possibilities." (Borrowing to Save) — States a prevailing assumption, then notes the absence of evidence that would disconfirm alternatives.

11. **What-Fails-to-Account-For:** "What this 'silver bullet' view of compensation regulation fails to account for is the Lucas critique." (The Economics of Deferral and Clawback Requirements) — Characterizes a view, then states what fundamental point it misses.

12. **Implicit-Novelty Gap:** "We are not aware of any study that directly estimates flow-to-performance sensitivities at the family level." (Institutional Investors and Corporate Governance) — A restrained novelty claim that states absence of prior work without insisting on primacy.

13. **Paradigm-Failure-Attribution Gap:** When existing literature has repeatedly failed, attribute the failure not to technical limitations but to a fundamental modeling choice. Step 1: show the standard method consistently fails. Step 2: argue this is not because the model is insufficiently flexible or the researchers insufficiently skilled. Step 3: identify the root cause as a fundamental setup error (e.g., "bonds in and of themselves do not possess the information needed to capture the behavior of exchange rates"). Step 4: introduce a new framework that addresses the root cause. (International Yield Curves and Currency Puzzles) — The most powerful motivation for a new framework: prior failures are not technical but foundational.

14. **Debate-Unresolved Gap:** "The debate centers on whether [X or Y]. Our findings provide evidence that [resolution]." (Naive Buying Diversification) — Names an active scholarly debate, then positions the paper as providing the decisive evidence.

---

## 5. Announcing Your Contribution

**Examples:**

1. "Our main contribution is to document the effects of financial distress on broad-based radicalization of the electorate with major political consequences." (Doerr et al., "Financial Crisis and Populism")

2. "In this paper, we provide the first systematic study of the role of gender-based disclosure on the gender pay gap." (Bennedsen et al., "Gender Pay Gap")

3. "This study provides novel evidence of cultural biases affecting the judgment of sell-side analysts." (Pursiainen, "Cultural Biases in Equity Analysis")

4. "Our paper makes two contributions. We first propose a quantitative measure of the economic dark matter in structural models... Then, under a general semiparametric framework, we formally show that models with larger dark-matter measures tend to have lower in-sample refutability." ("Measuring Dark Matter")

5. "We contribute to three strands of literature. First, we contribute to the literature on zombie credit... Second, we contribute to the literature on the effects of financial frictions on inflation... Third, we contribute to the literature on resource misallocation." ("Zombie Credit")

6. "The main contribution of our paper is to spotlight the importance of covenant violations to the contraction in bank credit supply during the 2008 to 2009 financial crisis." (Chu, "Loan Covenant")

7. "We make several contributions to this literature. First, we document the strength of the interaction effect... Second, we uncover a higher degree of crisis predictability than has been documented in prior studies. Finally, we calibrate a simple model..." (Greenwood et al., "Predictable Financial Crises")

8. "A key contribution of this paper is to highlight survey evidence as particularly useful for testing factor models." (Chinco et al., "A New Test of Risk Factor Relevance")

9. "Another contribution is to develop a theory of market risk insurance, building on the work of Froot (2007) for catastrophe insurance." (Koijen and Yogo, "The Fragility of Market Risk Insurance")

10. "The aim of the paper is to change how economists evaluate factor models." (Chinco et al., "A New Test of Risk Factor Relevance")

11. **Demystify Contribution:** "As another contribution of this paper, we demystify the workings of the countercyclical factor." (The Two-Pillar Policy for the RMB) — "Demystify" frames the contribution as revealing a hidden or poorly understood mechanism.

12. **Augmentation Contribution:** "We augment existing analyses of automatic enrollment by studying household liabilities." (Borrowing to Save) — Frames the contribution as extending prior work.

13. **Bridge-as-Contribution:** "We bridge these different strands of the literature by showing the importance of real linkages in the international transmission of monetary policy shocks across asset markets." (Stock Market Spillovers via Global Production Network) — Using "bridge" integrates disconnected literatures.

14. **Proxy Contribution:** "Our paper proposes a proxy for private information." (Clients' Connections) — A methodological contribution: proposing a new measurement approach.

15. **Primacy Claim:** "To the best of our knowledge, this paper conducts the first analysis of the distinctive asset pricing effects of the TBA/SP parallel trading environment." (Asset Pricing with Cohort-Based Trading in MBS Markets) — A patent-style priority claim qualified with "to the best of our knowledge."

16. **Dual Documentation Claim:** "We first document novel stylized facts and show empirically that a two-pillar policy has been in place..." (The Two-Pillar Policy for the RMB) — Pairs two contribution types (documentation + empirical demonstration) in a single template.

17. **First-Positive-Systematic-Answer:** "Is cross-sectional stock return predictability related to the time-series predictability of the aggregate market excess return? Our paper provides the first positive systematic answer to this question." (Anomalies and the Expected Market Return) — Layers three qualifiers: temporal primacy, directional result, and comprehensiveness.

18. **Pioneer-Credit Attribution:** "The study of value creation, or value-added, is pioneered by Berk and van Binsbergen (2015, BvB hereafter)." (Skill, Scale, and Value Creation in the Mutual Fund Industry) — A stronger-than-standard citation that explicitly credits prior work as having "pioneered" a field.

19. **Results-Are-Relevant-For-N-Strands:** "Our results are relevant for three strands of literature. First, our findings are related to the empirical literature on... Second, our findings are related to the literature on... Third, our findings are related to the literature on..." (Fully Closed) — A specific meta-discourse pattern where the conclusion's literature positioning is organized as explicitly numbered "strands."

20. **Shed-New-Light Contribution:** "Our results shed new light on the value creation process." (Skill, Scale, and Value Creation) — A more literary and less formulaic contribution statement than "we contribute to."

21. **First-Direct-Evidence Contribution:** "These findings are significant because they represent the first direct evidence that [X]." — Emphasizes both significance and novelty through "first direct evidence." Stronger than a standalone primacy claim because it ties novelty to substantive importance.

22. **Single-Author Demonstration Contribution:** "My main contribution is the demonstration that [X]." (Schilling, "Optimal Forbearance") — Uses "demonstration" rather than "documentation" or "examination," signaling a proof-oriented contribution. The singular possessive "My" marks single-author papers.

23. **Contrast-With-Conventional-Wisdom Contribution:** "Our results have normative implications for [X] that contrast drastically with common wisdom." (Axelson and Makarov, "Informational Black Holes") — Frames the contribution's importance through the sharpness of its divergence from conventional thinking. "Drastically" amplifies the contrast.

24. **Confident-Direct-Assertion Contribution:** "That is exactly what we provide." (Bryzgalova, Huang, and Julliard, "Bayesian Solutions for the Factor Zoo") — After enumerating what is missing from the literature, this short sentence asserts that the paper fills the gap precisely. Unusually confident for JF, reserved for papers with genuinely comprehensive solutions.

25. **Distinctive-Focus Contribution:** "Our paper is distinct in that we focus on [X] rather than [Y]." — Frames contribution through the lens of different focus rather than different method or different finding. Useful when the paper's object of study itself is novel.

26. **Facts-Require-Explanation Contribution:** "These facts require a demand-based explanation, which we provide." (Beyond Basis Basics) — After presenting a series of findings that existing theory cannot explain, asserts that the facts themselves "require" a new explanation. Stronger than "we offer an explanation" because it implies the explanation is necessitated by the empirical evidence.

27. **Restated-and-Amplified Puzzle Contribution:** "The joint evidence on total asset payouts and returns is thus reminiscent of the Mehra and Prescott (1985) equity premium puzzle, restated and amplified in the context of corporate assets." (How Risky Are U.S. Corporate Assets?) — Positions the paper's finding as a "restated and amplified" version of a classic puzzle. Simultaneously connects to the literature and highlights the incremental contribution.

28. **Impossibility-Motivates-Alternative Contribution:** "It is impossible to commit under the equity-based scheme, as the owner can always choose to reverse any previous commitment at time 2. This demand for commitment motivates tokenization." (Decentralization through Tokenization) — First proves an ideal state is impossible under the existing regime, then uses "this demand for X motivates Y" to introduce the alternative. Powerful for papers proposing new institutional forms or mechanisms.

---

## 6. Enumerating Findings (Multi-Finding Preview)

**Examples:**

1. "We present six findings. First, consistent with Schularick and Taylor (2012), we show that crises can be predicted using past credit growth... Second, we show that the degree of predictability rises substantially when we focus on large credit expansions... Third, we show that overheating in the business and household credit markets are separate phenomena..." (Greenwood et al., "Predictable Financial Crises")

2. "We document several additional results. First, we investigate the multiple hypothesis testing problem... Second, we study the implementability of the strategies... Third, we examine the similarity between the cryptocurrency market and the currency market." (Liu et al., "Common Risk Factors in Cryptocurrency")

3. **Design-Enumeration Variant:** "Our investigation has a number of key features. First, we focus on a cornerstone of the cross-sectional literature... Second, we employ out-of-sample tests... Third, we examine the predictive ability... Fourth, we explore economic rationales..." (Anomalies and the Expected Market Return) — Enumerates investigative design features rather than findings preview.

4. **Taxonomy-Enumeration Variant:** "These trade ideas differ from recommendations in five important ways. First, trade ideas are based on predictions of short-term price changes... Second, compared to recommendations, trade ideas have a very short investment horizon... Third... Fourth... Fifth..." (Are Analyst Short-Term Trade Ideas Valuable?) — A numbered taxonomy that systematically differentiates the paper's object of study from a well-known alternative.

---

## 7. Describing Your Data / Setting

**Examples:**

1. "We combine a number of data sources... several of which are hand-collected and digitized for the first time." (Doerr et al., "Financial Crisis and Populism")

2. "Our main data set comprises the matched employer-employee data set from the Integrated Database for Labor Market Research." (Bennedsen et al., "Gender Pay Gap")

3. "Our main sample consists of 24,466 CEO-years of data on 3,202 CEOs over the period 1976 to 2018." (Guenzel, Hamilton, Malmendier, "CEO Stress, Aging, and Death")

4. "Our full data set covers $2 trillion of loan commitments at the start of 2008." (Chu, "Loan Covenant")

5. "As a source of exogenous variation in internet use, we exploit a program rolled out by the Norwegian government in the 2000s." (Broadband Internet)

6. "We use three sources to construct a comprehensive panel data set on the variable annuity market at the contract level." (Koijen and Yogo, "Fragility")

7. "My sample includes 1,827 coins from the beginning of 2014 to July 2020." (Liu et al., "Common Risk Factors in Cryptocurrency")

8. **Laboratory Metaphor:** "Bilateral repurchase agreements are a unique laboratory for the purpose of understanding the terms of collateralized loans in general." (Loan Terms and Collateral) — Using "laboratory" to frame a specific institutional setting as particularly well-suited for answering a broad question.

9. **Before-Going-Into-Specifics Preview:** "Before going into specifics, it is useful to elaborate on the frequencies at which various variables are measured and how these work together in our analysis." (Stock Market's Assessment of Monetary Policy Transmission) — A data architecture overview before diving into variable definitions.

10. **Vivid Data Showcase:** "For example, we can see that in the first week of August 2008, 24 cans of Del Monte French-style green beans were sold in a particular store in Chicago at an average price of $1.15 per can." (Barbarians at the Store?) — Pauses to give a hyper-specific example of raw data granularity, including exact date, brand, product, location, quantity, and price. Builds credibility and makes the data feel tangible.

11. **Data-Representativeness Subsection:** "A limitation of our sample is that [source] reports only a subset of [activity]... To shed light on this possibility, for each day during the month of August 2020 we record all [measurements]..." (Non-Deal Roadshows) — A dedicated subsection within the data section that candidly admits a coverage limitation and provides hand-collected validation data.

12. **Desirable-Properties Method Description:** "The measure has several desirable properties, such as being impervious to [confound]." (Paravisini et al., "Specialization in Bank Lending") — When introducing a new measure or proxy, explicitly lists its methodological advantages. "Impervious to" is stronger than "robust to" — it signals immunity rather than resilience.

---

## 8. Stating Hypotheses / Predictions

**Examples:**

1. "If analyst recommendations are affected by the analyst's cultural biases, one might expect a stronger effect when the nationality of the firm is more salient." (Pursiainen)

2. "If rent extraction explains CEO rewards for luck, then we should expect CEOs with weaker pay scrutiny to receive higher compensation following positive tax shocks." (Chen et al.)

3. "If investors evaluate stocks at the portfolio level, then the propensity to sell a stock should depend not only on its own return but also on the returns of other stocks in the portfolio." (An et al.)

4. "The sunk cost hypothesis gives rise to the prediction that firms are less likely to divest acquired businesses that became exogenously more costly." (Guenzel)

5. "On the one hand, it is plausible that faster internet would reduce the cost of these activities. On the other hand, faster internet also reduces the cost of leisure-related activities... which could crowd out individuals' focus on personal finance." (Broadband Internet)

6. "With these two economic mechanisms in mind, we let the equity data speak for themselves. Both channels suggest the same empirical strategy..." (Friewald et al., "Debt Refinancing")

7. **A Priori Ambiguous:** "The effect on productivity is a priori ambiguous. If information on the gender pay gap lowers the job satisfaction of female employees, it may negatively affect their productivity... However, if increased transparency and firms' responses increase the perception of fairness among employees, productivity may be positively affected." (Gender Pay Gap Transparency) — Template: "The effect on [X] is a priori ambiguous. If [theory A], it may [direction A]. However, if [theory B], [direction B]."

8. **Hypothesis-then-Elaboration:** "We hypothesize that these two occurrences are linked, in particular, that the adverse impact of import competition on labor markets stimulated household debt expansion in the 2000s. More precisely, we argue that the displacement of domestic production by imports fueled credit demand in impacted areas." (Import Competition and Household Debt) — States a broad hypothesis, then immediately refines with "More precisely, we argue that..."

9. **Debate-Closing Variant:** "The effect of transparency on the gender pay gap and firm outcomes is ultimately an empirical question." (Gender Pay Gap Transparency) — After presenting competing theoretical predictions, declares that theory cannot settle the matter.

10. **Formal Numbered Predictions:** "PREDICTION 1: Holding foreign monetary policy constant, U.S. contractionary policy should: 1. Lead foreign currencies to depreciate against the U.S. dollar... 2. Increase foreign nominal interest rates..." (Monetary Policy Spillovers through Invoicing Currencies) — Uses formally numbered, standalone predictions in the body of the paper, each with sub-points. More formal than "we hypothesize that."

11. **Dual-Approach Hypothesis Testing:** "To distinguish between strategic versus sincere optimism, we follow Malmendier and Shanthikumar (2014), who argue that sincerely optimistic analysts should issue both optimistic recommendations and optimistic short-term earnings forecasts, while analysts aiming to curry favor with management will issue optimistic recommendations together with more pessimistic (or 'beatable') short-term earnings forecasts." (Are Analyst Short-Term Trade Ideas Valuable?) — Cites a prior paper to derive distinct testable implications for two competing interpretations.

12. **Hypothetical-Investor Perspective-Taking:** "Consider, for example, the discovery of a new A-minus-B factor, AMB. An investor who believes that this factor is associated with an unconditional return premium needs to determine, ex ante, which leg outperforms the other... An investor who seeks to profit from the autocorrelation in factor returns, by contrast, does not need an estimate of the factor's unconditional mean." (Factor Momentum and the Momentum Factor) — Contrasts two hypothetical investor types to illustrate a conceptual point.

---

## 9. Reporting Baseline Results

**Examples:**

1. "Table III shows that support for the NSDAP rose markedly more in Danat-exposed cities." (Doerr et al.)

2. "The results are reported in Panel A of Table II. As shown in columns (1) and (2), a higher trust bias is associated with significantly more positive stock recommendations." (Pursiainen)

3. "We find that, after the passage of the law, wages of male employees in treated firms increase by 1.7 percentage points less than wages of male employees in control firms." (Bennedsen et al.)

4. "The estimated first stage coefficient equals 0.11, which means that a 100 percentage point increase in broadband coverage induces an additional 11% of the population to adopt broadband internet within the next year." (Broadband Internet)

5. "We find that three factors -- cryptocurrency market, size, and momentum -- capture the cross-sectional expected cryptocurrency returns." (Liu, Tsyvinski, Wu)

6. "Column (1) of Table II reports our baseline result... We observe a significantly negative relation between LN Pay Ratio and the cumulative abnormal announcement return." (Pan et al., "Pay Ratio Disclosure")

7. **Average-Masks-Heterogeneity:** "This relatively small average result masks substantial investor-level heterogeneity." (Belief Disagreement and Portfolio Choice) — A two-move pattern: acknowledge modest average, reveal important heterogeneity.

8. **Contrary-to-Prevalent-View:** "This finding is contrary to the widespread view that the residual credit risk in collateralized contracts is negligible, a central building block of models in which collateral is used to overcome belief disagreement or information asymmetry." (Loan Terms and Collateral) — Labels the conventional view as "widespread" AND foundational, making the contrary finding more consequential.

9. **Striking-Expectation-Contrast:** "This finding is striking because one would expect differential real effects of election outcomes on the current and future economic circumstances of people with different political affiliations." (Import Competition and Household Debt) — Contrasts actual findings with what "one would expect."

10. **Always-Negative-But-Insignificant:** "The estimates on Retail times NDR are always negative but generally statistically insignificant." (Non-Deal Roadshows) — A specific scaffold for reporting a result with consistent sign but unreliable significance.

11. **Margin-Analysis-Ruling-Out:** "This pattern is also present in the extensive margin, which indicates that it is not driven by [confound]." (Paravisini et al., "Specialization in Bank Lending") — Uses the presence of a pattern across different margins (intensive vs. extensive) to rule out specific alternative explanations. The pattern's robustness across margins becomes evidence against a confound.

12. **Striking-Magnitude-With-Expectation-Contrast:** "This magnitude is striking, given that this market has traditionally been thought to be populated largely by institutional and/or sophisticated investors." (Bryzgalova, Pavlova, and Sikorskaya, "Retail Trading in Options") — Reports a surprising magnitude and immediately contrasts it with the conventional understanding of the market. "Given that" introduces the expectation, not the evidence.

13. **Not-X-but-Rather-Y Result Interpretation:** "These results should be interpreted not as estimates of a causal relationship between VC or IPO activity and defaults, but rather as consistent with disruption in an industry simultaneously leading to success for new firms and distress for incumbents." (Disruption and Credit Markets) — Explicitly limits the interpretation scope: "not as X, but rather as consistent with Y." Simultaneously completes the result statement and provides cautious interpretation. Useful for observational (nonexperimental) studies where causal claims would be overreaching.

14. **Economically-Indistinguishable Result:** "The pool of leveraged loans comprising CLO assets generates gross returns that are economically indistinguishable from a broad-based index of leveraged loans." (CLO Performance) — A precise null-result phrase: "economically indistinguishable from" is stronger than "not significantly different from" because it asserts practical equivalence, not just statistical insignificance. Use when the point estimate is close to zero AND the confidence interval is tight.

15. **Closer-Inspection-Reveals Pattern:** "Closer inspection reveals that the abnormal equity returns are concentrated among CLOs originated before 2010." (CLO Performance) — A transition from aggregate results to heterogeneity analysis. "Closer inspection reveals" signals that the aggregate result masked important variation, which is now being uncovered.

16. **It-Turns-Out-That Discovery Connection:** "It turns out that the answer varies greatly depending on whom you ask." / "It turns out that these characteristics are similar along a key dimension." — Connects an empirical finding to a theoretical explanation with an element of surprise. Less formal than "we find that" and conveys a sense of discovery. Use sparingly for genuinely surprising connections.

---

## 10. Reporting Economic Magnitude

**Examples:**

1. "A one-standard-deviation increase in trust bias is associated with an 8.2% increase in the likelihood of buy recommendation, relative to the sample average." (Pursiainen)

2. "This is a dramatic difference: the Danat-induced drop in incomes represents 54% of the mean income decline of 14.4% over the period 1928 to 1934, or 0.44 sd." (Doerr et al.)

3. "The effect is economically large -- the presence of a Republican-leaning CEO results in a relative increase in store traffic of 6% to 11%." (Kempf et al.)

4. "An interquartile increase in market-induced acquisition cost is estimated to reduce divestiture rates by 9.4%." (Guenzel)

5. "The effect of BC law protection on mortality is equivalent to being about two years younger." (Guenzel, Hamilton, Malmendier)

6. "To put the pain of variable annuity insurers into perspective, the equity drawdown on the airline industry was negative 62%." (Koijen and Yogo, "Fragility")

7. **Marginal Effects at Multiple Percentiles:** Reports effects at multiple percentiles of the interaction variable's distribution beyond the standard "one-standard-deviation" approach.

8. **Approximation Metaphor for Fit:** "it is within striking distance of the equity premium, unconditional stock market volatility, the VRP..." (The Price of Higher Order Catastrophe Insurance)

9. **Multiples Comparison:** "more than six times larger than the corresponding estimate for nonlocal institutional investors" (Institutional Investors and Corporate Governance) — Uses direct multiples comparison to amplify perceived magnitude.

10. **"To Put the Numbers in Perspective" Benchmarking:** "To put the numbers in perspective, we also estimate the incentives of activist investors who..." (Institutional Investors and Corporate Governance) — Introduces benchmarking by referencing a known comparator.

11. **Back-of-the-Envelope Calculation:** "A simple back-of-the-envelope calculation of potential economic magnitudes suggests that..." (Predictably Unequal?) — Self-deprecatingly labels a preliminary calculation before full modeling.

12. **Equivalence-Metaphor Benchmarking:** "The effect of BC law protection on mortality is equivalent to being about two years younger." (CEO Stress, Aging, and Death) — Translates an abstract coefficient into a concrete, intuitive comparison. More vivid than "X standard deviations" because readers can immediately grasp the real-world magnitude.

---

## 11. Reporting Robustness Checks

**Examples:**

1. "Our findings are robust to a wide range of alternative specifications." (Doerr et al.)

2. "Our results are robust to using an array of alternative classifications and to measuring price changes with the producer price index (PPI) instead of the CPI." ("Zombie Credit")

3. "We perform a battery of robustness checks." (Granja, Leuz, Rajan)

4. "The results are robust to various sample restrictions, alternative specifications, and the inclusion of additional controls." (Guenzel)

5. "We next conduct a battery of robustness tests to assess the sensitivity of our main results. To conserve space, we discuss the results here but tabulate them in the Internet Appendix." (Chen et al.)

6. "To assess the robustness of the main result, I perform an extensive battery of tests. I briefly describe them here and provide more details in the Internet Appendix." (Gomez-Cram)

7. **Falsification Test:** "As a falsification test, we show that our empirical measure of the countercyclical factor has little to zero explanatory power in the subperiods in which it was not imposed." (The Two-Pillar Policy for the RMB)

8. **External Validity Test:** "As an external validity test, we examine the out-of-sample predictive ability of long-short anomaly portfolio returns for industry excess returns." (Anomalies and the Expected Market Return)

9. **Misleading-Inference Check:** "To explore the extent to which our results might lead to misleading inferences, we test whether our results differ for single employees versus employees who are members of a couple." (Borrowing to Save)

10. **Reporting Appendix Allocation:** "We present the main results, discussion, and brief robustness analysis in this paper and relegate details and a battery of tests that further establish robustness to an extensive Internet Appendix." (Stock Market's Assessment of Monetary Policy Transmission)

11. **Placebo Interpretation:** "We show that the average placebo coefficients are close to zero both before and after the law change in all cases, mitigating concerns that our results are driven by a different factor."

12. **"Obviates the Need for" Dismissal:** "Given conditional random assignment to treatment, treated and control firms differ only randomly from each other in their characteristics. While this obviates the need for the kinds of control variables sometimes included in empirical work in this area..." (Testing Disagreement Models)

13. **Validation by Predictable Subsample:** "We expect the risk premium to be small for the subsample of observations for which the stock is easy to borrow... These results validate our approach in general... If our various computation decisions were not appropriate, we would not expect to recover near-zero risk premiums for these subsamples." (Is There a Risk Premium in the Stock Lending Market?) — Identifies subsamples where measure SHOULD be near zero by theory and uses this as validation.

14. **"Problem With This Approach" Self-Critique:** "A problem with this approach is that standard industry codes are coarsely defined... The granularity of our data potentially reduces this concern: we employ as counterfactuals not only similar firms, but also similar product categories and similar products themselves in the same store." (Barbarians at the Store?) — Candidly identifies limitation then immediately argues data granularity addresses it.

15. **Multiple-Validation-Exercise Framework:** "We conduct several validation exercises to verify our methodology. First, we consider the face validity... Second, we... perform a structured human audit... Third, our exposure measures are robust to excluding one keyword at a time... Fourth, our keyword search-based measures substantially improve the identification... And fifth, we find plausible industry patterns." (Firm-Level Climate Change Exposure) — An explicitly numbered sequence of validation tests, each targeting a different methodological concern. More structured than "a battery of tests" because each test has a named purpose.

16. **Dual-Caveat Conclusion:** "This result comes with two important caveats. First, not all [X] have [property]... Second, our findings may not translate to other settings because of unique features of [setting]." (Did FinTech Lenders Facilitate PPP Fraud?) — A two-part caveat structure that first limits the generalizability within the sample, then limits across settings. More disciplined than listing limitations ad hoc.

17. **Emphasize-Objective-Not-X-but-Y:** "We emphasize that our objective is not to [common but incorrect interpretation], but instead to [actual objective]." (Integrating Factor Models) — Preemptively clarifies what the paper does NOT aim to do before stating what it DOES aim to do. Especially useful when a paper's topic could be misread as claiming something it does not (e.g., proposing a new factor model vs. studying model uncertainty).

---

## 12. Discussing Mechanisms / Channels

**Examples:**

1. "This result suggests an intrapersonal sunk cost mechanism." (Guenzel)

2. "These results are consistent with the asymmetric treatment of good luck relative to bad luck in CEO compensation decisions." (Chen et al.)

3. "We first examine the economic channel, and then investigate the cultural channel." (Doerr et al.)

4. "The effect of zombie credit on CPI growth is driven by (i) high-fixed-cost industries and (ii) national markets for nontradable goods." ("Zombie Credit")

5. "With respect to the cryptocurrency size premium, the findings are potentially consistent with two mechanisms. First, the cryptocurrency size factor may capture the liquidity effect. Second, the size premium is consistent with the trade-off between capital gains and the convenience yield." (Liu et al., "Common Risk Factors")

6. "It is important to note that although we provide evidence in support of plausible mechanisms..., the channels considered are only possible explanations and do not imply a definitive answer." (Liu et al., "Common Risk Factors")

7. **Interaction-as-Mechanism:** "We interpret the interaction between a previous history of anti-Semitism and the effect of Danat's collapse, as well as the differential electoral impact of Danat and Dresdner, as indicative of a cultural channel." (Financial Crisis and Populism) — Template: "We interpret the interaction between [A] and [B] as indicative of [mechanism]."

8. **Common-Cause Clarification:** "Note that our mechanism does not imply causality between connections and performance in any direction. Instead, both higher performance and higher connectedness are caused by more private information." (Clients' Connections)

9. **Model-as-Optics Framing:** "Through the lens of our model, we show that a government that cares about the stability of changes in the exchange rate deviation... finds it optimal to introduce the countercyclical factor." (The Two-Pillar Policy for the RMB)

10. **Two-Mechanism Naming in Introduction:** "The first flexibility mechanism... Another possible mechanism, triangulation, is that..." (Predictably Unequal?) — Names and labels mechanisms directly in the introduction, making them conceptual anchors.

11. **Necessary-Interplay Clarification:** "It should be stressed that [X] alone cannot explain our results. It is the interplay between [X] and [Y] that is necessary for our results." (Axelson and Makarov, "Informational Black Holes") — Explicitly separates a single mechanism from the combined effect of two interacting forces. Crucial when readers might attribute the result to only one of the two mechanisms.

12. **Theory-Practice Alignment:** "This prediction of our theory squares well with practice, where [real-world observation]." (Axelson and Makarov, "Informational Black Holes") — Explicitly links a theoretical prediction to an observed real-world practice. "Squares well with" is a more elegant alternative to "is consistent with" for theory-practice alignment.

---

## 13. Handling Alternative Explanations

**Examples:**

1. "A potential concern for identification is that Danat-connected cities may have already been more vulnerable before the crisis." (Doerr et al.)

2. "One possible concern... To ensure that this explanation is not driving my results... I perform a regression analysis in which I focus on companies and analysts from Eurozone countries. My results continue to go through." (Pursiainen)

3. "Another mechanism one may propose is that entrenched incumbent managers become resistant to making divestitures. While such a channel could help explain general differences... it does not predict the key finding." (Guenzel)

4. "Next, we consider whether the political leanings of CEOs could explain the observed pay for tax windfalls... Taken together, these results are inconsistent with tax windfall-related pay being a reward for supporting the Trump campaign." (Chen et al.)

5. "To mitigate concerns that the negative correlation could be driven by demand shocks, we conduct a robustness check..." ("Zombie Credit")

6. "A related concern is that our results may be driven by Stambaugh (1999) bias... we use a moving-blocks panel bootstrap to assess the magnitude... and find that it is negligible." (Greenwood et al., "Predictable Financial Crises")

7. "It remains possible, however, that these pooled results mask the behavior of a subset of participants who act differently. To address this concern, we reestimate the coefficients... on each participant pool." (Chinco et al., "A New Test of Risk Factor Relevance")

8. **Concession-Dismissal:** "Such confounding factors would have to not only coincide in time with the EDGAR phase-in schedule... but also affect treated (but not control) firms at around the same time as their filings became available online -- which, while not impossible, strikes us as unlikely." (Testing Disagreement Models) — Concede theoretical possibility, then dismiss with epistemic judgment.

9. **Confident Absence-of-Concern:** "Unobserved heterogeneity is not a concern because borrower quality is fixed and collateral quality is directly observable." (Loan Terms and Collateral) — Confidently declares a standard concern inapplicable.

10. **First-Order Concern Flagging:** "A first-order concern with the diff-in-diff analysis is whether wages follow differential trends across small and large firms." (Gender Pay Gap Transparency) — Stronger than "A potential concern."

11. **Overcontrols Warning:** "It is important to emphasize, however, that since household FC debt exposure depresses local economic activity and house prices, controlling for unemployment and house prices overcontrols for the effect of financial distress induced by FC debt." (Financial Crisis and Populism)

12. **Consider-and-Refute Section Framing:** "In this section, we consider and refute potential alternative explanations for our findings that do not require connected clients to have private information." (Clients' Connections)

13. **Concern-Response Pairing:** "A simple comparison of violation outcomes based on lender health raises two main concerns. First, firms that violate covenants and have unhealthy lenders may differ along other dimensions... We attempt to assuage this concern by... Second, violation of a covenant may correlate with other firm characteristics... We address this concern by including..." (The Loan Covenant Channel) — Each concern explicitly labeled and immediately paired with a specific methodological response.

14. **Further-Confounding-Reduction:** "To further reduce the potentially confounding effects of [X], we [methodological step]." (Levine et al., "The Legal Origins of Financial Development") — Signals an additional step beyond the baseline identification to address residual confounding. "Further" acknowledges that prior steps were already taken.

15. **Ruling-Out-With-Direct-Evidence:** "[Alternative explanation] can be ruled out given our finding that [specific evidence]." (Heston et al., "Option Momentum") — A more assertive alternative to "the evidence does not support." The phrase "ruled out" is stronger and signals definitive exclusion rather than mere inconsistency.

---

## 14. Acknowledging Limitations

**Examples:**

1. "One caveat of our analysis is that our estimates represent the local average treatment effect for firms around the 35-employee cutoff." (Bennedsen et al.)

2. "We acknowledge limitations of our research designs that arise because lenders and borrowers do not contract at random." (Chu)

3. "One limitation of my study is that I do not observe possible time-variation in trust bias, as the last Eurobarometer survey was in 1996." (Pursiainen)

4. "The economic benefits that we document, by design due to the available data, are short term in nature." (Kempf et al.)

5. "We do not study the short-term economic benefits of the AI brain drain or its long-term welfare implications. We leave these important questions for future research." ("AI, Education, and Entrepreneurship")

6. "We acknowledge that distinguishing between investors' preferences and their subjective beliefs is imperfect. Notwithstanding, we believe that our findings remain interesting as they suggest that some investors are sufficiently concerned about inequality that their concerns affect stock prices." (Pan et al.)

7. **Candid-Limitation Preview (Upfront):** "We can provide only rough answers to these questions." (Belief Disagreement and Portfolio Choice) — Conversational in register, appears BEFORE the analysis.

8. **Quantification Deferral:** "We leave a proper quantification of this channel to future research." (Import Competition and Household Debt) — Specifies precisely what is left undone.

9. **Stance Deferral:** "At this point, we do not take a stance on the nature of the private information that connection captures. We investigate this question further in Section V.B." (Clients' Connections) — Explicitly brackets a question for later treatment within the same paper.

10. **Candid-Caveat Upfront:** "We simply caveat here that the results of our elementary computations should not be viewed as a precise prediction, but as a useful first step toward assessing magnitudes." (Predictably Unequal?) — A remarkably direct, nearly colloquial admission that manages expectations before presenting results.

11. **Upfront Candid Disclosure:** "We acknowledge limitations of our research designs that arise because lenders and borrowers do not contract at random and borrowers do not violate covenants randomly... Our research designs mitigate this concern, but absent true random assignment... we cannot fully rule it out." (The Loan Covenant Channel) — A standalone paragraph stating plainly what cannot be resolved.

---

## 15. Concluding Your Paper

**Examples:**

1. "In this paper, we propose a new tractable measure of model fragility based on quantifying the dark-matter measure." ("Measuring Dark Matter")

2. "In this paper, we have examined the impact of FinTech credit on entrepreneurial growth." (Cong et al.)

3. "This paper shows that quasi-random changes in acquisition costs significantly predict subsequent divestiture rates of acquired businesses." (Guenzel)

4. "Taken together, our findings support the view that rare disasters are important for asset pricing." (Hirshleifer, Mai, Pukthuanthong)

5. "In sum, our results indicate that financial distress and stricter corporate governance regimes impose significant personal health costs on CEOs." (Guenzel, Hamilton, Malmendier)

6. "Overall, our article provides novel insights into the pricing of debt-related risks in the cross-section of stock returns." (Friewald et al., "Debt Refinancing")

7. **One-Sentence Punchline Opening:** "Cash flow matters. Stock market participants know that firms with higher levels of unhedged floating rate obligations will fare worse in an increasing interest rate environment..." (Stock Market's Assessment of Monetary Policy Transmission) — Opens with a single short, declarative sentence summarizing the paper's core message.

8. **Questions-for-Future-Research:** "Our paper raises a number of interesting questions for future research. First... Second..." (Financial Crisis and Populism) — The paper actively poses questions rather than leaving them open.

9. **Bounded Generalizability:** "We expect that our insights go beyond treasury markets (as confirmed by a follow-up paper...), even if they might not be present in all segments of financial markets." (Clients' Connections) — Balanced scope expansion and boundary acknowledgment in one sentence.

10. **Data-Driven Future Direction:** "As such data sets are becoming increasingly accessible to the academic community, we expect that our approach points to new avenues to better understand the role of private information in financial markets." (Clients' Connections)

11. **Numbered-Specific-Questions Conclusion:** "We leave two questions for future research. First, although factor momentum is consistent with KNS model of sentiment investors, this consistency does not imply that factor momentum must stem from mispricing... Second, although we find no residual momentum net of factor momentum, this result does not conclusively prove that firm-specific returns are serially uncorrelated." (Factor Momentum and the Momentum Factor) — Uses a specific, numbered list of substantive future research questions, each a pointed intellectual question.

12. **Bounded-Effect Conclusion:** "The effectiveness of intervention policies is bounded." (Schilling, "Optimal Forbearance") — States a limit or boundary on the paper's findings. Signals intellectual honesty and realistic expectations. "Bounded" is more precise than "limited" because it implies an explicit upper bound rather than vague insufficiency.

---

## 16. The Roadmap Paragraph

**Examples:**

1. "The rest of the paper is organized as follows. Section I provides historical background. Section II discusses the data. Section III presents the main results. Section V concludes." (Doerr et al.)

2. "The remainder of the paper is organized as follows. Section I discusses our empirical design. Section II presents our main results. Section IV concludes the paper." (Kempf et al.)

3. "The paper proceeds as follows. Section I describes the broadband reform. Section II presents the data. Section III introduces the empirical methodology. Section IV presents the main results." (Broadband Internet)

4. "The remainder of this paper proceeds as follows. Section I provides institutional background. Section II develops the empirical predictions. Section III describes the data. Section IV presents the main results and robustness tests. Section V concludes." (Chen et al.)

5. "The paper is organized as follows. Section I describes the data. Section II examines the cross-sectional return predictors. Section III builds the cryptocurrency factor models. Section IV investigates potential mechanisms. Section V provides additional results. Finally, Section VI concludes." (Liu et al.)

6. "The remainder of this paper proceeds as follows. Section I describes variable annuities and details about their regulation. Section II describes the data construction and summarizes aggregate facts. Section III presents a model of variable annuity supply. Section IV estimates a differentiated product demand system. Section V estimates a model of variable supply. Section VI concludes." (Koijen and Yogo, "Fragility")

---

## 17. Identification and Methodology Framing

**Examples:**

1. **Key-Challenge Framing:** "The key challenge for identifying the role of beliefs in this portfolio rebalancing is that, even if investors held common priors and updated rationally, the election could still differentially change their real hedging needs or overall wealth levels." (Belief Disagreement and Portfolio Choice)

2. **What-Do-We-Gain Rhetorical:** "What do we gain by relying on a 'well-identified' moment as opposed to leverage? In Section V, we compare the two identification strategies in terms of their robustness to misspecification." (Quantifying Reduced-Form Evidence on Collateral Constraints)

3. **By-Definition Logical Necessity:** "By definition, the connection between borrowing and lending and the term structure cannot be made in a representative agent setup and thus departing from such a paradigm is essential." (Risk-Sharing and the Term Structure)

4. **Assumption Defense:** "We view this assumption as realistic given that we are studying a short-run effect of a demand-side shock and the level of aggregation (country-sector) that we use in our empirical analysis." (Stock Market Spillovers via Global Production Network)

5. **Parsimony Claim:** "We build our conceptual framework on a minimum of assumptions, offering an open-economy extension to the work of Ozdagli and Weber (2017)." (Stock Market Spillovers via Global Production Network)

6. **Simple-Approach Claim:** "We develop a simple approach to analyze nonlocal misspecification errors in structural work." (Quantifying Reduced-Form Evidence on Collateral Constraints)

7. **Methodological-Contribution-as-Usefulness:** "We believe this approach is useful for robustness checks in structural estimation, allowing one to explore sources of potential misspecification." (Quantifying Reduced-Form Evidence on Collateral Constraints)

8. **By-Construction Explanatory:** "By construction, OLS maximizes the fit of the model over the in-sample estimation period, which can lead to poor out-of-sample performance." (Anomalies and the Expected Market Return)

9. **Emphasis-Restatement:** "It is worth emphasizing that identification of the effects of U.S. monetary policy shocks on stock returns comes entirely from the time-series variation, as the shocks do not vary by country-sector." (Stock Market Spillovers via Global Production Network)

10. **Inter-Field Methodological Analogy:** "This is analogous to the approach in the interest rate literature whereby the difference between the three-month interest rate and the average overnight rate during the three-month term provides an estimate of the risk premium... A similar idea appears in the literature on the variance risk premium." (Is There a Risk Premium in the Stock Lending Market?) — Explicitly draws methodological analogies to other subfields to legitimize the paper's approach.

11. **Physical Counterfactual Reframing:** "We now compare a PE target's 16oz can of Italian-style green beans in a particular supermarket in Austin, Texas with a can of Italian-style green beans manufactured by another firm but sold in the same store. In other words, we use likely store shelf neighbors as counterfactuals." (Barbarians at the Store?) — The econometric identification strategy is recast in vivid physical terms, making the counterfactual tangible and intuitive.

12. **Primary-Challenge Framing:** "The primary challenge to assessing [causal question] is identifying [specific identification obstacle]." (Levine et al., "The Legal Origins of Financial Development") — Names the key obstacle using "the primary challenge" rather than "a key challenge." The definite article "the" signals that this is the singular, most important obstacle, not one among several.

---

## 18. Null Results and Precision Reporting

**Examples:**

1. **Null-Result Claim:** "The evidence does not support the hypothesis that automatic enrollment increases financial distress." (Borrowing to Save) — A clean, unambiguous null-result claim.

2. **Minuscule + Confidence Interval:** "Automatic enrollment's effect on credit scores is a minuscule 0.001 standard deviation increase, with a 95% confidence interval of [-0.02, 0.03] standard deviations." (Borrowing to Save) — Pairs a precise adjective with the full confidence interval to demonstrate both small magnitude and precision.

3. **Extremely-Tight Interval:** "an extremely tight interval around zero" (Borrowing to Save) — Signals that the null is informative, not noisy.

4. **Causal-Evidence Progression:** "The result that EDGAR inclusion leads to a reduction in both investor disagreement and stock price crash risk suggests but does not prove that disagreement causally affects crash risk. To test for causality, we estimate two-stage least squares regressions..." (Testing Disagreement Models)

5. **Dual-Interpretation of Own Results:** "The two findings above can be interpreted in two ways. First,... Alternatively,... Under the latter interpretation,... Regardless, the apparent increase in the risk premium is limited to the financial crisis period." (Is There a Risk Premium in the Stock Lending Market?) — Presents TWO valid interpretations without definitively choosing.

---

## 19. Policy Implications

**Examples:**

1. **Direct Policy Recommendation:** "Our results also suggest that financial stability policies such as unemployment insurance or mortgage market regulations (e.g., LTV limits) could mitigate future crises." (Import Competition and Household Debt)

2. **Necessary-But-Not-Sufficient:** "Thus, while it is important that investors have access to transparent, pertinent information, disclosure alone is not sufficient to assure good investor outcomes -- how information is displayed influences decisions in ways that can both help and hurt investors." (Attention-Induced Trading and Returns)

3. **Stakes-Heightening:** "A better answer to this question may prove crucial in understanding the dynamics of the next credit crisis." (Loan Terms and Collateral)

4. **Implication Cascade:** "An important implication of these findings is that increased financial distress... not only affects the real economy. Financial distress can also influence political outcomes. A related implication is that inadequate regulation of risky financial products can have far-reaching political implications." (Financial Crisis and Populism)

5. **Policy-as-Narrative-Thread:** Papers that introduce a specific regulation in the opening paragraph and return to it throughout, framing results in terms of whether they "run counter to" or "support" the regulation's objective. (Non-Deal Roadshows; Predictably Unequal?)

---

## 20. Clarifying, Boundary-Setting, and Interpretive Control

**Examples:**

1. **"Should Not Be Construed" Anti-Overinterpretation:** "This evidence, however, should not be construed as suggesting that there is no momentum in stock returns beyond that emanating from factor momentum. A more balanced and measured interpretation of our results is that factor momentum explains a significant portion of stock momentum profits." (Factor Momentum and the Momentum Factor) — Explicitly negates an extreme interpretation, then offers a "more balanced and measured" alternative. Functions as a prohibition on misinterpretation.

2. **"A Clarifying Note" Preemptive Correction:** "A clarifying note about momentum's status as a distinct risk factor is in order. Momentum is distinct from, for example, the five factors of the Fama-French model in the sense that a static combination of these factors does not span momentum. Our contribution is to show that we can capture all of momentum profits by timing other factors." (Factor Momentum and the Momentum Factor) — A standalone paragraph that begins with a deliberate meta-discursive signal to preempt a specific misinterpretation.

3. **"Note the Clear Establishment of Causality Here":** "Note the clear establishment of causality here. We are not looking at the effect of an interest rate change on firm behavior... Rather, our focus is on the effect of changes in interest rates, through changes in cash flows based on firms' balance sheets, on firm behavior." (Stock Market's Assessment of Monetary Policy Transmission) — Explicitly tells the reader what the analysis does and does not establish.

4. **"In Summary" Standalone Pre-Conclusion:** "In summary, our model generates the following novel testable predictions for aggregate stock market returns: (i) the lower the correlation..., (ii) the more likely the relation..., and (iii) the more likely the term structure..." (Stock Market and No-Dividend Stocks) — A standalone "In summary" paragraph that enumerates testable predictions BEFORE engaging with related literature.

5. **"Irrespective of Whether" Ambiguity-Acknowledgment:** "Irrespective of whether [interpretation A or interpretation B is correct], [bottom-line conclusion holds]." — States that a conclusion holds regardless of which of two competing explanations is correct.

6. **"The Picture Is Mixed" Complexity Summary:** "Overall, the picture is mixed." (Predictably Unequal?) — A short narrative pivot that summarizes complex findings without forcing a simplistic conclusion.

7. **Self-Raised Questions About Modeling Assumptions:** "This raises two potential questions. First, what are some (approximate) real-world analogs of the Poisson dividends that are experienced by owners of high-quality assets? And second, is the Poisson payoff structure special, or should we expect similar market dynamics when dividends and information arrive under alternative payoff processes?" (Learning by Owning in a Lemons Market) — The authors raise critical questions about their OWN modeling framework.

8. **Real-World Parameter Mapping:** "In the context of our other examples, housing and construction equipment, it is possible to view the payoff Y in terms of the units of utility... For example, a high-quality tractor might be one that is strong enough to pull a plow through rough terrain..." (Learning by Owning in a Lemons Market) — After presenting abstract model parameters, systematically maps each one to concrete real-world analogs.

9. **Neutrality-Agonistic Statement:** "We do not take a stand on [contested issue]." (Bryzgalova, Huang, and Julliard, "Bayesian Solutions for the Factor Zoo") — Explicitly declares the paper's agnosticism on a question that could invite interpretive controversy. Distinct from "we leave for future research" because it implies the question is deliberately bracketed, not merely deferred.

10. **Indistinguishability-Then-Pivot:** "The remaining two hypotheses, [A] and [B], are impossible to distinguish. We can, however, ask whether [testable implication that holds under either hypothesis]." (Heston et al., "Option Momentum") — Acknowledges that two competing explanations cannot be empirically separated, then pivots to a question that is answerable regardless. A pragmatic response to identification limits that preserves empirical content.

---

## 21. Layered Analysis and Narrative Scaffolding

**Examples:**

1. **"Peel the Onion" Layered Analysis Metaphor:** "To better understand price dynamics and what ultimately drives changes in sales and units, we begin to 'peel the onion.' To peel the onion further, we zoom in to the individual product-store level." (Barbarians at the Store?) — A culinary metaphor deployed repeatedly to signal successive layers of empirical analysis. Functions as a structural organizing device across the entire empirical section.

2. **Layered Selection Concern Hierarchy:** "We first address the following selection concerns with respect to who holds a fund that closes and when the event occurs. (i)... (ii)... (iii)... We next address the following selection concerns with respect to who holds a closing fund at a gain versus a loss: (i)... (ii)... (iii)... (iv)... (v)..." (Fully Closed) — Organizes endogeneity discussions into a hierarchical, multi-level structure.

3. **Analytical Intractability + Numerical Pivot:** "While we are unable to analytically characterize an equilibrium in this setting, in the Internet Appendix, we show through numerical simulation that... just as in the base model." (Learning by Owning in a Lemons Market) — Two-part pattern: honest admission of analytical limits, then pivot to numerical simulation.

4. **Results-Unification Explanation:** "The reason we obtain similar qualitative results in both the preceding models and the base model is that in each case, the owner learns negative information gradually over time." (Learning by Owning in a Lemons Market) — After presenting multiple model variants, identifies the common mechanism that explains why all yield similar results.


---

# Meta-Discursive Interventions

*Extracted from the JF Master Writing Style Guide. These sections document how JF authors explicitly manage reader interpretation, set boundaries around findings, and scaffold layered analysis.*

---

## Section 20: Clarifying, Boundary-Setting, and Interpretive Control

**When to use:** When you need to explicitly manage how readers interpret your results, preempt misinterpretations, or set explicit boundaries around what your findings do and do not show.

**Examples:**

1. **"Should Not Be Construed" Anti-Overinterpretation:** "This evidence, however, should not be construed as suggesting that there is no momentum in stock returns beyond that emanating from factor momentum. A more balanced and measured interpretation of our results is that factor momentum explains a significant portion of stock momentum profits." (Factor Momentum and the Momentum Factor) — Explicitly negates an extreme interpretation, then offers a "more balanced and measured" alternative. Functions as a prohibition on misinterpretation.

2. **"A Clarifying Note" Preemptive Correction:** "A clarifying note about momentum's status as a distinct risk factor is in order. Momentum is distinct from, for example, the five factors of the Fama-French model in the sense that a static combination of these factors does not span momentum. Our contribution is to show that we can capture all of momentum profits by timing other factors." (Factor Momentum and the Momentum Factor) — A standalone paragraph that begins with a deliberate meta-discursive signal to preempt a specific misinterpretation.

3. **"Note the Clear Establishment of Causality Here":** "Note the clear establishment of causality here. We are not looking at the effect of an interest rate change on firm behavior... Rather, our focus is on the effect of changes in interest rates, through changes in cash flows based on firms' balance sheets, on firm behavior." (Stock Market's Assessment of Monetary Policy Transmission) — Explicitly tells the reader what the analysis does and does not establish.

4. **"In Summary" Standalone Pre-Conclusion:** "In summary, our model generates the following novel testable predictions for aggregate stock market returns: (i) the lower the correlation..., (ii) the more likely the relation..., and (iii) the more likely the term structure..." (Stock Market and No-Dividend Stocks) — A standalone "In summary" paragraph that enumerates testable predictions BEFORE engaging with related literature.

5. **"Irrespective of Whether" Ambiguity-Acknowledgment:** "Irrespective of whether [interpretation A or interpretation B is correct], [bottom-line conclusion holds]." — States that a conclusion holds regardless of which of two competing explanations is correct.

6. **"The Picture Is Mixed" Complexity Summary:** "Overall, the picture is mixed." (Predictably Unequal?) — A short narrative pivot that summarizes complex findings without forcing a simplistic conclusion.

7. **Self-Raised Questions About Modeling Assumptions:** "This raises two potential questions. First, what are some (approximate) real-world analogs of the Poisson dividends that are experienced by owners of high-quality assets? And second, is the Poisson payoff structure special, or should we expect similar market dynamics when dividends and information arrive under alternative payoff processes?" (Learning by Owning in a Lemons Market) — The authors raise critical questions about their OWN modeling framework.

8. **Real-World Parameter Mapping:** "In the context of our other examples, housing and construction equipment, it is possible to view the payoff Y in terms of the units of utility... For example, a high-quality tractor might be one that is strong enough to pull a plow through rough terrain..." (Learning by Owning in a Lemons Market) — After presenting abstract model parameters, systematically maps each one to concrete real-world analogs.

9. **Neutrality-Agonistic Statement:** "We do not take a stand on [contested issue]." (Bryzgalova, Huang, and Julliard, "Bayesian Solutions for the Factor Zoo") — Explicitly declares the paper's agnosticism on a question that could invite interpretive controversy. Distinct from "we leave for future research" because it implies the question is deliberately bracketed, not merely deferred.

10. **Indistinguishability-Then-Pivot:** "The remaining two hypotheses, [A] and [B], are impossible to distinguish. We can, however, ask whether [testable implication that holds under either hypothesis]." (Heston et al., "Option Momentum") — Acknowledges that two competing explanations cannot be empirically separated, then pivots to a question that is answerable regardless. A pragmatic response to identification limits that preserves empirical content.

---

## Section 21: Layered Analysis and Narrative Scaffolding

**When to use:** When your empirical analysis has multiple levels of granularity or probes increasingly deeper into the data.

**Examples:**

1. **"Peel the Onion" Layered Analysis Metaphor:** "To better understand price dynamics and what ultimately drives changes in sales and units, we begin to 'peel the onion.' To peel the onion further, we zoom in to the individual product-store level." (Barbarians at the Store?) — A culinary metaphor deployed repeatedly to signal successive layers of empirical analysis. Functions as a structural organizing device across the entire empirical section.

2. **Layered Selection Concern Hierarchy:** "We first address the following selection concerns with respect to who holds a fund that closes and when the event occurs. (i)... (ii)... (iii)... We next address the following selection concerns with respect to who holds a closing fund at a gain versus a loss: (i)... (ii)... (iii)... (iv)... (v)..." (Fully Closed) — Organizes endogeneity discussions into a hierarchical, multi-level structure.

3. **Analytical Intractability + Numerical Pivot:** "While we are unable to analytically characterize an equilibrium in this setting, in the Internet Appendix, we show through numerical simulation that... just as in the base model." (Learning by Owning in a Lemons Market) — Two-part pattern: honest admission of analytical limits, then pivot to numerical simulation.

4. **Results-Unification Explanation:** "The reason we obtain similar qualitative results in both the preceding models and the base model is that in each case, the owner learns negative information gradually over time." (Learning by Owning in a Lemons Market) — After presenting multiple model variants, identifies the common mechanism that explains why all yield similar results.

---

*Source: Extracted from the JF Master Writing Style Guide (Sections 20-21), compiled from 124 published Journal of Finance papers (2022-2025).*


---

# Phrase Bank Reference

*A comprehensive collection of phrase-level resources extracted from 124 published Journal of Finance papers (2022--2025). This file contains high-frequency collocations, hedging phrases, confidence expressions, logical connectors, model description patterns, and the non-academic to JF alternatives table -- organized as lookup references for polishing academic writing to JF standards.*

---

## Section 22: High-Frequency Verb + Noun Collocations

Common verb + noun pairings and verb phrases used throughout JF papers, with usage examples.

| Collocation | Example |
|---|---|
| "provide evidence" | "We provide evidence on the circumstances under which such risk-taking is exacerbated." |
| "document evidence" | "I document evidence of a negative North-South bias." |
| "shed light on" | "Our analysis sheds light on the mechanisms through which FinTech credit affects entrepreneurship." |
| "exploit variation" | "We exploit quasi-random variation in acquisition costs." |
| "mitigate concern" | "This finding mitigates the concern that my results might be driven by differences in information." |
| "address concern" | "To address this concern, we employ a diff-in-disc design." |
| "rule out" | "Our additional tests rule out several alternative explanations." |
| "corroborate" | "These results corroborate the evidence on corporate sunk cost effects." |
| "draw inference" | "This allows us to draw causal inferences about the effect of transparency on wages." |
| "yield results" | "Including the full set of fixed effects yields estimates that are slightly larger." |
| "give rise to" | "The sunk cost hypothesis gives rise to the prediction that firms are less likely to divest." |
| "pose a challenge" | "Risk mismatch... poses a challenge for insurers in the low interest rate environment." |
| "speak to" | "This evidence on how debt maturity relates to the cross-section of stocks speaks to refinancing risk." |
| "touch on" | "The research in this paper touches on several different strands of literature." |
| "point to" | "Tables III and IV point to a fundamental nonlinearity in the data." |
| "account for" | "The three-factor model well accounts for the cross-sectional expected cryptocurrency returns." |
| "play a crucial role" | "Sticky inflation expectations play a crucial role in the results." |
| "sow the seeds of" | "The combination... sows the seeds of its own destruction." |
| "obviates the need for" | "While this obviates the need for the kinds of control variables sometimes included..." |
| "devise tests that differentiate" | "We devise tests that differentiate between the two alternatives." |
| "demystify the workings of" | "We demystify the workings of the countercyclical factor." |
| "bridge different strands of literature" | "We bridge these different strands of the literature by showing the importance of real linkages." |
| "augment existing analyses" | "We augment existing analyses of automatic enrollment by studying household liabilities." |
| "propose a proxy for" | "Our paper proposes a proxy for private information." |
| "curry favor with" | "analysts aiming to curry favor with management" |
| "run counter to" | "our findings suggest that they run counter to Reg FD's stated objective" |
| "level the playing field" | "was introduced to level the information playing field for retail investors" |
| "exercise voice" | "larger institutions often exercise 'voice' through proxy voting" |
| "shed new light on" | "Our results shed new light on the value creation process." |
| "paint a more complete picture" | "To paint a more complete picture of the dynamics of commissions" |
| "exacerbate concerns" | "The secretive nature of NDRs exacerbates concerns" |
| "amplify conflicts" | "amplify analyst conflicts of interest" |
| "resonate with" | "this finding resonates with that of [prior work]" |
| "mirror results for" | "mirroring results for mutual funds" |
| "strikes us as" | "which strikes us as a more appropriate magnitude to consider" |
| "pioneered by" | "The study... is pioneered by Berk and van Binsbergen (2015)" |
| "challenge the view" | "In this paper, we challenge this view." |
| "square well with practice" | "This prediction of our theory squares well with practice." |
| "take a stand on" | "We do not take a stand on the origin of the factors." |
| "strike a balance between" | "We strike a balance between these two concerns by..." |
| "formalize intuition" | "We first formalize intuition for the mechanism in a simple model." |
| "contrast drastically with" | "Our results contrast drastically with common wisdom." |
| "be impervious to" | "The measure is impervious to [confound]." |
| "let the data speak" | "We let the data speak." |
| "carry information about" | "the basis captures information about liquidity demand" |
| "reflect a wedge between" | "The futures-cash basis reflects a wedge between benchmark borrowing rates and the true borrowing rates" |
| "mask the exposure of" | "nonsystematic fluctuations in net repurchases mask the exposure of cash payouts to economic growth risks" |
| "serve as a commitment device" | "tokenization through utility tokens acts as a commitment device that prevents a platform from exploiting users" |
| "internalize the network effect" | "The equity cash flows give the owner the incentive to internalize the network effect" |
| "transcend industry classifications" | "the scope of disruption may transcend industry classifications" |
| "point to a trade-off between" | "These findings point to a trade-off between shielding consumers from certain collection practices and pushing them into higher cost payday lending markets." |
| "sidestep these concerns" | "By using heterogeneous beliefs to model nonfundamental trading, this paper sidesteps these concerns." |
| "underscore that" | "The evidence underscores that the basis captures demand for equity index exposure reflected in both futures and spot markets." |
| "depart from along two dimensions" | "We depart from these papers, however, along two dimensions. First... Second..." |
| "bolster confidence that" | "Having bolstered confidence that the firm-level variation in measured climate change exposure is meaningful, we apply it to four real and financial market outcomes." |

---

## Section 23: High-Frequency Adjective + Noun Collocations

Common adjective + noun pairings used in JF writing to describe results, identification, and theoretical properties.

- "economically significant" / "statistically significant"
- "plausibly exogenous" -- "We exploit plausibly exogenous variation."
- "causal effect" -- "Our identification strategy allows us to estimate the causal effect."
- "robust to" -- "Our findings are robust to a wide range of alternative specifications."
- "suggestive evidence" -- "Earlier work finds suggestive evidence."
- "quasi-random" -- "triggered by quasi-random acquisition costs"
- "incremental" -- "strong incremental predictive power"
- "pronounced" -- "the size premium is more pronounced among coins with high arbitrage costs"
- "striking" -- "A striking change is evident in the beta in recessionary periods."
- "sizable" -- "sizable and statistically significant excess returns"
- "compelling" -- "there is no compelling evidence that..."
- "minuscule" -- "a minuscule 0.001 standard deviation increase" (paired with full CI for precisely estimated nulls)
- "a priori ambiguous" -- "The effect on productivity is a priori ambiguous."
- "first-order concern" -- Stronger than "potential concern"; signals the primary threat to identification.
- "a unique laboratory for" -- "[Setting] is a unique laboratory for understanding [X]."
- "a priori surprising" -- "This result is a priori surprising because funds always have the option to invest passively."
- "an oft-stated view" -- "An oft-stated view in the literature is that many... institutions have little incentive..."
- "daunting challenge" -- "a daunting challenge for which theory offers little guidance"
- "back-of-the-envelope" -- "a simple back-of-the-envelope calculation of potential economic magnitudes"
- "immune to" -- "the estimated average is the only one that is immune to the EIV bias"
- "pervasive" -- "a pervasive activity among brokerages"
- "desirable" -- "The measure has several desirable properties"
- "compelling" -- "There are two compelling reasons from economic theory"
- "bounded" -- "The effectiveness of intervention policies is bounded"
- "impossible to distinguish" -- "The remaining two hypotheses are impossible to distinguish"
- "persistent supply-demand imbalances" -- Describes sustained mismatches between supply and demand.
- "sharp implication" -- "Comparing utility tokens to equity leads to a sharp implication"
- "sufficient statistics" -- "a planner who seeks to determine the optimal tax rate needs to know only two high-level sufficient statistics"
- "corrective theory" -- "this paper has finally provided a robust and an internally consistent corrective theory"
- "unifying feature" -- "The unifying feature of these distributions is that they are readily accessible to investors"
- "broad phenomenon" -- "disruption is a broad phenomenon, negatively affecting incumbent firms across the spectrum"
- "near-comprehensive view" -- "a novel data set that offers a near-comprehensive view of the CLO market"

---

## Section 24: High-Frequency Adverb Combinations

Adverb + adjective/verb combinations for precise qualification of relationships, magnitudes, and comparisons.

1. "significantly more positive/negative"
2. "strongly correlated with" / "strongly predicts"
3. "systematically biased"
4. "materially affect" -- "does not materially affect my main results"
5. "monotonically increasing/decreasing"
6. "broadly interpreted"
7. "virtually no impact"
8. "qualitatively similar"
9. "markedly stronger"
10. "largely unaffected"
11. "potentially consistent with"
12. "Heuristically" -- paragraph-initial intuitive explanation marker
13. "Clearly, there is unlikely to be" -- complexity acknowledgment upfront
14. "Helpfully... Equally helpfully..." -- parallel advantageous-setting adverbs
15. "in a similar vein" -- "In a similar vein, it is important to note that..."
16. "along this dimension" -- "The benchmark model fails along this dimension as well."
17. "at the heart of" -- "motivating the distributional concerns at the heart of our analysis"
18. "of particular interest to" -- "should be of particular interest to policy makers"
19. "beyond the scope of" -- "would require rather complicated machinery... beyond the scope of this paper"
20. "strongly rooted in" -- "Value-added is an intuitive measure that is strongly rooted in economics"
21. "drastically" -- "implications that contrast drastically with common wisdom"
22. "exactly" -- "That is exactly what we provide."
23. "contemporaneously positively/negatively correlated" -- "the basis is contemporaneously positively correlated with futures and spot market returns"
24. "nearly perfectly correlated" -- "it is nearly perfectly correlated with equity returns" (correlation > 99%)
25. "generically optimal" -- "corrective policies are generically optimal"
26. "economically indistinguishable from" -- "generates gross returns that are economically indistinguishable from a broad-based index"
27. "plausibly correlated with" -- "shocks to the time rate of preference are plausibly correlated with news about current and expected future economic growth"
28. "sizably" / "sizable impact" -- "These results highlight the sizable impact of model uncertainty"
29. "remarkably higher" -- "most of the factors display remarkably higher variance through the lens of the integrated model"
30. "inherently local to" -- "optimal tax characterizations are inherently local to the optimum"

---

## Section 25: Hedging Phrases (by Certainty Level)

JF calibrates epistemic commitment carefully. Use stronger hedges for speculative claims, moderate hedges for well-supported claims, and confident phrasing only when the evidence is strong.

### Speculative (tentative possibilities)

- "It is also possible that..."
- "We cannot rule out the possibility that..."
- "One caveat of our analysis is that..."
- "These findings could be due to a variety of factors."
- "We lack power, however, to rule out that these differences are due to chance."
- "It is important to note that although we provide evidence..., the channels considered are only possible explanations and do not imply a definitive answer."
- "It remains possible, however, that these pooled results mask the behavior of a subset of participants."
- "To the best of our knowledge, [factual claim]"
- "which, while not impossible, strikes us as unlikely"
- "We simply caveat here that the results... should not be viewed as a precise prediction"
- "As it is not obvious how to improve on this limitation of our analysis, we leave it for future research."
- "To the extent that bonds are widely held, often by pension funds and retirees, the distributional consequences of this would appear adverse."
- "Although we interpret these results with due caution, they suggest that measurement error in the firm-level dimension is higher than that in the overall panel, but only modestly so."
- "Notwithstanding, we believe that our findings remain interesting as they suggest that..."

### Qualified (confident but carefully bounded)

- "The results suggest that..."
- "These results are consistent with..."
- "It is plausible that..."
- "Our findings line up with a conjecture from..."
- "The findings are potentially in line with two mechanisms."
- "This pattern is plausibly consistent with the investor overreaction mechanism."
- "We cannot determine whether the strategy's profits are due to rational variation in expected returns or to behavioral biases."
- "A working hypothesis is that..."
- "Irrespective of whether [A or B], [conclusion stands]"
- "suggests but does not prove"
- "The picture is mixed"
- "We are not aware of any study that..."

### Confident (well-supported, nearly certain)

- "Our findings indicate that..."
- "These results suggest that internet use spurs a democratization of finance."
- "We interpret these results as causal, consistent with our identification strategy."
- "We view [Figure X] as out-of-sample evidence."
- "the evidence does not support the hypothesis that [X]"
- "Note the clear establishment of causality here. We are not looking at [X]... Rather, our focus is on [Y]"

---

## Section 26: Certainty / Confidence Phrases

Phrases for expressing well-supported conclusions and strong findings.

1. "We establish that municipalities suffered sharper economic declines."
2. "Taken together, the evidence suggests that..."
3. "Overall, we conclude that the cryptocurrency three-factor model well captures the cross section of expected returns."
4. "Our results confirm that the effects are not driven solely by same-country observations."
5. "We show that the German banking crisis not only reduced output, but also had important political consequences."
6. "We find that consumption growth does indeed contain a persistent component."
7. "The bottom line is that at horizons of three years and longer, crises seem highly predictable."
8. "Our estimates imply that two-thirds of the decline in the real interest rate since the early 1980s is attributable to regime changes in monetary policy."
9. "Thus, the evidence appears to be more consistent with an initial underreaction to news."
10. "[X], clearly violating [established theory]" -- "The cash flow exposure... clearly violates the Modigliani-Miller theorem."
11. "This characterization of [X] resolves the perennial question about [Y]"

---

## Section 27: Logical Connectors

Transitional phrases organized by logical function for connecting ideas within and across paragraphs.

**Contrast:** "However" / "In contrast" / "By contrast" / "Nevertheless" / "Although" / "While" / "Yet"

**Addition:** "Moreover" / "Furthermore" / "In addition" / "In particular" / "Specifically"

**Causation:** "Thus" / "Therefore" / "As a result" / "Hence" / "Because"

**Sequence:** "First... Second... Third... Finally" / "Turning to" / "Next" / "Then"

**Summary:** "Taken together" / "In sum" / "Overall" / "The bottom line is that"

**Connecting to literature:** "In this regard" / "In contrast to this work" / "Notwithstanding this evidence, however"

**Transition between analytic sections:** "Shifting from [X] to [Y], a natural question that arises is whether..."

**Returning to motivation:** "In the final section of the paper, we turn to the question motivating our analysis: How high should..."

**Layering explanation:** "To build intuition..." to "To gain further insight into this mechanism..." to "I further express [equation] as..."

**Parallel argument extension:** "A similar argument applies to [X]"

**Digression signal:** "Some remarks regarding [X] are in order."

**Escalating critique:** "To make things worse"

**Restating-before-challenging:** "One may paraphrase [X]'s rationale as follows."

**Detour transition:** "Before proceeding to [X], we take a detour and ask what we find to be an interesting question."

**Intuition marker:** "Heuristically, [explanation]"

**Analogy bridge:** "Loosely, one can think of [X] as being [Y]"

**Metaphor bridging:** "[X] acts similar to a [concept]."

**Concept reframing:** "Through the lens of our model, we show that [X]"

**Analysis escalation:** "Shedding further light on these hypotheses requires a quantitative assessment."

**Natural-extension question:** "A natural question in this regard is whether..."

**Final-analysis transition:** "In a final analysis, we examine..."

**Endogenous-combination statement:** "In reality, [X] endogenously has elements of both [A] and [B]."

**Clarifying intervention:** "A clarifying note about [X] is in order."

**Interpretive boundary:** "This evidence, however, should not be construed as suggesting that [X]"

**Methodological analogy:** "This is analogous to the approach in the [Y] literature..."

**Perspective anchoring:** "To put the numbers in perspective..."

**Disciplinary reframing:** "To put this result in an industrial organization context, industry default dynamics in our sample period are driven more by disruption shocks than by 'standard' shocks."

**Against-this-background transition:** "Against this background, the consequences of our findings are numerous and diverse."

**Starting-point derivation:** "This lack of bond spanning should be a starting point for any equilibrium joint model of exchange rates and bond returns."

**Nomenclature-risk signal:** "At the risk of abusing our nomenclature, we refer to this hybrid cryptocurrency as 'equity tokens.'"

**Perhaps-surprisingly observation:** "Perhaps surprisingly, as climate change is often seen as an aggregate risk factor associated with global changes in the physical climate, its within-sector impact is far from uniform."

**In-doing-so contribution link:** "In doing so, we provide the first large-sample evidence on CLO performance."

**It-follows-that formal deduction:** "It follows that the unconditional average returns of PEPs and PAPs are exactly proportional to their respective eigenvalues."

---

## Section 28: Model Description Patterns

Phrases for describing, motivating, and discussing models and theoretical frameworks.

### When describing a model's structure:

- "The [model/framework] has [N] main ingredients. The first... The second..."
- "A key aspect of the model for explaining... is the evolution of..."
- "The success of the model in explaining these phenomena comes from the product of two forces: (i)... and (ii)..."
- "In the benchmark specification, I make two main assumptions. First... Second..."
- "We build our conceptual framework on a minimum of assumptions"
- "The key theoretical result of our paper is that..."

### When describing the modeling strategy:

- "We first formalize intuition for [mechanism] in a simple [model type] using [method]."
- "To allow [mechanism] to affect the real economy, we extend the simple model to a production economy with distortions."

### When describing what a model implies:

- "Our estimates imply that..."
- "The model parameter estimates imply that..."
- "The model imposes enough structure to identify..."
- "Through the lens of our model, we show that [X]"

### When models cannot be solved analytically:

- "While we are unable to analytically characterize an equilibrium in this setting, in the Internet Appendix, we show through numerical simulation that..."
- "The reason we obtain similar qualitative results in both [model variants] is that in each case, [common mechanism]"

### When mapping models to reality:

- "In the context of our other examples, [real-world domain], it is possible to view the payoff [parameter] in terms of the units of utility... For example, a high-quality tractor might be one that..."

### When raising questions about model assumptions:

- "This raises two potential questions. First, what are some (approximate) real-world analogs of [model feature]? And second, is [modeling choice] special, or should we expect similar dynamics under alternative processes?"

---

## Round 4 Additions: New Verb Collocations (Round 4)

Additional verb + noun/preposition collocations identified from the Round 4 paper expansion.

| Verb + Noun/Preposition | Example |
|---|---|
| shed new light on | "This paper sheds new light on the trade-offs of generous bankruptcy" |
| inform the debate about | "These findings inform the debate about the political economy of central banking" |
| formalize the following insights | "Our analysis formalizes the following insights" |
| overcome the endogeneity issue | "We overcome this endogeneity issue by exploiting..." |
| address the identification challenge | "To address this identification challenge, we use..." |
| exploit quasi-experimental variation | "Exploiting quasi-experimental variation in mortgage payment reductions" |
| reject the null hypothesis | "Taken together, these results reject the null hypothesis that..." |
| rule out alternative explanations | "We do not find evidence that the bunching is driven by..." |
| assess the robustness | "We conduct several additional tests to assess the robustness" |
| conduct additional tests | "We conduct several additional tests to examine whether..." |
| document a discontinuity | "We document that central banks are discontinuously more likely to report..." |
| corroborate the interpretation | "Additional robustness tests provide further support" |

---

## Round 4 Additions: New Adjective + Noun Pairs (Round 4)

Additional adjective + noun pairings from the Round 4 paper expansion.

| Pair | Context |
|---|---|
| long-standing goal | "A long-standing goal of macro finance is to disentangle..." |
| important and timely | "This question is important and timely because..." |
| first-order economic importance | "The answers are of first-order economic importance" |
| nontrivial limitations | "These limitations are nontrivial" |
| disproportionally large | "A disproportionally large number of observations" |
| economically large | "The estimated coefficients indicate that this difference is economically large" |
| compelling theoretical argument | "A compelling theoretical argument suggests that..." |
| competing hypotheses | "Bouwman (2013) rules out three key competing hypotheses" |
| analytically tractable | "A theoretical framework that remains analytically tractable" |
| parsimonious framework | "Our parsimonious framework captures many situations" |
| tractable dynamic framework | "The objective of this paper is to propose a tractable dynamic framework" |
| sharp discontinuity | "We observe a sharp discontinuous jump at the zero-profit threshold" |

---

## Round 4 Additions: New Hedging Phrases (Round 4)

Additional hedging phrases by strength level from the Round 4 paper expansion.

| Strength | Phrase |
|---|---|
| Weak | "is unlikely to be driven by" |
| Weak | "is consistent with the view that" |
| Weak | "can be interpreted as" |
| Moderate | "does not necessarily imply that" |
| Moderate | "admits several possible interpretations" |
| Moderate | "should be viewed as exploratory, rather than as conclusive evidence" |
| Moderate | "plausibly bound the magnitude" |
| Moderate | "arguably be discerned" |
| Strong-with-caveat | "speaks to the robustness of" |
| Strong-with-caveat | "These null effects are informative" |

---

## Round 4 Additions: New Logical Connectors (Round 4)

Additional transitional connectors from the Round 4 paper expansion.

| Connector | Usage |
|---|---|
| by contrast | "By contrast, a disproportionally large number of central bank-year observations just above zero" |
| in sharp contrast to | "In sharp contrast to private firms—central banks do not have a mandate to maximize their profits" |
| taken together | "Taken together, these results reject the null hypothesis" |
| in sum | "In sum, at both the individual-fund level and at the aggregate level" |
| consistent with this interpretation | "Consistent with this interpretation, we will for now restrict the weights" |
| inconsistent with these predictions | "Inconsistent with these predictions, however, we find that total debt declines" |
| instead of the X above | "Instead of the rational explanations above, we find that our results are most consistent with..." |
| even more puzzling | "Even more puzzling, we find that enrolled students with large amounts of credit card debt..." |
| if anything | "If anything, our estimates likely underestimate the frequency" |
| in this regard | "In this regard, the within-firm allocation of resources is analogous to..." |
| consistent with concerns that | "Consistent with concerns that large public companies find ways to make reportable transactions nonreportable" |
| in support of this assumption | "In support of this assumption, we show that treated and control counties are observably similar" |
| as a direct test of | "As a direct test of the impact of stealth acquisitions on consumers, we narrow our focus" |
| in other words | "In other words, optimal contracts should not 'pay for luck'" |
| that is | "MULTIDIVISION FIRMS—THAT IS, FIRMS that operate two or more divisions" |
| to give a sense of this | "To give a sense of this heterogeneity, consider two examples" |

---

## Section 57: Non-Academic to JF Alternatives

A translation table mapping informal or non-academic phrasing to JF-appropriate alternatives. Critical for translation and polishing work.

**Note:** These are directional guides, not mechanical substitutions. Always adapt to your specific context -- the JF alternative may need modification to fit your sentence structure and argument.

| Avoid | Use Instead |
|---|---|
| "A lot of studies show..." | "A large literature documents that..." |
| "We looked at..." | "We examine / analyze / investigate..." |
| "We figured out that..." | "We find that... / Our results indicate that..." |
| "It turns out that..." | "We find that... / Our results show that..." |
| "This is a big deal because..." | "This is economically significant because..." |
| "Old research says..." | "Prior work documents / Earlier studies find..." |
| "We did a bunch of tests..." | "We perform a battery of robustness checks..." |
| "There's no proof that..." | "We find no evidence that..." |
| "It seems like..." | "The results are suggestive of... / This finding is consistent with..." |
| "Basically..." | "In sum... / Taken together... / Overall... / The bottom line is that..." |
| "This paper is about..." | "In this paper, we study / examine / investigate..." |
| "We picked X because..." | "Our empirical strategy exploits... / Our identification relies on..." |
| "The reason is..." | "This result reflects... / The mechanism operates through..." |
| "Pretty much the same" | "Qualitatively similar / Largely consistent / Not materially different" |
| "A really big effect" | "An economically large / substantial / pronounced effect" |
| "We can't say for sure" | "We cannot draw causal inferences... / Our results should be interpreted with caution." |
| "The paper goes like this..." | "The rest of the paper is organized as follows." |
| "This is puzzling because..." | "This presents a puzzle because... / Deepening the puzzle is the fact that..." |
| "We found N things" | "We present N findings. First... Second..." |
| "Our model has two parts" | "Our [model/framework] has two main ingredients. The first... The second..." |
| "Let me explain this simply" | "To build intuition..." |
| "Both sides have a point" | "With these two mechanisms in mind, we let the data speak for themselves." |
| "We connect different literatures" | "We bridge these different strands of the literature by showing..." |
| "Nobody has studied this before" | "To the best of our knowledge, this paper conducts the first analysis of..." |
| "This idea doesn't work" | "The evidence does not support the hypothesis that..." |
| "It's a really precise zero" | "an extremely tight interval around zero" |
| "We explain how X works" | "We demystify the workings of [X]" |
| "We add to existing research" | "We augment existing analyses of [X] by studying [Y]" |
| "We created a new measure" | "Our paper proposes a proxy for [X]" |
| "Six times bigger" | "more than six times larger than the corresponding estimate" |
| "Our results go against X" | "Our findings run counter to [X's] stated objective" |
| "None of the controls matter" | "This obviates the need for the kinds of control variables sometimes included..." |
| "It's a really hard problem" | "a daunting challenge for which theory offers little guidance" |
| "We did a rough calculation" | "A simple back-of-the-envelope calculation of potential economic magnitudes" |
| "It's complicated" | "Overall, the picture is mixed." |
| "We can't solve this model" | "While we are unable to analytically characterize an equilibrium in this setting..." |
| "Here's what I'm not saying" | "A clarifying note about [X] is in order." / "This evidence should not be construed as suggesting that..." |
| "We found a middle ground" | "We find a middle way between trade-offs in existing studies: [A] versus [B]." |
| "This goes against what people think" | "Our results contrast drastically with common wisdom." |
| "The two ideas can't be told apart" | "The remaining two hypotheses are impossible to distinguish. We can, however, ask whether..." |
| "The measure works well" | "The measure has several desirable properties, such as being impervious to [confound]." |
| "There are good reasons to expect this" | "There are two compelling reasons from economic theory to support these expectations." |
| "It's not just X, it's X and Y together" | "It is the interplay between [X] and [Y] that is necessary for our results." |
| "Our theory matches real life" | "This prediction of our theory squares well with practice." |
| "We stay neutral on this" | "We do not take a stand on [contested issue]." |
| "These facts need an explanation" | "These facts require a [X]-based explanation, which we provide." |
| "We can't answer X, but we can answer Y" | "Although this study is unable to speak to [X], it provides [causal/empirical] evidence on [Y]." |
| "It's basically the same as" | "is economically indistinguishable from" |
| "If you look closer" | "Closer inspection reveals that..." |
| "Our method gets around this problem" | "By [methodological choice], this paper sidesteps these concerns." |
| "The findings show there's a trade-off" | "These findings point to a trade-off between [A] and [B]." |
| "This result highlights" | "The evidence underscores that..." |
| "It seems like X but actually Y" | "nonsystematic fluctuations in [X] mask the exposure of [Y] to [Z]" |
| "When you think about it at a high level" | "At a high level, [X] captures the idea that..." |
| "The old debate is about X vs Y" | "The debate centers on whether [X or Y]." |
| "It comes back again and again" | "[X] periodically gains broad relevance after [Y]." |
| "We're not trying to do X" | "We emphasize that our objective is not [X], but instead [Y]." |

---

*Compiled from the JF Writing Style Guide (sections 22-28, Round 4 additions, and Section 57). Updated 2026-06-05.*


---

# Paragraph-Level Patterns (Part C: Sections 29-61 + Round 4)

*Extracted from the JF Master Writing Style Guide. "When to use" intros trimmed to 1 sentence each. All examples and structural descriptions preserved.*

---

## 29. The Claim-Evidence-Interpretation Paragraph

Dominant pattern in JF Results sections.

**Structure:** (1) Topic/Claim sentence, (2) Evidence with table/column references, (3) Interpretation.

**Example (Guenzel, "In Too Deep"):**
[CLAIM] "The first set of results investigates the effect of quasi-random variation in acquisition costs on divestiture rates." [EVIDENCE] "Table III establishes the main result... The coefficient on acquisition cost variation is negative and strongly significant (at the 1% level)." [INTERPRETATION] "This result reveals that an increase in quasi-random acquisition costs reduces the rate of subsequent divestitures, consistent with managers taking sunk costs into account." [ECONOMIC MAGNITUDE] "The coefficient estimate of -0.065 implies that an interquartile increase... is estimated to reduce divestiture rates by 8%."

---

## 30. The Gap-Fill Paragraph

For introductions.

**Structure:** [BROAD] → [NARROWING] → [GAP] → [THIS PAPER]

**Example (Chu, "Loan Covenant"):**
[BROAD] "A LARGE LITERATURE DOCUMENTS THAT the health of the banking sector is important." [NARROWING] "Yet, at the start of the financial panic in 2008, only 10% of bank loans had remaining maturity of less than one year." [GAP] "These observations point to an important gap in our understanding: why do shocks to lenders affect their existing corporate borrowers?" [THIS PAPER] "We document the central role of loan covenant violations in this transmission mechanism."

---

## 31. The Broad-to-Narrow Funnel

Opening of your introduction.

**Structure:** [BROAD] → [CONTEXT] → [NARROWING] → [THIS PAPER]

**Example (Guenzel, Hamilton, Malmendier):**
[BROAD] "Do CEOs pay a personal cost for the demands of their jobs?" [CONTEXT] "A large literature has examined the determinants of CEO compensation." [NARROWING] "Much less is known about how the demands of the CEO position affect managers' personal well-being." [THIS PAPER] "In this paper, we assess the health consequences of being exposed to increased job demands."

---

## 32. The Alternative-Explanation Paragraph

State alternative, test it, show it fails.

**Example (Chen et al.):**
[ALTERNATIVE] "Next, we consider whether the political leanings of CEOs could explain the observed pay." [TEST] "The results in Table VI show..." [REJECTION] "Taken together, these results are inconsistent with tax windfall-related pay being a reward for supporting the Trump campaign."

**Variant: Consider-and-Refute Section Framing**
[FRAMING] "In this section, we consider and refute potential alternative explanations for our findings that do not require [confound]." [ALTERNATIVE 1] "One alternative is that..." [REFUTE 1] "We address this by..." [ALTERNATIVE 2] "Another possibility is..." [REFUTE 2] "However, this explanation is inconsistent with..."

---

## 33. The Surprise-Result Paragraph

For findings that contradict prior work.

**Example (Broadband Internet):**
[PRIOR VIEW] "Pioneering studies suggest individuals who adopted online trading platforms increased trading activity without improved returns." [CONTRAST] "By contrast, we document positive effects of internet use on portfolio efficiency." [EXPLANATION] "We believe our results differ because existing literature documents effects of platforms that aim to make trading easier; broadband internet eases all internet activities."

---

## 34. The Literature-Positioning Paragraph

Summarize related work, differentiate, state your contribution.

**Example (Bennedsen et al.):**
[CITE] "Breza, Kaur, and Shamdasani (2018) show that..." [CITE] "Cullen and Perez-Truglia show that..." [DIFFERENTIATE] "Our paper is distinct from these studies in that they focus on job satisfaction and productivity, whereas we focus on wages and firm outcomes."

**Variant: "Differs Considerably" Comparison**
[ACKNOWLEDGE SIMILARITY] "Our methodology and modeling of [X], and hence many of our results, differ considerably from both of these works, though each paper contains a result that is similar to one of our main cross-sectional results." [PAPER A] "[Paper A] finds... different from our setting because..." [PAPER B] "[Paper B] documents... one key difference is that we show..."

---

## 35. The Puzzle-Resolution Paragraph

State empirical puzzle, explain why standard theories fail, preview how your paper resolves it.

**Example (Bianchi, Lettau, Ludvigson):**
[PUZZLE] "But this leads to a puzzle. Asset pricing theories can generally rationalize such large responses only if market participants believe that something related to monetary policy will have a long-lasting effect on real variables." [STANDARD FAILURE] "Yet the notion that monetary policy shocks could have long-lived effects on real variables is contravened by both foundational New Keynesian macro theories and prior empirical evidence." [RESOLUTION] "One possibility is that some component of monetary policy has long-lasting, first-order effects on the aggregate economy... In this paper, we present new empirical evidence consistent with this hypothesis."

**Variant: Frictionless-Benchmark Puzzle**
[NULL PREDICTION] "In a frictionless world, [X] need not have any predictable relation to [Y]." [EMPIRICAL REALITY] "In contrast, the data clearly show that [Y] rises as [X] drops." [PUZZLE] "Why would [X] systematically predict [Y] in a market where transaction costs should eliminate such patterns?"

**Variant: Contrasting-Facts Puzzle**
[FACT A] "Yet, at the start of the financial panic in 2008, only 10% of bank loans had remaining maturity of less than one year." [FACT B] "Yet bank shocks rapidly affected real outcomes." [TENSION] "These observations point to an important gap: why do shocks to lenders affect their existing corporate borrowers despite the prevalence of long-term credit?"

---

## 36. The Competing-Mechanisms Pattern

Present two (or more) economic channels with opposite predictions, then let data arbitrate.

**Example (Friewald, Nagler, Wagner, "Debt Refinancing"):**
[MECHANISM A] "On the one hand, He and Xiong (2012) show that short-term debt exposes equity holders to debt rollover risk, while long-term debt does not." [MECHANISM B] "On the other hand, short-term debt may increase a firm's financial flexibility... short-term debt mitigates agency conflicts, most notably debt overhang." [PREDICTIONS] "In a nutshell, the first channel suggests that equity risk increases in short-term leverage, while the second channel implies the opposite." [EMPIRICAL ARBITRATION] "Our empirical analysis shows that refinancing risk plays the dominant role in understanding leverage-related equity risk premia."

---

## 37. The Layered-Explanation Paragraph

Build intuition in stages: simple version, deeper version, formal model.

**Example (Gomez-Cram, "Late to Recessions"):**
[SIMPLE] "To build intuition on how the model parameters affect the Kalman gain, I write the Kalman gain for period one, for which we have an analytical expression." [DEEPER] "To gain further insight into this mechanism, I further express [equation] as a weighted average of past excess returns rather than past return surprises." [FORMAL] "I then combine equations (9) and (10) and iterate backward..." followed by the formal derivation.

---

## 38. The Two-Effects Logical Unpacking Paragraph

When a single event or treatment can operate through two complementary channels.

**Structure:**
[SETUP] "Given this difference, [event] has two effects." [EFFECT A] "First, [effect A]... The first effect, if present in the data, is [nature A]. But if [theory] holds, it will not have [implication]." [EFFECT B] "In contrast, the second possible effect involves [nature B], and hence, is a direct test of [theory]."

---

## 39. The Meta-Reflexive Paragraph

Explicitly tells the reader what the analysis does and does not establish.

**Structure:**
[META-CLAIM] "Note the clear establishment of causality here." [NEGATION] "We are not looking at the effect of an interest rate change on firm behavior... Rather, our focus is on the effect of changes in interest rates, through changes in cash flows based on firms' balance sheets, on firm behavior." [DEFENSE] "Individual firms' balance sheets are exogenous to [confound], and hence, our identification comes from [source]."

**Variant: "Should Not Be Construed"**
[FINDING] "[Finding]." [NEGATION] "This evidence, however, should not be construed as suggesting that [extreme interpretation]." [BALANCED] "A more balanced and measured interpretation of our results is that [nuanced claim]."

---

## 40. The Implication-Cascade Paragraph

Builds from direct to broader implications.

**Structure:**
[DIRECT] "An important implication of these findings is that increased financial distress as a consequence of risky lending not only affects the real economy. Financial distress can also influence political outcomes." [BROADER] "A related implication is that inadequate regulation of risky financial products can have far-reaching political implications."

---

## 41. The Generalizability Paragraph

Addresses whether findings extend beyond the specific setting.

**Structure:**
[QUESTION] "Are our findings relevant for other elections, that is, would we expect Democrats and Republicans to trade differently following other major U.S. elections?" [HYPOTHESIS] "We hypothesize that the answer is yes, although we expect these differences to be smaller for elections in which the candidates are more similar..."

---

## 42. The Theory-Testing Paragraph

Derives and tests logical implications of a specific prior theory.

**Structure:**
[THEORY] "An implication of [Author (Year)] analysis is that [prediction]." [SECOND IMPLICATION] "A second implication... is that [prediction]..." [TEST] "We test these predictions..." [RESULT] "...and find that the evidence does not support them."

---

## 43. The Dual-Interpretation Paragraph

Presents two valid interpretations of the same findings without definitively choosing.

**Structure:**
[FINDINGS] "The two findings above can be interpreted in two ways." [INTERPRETATION A] "First,..." [INTERPRETATION B] "Alternatively,... Under the latter interpretation,..." [BOTTOM LINE] "Regardless, the apparent increase is limited to the financial crisis period."

---

## 44. The Vivid-Data-Showcase Paragraph

Pauses analysis to zoom into a single hyper-specific data observation.

**Example:**
[ZOOM IN] "For example, we can see that in the first week of August 2008, 24 cans of Del Monte French-style green beans were sold in a particular store in Chicago at an average price of $1.15 per can." — Exact date, brand, product, location, quantity, and price.

---

## 45. The Taxonomy-Enumeration Paragraph

Systematically differentiates the paper's object of study from a well-known alternative through an exhaustive, numbered list.

**Structure:**
[SETUP] "These [objects of study] differ from [alternative] in [N] important ways." [LIST] "First,... Second... Third... Fourth... Fifth..." — Each difference receives its own paragraph.

---

## 46. The Self-Critique-Then-Defense Paragraph

Candidly identifies a methodological limitation and then immediately argues that the research design addresses it.

**Structure:**
[PROBLEM] "A problem with this approach is that standard industry codes are coarsely defined, and firms in the same broad industry can sell very different products." [DEFENSE] "The granularity of our data potentially reduces this concern: we employ as counterfactuals not only similar firms, but also similar product categories and similar products themselves in the same store."

---

## 47. The Middle-Way Compromise Paragraph

Frames the paper's research design as the optimal middle ground between two opposing methodological poles.

**Structure:**
[SETUP] "We find a middle way between trade-offs in existing studies: clean identification versus a real-world setting and important experiences." [POLE A] "For instance, [Paper A] does [strength A]... but [weakness A]..." [POLE B] "In contrast, [Paper B] does [strength B]... but [weakness B]..." [SYNTHESIS] The paper combines the strengths of both approaches.

---

## 48. The Concern-Response Pairing Paragraph

Organizes identification challenges as an explicitly numbered framework.

**Structure:**
[FRAMING] "A simple comparison raises two main concerns." [CONCERN 1] "First, [concern 1]. We attempt to assuage this concern by..." [CONCERN 2] "Second, [concern 2]. We address this concern by..."

---

## 49. The Peel-the-Onion Layered Analysis Transition

Signals successive levels of empirical granularity using a recurring metaphor.

**Structure:**
[LAYER 1] "To better understand [X], we begin to 'peel the onion.'" [LAYER 2] "To peel the onion further, we zoom in to the individual product-store level."

---

## 50. The Real-World-Parameter-Mapping Paragraph

Systematically maps each abstract model parameter to concrete real-world analogs.

**Structure:**
[QUESTION] "This raises two potential questions. First, what are some real-world analogs of [model feature]?" [MAPPING] "In the context of our examples, [real-world domain], it is possible to view [parameter] in terms of... For example, [concrete example]."

---

## 51. The Analytical-Intractability-Pivot Paragraph

Honestly admits the model cannot be solved analytically, then pivots to a numerical alternative.

**Structure:**
[ADMISSION] "While we are unable to analytically characterize an equilibrium in this setting," [PIVOT] "in the Internet Appendix, we show through numerical simulation that... just as in the base model."

---

## 52. The Results-Unification Paragraph

After presenting multiple model variants, explains why they all yield similar results by identifying the common mechanism.

**Structure:**
[SYNTHESIS] "The reason we obtain similar qualitative results in both the preceding models and the base model is that in each case, [common mechanism]."

---

## 53. The Expectation-Then-Contradiction Paragraph

Builds up an intuitive expectation with theoretical support, then introduces contradictory evidence.

**Structure:**
[INTUITION] "One might expect that when [X], [Y] should improve." [THEORETICAL SUPPORT] "There are two compelling reasons from economic theory to support these expectations. First... Second..." [CONTRADICTION] "Yet, research on 'Z' suggests that [contrary evidence]."

*Note: A three-part structure that makes the contradiction more surprising because the theory supporting the expectation has been explicitly articulated. (Axelson and Makarov, "Informational Black Holes")*

---

## 54. The Necessary-Interplay Clarification Paragraph

Explicitly separates a single mechanism from the combined effect of two interacting forces, preventing readers from attributing results to only one factor.

**Structure:**
[SINGLE-MECHANISM NEGATION] "It should be stressed that [X] alone cannot explain our results." [INTERPLAY ASSERTION] "It is the interplay between [X] and [Y] that is necessary for our results." [ELABORATION] "The winner's curse is present in any standard auction. Yet... This is not necessarily true in our setting."

*Note: Crucial when the paper's contribution depends on the interaction of two mechanisms, not merely their individual effects. (Axelson and Makarov, "Informational Black Holes")*

---

## 55. The Indistinguishability-Then-Pivot Paragraph

Acknowledges that two competing explanations cannot be empirically separated, then pivots to a question that is answerable regardless.

**Structure:**
[ACKNOWLEDGMENT] "The remaining two hypotheses, [A] and [B], are impossible to distinguish." [PIVOT] "We can, however, ask whether [testable implication]." [RESULT] "We find only weak evidence of [implication]..."

*Note: A pragmatic response to identification limits that preserves empirical content. Avoids the trap of claiming to distinguish what cannot be distinguished. (Heston et al., "Option Momentum")*

---

## 56. The Masking-Revelation Mechanism Paragraph

Handles "on the surface X, but actually Y" contradictions where a noise component conceals a true signal.

**Structure:**
[STEP 1] Present the apparent pattern (e.g., total payouts appear acyclical).
[STEP 2] Attribute the contradiction to a masking component (e.g., "nonsystematic fluctuations in net repurchases mask the exposure of cash payouts to economic growth risks").
[STEP 3] Use a model or decomposition to reveal the underlying signal that the noise component was masking.

(How Risky Are U.S. Corporate Assets?) — This pattern is the analytical inverse of the average-masks-heterogeneity pattern (Section 9, item 7). There, the average masked heterogeneity; here, a specific component masks a systematic relationship.

---

## 57. The Trade-off-with-Converse Paragraph

Presents a core trade-off, then shows that extending the model produces the "converse of the key trade-off."

**Structure:**
[FIRST LAYER] Present the central trade-off (e.g., decentralization protects users but prevents cross-subsidization).
[SECOND LAYER] Extend the model (e.g., introduce equity tokens that allow cross-subsidization).
[CONVERSE] Show the extension reintroduces the problem the original trade-off solved (e.g., equity tokens reintroduce the commitment problem).
[TAKEAWAY] The structure of trade-offs is fundamental and cannot be eliminated, only shifted.

(Decentralization through Tokenization) — Deeper than a standard "extensions" section because it shows the trade-off is structural, not incidental.

---

## 58. The Paradigm-Failure-Attribution Paragraph

When the existing literature has repeatedly failed, attributes the failure not to technical limitations but to a fundamental modeling choice.

**Structure:**
[STEP 1] Show the standard method consistently fails to explain key phenomena.
[STEP 2] Argue this is not because the models are insufficiently flexible or the researchers insufficiently skilled.
[STEP 3] Identify the root cause as a fundamental setup error (e.g., the data source itself lacks the necessary information).
[STEP 4] Introduce a new framework that addresses the root cause.

(International Yield Curves and Currency Puzzles) — The most powerful motivation for a new framework: prior failures are not technical but foundational. Use only when the evidence genuinely supports a fundamental attribution.

---

## 59. The Sufficient-Statistics-to-Implementation Bridge Paragraph

Bridges abstract theoretical optimal conditions to implementable policy by identifying "sufficient statistics."

**Structure:**
[THEORETICAL RESULT] The optimal policy depends on parameters that are difficult to measure directly.
[BRIDGE] Identify "sufficient statistics" — a small set of aggregate quantities that encode all the information needed for the optimal policy.
[IMPLEMENTATION] Show that these sufficient statistics can be estimated or proxied from observable data.
[CALIBRATION] Use existing literature estimates to quantify the policy implications.

(Optimal Financial Transaction Taxes) — This pattern is specific to normative/policy papers but generalizable to any theoretical paper that needs to demonstrate practical relevance.

---

## 60. The Novel-Data-Unlock Paragraph

When a novel data source enables answering a previously unanswerable question.

**Structure:**
[UNANSWERABLE QUESTION] Prior literature could not address a key question because of data limitations.
[DATA INTRODUCTION] "We study a data set of [novel data], which are claims on [specific cash flows]."
[IDENTIFICATION ADVANTAGE] "These [data] allow us to hold fixed all of the characteristics of a given firm and vary only [the dimension of interest], and conversely to hold fixed [the dimension of interest] and vary the firm characteristics."
[RESULT] "This type of identification is unique within [subfield], as we usually cannot obtain model-free identification of the role of a given characteristic."

(Duration-Driven Returns) — Distinct from the "laboratory metaphor" because it emphasizes the data's ability to isolate a specific causal channel, not just the institutional setting's suitability.

---

## 61. The Competing-Model-Horse-Race Paragraph

Pits multiple theoretical models against the same empirical facts to show which best explains the data.

**Structure:**
[EMPIRICAL FACTS] Establish the key empirical patterns that need explaining.
[MODEL ENSEMBLE] "We start by conducting return simulations from four workhorse rational expectations asset pricing models."
[UNIFORM FAILURE] "None of these workhorse models is capable of matching the empirically observed [pattern]."
[ALTERNATIVE MODEL] "We finally consider an alternative explanation..."
[PARTIAL SUCCESS] "The [alternative] model can replicate the degree of [pattern] observed in the data."

(Pockets of Predictability) — More persuasive than testing a single model because showing uniform failure across diverse models strengthens the case for a fundamentally different explanation.

---

# Round 4 Paragraph Patterns (2026-06-04)

---

## Question-As-Opening

**Structure:**
[QUESTION IN ALL CAPS] — "DO CENTRAL BANKS AVOID REPORTING losses, and if so why?"
[IMPORTANCE] — "This question is important and timely because..."
[APPROACH] — "In this paper, we address this challenge by..."
[KEY FINDING] — "We document that central banks are discontinuously more likely to..."

**Examples:**
- "DO CENTRAL BANKS AVOID REPORTING losses, and if so why?"
- "How do wage gains affect the borrowing and debt decisions of low-wage workers?"
- "Which characteristics of auctions and the economic environment determine whether auctions are bidder- or seller-initiated?"

The question immediately focuses the reader on the paper's puzzle. Follow with: "This question is important and timely because..." or "The answers to these questions are of first-order economic importance for at least two reasons."

---

## Two-Camp Literature Classification

Classifying the existing literature into two opposing views before positioning your paper.

**Structure:**
[CLASSIFICATION] — "Broadly speaking, the theoretical literature on X can be classified into two camps."
[CAMP 1] — "The bright side theories highlight..."
[CAMP 2] — "In contrast, dark side theories argue that..."
[LIMITATION OF BOTH] — "While these models have been influential, they are subject to two main limitations."
[GAP-FILLING] — "This paper aims to fill this gap by..."

**Examples:**
- "Broadly speaking, the theoretical literature on multidivision firms can be classified into two camps, namely, the 'bright side' and the 'dark side' theories of internal capital markets."
- "Challenges to the replicability of finance research take two basic forms: 1. No internal validity. 2. No external validity."

This structure creates a natural gap: your paper resolves the tension between the two camps, synthesizes them, or shows both are incomplete.

---

## Ruling-Out-Alternatives Summary

A summary sentence that explicitly lists what has been ruled out.

**Structure:**
[PREFERRED INTERPRETATION] — "These results are consistent with the interpretation that central banks manage their earnings to avoid reporting a loss."
[ALTERNATIVE 1] — "However, the discontinuity could also be due to factors other than earnings management."
[REJECTION 1] — "The most likely alternative explanation is that it is an artifact of pooling central banks whose profit distributions are bounded below at zero."
[TEST 1] — "We begin by rerunning the McCrary test after excluding central banks whose profits may be bounded below at zero."
[RESULT 1] — "Removing these central banks from the sample does not change the results."
[TEST 2 + RESULT 2] — "Further, in Figure 3, we examine whether a discontinuity at zero is observed across central banks that appear to differ in the financial risks of their activities."
[CONCLUSION] — "Overall, these results indicate that it is less likely that the discontinuity at zero is a mechanical byproduct..."

**Examples:**
- "These results indicate that it is very unlikely that the discontinuity at zero is simply an artifact of central banks whose profit distributions are likely to be bounded from below at zero."
- "When we consider several nonmutually exclusive alternative explanations, we do not find evidence that the bunching we find below the threshold is driven by (i)... (ii)... or (iii)..."
- "We investigate several rational explanations for the decline in student loan debt. ... We explore and reject numerous other rational explanations."

This pattern provides a comprehensive "negative result" that strengthens the preferred interpretation. The enumeration format (i)/(ii)/(iii) is standard.

---

## Multiple-Explanation Testing with Pivot

Systematically testing multiple explanations before pivoting to the preferred one.

**Structure:**
[PHENOMENON] — "We find that angel tax credits increase the number of angel investments by approximately 18%... However, additional investment flows to older firms, to firms with lower employment growth."
[NULL RESULT] — "Across many approaches, we consistently find null effects that are statistically insignificant and have economically small confidence intervals."
[EXPLANATION TESTING] — "Two mechanisms explain these results: crowding out of alternative financing and low sensitivity of professional investors to tax credits."
[MULTIPLE REJECTIONS] — "We investigate several rational explanations... [reject each in turn]"
[PIVOT] — "Instead of the rational explanations above, we find that our results are most consistent with [behavioral explanation]."

**Examples:**
- "We investigate several rational explanations for the decline in student loan debt. [Tests 1, 2, 3...] Instead of the rational explanations above, we find that our results are most consistent with two behavioral explanations."
- "We explore and reject numerous other rational explanations for the decline in student loan debt. These explanations include [list]. Even more puzzling, we find that..."

This structure is more convincing than testing a single alternative because it shows the preferred explanation survived a gauntlet of alternatives.

---

## Null-Result Robustness Statement

Framing null results as informative rather than disappointing.

**Structure:**
[NULL FINDING] — "We consistently find null effects."
[POWER DEFENSE] — "We conduct a power analysis to determine the smallest effect that could be statistically rejected."
[COMPARISON] — "The estimated effect on the count of young, high-tech firms in our preferred model is -0.3%, compared to a minimum detectable effect at 80% power of 1.9%."
[AUTHORITY CITE] — "[Citation] notes that when a policy is expected to be effective and there is sufficient power, null effects are potentially more informative than significant effects."
[PERSISTENCE] — "Null effects persist across other outcome variables, including..."

**Examples:**
- "Across many approaches, we consistently find null effects that are statistically insignificant and have economically small confidence intervals."
- "Null effects persist across other outcome variables, including..."
- "These null effects are informative. [Citation] notes that when a policy is expected to be effective and there is sufficient power, null effects are potentially more informative than significant effects."

The last template is particularly effective because it cites an authority on the value of null results.

---

## Lower-Bound Claim

Framing results as conservative estimates.

**Structure:**
[RESULT] — "We find that X has effect size Y."
[BIAS DIRECTION] — "If anything, our estimates likely underestimate the true frequency/impact of..."
[JUSTIFICATION] — "This is because [reason the estimate is conservative]."

**Examples:**
- "If anything, our estimates likely underestimate the frequency and impact of M&A antitrust regulation avoidance."
- "Therefore, our estimates likely represent a lower bound on the true effect."

This claim requires justification (explain why the bias is downward). Without justification, it sounds like hand-waving.


---

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

## L. AI-Fingerprint Warning: Quotation Marks and Dashes

When using this skill for polishing or translation, watch for the following AI fingerprints that NEVER appear in published JF papers:

1. **Double quotation marks around technical terms for emphasis:** JF papers use double quotes ONLY for direct quotations, article titles, or the first introduction of a coined term. Never use them for emphasis: wrong -- "stealth acquisitions" (unless you are coining the term), correct: stealth acquisitions.

2. **Em dashes used as sentence connectors:** AI models often create sentences like "The results are robust--across all specifications, we find..." In JF, em dashes are used for parenthetical insertions, not as sentence connectors. Use a period or semicolon instead.

3. **Triple-dot ellipses (...)** in body text: These appear only in direct quotations with omissions. Never use them for dramatic effect.

4. **Overuse of "notably" and "importantly" as sentence starters:** These are used roughly once per JF paper, but AI models insert them every few sentences. If "notably" or "importantly" appears more than once in your draft, delete all but the most important instance.

5. **"This is because" as explanation connector:** While grammatically correct, JF authors prefer "The reason is that..." or simply state the explanation without a connector. "This is because" is slightly informal for JF.

**Key principle:** After AI-assisted polishing, search for these five markers. If any appear more than twice in the entire paper, the text likely reads as AI-generated to an experienced academic reader.

---

*Consolidated from the JF Writing Style Guide master SKILL.md (124 Journal of Finance papers, 2022--2025). Caveats A-I added 2026-06-03 following critical self-reflection on the skill's scope and potential for misuse. Caveats J-L added 2026-06-04 following Round 4 quality review and AI-fingerprint testing.*
