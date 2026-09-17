---
name: lit-review-summary
description: Summarize a folder of research papers into a tiered literature review using a parallel multi-agent pipeline (summarize → critic-review → revise → aggregate). Produces a deep Tier 1 reference sheet per paper, a Tier 2 cheat-sheet table, a Tier 3 themes-by-studies synthesis matrix, and one assembled literature-review document. Use this skill whenever the user wants to build a literature review from a batch/set/folder of papers, apply a paper-summary or lit-review framework to multiple papers, create a synthesis matrix or cheat sheet across papers, summarize the papers in a Reference/ or references folder, or turn a pile of PDFs into a structured review. Trigger even when the user does not say "literature review" explicitly, e.g. "summarize the papers in Reference", "build me a synthesis of these PDFs", "make reference sheets for all the papers in this folder", "what do these N papers collectively say".
version: 0.1.0
---

# Literature-Review Summary (Multi-Agent Pipeline)

Turn a folder of papers into a tiered literature review. The pipeline runs a fleet of subagents in parallel: one summarizer per paper, then critics, then revisers, then one aggregator. The mother agent orchestrates and assembles the final document. Everything is automated end to end.

The mother agent's context is scarce and precious. The whole design rests on two rules that protect it:
1. **Subagents save their own output to disk** and return only a one-line status.
2. **The mother agent never reads full papers or full sheets into its own context.** It reads only the small aggregate files (cheat sheet, synthesis matrix) at the end.

## Inputs

Parse `$ARGUMENTS` for these. All are optional with sensible defaults.

- **papers folder** — default `Reference/` in the current working directory. Accept any folder of papers (PDFs primarily; also `.docx`, `.txt`, `.md`).
- **framework** — default: the bundled three-tier framework at `references/framework-three-tier.md`. If the user names a framework file (e.g. `paper-summary-lit-review2.txt` or any path), use that file's structure instead — read it first, and substitute its sections wherever the skill says "Tier 1 / 2 / 3".
- **output folder name** — default `<short-slug>_<yyyymmddhh>/` where the slug comes from the task and the timestamp is **Beijing time**. CRITICAL: place this folder at the **project root**, NOT inside `agent_tasks/`. (This is a user preference; do not bury output under `agent_tasks/`.) If a folder with the chosen name already exists, append a suffix to avoid overwriting.
- **severity** — default MEDIUM-HIGH (Execution). Use encouraging/Discovery severity only if the user calls this exploratory.

If anything is ambiguous, pick the sensible default and state it in one line, then proceed. Do not stall.

## The pipeline (run all phases, no human-in-the-loop)

Set up a todo list with one item per phase before starting, so progress is visible.

### Phase 1 — Inventory & plan
1. Get current **Beijing time** (`TZ='Asia/Shanghai' date +"%Y%m%d%H"`).
2. List the papers folder; count files; number them zero-padded (`01`, `02`, ...). Derive a short slug per paper from its filename.
3. Create the output folder at the project root: `{output_folder}/summaries/` and `{output_folder}/reviews/`.
4. Fill `assets/plan_template.md` with the paper list and counts, save it to `{output_folder}/plan.md`.
5. Do NOT ask for plan approval. Move straight to Phase 2.

