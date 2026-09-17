---
name: nsfc-figure
description: 为 NSFC 申请书创建或重绘概念图、研究内容关系图和技术路线图；当交付物需要可编辑源图、稳定版式或可验证导出时，优先生成 Draw.io XML。纯数据统计图、照片处理或论文原图复用不应触发本 skill。
---

# NSFC 申请书图示

目标是让图在脱离正文时仍能传达一个明确结论，并同时交付可编辑、可追溯的源图。默认使用未压缩的 `.drawio` XML；只有数据驱动的统计图才优先考虑 Python 绘图。

## 工作流

1. 先从正文提炼“对象/问题 → 研究阶段或内容 → 验证 → 预期认识”的信息骨架。不得为了版式美观虚构研究内容、证据或因果关系。
2. 根据主要关系选择布局：
   - 递进过程：横向或纵向技术路线；
   - 多项内容共同支撑目标：并列分栏后汇聚；
   - 理论与实验反复校正：闭环，但仅在正文确有反馈关系时绘制回路；
   - 时间与任务：甘特图，不要硬套流程图。
3. 将正文压缩为两级文本。卡片标题表达动作或产物，说明文字只保留区分该卡片所需的信息；避免把段落搬进图中。
4. 优先生成或编辑 Draw.io 源文件：

   ```bash
   python nsfc-figure/scripts/generate_roadmap.py \
     --config nsfc-figure/assets/three-stage-roadmap.json \
     --output roadmap.drawio
   ```

   三阶段或四阶段的分栏技术路线可直接使用脚本。需要自由构图、实验装置或复杂示意时，从生成结果继续在 diagrams.net 中编辑，不要退化成不可编辑截图。
5. 运行结构验证：

   ```bash
   python nsfc-figure/scripts/validate_drawio.py roadmap.drawio
   ```

6. 交付前使用官方 Draw.io Desktop 实际导出 SVG/PDF/PNG，打开导出文件并按申请书中的实际尺寸检查。仅有 XML 可解析、导出命令成功或第三方渲染结果都不能代替视觉验收。若本机无法完成官方渲染，应明确说明“XML 已验证、渲染导出未在本机执行”，并把结果标记为待视觉验收，不得称为可直接使用。
7. 对最终 SVG/PNG 检查是否意外嵌入完整编辑源：

   ```bash
   python nsfc-figure/scripts/check_export_metadata.py roadmap.svg
   ```

## Draw.io 交付约束

- 保留未压缩 XML，便于版本审查、局部修改和错误定位。
- 所有 `mxCell` ID 唯一；顶层包含 `0`、`1` 两个根单元；边必须引用存在的源/目标节点。
- 给节点写明几何尺寸，使用正交连接线，尽量让主阅读方向一致并避免交叉。
- 使用一套字体、圆角、边框和语义色。颜色负责区分研究阶段，不负责装饰。
- 图片若不可避免，应嵌入文件或使用可移交的相对资源；禁止保留仅在作者机器有效的绝对路径。
- 涉及未公开申请书时优先使用本地桌面版编辑，不把 `.drawio` 源文件或完整正文上传到未经授权的在线服务。
- 图中术语、编号和正文逐项核对。图注解释“图说明什么”，不要重复图内全部文字。
- 内部工作包同时保留 `.drawio` 源文件和矢量预览；正式提交或公开分发的 SVG/PNG 不应嵌入完整编辑源，且必须检查隐藏图层、画布外对象和元数据。只有投稿系统限制时才使用高分辨率 PNG。

## 资源路由

- 需要选择版式、配色、字号或导出格式时，阅读 [references/drawio-authoring.md](references/drawio-authoring.md)。
- 需要快速搭建分栏技术路线时，复制并修改 [assets/three-stage-roadmap.json](assets/three-stage-roadmap.json)，再运行生成脚本。
- 需要检查生成器的完整用例时，查看 [examples/fictional-technical-roadmap.json](examples/fictional-technical-roadmap.json)、对应的 `.drawio` 源文件和官方 Draw.io 导出的 PNG 预览。示例是虚构内容，只用于验证工作流。

## 验收

- 只看图，能否说出核心问题、研究阶段、验证方式和最终汇聚点？
- 缩放到申请书中的实际宽度后，最小文字是否仍可读？
- 箭头是否表达真实依赖，而非仅为了连接所有卡片？
- XML 验证是否通过？是否已实际打开官方 Draw.io 导出的 SVG/PDF/PNG，确认无裁切、溢出、字体替换、连接线错位或意外嵌入的编辑源？
- 图与正文的术语、顺序、编号和预期产出是否一致？
