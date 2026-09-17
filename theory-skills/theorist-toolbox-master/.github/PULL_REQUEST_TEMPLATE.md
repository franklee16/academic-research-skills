<!-- Thanks for contributing! Keep PRs to one module at a time. -->

## What this PR adds / changes

<!-- One or two sentences. Link any related issue or discussion. -->

## Type

- [ ] New skill (`skills/<name>/`)
- [ ] New agent (`agents/<name>.md`)
- [ ] Case study (`examples/`)
- [ ] Fix / improvement to an existing module
- [ ] Core change (scaffolding / hooks / `paper.tex` macros) — discussed in an issue first

## The no-hand-waving bar

<!-- The project's whole point. Check what applies. -->

- [ ] The module makes the model more **correct**, not just more confident.
- [ ] It has an honest **failure mode** (block / flag / `\unproven{}`), not a confident wrong one.
- [ ] If it adds code: tests + golden values are included and pass.
- [ ] If it states a result: it traces to a proof, citation, passing test, or explicit `\unproven{}`.

## Module checklist

- [ ] Frontmatter present and correct (`name`, `description`; `tools` for agents; `author` for skills).
- [ ] Self-contained, or any dependency (other module / external CLI / toolchain) is stated.
- [ ] `README.md` updated (skills or agents table, with an honest `Status`).
- [ ] If co-math-related: registered in `co-math-config.json` and any `paper.tex` macro / hook contract updated.

## Anything reviewers should know

<!-- Caveats, open questions, things you're unsure about. Honesty here speeds review. -->
