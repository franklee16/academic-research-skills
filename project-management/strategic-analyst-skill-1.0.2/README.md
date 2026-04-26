# Strategic Analyst - 战略分析专家

## 概述

麦肯锡风格的战略分析助手，帮助小企业CEO、大企业高管、高校学生和行业新进入者建立系统的行业认知，为关键决策提供数据支撑和分析框架。

## 目录结构

```
strategic-analyst/
├── skill.yaml                 # Skill 配置
├── agent_instructions.md      # 智能体人设 + 数据透明度 + 边界保持
├── README.md                  # 使用说明
├── frameworks/                # 6大分析框架
│   ├── industry_structure.md
│   ├── market_sizing.md
│   ├── competitive_landscape.md
│   ├── trend_analysis.md
│   ├── key_success_factors.md
│   └── value_chain.md
├── templates/                 # 报告模板
│   ├── executive_summary.md
│   ├── student_edition.md
│   ├── full_report.md         # 含数据溯源
│   └── data_provenance.md     # 数据溯源模板
├── data_sources/              # 数据源指南
│   ├── general.md
│   └── by_industry/
│       ├── consumer.md
│       ├── saas.md
│       ├── healthcare.md
│       ├── new_energy.md
│       └── ai.md
├── tools/                     # 工具脚本
│   ├── data_collector.py
│   ├── report_generator.py
│   └── quality_gate.py        # 质量门禁 ⭐
├── checklists/                # 检查清单
│   ├── pre_analysis.md
│   ├── data_collection.md
│   ├── quality_check.md
│   └── professional_boundaries.md  # 边界检查 ⭐
├── cases/                     # 分析案例
│   └── new_tea_drinks_analysis.md
└── docs/                      # 用户文档
    └── how_to_read_report.md  # 数据阅读指南
```

## 前置要求

本 skill 依赖 **Tavily** 进行深度研究级搜索。Tavily 通过 MCP 服务器在 `settings.json` 中配置。

- 你需要**自行申请 Tavily API Key**：访问 [https://tavily.com](https://tavily.com) 注册并获取 API Key。
- 将 API Key 填入 Claude Code 的 `settings.json` 中的 `tavily` MCP 服务器配置，示例如下：

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@0.1.4"],
      "env": {
        "TAVILY_API_KEY": "tvly-你的API密钥"
      }
    }
  }
}
```

- 若未配置 Tavily，系统会自动降级使用 WebSearch / web-search skill 等备用工具，但深度搜索能力将受限，可能影响复杂行业分析的数据完整度。

## 核心功能

### 1. 需求诊断
- 识别用户身份（CEO/高管/学生/新进入者）
- 了解核心决策问题
- 确定分析深度和侧重点
- **检查清单引导**：使用`checklists/pre_analysis.md`确保不遗漏关键问题

### 2. 框架化分析
- 行业结构分析（五力模型）
- 市场规模测算（TAM-SAM-SOM）
- 竞争格局研判
- 趋势分析（PESTEL）
- 价值链分析
- 关键成功因素识别
- **智能搜索增强**：自动搜索最新行业数据、主要玩家、投融资动态

### 3. 数据支持
- **数据源指南**：分行业数据源清单（`data_sources/`）
  - 通用数据源：政府统计、上市公司财报、券商研报
  - 行业特化：新茶饮、SaaS、医疗、新能源、AI等行业专属数据源
- **数据收集工具**：`tools/data_collector.py`系统化数据整理
- **可信度分级**：五星评级体系，确保数据质量

### 4. 报告生成
- **模板化输出**：3种报告模板适配不同用户
- **自动化生成**：`tools/report_generator.py`快速生成报告框架
- **质量检查**：`checklists/quality_check.md`确保报告完整性

### 5. 案例学习
- **完整案例**：新茶饮行业分析示例（`cases/`）
- **框架应用示范**：展示如何将理论框架应用于实际分析

### 6. 专业边界保持 ⭐
即使对话发散，确保报告专业性的机制：

**边界定义：**
- ✅ 行业分析、战略框架、数据方法
- ❌ 闲聊、技术实现、法律财务建议、非公开情报

**拉回机制：**
- 开场明确分析范围和边界
- 中场对齐检查（每10轮或明显发散时）
- 礼貌但坚定地拒绝超范围请求

**强制质量门禁：**
- 输出前自检清单（结构/框架/语言/数据/建议）
- 质量红线：结构不完整、语言口语化、无数据支撑 → 必须修正

**工具支持：**
- `checklists/professional_boundaries.md` - 边界检查清单
- `tools/quality_gate.py` - 自动质量门禁

## 使用场景

### 场景1：市场进入决策
> "我想进入新茶饮行业，帮我分析一下市场机会"

### 场景2：竞争策略制定
> "我们是SaaS公司，面临激烈竞争，该如何定位？"

### 场景3：投资决策支持
> "这个新能源项目值得投吗？帮我做个行业分析"

### 场景4：行业学习研究
> "我想系统学习新能源汽车行业，带带我"

## 触发方式

以下关键词或意图将激活本skill：
- "战略分析"
- "行业分析"
- "市场研究"
- "竞争分析"
- "麦肯锡"
- "分析XX行业"
- "了解XX市场"
- "进入XX行业"

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1.需求访谈  │ → │ 2.框架选择  │ → │ 3.数据采集  │
│  (5-10分钟)  │    │  (自动推荐)  │    │  (多渠道)   │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             ↓
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 5.迭代优化  │ ← │ 4.报告生成  │ ← │ 深度分析    │
│ (可选)       │    │ (结构化输出)│    │ (AI+数据)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 分析框架详解

### 波特五力模型
评估行业竞争强度和盈利能力：
- 现有竞争者竞争强度
- 新进入者威胁
- 替代品威胁
- 买方议价能力
- 供应商议价能力

### TAM-SAM-SOM
三层市场规模测算：
- **TAM**：总潜在市场（理论上最大）
- **SAM**：可服务市场（商业模式可触达）
- **SOM**：可获得市场（短期内实际可获取）

### PESTEL趋势分析
宏观环境扫描：
- Political（政治/政策）
- Economic（经济）
- Social（社会）
- Technological（技术）
- Environmental（环境）
- Legal（法律）

### 竞争格局分析
- 市场集中度（CR4/HHI）
- 战略群组划分
- 主要竞争者画像
- 竞争态势演变

### 关键成功因素（CSF）
- 识别行业关键能力要求
- 竞争者能力对比
- 差距分析与建设建议

### 价值链分析
- 价值创造各环节分析
- 利润池分布
- 价值链整合策略

## 报告模板

### 执行摘要版
- 核心结论（3-5条）
- 关键数据一览
- 机会与风险
- 建议行动清单

### 学生学习版
- 详细方法论讲解
- 理论+案例结合
- 学习检查清单
- 延伸阅读推荐

### 完整版
- 8大章节全面分析
- 详细数据支撑
- 战略建议与行动计划
- 附录（数据源、方法论）

## 工具使用

### 数据收集工具
```bash
# 生成搜索计划
python tools/data_collector.py "新能源汽车"

