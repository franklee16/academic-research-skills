#!/usr/bin/env python3
"""
LLM Analyzer - 调用大模型进行思考判断的核心模块

该模块负责：
1. 数据本体识别（调用LLM思考）
2. 分析方案规划（调用LLM思考）
3. 分析脚本生成（调用LLM思考）
4. 分析报告生成（调用LLM思考）

特点：每次判断都调用大模型，不使用硬编码关键词匹配
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class OntologyResult:
    """数据本体识别结果"""
    entity_type: str  # 交易/事件型、状态/存量型、关系/网络型、特征/属性型、时序/轨迹型
    entity_type_reason: str  # 判断依据
    generation_mechanism: str  # 观测/实验/模拟/测量/报告
    mechanism_reason: str  # 判断依据
    core_dimensions: List[Dict[str, str]]  # 核心维度及说明
    is_economic: bool
    economic_type: Optional[str]  # 如果是经济数据，具体类型
    domain_type: str  # 领域类型（如劳动力市场、地球科学等）
    keywords: List[str]  # 3-5个关键词标签
    recommended_questions: List[str]  # 适合回答的问题类型
    limitations: List[str]  # 数据局限性
    confidence: str  # 高/中/低


@dataclass
class AnalysisPlan:
    """分析方案"""
    question_type: str  # 描述/诊断/预测/规范/因果
    question_type_reason: str  # 判断依据
    frameworks: List[Dict[str, str]]  # 推荐框架及理由
    analysis_steps: List[Dict[str, Any]]  # 分析步骤详情
    scripts: List[Dict[str, str]]  # 脚本清单
    expected_outputs: List[str]  # 预期输出
    prerequisites: List[str]  # 前置条件/数据要求
    risks: List[str]  # 潜在风险


class LLMAnalyzer:
    """LLM分析器 - 封装所有需要大模型思考的调用"""

    def __init__(self):
        self.conversation_history = []

    def identify_ontology(self, data_profile: Dict[str, Any]) -> OntologyResult:
        """
        步骤1: 数据本体识别

        调用大模型思考判断：
        - 这是什么类型的数据（实体类型）
        - 数据如何生成的（生成机制）
        - 有什么核心维度
        - 是否经济型数据，什么类型
        """

        prompt = f"""你是一位数据本体论专家。请深入分析这份数据的本质特征。

## 数据概况
- 数据形状: {data_profile['shape'][0]:,} 行 × {data_profile['shape'][1]} 列
- 内存占用: {data_profile['memory_mb']:.2f} MB

## 字段详情
"""
        for col in data_profile['columns'][:15]:  # 前15个字段
            prompt += f"\n- **{col['name']}** ({col['type']}, {col['dtype']})"
            prompt += f"\n  - 唯一值: {col['unique_count']:,}, 缺失率: {col['null_pct']:.1f}%"
            if col.get('min') is not None:
                prompt += f"\n  - 范围: [{col['min']:.2f}, {col['max']:.2f}], 均值: {col['mean']:.2f}" if col['mean'] else ""
            if col.get('sample_values'):
                prompt += f"\n  - 示例值: {col['sample_values'][:3]}"

        if data_profile.get('potential_time_cols'):
            prompt += f"\n\n## 潜在时间列\n{data_profile['potential_time_cols']}"
        if data_profile.get('potential_price_cols'):
            prompt += f"\n\n## 潜在价格/货币列\n{data_profile['potential_price_cols']}"
        if data_profile.get('potential_id_cols'):
            prompt += f"\n\n## 潜在ID/实体列\n{data_profile['potential_id_cols']}"

        prompt += """

---

## 请深入思考并回答以下问题：

### 1. 实体类型识别
这份数据记录的是什么类型的存在？从以下选择并说明依据：
- **交易/事件型**: 离散发生、有时间戳、不可重复（如订单、点击、地震）
- **状态/存量型**: 时间点快照、可累积（如库存、人口、余额）
- **关系/网络型**: 实体间连接（如社交关系、贸易流、引用）
- **特征/属性型**: 描述静态属性（如用户画像、商品参数、地质特征）
- **时序/轨迹型**: 连续测量、有序列依赖（如股价、气温、传感器）

