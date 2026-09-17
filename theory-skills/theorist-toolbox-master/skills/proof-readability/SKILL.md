---
name: proof-readability
description: Improve the readability and exposition of mathematical proofs that are
  already verified as correct, without changing their mathematical content. Use when
  the user asks to polish, edit, or improve the readability/exposition/presentation
  of a proof, lemma, or appendix; after a co-math prover/reviewer cycle accepts a
  proof; or on "make this proof readable", "polish this proof", "improve the
  exposition", "readability pass".
---

# Proof readability

Edit verified proofs so a reader can follow them without reconstructing steps, chasing broken references, or decoding notation. This skill sits **above the prover**: it runs *after* a proof has been written (e.g., by `math-proof` or a co-math `prover` workstream) and *after* its correctness has been verified (by a reviewer, Lean, or the user). It is an exposition pass, not a proving pass.

## Position in the pipeline

```
prover / math-proof  →  verification (reviewer, Lean, user)  →  proof-readability
        (correctness)              (acceptance)                  (exposition only)
```

**The prime invariant: never change the mathematics.** Every edit must be content-preserving — reorder, signpost, expand, annotate, rename consistently, fix references and typos. Do not strengthen, weaken, or "simplify" any claim; do not replace an argument with a different one; do not silently fill what you believe is a gap with new mathematics.

**If you find an actual gap or error while editing, stop editing that proof and flag it.** Report the suspect step precisely ("the inequality in Eq. (3) silently uses FOSD via Eq. (1); I cannot verify it from the stated assumptions") and route it back: in a co-math project, return the workstream to the prover; otherwise tell the user. A readability pass that quietly patches math defeats the verification that already happened.

**In a co-math project** this skill is wired into the workflow (see the agent definitions in `~/.claude/agents/`): the `project-coordinator` dispatches a `W{NNN}-readability-{slug}` workstream after a prover/lean-prover workstream is APPROVED (its "Phase 4.5: readability pass"); the `prover` executes it in **readability mode** following this skill; and the `paper-reviewer` reviews the result for *content preservation and plumbing only* — statement preservation, no new mathematical claims beyond reported derived lines, no contested edits applied. Scope is strictly the approved proofs named in `instructions.md`.

## Guiding principles

- **Minimize the reader's work** (Lee): every edit is judged by whether it reduces what the reader must reconstruct, look up, or hold in memory.
- **Readers are human** (Hwang): "We get tired, we forget, we skim when we should scan. Write accordingly." Judicious redundancy is expository error-correction, not padding; "mathematical prose should not be an access barrier a reader must overcome to prove their worthiness."
- **The detail criterion** (Lee): omit a step only if it would be obvious *to this audience* how to fill it in; if it wasn't obvious to the writer at first, something needs to be said. Aim for "just enough to give the reader the Aha! experience that makes the rest obvious."
- **Be accurate even when imprecise** (Hwang): informal glosses and intuition sentences must be literally defensible, not merely morally true.

## The six-layer pass

Work through these layers in order. Layers 1–2 are structural (read the whole proof first); layers 3–6 are local.

### Layer 1 — Architecture

