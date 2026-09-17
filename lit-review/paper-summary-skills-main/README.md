# Paper Summary Skills｜文献总结技能包

一套面向科研文献管理的 Claude Code 技能（skill）集合，帮助你把一批 Word（`.docx`）文献，自动整理成**可检索、可筛选、可问答**的结构化资料。

整个流程围绕三件产出物：

| 产出物 | 文件 | 作用 |
| --- | --- | --- |
| 文献总结表 | `paper_archiving.xlsx` | 每篇文献一行，汇总基本信息与研究脉络 |
| 文献分组表 | `keyword_summary.xlsx` | 关键词矩阵，按任一关键词筛选出相关文献 |
| 文献名单 | `<问题关键词>.docx` | 针对你的提问，整理出可参考的文献清单 |

---

## 一、技能总览

本技能包包含 1 个主技能与 3 个子技能。主技能按你的意图自动调度子技能，子技能也可单独调用。

| 技能 | 触发示例 | 输入 | 输出 |
| --- | --- | --- | --- |
| **summary_note**（主） | `/summary_note` 或「帮我处理文献」 | 你的自然语言指令 | 路由到下方某个子技能 |
| **summary_archiving** | 「总结文献」「整理文献」 | `note\` 中的 `.docx` | `paper_archiving.xlsx` |
| **summary_grouping** | 「整理文献标签」 | `note\` 中的 `.docx` | `keyword_summary.xlsx` ＋ `searching_readme.md` |
| **summary_answering** | 「回答我的问题：XXX」 | 你的问题 ＋ 上述两张表 | `<问题关键词>.docx` |

> **术语约定**：本文中「文献文件夹」默认指项目根目录下的 `note\`（含其所有子文件夹）；「文献总结表」指 `paper_archiving.xlsx`；「文献分组表」指 `keyword_summary.xlsx`。全文保持一致，不使用同义替换。

---

## 二、安装

### 方式 A：作为插件全局使用（推荐）

1. 在 Claude Code 中添加本仓库为插件市场：
   ```
   /plugin marketplace add <你的-GitHub-用户名>/paper-summary-skills
   ```
2. 安装插件：
   ```
   /plugin install paper-summary
   ```
3. 重启或刷新后，`/summary_note` 等技能即可在任意项目中使用。

### 方式 B：作为单个项目使用

将 `skills\` 目录下的四个技能文件夹复制到目标项目的 `.claude\skills\` 中即可，仅在该项目内生效。

---

## 三、前置依赖

| 依赖 | 说明 |
| --- | --- |
| Python 3.9+ | 用于解析 `.docx` 与读写 `.xlsx` |
| `python-docx` | 解析 Word 文献 |
| `openpyxl` | 读写 Excel 表格 |

首次运行时，技能会自动检测并安装 `python-docx` 与 `openpyxl`，通常无需手动操作。如需手动安装：

```bash
pip install python-docx openpyxl
```

---

## 四、快速开始

1. 在项目根目录建立文献文件夹 `note\`，把要处理的 `.docx` 文献放进去（可分子文件夹）。
2. 生成文献总结表：
   ```
   总结文献
   ```
3. 生成文献分组表与检索说明：
   ```
   整理文献标签
   ```
4. 基于上述成果提问：
   ```
   回答我的问题：为什么 prior 很重要
   ```

所有产出文件都会生成在**项目根目录**。

---

## 五、大规模批量处理与 Auto-Continue 集成

当文献数量较多（> 20 篇）时，建议使用 `/loop` 模式配合批量并行处理，并可选集成 **Auto-Continue** 技能，在接近 Claude 5-hour 用量上限时自动暂停/恢复，无需人工守候。

### 5.1 `/loop` 批量处理模式

在 Claude Code 中，以 `/loop` 启动技能调用：

```
/loop 总结文献
/loop 整理文献标签
```

技能会自动循环执行以下步骤，直到所有新文献处理完毕：

1. 用 `extract` 命令找出尚未处理的新文献；
2. 将文献文本预先提取到 `_work/r/` 目录（每篇一个 `.txt` 文件）；
3. 分批（每批约 12 篇）派发并行 agent，每个 agent 独立处理一篇，返回 JSON；
4. 每批处理完毕后写入 xlsx，然后检查 Auto-Continue 控制文件，决定继续还是暂停；
5. 全部处理完毕后，用 `extract` 验证 `new_count == 0`，`/loop` 自动结束。

**效率说明**：12 个 agent 并行运行，处理速度约为逐篇串行的 10 倍，百篇文献通常在 2–3 个 `/loop` 迭代内完成。

### 5.2 Auto-Continue 集成（可选）

[Auto-Continue](https://github.com/CrisChenYingyan/auto-continue) 是一个独立的监控进程，定期读取 Claude 网页版的 5-hour 用量百分比，并将 `state: "RUN" / "PAUSE"` 写入本地控制文件（默认路径：`~/.claude/auto_continue/control.json`）。

本技能在以下**安全检查点**读取控制文件：

- 每次 `/loop` 迭代开始时
- 派发每批并行 agent 之前

| 读到的 `state` | 行为 |
| --- | --- |
| `"RUN"` | 继续派发下一批 |
| `"PAUSE"` | 完成当前最小原子步骤 → 保存进度到 `CLAUDE.md` → 等待下轮 `/loop` 自动唤醒 |
| 文件缺失 / 解析失败 / 时间戳超过 40 分钟 | 视为 `RUN`，正常处理，不卡死 |

恢复时，配合增量去重（`extract` 只返回尚未处理的文献），从中断处继续，**不重复处理已完成文献**。

### 5.3 工作目录结构（`_work/`）

批量处理过程中，中间结果存储在 `_work/` 目录（已被 `.gitignore` 排除，不上传 GitHub）：

```
_work/
├─ archiving_extract.json   # extract 输出（含待处理文献列表与 text）
├─ grouping_extract.json    # grouping extract 输出
├─ r/
│   ├─ 000.txt              # 第 0 篇文献的完整文本（供 agent 读取）
│   ├─ 001.txt
│   └─ ...
├─ rows_b1.json             # 第 1 批 agent 汇总的文献总结 rows
├─ kw_b1.json               # 第 1 批 agent 汇总的关键词
└─ gen_b1.py                # 生成上述 json 的临时脚本（可删除）
```

---

## 六、各技能详解

### 1. summary_archiving — 文献总结表

逐篇阅读文献全文，生成「每篇一行」的总结表 `paper_archiving.xlsx`。

- **默认范围**：`note\`（递归）中的全部 `.docx`；也可指定文件夹或单篇文献。
- **增量更新**：若表已存在，仅追加新文献，自动忽略重复条目。
- **列结构**（从左到右）：

  | 列 | 内容 |
  | --- | --- |
  | 文献名 | 文件名 |
  | 发表年份 | |
  | 期刊 | |
  | 摘要 | 研究背景（一句）／解决方案（一句）／创新点（一句） |
  | 研究内容 | 研究问题（一句）／研究方法（关键词或短句） |
  | 主要结果 | 分点短句，与数据分析方法一一对应（结果1：xxx，数据分析方法：xxx） |
  | 研究思路 | 提出 xxx 问题，通过 xxx 实验/方法得到 xxx 结果，解决该问题（若未解决则引入 xxx 实验） |

- **排版**：单元格内容自动换行；文字精简，优先用关键词或短句。

### 2. summary_grouping — 文献分组表

提取每篇文献的关键词，建立**关键词矩阵**，实现「检索任一关键词 → 筛出所有含该关键词的文献」。

- **默认范围**：`note\`（递归）中的全部 `.docx`。
- **关键词一致性**：尽可能多地提取关键词，并在不同文献间保持同一表述。
- **表结构**：第一列为文献名，其后每个关键词占一列，文献含该关键词则标 `X`。
- **筛选能力**：表头开启自动筛选，首列与表头冻结。
- **配套说明**：同时生成 `searching_readme.md`，详述单关键词筛选、多关键词组合筛选与清除筛选的操作步骤。

### 3. summary_answering — 文献名单

把你的问题规范化、分解，再检索现有表格，整理出可参考的文献。

- **触发**：`回答我的问题：XXX`
- **检索逻辑**：
  - 文献分组表与文献总结表**都存在** → 同时检索两者；
  - **仅存在其一** → 用现有的检索，并在反馈中提示缺失的另一份；
  - **两者都不存在** → 先与你确认确无此二表，并申请直接检索全部 `.docx` 来整理名单。
- **输出**：生成 `<问题关键词>.docx`，列出「可直接回答的文献」与「话题相关的文献」两类名单；同时在文献总结表中筛选呈现这些文献对应的行。若无文献总结表，会先与你确认是否需要生成。

### 4. summary_note — 主技能（意图路由）

根据你的指令自动选择子技能：

| 你的意图 | 调度的子技能 |
| --- | --- |
| 含「总结 / 归档 / 整理文献」 | summary_archiving |
| 含「标签 / 分组 / 关键词分组」 | summary_grouping |
| 含「回答 / 问题」 | summary_answering |
| 意图不明确 | 列出菜单，由你选择 |

---

## 七、目录结构

```
paper-summary-skills\
├─ README.md                       本文件
├─ .claude-plugin\
│   ├─ plugin.json                 插件清单
│   └─ marketplace.json            插件市场清单
└─ skills\
    ├─ summary_note\        SKILL.md
    ├─ summary_archiving\   SKILL.md ＋ scripts\archiving.py
    ├─ summary_grouping\    SKILL.md ＋ scripts\grouping.py
    └─ summary_answering\   SKILL.md ＋ scripts\answering.py
```

---

## 八、注意事项

- **文件名**：支持中英文混合与较长文件名，处理时按原样保留；去重以「文件名（去扩展名、去首尾空格）」为准。
- **临时文件**：自动跳过以 `~$` 开头的 Word 临时文件。
- **数据安全**：所有处理均在本地完成，不上传文献内容。
- **重复运行**：总结表与分组表均为增量更新，可安全地多次运行。

---

## 九、许可证

MIT License。欢迎自由使用、修改与分发。