**你的判断**:
**判断依据**:

### 2. 数据生成机制
数据是如何产生的？这暗示了什么偏差？
- **观测型**: 被动记录，可能存在选择偏差、幸存者偏差
- **实验型**: 有干预/对照，可建立因果
- **模拟型**: 基于规则生成，结论仅限模拟场景
- **测量型**: 仪器采集，有测量误差
- **报告型**: 人工填报，有社会期望偏差

**你的判断**:
**判断依据**:

### 3. 核心维度识别
数据中有哪些可以用来分组、对比、追溯的关键维度？
- 时间维度？
- 地理/空间维度？
- 分类/层级维度？
- 实体/关系维度？

**列出核心维度及说明**:

### 4. 经济类型判定
这份数据是否涉及经济行为？
- 是否有价格、成本、收入、利润、交易等字段？
- 是否描述买卖双方或供需关系？

**如果是经济数据**，初步判断属于：
- 零售经济 / 订阅经济 / 租赁经济 / 注意力经济
- 佣金经济 / 劳动力市场经济 / 金融时序 / 其他

**如果不是经济数据**，属于什么领域：
- 地球科学 / 生物医学 / 社会科学 / 工程技术 / 其他

**你的判断**:
**判断依据**:

### 5. 关键词标签
给出3-5个关键词标签概括这份数据：

### 6. 适合回答的问题
基于数据特征，这份数据最适合回答什么类型的问题？（描述/诊断/预测/规范/因果）
具体可以回答哪些问题？

### 7. 数据局限性
从样本量、时间跨度、字段完整性、潜在偏差等角度，这份数据有什么明显的局限性？
不能回答什么问题？

### 8. 置信度评估
你对以上判断的置信度如何？（高/中/低）

---

请以结构化JSON格式输出：
{
  "entity_type": "",
  "entity_type_reason": "",
  "generation_mechanism": "",
  "mechanism_reason": "",
  "core_dimensions": [{"dimension": "", "description": ""}],
  "is_economic": true/false,
  "economic_type": "",
  "domain_type": "",
  "keywords": [],
  "recommended_questions": [],
  "limitations": [],
  "confidence": ""
}
"""

        # 实际使用时调用LLM
        # result = call_llm(prompt)
        # return parse_ontology_result(result)

        return prompt  # 返回提示词供上层调用

    def plan_analysis(self, ontology: OntologyResult, user_intent: str,
                     data_sample: str, column_details: List[str]) -> AnalysisPlan:
        """
        步骤2: 分析方案规划

        调用大模型思考判断：
        - 用户想回答什么问题类型
        - 该领域公认的分析方法是什么
        - 具体分步骤的分析路径
        """

        prompt = f"""你是一位跨领域数据分析专家。请基于数据本体和用户诉求，规划完整的分析方案。

---

## 第一部分：数据本体（已识别）

**实体类型**: {ontology.entity_type}
**判断依据**: {ontology.entity_type_reason}

**数据生成机制**: {ontology.generation_mechanism}
**判断依据**: {ontology.mechanism_reason}

**核心维度**:
"""
        for dim in ontology.core_dimensions:
            prompt += f"\n- {dim['dimension']}: {dim['description']}"

        prompt += f"""

**经济类型判定**: {"是 - " + ontology.economic_type if ontology.is_economic else "否 - " + ontology.domain_type}

**关键词**: {', '.join(ontology.keywords)}

**数据局限性**:
"""
        for lim in ontology.limitations:
            prompt += f"\n- {lim}"

        prompt += f"""

---

## 第二部分：用户诉求

**用户原话**: "{user_intent}"

请解析：
1. 用户想解决什么实际问题？
2. 用户的角色是什么？（业务决策者/研究人员/学生/其他）
3. 预期产出是什么？（洞察报告/预测模型/可视化/其他）

---

## 第三部分：数据样本（前10行）

```
{data_sample}
```

---

## 第四部分：字段详情

