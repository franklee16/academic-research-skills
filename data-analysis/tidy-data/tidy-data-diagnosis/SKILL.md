---
name: tidy-data-diagnosis
description: |
  当用户拿到一个新数据集想判断其结构是否规范时激活。典型场景:用户刚导入 CSV/Excel/数据库表,觉得"这个表看着不对劲"、"列名怎么是数字"、"行和列好像反了"、"数据太宽/太长"。
  语言信号: "这个数据集很乱"、"怎么把宽表变长表"、"列头是年份/月份不是变量名"、"一个人占了多行"、"一个单元的数据分成了好几个文件"。
  不适用于: 数据清洗中的缺失值处理、异常值检测、日期解析 — 这些是数据质量(data quality)问题,不是数据结构(data structure)问题。
source_book: "Tidy Data — Hadley Wickham"
source_chapter: Section 2–3
tags: [data-structure, diagnosis, tidy-data, data-cleaning]
related_skills: []
---

# 整洁数据诊断

## R — 原文 (Reading)

> "Tidy datasets are easy to manipulate, model and visualise, and have a specific structure: each variable is a column, each observation is a row, and each type of observational unit is a table."
>
> "Real datasets can, and often do, violate the three precepts of tidy data in almost every way imaginable. This section describes the five most common problems with messy datasets, along with their remedies."
>
> — Hadley Wickham, Section 2.3 & Section 3

---

## I — 方法论骨架 (Interpretation)

整洁数据有三条规则: (1) 每个变量占一列, (2) 每个观察占一行, (3) 每种观察类型占一个表。违反任何一条就是杂乱数据。

作者从实战经验中提炼出**五种高频杂乱模式**:

1. **列头是值,不是变量名** — 列头是"2019"、"2020"或"<$10k"、"$10-20k"这样的值
2. **一列含多个变量** — 列名 "m1524" 实际编码了性别(m)和年龄段(15-24)
3. **变量同时散布在行和列** — 有些变量在列头里,另一些在行值里(如气象数据的 tmin/tmax 作为行值)
4. **一个表里混了多种观察类型** — 歌曲(元数据)和排名(时序)挤在同一张表
5. **一种观察类型分散在多表/多文件** — 每年一个 CSV,结构相似但不合并

诊断的核心动作是: 对着三条规则逐一检查,把违规之处归入上述五类之一。归类完成,修复路径就明确了 (melt / split / cast / 分表 / 合并)。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: Pew 宗教收入调查
- **问题**: 列头是收入区间("<$10k", "$10-20k", ...),不是变量名;数据是宽表,三个变量 (religion, income, frequency) 中 income 被铺成了列头
- **方法论的使用**: 归类为模式 1 (列头是值), 用 melt 操作将收入区间列头转为 income 变量, 原数值转为 freq 变量
- **结论**: 融化后每行 = 一个 (religion, income) 组合的频次, 满足三条规则
- **结果**: 得到标准的三列表 (religion, income, freq), 可直接接入可视化或建模

### 案例 2: TB (结核病) 数据集
- **问题**: 列名如 "m014"、"f1524" 同时编码了性别和年龄段 — 一列含两个变量
- **方法论的使用**: 归类为模式 1 + 模式 2 的组合; 先 melt 将列头转为单列, 再 split 该列拆出 sex 和 age 两个独立变量
- **结论**: 整洁后的数据还方便加入 population 变量计算发病率, 这在原始格式中极难实现
- **结果**: 四列表 (country, year, sex, age, cases), 可与人口数据 join

### 案例 3: 墨西哥气象站数据
- **问题**: 变量 tmin/tmax 出现在行值 (element 列) 中, 日期铺在 d1–d31 列头里 — 变量同时散布在行和列
- **方法论的使用**: 归类为模式 3; 先 melt (colvars=id, year, month), 再 cast 将 element 列的变量名转回列头
- **结论**: 整洁后每行 = 一天一个站点的气象记录, tmin 和 tmax 各占一列
- **结果**: 标准五列表 (id, date, tmax, tmin), 可直接用于时间序列分析

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?

1. 刚拿到一个 CSV/Excel/数据库导出, 打开一看觉得"结构很奇怪", 想判断哪里不规范
2. 在做数据分析前想先"检查一下数据结构是否正确", 避免后续反复返工
3. 接手了别人的数据集, 列名看不懂或者明显不是变量名, 需要快速定位问题
4. 多个文件/表需要合并, 但不确定它们是否已经是统一的整洁格式

### 语言信号 (用户的话里出现这些就应激活)

- "这个数据集的结构不对/很乱/需要整理"
- "列名怎么是年份/月份/数值"
- "这个表太宽了/太长了, 需要变换格式"
- "行和列好像反了"
- "一个单元的数据分成好几个文件"
- "怎么判断数据是不是 tidy 的"