- **Three-layer presentation for main results.** Main text: statement + short proof sketch + an intuition paragraph outside the proof environment ("The intuition behind this result is as follows…"). Formal proof in the appendix. State explicitly where each proof lives ("The proof of Proposition 3 is in Appendix C").
- **Restate before proving.** When a proof is deferred to an appendix, restate the result verbatim immediately before its proof. Open a proofs appendix with a notation-recap block (a short glossary plus the pre-derived equations the proofs reuse).
- **Gloss-then-state.** Precede every lemma with one or two plain-language sentences giving what it says and its role in the main proof: "The next lemma shows that the threshold is monotone in q; this is the engine of Theorem 2."
- **Close composite proofs explicitly.** When a theorem is assembled from lemmas, end with a wrap-up sentence — "Combining Lemmas 1, 2, and 5 establishes Theorem 2" — and a QED. The end of every proof must be unmistakable, so the reader needs no mental backtracking to confirm all obligations are discharged.
- **Factor exact duplicates.** "A lemma is to a proof what a subroutine is to an algorithm" (Hwang). If a long derivation is repeated with cosmetic substitutions (hats, bars, swapped indices), extract one symmetric lemma and instantiate it twice. (Coarser re-chunking of the lemma structure is a contested edit — see below.)
- **Prose order = logical order, or motivate the inversion.** Reorder so each statement follows from what immediately precedes it or from something much earlier — avoid jumping around. When a hard auxiliary lemma must be proved before its use, add a motivating sentence first, or its appearance "could seem arbitrarily magical."
- **Self-contained statements.** A lemma must be readable in isolation: restate the objects and quantifiers in the statement itself ("Let w ∈ W and let w′ be the η-coarse contract of Definition 3…"), never inherit them silently from a page of surrounding prose. No theorem statement may read as *false* in isolation because of an off-page standing convention; if hypotheses pile up, bundle them into a named definition ("a *regular* economy is one satisfying…").
- **Labels signal role.** Theorem = important result; Proposition = interesting but lesser; Lemma = a tool for proving something else; Corollary = follows easily from the preceding result. Check each label matches the result's role.

### Layer 2 — Signposting

- **Architecture opener.** The first sentence of every proof states the method and plan: "The result is established in two steps: first we show X; then we use X to bound Y." "We prove the contrapositive." "By Lemma 2 it suffices to prove the claim for t′ = 1." Any non-direct method (contrapositive, contradiction, induction) must be declared within the first lines.
- **Named steps for long proofs.** Any proof over roughly half a page gets numbered or named steps, each opening with what it will show, and a closing recap reciting which step delivered which piece ("the first bound came from Step 1; the tighter bound from Steps 2–3").
- **Roadmap counts must match the body.** "We split the proof into three cases" followed by four cases, or step numbers that contradict the prose, is worse than no roadmap. Verify every announced count and every "by step 1" pointer.
- **Enumerate cases up front.** State all cases, confirm they are exhaustive and mutually exclusive, label them (Case I, Case II, … with explicit parameter ranges), then prove each.
- **Mark where assumptions open and close** (Gro-Tsen). "We temporarily assume x > 0. … This concludes the case x > 0." In a long case or induction, drop reminders: "still working under the assumption that x > 0," "recall the inductive hypothesis gives…". The structure must be visible even to a reader skipping the details.
- **State the purpose of every assumption.** Always "assume toward a contradiction that…" — never a bare assumption the reader can't classify as to-be-refuted versus a genuine case. Flag atypical branches: "we first handle the degenerate case where…".
- **Goal statements before algebra.** "It remains to show that w′(i) ≤ 2H." "We want to show the left-hand side is smaller than 1." The reader should know the destination before wading in.
- **Meta-comments that don't participate in the logic** (Abou Samra): announce the technique ("we construct A by diagonalizing over all strategies"), flag surprises ("we cannot apply Dijkstra's algorithm directly because…"), preempt natural questions ("one could show a₁ already works, but this argument is simpler"). Keep them to a sentence or two; longer asides move before or after the proof.

### Layer 3 — Line-level justification

- **Every assertion has a visible status** (Sundstrom): assumption of the theorem, previous step of this proof, previously proved result, definition, axiom, or well-known background fact — these are the only legitimate justifications (Lee), and the reader must be able to tell which one each line uses. Omit the citation only when it is genuinely more effective unstated for this audience.
- **Every inequality gets a named reason at the line where it occurs** — an assumption, lemma, equation number, or one-clause argument ("by convexity of r⁻¹"). A trailing "where the second and third inequalities follow from…" clause is acceptable only if it covers *every* relation in the chain; an uncited step two displays later is the failure mode to hunt for.
- **Every sign, monotonicity, or limit claim gets a one-clause justification.** "The derivative is negative" → "negative, since each factor is positive and (2q−1) > 0." Bare declaratives like "the expression above is positive for every q" are the single most common stumbling block — expand each one or point it at a lemma.
- **Instantiate cited theorems at the call site** (Gro-Tsen): don't just write "by Theorem 3.1 of [12]" — say what each of the theorem's quantified variables is in the present context, like passing arguments to a function. When importing an external result, restate it in this paper's notation; cite with precise pointers ("[12, Theorem 3.1]", never "by [12]").
- **Chain discipline** (Lee): write a = b = c = d only when the steps are provable in the order shown; transitive relations may mix (a ≤ b = c < d) but never a ≤ b ≥ c, and never chain ≠. In displayed derivations, align the relation symbols vertically and do not repeat an unchanged side.
- **Narrated algebra: one display per transformation,** each prefaced by an active-voice sentence: "Rearranging, we get," "Factoring out common terms," "Substituting m̄ = αn," "As n → ∞, the second term vanishes, so". Break unbroken page-width algebra blocks into this rhythm.
- **Expand compressed steps.** "By plugging this into Definition 2 we get…" costs the writer one displayed line and saves every reader the reconstruction. Same for skipped telescoping sums, omitted LP solutions, and "which is simply…" closed forms: show one intermediate line or name the cancellation.
- **Display and number key derived quantities.** A formula that the proof leans on (a threshold, a cutoff, a closed form) must not arrive as a dense inline fraction; display it, number it if it is ever referenced again, and show the one-line derivation that produced it.