"""
        for detail in column_details[:20]:
            prompt += f"\n- {detail}"

        prompt += """

---

## 请深入思考并输出分析方案：

### 第一步：问题类型判定

用户的问题属于什么类型？从以下选择并详细说明判断依据：

**描述型（是什么）**
- 关键词：现状、分布、特征、趋势、统计
- 示例：平均薪资是多少？各地区销量如何分布？
- 数据要求：有代表性的样本即可

**诊断型（为什么）**
- 关键词：原因、为什么、归因、差异、解释
- 示例：为什么转化率下降？为什么A地区比B地区好？
- 数据要求：多维度分解的可能、时间序列或分组对比

**预测型（会怎样）**
- 关键词：预测、趋势、未来、预警、容量
- 示例：下季度销量会如何？什么时候需要扩容？
- 数据要求：时间序列数据或特征-目标关系明确

**规范型（应怎样）**
- 关键词：最优、应该、策略、资源配置、建议
- 示例：最优定价策略是什么？资源如何分配？
- 数据要求：行动-结果映射清晰、有约束条件

**因果型（有效应吗）**
- 关键词：因果、影响、效果、机制、验证
- 示例：促销活动是否提升了销售？新药是否有效？
- 数据要求：有时间变化或对照组、可排除混淆因素

**你的判定**:
**判断依据**（引用用户问题中的关键词）:
**数据支持程度**（高/中/低）:

---

### 第二步：领域分析方法匹配

基于数据类型和问题类型，该领域公认的分析方法是什么？

如果涉及**经济数据**，选择相应框架：
- **零售经济** → 价值链分析、ABC-XYZ产品组合、RFM客户分层
- **订阅经济** → LTV/Cohort分析、留存曲线、收入瀑布
- **注意力/转化经济** → 漏斗分析、AARRR、会话序列挖掘
- **佣金/平台经济** → 双边网络效应、单位经济模型、匹配效率
- **租赁/资产经济** → 资产利用率、收益管理、资产生命周期
- **劳动力市场** → 技能溢价分析、经验弹性、供需缺口
- **金融时序** → 技术分析、波动率建模、组合优化

如果涉及**非经济数据**，选择相应框架：
- **科学测量** → 不确定性分析、假设检验、实验设计
- **社会网络** → 中心性分析、社区发现、传播模型
- **时空地理** → 空间自相关、热点分析、地理加权回归
- **文本/NLP** → 主题模型、情感分析、语义网络
- **生物医学** → 生存分析、差异表达、通路富集

**推荐框架**（1-3个，按优先级排序）:
- 框架1: 名称 + 适用理由 + 具体应用场景
- 框架2: 名称 + 适用理由 + 具体应用场景
- 框架3: 名称 + 适用理由 + 具体应用场景（如需要）

**为什么不推荐其他框架**:

---

### 第三步：分析路径设计

设计具体的分析步骤，每一步都要有明确的：
- 步骤名称
- 目的（要解决什么子问题）
- 方法（具体技术/算法）
- 输入（需要什么数据字段）
- 输出（产生什么结果/图表/数值）
- 代码逻辑（伪代码或关键操作）

**起手式分析**（所有数据都做的基础分析）:
步骤1:
步骤2:
步骤3:

**核心分析**（针对用户问题的深度分析）:
步骤4:
步骤5:
步骤6:

**验证分析**（稳健性检查）:
步骤7:
步骤8:

**可视化方案**:
- 图表1: 类型 + 目的 + 关键发现
- 图表2: 类型 + 目的 + 关键发现

---

### 第四步：脚本规划

规划需要生成的Python分析脚本：

**脚本文件1: xxx.py**
- 功能:
- 依赖:
- 输入:
- 输出:
- 关键函数:

**脚本文件2: xxx.py**（如需要）
...

**脚本之间的依赖关系**:

---

### 第五步：预期输出与交付

**用户将看到什么**:
- 数字结论（具体指标）:
- 可视化图表（类型和洞察）:
- 文字报告（结构和重点）:

