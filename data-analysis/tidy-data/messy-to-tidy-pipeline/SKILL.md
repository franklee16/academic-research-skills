---
name: messy-to-tidy-pipeline
description: |
  当用户已经知道数据集结构不规范(或经 tidy-data-diagnosis 诊断后),需要端到端执行从杂乱到整洁的转换时激活。典型场景:用户说"帮我把这个宽表变成长表"、"把这几列拆开"、"数据需要reshape/pivot/melt"。
  语言信号: "帮我 melt/reshape/pivot 这个表"、"把宽表变长表"、"列头里有变量信息需要提取"、"这个表需要分拆"。
  不适用于: 纯数据质量问题(缺失值/异常值)、数据库设计、可视化。
source_book: "Tidy Data — Hadley Wickham"
source_chapter: Section 3–4
tags: [data-transformation, tidy-data, pipeline, melt, cast, split]
related_skills: []
---

# 从杂乱到整洁的端到端流程

## R — 原文 (Reading)

> "Surprisingly, most messy datasets, including types of messiness not explicitly described above, can be tidied with a small set of tools: melting, string splitting, and casting."
>
> "Tidy datasets and tidy tools work hand in hand to make data analysis easier, allowing you to focus on the interesting domain problem, not on the uninteresting logistics of the data."
>
> — Hadley Wickham, Section 3 & Section 1

---

## I — 方法论骨架 (Interpretation)

整洁化数据只需要三种原子操作, 按需组合:

1. **Melt (融化)**: 把列头变成值。参数化方式是指定 "colvars"(保持不动的列),其余列的列头汇入一个新变量(原列名),数据汇入另一个新变量(原值)。效果: 宽表变长表。

2. **Split (拆分)**: 把一个列拆成多个变量。当一个列名编码了多个维度(如 "m1524" = 性别 m + 年龄 15-24),用分隔符或正则把一列拆成独立的列。

3. **Cast (铸造)**: 把行中的值变成列。是 melt 的逆操作,把一个"变量名"列里的不同取值展开成独立列。效果: 长表变宽表 (但与原始宽表不同,现在变量在正确的维度上)。

端到端流程是: **诊断 → (melt → split → cast) 按需组合 → 分表(若混合观察类型) → 验证**。关键洞察是: 绝大多数杂乱数据都可以通过这三种操作的组合修复, 不需要为每种特殊情况发明新工具。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: Billboard 排行榜数据
- **问题**: 列头是 wk1–wk75 (周排名), 列头是值; 且同一张表混了歌曲元数据(artist, track, time)和每周排名两种观察类型
- **方法论的使用**: Step 1 — melt (colvars=year, artist, track, time, date.entered), 得到 week 和 rank 两列; Step 2 — 清洗 week 列(提取数字); Step 3 — 计算 date = date.entered + week; Step 4 — 分表: 歌曲表(id, artist, track, time) + 排名表(id, date, rank)
- **结论**: 分表后消除了歌曲元数据的冗余重复, 每个事实只表达一次
- **结果**: 两张整洁表, 可独立查询歌曲信息和排名趋势, 也可通过 id join

### 案例 2: TB 数据集 (融化 + 拆分组合)
- **问题**: 列名 "m014"/"f1524" 同时编码性别和年龄; 先 melt 后 column 列含复合信息
- **方法论的使用**: Step 1 — melt (colvars=country, year), 得到 column 和 cases; Step 2 — split column 列: 用字符串匹配或查找表将 "m014" → sex="m", age="0-14"; Step 3 — 额外收益: 整洁格式下可直接添加 population 和 rate 列
- **结论**: 先 melt 后 split 是处理复合列名的标准两步法; 分拆后还解锁了原格式下不可能的派生变量计算
- **结果**: (country, year, sex, age, cases) 五列表, 可与人口数据 join 计算发病率

### 案例 3: 墨西哥气象数据 (融化 + 铸造组合)
- **问题**: 日期铺在 d1–d31 列, 变量名(tmin/tmax)在 element 列的行值里
- **方法论的使用**: Step 1 — melt (colvars=id, year, month, element), 得到 day 和 value; Step 2 — 删除结构性缺失值; Step 3 — cast: 将 element 列(tmin/tmax)展开为独立列; Step 4 — 从 year/month/day 合成 date 变量
- **结论**: melt→cast 组合解决了"变量同时在行和列"的复杂杂乱模式
- **结果**: (id, date, tmax, tmin) 整洁表, 每行 = 一天一站点的气象记录

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?

1. 经 `tidy-data-diagnosis` 诊断后, 知道了杂乱模式, 需要执行修复
2. 拿到宽表(列头是时间/类别/区间)需要变成长表以便分析
3. 列名中嵌入了多个维度信息(如 "Q1_2023_Beijing"), 需要拆成独立变量
4. 一个表里既有实体属性又有时序/重复测量数据, 需要分表
5. 多个格式相同的文件/表需要合并后再整洁化

### 语言信号 (用户的话里出现这些就应激活)