### Layer 4 — Notation hygiene

- **Dual-code definitions** (Gro-Tsen): state each definition in symbols *and* in words — "let P := {x ∈ ℝ : x > 0} be the set of positive real numbers." The verbal gloss is an error-correcting code; "a misunderstood definition often makes all that follows unrecuperable."
- **Define before use, once, in a visible place.** Every symbol is either previously defined or quantified, at the latest within the sentence where it first appears (Lee). Proof-local objects (ad hoc sequences, mid-proof abbreviations like δ(μ, q, γ)) get an explicit displayed definition, ideally collected at the proof's start rather than minted mid-sentence.
- **No notation dumps.** Introducing four symbols at once followed by an asserted identity is the anti-pattern; introduce one symbol at a time with a purpose clause ("let η_q denote the contribution of high-signal players to the numerator").
- **Restate object types and names on reuse** (Wintz): "Thus, the vector x solves the optimization problem in (2)" beats "Thus, x solves (2)" — it saves the reader a back-search and avoids opening a sentence with a symbol. Likewise recall decorated notation at the point of use: when r̄ or J̄_B reappears pages after its definition — especially alongside its undecorated twin — append "(the ranking under truthful bidding)".
- **Use descriptive names alongside numbers** (mlk): "combining the monotonicity formula (7) with the reduction Lemma 3.13" — five extra words and the reader immediately feels what is going on, instead of cross-referencing three bare numbers.
- **Naming hygiene** (Rüping): keep names stable across sections (a group called G stays G); use parallel names for parallel objects (W ⊂ V and W′ ⊂ V′); never double-book a letter (k as field and as index); don't name what is used only once ("For every vector v…" needs no "Let V be a vector space" if V never recurs).
- **Describe constructed objects in words, not encodings** (Abou Samra): "the graph H obtained by removing vertex v from G," not H := (V_G∖{v}, {e ∈ E_G : v ∉ e}).
- **Prefer unambiguous symbols:** ⊆/⊊ over bare ⊂ where the convention is not fixed, ⌊x⌋ over [x], gcd(a, b) over (a, b).
- **Audit consistency mechanically:** argument orders of multi-argument functions (φ(γ, n, k) vs φ(γ, k, n)), ε vs ϵ, subscript slips (μ_n for μ_{t′}, s₂ for s₃), subsequences taken but never renamed (lim sup silently becoming lim), bounds that differ between a statement and its appendix restatement, variant spellings ("finite dimensional" vs "finite-dimensional").
- **Abbreviate repeated parameter lists.** After the first full appearance of x*(q_i, q_j, μ_i, μ_j, γ_i, γ_j), declare "we write x* for short" and use the short form; a monotonicity claim drowning in six-argument lists is unreadable.

### Layer 5 — Intuition