**前置条件/数据要求**:
- 必须满足什么条件才能执行？
- 如果条件不满足，有什么替代方案？

**潜在风险/注意事项**:
- 什么情况下结论可能不可靠？
- 用户使用时需要注意什么？

---

请以结构化JSON格式输出：
{
  "question_type": "",
  "question_type_reason": "",
  "frameworks": [{"name": "", "reason": "", "application": ""}],
  "analysis_steps": [
    {
      "step_number": 1,
      "name": "",
      "purpose": "",
      "method": "",
      "input_fields": [],
      "output": "",
      "code_logic": ""
    }
  ],
  "scripts": [{"filename": "", "function": "", "dependencies": []}],
  "expected_outputs": [],
  "prerequisites": [],
  "risks": []
}
"""

        return prompt

    def generate_script(self, analysis_plan: AnalysisPlan, ontology: OntologyResult,
                       file_path: str) -> str:
        """
        步骤3: 生成分析脚本
        """

        steps_description = "\n\n".join([
            f"步骤{s['step_number']}: {s['name']}\n"
            f"目的: {s['purpose']}\n"
            f"方法: {s['method']}\n"
            f"输入字段: {', '.join(s['input_fields'])}\n"
            f"输出: {s['output']}\n"
            f"代码逻辑: {s['code_logic']}"
            for s in analysis_plan.analysis_steps
        ])

        prompt = f"""你是一位Python数据分析专家。请生成完整可执行的分析脚本。

## 分析方案

**问题类型**: {analysis_plan.question_type}

**推荐框架**:
"""
        for fw in analysis_plan.frameworks:
            prompt += f"\n- {fw['name']}: {fw['reason']}"

        prompt += f"""

## 分析步骤

{steps_description}

## 数据信息

**文件路径**: {file_path}

**数据本体**:
- 实体类型: {ontology.entity_type}
- 经济类型: {ontology.economic_type if ontology.is_economic else ontology.domain_type}

---

## 生成要求

请生成一个完整的Python脚本，要求：

1. **标准依赖**
   ```python
   import sys
   from pathlib import Path
   SKILL_DIR = Path(__file__).parent
   sys.path.insert(0, str(SKILL_DIR / 'layers'))
   from data_loader import DataLoader
   from data_validator import DataValidator

   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import seaborn as sns
   ```

2. **错误处理**
   - 所有文件操作和计算都要有try-except
   - 检查空值和异常值
   - 提供友好的错误信息

3. **模块化设计**
   - 每个分析步骤一个函数
   - 函数有清晰的docstring
   - 主函数 orchestrate 全流程

4. **结果保存**
   - 图表保存到 ./output/ 目录
   - 数值结果保存到JSON
   - 生成Markdown报告

5. **注释完整**
   - 每个关键步骤说明目的
   - 复杂逻辑要有解释
   - 引用分析框架的出处

---

请直接输出完整的Python脚本代码，使用以下结构：

```python
#!/usr/bin/env python3
\"\"\"
分析脚本: [根据分析目的命名]
数据文件: {file_path}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

分析框架: {', '.join([f['name'] for f in analysis_plan.frameworks])}
问题类型: {analysis_plan.question_type}

功能说明:
[详细说明脚本功能]
\"\"\"

# 导入和配置
...

# 全局配置
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 函数定义
...

# 主函数
if __name__ == "__main__":
    main()
```
"""

        return prompt

    def generate_report(self, ontology: OntologyResult, analysis_plan: AnalysisPlan,
                       results: Dict[str, Any]) -> str:
        """
        步骤4: 生成分析报告
        """

        prompt = f"""你是一位数据分析报告撰写专家。请基于分析结果生成专业的数据解读报告。

## 数据本体

**实体类型**: {ontology.entity_type}
**数据生成机制**: {ontology.generation_mechanism}
**经济/领域类型**: {ontology.economic_type if ontology.is_economic else ontology.domain_type}

**核心维度**:
"""
        for dim in ontology.core_dimensions:
            prompt += f"\n- {dim['dimension']}: {dim['description']}"

        prompt += f"""

**关键词**: {', '.join(ontology.keywords)}

