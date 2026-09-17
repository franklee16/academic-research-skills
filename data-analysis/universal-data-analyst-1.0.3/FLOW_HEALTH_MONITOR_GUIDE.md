# Flow Health Monitor 流程健康监控指南

## 问题背景

在使用 Universal Data Analyst Skill 时，可能会遇到以下问题：
- 某个步骤失败了，但用户没有及时察觉
- 后续步骤继续执行，但结果不完整或有误
- 没有清晰的错误提示和修复建议
- 不知道流程执行到了哪一步

## 解决方案：Flow Health Monitor

新增 `flow_health_monitor.py` 和 `orchestrator_v2.py`，提供：

1. **步骤状态追踪** - 每个步骤都有明确的执行状态
2. **依赖检查** - 前置步骤失败时阻止后续步骤执行
3. **清晰报错** - 步骤失败时给出明确的错误信息和修复建议
4. **健康报告** - 最终输出完整的流程执行状态

## 使用方法

### 1. 使用增强版 Orchestrator

```python
from orchestrator_v2 import DataAnalysisOrchestratorV2

# 创建实例
orch = DataAnalysisOrchestratorV2(output_dir="./output")

# 运行完整分析
results = orch.run_full_analysis(
    file_path="data.csv",
    user_intent="分析用户行为模式"
)
```

### 2. 查看流程状态

执行过程中会实时显示：

```
================================================================================
📊 流程健康监控报告
================================================================================

执行摘要:
  总步骤: 7
  成功: 3 ✅
  失败: 1 ❌
  被阻塞: 2 ⛔
  健康分数: 70/100

⚠️  流程已中断!
   原因: 关键步骤 '数据加载' 失败: 编码错误

步骤详情:

  ✅ 步骤1: 数据加载
     重要性: 🔴 关键
     状态: 失败
     错误: utf-8 codec can't decode byte...
     建议:
       1. 文件编码可能不是UTF-8，尝试手动指定encoding参数
       2. 常见中文编码: gbk, gb2312, gb18030
       3. 可使用文本编辑器查看或转换文件编码

  ⛔ 步骤2: 数据本体识别
     重要性: 🟡 必需
     状态: 被阻塞
     信息: 前置步骤 'load' 执行失败
     建议:
       1. 请检查步骤 'load' 的错误信息并修复问题
       2. 修复后重新运行完整流程

...
```

### 3. 查看健康报告

流程结束后会生成 `FLOW_HEALTH_REPORT.json`：

```json
{
  "health_score": 70,
  "flow_completed": false,
  "flow_interrupted": true,
  "interrupt_reason": "关键步骤 '数据加载' 失败...",
  "steps_summary": {
    "load": {
      "name": "数据加载",
      "status": "失败",
      "error": "编码错误",
      "suggestions": ["建议1", "建议2"]
    },
    "ontology": {
      "name": "数据本体识别",
      "status": "被阻塞",
      "message": "前置步骤 'load' 执行失败"
    }
  }
}
```

## 步骤重要性分级

| 级别 | 标识 | 说明 | 失败后果 |
|-----|------|------|---------|
| CRITICAL 🔴 | 关键 | 步骤失败则整个流程终止 | 流程立即中断，健康分-50 |
| REQUIRED 🟡 | 必需 | 步骤失败会阻塞后续步骤 | 后续依赖步骤被阻塞，健康分-30 |
| OPTIONAL ⚪ | 可选 | 步骤失败不影响后续步骤 | 流程继续，健康分-10 |

## 步骤依赖关系

```
load (关键)
  ├── ontology (必需) ──► planning (必需)
  │                         │
  └── validation (必需) ────┤
                            ▼
                    script_generation (必需) ──► execution (必需) ──► report (可选)
```

## 错误提示示例

### 数据加载失败

```
❌ 加载失败: ['utf-8 codec can\'t decode byte 0xb8 in position 1382...']

修复建议:
  1. 文件编码可能不是UTF-8，尝试手动指定encoding参数
  2. 常见中文编码: gbk, gb2312, gb18030
  3. 可使用文本编辑器查看或转换文件编码
```

### 前置步骤失败导致被阻塞

```
⛔ 步骤被阻塞: 前置步骤 'load' 执行失败

建议:
  1. 请检查步骤 'load' 的错误信息并修复问题
  2. 修复后重新运行完整流程
```

### 需要手动调用LLM的提醒

```
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
【重要提醒】
⚠️  本体识别需要调用大模型完成！
⚠️  提示词已保存到: session_xxx/step2_ontology_prompt.txt
⚠️  请使用此提示词调用 Claude 或其他LLM，
⚠️  然后将结果保存为: ontology_result.json
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
```

## 与原版对比

| 功能 | 原版 orchestrator.py | 增强版 orchestrator_v2.py |
|-----|---------------------|-------------------------|
| 步骤状态追踪 | ❌ 无 | ✅ 有 |
| 依赖检查 | ❌ 弱 | ✅ 强 |
| 流程中断检测 | ❌ 不完善 | ✅ 完善 |
| 错误提示 | ⚠️ 简单 | ✅ 详细+建议 |
| 健康报告 | ❌ 无 | ✅ JSON报告 |
| 最终状态汇总 | ⚠️ 简单打印 | ✅ 可视化状态表 |

## 迁移指南

从原版迁移到增强版非常简单：

```python
# 原版
from orchestrator import DataAnalysisOrchestrator
orch = DataAnalysisOrchestrator()

# 增强版
from orchestrator_v2 import DataAnalysisOrchestratorV2
orch = DataAnalysisOrchestratorV2()
```

API 完全兼容，只需修改导入语句即可。

## 测试

运行测试查看健康监控效果：

```bash
# 测试正常文件
python3 orchestrator_v2.py data.csv --intent "探索性分析"

# 测试有问题的文件（如编码错误）
python3 orchestrator_v2.py bad_encoding.csv --intent "测试错误处理"
```

## 文件列表

- `flow_health_monitor.py` - 流程健康监控核心模块
- `orchestrator_v2.py` - 增强版流程编排器
- `FLOW_HEALTH_MONITOR_GUIDE.md` - 本文档
