---
name: write-economics-introduction
description: "Use this Skill for every economics-paper introduction, intro, opening section, first-two-pages, 英文引言, or 经济学论文引言 task, especially requests to read a completed paper body/正文 and write directly usable English introduction prose. It drafts, rewrites, shortens, restructures, outlines, audits, positions, or fact-checks introductions for empirical, structural, theory, historical, measurement, and mixed economics papers. It also checks whether an introduction's contribution, novelty, gap, or citation paragraph overstates the paper body or references. Invoke before answering even when the user supplies a complete packet or requests only final prose. Never use it for an abstract, conclusion, title, standalone literature review, grant or funding application/基金申请, 研究动机或立项依据 proposal, referee report, or nonacademic opening unless an economics-paper introduction is also requested."
---

# Write an Economics Introduction

Write an English introduction that lets an informed reader recover the paper's question, answer, credibility, main findings, and verified place in the literature without receiving a false impression. An introduction is an argument about a completed or substantially developed paper, not a longer abstract and not a fixed paragraph template.

## Start here

Read `references/runtime-core.md` completely on every invocation. It contains the closed-world evidence rules, cold classification, fact and literature ledgers, contribution test, composition spine, and private final audits. Do not draft from this file or the frontmatter alone.

Treat detailed references as normative resources that are loaded when their issue arises. Read only the routed sections unless a route says to read the whole file. Search headings first, then read the complete selected section with enough neighboring text to preserve qualifications.

## Choose the mode

Infer the narrowest mode that fulfills the request:

- **draft** writes a new introduction from the paper body and verified positioning material.
- **rewrite** reconstructs existing prose so its hierarchy and claims match the delivered paper.
- **outline** provides paragraph functions and their evidence needs without silently turning them into prose.
- **audit** diagnoses factual fidelity, argument, positioning, structure, length, and style; it rewrites only when asked.
- **fact-check** maps claims to manuscript and cited-source evidence and identifies conflicts or unsupported additions.
- **positioning** examines gaps, closest work, contributions, and citation support without rewriting unrelated prose.

Polishing never authorizes factual, causal, mechanism, scope, citation, or novelty drift. Do not alter manuscript files unless the user explicitly asks for file edits.

## Route the detailed knowledge

First cold-read the user's materials and privately freeze the mode, evidence universe, central object, headline claim type, paper type, positioning burden, and readiness. Do this before reading type examples, calibration cases, evals, or historical test feedback. Examples are diagnostic counterexamples, never evidence for the current paper.

Then use these routes:

| Need | Read |
|---|---|
| The authoritative paper evidence is a compact fact packet, abstract, author note, table, or local excerpt rather than readable supporting sections | `references/sparse-packet-protocol.md`. For a wholly sparse packet, this replaces the normal composition and paper-type references; do not load those broader pattern files. For mixed evidence, apply it only to sparse claim owners and use normal type/composition knowledge only for full claim owners |
| Every complete draft or rewrite | `references/evidence-and-positioning-protocol.md` §§4, 8, 10, 11, and 13. Claim-span provenance, method/model language, motivating context, promises, and final auditing are universal introduction risks, not optional exceptions |
| Draft, rewrite, or outline needs ordering, paragraph work, transitions, or length | `references/composition-and-length.md` §§1–6; add §§7–8 for shortening, expansion, journal length, repetition, or density decisions |
| Type-specific expression and failure risks | The one relevant section of `references/paper-type-patterns.md` plus §8; for a mixed paper read §7 and the section carrying the headline claim |
| Citation, gap, novelty, contribution, or literature relationship | `references/literature-positioning-and-contributions.md`; use the whole file for positioning mode or complex multi-literature claims, otherwise read the relevant sections |
| Version conflict, source ownership, exact result identity, causal/mechanism/model boundary, missing evidence, or fact-check | The relevant sections of `references/evidence-and-positioning-protocol.md`; read it wholly for a dedicated fact-check or several simultaneous high-risk conflicts |
| Opening, question-answer chain, result story, roadmap, or existing introduction fails at the argument level | The relevant sections of `references/introduction-knowledge.md`; read it wholly for a deep rewrite, comprehensive audit, outline explanation, or guide-based coaching |
| Comprehensive audit, independent scoring, provenance, or 95+ acceptance test | `references/quality-and-sources.md`; its calibration and provenance sections are development resources, not facts about the user's paper |

A routine full-evidence draft normally needs the runtime core, the five universal evidence sections, composition §§1–6, one paper-type section, any genuinely required literature section, and the final gate. A wholly sparse draft instead needs the runtime core, sparse-packet protocol, universal evidence sections, verified literature guidance only when actual literature content is available, and the final gate. It does not load the normal composition or type-pattern files or pad toward a calibration length. A high-risk audit may require all detailed resources.

## Execute the request

Use the runtime core to build private claim-level ledgers and one conservative question–answer–credibility spine. Organize the introduction by reader dependencies—normally tension or obstacle, bounded question, early answer capsule, credibility architecture, ordered findings, changed understanding, verified positioning, and an optional roadmap—while merging, splitting, or reordering functions to fit the paper.

Give the main answer the greatest weight. Include a mechanism, heterogeneity result, null, robustness check, cost, limitation, or secondary result only when it changes the principal answer, its credibility, or an indispensable boundary. A statement can be true yet still not belong in the introduction.

Use the paper body as the authority for what this paper does and finds. Use the exact cited source as the authority for what prior work does and finds. A contribution requires both sides of that comparison. If literature evidence is insufficient, describe the paper concretely and omit or qualify unsupported gap, priority, and global novelty claims rather than inventing them.

Length is elastic. Follow the target journal or user's constraint when supplied; otherwise let question complexity, credibility burden, result hierarchy, and literature-positioning burden determine length. The Top Five ranges in the references are calibration evidence, not quotas or paragraph templates.

## Deliver the requested surface

For **draft** and **rewrite**, output directly usable English manuscript prose. Do not reveal classification, readiness, ledgers, plans, source-reading narration, internal audits, or workflow. Begin with prose, without an `Introduction` heading, preface, separator, or code fence. If a material positioning issue remains but does not block an honest draft, add only one or two plain sentences in the user's language after the prose; omit the note when nothing material remains.

All reading, classification, ledger work, planning, drafting, and checking occur before the first user-visible character. Do not stream or preserve intermediate prose. Compose `formal_prose` and any permitted `risk_note` privately, serialize them once into one `delivery_buffer`, and apply the final gate to that exact buffer. Return `delivery_buffer` once; emit nothing before or after it. The final response is the audited deliverable, never a report that a deliverable is about to follow.

For **outline**, return paragraph functions, evidence inputs, transitions, and unresolved dependencies. For **audit**, **fact-check**, and **positioning**, return the requested diagnosis or mapping and distinguish unsupported, unverified, conflicting, and outside-scope claims precisely. These modes do not inherit the manuscript-prose-only surface unless they also deliver a complete replacement introduction.

For any complete draft or rewrite, render the entire candidate response first, including any necessary risk note. Then read `references/final-delivery-gate.md` last and apply it to that exact user-visible surface. If anything changes, rerun the gate. After it passes, copy the passing candidate directly and add nothing.
