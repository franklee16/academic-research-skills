# Monthly Workflow Skill

Monthly Workflow is a Codex skill for running a file-based monthly planning, daily logging, task tracking, review, and monthly settlement system.

It turns a vague month of work into a visible operating system: goals are written down, daily tasks have completion standards, progress is recorded honestly, paused work stays paused, and the end of the month can be reviewed from actual evidence instead of memory.

## Why This Skill Exists

Many people try to manage monthly goals with scattered chats, todo lists, notebooks, and half-remembered plans. That works for a day or two, but it becomes fragile when:

- there are several parallel projects;
- plans change frequently;
- some days are skipped;
- tasks are partially completed;
- decisions get forgotten;
- AI conversations lose context;
- the user needs a weekly or monthly review.

This skill solves that by using a small set of stable Markdown files as long-term memory. Codex can read those files at the start of a conversation, update them during planning or review, and use them to keep the user’s workflow consistent across many days.

## Core Advantages

### 1. File-Based Memory

The workflow does not rely on one long chat thread. Important state is stored in Markdown files, so it can be restored in a new conversation or after context compression.

### 2. Honest Progress Tracking

The system separates planned work from completed work. Missed days, rest days, partial progress, and blockers are all valid records. This prevents the common problem of turning plans into fake achievements.

### 3. Clear Workstream Boundaries

Different lines of work can be separated into workstreams. For example: writing, experiments, reading, coding, meetings, collaboration, or personal study. Each workstream has its own scope and out-of-scope rules, which helps prevent context mixing.

### 4. Daily Execution Control

Each day starts with one main goal and a small task table. Every task has a completion standard, so the user can tell whether the day actually closed a useful loop.

### 5. Decision Preservation

Important decisions are written into a decision log. This is especially useful for paused projects, strategic pivots, priority changes, and rules that future planning must respect.

### 6. Weekly And Monthly Reviews

Because daily records are preserved, Codex can generate weekly reviews and month-end settlements from actual logs. This makes review work concrete rather than emotional or impression-based.

### 7. Domain-Agnostic Design

The workflow can be used for research, study, software development, writing, freelancing, career preparation, team collaboration, fitness plans, or any month-long goal system.

## What The Skill Provides

The skill includes a core instruction file:

- `SKILL.md`: the operating protocol for Codex.

It also includes reusable templates:

- `assets/templates/START_HERE.md`
- `assets/templates/current_state.md`
- `assets/templates/thread_index.md`
- `assets/templates/task_board.md`
- `assets/templates/daily_work_log.md`
- `assets/templates/decision_log.md`
- `assets/templates/monthly_review.md`

And a reference file:

- `references/workflow-patterns.md`: examples for adapting the workflow to research, coding, learning, and collaboration.

## Recommended Monthly Workspace

A typical monthly workspace looks like this:

```text
2026-06-workflow/
├── START_HERE.md
├── current_state.md
├── thread_index.md
├── task_board.md
├── daily_work_log.md
├── decision_log.md
└── monthly_review.md
```

## How To Install