### 与相邻 skill 的区分

- 与 `messy-to-tidy-pipeline` 的区别: 本 skill 只做**诊断**(识别问题并归类), 不执行修复; `messy-to-tidy-pipeline` 是从诊断到修复的端到端流程
- 与 `multi-table-merge` 的区别: 本 skill 诊断单表的结构问题; `multi-table-merge` 处理多表/多文件的合并问题

---

## E — 可执行步骤 (Execution)

当 skill 被激活后, agent 应按以下步骤执行:

1. **展示三条整洁规则, 逐一对照数据集**
   - 规则 1: 每个变量是否占一列? 列头是否真的是变量名 (而不是值)?
   - 规则 2: 每个观察是否占一行? 有没有同一观察的属性散布在多行?
   - 规则 3: 表中是否只有一种观察类型? 有没有不同粒度的实体混在一起?
   - 完成标准: 对每条规则给出 "通过 / 违反" 的判断, 并指出具体位置

2. **将违规归类到五种杂乱模式之一**
   - 模式 1: 列头是值 → 标出哪些列头其实是值
   - 模式 2: 一列多变量 → 标出哪些列编码了多个变量, 拆分点在哪
   - 模式 3: 变量在行和列 → 标出哪些行值其实是变量名
   - 模式 4: 混合观察类型 → 标出哪些行/列属于不同实体
   - 模式 5: 分散多表 → 标出文件/表之间的共性结构
   - 完成标准: 每个违规都有明确的模式归属和修复方向
   - 判停条件: 如果三条规则全部通过 → 报告"数据集已是整洁格式", 跳到步骤 4

3. **输出诊断报告**
   - 格式: 表格 (规则 | 状态 | 违规描述 | 归属模式 | 修复方向)
   - 对每个违规给出修复操作的关键词 (melt / split / cast / 分表 / 合并)
   - 完成标准: 报告可独立交付给用户或直接喂给 `messy-to-tidy-pipeline` 执行

4. **建议下一步**
   - 如果有违规: 推荐调用 `messy-to-tidy-pipeline` 进行修复
   - 如果全部通过: 建议直接进入分析 (filter / transform / aggregate / sort)

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill

- 数据质量问题 (缺失值、异常值、编码错误、日期解析) — 这是 data quality 而非 data structure 问题
- 用户明确知道问题所在只是想执行 melt/pivot 操作 — 直接进入 `messy-to-tidy-pipeline`
- 模式设计 / 数据库 schema 设计 — 本 skill 面向已有数据集的事后诊断, 不用于从零设计

### 作者在书中警告的失败模式

- **变量 vs. 观察的判定不总是明确的**: 同样的数据在不同分析目的下, 变量和观察的划分可能不同 (身高/体重可以是两个变量,也可以是"维度"变量的两个值)。诊断时必须结合分析意图, 不能机械套用
- **过度整洁化**: 并非所有非整洁格式都需要修复 — 宽表对于完全交叉设计更紧凑且支持矩阵运算, 如果分析本身只需要矩阵操作就不必 melt

### 作者的盲点 / 时代局限

- 论文基于 2014 年的 R 生态 (reshape2/plyr); 如今 tidyr/dplyr/pandas 的 API 已不同, 但诊断逻辑 (五种模式) 仍然成立
- 未讨论大数据场景: 当数据集无法全部载入内存时, 诊断策略需要调整 (采样诊断 vs. 全量诊断)

### 容易混淆的邻近方法论

- **数据库范式化 (Normalization)**: 概念相关 (Codd 3NF ≈ 整洁数据), 但范式化关注的是消除冗余和依赖异常, 整洁数据更关注分析便利性。二者有时冲突: 范式化到极致可能不利于分析
- **数据质量清洗**: 结构问题 (本 skill) vs. 内容问题 (缺失/异常/编码) — 两个不同维度

---

## 相关 skills

- **depends-on**: (无 — 这是基础诊断 skill)
- **composes-with**: [`messy-to-tidy-pipeline`](../messy-to-tidy-pipeline/SKILL.md) — 诊断结果直接驱动修复操作序列; [`multi-table-merge`](../multi-table-merge/SKILL.md) — 诊断识别模式 4/5 后推荐合并/拆分

---

## 审计信息

- **验证通过**: V1 ✓ (五种模式在 Pew/TB/weather/Billboard/baby-names 五个独立案例中均有佐证) / V2 ✓ (可诊断书外数据集如 Kaggle 竞赛数据) / V3 ✓ (五种杂乱模式的分类体系是 Wickham 独创, 非常识)
- **测试通过率**: 待阶段 4 测试
- **蒸馏时间**: 2026-05-15
