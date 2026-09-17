# Contributing to the Theorist Toolbox

Thanks for being here. This toolbox grows the way the Linux kernel does: a small,
stable core and a lot of self-contained modules contributed by people who needed
them. You don't have to understand the whole tree to add to it — you only have to
understand the **contract for the kind of module you're adding**. This document is
that contract.

If anything here is unclear, open a [Discussion](../../discussions) — an unclear
contributing guide is a bug, and fixing it is a great first contribution.

---

## The shape of the repo

Everything is a module. There are exactly three kinds, and each has a fixed home:

| You're adding… | It lives in… | It is… |
|---|---|---|
| A **skill** (a discipline/playbook the model follows) | `skills/<name>/SKILL.md` | A self-contained folder, optionally with `templates/`. |
| An **agent** (a co-math sub-agent with a job and tools) | `agents/<name>.md` | A single Markdown file with frontmatter. |
| A **case study** (a worked example of the toolkit in use) | `examples/` | A self-contained writeup (PDF + optional sources). |

The **core** — the `co-math-init` scaffolding, the hooks contract, the `paper.tex`
macros — changes rarely and deliberately. Most contributions are *new modules*, not
edits to the core. If your idea requires changing the core, open an issue first so we
can talk about the architecture before you write code.

---

## The one rule that governs everything: no hand-waving

The toolbox exists to push an LLM through a proof **without letting it hand-wave**.
Every module must uphold that, in its own way:

- A **skill** must encode a discipline that *reduces* the chance of an unjustified
  step — not just "ask the model nicely."
- An **agent** must treat its own output as a lead, not a verdict, and must have an
  honest failure mode (block / flag / `\unproven{}`) rather than a confident wrong one.
- **Code** must come with tests and golden values; a claim in a paper must trace to a
  proof, a citation, a passing test, or an explicit `\unproven{}`.

A contribution that makes the model *sound* more authoritative without being more
*correct* is exactly what this project is against. That's the bar your PR is reviewed
against.

---

## Adding a skill

A skill is a folder under `skills/` containing `SKILL.md` (lowercase `skill.md` is
also accepted; match the neighbours). It is picked up by Claude Code from its
frontmatter `description`, so that line is load-bearing.

**Required frontmatter:**

```yaml
---
name: your-skill-name           # kebab-case, matches the folder
description: One or two sentences. Lead with WHEN to use it and the trigger
  phrases, because the model selects skills by this field alone.
author: Your Name <you@example.edu> (Affiliation)
---
```

**The body should answer, in this order:**

1. **When to invoke** — trigger phrases and the situation it's for.
2. **The discipline** — the actual method, step by step. This is the substance.
   Concrete rules ("sign every term", "name the reason for every inequality") beat
   vibes ("be rigorous").
3. **What it does NOT do** — the boundary. Every good skill has one.
4. **Failure modes** — what going wrong looks like, and what the model should do
   instead of faking success.

**Checklist before you open the PR:**

- [ ] Frontmatter has `name`, `description`, `author`.
- [ ] The skill is self-contained — no dependency on another skill being installed,
      unless you state it explicitly.
- [ ] Any external tool it needs (a CLI, a toolchain) is named, with how to get it.
- [ ] Added a row to the **skills table** in `README.md`, with an honest `Status`
      (deps, maturity).
- [ ] If it touches the co-math workflow, the relevant agent(s) and
      `co-math-config.json` reference it.

---

## Adding an agent (co-math sub-agent)

An agent is a single file `agents/<name>.md`. It is a worker the
`project-coordinator` can dispatch a workstream to.

**Required frontmatter:**

```yaml
---
name: your-agent-name           # kebab-case, matches the filename
description: What it does and WHEN the coordinator should dispatch it.
tools: Read, Write, Edit, Bash, Glob, Grep   # only what it actually needs
---
```

**The body should define:**

1. **When you are invoked** and what you receive (the workstream contract:
   `instructions.md`, `status.md`, `log.md`, `report.md`).
2. **Your method** — the disciplined steps the agent follows.
3. **Acceptance condition** — what counts as done, and that it sets `status` to
   `review` (never `complete` itself — completion is the `paper-reviewer`'s gate).
4. **Failure modes you must avoid** — the honest-failure clause.

**Checklist:**

- [ ] Frontmatter has `name`, `description`, `tools` (minimal set).
- [ ] The agent sets `status: review` and does not self-approve.
- [ ] If it produces a new kind of evidence (like `lean-prover`'s `\leanproved`),
      the `paper.tex` macro and `paper_tex_guard` contract are updated to recognise it.
- [ ] Registered in `co-math-config.json` under `agents`, and documented in the
      README agents table.

---

## Adding a case study

Drop a self-contained writeup in `examples/`. Name it `N-<skill>_<topic>` to match the
existing ones. A case study earns its place by being *reproducible enough to learn
from*: say which skill produced it, and what the discipline caught or missed. Honest
"here's where it broke" studies are more valuable than triumphant ones.

---

## The pull-request flow

1. **Fork**, branch (`add-<thing>` or `fix-<thing>`), and make your change.
2. Keep PRs **one module at a time**. A skill and an unrelated bugfix are two PRs.
3. Fill in the PR template — it's the checklist above in short form.
4. Expect a **review against the no-hand-waving bar**, not a rubber stamp. This is
   the project's whole point; pushback on rigor is a feature. It's meant to be
   strict *and* encouraging — if a change is rejected, the review will say exactly
   what would make it mergeable.
5. By contributing you agree your work is released under the repo's **MIT license**.
   There is **no CLA** and no ceremony.

---

## Good first contributions

- Fix or sharpen the discipline in an existing skill (a banned phrase that slips
  through, a missing justification rule).
- Write a case study applying the toolkit to a model you know.
- Improve `docs/co-math-architecture.md` or this guide.
- Pick up an issue tagged [`good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

See [`ROADMAP.md`](ROADMAP.md) for where the project is headed and which modules are
most wanted next. Roadmap direction is discussed in the open — weigh in on the pinned
RFC issue.

---

Maintained by Moran Koren (Ben-Gurion University of the Negev). Be rigorous, be kind,
and assume the other person is trying to get the mathematics right.
