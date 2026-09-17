---
name: paper-reading-workspace-presentation
description: Create a React/Vite Workspace Presentation from one paper-reading source workspace or source chain. Use when the user wants to package, present, review, hand off, reread, or browse generated paper-reading artifacts in an interactive frontend.
---

# Workspace Presentation

Use this skill to generate a read-only Workspace Presentation: a local React/Vite app that presents exactly one source workspace or source chain through source-linked summaries, structured modules, and direct source-file previews.

This is a presentation layer. It does not edit source artifacts, replace workflow outputs, create a slide deck, run a new research workflow, or merge multiple unrelated workspaces into one collage.

## Output Root

Set `{workspace-root}` before creating or updating a presentation:

- Default `{workspace-root}` to `workspace` in the repository.
- If the user specifies a workspace root, use it exactly.
- Generate presentations at `{workspace-root}/presentations/{presentation-slug}/`.
- Derive `{presentation-slug}` from the source workspace path unless the user provides one.

## Core Workflow

1. Locate exactly one source workspace or one source chain.
2. Pass the Presentation Source Gate with the user unless the source and slug are already explicit.
3. Classify source artifacts with `references/presentation-display-map.md`.
4. Copy `templates/react-vite/` into `{workspace-root}/presentations/{presentation-slug}/` if the presentation does not already exist.
5. If the presentation exists, preserve app code by default and update only generated metadata.
6. Write `public/presentation-manifest.json`.
7. Write `public/source-index.json`.
8. Read Primary Display and Summarize-Then-Link artifacts.
9. Write one source-linked `public/generated-summaries/{module-id}.json` per presentation module.
10. Stop with the local run commands. Do not run `npm install` or `npm run dev` unless the user explicitly asks.

## Presentation Source Gate

Before generating files, show a compact source packet:

- source workspace or source chain path
- detected workflow coverage
- presentation slug
- output path
- update mode: new scaffold or metadata refresh
- major modules to display

Ask for confirmation if any of these are ambiguous. The source must be exactly one workspace or one coherent source chain.

## Generation Rules

Use the source artifacts as the facts of record. The generated presentation may summarize, condense, and reorganize cumbersome process files, but every module summary must cite source file paths.

Do not copy source markdown into the presentation. Use `source-index.json` to list source files and Vite `/@fs/` read URLs for previewing them through the local development server.

Use:

- `references/manifest-schema.md` for `presentation-manifest.json`
- `references/source-index-schema.md` for `source-index.json`
- `references/summary-schema.md` for generated module summaries
- `references/ui-guidelines.md` for frontend presentation behavior and visual rules

## Existing Presentations

If `{workspace-root}/presentations/{presentation-slug}/` already exists:

- Preserve `src/`, `package.json`, `vite.config.ts`, and styling unless the user requests a full re-scaffold.
- Regenerate `public/presentation-manifest.json`.
- Regenerate `public/source-index.json`.
- Regenerate only skill-owned files under `public/generated-summaries/`.
- Tell the user when template code looks older than this skill, but do not overwrite user edits automatically.

## Finish Message

End with:

```text
cd {workspace-root}/presentations/{presentation-slug}
npm install
npm run dev
```

If the user asked you to run it, install dependencies with approval if network is required, start the dev server, and provide the local URL.
