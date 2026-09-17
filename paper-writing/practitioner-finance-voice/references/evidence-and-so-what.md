# Evidence and the Practitioner "So What"

How the corpus handles numbers, definitions, exhibits, and implication. This is the layer that makes a piece *useful to a portfolio manager* rather than just correct. Layer 1 (always on); applies to every transform.

The academic default — "the coefficient is significant (t = 3.41)" then a table — is necessary but not sufficient here. A practitioner piece narrates the number *and* tells the reader what to do with it.

For verbatim sentences to pattern-match, see [exemplars.md](exemplars.md).

---

## 1. Narrate statistics in prose — number, benchmark, verdict, in one breath

Never dump a number naked. Each statistic arrives wrapped in its benchmark, its statistical significance, *and* a plain-English verdict on what it means.

> "SMB has a 1.9% annualized mean return with almost 10% annual volatility, translating into a 0.19 Sharpe ratio. The mean return of SMB over the 1936 to 1975 period, however, is not statistically significant, with a t-statistic of only 1.21." — Size

> "the standard HML approach subtracts −58 basis points (bps) annually (which is statistically insignificant). Our more timely HML factor adds 143 bps (which is statistically significant)…" — HML *(contrast pair with verdicts inline)*

**The four-part pattern:**

| Part | Job | Example fragment |
|---|---|---|
| **Number** | The estimate | "a t-statistic of 1.21" |
| **Benchmark / scale** | What it's measured against | "with almost 10% annual volatility" |
| **Significance** | Statistical read | "not statistically significant" |
| **Verdict** | Economic meaning | "translating into a 0.19 Sharpe ratio" |

Not every statistic needs all four — but a naked number with no verdict is an academic tell. Always supply at least the verdict.

**Report economic magnitude alongside statistical significance.** The user's `paper-taste` skill already requires this; the practitioner voice makes it non-negotiable, because a PM cares about basis points and Sharpe, not asterisks.

## 2. Define jargon inline, in apposition — never make the reader leave the page

The first time a term appears, gloss it in parentheses or a short appositive. The reader should never have to stop and look something up.

| Term, first mention | How the corpus glosses it |
|---|---|
| HML | "often referred to as HML (high minus low)" |
| anomaly | "an anomaly (i.e., a trading opportunity)" |
| Sharpe ratio | "Sharpe ratio (SR, excess return divided by volatility)" |
| information ratio | "information ratio (IR), which is the SR of the alpha" |
| high B/P | "A high B/P means a stock is cheap (or high risk, to efficient market fans) and has a high expected return." |

**Plain-English unpacking for concepts, not just acronyms:**
> "Value is the phenomenon in which securities that appear cheap, on average, outperform securities that appear to be expensive." — Value
> "Before proceeding, it is useful to define factor investing. We define it as a systematic tilting toward a style/theme (and away from its polar opposite) implemented across a diversified set of assets." — Factor

**Do not** over-define. Define on first mention, then use the term cleanly thereafter (this is the `paper-taste` consistency rule). Re-glossing the same term on page 8 condescends.

## 3. Exhibits support the narrative — they do not replace it

Tables and figures hold the detail; **the prose carries the argument**. Every exhibit referenced in text gets a one-line narration of what the reader is looking at and why it matters.

> "Simple eyeballing of Exhibit 6 confirms this claim." — Low-Risk
> "Exhibit 2 clearly shows the historical success of low-risk strategies." — Low-Risk

**The rule:** a reader who skips the exhibits should still follow the argument from the prose alone. If a finding lives only in a table and the text just says "see Table 3," that's an academic tell — rewrite to narrate the result, then point to the exhibit for the detail.

**Worked numerical examples beat derivations.** When the mechanism is subtle, walk through a concrete dollar example instead of algebra:
> "buying $2 worth of safe stocks and shorting $0.67 worth of risky ones, creating an expected excess return of 2 × 10% − 0.67 × 12% = 12%." — Low-Risk

## 4. The practitioner "so what" — every finding gets an implication

