---
name: practitioner-finance-voice
description: >
  Rewrite academic finance/economics prose into — or draft new sections in — the voice of top
  practitioner journals: Financial Analysts Journal (FAJ), Journal of Portfolio Management (JPM),
  Journal of Investing, Journal of Wealth Management, and Journal of Fixed Income. Built from a
  close reading of 7 Journal of Portfolio Management papers by the AQR orbit (Asness, Frazzini,
  Israel, Moskowitz, Pedersen, Ilmanen, et al.). USE THIS SKILL whenever the user is writing or
  revising for a practitioner outlet (FAJ / JPM / JOI / JWM / JFI); converting a Journal-of-Finance-
  style academic draft into practitioner voice; drafting a practitioner-facing abstract, intro,
  results, or conclusion; or asks to "make this FAJ-style," "rewrite for the Journal of Portfolio
  Management," "practitioner tone," "less academic," or "sound like an AQR / Research Affiliates
  piece." Do NOT use for academic journals (JF/RFS/JFE/QJE — use econ-write / paper-taste) or for
  generic de-AI polishing (use humanizer / no-ai-slop).
argument-hint: "<task> e.g. 'rewrite this intro in FAJ/JPM style' or 'draft a practitioner-voice conclusion for my value paper' or 'convert this JF-style results section for FAJ'"
user-invocable: true
---

# Practitioner Finance Voice

Rewrite or draft prose in the voice of the top finance **practitioner** journals — *Financial Analysts Journal*, *Journal of Portfolio Management*, *Journal of Investing*, *Journal of Wealth Management*, *Journal of Fixed Income*. This is the voice of an opinionated expert writing for portfolio managers, not a neutral technician writing for referees.

**Provenance.** Built from a close reading of 7 *Journal of Portfolio Management* papers by the AQR orbit (Asness, Frazzini, Israel, Moskowitz, Pedersen, Ilmanen, Alquist, Maloney, Aghassi, Fattouhe): the "Fact, Fiction, and {Factor}" series, "The Devil in HML's Details," and "Value and Interest Rates." Every rule below is backed by verbatim exemplars in [references/exemplars.md](references/exemplars.md).

## What this skill is — and isn't

It is a **voice layer**. It assumes the baseline clarity rules from `paper-taste` and `econ-write` (active voice by default, one idea per sentence, precision over abstraction, no stacked hedges, consistent terminology) and layers the practitioner **voice** on top. It does not repeat those rules.

It is **not** a LaTeX formatter, a citation manager, or an econometrics checker. It changes *how the prose sounds and argues*; it does not touch the author's numbers, claims, or evidence.

**Hard rule — voice only, never fabricate.** A transform changes voice, not content. Never invent quotes, statistics, citations, or "fictions" the field isn't actually debating. Every number and claim in the output must come from the user's source material verbatim. If the user's draft lacks a "so what" implication, say so and ask — do not invent one.

## When to use / when not to

| Use it | Don't use it |
|---|---|
| Writing for FAJ / JPM / JOI / JWM / JFI | Writing for JF / RFS / JFE / QJE (academic) → use `econ-write` / `paper-taste` |
| Converting an academic draft to practitioner voice | Generic de-AI polishing → use `humanizer` / `no-ai-slop` |
| Drafting a practitioner abstract / intro / results / conclusion | Fixing LaTeX, citations, or identification → use the relevant skill |
| User asks for "FAJ-style," "JPM voice," "practitioner tone," "less academic" | Pure proofreading / typos |

## The two-layer voice model (the core mental model)

The user chose **Moderate** voice strength. That maps to a two-layer model:

- **Layer 1 — Always-on baseline.** The durable house-style traits every practitioner piece shares, regardless of topic. Apply to *every* transform. → [references/voice-and-register.md](references/voice-and-register.md) and [references/evidence-and-so-what.md](references/evidence-and-so-what.md).
- **Layer 2 — Optional rhetorical moves.** The distinctive flair — Fact/Fiction scaffold, contrarian-pivot openers, cute titles, discursive footnotes. Deploy *selectively*, only where the material earns them. → [references/structure-and-framing.md](references/structure-and-framing.md).

The dial: Layer 1 alone produces a clean, credible practitioner piece. Layer 2 is added when the paper is genuinely corrective or the user wants personality. **When in doubt, default to Layer 1 only.**

## Workflow

Ask one question if it isn't obvious: *which mode, and which register?*

### Rewrite mode (transform existing prose)
1. **Read the draft.** Diagnose where it reads "academic/JF" — passive voice, naked statistics without verdicts, no "so what," trailing-hedge paragraphs, citation walls, noun-headers.
2. **Apply Layer 1 across the board.** Opinionated "we," long+short rhythm, topic-sentence-first paragraphs that end on a punchline, concession + restatement tics, prose-narrated stats, inline definitions, "so what" on every finding.
3. **Consider Layer 2.** Is the paper genuinely corrective? Does the topic carry wit? If yes, offer the moves; if no, skip them.
4. **Return the rewrite + a short "what changed" note** (2–5 bullets: voice, rhythm, stats, so-what, any Layer 2 moves added/skipped and why).

