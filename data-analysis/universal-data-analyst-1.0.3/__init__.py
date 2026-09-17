"""
Universal Data Analyst - 通用数据分析专家

基于四层通用分析框架的数据分析技能：
1. 数据本体论（Data Ontology）- 不问"什么经济"，问"什么存在"
2. 问题类型学（Problem Typology）- 不问"怎么赚钱"，问"解决什么问题"
3. 方法论映射（Methodology Mapping）- 匹配领域公认方法
4. 验证与输出（Validation & Output）- 确保结论稳健

核心特点：
- 每次分析都调用大模型进行思考判断
- 不使用关键词硬编码
- 支持经济型和非经济型数据
- 支持单轮完整分析和多轮交互

主要组件：
- UniversalDataAnalyst: 基础数据操作
- LLMAnalyzer: 大模型分析封装
- DataAnalysisOrchestrator: 流程编排

使用方法：
    from universal_data_analyst import DataAnalysisOrchestrator

    orchestrator = DataAnalysisOrchestrator()
    results = orchestrator.run_full_analysis(
        file_path="data.csv",
        user_intent="分析销售趋势和客户行为"
    )
"""

__version__ = "1.0.0"
__author__ = "Claude"

from .main import UniversalDataAnalyst, DataOntology, AnalysisPlan
from .llm_analyzer import LLMAnalyzer, OntologyResult, AnalysisPlan as LLMAnalysisPlan
from .orchestrator import DataAnalysisOrchestrator

__all__ = [
    'UniversalDataAnalyst',
    'LLMAnalyzer',
    'DataAnalysisOrchestrator',
    'DataOntology',
    'AnalysisPlan',
    'OntologyResult',
]
