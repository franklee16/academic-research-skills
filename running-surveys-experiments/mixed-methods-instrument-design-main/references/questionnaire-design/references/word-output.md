# 问卷 Word 输出

## 目的与边界

Word 是问卷的审查、伦理附件、纸面实施、访员培训与版本归档载体。Web/移动端正式实施仍以平台无关编程规格和经过测试的平台实现为准；Word 预览不能证明跳题、校验、无障碍或移动端交互已经可用。

每次生成 DOCX 时完整执行文档 skill。使用 `assets/questionnaire-docx-template.js` 从已经通过结构校验的 `questionnaire-spec.json` 生成两种受控视图：

- **研究者设计版**：保留 RQ、构念、总体、题项来源、许可、编码、逻辑、计分、验证状态、测试和治理信息。
- **实施版**：只保留参与者或访员需要的研究说明、同意、说明、正式题面、响应控件、必要跳转和结束语；隐藏 RQ、构念、假设、计分方向、反向题标记、来源、内部质量规则和预期答案。

一份 `questionnaire-spec.json` 可以包含多个 `forms`。每个 form 明确绑定一个目标人群、语言和模式；生成器按 form 分别输出实施版，避免把不同受访者的题目混在同一份现场问卷中。

## 生成命令

先运行结构验证器：

```bash
python scripts/validate_questionnaire_spec.py path/to/questionnaire-spec.json
```

再使用文档 skill 提供的 Node.js 与 `docx` 依赖运行：

```bash
node assets/questionnaire-docx-template.js path/to/questionnaire-spec.json path/to/output-directory
```

若当前 Node 环境无法解析 `docx`，先调用文档 skill 的工作区依赖加载器，并把返回的 Node packages 目录加入 `NODE_PATH`。不要在 skill 目录中临时安装依赖或提交 `node_modules`。

默认文件名：

```text
01_问卷_研究者版_[问卷名称].docx
02_问卷_实施版_[form]_[人群]_[语言]_[模式].docx
```

由上位 `mixed-methods-instrument-design` 调用时，这两种视图只作为内部生成能力，不单独交付给用户；上位 skill 会把问卷实施内容和访谈提纲汇入一份完整 Word。只有用户明确要求“单独问卷”“研究者审查版”或“按人群分卷”时，才运行本节的多文件命令。

## Word 版式契约

- 明确设置 A4 页面与页边距，不依赖软件默认值。
- 正文使用规范中文字体，英文数字使用 Times New Roman；标题层级、页眉、页脚、版本和页码保持一致。
- 表格固定 DXA 宽度，同时设置表格列宽与单元格宽度；表头可重复，题目块不拆行。
- 题号保持稳定；同一题在 DOCX、JSON、XLSX 和平台实现中使用同一个 `item_id`。
- `required=true` 表示必须提交一个响应，不等于强迫提供实质答案；参与者可以按伦理与题目设计选择 `missing_display` 中获准的“不愿回答”“不知道”或“不适用”。系统状态 `not_shown` 不得显示为现场选项。
- 题干与主要选项尽量不跨页；开放题提供真实书写空间，排序与定和题使用可填写表格。
- 纸面、电话、CAPI/CATI 或访员协助模式显示必要跳转提示；Web/移动端的机器逻辑不直接暴露给参与者。
- 实施版首页显示适用对象、语言、模式、版本、日期、预计时长和问卷编号。
- 草稿中的占位符、许可待核项、伦理待定项和未完成测试不得在正式生产版中保留。

## 学术和实施依据

版式只承担可读、可执行与可追溯功能，不能代替测量证据。设计研究者版字段时参考 Census 的 question template，将研究问题、question universe、题面、响应选项和测试反馈保留在同一证据记录中；设计实施版时结合 Census 的问卷测试和多模式设计要求，并参考 WHO 正式调查工具中问卷、访员材料、showcards 和 QxQ 指南分离的做法。原始链接见 `sources.md`。

## 生成后必检

1. 用文档 skill 的 DOCX 验证器检查 OOXML 结构。
2. 转成 PDF，再逐页渲染为图片检查标题、分页、表格、选项、跳题和页脚。
3. 用文本抽取检查实施版是否泄漏 RQ、构念、来源、计分或质量排除规则。
4. 检查研究者版是否完整保留题项来源、编码、缺失、逻辑、验证状态与变更记录。
5. 对每个 form 核对人群、语言、模式与题目 universe；不得把“成功生成文件”写成“问卷已预测试或验证”。