### Draft mode (new prose from notes/outline)
1. **Confirm register** — dry-measured-verdict (default) vs witty-extrovert. Ask if unclear; default to dry.
2. **Draft in voice.** Layer 1 always; Layer 2 where it fits the material.
3. **Flag the Layer 2 moves used** so the user can dial them up or down.

## Layer 1 — the always-on transform

| Academic tell (strip) | Practitioner move (reach for) | See |
|---|---|---|
| "It is found that…" / passive voice | Opinionated "we find / we believe / we argue"; direct "you" | [voice-and-register §1](references/voice-and-register.md) |
| Uniform sentence length | Long technical sentence + short punchy verdict | [voice-and-register §2](references/voice-and-register.md) |
| Paragraphs that trail off | Topic sentence → evidence → **punchline close** | [voice-and-register §3](references/voice-and-register.md) |
| "Although the evidence is mixed…" buried | Concession up front: "Of course / It is true that… **but**" | [voice-and-register §4](references/voice-and-register.md) |
| Stated once, formally | Stated twice: formal, then "in other words" plain English | [voice-and-register §5](references/voice-and-register.md) |
| Naked statistic: "coef = 0.23 (t=3.4)" | Number + benchmark + significance + verdict in one breath | [evidence §1](references/evidence-and-so-what.md) |
| Undefined jargon / "see Table 3" | Inline apposition gloss; narrate the exhibit | [evidence §2–3](references/evidence-and-so-what.md) |
| Result with no implication | Every finding → "so what for a portfolio manager" | [evidence §4](references/evidence-and-so-what.md) |
| Citation wall | Light, narrative, clustered author-year | [evidence §5](references/evidence-and-so-what.md) |

## Layer 2 — optional rhetorical moves (deploy selectively)

| Move | When to use | When to skip |
|---|---|---|
| **Contrarian-pivot opener** ("You'd be forgiven for thinking X… In fact, not-X") | Paper overturns a real belief | Confirmatory / descriptive papers |
| **Fact/Fiction scaffold** (numbered ledger + `FACT:`/`FICTION:` headers) | Genuinely corrective; each item is a real claim someone holds | Methods pieces; would require inventing a "fiction" |
| **Rhetorical question** (answered within 2 sentences) | To launch a section or dramatize a puzzle | If you'd write three in a row |
| **Vivid analogy / aphorism** | One per section, max; cross-domain intuition | Serious topics (drawdowns, risk) |
| **Cute title + serious subtitle** | Light or corrective topic | Risk-management / methodology papers |
| **Discursive footnote** (wit, biography, provenance) | Carries a real aside | Empty name-dropping |
| **Humble/inviting close** ("we wish to learn") | Forward-looking, contested terrain | — |

Full guidance and when-not-to in [references/structure-and-framing.md](references/structure-and-framing.md).

## The two registers

| Register | Vibe | Use when |
|---|---|---|
| **Dry-measured-verdict** (default) | Authoritative, calm; "this emperor has no clothes." Semicolons, em-dashes, logical-zinger closes, few exclamations. | Serious topics, mixed evidence, restrained authorial voice |
| **Witty-extrovert** | Conversational, contrarian, name-dropping. Exclamations, named names, parenthetical asides, slang. | Corrective/myth-busting topics, broad audience, author wants personality |

Most papers mix the two — dry for empirics, witty for framing. **Default to dry**; dial up wit only on request or when the material clearly calls for it. Never force wit onto a paper about losses or risk.

## Lexical fingerprint

**Reach for:** "we find / we believe / we argue / in our view," "in fact," "however," "of course," "in other words," "put differently," "that is," "the bottom line is," "clearly," "robust," "broadly speaking," "for example," "importantly," "in short," "on first principles," "appears to," "is consistent with," "suggests."

**Strip:** "it is found that," "it has been shown that," "performance" (name the metric), "significant" (give the t-stat), "a number of," "in order to," "it is worth noting that," "to our knowledge," any stacked hedge ("may perhaps potentially"), "this paper examines" (just examine it).

## Anti-patterns

- **Don't** swing passive→first-person *and* rant. The persona is *measured partisan*, not columnist.
- **Don't** force the Fact/Fiction scaffold onto a paper that isn't corrective — and **never invent a "fiction"** to fill the frame.
- **Don't** table-dump. If a finding lives only in a table, narrate it.
- **Don't** stack hedges. One calibrated hedge per claim, paired with the number.
- **Don't** over-wit a serious topic. Exclamation marks about drawdowns are tone-deaf.
- **Don't** make every paragraph end on a quip — vary the punchline shape (verdict, question, zinger, implication).
- **Don't** invent quotes, statistics, analogies, or citations. Voice only.
- **Don't** re-gloss jargon you defined three pages ago.

## For real sentences to pattern-match

The rules above tell you *what* to do. When you need to hear *how it sounds*, read [references/exemplars.md](references/exemplars.md) — ~50 verbatim sentences from the corpus, keyed by rhetorical move and tagged dry/witty. Pattern-match a real cadence, then adapt it to the user's content. This is the file that makes the skill actually work; reach for it on every transform.
