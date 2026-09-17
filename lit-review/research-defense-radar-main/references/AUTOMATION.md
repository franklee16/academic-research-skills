# Cross-platform Monitoring and Scheduling

Installation, the research workflow, and scheduling are separate. Install and enable the skill, complete a baseline manually, then create a schedule only after the user opts in.

## Default schedule proposal

When the user gives no cadence, propose Monday at 09:00 in the user's local timezone. Record the IANA timezone such as `Asia/Shanghai`, not only a UTC offset.

## Durable context choices

Prefer, in order:

1. a scheduled task inside the ongoing research chat;
2. a project-backed local task with explicit absolute state paths;
3. task/project attachments or an authorized connected service;
4. a standalone task whose prompt embeds the compact fingerprint and known-paper registry.

A task without readable prior state cannot perform an incremental comparison. It must announce a baseline reset.

## Codex / ChatGPT desktop prompt

```text
Use $research-defense-radar to run the incremental monitor for <project>.
Timezone: <Area/City>. State: <absolute project path or attached/connected location>.
Load the current fingerprint and prior paper registry. Search new and materially
revised scholarly work across the configured source families, verify substantive
claims from abstracts or full text, merge paper lineages, and report only material
A/B/C/E changes or exceptional D items. Record completed and failed coverage.
If the project WP has a verified public-disclosure date, keep later convergence
separate from pre-disclosure prior work and do not let it negate public-time novelty.
If prior state is unavailable, run a new baseline and do not call items newly found.
If coverage is incomplete, report that rather than saying nothing changed.
Respond in <English/Simplified Chinese/bilingual>.
```

When creating a ChatGPT task through the Skills UI, explicitly select `@Research Defense Radar`. A web task cannot use a path that exists only on the user's computer; use task/project files or a connected service instead.

## Claude Code prompt

```text
/research-defense-radar Run the incremental monitor for <project>.
Use the fingerprint and radar-state files at <absolute path>. Search and verify
new or materially revised work, update durable state, and report only meaningful
changes. Treat missing state as a baseline reset and incomplete source coverage
as a coverage warning. Apply the verified project-WP public date as the priority
cutoff; later papers are post-disclosure convergence, not prior work. Respond in <language>.
```

Claude cloud/Cowork sessions must have the skill enabled for the account or committed in the cloned project's `.claude/skills/`. Local-only personal skills are not automatically available to fresh remote runs.

## Scheduled-run checks

Before trusting the monitor:

- manually test the exact prompt;
- confirm web access on the scheduled surface;
- confirm the scheduled run can read and update durable state;
- review the first few runs for noise and missed known papers;
- verify the task reports coverage degradation;
- update the existing task after material project revisions.

Do not create overlapping schedules unless the user explicitly wants separate projects or cadences.
