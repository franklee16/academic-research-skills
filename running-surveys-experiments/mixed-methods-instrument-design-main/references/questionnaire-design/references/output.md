# 问卷交付、变量字典与版本控制

## 1. 默认交付包

### A. 研究者设计版

1. 边界、工具类型、研究目的与 RQ；
2. 目标总体、样本与分析单位；
3. 总调查误差风险图；
4. RQ—构念—变量—题项映射；
5. 逐题来源、许可、改编和证据状态；
6. 题序、模式、语言、敏感性与设计理由；
7. 预测试、验证、抽样、质量和伦理计划；
8. 尚未完成/待核事项。

### B. 实施版

只包含受访者实际看到或听到的内容：邀请/同意、筛选、说明、题面、选项、帮助、错误与结束页。不得展示 RQ、构念、假设、计分键、反向题标记、质量排除规则或研究者备注。

不同人群、语言和模式分别成版，首页标版本、适用对象和日期。

### C. 数据与编程版

提供数据字典、代码本、显示/跳题、随机化、校验、piping、派生、缺失、计分、测试用例、平台实现说明和导出检查。

## 2. 变量字典最低字段

| 字段 | 内容 |
|---|---|
| `item_id` / `variable_name` | 稳定题号与唯一机器名 |
| `version` / `language` / `mode` | 版本、语言、模式 |
| `rq_ids` / `construct_ids` | 研究问题与构念映射 |
| `population_ids` / `universe` | 适用人群和回答条件 |
| `question_text` / `instruction` | 现场题面与说明 |
| `response_type` / `values` | 类型、编码和值标签 |
| `recall_period` / `referent` | 回忆期与参照对象 |
| `display_logic` / `skip_logic` | 显示、跳转和回流 |
| `validation` / `error_message` | 范围、软硬校验与提示 |
| `randomization` / `piping` | 随机化和动态填充 |
| `source_status` / `citation` / `license` | 来源状态、出处和许可 |
| `scoring` / `derived_variable` | 计分与派生规则 |
| `missing_codes` / `missing_display` | 缺失编码，以及哪些“不知道/不适用/不愿回答”允许现场显示；`not_shown` 等系统状态不得展示 |
| `validation_status` | 已有证据、待认知测试、待 pilot、待正式验证 |
| `change_log` | 改动、理由、日期和负责人 |

## 3. 文件建议

```text
00_research-design-and-map.md
01_questionnaire-researcher-version.md
02_questionnaire-field-[population]-[language]-[mode].docx
03_variable-dictionary-and-codebook.xlsx
04_programming-and-routing-spec.md
05_pretest-and-validation-plan.md
06_source-license-and-adaptation-log.md
07_ethics-and-data-management.md
08_quality-and-reporting-plan.md
instrument-map.json
questionnaire-spec.json
```

## 4. 格式要求

- Markdown 用于设计逻辑与可审阅版本；DOCX 用于纸面/访员实施；XLSX 用于字典、路由、来源和测试用例。
- Word 版控制分页，题干与选项尽量不跨页；纸面跳题采用清晰箭头和目标题号。
- Excel 不合并数据单元格；一个字段一列、一个题项/选项/测试用例一行；设置数据验证但保留纯文本导出。
- Web 平台实施前先输出平台无关规格，避免逻辑被某个平台私有设置锁定。

单独交付问卷 DOCX 时完整执行 `references/word-output.md`。由上位混合工具 skill 调用时，只向单文件生成器提供通过校验的问卷规格，不另外向用户输出研究者版、实施版或 JSON。每个 form 仍须绑定一个目标人群、一个语言和一个模式。

## 5. 版本链

状态使用 `draft → cognitive-test → pilot → production → retired`。每次发布记录版本号、日期、语言、模式、题项差异、原因、批准/审查、适用数据批次和可比性影响。正式数据必须保留所用问卷版本的不可变副本。

## 6. 交付声明

明确哪些来源已核、哪些许可待确认、哪些题待认知测试、哪些量表待验证、哪些抽样/伦理决定由实施团队完成。不得把模板、计划或机器结构校验写成“问卷已验证”。
