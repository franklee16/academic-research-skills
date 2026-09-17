---
name: co-math-status
description: Render a compact status view of an AI co-mathematician research project — goals, active workstreams, blocked items, pending reviews, recent decisions. Use when the user asks "what's the status of this project", "show me the workstreams", "/co-math-status", "what's blocked", or wants to understand project state without opening files manually. Replaces the visual workstream branching diagrams of the DeepMind paper (Fig. 2-4) with an ASCII rendering.
author: Moran Koren <korenmor@bgu.ac.il> (Ben-Gurion University of the Negev)
---

> **Author:** Moran Koren, Ben-Gurion University of the Negev (korenmor@bgu.ac.il). Part of the [Theorist Toolbox](https://github.com/morankor/theorist-toolbox).


# co-math-status

Render a compact, human-readable status view of the current AI co-mathematician project.

## When to invoke

- `/co-math-status`
- "show project status"
- "what's the state of this project"
- "what's blocked"
- "which workstreams are running"

## What it does

Runs `python3 ~/.claude/co-math/tools/render_status.py` from the current directory. The script walks up from the cwd to find a `co-math-config.json`; if there is no co-math project in the ancestry, it prints "not inside a co-math project" and exits cleanly.

When inside a project, the output looks like:

```
Project: ambidextrous-sofa
Created: 2026-05-10  |  Strict mode: ON  |  Paper format: latex

Research question:
  Prove an upper bound on the ambidextrous sofa problem area.

Goals (approved: YES)
  G1 Literature review of prior sofa bounds
  G2 Computational framework for branch-and-bound search
  G3 Execute the search

Workstreams                         status      agent              last update
  W001-prior-bounds          [G1]   COMPLETE    literature-reviewer 2026-05-10
  W002-comp-framework        [G2]   RUNNING     coder              2026-05-11
  W003-pruning-heuristic     [G2]   BLOCKED     prover             2026-05-12  <-- needs attention
  W004-search                [G3]   PLANNED     -                  -

Pending reviews
  W002-comp-framework  -- in review by paper-reviewer (round 1)

Open obligations in paper.tex
  3 \unproven blocks (see appendix A)

Recent decisions (last 3)
  2026-05-12  Pruning heuristic blocked; user steering needed (per W003 report.md)
  2026-05-11  Approved goals G1-G3
  2026-05-10  Project initialized

Failed explorations: 1 (see failed-explorations/)
```

## Output

Output is printed directly. The script does not modify any files. After printing, **briefly summarise** the most important item for the user — typically "X workstreams running, Y blocked" — rather than re-explaining what the user just saw.

## When to do more than render

If the user follows up with "open the blocked workstream" or "show me W003's log", read the relevant file with the Read tool and surface the contents.
