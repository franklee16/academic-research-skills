# Data Analysis Router

一个多领域 AI 数据分析 Codex Skill。

它不是直接套一个固定的数据分析模板，而是先识别数据所属的业务场景，再选择对应的分析框架、指标体系和报告结构。

## 这个 Skill 解决什么问题

很多数据分析任务真正难的不是算指标，而是先判断：

- 这份数据属于什么业务领域？
- 应该看哪些核心指标？
- 应该用哪套分析模型？
- 当前数据能不能支撑这些结论？
- 还缺哪些表或字段？

`data-analysis-router` 的设计目标是让 Codex 先像数据分析顾问一样判断场景，再开始分析。

## 工作流程

```text
用户上传数据或提出分析问题
        ↓
识别字段、表结构、文件名、sheet 名和用户意图
        ↓
判断业务领域
        ↓
读取对应领域分析框架
        ↓
输出结构化数据分析报告
```

## V1 支持的分析框架

- 电商分析
- 内容运营分析
- 广告投放分析
- 门店经营分析
- 财务经营分析
- 用户反馈分析
- 通用数据分析框架

## 能处理什么数据

- CSV 单文件
- Excel `.xlsx` 多 sheet 文件
- 多个 CSV / XLSX 文件
- 业务指标表
- 用户反馈、评论、客服记录等文本型数据

内置脚本 `scripts/profile_dataset.py` 可以对数据做初步体检，包括：

- 行列数
- 字段类型
- 缺失率
- 唯一值数量
- 样例值
- 表角色推断
- 多表候选关联键
- 可能业务领域

## 目录结构

```text
data-analysis-router/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── profile_dataset.py
└── references/
    ├── routing-rules.md
    ├── general-analysis.md
    ├── ecommerce.md
    ├── content-operation.md
    ├── advertising.md
    ├── store-operation.md
    ├── finance.md
    ├── user-feedback.md
    └── report-format.md
```

## 安装

将这个目录复制到 Codex 的 skills 目录：

```bash
cp -R data-analysis-router ~/.codex/skills/data-analysis-router
```

然后重启 Codex，让新 Skill 被自动发现。

## 使用方式

在 Codex 中显式调用：

```text
$data-analysis-router 帮我分析这个表格
```

也可以上传数据后直接提出业务问题，例如：

```text
$data-analysis-router 看看这份订单数据为什么退款率变高了
```

```text
$data-analysis-router 分析一下这些广告计划，哪些应该加预算，哪些应该暂停
```

```text
$data-analysis-router 帮我从这些用户评论里找出主要投诉原因
```

## 数据体检脚本

直接运行：

```bash
python3 scripts/profile_dataset.py path/to/file.csv path/to/workbook.xlsx
```

输出示例：

```text
# Dataset Profile

## File: ecommerce.xlsx

### Table: ecommerce.xlsx::orders
- Rows profiled: 12000
- Columns: 8
- Likely table role: orders

## Candidate Relationships
- sku_id: orders.sku_id, products.sku_id

## Likely Domains
- ecommerce: order, sku, payment, refund
```

脚本不依赖 pandas 或 openpyxl，使用 Python 标准库即可运行。

## 输出报告包含什么

默认报告结构包括：

- 领域判断
- 判断依据
- 数据概览
- 适用分析框架
- 核心指标
- 主要发现
- 可能原因
- 行动建议
- 图表建议
- 还需要补充的数据

## 设计理念

普通 AI 很容易变成“用户问什么，它答什么”。

这个 Skill 的核心是：

> 先判断业务场景，再选择分析框架。

这会让数据分析更接近真实顾问工作流，而不是泛泛地描述表格。

## License

MIT