- **One intuition sentence after each key derivation,** connecting the math to the model: "The threshold drops because no-votes carry less information, so fewer yes-votes suffice to outweigh them."
- **An intuition paragraph after every main theorem,** outside the proof environment, possibly with a concrete narrative (extreme cases, an Alice/Bob story, a toy example with a table).
- **"In words" translations** after dense formal statements: "In words, Corollary 1 states that if the price is moderate, the probability the campaign succeeds in state H approaches one."
- **Provide what the reader would have to draw or compute** (Latapy): if following the proof requires sketching a region, tabulating cases, or tracking a small example, supply the figure, table, or worked instance. After a long proof, consider a short walk-through on a concrete example.
- Keep intuition **segregated from the formal argument** — before the proof or after the QED, never interleaved with the algebra in a way that blurs what is proved versus what is motivated. Every informal gloss must be literally defensible (no "f(x′) is close to f(x)" when the true statement is a limit).

### Layer 6 — Sentence and formula grammar

The line-by-line mechanics, mostly from Lee's *Some Remarks on Writing Mathematical Proofs*:

- **Complete sentences in paragraphs.** Every formula functions grammatically as a noun (an expression) or a clause (a relation, whose verb is the relation symbol); a formula cannot stand alone as a sentence. Sentences end with punctuation — including a period after a sentence-ending displayed equation.
- **Never begin a sentence with a mathematical symbol.** Reword: "f is continuous" → "The function f is continuous."
- **Never let two formulas meet with only punctuation between them.** "If x ≠ 0, x² > 0" → "If x ≠ 0, then x² > 0."
- **Relation symbols connect formulas, never words.** "a number that is > 2" is banned; write "a number greater than 2" or "a number x with x > 2."
- **Logical symbols (∀, ∃, ⇒, ⇔, ∧, ∨, ∴) become English words in prose.** "For every," "there exists," "implies." ⇒/⇔ are tolerated only between fully symbolic statements or statement labels ("we prove (a) ⇔ (b)"), never splicing English clauses.
- **No blackboard abbreviations in formal text:** "s.t.", "w.r.t.", "w.l.o.g.", "iff" — write them out. Use "i.e." and "e.g." correctly or not at all. Don't double a connective word with a symbol ("Since x ∈ V → x has a magnitude" uses two connectives for one).
- **No computer notation:** no * for multiplication, no ^ for powers, no slashed complex fractions — display them. Roman type for operator names (sin, log, gcd), italics for variables, consistent fonts (a symbol must look the same at every occurrence).
- **No ambiguous pronouns** (Hwang): every "it"/"this" has an unmistakable antecedent — "if you aren't sure what noun 'it' refers to, there is an important detail you don't understand."
- **Prefer positive statements to negated ones** (Wintz): "There is no solution x with x > 0" → "Every solution x satisfies x ≤ 0."
- **Untangle "respectively" and parenthetical (resp.) constructions** into serial clauses when they force the reader to zip two lists.
- **Two read-tests:**
  - *Read-aloud test*: expand each relation symbol to its verb phrase and check the sentence is grammatical ("let x < y be real numbers" fails — it reads "let x is less than y be real numbers").
  - *Knuth's "blah" test*: replace every formula with "blah" and check the surrounding prose still makes sense, because readers skim equations on a first pass. If the prose collapses, add connective words.

## Banned phrases and their replacements

| Found | Replace with |
|---|---|
| "Clearly," / "Obviously," / "It is easy to see" | The one-line argument, a pointer to the definition/lemma that makes it immediate — or often just **delete the word**: "f is obviously integrable because it is continuous" → "f is integrable because it is continuous" |
| "It is straightforward to see/show" | The displayed computation (it is usually one line) |
| "It can be seen that…" / "we are able to show that…" | Delete the filler; state the fact with its reason |
| "naturally follows" / "readily follows" | "follows from [named result] because [one clause]" |
| "The proof of (b) is similar and omitted" | One sentence naming exactly what changes: "identical with the inequality on price reversed, since a seller gains when p > vᵢ" |
| "Similar arguments apply to the case…" | Same — name the substitution or sign flip that maps the proved case onto this one |
| "one can see that…" / "we get that…" (over a gap) | The intermediate line |
| "this leads to a contradiction" | The two incompatible statements, side by side |
| "A dominates B" (unproved) | The inequality, or an explicit flag that it is a verified-elsewhere fact with a pointer |
| "See the proof of Lemma X" (as an entire proof) | A one-sentence extraction of the relevant fact from Lemma X's proof, plus the pointer |
| "by [12]" (bare citation) | "[12, Theorem 2.7.6]" — and instantiate the theorem's variables at the call site |