Copy this skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R monthly-workflow ~/.codex/skills/monthly-workflow
```

After that, restart Codex or start a new conversation so the skill can be discovered.

## How To Use

### Start A New Monthly Workflow

Ask Codex:

```text
Use monthly-workflow to create my June work system.
My theme is research sprint.
My main goals are:
1. Finish the paper submission package.
2. Complete three software copyright documents.
3. Organize a new collaboration direction.
Please create the monthly workspace and templates.
```

Codex should create a folder, copy the templates, customize the workstreams, and initialize the current state, task board, daily log, and decision log.

### Plan A Day

Ask Codex:

```text
Today is 2026-06-04.
I have about 3 hours.
Please read my monthly workflow files and make today’s plan.
```

Codex should read the current state, recent logs, and task board, then write a daily plan into `daily_work_log.md`.

### Close A Day

Ask Codex:

```text
Update today’s progress:
I finished the paper outline, partially edited the figures, and did not start the cover letter.
Please update the daily log and task board honestly.
```

Codex should record completed, partial, and unfinished work separately.

### Pause A Workstream

Ask Codex:

```text
I do not want to continue the remote sensing task for now.
Please pause it and keep the restart condition.
```

Codex should record why it is paused, what has been done, the current blocker, and what would count as a restart condition.

### Review A Week

Ask Codex:

```text
Please review this week using my daily logs.
Summarize completed work, missed plans, blockers, and next week’s priorities.
```

### Settle A Month

Ask Codex:

```text
Please create my monthly review.
Use actual logs only.
Do not count planned work as completed work.
List completed outputs, unfinished tasks, open risks, and next month’s recommendations.
```

## Best Practices

- Keep one main goal per day.
- Use 3-6 task nodes per daily plan.
- Define completion standards before starting.
- Record missed days directly.
- Keep paused work out of daily plans until explicitly restarted.
- Write strategic decisions into `decision_log.md`.
- Do not let temporary tasks silently replace the month’s main goal.
- At month end, review from logs, not from memory.

## 中文介绍

Monthly Workflow 是一个用于 Codex 的月度工作流 Skill。它可以帮助用户建立一套基于 Markdown 文件的月度计划、每日工作日志、任务看板、决策记录、周复盘和月度决算系统。

它的核心作用是：把一个模糊的月份变成一个可以被看见、被记录、被复盘的工作系统。目标写在文件里，每日任务有完成标准，实际进展如实记录，暂停任务不会偷偷复活，月底复盘也不再依赖印象，而是根据真实日志进行整理。

## 为什么需要这个 Skill

很多人会用聊天记录、待办清单、笔记软件或者脑内计划来管理一个月的任务。短期内看起来能用，但一旦出现下面这些情况，就很容易混乱：

- 同时有多个项目；
- 计划经常变化；
- 有几天没有工作；
- 一些任务只完成了一部分；
- 重要决定过几天就忘了；
- AI 对话上下文丢失或被压缩；
- 月底想复盘，却记不清自己到底做了什么。

这个 Skill 的解决方式是：用一组稳定的 Markdown 文件保存长期记忆。Codex 每次开始新对话时都可以先读取这些文件，恢复当前状态；每次计划、记录、复盘时再更新这些文件，让整个工作流可以跨天、跨对话持续运行。

## 主要优点

### 1. 文件化长期记忆

它不依赖某一个超长聊天记录保存所有上下文，而是把关键状态写入文件。即使换一个新对话，也可以通过读取文件恢复工作状态。

### 2. 如实记录进展

系统明确区分“计划了”和“完成了”。没工作的日子、休息日、部分完成、任务卡住，都可以被正常记录，不需要伪装成进展。

### 3. 多主线清晰隔离

不同任务可以拆成不同工作流。例如：论文写作、实验代码、文献阅读、组会准备、外部协作、个人学习。每条主线都有自己的职责范围和边界，避免所有事情混在一个对话里。

### 4. 每日执行更具体

每天只设定一个主目标，并拆成少量任务节点。每个节点都有完成标准，所以当天结束时可以明确判断：今天到底有没有形成可验收进展。

### 5. 重要决定不会丢

战略性决定会写入 `decision_log.md`，例如暂停某个项目、改变优先级、切换方向、确认某条规则。之后做计划时必须尊重这些决定。

### 6. 周复盘和月度决算更可靠

因为每天都有记录，周复盘和月度决算可以直接从日志中整理，不需要依赖模糊印象。这样能更真实地看到完成了什么、没完成什么、为什么卡住、下个月应该怎么调整。

### 7. 适用于很多场景

它不只适合科研，也适合学习、编程、写作、自由职业、考研备考、求职准备、团队项目、健身计划和个人成长项目。

## Skill 内容

核心文件：

- `SKILL.md`：Codex 使用这个 Skill 时遵循的工作协议。

模板文件：

- `assets/templates/START_HERE.md`
- `assets/templates/current_state.md`
- `assets/templates/thread_index.md`
- `assets/templates/task_board.md`
- `assets/templates/daily_work_log.md`
- `assets/templates/decision_log.md`
- `assets/templates/monthly_review.md`

参考文件：

- `references/workflow-patterns.md`：针对科研、编程、学习、协作等场景的适配建议。

## 推荐的月度工作区结构

```text
2026-06-workflow/
├── START_HERE.md
├── current_state.md
├── thread_index.md
├── task_board.md
├── daily_work_log.md
├── decision_log.md
└── monthly_review.md
```

## 安装方法

把这个 skill 文件夹复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R monthly-workflow ~/.codex/skills/monthly-workflow
```

然后重启 Codex 或开启一个新对话，让 Codex 重新发现这个 Skill。

## 使用方法

### 创建新的月度工作流

可以这样对 Codex 说：

```text
请使用 monthly-workflow 帮我创建 6 月工作系统。
我的主题是科研冲刺。
我的主要目标是：
1. 完成论文投稿材料。
2. 整理三个软著文件。
3. 梳理新的科研合作方向。
请帮我创建月度工作区和模板文件。
```

Codex 应该会创建一个月度目录，并初始化当前状态、任务看板、每日工作日志、决策日志等文件。

### 制定当天计划

可以这样说：

```text
今天是 2026-06-04。
我大概有 3 个小时。
请读取我的月度工作流文件，帮我制定今天的计划。
```

Codex 会读取当前状态、最近日志和任务看板，然后把当天计划写入 `daily_work_log.md`。

### 记录当天进度

可以这样说：

```text
更新今天进度：
我完成了论文大纲，部分修改了图件，没有开始写 cover letter。
请如实更新每日工作日志和任务看板。
```

Codex 应该把完成、部分完成、未开始分别记录，不把计划项写成完成项。

### 暂停某条任务线

可以这样说：

```text
我暂时不想继续做遥感任务了。
请把它封存，保留当前卡点和重启条件。
```

Codex 会记录暂停原因、已完成内容、当前卡点，以及以后什么情况下可以重启。

### 做周复盘

可以这样说：

```text
请根据本周每日工作日志做一次周复盘。
总结完成事项、未完成计划、卡点和下周优先级。
```

### 做月度决算

可以这样说：

```text
请帮我做本月月度决算。
只根据实际日志记录，不要把计划过但没完成的任务写成完成。
请列出完成成果、遗留问题、风险和下个月建议。
```

## 最佳实践

- 每天只设定一个主目标。
- 每日计划控制在 3-6 个任务节点。
- 开始前写清楚完成标准。
- 没工作的日子也要如实记录。
- 暂停任务不要自动重新加入每日计划。
- 重要决定必须写进 `decision_log.md`。
- 临时任务不能悄悄挤掉月度主目标。
- 月底复盘要根据日志，而不是根据记忆。

## License

Choose a license before publishing this repository publicly.
