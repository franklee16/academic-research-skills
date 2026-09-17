# Theorist Toolbox

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-2606.22337-b31b1b.svg)](https://arxiv.org/abs/2606.22337)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills%20%26%20agents-da7756.svg)](https://claude.com/claude-code)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

*Shared tooling for doing economic theory with LLMs — prove results, check them, and run a proof-building project like a research team, without letting the model hand-wave.*

> **If you use this toolbox, please cite:** Moran Koren (2026), *Theorist Toolbox: Tools for Agent-Based LLM-Assisted Economic Theory Research*, arXiv:2606.22337 — <https://arxiv.org/abs/2606.22337>.

<details><summary>BibTeX</summary>

```bibtex
@article{koren2026theorist,
  title         = {Theorist Toolbox: Tools for Agent-Based LLM-Assisted Economic Theory Research},
  author        = {Koren, Moran},
  year          = {2026},
  eprint        = {2606.22337},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2606.22337}
}
```
</details>

A small set of Claude Code *skills* for doing economic theory with LLMs — proving
results, checking them, and running a whole proof-building project the way you'd run
a research team. 

Empirical economists have had shared tooling for years. The empiricist learns the
craft from reusable, opinionated tools. Theorists rarely really got that. This is an
attempt at the theory-side equivalent: a toolkit that encodes *how* to push an LLM
through a proof without letting it hand-wave.

The three skills are three different bets on the same problem — *how do you get
machine help on a theorem you don't already know how to prove, and trust the answer?*

## The skills

| Skill | The bet | What it is | Status |
|-------|---------|-----------|--------|
| **`math-proof`** | One careful pass. | A discipline for writing a full, gap-free proof in a single shot: state what you'll show before showing it, sign every term, no "clearly," no overgeneralizing from examples. | ✅ stable · no deps |
| **`codex-math`** | Two minds, one adversarial. | Drives OpenAI Codex (gpt-5.5) as a *co-processor and hostile verifier* — propose, then try to break, then triage. Built around the rule that Codex is a brilliant, unreliable mathematician: every output is a lead, not a verdict. | ⚙️ needs OpenAI Codex CLI |
| **`co-math-init` / `co-math-status`** | A research team, not a chat. | Scaffolds a structured proof-building *project* — `paper.tex`, goals, decisions log, workstreams, strict mode where every gap is flagged `\unproven{}` and nothing is "complete" without a reviewer's sign-off. The architecture follows Zheng et al. (2026), *AI co-mathematician* (Google DeepMind). `co-math-status` renders the project state. | ✅ stable · agents required, hooks optional |
| **`proof-readability`** | Correctness first, then clarity. | A post-verification exposition pass for proofs that are *already* verified — six layers (architecture, signposting, line-level justification, notation, intuition, grammar) that minimise the reader's work without ever changing the mathematics. In a co-math project the coordinator runs it after a proof is approved; a suspected gap routes the workstream back to the prover rather than getting quietly patched. | ✅ stable · no deps |

Each is a different point on a trade-off between speed, verification, and coverage:
the single pass is fastest and cleanest but unchecked; the adversarial pair is the
most reliable per claim; the structured team gives the broadest, most disciplined
coverage and can *reject its own work*; `proof-readability` runs after any of them
to make an accepted proof legible.

### The co-math agents (`agents/`)

The `co-math-init` project is run by a small team of Claude Code sub-agents, shipped
in [`agents/`](agents/):

| Agent | Role |
|-------|------|
| `project-coordinator` | The front door — reads `goals.md`, formalises intent, dispatches and steers workstreams. |
| `literature-reviewer` | Literature searches and verified, cited workstream reports. |
| `prover` | Drafts proofs into `paper.tex` with strict discipline — every step justified, cited, or `\unproven{}`. Also runs the `proof-readability` pass in readability mode. |
| `coder` | Python for computational exploration and numerical verification, with mandatory tests and golden values. |
| `lean-prover` | Formalises a lemma in Lean 4 and verifies it with `lake build`. A green build is the strongest "proven" the system supports — `paper-reviewer` re-runs the build rather than re-checking the mathematics, and the theorem is closed with `\leanproved{}`. |
| `paper-reviewer` | Adversarial gate — a workstream cannot be marked complete until it writes an explicit approval file. |

📐 **Diagrams:** see [`docs/co-math-architecture.md`](docs/co-math-architecture.md) for the agent topology, the workstream lifecycle, and the verification ladder (informal proof → Lean-verified → readable).

## The case study (`examples/`)

I built these while testing all three on one problem: turning the *eigengrade* of
Gans & Kominers (2026, *"What Does a Grade Mean?"*, NBER w35183) into a VCG-style
mechanism against grade inflation. Each skill produced a self-contained writeup:

- `1-math-proover_…` — a student-side enrollment VCG (single pass, `math-proof`).
- `2-codex-proover_…` — an instructor-side Pigouvian/Groves transfer, adversarially
  verified with Codex + Monte Carlo (`codex-math`).
- `3-co-math_…` — a money-free, report-space mechanism *suite* with an impossibility
  theorem and a numerically validated running example (`co-math`).

Two of the three independently rediscovered the same externality kernel; the third's
reviewer gate killed one of its own sub-goals. The write-up of that comparison lives
in the accompanying Substack post.

## Install

These are Claude Code skills and agents. Drop the skills into your skills directory,
and — for the `co-math` workflow — the agents into your agents directory:

```bash
cp -R skills/* ~/.claude/skills/
cp -R agents/* ~/.claude/agents/   # only needed for the co-math project workflow
```

Then invoke them from Claude Code (`/math-proof`, `/co-math-init`, …) or let the model
pick them up by description.

### Notes

- **`codex-math`** documents the *interface* to a set of companion runner scripts
  (`codex_verify.sh`, `codex_write.sh`, `codex_explore.sh`) that wrap the
  [OpenAI Codex CLI](https://github.com/openai/codex). Those live alongside your
  project (`code/utils/codex_math/`) and call `codex exec`; you'll need the Codex CLI
  installed and authenticated. The skill is the playbook for using it well.
- **`co-math-init`** writes per-project hooks that reference
  `~/.claude/co-math/hooks/` (a `paper_tex_guard.py` and a
  `workstream_complete_guard.py` that enforce strict mode). Provide your own, or run
  with the guards disabled — the skill works either way; the hooks are the teeth.
- **`lean-prover`** needs a working Lean 4 toolchain (`lean` and `lake` on `PATH`);
  it pins the toolchain per workstream and builds against mathlib. Without it the
  agent blocks the workstream cleanly rather than faking a proof. Every other agent
  runs with no extra tooling.

## Contributing

Issues and PRs welcome — bug reports, new skills, a sharper proof discipline, or
fixes to the ones here. No CLA and no ceremony.

The toolbox grows the Linux way: a small core, plus self-contained **modules**
(skills, agents, case studies). You don't need the whole tree — just the contract for
the kind of module you're adding:

- **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — the module contract: where a skill/agent
  lives, its frontmatter, and the *no-hand-waving* bar your PR is reviewed against.
- **[`ROADMAP.md`](ROADMAP.md)** — where it's headed and which modules are most wanted next.
- **[Discussions](../../discussions)** — questions, prompt-sharing, ideas (lower-stakes than issues).
- **[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)** — be rigorous about ideas, kind to people.

New here? Try a [`good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
or weigh in on the pinned roadmap RFC.

## Author

Moran Koren, Ben-Gurion University of the Negev — korenmor@bgu.ac.il.
If you use the toolbox in research, a mention is appreciated.

## License

MIT. See `LICENSE`. Use them, fork them, tell me what broke.