- "帮我把这个表 melt/reshape/pivot 一下"
- "宽表变长表" / "长表变宽表"
- "列名里有变量信息需要提取出来"
- "这个表需要分拆成多个表"
- "数据需要 unpivot/normalize"
- "怎么把这个 Excel 的交叉表转成能分析的格式"

### 与相邻 skill 的区分

- 与 `tidy-data-diagnosis` 的区别: 本 skill 执行修复, 诊断 skill 只识别问题。如果用户还没诊断, 先调 `tidy-data-diagnosis`
- 与 `multi-table-merge` 的区别: 本 skill 处理单表的 reshape/分拆; `multi-table-merge` 处理多文件/多表的合并。但二者经常顺序配合: 先 multi-table-merge 再 messy-to-tidy-pipeline

---

## E — 可执行步骤 (Execution)

当 skill 被激活后, agent 应按以下步骤执行:

1. **诊断 (若未完成)**
   - 如果用户已提供诊断结果, 直接进入步骤 2
   - 如果未诊断, 先执行 `tidy-data-diagnosis` 的三步流程
   - 完成标准: 明确每个违规的模式归属 (1–5)

2. **规划操作序列**
   - 根据诊断结果, 列出需要的操作序列 (melt → split → cast → 分表 → 合并)
   - 每个操作指定参数: melt 的 colvars 是什么, split 的分隔符/正则是什么, cast 的 key 是什么
   - 完成标准: 有一张"操作清单", 用户可审核
   - 判停条件: 如果诊断发现数据已整洁 → 直接报告, 跳到步骤 5

3. **逐步执行操作**
   - **模式 1 (列头是值)**: 执行 melt, 指定 colvars, 生成 column + value 两列; 重命名以反映语义
   - **模式 2 (一列多变量)**: 在 melt 之后, 执行 split — 用分隔符/正则/查找表将复合列拆为多列
   - **模式 3 (变量在行和列)**: 先 melt (保留含变量名的列为 colvar), 再 cast 将变量名列展开
   - **模式 4 (混合观察类型)**: 识别重复的事实(如歌曲元数据), 拆为两张表, 用外键关联
   - **模式 5 (分散多表)**: 先调用 `multi-table-merge` 合并, 再整洁化
   - 完成标准: 每步操作后数据集的行数/列数符合预期; 无数据丢失

4. **验证整洁性**
   - 用三条规则逐一检查输出
   - 抽查: 随机取 5 行, 确认每行是一个观察、每列是一个变量
   - 完成标准: 三条规则全部通过

5. **交付**
   - 输出整洁后的数据集 (或代码)
   - 如果做了分表, 说明表间关系和外键
   - 标注哪些变量是 fixed (设计变量), 哪些是 measured (测量变量), 建议排序顺序

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill

- **数据质量问题**: 缺失值插补、异常值修正、编码转换 — 这些在整洁化之前或之后处理, 但不是整洁化本身
- **小规模手动调整**: 如果只是改几个列名或删几列, 不需要走完整流程
- **流数据 / 实时数据**: 本流程假设数据已收集完毕, 是批量(batch)操作

### 作者在书中警告的失败模式

- **变量和观察的误判**: 同样的数据在不同分析目的下整洁格式可能不同 (如身高/体重作为两列 vs. 作为 "维度" 变量的两个值)。必须先明确分析目的再执行 reshape
- **过度 reshape**: 宽表对于完全交叉设计有时更自然; 如果分析只需要矩阵运算, 不必强行 melt
- **分表后的不可逆性**: 分表后如果要分析需要 denormalize (join 回来), 但大多数统计工具不直接支持关系数据操作

### 作者的盲点 / 时代局限

- 三种操作 (melt/split/cast) 是以 R 的 reshape2 为原型的; Python pandas 中对应的是 melt/str.split/pivot_table, API 和参数名不同但逻辑一致
- 未考虑大数据场景: 当数据无法全量载入时, melt/cast 需要在数据库或 Spark 中执行, 策略不同
- 未考虑嵌套数据 (JSON/XML) 的整洁化: 这在现代数据工程中很常见, 但超出了论文范畴

### 容易混淆的邻近方法论

- **数据库范式化**: 目标相似(消除冗余), 但动因不同 — 范式化为了存储一致性, 整洁化为了分析便利性
- **ETL (Extract-Transform-Load)**: 更宽泛的概念, 整洁化是 T (Transform) 的一个子集

---

## 相关 skills

- **depends-on**: [`tidy-data-diagnosis`](../tidy-data-diagnosis/SKILL.md) — 修复前需先诊断
- **composes-with**: [`multi-table-merge`](../multi-table-merge/SKILL.md) — 先合并多文件再 reshape, 或分表后分别整洁化

---

## 审计信息

- **验证通过**: V1 ✓ (melt/split/cast 在 Billboard/Pew/TB/weather 四个独立案例中组合使用) / V2 ✓ (可处理书外场景如 Kaggle 竞赛数据的 reshape) / V3 ✓ (三种操作的组合逻辑是 Wickham 框架的核心贡献, 非常识)
- **测试通过率**: 待阶段 4 测试
- **蒸馏时间**: 2026-05-15
