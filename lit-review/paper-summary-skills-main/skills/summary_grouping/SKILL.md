---
name: summary_grouping
description: 整理文献标签。读取文献文件夹（默认 note，递归含子文件夹）中的 docx，提取每篇文献的关键词，建立或更新关键词矩阵 keyword_summary.xlsx，并生成检索说明 searching_readme.md。触发示例：「整理文献标签」「给文献打标签」「文献分组」「提取关键词」。
---

# summary_grouping — 文献分组表（关键词矩阵）

提取每篇文献的关键词，建成关键词矩阵 `keyword_summary.xlsx`，实现「检索任一关键词 → 筛出所有含该关键词的文献」。

## 参数与默认值
- 目标文件夹：用户指定，否则默认项目根目录下的 `note\`（递归）。
- 指定 docx：用户指定，否则处理文件夹中全部 docx。
- 输出文件名：用户指定，否则默认 `keyword_summary.xlsx`（生成在项目根目录）。

## 脚本
`scripts/grouping.py`（与本 SKILL.md 同级的 scripts 目录，用其绝对路径调用 `python`）。

## 流程
1. **抽取待处理文献与已有关键词**（结果写入工作文件）：
   ```
   python <脚本绝对路径> extract --folder <目标文件夹> --out <输出.xlsx> --json-out _work\grouping_extract.json
   ```
   stdout 打印摘要 `{"existing_keywords_count","new_count","json_out"}`；完整数据在 `_work\grouping_extract.json`：
   `{"existing_keywords":[...], "existing_papers":[...], "new":[{"filename","stem","text"},...]}`。
2. 若 `new_count` 为 0 → 告知用户没有新文献需要打标签，结束。
3. **逐篇提关键词**：用 Read 工具读取 `_work\grouping_extract.json`（文献多时分批），阅读每篇 `text`，**尽可能多地**提取关键词。
   - **关键词一致性（重要）**：凡能复用 `existing_keywords` 中已有表述的，必须复用，不要造同义新词（如已有「空间导航」就不要再用「空间定位」）。同一概念全程同一表述。
4. 汇总为 JSON 数组写入临时文件 `kw.json`（UTF-8）：`[{"文献名":"xx.docx","keywords":["a","b",...]}, ...]`。
5. **写入矩阵**：
   ```
   python <脚本绝对路径> write --out <输出.xlsx> --data kw.json
   ```
   脚本会建立/更新矩阵（第一列文献名，每关键词一列，含则标 X）、开启自动筛选、冻结首列与表头、自动换行，并在同目录生成 `searching_readme.md`。
6. 向用户报告文献数、关键词数、两个产出文件路径，并删除临时 `kw.json` 与 `_work\grouping_extract.json`。

## 注意
- 自动跳过以 `~$` 开头的 Word 临时文件，增量更新已有矩阵。
- 提醒用户：详细的筛选/检索操作见生成的 `searching_readme.md`。

## 大批量处理模式（文献数 > 20 篇时推荐，在 `/loop` 下运行）

与 summary_archiving 并行：同一批 agent 在生成 `row` 的同时，也提取并返回关键词列表，两项工作合并在一次 agent 调用中完成：

1. **预提取文本**：复用 summary_archiving 预提取的 `_work/r/NNN.txt` 文件（若单独运行 summary_grouping，则用 `grouping_extract.json` 的 `new[i].text` 同样预提取）。
2. **分批派发 agent**：每个 agent 读取一篇 txt，同时返回 `row`（文献总结）和 `keywords`（关键词列表）。
3. **关键词一致性**：agent 提示中须附上 `existing_keywords` 列表，要求复用已有表述，禁止造同义新词。
4. **汇总写入**：将各 agent 的 `keywords` 汇总写入 `_work/kw_bN.json`，再执行 `grouping.py write`。
5. **Auto-Continue 检查点**与 **增量去重** 规则同 summary_archiving：每批前检查控制文件，`grouping.py write` 按文献名自动去重。
