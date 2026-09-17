# AI PPT 生成 Agent - 使用指南

## 目录

1. [快速开始](#1-快速开始)
2. [安装依赖](#2-安装依赖)
3. [基本用法](#3-基本用法)
4. [输入格式](#4-输入格式)
5. [配置选项](#5-配置选项)
6. [高级功能](#6-高级功能)
7. [模板系统](#7-模板系统)
8. [API 参考](#8-api-参考)
9. [常见问题](#9-常见问题)

---

## 1. 快速开始

### 1.1 最短代码示例

```python
from aut_sci_ppt import PPTAgent

agent = PPTAgent()

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

2. 获奖经历
- "徕卡杯"第十三届全国大学生金相技能大赛 国三 2024年
- 第六届重庆市大学生物理创新竞赛 市一 2023年
"""

output_path = agent.generate(user_input, "我的简历.pptx")
print(f"PPT已生成: {output_path}")
```

### 1.2 运行测试

```bash
cd aut_sci_ppt
python test.py
```

---

## 2. 安装依赖

### 2.1 Python 版本要求

- Python 3.8+

### 2.2 安装必要的库

```bash
pip install python-pptx pyyaml
```

---

## 3. 基本用法

### 3.1 使用文本输入

```python
from aut_sci_ppt import PPTAgent

agent = PPTAgent()

# 方式1：直接使用文本
user_input = """
主题：汇报标题
申请人：姓名
导师：导师姓名

1. 章节一
- 内容1
- 内容2
"""

agent.generate(user_input, "output.pptx")
```

### 3.2 使用便捷函数

```python
from aut_sci_ppt import create_ppt

# 一行代码生成PPT
create_ppt("""
主题：标题
申请人：姓名

1. 内容
- 事项1
""", "output.pptx")
```

### 3.3 预览模式

在生成文件之前预览页面结构：

```python
agent = PPTAgent()

preview = agent.preview(user_input)

for page in preview:
    print(f"第{page['page_num']}页: {page['page_type']} - {page['title']}")
```

输出示例：
```
第1页: cover - 汇报标题
第2页: section - 教育背景
第3页: content-list - 教育背景
第4页: section - 获奖经历
第5页: content-list - 获奖经历
第6页: ending - 请老师批评指正！
```

---

## 4. 输入格式

### 4.1 基本格式 (推荐)

使用 `key: value` 格式：

```
主题：汇报标题
申请人：姓名
导师：导师姓名（可选）
申请方向：方向（可选）
时间：2025-01-01（可选）

1. 章节标题
- 内容项1
- 内容项2
```

### 4.2 支持的章节类型

| 章节关键词 | 自动识别类型 | 说明 |
|-----------|------------|------|
| 教育 | content-list | 教育背景列表 |
| 科研 | content-detail | 科研经历详情 |
| 获奖 | content-list | 获奖经历列表 |
| 学生工作 | content-list | 学生工作列表 |
| 优势 | content-list | 个人优势列表 |
| 计划 | timeline | 时间线展示 |

### 4.3 JSON 格式输入

```python
import json

data = {
    "meta": {
        "title": "研究生推免申请汇报",
        "author": "赵烁",
        "advisor": "武海军教授",
        "direction": "高性能新型智能材料",
        "date": "2025-9-15"
    },
    "sections": [
        {
            "title": "教育背景",
            "type": "content-list",
            "content": ["学校：重庆交通大学", "专业：材料科学与工程"]
        },
        {
            "title": "获奖经历",
            "type": "content-list",
            "content": ["奖项1", "奖项2"]
        }
    ]
}

# 转换为文本格式
text = json.dumps(data, ensure_ascii=False)
agent.generate(text, "output.pptx")
```

### 4.4 章节格式示例

#### 列表页（教育背景、获奖经历等）

```
1. 教育背景
- 时间：2022.09-2026.07
- 学校：重庆交通大学
- 专业：材料科学与工程专业
- 绩点：3.61/4.0
```

#### 详情页（科研经历）

```
2. 科研经历
- 2023.01-2024.06 智能材料研究项目
- 研究背景：...
- 研究要点：
  1. xxx
  2. xxx
```

#### 时间线页（研究生计划）

```
5. 研究生计划
- 研一：基础课程学习
- 研二：科研训练
- 研三：论文撰写
```

---

## 5. 配置选项

### 5.1 创建自定义配置

```python
from aut_sci_ppt.config import Config

# 方式1：使用默认配置
config = Config()

# 方式2：指定日志级别
config = Config(log_level="DEBUG")

# 方式3：从文件加载
config = Config(config_path="config.yaml")

# 使用配置创建 Agent
agent = PPTAgent(config)
```

### 5.2 配置文件格式 (config.yaml)

```yaml
# 页面尺寸（英寸）
page_size:
  width: 10
  height: 7.5

# 页边距
margins:
  top: 0.5
  bottom: 0.5
  left: 0.5
  right: 0.5

# 字体配置
fonts:
  title:
    name: 微软雅黑
    size: 44
    bold: true
  subtitle:
    name: 微软雅黑
    size: 28
  body:
    name: 微软雅黑
    size: 18

# 颜色配置
colors:
  primary: "#1E3A5F"
  secondary: "#4A90D9"
  accent: "#E8B339"
  text: "#333333"
  background: "#FFFFFF"

# 日志级别
log_level: "INFO"
```

### 5.3 日志级别

| 级别 | 说明 |
|------|------|
| DEBUG | 详细调试信息 |
| INFO | 一般信息 |
| WARNING | 警告信息 |
| ERROR | 错误信息 |

---

## 6. 高级功能

### 6.1 解析验证

```python
from aut_sci_ppt.parser import TextParser

parser = TextParser()
parsed = parser.parse(user_input)

# 获取验证警告
warnings = parser.validate(parsed)

if warnings:
    print("发现以下问题：")
    for warning in warnings:
        print(f"  - {warning}")
```

### 6.2 使用结构化数据生成

```python
 PPTAgent
from aut_sci_ppt.models import (
    CoverData,from aut_sci_ppt import ContentListData, ListItem,
    Page, PAGE_TYPE_CONTENT_LIST
)

agent = PPTAgent()

# 直接使用结构化数据
data = {
    "meta": {
        "title": "汇报标题",
        "author": "张三"
    }
}

agent.generate_from_structured(data, "output.pptx")
```

### 6.3 自定义模板

```python
from aut_sci_ppt.templates import register_template, get_template
from aut_sci_ppt.templates.base import BaseTemplate

# 创建自定义模板类
class MyCustomTemplate(BaseTemplate):
    def render(self, slide, data):
        # 实现自定义渲染逻辑
        pass

# 注册模板
register_template('my-custom', MyCustomTemplate)

# 使用模板
template = get_template('my-custom', config)
```

---

## 7. 模板系统

### 7.1 内置模板类型

| 模板类型 | 说明 | 典型用途 |
|---------|------|---------|
| cover | 封面页 | 标题、申请人、导师 |
| toc | 目录页 | 内容导航 |
| section | 章节封面 | Part X 章节标题 |
| content-list | 列表内容页 | 教育背景、获奖经历 |
| content-detail | 详情内容页 | 科研经历 |
| content-detail-image | 带图详情页 | 成果展示 |
| timeline | 时间线页 | 计划、经历 |
| ending | 结束页 | 致谢 |

### 7.2 使用带图片的详情页

```python
from aut_sci_ppt.models import (
    ContentDetailImageData, ImageItem, Page, 
    PAGE_TYPE_CONTENT_DETAIL_IMAGE
)

# 创建带图片的详情数据
data = ContentDetailImageData(
    title="研究成果展示",
    background="研究背景描述",
    points=["要点1", "要点2", "要点3"],
    results=["成果1", "成果2"],
    images=[
        ImageItem(
            path="path/to/image.jpg",
            position="right",  # left, right, top, bottom
            size={"width": 4, "height": 3},
            caption="图1：实验结果"
        )
    ],
    layout="right"  # 图片位置布局
)

page = Page(page_type=PAGE_TYPE_CONTENT_DETAIL_IMAGE, data=data)
```

---

## 8. API 参考

### 8.1 PPTAgent 类

```python
class PPTAgent:
    def __init__(self, config: Config = None)
        """初始化 Agent
        
        Args:
            config: 配置对象，默认使用全局配置
        """
    
    def generate(self, user_input: str, output_path: str = "output.pptx") -> str:
        """生成 PPT
        
        Args:
            user_input: 用户输入文本
            output_path: 输出文件路径
        
        Returns:
            生成的 PPT 文件路径
        """
    
    def generate_from_structured(self, data: Dict, output_path: str = "output.pptx") -> str:
        """从结构化数据生成 PPT
        
        Args:
            data: 结构化数据字典
            output_path: 输出文件路径
        
        Returns:
            生成的 PPT 文件路径
        """
    
    def preview(self, user_input: str) -> List[Dict]:
        """预览页面结构
        
        Args:
            user_input: 用户输入文本
        
        Returns:
            页面结构列表
        """
```

### 8.2 TextParser 类

```python
class TextParser:
    def parse(self, text: str) -> ParsedData:
        """解析文本内容"""
    
    def validate(self, data: ParsedData) -> List[str]:
        """验证解析结果
        
        Returns:
            警告信息列表
        """
```

### 8.3 SmartPaginator 类

```python
class SmartPaginator:
    def paginate(self, parsed_data: ParsedData) -> List[Page]:
        """将解析的数据分页"""
```

---

## 9. 常见问题

### Q1: 如何自定义字体？

在配置文件中修改 `fonts` 部分：

```yaml
fonts:
  title:
    name: 黑体
    size: 48
    bold: true
```

### Q2: 如何添加自定义章节类型？

修改 `parser/text_parser.py` 中的 `SUPPORTED_CONTENT_TYPES` 字典：

```python
SUPPORTED_CONTENT_TYPES = {
    '教育': 'content-list',
    '科研': 'content-detail',
    '你的关键词': 'content-list',  # 添加新类型
}
```

### Q3: 如何处理解析失败？

使用验证功能检查问题：

```python
parser = TextParser()
result = parser.parse(user_input)
warnings = parser.validate(result)

if warnings:
    # 处理警告
    for w in warnings:
        print(w)
```

### Q4: 如何调试生成过程？

设置日志级别为 DEBUG：

```python
from aut_sci_ppt.config import Config

config = Config(log_level="DEBUG")
agent = PPTAgent(config)
agent.generate(user_input, "output.pptx")
```

### Q5: 支持哪些图片格式？

支持：JPG, JPEG, PNG, GIF, BMP, WebP

---

## 附录：完整示例

```python
"""
完整的 PPT 生成示例
"""
from aut_sci_ppt import PPTAgent
from aut_sci_ppt.config import Config

# 1. 创建配置
config = Config(log_level="INFO")

# 2. 创建 Agent
agent = PPTAgent(config)

# 3. 准备输入
user_input = """
主题：研究生推免申请汇报
申请人：赵烁
导师：武海军教授
申请方向：高性能新型智能材料
时间：2025-9-15

目录：
1. 教育背景
2. 科研经历
3. 获奖经历
4. 学生工作
5. 研究生计划

1. 教育背景
- 时间：2022.09-2026.07
- 学校：重庆交通大学
- 专业：材料科学与工程专业
- 绩点：3.61/4.0，专业排名18/145
- CET-4：已通过
- 主修课程：材料科学基础（86），材料工程基础（87），复合材料学（87），材料性能学（89）

2. 科研经历
- 2023.01-2024.06 智能材料研究项目
- 研究背景：研究新型智能材料的性能
- 研究要点：
  1. 材料合成工艺优化
  2. 性能测试与表征
  3. 数据分析与总结

3. 获奖经历
- "徕卡杯"第十三届全国大学生金相技能大赛 国三 2024年07月
- 第六届重庆市大学生物理创新竞赛 市一 2023年12月

4. 学生工作
- 2022-2023 班级班长
- 2023-2024 学生会宣传部干事

5. 研究生计划
- 研一：夯实理论基础，修满学分
- 研二：进入课题组，开展科研
- 研三：撰写论文，完成答辩
"""

# 4. 预览结构
print("预览页面结构：")
preview = agent.preview(user_input)
for page in preview:
    print(f"  第{page['page_num']}页: {page['page_type']}")

# 5. 生成 PPT
print("\n正在生成PPT...")
output_path = agent.generate(user_input, "研究生推免申请汇报.pptx")
print(f"生成完成: {output_path}")
```

---

*文档版本：1.2*
*更新日期：2026-03-06*
*更新内容：新增日志系统、输入验证、多格式支持、单元测试、content-detail-image模板*