### Phase 2 — Summarize (parallel, waves of ≤10)
- Dispatch **one summarizer subagent per paper** using the template in `references/subagent-prompts.md` (Summarizer section). Fill `{paper_path}`, `{output_path}` = `{output_folder}/summaries/NN_<slug>.md`, `{project_root}`.
- Cap parallel dispatch at **10 subagents per wave**. If there are more than 10 papers, run successive waves. (Each subagent reads its own PDF via the Read tool's `pages` parameter; it does not need every page of a long PDF.)
- Grant each subagent: Read, Write, Edit, Bash. Use the `general-purpose` agent type.
- Dispatch all subagents in a wave **in a single message** so they run concurrently. Collect only their one-line statuses.

### Phase 3 — Critic review (parallel)
- Split the sheets across **2 critic subagents** (~7 each; use 3 critics if >14 papers). Use the Critic template. Each writes `{output_folder}/reviews/review_{tag}.md`.
- Critics spot-check at least 3 sheets against the source papers to catch hallucinated numbers.
- Collect one-line statuses (scores + high-severity-issue count).

### Phase 4 — Revise (parallel)
- Mirror the critic split: **2 reviser subagents** (or 3), each owning the sheets one critic reviewed. Use the Reviser template.
- Revisers apply surgical fixes in place via Edit, and verify any flagged-as-possibly-hallucinated numbers against the source. No wholesale rewrites. Sheets scoring ≥85 get only light touches.
- Collect one-line statuses.

### Phase 5 — Aggregate (single subagent)
- Dispatch **one aggregator** using the Aggregator template. It reads all revised sheets (NOT the source papers) and writes `{output_folder}/cheat_sheet.md` (Tier 2) and `{output_folder}/synthesis_matrix.md` (Tier 3).
- The aggregator infers themes from the actual sheets rather than imposing a generic list, and produces a 4-5 sentence "Headline synthesis" at the top of the matrix.
- Collect its one-line status.

### Phase 6 — Assemble final deliverable (mother agent, on disk)
Do NOT read the 14+ sheets into context. Assemble by concatenating files on disk via Bash:

1. Read `assets/final_header_template.md`, substitute `{Title}` / `{date}` / `{N}` / `{papers_folder}`, write to a temp `_header.md`.
2. Write small divider snippets for Parts B, C, D.
3. Concatenate into `{output_folder}/final_literature_review.md`:
   `cat _header.md divider_b cheat_sheet.md divider_c synthesis_matrix.md divider_d summaries/*.md`
4. Remove the temp divider files. Report final line/word count and a one-line headline synthesis to the user.

## When to adapt vs. hold firm

- **Few papers (≤4):** you can collapse to a single wave and skip critic/reviser splits, but keep at least one critic + one reviser pass, the value is in the adversarial check.
- **Custom framework:** if the user supplied one, the summarizer/critic/reviser prompts reference it by path; the aggregator still builds a Tier-2-style cheat sheet and a themes-by-studies matrix using whatever sections the framework defines.
- **Non-PDF sources:** the summarizer prompt says "read the paper at {path}"; the Read tool handles `.docx`/`.txt`/`.md`. For `.doc`, fall back to the user's PDF-extraction cascade (pdftotext → pypdf/pdfplumber → OCR) per global CLAUDE.md.
- **A subagent returns a suspiciously precise number:** the critic phase is the safety net. Trust the critic + reviser verification loop over any single sheet.

## Why this design works (read before changing it)

- **Parallel summarizers** make the per-paper cost roughly constant in wall-clock regardless of how many papers, up to the wave cap.
- **Adversarial critic + reviser separation** (critics never create, revisers never self-score) keeps the quality check honest, matching the user's worker-critic pairing rule.
- **Aggregation as its own phase** is what turns N isolated sheets into a literature review: the synthesis matrix is the actual intellectual output, the sheets are just the evidence.
- **On-disk final assembly** means a 20-paper review does not blow up the mother agent's context. This is the single most important rule to preserve.

## Reference files (read when needed)
- `references/framework-three-tier.md` — the default Tier 1/2/3 rubric, with the marking system (✅/❌/➕/—) and pro-tips.
- `references/subagent-prompts.md` — copy-paste prompt templates for Summarizer, Critic, Reviser, Aggregator. Fill the `{PLACEHOLDERS}`.
- `assets/plan_template.md` — Phase 1 plan skeleton.
- `assets/final_header_template.md` — Phase 6 final-document header.

## Style rules (project-wide, non-negotiable)
- No em dashes anywhere in outputs. Use commas, colons, or parentheses.
- Folder timestamps use Beijing time.
- Output lives at the project root, not under `agent_tasks/`.

## After completion
Tell the user: the path to `final_literature_review.md`, the headline synthesis (one sentence), and offer to (a) tighten any sheet, (b) expand the synthesis matrix with extra themes, or (c) draft an actual lit-review section from the matrix. Save a project memory noting where the output folder lives so future sessions find it.
