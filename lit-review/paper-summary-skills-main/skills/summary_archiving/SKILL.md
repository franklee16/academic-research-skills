---
name: summary_archiving
description: 读取文献文件夹（默认 note，递归含子文件夹）中的 docx，逐篇生成或更新文献总结表 paper_archiving.xlsx（每篇文献一行）。触发示例：「总结文献」「整理文献」「归档文献」「生成文献总结表」。
---

# summary_archiving — 文献总结表

把文献文件夹里的 docx 逐篇读完，汇总成「每篇一行」的文献总结表 `paper_archiving.xlsx`。

## 参数与默认值
- 目标文件夹：用户指定，否则默认项目根目录下的 `note\`（递归）。
- 指定 docx：用户指定，否则处理文件夹中全部 docx。
- 输出文件名：用户指定，否则默认 `paper_archiving.xlsx`（生成在项目根目录）。

## 脚本
`scripts/archiving.py`（与本 SKILL.md 同级的 scripts 目录，用其绝对路径调用 `python`）。

## 流程
1. **抽取待处理文献**（结果写入工作文件，避免大体量输出）：
   ```
   python <脚本绝对路径> extract --folder <目标文件夹> --out <输出.xlsx> --json-out _work\archiving_extract.json
   ```
   stdout 打印摘要 `{"existing_count","new_count","json_out"}`；完整数据在 `_work\archiving_extract.json`：
   `{"existing":[...已收录...], "new":[{"filename","stem","text"},...]}`。
   `new` 为尚未收录的文献（已收录的自动忽略，实现增量更新去重）。
2. 若 `new_count` 为 0 → 告知用户没有新文献需要添加，结束。
3. **逐篇生成总结**：用 Read 工具读取 `_work\archiving_extract.json`（文献多时分批读取 `new`），阅读每篇 `text`，按下方列模板生成一行。文字精简，能用关键词/短句就不写整句。
4. 把所有行汇总为 JSON 数组写入临时文件 `rows.json`（UTF-8），每个元素含下列键。
5. **写入表格**：
   ```
   python <脚本绝对路径> write --out <输出.xlsx> --data rows.json
   ```
   脚本会追加写入（按文献名去重）、设置单元格自动换行、表头加粗、冻结首行。
6. 向用户报告新增条数与表格路径，并删除临时 `rows.json` 与 `_work\archiving_extract.json`。

## 列模板（每行的 JSON 键，从左到右）
- `文献名`：文件名（含或不含扩展名均可，去重以文件名为准）
- `发表年份`
- `期刊`
- `摘要`：研究背景（一句）／解决方案（一句）／创新点（一句）
- `研究内容`：研究问题（一句）／研究方法（关键词或短句）
- `主要结果`：分点短句，与数据分析方法一一对应，如「结果1：xxx，数据分析方法：xxx；结果2：…」
- `研究思路`：提出 xxx 问题，通过 xxx 实验/方法得到 xxx 结果，解决该问题（若未解决则写：引入 xxx 实验）

## 注意
- 自动跳过以 `~$` 开头的 Word 临时文件。
- 文件名支持中英文混合与较长名称，按原样保留。

## 大批量处理模式（文献数 > 20 篇时推荐，在 `/loop` 下运行）

当 `new_count` 较大时，建议改用下列批量并行流程以大幅提速：

1. **预提取文本**：写小脚本读 `_work/archiving_extract.json`，将每篇 `new[i].text` 分别写入 `_work/r/000.txt`、`001.txt`……（每篇一个文件，文件头加 `FILENAME: <原文件名>` 一行）。
2. **分批派发 agent**：每批约 12 篇，每个 agent 独立读取一个 txt 文件，按列模板生成对应的 `row` JSON 后返回。
3. **汇总写入**：将各 agent 的返回值合并写入 `_work/rows_bN.json`，再执行 `archiving.py write`。为避免 Windows shell 引号问题，推荐将汇总数据写成临时脚本 `_work/gen_bN.py`，由 Python 直接 `json.dump` 输出 json 文件。
4. **Auto-Continue 检查点**：每批派发前读取控制文件（`~/.claude/auto_continue/control.json`）：
   - `state == "RUN"` → 继续派发；
   - `state == "PAUSE"` → 保存当前批次索引到 `CLAUDE.md`，停止派发，等待下轮 `/loop` 自动恢复；
   - 文件缺失 / 解析失败 / 时间戳超过 40 分钟 → 视为 RUN。
5. **增量去重**：`archiving.py write` 按文献名自动去重，每批写入后可安全中断并重启，不会产生重复行。
