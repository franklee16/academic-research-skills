---
name: monthly-workflow
description: Create and operate a file-based monthly planning, daily work log, task board, decision log, weekly review, and monthly settlement workflow. Use when the user wants to plan a month, track daily tasks, maintain honest progress records, monitor goals, review a week/month, archive work, or turn a personal/project sprint into reusable Markdown logs.
---

# Monthly Workflow

Use this skill to help a user run a month-long work system with file-based memory. The workflow is domain-agnostic: research, study, writing, coding, freelancing, team projects, career prep, fitness, or any recurring goal system.

## Core Idea

Maintain one monthly workspace folder with stable Markdown files:

- `START_HERE.md`: entry point for restoring context.
- `current_state.md`: short, current state snapshot.
- `thread_index.md`: boundaries for workstreams/conversations.
- `task_board.md`: To Do / Doing / Done / Paused board.
- `daily_work_log.md`: daily plan, check-in, completion record, blockers, review.
- `decision_log.md`: important decisions that future planning must respect.
- `monthly_review.md`: end-of-month settlement.

For template wording, copy or adapt files from `assets/templates/`.

## Workflow

### 1. Initialize A Monthly Workspace

When the user asks to start a new month, create a folder named with a stable month slug, such as `2026-06-workflow` or `2026-06-research-sprint`.

Create or adapt these files:

1. `START_HERE.md`
2. `current_state.md`
3. `thread_index.md`
4. `task_board.md`
5. `daily_work_log.md`
6. `decision_log.md`

Ask for only the minimum missing information:

- Month and theme.
- 1-3 primary goals.
- Major workstreams.
- Known deadlines.
- Any tasks that should be paused or explicitly excluded.

If the user gives fuzzy goals, convert them into measurable outcomes, but keep uncertainty visible.

### 2. Plan The Month

Create a monthly plan with:

- Primary goals: the few outcomes that would make the month successful.
- Workstreams: separate lines of work with clear boundaries.
- Time allocation: approximate shares, not rigid schedules.
- Milestones: weekly or deadline-based checkpoints.
- Risks: foreseeable blockers and overcommitment traps.
- Definition of done: what counts as finished.

Do not inflate aspirations into commitments. Keep “planned”, “started”, “completed”, “paused”, and “abandoned” separate.

### 3. Start A Day

When the user asks for today’s plan:

1. Read `current_state.md`, `task_board.md`, and recent entries in `daily_work_log.md`.
2. Confirm the date if it is ambiguous.
3. Choose one daily main goal.
4. Create a checklist with 3-6 task nodes.
5. Give each node a completion standard.
6. Add a short execution order and cutoff rules.
7. Write the plan into `daily_work_log.md`.

Prefer this shape:

```text
今日主目标：
- One clear main outcome.

今日计划打卡表：
T0 启动与材料定位
T1 主任务
T2 次任务
T3 收尾记录

完成标准：
- Concrete, observable, and small enough to verify today.
```

### 4. Close A Day

When the user reports progress:

1. Record actual work by date.
2. Mark partial completion honestly.
3. Preserve blockers with enough detail to resume later.
4. Write the next day’s first task.
5. Update `task_board.md` when task state changes.
6. Update `current_state.md` when the project state changes.
7. Update `decision_log.md` only for durable strategic decisions.

Use this distinction:

- Completed: finished and verifiable.
- Partial: started but not closed; specify remaining work.
- Blocked: stopped by a concrete issue; record the issue.
- No work/rest: valid record; do not disguise it as progress.

### 5. Manage Workstreams

Use `thread_index.md` to keep workstreams separate. For each workstream, define:

- Scope: what this stream handles.
- Out of scope: what it must not handle.
- Entry files or resources.
- Current priority and status.

When a user wants to stop a line of work, create a paused/sealed state instead of deleting it:

- Why it is paused.
- What has been done.
- Current blocker.
- What would restart it.

### 6. Review Weekly Or Monthly

For reviews, read the logs first. Then produce:

- Overall conclusion.
- Summary by workstream.
- Date timeline.
- Concrete completed outputs.
- Unfinished work and residual risks.
- Lessons about process and attention.
- Next-period recommendations.

For a monthly settlement, create or update `monthly_review.md`. Be strict: if completion status is not logged, write “待确认” rather than assuming success.

## Logging Standards

Be honest and low-drama:

- Do not rewrite missed days as productive days.
- Do not count plans as completed work.
- Do not hide rest days.
- Do not reactivate paused work unless the user explicitly asks.
- Do not mix unrelated workstreams in the same execution thread unless the user is doing a total-control review.

Use exact dates for records. If the user gives relative dates like “yesterday” and the current date is known, resolve it to an exact date before writing.

## File Update Rules

Update files only when the user asks to record, plan, review, initialize, archive, or settle work.

Use this mapping:

- Daily plan or progress: `daily_work_log.md`
- Task state changes: `task_board.md`
- Current project status: `current_state.md`
- Strategic decisions: `decision_log.md`
- Workstream boundaries: `thread_index.md`
- Month-end summary: `monthly_review.md`

When editing existing logs, preserve prior entries. Add corrections explicitly instead of silently overwriting history, unless the user asks to fix a mistaken record.

## Templates

Use these bundled templates as starting points:

- `assets/templates/START_HERE.md`
- `assets/templates/current_state.md`
- `assets/templates/thread_index.md`
- `assets/templates/task_board.md`
- `assets/templates/daily_work_log.md`
- `assets/templates/decision_log.md`
- `assets/templates/monthly_review.md`

Copy templates into the user’s workspace and customize names, dates, goals, workstreams, and rules.