**数据局限性**:
"""
        for lim in ontology.limitations:
            prompt += f"\n- {lim}"

        prompt += f"""

## 分析方案

**问题类型**: {analysis_plan.question_type}

**使用框架**:
"""
        for fw in analysis_plan.frameworks:
            prompt += f"\n- **{fw['name']}**: {fw['reason']}"

        prompt += f"""

## 分析结果（关键发现）

```json
{json.dumps(results, indent=2, ensure_ascii=False, default=str)[:2000]}
```

---

## 报告生成要求

请生成一份专业的Markdown格式分析报告，包含以下章节：

### 1. 执行摘要（Executive Summary）
- 3-5条核心发现，每条一句话
- 1条总体结论
- 关键数字（用粗体标注）

### 2. 数据画像（Data Profile）
- 数据来源和规模
- 实体类型说明
- 核心维度介绍
- 质量评估

### 3. 分析方法（Methodology）
- 为什么选这个分析框架？
- 具体使用了什么技术？
- 分析的局限性是什么？

### 4. 详细发现（Key Findings）
- 按主题组织，每个主题一个小节
- 每个发现都要有具体数字支撑
- 包含可视化图表的描述（图表已保存到output目录）
- 区分"数据显示"和"可能意味着"（前者是事实，后者是推测）

### 5. 结论与建议（Conclusions & Recommendations）
- 回答用户最初的问题
- 基于数据的具体建议
- 下一步行动（如果需要）

### 6. 数据局限与注意事项（Limitations）
- 数据不能回答什么问题？
- 使用结论时需要注意什么？
- 什么情况下结论可能不适用？

---

## 写作风格要求

1. **专业但易懂**：避免过度学术化，但保持专业性
2. **数字说话**：每个结论都要有具体数值支撑
3. **诚实边界**：明确区分"确定"和"推测"
4. **行动导向**：结论要能指导实际决策
5. **格式规范**：使用Markdown标题、列表、表格、代码块

请直接输出完整的Markdown报告。
"""

        return prompt


def main():
    """测试入口"""
    analyzer = LLMAnalyzer()

    # 示例数据画像
    sample_profile = {
        'shape': (10000, 10),
        'memory_mb': 2.5,
        'columns': [
            {'name': 'timestamp', 'type': 'datetime', 'dtype': 'datetime64[ns]',
             'unique_count': 10000, 'null_pct': 0, 'min': '2020-01-01', 'max': '2020-12-31'},
            {'name': 'user_id', 'type': 'categorical', 'dtype': 'int64',
             'unique_count': 5000, 'null_pct': 0, 'sample_values': [1, 2, 3]},
            {'name': 'product_id', 'type': 'categorical', 'dtype': 'int64',
             'unique_count': 100, 'null_pct': 0, 'sample_values': [101, 102, 103]},
            {'name': 'category', 'type': 'categorical', 'dtype': 'object',
             'unique_count': 10, 'null_pct': 0, 'sample_values': ['A', 'B', 'C']},
            {'name': 'price', 'type': 'numeric', 'dtype': 'float64',
             'unique_count': 500, 'null_pct': 0, 'min': 10.0, 'max': 1000.0, 'mean': 150.0},
            {'name': 'quantity', 'type': 'numeric', 'dtype': 'int64',
             'unique_count': 50, 'null_pct': 0, 'min': 1, 'max': 100, 'mean': 3.5},
            {'name': 'total_amount', 'type': 'numeric', 'dtype': 'float64',
             'unique_count': 2000, 'null_pct': 0, 'min': 10.0, 'max': 50000.0, 'mean': 500.0},
        ],
        'potential_time_cols': ['timestamp'],
        'potential_price_cols': ['price', 'total_amount'],
        'potential_id_cols': ['user_id', 'product_id']
    }

    ontology_prompt = analyzer.identify_ontology(sample_profile)
    print("=" * 80)
    print("数据本体识别提示词（前2000字符）:")
    print("=" * 80)
    print(ontology_prompt[:2000])


if __name__ == '__main__':
    main()
