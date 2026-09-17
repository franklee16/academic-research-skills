#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试PPT Agent"""

import sys
import os

# Add parent of the package to path (src/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aut_sci_ppt import PPTAgent

# 测试输入
user_input = """
主题：研究生推免申请汇报
申请人：赵烁
导师：武海军教授
申请方向：高性能新型智能材料
时间：2025-9-15

1. 教育背景
- 2022.09-2026.07 重庆交通大学 材料科学与工程专业
- 绩点：3.61/4.0，专业排名18/145
- CET-4：已通过
- 主修课程：材料科学基础（86），材料工程基础（87），复合材料学（87），材料性能学（89）

2. 获奖经历
- 徕卡杯第十三届全国大学生金相技能大赛 国三 2024年07月
- 第六届重庆市大学生物理创新竞赛 市一 2023年12月
"""

# 生成PPT
agent = PPTAgent()
output_path = agent.generate(user_input, 'test_output.pptx')
print(f'PPT已生成: {output_path}')
