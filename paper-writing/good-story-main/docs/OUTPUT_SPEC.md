# Output Specification

This file describes the expected output shape for `good-story`.

## Default Story Card

Use this when the user provides materials and asks for story diagnosis.

```markdown
## 最强故事

## 为什么这个故事成立

## 故事主线

## 证据地图

| 结论 | 证据 | 边界 |
|---|---|---|

## 薄弱点

## 重写目标
```

For English users:

```markdown
## Best story

## Why this story works

## Story spine

## Evidence map

| Claim | Evidence | Boundary |
|---|---|---|

## Weak points

## Rewrite targets
```

## Field Calibration Add-On

Use when the user is working across fields or asks whether the skill applies to a field.

```markdown
## 领域校准

- 你手里的材料属于哪类证据：
- 这个领域认什么证据：
- 结论可以说到什么强度：
- 这个领域的意义在哪里：
- 主要审稿风险：
```

## Candidate Story Add-On

Use for early projects.

```markdown
## 候选故事

| 排名 | 故事 | 优点 | 风险 |
|---|---|---|---|
```

## Figure Order Add-On

Use when the user provides a figure list.

```markdown
## 推荐图序

| 顺序 | 图 | 在故事里的任务 |
|---|---|---|

## 缺口
```

## Rebuttal Add-On

Use when the user asks for reviewer resistance.

```markdown
## 审稿风险

| 攻击点 | 严重程度 | 修补路径 |
|---|---|---|

## 更稳的写法
```

## Hard Requirements

- Do not invent evidence.
- Do not turn correlation into causation.
- Do not hide negative results or limitations.
- Do not use stronger claim verbs than the evidence supports.
- For Chinese users, avoid English framework labels unless they prevent ambiguity.
