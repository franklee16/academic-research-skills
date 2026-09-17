# Universal Data Analyst - 通用数据分析专家

基于四层通用分析框架的智能数据分析技能，每次分析都通过大模型思考判断，不使用硬编码规则。

## 核心设计理念

```
┌─────────────────────────────────────────────────────────────┐
│                     数据输入（任意类型）                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第一层：数据本体论（Data Ontology）                          │
│  —— 不问"这是什么经济"，问"这是关于什么的存在"                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第二层：问题类型学（Problem Typology）                       │
│  —— 不问"怎么赚钱"，问"要解决什么认知问题"                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第三层：方法论映射（Methodology Mapping）                    │
│  —— 匹配领域公认的分析方法                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第四层：验证与输出（Validation & Output）                    │
└─────────────────────────────────────────────────────────────┘
```

## 工作流程

### 六步分析流程

```
用户上传数据
    ↓
【步骤1】数据加载 (data_loader.py)
    ↓
【步骤2】本体识别 → 调用LLM思考（这是什么存在？）
    ↓
【步骤3】数据校验 (data_validator.py) [可选]
    ↓
【步骤4】方案规划 → 调用LLM思考（用什么方法分析？）
    ↓
【步骤5】脚本生成 → 调用LLM思考（写什么代码？）
    ↓
【步骤6】执行分析 → 调用LLM思考（报告怎么写？）
    ↓
输出分析报告
```

## 核心特点

| 特点 | 说明 |
|------|------|
| **无硬编码** | 不使用关键词匹配，每次判断都调用大模型 |
| **通用性强** | 支持经济型和非经济型数据 |
| **灵活适配** | 根据数据特征自动选择分析框架 |
| **单轮完成** | 用户信息充分时可一次完成分析 |
| **可解释性** | 每个判断都有明确依据说明 |

## 安装与配置

```bash
# 确保依赖已安装
pip install pandas numpy matplotlib seaborn scipy

# 添加到Python路径
export PYTHONPATH="/path/to/universal-data-analyst:$PYTHONPATH"
```

## 使用方法

### 命令行使用

```bash
# 基础用法
python orchestrator.py data.csv --intent "分析销售趋势"

# 完整参数
python orchestrator.py data.csv \
    --intent "分析客户细分和购买行为" \
    --validate \
    --output ./my_analysis
```

### Python API 使用

```python
from universal_data_analyst import DataAnalysisOrchestrator

# 初始化编排器
orchestrator = DataAnalysisOrchestrator(output_dir="./analysis_output")

# 运行完整分析
results = orchestrator.run_full_analysis(
    file_path="data.csv",
    user_intent="探索性数据分析，了解数据特征",
    run_validation=False
)

print(f"分析结果保存在: {results['session_dir']}")
```

### 分步骤使用

```python
from universal_data_analyst import DataAnalysisOrchestrator

orchestrator = DataAnalysisOrchestrator()

# 步骤1: 加载数据
orchestrator.step1_load_data("data.csv")

# 步骤2: 生成本体识别提示词
ontology_prompt, ontology_file = orchestrator.step2_identify_ontology()
# → 将 ontology_prompt 发送给大模型获取本体结果

# 步骤4: 生成方案规划提示词
planning_prompt, planning_file = orchestrator.step4_plan_analysis("分析销售趋势")
# → 将 planning_prompt 发送给大模型获取分析方案

# 步骤5: 生成脚本
script_prompt, script_file = orchestrator.step5_generate_script()
# → 将 script_prompt 发送给大模型获取分析脚本
```

## 提示词使用说明

本技能生成的是**高质量的LLM提示词**，需要配合大模型使用：

1. **步骤2生成的提示词** → 获取数据本体识别结果（JSON格式）
2. **步骤4生成的提示词** → 获取分析方案（JSON格式）
3. **步骤5生成的提示词** → 获取分析脚本（Python代码）
4. **步骤6生成的提示词** → 获取分析报告（Markdown格式）

### 示例：使用Claude API

```python
import anthropic

client = anthropic.Anthropic()

# 读取步骤2的提示词
with open("step2_ontology_prompt.txt") as f:
    ontology_prompt = f.read()

# 调用Claude进行本体识别
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    messages=[{"role": "user", "content": ontology_prompt}]
)

# 解析JSON结果
ontology_result = json.loads(response.content[0].text)
```

## 支持的文件格式

通过 `data_loader.py` 支持：
- CSV (.csv)
- Excel (.xlsx, .xls)
- Parquet (.parquet)
- JSON (.json)
- SQL 数据库（通过连接字符串）

## 输出文件说明

每个分析会话生成以下文件：

```
analysis_output/
└── session_YYYYMMDD_HHMMSS/
    ├── SESSION_SUMMARY.json          # 会话摘要
    ├── step1_data_info.json          # 数据基本信息
    ├── step2_ontology_prompt.txt     # 本体识别提示词
    ├── step3_validation_report.json  # 数据校验报告[可选]
    ├── step3_cleaning_report.txt     # 清洗建议报告[可选]
    ├── step4_planning_prompt.txt     # 方案规划提示词
    ├── step5_script_prompt.txt       # 脚本生成提示词
    ├── step6_report_prompt.txt       # 报告生成提示词
    └── output/                       # 分析结果输出目录
        ├── analysis_script.py
        ├── figures/
        └── report.md
```

## 经济类型识别速查

当数据被识别为经济类型时，自动匹配相应框架：

| 数据特征 | 经济类型 | 分析框架 |
|---------|---------|---------|
| 订单+价格+利润+SKU | 零售经济 | 价值链 + ABC-XYZ + RFM |
| 用户+订阅周期+Churn | 订阅经济 | LTV/Cohort + 留存曲线 |
| view/cart/buy事件链 | 注意力/转化经济 | 漏斗分析 + 会话挖掘 |
| GMV+平台撮合 | 佣金经济 | 双边网络效应 + 单位经济 |
| 资产+使用记录 | 租赁经济 | 资产利用率 + 收益管理 |
| OHLCV价格数据 | 金融时序 | 技术分析 + 波动率模型 |
| 职位+技能+薪资 | 劳动力市场 | 技能溢价 + 经验弹性 |

## 非经济数据支持

| 数据类型 | 领域 | 分析方法 |
|---------|------|---------|
| 传感器连续数据 | 地球科学 | 时间序列分解、极值分析 |
| 网络连接数据 | 社交网络 | 中心性、社区发现 |
| 文本语料 | NLP | 主题模型、情感分析 |
| 图像像素 | 计算机视觉 | 特征提取、分类聚类 |

## 架构说明

```
universal-data-analyst/
├── skill.yaml              # Skill定义和提示词模板
├── __init__.py             # 包入口
├── main.py                 # 基础数据操作（加载、校验）
├── llm_analyzer.py         # LLM提示词生成器
├── orchestrator.py         # 流程编排器（主入口）
├── layers/                 # 依赖层
│   ├── data_loader.py      # 多格式数据加载
│   └── data_validator.py   # 数据质量校验
└── README.md               # 本文件

## License

CC BY-NC-SA 4.0
