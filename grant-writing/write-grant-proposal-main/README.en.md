# write-grant-proposal

[中文](README.md)

This Codex Skill helps draft, revise, and review Chinese grant proposals and technical application documents. It turns proposal writing into a structured workflow: parse the template and call guide first, define the method system, build an outline, draft the content, and then run consistency checks across the full document.

## Acknowledgements

This project used extensive AI-assisted programming during its development. Part of the API call cost was sponsored by the **Code Go** relay station.  
If you also want to use Codex, Claude and other models at low cost for writing proposals, check it out:  
🔗 [Code Go](https://shu26.cfd)  
(New users receive $5 free credit)

## What This Skill Is For

This Skill is designed for Chinese grant proposal and technical application writing, including:

- Industry-university-research fund applications
- Natural science foundation proposals
- Special program applications
- Enterprise challenge or “open competition” proposals
- Technical implementation plans
- Proposal rewriting, technical route drafting, indicator design, and consistency review

## Key Features

- **Template-first workflow**: Parse the official proposal template before drafting.
- **Call-guide mapping**: Map requirements, indicators, deliverables, and constraints to proposal sections.
- **Method system design**: Define the core technical storyline, research task breakdown, method names, title mapping, and indicator mapping before writing.
- **Outline freeze**: Build a complete outline before drafting full sections.
- **Section drafting**: Support proposal overview, research objectives, research contents, technical routes, innovation points, milestones, assessment indicators, and deliverables.
- **Full-document checks**: Review template coverage, title consistency, indicator consistency, terminology consistency, subject consistency, and privacy safety.
- **Open-source safe**: The Skill contains only abstract writing patterns and procedural guidance. It does not include private proposal examples, private paths, or project-specific content.

## Recommended Workflow

1. Prepare the call guide, proposal template, existing draft, and supporting materials.
2. Ask Codex to use this Skill to produce template parsing, method-system design, and a full outline first.
3. Confirm the outline before drafting sections.
4. Draft the proposal section by section.
5. Run a full-document consistency check.
6. Revise titles, terminology, method names, indicators, deliverables, and cross-references based on the review.

## Example Prompts

```text
Use $write-grant-proposal with this call guide and proposal template. First produce the template analysis, method system, and full outline. Do not draft the body text yet.
```

```text
Use $write-grant-proposal to draft the Research Contents and Technical Route sections from my outline. Make sure each research-content title exactly matches its corresponding technical-route title.
```

```text
Use $write-grant-proposal to review this proposal for missing template sections, inconsistent titles, unsupported indicators, unmapped deliverables, terminology drift, and cross-reference errors.
```

## Installation

Place this folder under your Codex skills directory:

```text
~/.codex/skills/write-grant-proposal/
```

Expected structure:

```text
write-grant-proposal/
├── SKILL.md
├── README.md
├── README.en.md
└── agents/
    └── openai.yaml
```

## Design Principles

- Do not start from a fixed universal template; every proposal template may have different sections, fields, and review criteria.
- Do not skip the outline stage; research contents, technical routes, innovation points, indicators, and deliverables must be aligned before drafting.
- Do not invent indicators, team achievements, external data, or unsupported commitments.
- Do not reuse private proposal text. Extract only structural patterns, reasoning flow, and writing methods.