This is the heart of the practitioner voice. Every empirical result gets translated into what it means for someone running money: timing, Sharpe, after-cost, drawdown behavior, capacity.

> "If a strategy works only because it has a bigger market beta, then a more efficient and reliable way to capture those returns is simply to allocate more to the market factor itself." — Size
> "investors could have earned the same equity premium as a value-weighted market index with roughly a third lower risk (a beta of 0.67 instead of 1.0 or a volatility of 10% rather than 15%)." — Low-Risk
> "a value timing strategy based on interest rate signals is likely to yield poor out-of-sample performance." — Rates
> "Being able to stick with short-term drawdowns, in order to reap the long-term returns associated with a factor, requires a level of faith and confidence." — Factor

**A reliable test:** after any result paragraph, ask *"so what does a portfolio manager do differently because of this?"* If the answer isn't in the text, add a sentence that delivers it. Common implication frames:
- **Magnitude:** "lower risk for the same return" / "X bps of after-cost alpha"
- **Action:** "allocators should…" / "a timing strategy based on this is likely to…"
- **Behavioral:** "sticking with the strategy through drawdowns requires…"
- **Cost/implementation:** "after transaction costs" / "the breakeven fee is…"

The corpus also **calls out practitioner bad habits by name** — this is fair game and reads as candid, not rude:
> "all too often we still see practitioners presenting results based on raw returns even when the factor exposure is large and intuitive." — Size

## 5. Citations — light, narrative, never a wall

In-text author-year (parentheses or brackets — match the outlet's style). Keep density light; cluster related citations; prefer the narrative form ("Banz (1981) documented that…") over a parenthetical dump.

> "Banz (1981) documented that small stocks outperformed large stocks over his sample period, which spanned January 1936 to December 1975." — Size *(narrative)*
> "Harvey, Liu, and Zhu (2016) document more than 300 factor discoveries in the literature…" — Factor *(narrative)*
> "(Fama and French 2007; Shleifer 2000; Thaler 2003; Barberis 2018)" — Factor *(clustered)*

**Do not** build a citation wall — three or more parenthetical citations stacked behind every sentence is an academic tell. Cite the 3–5 papers that actually anchor the claim; move the rest to a footnote or cut them.

## 6. Discursive footnotes for provenance and asides

Push digressions, data provenance, and methodological caveats into numbered footnotes so the main text stays lean. The corpus footnotes are long, often witty, and frequently the most-cited part of the paper.

**Data provenance footnote** (very common — practitioners want to replicate):
> "See Banz 1981, Keim 1983, and Roll 1983." — Size
> Name the public data library so a reader can reproduce the result: Ken French's data library, the AQR data library, etc.

**Biographical / historical aside:**
> Fischer Black "stomped out" of the Wells Fargo meeting that rejected low-risk investing — "the day alpha died." — Low-Risk

**Self-aware methodological caveat:**
> "We could choose to describe something as a 'fact' or 'fiction' at will… We choose the framing we think most intuitive but recognize it is an arbitrary decision." — Factor

(Full guidance on witty footnotes is in [structure-and-framing.md](structure-and-framing.md) §6 — that's a Layer 2 move; provenance and citation footnotes here are Layer 1.)

## 7. Replicability ethos — say how to reproduce it

Practitioner readers want to rebuild the result. The corpus repeatedly stresses that tests use "the most well-known and straightforward publicly available data" and explicitly names the data library. When the user's draft describes data or method, make sure the prose tells the reader *where the data comes from* and *that it is reproducible* — without turning into a methods manual.

---

## Quick self-check (evidence layer applied?)

- [ ] Does every reported statistic carry a verdict (significant / not / economically meaningful) inline?
- [ ] Is every piece of jargon glossed on first mention?
- [ ] Can a reader follow the argument from the prose alone, without opening the exhibits?
- [ ] Does every result paragraph end with a "so what" for a portfolio manager?
- [ ] Are citations clustered and narrative, not walled?
- [ ] Does the data section tell the reader where the data comes from and that it's reproducible?
- [ ] Did I preserve the author's actual numbers and claims verbatim — changing voice only?
