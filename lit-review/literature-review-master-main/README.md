# Literature Review Master

Literature Review Master is a mode-driven literature intelligence skill for academic research. It helps researchers search, map, evaluate, verify and write with literature. It is designed for open-ended exploration, idea validation, project foundation, manuscript support, citation verification, reviewer-defence preparation and journal-specific positioning.

The skill is deliberately broad. It can be used in business, management, economics, finance, marketing, operations, information systems, engineering, computer science, statistics, public policy, health, education, social science and interdisciplinary research. It is particularly strong for quantitative research, theory-driven research, formal modelling, simulation-supported work, computational work, empirical designs, statistical modelling, probabilistic modelling, Bayesian approaches, optimisation, machine learning, AI systems and strategic-interaction models.

## What this skill is for

Use it when you need to answer questions such as these.

- Is this research direction worth entering?
- What are the main literature streams in this topic?
- Is my idea new, or is there a killer paper?
- Is the research gap real, or merely cosmetic?
- Can this gap be addressed with theory, simulation or computation when real data are unavailable?
- Which journals or venue families are plausible targets?
- Which papers must be cited before a manuscript is credible?
- Does each citation actually support the claim attached to it?
- What would a hostile reviewer say about my literature review?
- How should the same project be positioned for different journal families?

## Core idea

The skill uses modes rather than a single generic literature-review prompt. Each mode has a different purpose.

| Mode | Purpose |
|---|---|
| Mode 0 | Meta-decision before starting research |
| Mode A | Exploration when the user has keywords but no concrete idea |
| Mode B | Idea validation and killer-paper analysis |
| Mode C | Project foundation and literature-tree construction |
| Mode D | Manuscript support for introduction, related work, discussion and limitations |
| Mode E | Citation and evidence verification before submission |
| Mode F | Rolling updates after time passes or framing changes |
| Mode G | Reviewer attack and literature defence |
| Mode H | Journal-specific literature positioning |
| Mode I | Systematic, scoping, bibliometric or survey-review protocol |
| Mode J | Theory-only or simulation-only gap viability |

## Why it is different from a normal literature-review assistant

The skill does not merely summarise papers. It is designed to make decisions. It produces cold verdicts such as Pursue, Pivot, or Drop. It distinguishes direct predecessors from broad background. It checks whether a gap changes the framework or merely changes the setting. It runs a no-data viability filter before recommending theory-only or simulation-supported work. It uses a two-pass citation evidence gate before submission.

## Embedded ABS AJG 2024 database

The package includes a bundled database of ABS AJG 2024 journals in the included dataset.

Use the database as a search-priority and journal-scope resource. Do not use ratings as proof of relevance. A highly rated journal article should be cited only when it directly supports the research question, method, mechanism, empirical design or gap.

## Quick start

For a broad topic without a concrete idea, ask this.

```text
Use Literature Review Master in Mode A.
I am interested in [topic or keywords].
Please map the main literature streams, identify plausible research gaps, search for killer-paper risks, and rank candidate directions by ROI.
```

For a rough idea, ask this.

```text
Use Literature Review Master in Mode B and Mode J.
My idea is [brief description].
The available evidence is [real data, public data, theory, simulation, computation, experiment, qualitative evidence, or none].
Please run killer-paper analysis, framework-versus-cosmetic gap testing, no-data viability if relevant, and give a Pursue, Pivot, or Drop verdict.
```

For manuscript support, ask this.

```text
Use Mode C and Mode D.
My target journal family is [journal or field].
Please build a literature tree, claim-citation map, closest-predecessor table and related-work writing plan.
Use British English for manuscript prose.
```

For submission checks, ask this.

```text
Use Mode E.
First extract all citation-bearing and evidence-bearing claims.
Then verify citations, metadata, claim support, numerical values, tables, figures and internal evidence.
Give a final safety verdict using PASS, PASS WITH MINOR FIXES, MAJOR REPAIR REQUIRED, or UNSAFE FOR SUBMISSION.
```

## Documentation

Read the full guide here.

```text
docs/DETAILED_USAGE_GUIDE.md
```

The repository also includes contribution guidance, release notes, and a licensing note.

## Important limitations

This skill does not guarantee that a literature review is exhaustive. It should always state search limitations. It does not invent papers or fill missing metadata by guesswork. It does not treat citation existence as evidence that a citation supports a claim. It does not treat simulation as empirical evidence unless the simulation is tied to observed data.

## Licence and third-party notices

This package contains third-party-derived components. Preserve `THIRD_PARTY_NOTICE.md` when redistributing the skill. A licence for the repository owner’s own contributions should be selected before public release. See `LICENSING_NOTE.md`.