# 在Python中使用
from tools.data_collector import create_collector, generate_search_plan

collector = create_collector("新茶饮")
collector.add_market_size("¥3300亿", "中国连锁经营协会", "2023-12", 4)
collector.add_player("喜茶", "高端新茶饮品牌，3200家门店", "公司公告", "2024-01", 5)
print(collector.generate_summary_table())
```

### 报告生成工具
```bash
# 快速生成报告模板（仅Markdown）
python tools/report_generator.py "新能源汽车" report.md

# 生成双格式报告（Markdown + HTML）
python tools/report_generator.py "新能源汽车" report.md report.html

# 转换已有Markdown报告为HTML
python tools/report_generator.py convert report.md report.html

# 在Python中使用
from tools.report_generator import quick_generate, convert_report

# 双格式输出
result = quick_generate("新能源汽车", "output.md", "output.html")
# 返回: {'markdown': 'output.md', 'html': 'output.html'}

# 转换已有报告
html_path = convert_report("report.md", "report.html")
```

**HTML报告特性：**
- 专业商务风格（深蓝主色调）
- 自动转换Markdown表格为HTML表格
- 支持可信度星级颜色标注（★★★★★）
- 支持优先级徽章（P1/P2/P3）
- 支持趋势箭头样式（↑→↓）
- 响应式设计，支持打印

## 数据来源

### 通用数据源
- **政府统计**：国家统计局、各省统计局、行业主管部门
- **上市公司**：巨潮资讯、港交所披露易、SEC EDGAR
- **券商研报**：东方财富、萝卜投研
- **咨询机构**：麦肯锡、BCG、艾瑞、易观、亿欧智库

### 行业特化数据源
| 行业 | 主要数据源 |
|-----|-----------|
| 新茶饮/餐饮 | 窄门餐眼、美团研究院、红餐网 |
| SaaS | 崔牛会、IT桔子、G2、36氪企服点评 |
| 医疗健康 | NMPA、动脉网、药智网、Insight |
| 新能源 | 乘联会、中汽协、高工锂电 |
| AI | 机器之心、量子位、中国信通院 |

完整数据源清单见 `data_sources/` 目录。

## 使用流程示例

### 完整分析流程
```
1. 需求访谈
   └── 使用 checklists/pre_analysis.md

2. 数据收集
   ├── 查阅 data_sources/by_industry/[行业].md
   ├── 执行搜索关键词
   └── 使用 tools/data_collector.py 整理数据

3. 框架分析
   ├── 应用 frameworks/ 中的分析框架
   └── 填写各框架分析模板

4. 报告生成
   ├── 使用 templates/full_report.md 作为基础
   ├── 或使用 tools/report_generator.py 生成框架
   └── 填充分析内容

5. 质量检查
   └── 对照 checklists/quality_check.md

6. 交付与迭代
   └── 根据反馈调整
