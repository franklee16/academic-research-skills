# thu-digitizer OA Figure Gallery

## 交互式风格复现

画廊中的交互图分为两种模式：

- `evidence-backed`：逐案例使用原图像素或 OA PDF 矢量几何定义画布、坐标、颜色、线宽、标记和布局；当前覆盖剂量—反应曲线、分组柱、热力图和纵向箱线图。
- `data-redraw`：只保证 CSV 中的提取值和图形语义，样式是独立重绘，不宣称逐像素复现原图。

两种模式都把悬停/键盘焦点绑定到 CSV 的真实记录。作者拟合曲线、箱线图的五数概括、热力图的截尾端点等不可从图像确定的内容，会在案例说明中单独标注。

这个静态画廊现在包含：

- 首页类型目录：采用紧凑白色卡片矩阵，直接展示 12 种可提取图形。点击原图卡片后进入案例详情，可切换原图、提取覆盖和静态数据复现，查看核验指标、可双向拖动的完整数据表并下载 CSV。
- 交互数据视图：直接从同一份 CSV 构建本地 SVG 图，鼠标或键盘聚焦数据标记时显示精确值。它单独标为“交互数据视图”，不声称逐像素复现论文原图样式。
- 真实论文：保留 Nature Portfolio OA 文章的题名、图号、原文链接和证据口径。

R Graph Gallery 只用于补充图表词汇，不是画廊的顶层分类。

## 本地预览

从仓库根目录运行：

```powershell
python -m http.server 8793 --bind 127.0.0.1 --directory gallery
```

然后打开 <http://127.0.0.1:8793/>。本项目使用 8793，是为了避开本机已有的 8765 服务。

## 内容结构

- `data/basics.json`：首页基础单图和精选论文案例；由 `scripts/build_basic_gallery.py` 生成。
- `data/cases.json`：完整论文案例清单；由 `scripts/build_gallery_evidence.py` 生成。
- `assets/cases/<case-id>/original.*`：OA 论文原图。
- `assets/basics/<type>/`：确定性基础单图的原图、覆盖层、复现图、CSV 与报告。
- `assets/cases/<case-id>/atlas-*.jpg`：只用于类型路由的代表面板裁剪，不是数值提取结果。
- `overlay.png`：提取图元与原图的可视注册检查。
- `recreated.png`：从提取数据绘制的复现图。
- `data.csv`：站点可下载的表格数据。
- `report.json`：校准、范围、验证与局限性。
- `source-data.*`：作者发布的官方附件或其可复核导出。

重新生成证据资产：

```powershell
python scripts\build_gallery_evidence.py
python scripts\build_basic_gallery.py
```

## 证据口径

`official_source_data_mapped` 表示官方源数据已逐行映射到可见图元；`visible_geometry_extracted` 表示数值来自像素几何；`partial_visible_geometry` 表示只处理了复杂图中的明确子面板。三者不可互换。

能力地图另外区分引擎成熟度和案例证据。`oa_reference` 只表示已经定位真实 OA 文章、图号和许可，不能据此宣称数字化成功。

当前未进行 WebPlotDigitizer 同条件对比，因此站点明确显示 `not compared`，不宣称优于或等价于该工具。