Note: a verified proof may legitimately omit a symmetric case — the verification covered it. The readability edit is to *say what changes*, not to doubt the omission.

## Contested edits — propose, don't apply

These changes are recommended by some style authorities and disputed by others, and all of them border on changing content. Never apply unilaterally; list them as suggestions in the report and let the user (or prover) decide:

- **Converting a proof by contradiction into a direct proof.** Sometimes more readable (Rüping), but it is a different argument — and the contradiction form may have been chosen deliberately (grinberg: the direct form's real benefits are reusability and constructivity, not readability).
- **Re-chunking the lemma structure** (merging fragmented lemmas, splitting a monolith). Useful tests: split off a lemma only if a reader could easily imagine an instance of its hypothesis (grinberg), or if it would be cited again (Dotsenko). Over-fragmenting destroys readability too.
- **Adding, removing, or rewording standing assumptions,** including bundling hypotheses into a new named definition — touching hypotheses is touching content. The content-safe portion (repeating an existing convention where it is load-bearing) is Layer 2 work.
- **Reordering an equality/inequality chain** so steps are provable in the order shown — verifying the new order is provable is a correctness judgment.

## Mechanical lint (always run, last)

These are cheap checks that catch the errors that most erode reader trust:

1. **Cross-reference types**: every "Theorem n" / "Proposition n" / "Lemma n" mention points to an object of that kind (mislabeling propositions as theorems is a recurring real error). No equation cites itself; every \ref resolves.
2. **Proof environment boilerplate**: no "Proof. Proof." doubling; one consistent terminator throughout (□ or Q.E.D., never mixed); QED not glued inside a displayed equation; `\qedhere` where a proof ends in a display.
3. **Counts**: announced number of steps/cases equals the number delivered; enumerated list numbers match prose references ("by step 2").
4. **Statement/restatement equality**: an appendix restatement is verbatim identical to the main-text statement (bounds, indices, quantifiers).
5. **Typos in math-adjacent prose**: "than/then", "principle/principal", "the the", agreement errors, unmatched parentheses, sentences starting mid-thought ("Where the last inequality holds…", capitalized, as a fragment) — fold fragments into the preceding display's sentence. Treat every typo as a smell: "a typo usually signals a section that hasn't been looked at enough" (grinberg) — re-read its surroundings.
6. **Footnoted rigor**: a footnote that is *required* to verify a step gets promoted into the proof body; footnotes are for caveats and asides only. Footnote anchors must not be placeable as exponents (ℝ³ vs. footnote 3) — move the anchor to text.
7. **Symbol audit**: every symbol used is defined earlier; no letter double-booked; no math symbol immediately following a punctuation mark; ambiguous comma lists ("a ≤ b, c ≤ d") disambiguated with words. Flag undefined symbols (do not invent a definition — that is a content change; ask or route back).

## House style (match the author's voice)

Edits should read like the surrounding text, not like a different author. The house fingerprints to preserve:

- First-person plural narration ("We construct…", "We now show…") — "we" means the writer and reader doing the mathematics together; never "I" in proofs. Active voice, short sentences, one idea per sentence.
- Stock connectives: "Note that", "Recall that", "That is,", "To that end", "It remains to show", "as required", "Combining both results".
- Display-dominant math: any multi-term expression or relation chain gets a display; inline math only for single symbols and parameter ranges. Derivation chains as aligned displays, one transformation per line, introduced by a short prose clause ending in a colon or comma.
- `\triangleq` (≜) for definitions; selective equation numbering (number only what is referenced later; numbered equations are always displayed; "equation (7)" lowercase in running text).
- Contradiction proofs announced ("Assume by contradiction that…") and closed by exhibiting the contradiction.
- Intuition paragraphs placed outside proof environments.
- Replace non-idiomatic connectives where they appear ("From this we entail" → "It follows that"; "we get that" → "we obtain").

## Workflow

1. **Confirm verified status.** This skill assumes correctness is already established. If the proof has not been through a prover/review cycle (or the user hasn't vouched for it), say so and offer `math-proof` / the co-math pipeline instead.
2. **Identify the audience.** The detail level, which justifications may go unstated, and how much background to gloss all depend on who reads this (journal referees in the field vs. an interdisciplinary venue vs. students). Default for the user's papers: economics/game-theory journal readers.
3. **Read the entire proof and its context** (statement, the results it cites, the results that cite it) before editing anything. Build a small dependency map: which lemmas feed which theorems, which equations are reused.
4. **Pass 1 — Architecture & signposting** (Layers 1–2): placement, restatements, glosses, openers, steps, case enumeration, assumption open/close markers.
5. **Pass 2 — Lines & notation** (Layers 3–4): justify every relation and sign claim, narrate algebra, expand compressed steps, instantiate citations, fix notation.
6. **Pass 3 — Intuition** (Layer 5): add the missing intuition sentences, "in words" translations, and any figure/table/example the reader would otherwise have to produce.
7. **Pass 4 — Grammar & lint** (Layer 6 + Mechanical lint): run the read-aloud and "blah" tests on edited passages, then the lint checklist.
8. **Report.** Summarize the edits grouped by layer, list the contested edits as proposals, and separately list (a) any spots where you suspected a mathematical gap and deliberately did **not** edit — these go back to the prover; (b) any expansion where you had to derive an intermediate line yourself — these need a correctness re-check, since even "obvious" filled-in algebra is new content. In a co-math project, suspected gaps mean the workstream returns to `prover`; the readability edit is re-reviewed by `paper-reviewer` for plumbing (references, compilation), not re-proved.

## What NOT to do

- Do not alter any theorem, lemma, or definition statement beyond making it self-contained — and if making it self-contained requires choosing quantifiers or hypotheses that were ambiguous, ask rather than choose.
- Do not replace a verified argument with a "cleaner" different argument.
- Do not delete steps to shorten a proof — this skill adds clarity, it does not compress rigor. But do cut *empty* filler: padding sentences, "wishy-washy" conceptual asides irrelevant to the logic, and prose that merely rephrases adjacent symbols add length without informing.
- Do not resolve an undefined symbol by guessing its definition.
- Do not let added intuition smuggle in claims the proof does not establish ("this is because the effect dominates" is a new claim unless proved), and keep every informal gloss literally defensible.
- Do not apply a contested edit (contradiction→direct, lemma re-chunking, assumption changes, chain reordering) without explicit approval.
- Do not mark the pass complete while any banned phrase, unresolved reference, or unjustified sign claim remains — or explicitly list the survivors and why they were left.

## Sources

Derived from the author's own published papers (Gatekeeper Effect, *Mgmt Sci* 2026; Information Aggregation in Large Collective Purchases, *Econ Theory* 2024; Welfare Costs of Informationally Efficient Prices, *GEB* 2022; Multi-BMBY, *JEMS* 2026; Learning Approximately Optimal Contracts, arXiv:1811.06736; Counterbalancing Learning and Strategic Incentives, NeurIPS 2021), plus:

- John M. Lee, *Some Remarks on Writing Mathematical Proofs* (U. Washington) — formula grammar, justification taxonomy, detail calibration.
- MathOverflow #498885, "Improving readability of proofs" — the post-verification checklist framing; Gro-Tsen on redundancy and assumption scoping; Rüping's naming/organization checklist; grinberg, Dotsenko, Abou Samra, mlk.
- Math.SE #4457318 (Andrew D. Hwang, Paul Wintz) — reader-as-human principles, "blah" test, pronoun and negation rules.
- Hamilton College Writing Center, *Writing Mathematical Proofs* — sentence mechanics, variable introduction.
- Sundstrom, *Mathematical Reasoning*, Appendix A (LibreTexts) — keep-the-reader-informed rules, display conventions.
- Classics worth consulting for deeper judgment calls: Halmos, *How to Write Mathematics*; Knuth, Larrabee & Roberts, *Mathematical Writing*; Higham, *Handbook of Writing for the Mathematical Sciences*; Lamport, *How to Write a 21st Century Proof*; Serre's talk *How to Write Mathematics Badly*.