```

## 限制说明

1. **数据局限**：基于公开数据，可能存在时效性和完整性局限
2. **分析深度**：受信息获取限制，部分分析基于合理推断
3. **专业建议**：本分析仅供参考，重大决策请咨询专业顾问
4. **动态变化**：行业环境快速变化，建议定期更新分析

## 数据透明度机制

### 三类数据明确区分

| 数据类型 | 标识方式 | 可靠性 |
|---------|---------|-------|
| **直接引用数据** | 来源+发布时间+可信度星级 | ★★★★★ |
| **推算/估算数据** | 明确标注"估算"+计算公式+置信区间 | ★★★☆☆ |
| **行业共识数据** | 标注"经验值"+影响因素说明 | ★★☆☆☆ |

### 多模态数据获取 ⭐

**自动提取能力**：
- **PDF报告** → 通过`summarize`工具提取表格和关键数字
- **动态网页** → 通过`agent-browser`抓取结构化数据
- **图片/图表** → 通过`summarize`工具OCR识别数字和标签

**提取方式标注**：
```
| 数据项 | 数值 | 来源 | 可信度 | 提取方式 |
|-------|------|-----|-------|---------|
| 市场规模 | ¥500亿 | 艾瑞报告 | ★★★☆☆ | PDF提取 |
| 用户规模 | 3.2亿 | 网页截图 | ★★★☆☆ | OCR识别 |
```

**可信度调整规则**：
- PDF提取：原星级 - 0.5（OCR可能有误差）
- 网页抓取：保持原星级
- OCR识别：原星级 - 1（需人工复核）

### 可信度星级标准
```
★★★★★ = 政府统计/上市公司财报（可直接引用）
★★★★☆ = 头部券商/知名咨询机构（可信，注意偏差）
★★★☆☆ = 行业媒体/第三方平台（参考，需验证）
★★☆☆☆ = 自媒体/估算（仅作参考，谨慎使用）
```

### 每份报告必含
- **数据溯源章节**：全部数据来源、时效、可信度一览
- **推算逻辑说明**：所有估算数据的计算过程
- **时效性分布**：2024/2023/更早数据的占比和可靠性
- **数据缺口说明**：坦诚告知未能获取的关键数据

### 用户如何验证
- 查看`数据溯源与可信度说明`章节
- 对比报告中的数据来源和你的独立搜索
- 关注执行摘要中的⚠️数据时效性提示
- 参考`docs/how_to_read_report.md`数据阅读指南

## 更新日志

### v0.3.0 (2026-03-29)
- **HTML 表格下载**：报告生成器中每个 HTML 表格支持右上角悬停下载 PNG/SVG（零依赖纯 JS 实现）
- **强制中间产物**：`data_collection.md` 成为强制保存项，记录所有搜索关键词、工具、来源 URL 和原始摘要
- **来源链接规范化**：TAM-SAM-SOM、增长预测、关键数据表必须包含 `[来源](URL)` Markdown 链接，HTML 中可点击跳转
- **Tavily API Key 前置提醒**：`README.md` 和 `agent_instructions.md` 均明确要求用户自行配置 Tavily API Key，并给出 `settings.json` 示例

### v0.2.0 (2026-03-29)
- **搜索增强**：agent_instructions 增加实时搜索指引
- **数据源清单**：新增5个行业数据源指南
- **工具脚本**：新增 data_collector.py 和 report_generator.py
- **检查清单**：新增需求访谈、数据收集、质量检查3套清单
- **分析案例**：新增新茶饮行业完整分析案例
- **多模态数据获取** ⭐ 核心新增
  - 配置 `skill.yaml` 声明依赖（web-search/agent-browser/summarize）
  - PDF报告自动提取（summarize工具）
  - 动态网页数据抓取（agent-browser工具）
  - 图片/图表OCR识别（summarize工具）
  - 提取方式标注规范（PDF提取/网页抓取/OCR识别/直接引用）
  - 可信度自动调整规则
- **数据透明度机制**
  - agent_instructions 强制数据透明度规则
  - 三类数据明确区分（直接引用/推算/经验）
  - 标准可信度星级（★★★★★至★☆☆☆☆）
  - 数据溯源章节模板
  - 用户数据阅读指南
- **专业边界保持机制** ⭐ 核心新增
  - agent_instructions 增加边界定义和拉回话术
  - checklists/professional_boundaries.md 边界检查清单
  - tools/quality_gate.py 自动质量门禁
  - 输出前强制6项质量检查
- **报告标准化机制** ⭐ 核心新增
  - `templates/standard_report_structure.md` 标准章节顺序模板
  - `docs/visualization_standards.md` 10种标准表格格式
  - 质量门禁新增3项结构一致性检查：
    - `check_section_order()` - 验证章节顺序符合标准
    - `check_table_consistency()` - 验证表格格式统一
    - `check_rating_consistency()` - 验证评级符号（★/P1/P2/P3）使用

### v0.1.0 (2026-03-29)
- 初始版本发布
- 6大分析框架（五力、TAM-SAM-SOM、竞争格局、PESTEL、CSF、价值链）
- 3种报告模板（执行摘要、学生版、完整版）
- 4类用户适配（CEO/高管/学生/新进入者）

## 作者

Claude Code

---

*本skill旨在提供专业、系统、实用的战略分析服务，帮助用户在复杂商业环境中做出更明智的决策。*
