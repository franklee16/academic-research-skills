#!/usr/bin/env python3
"""
Universal Data Analyst - 使用示例

演示如何使用通用数据分析技能进行完整分析流程
"""

import sys
from pathlib import Path

# 添加 skill 路径
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import DataAnalysisOrchestrator


def example_single_run():
    """
    示例1: 单轮完整分析

    适用于用户信息充分的情况，一次性完成全部流程
    """
    print("="*80)
    print("示例1: 单轮完整分析")
    print("="*80)

    # 初始化编排器
    orchestrator = DataAnalysisOrchestrator(
        output_dir="./example_output"
    )

    # 运行完整分析
    results = orchestrator.run_full_analysis(
        file_path="/path/to/your/data.csv",
        user_intent="分析销售趋势和客户行为，识别高价值客户群体",
        run_validation=True  # 同时执行数据质量校验
    )

    print(f"\n分析完成！结果保存在: {results['session_dir']}")
    print("\n生成的提示词文件:")
    for step, info in results['steps'].items():
        if 'prompt_file' in info:
            print(f"  - {step}: {info['prompt_file']}")

    return results


def example_step_by_step():
    """
    示例2: 分步骤交互式分析

    适用于需要人工审核每步结果的情况
    """
    print("="*80)
    print("示例2: 分步骤交互式分析")
    print("="*80)

    orchestrator = DataAnalysisOrchestrator()

    # 步骤1: 加载数据
    success, msg = orchestrator.step1_load_data("data.csv")
    if not success:
        print(f"加载失败: {msg}")
        return

    # 步骤2: 生成本体识别提示词
    ontology_prompt, ontology_file = orchestrator.step2_identify_ontology()
    print(f"\n请将 {ontology_file} 中的提示词发送给大模型")
    print("获取JSON结果后，保存为 ontology_result.json")
    input("按回车继续...")

    # 步骤3: 数据校验（可选）
    orchestrator.step3_validate_data(run_validation=True)

    # 步骤4: 生成方案规划提示词
    planning_prompt, planning_file = orchestrator.step4_plan_analysis(
        user_intent="分析销售趋势"
    )
    print(f"\n请将 {planning_file} 中的提示词发送给大模型")
    print("获取JSON结果后，保存为 analysis_plan.json")
    input("按回车继续...")

    # 步骤5: 生成脚本
    script_prompt, script_file = orchestrator.step5_generate_script()
    print(f"\n请将 {script_file} 中的提示词发送给大模型")
    print("获取Python脚本后，保存为 analysis_script.py")
    input("按回车继续...")

    # 步骤6: 执行并生成报告
    orchestrator.step6_execute_and_report("analysis_script.py")

    print("\n分析流程完成！")


def example_different_data_types():
    """
    示例3: 不同类型数据的分析提示词
    """
    examples = {
        "零售交易数据": {
            "file": "sales_data.csv",
            "intent": "分析销售趋势、客户细分和产品组合优化",
            "expected_framework": "价值链分析 + ABC-XYZ + RFM"
        },
        "用户行为数据": {
            "file": "user_events.csv",
            "intent": "分析用户转化漏斗和推荐策略",
            "expected_framework": "漏斗分析 + 会话挖掘"
        },
        "股票价格数据": {
            "file": "stock_prices.csv",
            "intent": "分析价格趋势和风险特征",
            "expected_framework": "技术分析 + 波动率建模"
        },
        "科学实验数据": {
            "file": "experiment_results.csv",
            "intent": "验证假设和分析实验效应",
            "expected_framework": "假设检验 + 因果推断"
        }
    }

    print("="*80)
    print("示例3: 不同类型数据的分析")
    print("="*80)

    for data_type, config in examples.items():
        print(f"\n【{data_type}】")
        print(f"  文件: {config['file']}")
        print(f"  诉求: {config['intent']}")
        print(f"  预期框架: {config['expected_framework']}")


def main():
    """主入口"""
    print("Universal Data Analyst - 使用示例")
    print("="*80)

    # 显示可用示例
    print("\n可用示例:")
    print("  1. 单轮完整分析")
    print("  2. 分步骤交互式分析")
    print("  3. 不同类型数据示例")

    # 实际演示
    print("\n" + "="*80)
    print("运行示例3: 不同类型数据")
    print("="*80)
    example_different_data_types()

    print("\n" + "="*80)
    print("提示: 修改 example_usage.py 中的文件路径后，可以运行示例1和2")
    print("="*80)


if __name__ == "__main__":
    main()
