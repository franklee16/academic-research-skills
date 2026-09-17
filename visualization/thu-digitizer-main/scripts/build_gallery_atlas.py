"""Build the OA case atlas and chart-type capability map for the gallery.

This script creates only crops, provenance reports, and taxonomy metadata. A crop
is a routing aid, not a numeric extraction. The manifest keeps engine maturity
and gallery evidence as separate fields so an identified OA example cannot be
mistaken for a validated extractor.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
CASES = GALLERY / "assets" / "cases"
DATA = GALLERY / "data"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


REFERENCE_CASES = [
    {
        "id": "nature-borneo-edge",
        "title": "森林边缘效应：散点、模型与重叠直方图",
        "articleTitle": "Long-term carbon sink in Borneo’s forests halted by drought and vulnerable to edge effects",
        "authors": "Qie et al.",
        "journal": "Nature Communications",
        "year": 2017,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-017-01997-0",
        "articleUrl": "https://www.nature.com/articles/s41467-017-01997-0",
        "figureUrl": "https://www.nature.com/articles/s41467-017-01997-0/figures/2",
        "original": "assets/cases/nature-borneo-edge/original.jpg",
        "evidenceStatus": "source_mapped",
        "coverage": ["scatter", "histogram", "model curve"],
        "report": "assets/cases/nature-borneo-edge/report.json",
    },
    {
        "id": "nature-blood-forest",
        "title": "29 项血液指标的 forest plot",
        "articleTitle": "Genetic architecture of routinely acquired blood tests in a British South Asian cohort",
        "authors": "Jacobs et al.",
        "journal": "Nature Communications",
        "year": 2024,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-024-53091-x",
        "articleUrl": "https://www.nature.com/articles/s41467-024-53091-x",
        "figureUrl": "https://www.nature.com/articles/s41467-024-53091-x/figures/2",
        "original": "assets/cases/nature-blood-forest/original.jpg",
        "evidenceStatus": "visible_geometry",
        "coverage": ["forest plot", "confidence interval", "color scale"],
        "report": "assets/cases/nature-blood-forest/report.json",
    },
    {
        "id": "nature-ribotie-multipanel",
        "title": "十面板混合科研图",
        "articleTitle": "Deep learning to decode sites of RNA translation in normal and cancerous tissues",
        "authors": "Clauwaert et al.",
        "journal": "Nature Communications",
        "year": 2025,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-025-56543-0",
        "articleUrl": "https://www.nature.com/articles/s41467-025-56543-0",
        "figureUrl": "https://www.nature.com/articles/s41467-025-56543-0/figures/2",
        "original": "assets/cases/nature-ribotie-multipanel/original.jpg",
        "evidenceStatus": "partial_visible",
        "coverage": ["boxplot", "bar", "donut", "scatter", "volcano", "histogram", "marginal plot", "multi-panel"],
        "report": "assets/cases/nature-ribotie-multipanel/report.json",
    },
    {
        "id": "nature-nanopore-scatter",
        "title": "纳米孔信号：密集散点、边际分布与波形",
        "articleTitle": "Detecting topological variations of DNA at single-molecule level",
        "authors": "Bell et al.",
        "journal": "Nature Communications",
        "year": 2019,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-018-07924-1",
        "articleUrl": "https://www.nature.com/articles/s41467-018-07924-1",
        "figureUrl": "https://www.nature.com/articles/s41467-018-07924-1/figures/2",
        "original": "assets/cases/nature-nanopore-scatter/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["dense scatter", "histogram", "signal trace", "multi-panel"],
    },
    {
        "id": "nature-violin-heatmap",
        "title": "分布与矩阵：violin、boxplot 和 heatmap",
        "articleTitle": "Dynamic control of enhancer activity drives stage-specific gene expression during flower morphogenesis",
        "authors": "Yan et al.",
        "journal": "Nature Communications",
        "year": 2019,
        "figure": "Fig. 5",
        "doi": "10.1038/s41467-019-09513-2",
        "articleUrl": "https://www.nature.com/articles/s41467-019-09513-2",
        "figureUrl": "https://www.nature.com/articles/s41467-019-09513-2/figures/5",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6461659/",
        "original": "assets/cases/nature-violin-heatmap/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["violin", "boxplot", "heatmap", "Venn"],
    },
    {
        "id": "nature-protaide-heatmap",
        "title": "相关矩阵：色条校准与显著性标记",
        "articleTitle": "A deep joint-learning proteomics model for diagnosis of six conditions associated with dementia",
        "authors": "An et al.",
        "journal": "Nature Medicine",
        "year": 2026,
        "figure": "Fig. 4c",
        "doi": "10.1038/s41591-026-04303-y",
        "articleUrl": "https://www.nature.com/articles/s41591-026-04303-y",
        "figureUrl": "https://www.nature.com/articles/s41591-026-04303-y/figures/4",
        "original": "assets/cases/nature-protaide-heatmap/original.png",
        "evidenceStatus": "source_mapped",
        "coverage": ["heatmap", "correlation matrix", "colour bar", "significance overlay"],
        "report": "assets/cases/nature-protaide-heatmap/report.json",
    },
    {
        "id": "nature-spatial-treemap",
        "title": "空间组学：Voronoi treemap、点阵与空间地图",
        "articleTitle": "Spatial-ID: a cell typing method for spatially resolved transcriptomics via transfer learning and spatial embedding",
        "authors": "Shen et al.",
        "journal": "Nature Communications",
        "year": 2022,
        "figure": "Fig. 6",
        "doi": "10.1038/s41467-022-35288-0",
        "articleUrl": "https://www.nature.com/articles/s41467-022-35288-0",
        "figureUrl": "https://www.nature.com/articles/s41467-022-35288-0/figures/6",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9741613/",
        "original": "assets/cases/nature-spatial-treemap/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["Voronoi treemap", "spatial point map", "dot matrix", "bar"],
    },
    {
        "id": "nature-graphddp-ternary",
        "title": "结构数据：网络、ternary 与侧栏 bar",
        "articleTitle": "GraphDDP: a graph-embedding approach to detect differentiation pathways in single-cell-data using prior class knowledge",
        "authors": "Costa, Grün & Backofen",
        "journal": "Nature Communications",
        "year": 2018,
        "figure": "Fig. 3",
        "doi": "10.1038/s41467-018-05988-7",
        "articleUrl": "https://www.nature.com/articles/s41467-018-05988-7",
        "figureUrl": "https://www.nature.com/articles/s41467-018-05988-7/figures/3",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6134144/",
        "original": "assets/cases/nature-graphddp-ternary/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["network", "ternary", "bar", "annotation"],
    },
    {
        "id": "nature-economic-map",
        "title": "地理栅格：连续色标地图与分类地图",
        "articleTitle": "A human-machine collaborative approach measures economic development using satellite imagery",
        "authors": "Ahn et al.",
        "journal": "Nature Communications",
        "year": 2023,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-023-42122-8",
        "articleUrl": "https://www.nature.com/articles/s41467-023-42122-8",
        "figureUrl": "https://www.nature.com/articles/s41467-023-42122-8/figures/2",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10603027/",
        "original": "assets/cases/nature-economic-map/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["raster map", "choropleth", "categorical map", "grid"],
    },
    {
        "id": "nature-sankey-flow",
        "title": "食物网简化中的 Sankey 信息流",
        "articleTitle": "A network simplification approach to ease topological studies about the food-web architecture",
        "authors": "Gini, Re & Facchini",
        "journal": "Scientific Reports",
        "year": 2022,
        "figure": "Fig. 3",
        "doi": "10.1038/s41598-022-17508-1",
        "articleUrl": "https://www.nature.com/articles/s41598-022-17508-1",
        "figureUrl": "https://www.nature.com/articles/s41598-022-17508-1/figures/3",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9385703/",
        "original": "assets/cases/nature-sankey-flow/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["Sankey", "alluvial", "flow labels"],
    },
    {
        "id": "nature-nagler-polar",
        "title": "极坐标、显微图、空间场与光谱的复合图",
        "articleTitle": "Giant magnetic splitting inducing near-unity valley polarization in van der Waals heterostructures",
        "authors": "Nagler et al.",
        "journal": "Nature Communications",
        "year": 2017,
        "figure": "Fig. 1",
        "doi": "10.1038/s41467-017-01748-1",
        "articleUrl": "https://www.nature.com/articles/s41467-017-01748-1",
        "figureUrl": "https://www.nature.com/articles/s41467-017-01748-1/figures/1",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5691051/",
        "original": "assets/cases/nature-nagler-polar/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["polar plot", "microscopy", "raster field", "spectrum", "multi-panel"],
    },
    {
        "id": "nature-phf6-survival",
        "title": "Kaplan–Meier 阶梯曲线、删失标记与风险表",
        "articleTitle": "Molecular and clinical analyses of PHF6 mutant myeloid neoplasia provide their pathogenesis and therapeutic targeting",
        "authors": "Kubota et al.",
        "journal": "Nature Communications",
        "year": 2024,
        "figure": "Fig. 4",
        "doi": "10.1038/s41467-024-46134-w",
        "articleUrl": "https://www.nature.com/articles/s41467-024-46134-w",
        "figureUrl": "https://www.nature.com/articles/s41467-024-46134-w/figures/4",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10901781/",
        "original": "assets/cases/nature-phf6-survival/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["Kaplan–Meier", "censor marks", "risk table", "multi-panel"],
    },
    {
        "id": "nature-xenopus-polar",
        "title": "生理信号复合图：波形、散点、误差棒与极坐标插图",
        "articleTitle": "Locomotion-induced ocular motor behavior in larval Xenopus is developmentally tuned by visuo-vestibular reflexes",
        "authors": "Bacqué-Cazenave et al.",
        "journal": "Nature Communications",
        "year": 2022,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-022-30636-6",
        "articleUrl": "https://www.nature.com/articles/s41467-022-30636-6",
        "figureUrl": "https://www.nature.com/articles/s41467-022-30636-6/figures/2",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9135768/",
        "original": "assets/cases/nature-xenopus-polar/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["signal traces", "scatter", "bar", "error bars", "polar inset", "multi-panel"],
    },
    {
        "id": "nature-acth-spectrum",
        "title": "多面板质谱峰图与标注峰",
        "articleTitle": "Ultrafast enzymatic digestion of proteins by microdroplet mass spectrometry",
        "authors": "Zhong, Chen & Zare",
        "journal": "Nature Communications",
        "year": 2020,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-020-14877-x",
        "articleUrl": "https://www.nature.com/articles/s41467-020-14877-x",
        "figureUrl": "https://www.nature.com/articles/s41467-020-14877-x/figures/2",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7044307/",
        "original": "assets/cases/nature-acth-spectrum/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["mass spectrum", "peak labels", "stacked panels"],
    },
    {
        "id": "nature-autospill-flow",
        "title": "流式细胞术密度场、门控边界与小倍图",
        "articleTitle": "AutoSpill is a principled framework that simplifies the analysis of multichromatic flow cytometry data",
        "authors": "Roca et al.",
        "journal": "Nature Communications",
        "year": 2021,
        "figure": "Fig. 1",
        "doi": "10.1038/s41467-021-23126-8",
        "articleUrl": "https://www.nature.com/articles/s41467-021-23126-8",
        "figureUrl": "https://www.nature.com/articles/s41467-021-23126-8/figures/1",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8129071/",
        "original": "assets/cases/nature-autospill-flow/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["flow cytometry", "density field", "gating polygon", "small multiples"],
    },
    {
        "id": "nature-sarscov2-phylogeny",
        "title": "系统发育树、世界地图与分布图的复合图",
        "articleTitle": "No evidence for increased transmissibility from recurrent mutations in SARS-CoV-2",
        "authors": "van Dorp et al.",
        "journal": "Nature Communications",
        "year": 2020,
        "figure": "Fig. 1",
        "doi": "10.1038/s41467-020-19818-2",
        "articleUrl": "https://www.nature.com/articles/s41467-020-19818-2",
        "figureUrl": "https://www.nature.com/articles/s41467-020-19818-2/figures/1",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7688939/",
        "original": "assets/cases/nature-sarscov2-phylogeny/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["phylogenetic tree", "point map", "violin", "multi-panel"],
    },
    {
        "id": "nature-hypergraph-roc",
        "title": "多系列 ROC 阶梯曲线与网络插图",
        "articleTitle": "Hypergraph reconstruction from dynamics",
        "authors": "Delabays et al.",
        "journal": "Nature Communications",
        "year": 2025,
        "figure": "Fig. 2",
        "doi": "10.1038/s41467-025-57664-2",
        "articleUrl": "https://www.nature.com/articles/s41467-025-57664-2",
        "figureUrl": "https://www.nature.com/articles/s41467-025-57664-2/figures/2",
        "pmcUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11923283/",
        "original": "assets/cases/nature-hypergraph-roc/original.jpg",
        "evidenceStatus": "oa_reference",
        "coverage": ["ROC", "step curves", "network inset", "multi-panel"],
    },
    {
        "id": "nature-40822-fig1f",
        "title": "四组细胞类型组成的环形饼图",
        "articleTitle": "Driver gene combinations dictate cutaneous squamous cell carcinoma disease continuum progression",
        "authors": "Bailey et al.",
        "journal": "Nature Communications",
        "year": 2023,
        "figure": "Fig. 1f",
        "doi": "10.1038/s41467-023-40822-9",
        "articleUrl": "https://www.nature.com/articles/s41467-023-40822-9",
        "figureUrl": "https://www.nature.com/articles/s41467-023-40822-9/figures/1",
        "original": "assets/cases/nature-40822-fig1f/original.png",
        "evidenceStatus": "candidate",
        "coverage": ["donut", "visible percentage labels", "shared annular geometry validation"],
        "report": "assets/cases/nature-40822-fig1f/report.json",
    },
]


CROPS = {
    "nature-borneo-edge": {
        "scatter": (0, 0, 455, 387),
        "histogram": (455, 0, 676, 387),
    },
    "nature-blood-forest": {"forest": (0, 0, 675, 452)},
    "nature-ribotie-multipanel": {
        "boxplot": (0, 0, 250, 275),
        "bar": (245, 0, 515, 275),
        "donut": (510, 0, 798, 275),
        "scatter": (250, 275, 505, 470),
        "volcano": (0, 460, 265, 734),
        "histogram": (260, 460, 555, 734),
        "marginal": (545, 460, 798, 734),
    },
    "nature-nanopore-scatter": {
        "dense_scatter": (145, 0, 662, 235),
        "signal": (0, 180, 545, 470),
    },
    "nature-violin-heatmap": {
        "violin": (0, 0, 215, 252),
        "heatmap": (205, 0, 380, 252),
    },
    "nature-protaide-heatmap": {
        "heatmap": (75, 45, 900, 725),
    },
    "nature-spatial-treemap": {
        "spatial_map": (0, 150, 685, 385),
        "treemap": (0, 360, 430, 565),
        "dot_matrix": (0, 535, 430, 760),
    },
    "nature-graphddp-ternary": {
        "network": (150, 0, 650, 541),
        "ternary": (440, 0, 665, 220),
        "bar": (640, 0, 798, 541),
    },
    "nature-economic-map": {
        "raster_map": (0, 0, 500, 545),
        "grid_map": (225, 500, 480, 700),
    },
    "nature-sankey-flow": {"sankey": (0, 0, 676, 420)},
    "nature-nagler-polar": {
        "microscopy": (35, 20, 330, 270),
        "polar": (345, 0, 676, 280),
        "raster_field": (30, 265, 360, 551),
        "spectrum": (365, 265, 676, 551),
    },
    "nature-phf6-survival": {
        "kaplan_meier": (0, 0, 275, 450),
        "risk_table": (0, 285, 800, 450),
    },
    "nature-xenopus-polar": {
        "waveform": (135, 0, 800, 210),
        "scatter": (25, 190, 230, 395),
        "errorbar": (205, 185, 800, 405),
        "polar_inset": (650, 175, 800, 335),
    },
    "nature-acth-spectrum": {
        "mass_spectrum": (0, 0, 650, 851),
        "peak_panel": (55, 0, 650, 185),
    },
    "nature-autospill-flow": {
        "flow_cytometry": (190, 0, 605, 430),
        "small_multiples": (0, 0, 800, 850),
    },
    "nature-sarscov2-phylogeny": {
        "phylogeny": (0, 0, 365, 391),
        "point_map": (350, 0, 680, 225),
        "violin": (385, 185, 680, 391),
    },
    "nature-hypergraph-roc": {
        "roc": (0, 0, 743, 720),
        "network_inset": (285, 205, 735, 630),
    },
    "nature-40822-fig1f": {"donut": (0, 0, 1025, 215)},
}


GROUPS = [
    {"id": "xy-curves", "label": "Cartesian curves", "title": "XY 曲线与轨迹", "route": "xy"},
    {"id": "xy-points", "label": "Cartesian points", "title": "XY 点、拟合与嵌入", "route": "xy"},
    {"id": "categorical-bars", "label": "Categorical marks", "title": "分类柱、条与点", "route": "bar"},
    {"id": "distribution", "label": "Distributions", "title": "分布与样本概括", "route": "xy"},
    {"id": "intervals", "label": "Intervals", "title": "区间、不确定性与估计", "route": "xy"},
    {"id": "matrix-fields", "label": "Matrix & fields", "title": "矩阵、等高线与连续场", "route": "xy"},
    {"id": "polar-radial", "label": "Polar & radial", "title": "极坐标、径向与圆记录图", "route": "polar"},
    {"id": "ternary", "label": "Ternary", "title": "三元与单纯形", "route": "ternary"},
    {"id": "map-image", "label": "Map & scaled image", "title": "地图、显微图与标尺图像", "route": "map_scale"},
    {"id": "composition-hierarchy", "label": "Composition & hierarchy", "title": "组成、嵌套与层级", "route": "structure"},
    {"id": "flow-network", "label": "Flow & network", "title": "流、网络与树", "route": "structure"},
    {"id": "scientific-specialty", "label": "Scientific specialty", "title": "科研专用语义图", "route": "semantic_router"},
    {"id": "composite", "label": "Composite figures", "title": "复合图、多面板与嵌入表", "route": "semantic_router"},
]


CALIBRATION_FAMILIES = [
    {
        "id": "xy",
        "label": "2D XY",
        "origin": "WebPlotDigitizer",
        "description": "线性、对数或日期轴；承载曲线、散点、直方图与大多数统计图。",
    },
    {
        "id": "bar",
        "label": "Bar axis",
        "origin": "WebPlotDigitizer",
        "description": "一个分类轴和一个连续轴；与两个连续轴的直方图分开。",
    },
    {
        "id": "polar",
        "label": "Polar",
        "origin": "WebPlotDigitizer",
        "description": "中心、径向标尺和角度方向的专用校准。",
    },
    {
        "id": "ternary",
        "label": "Ternary",
        "origin": "WebPlotDigitizer",
        "description": "三角形三个顶点和方向决定三分量坐标。",
    },
    {
        "id": "map_scale",
        "label": "Map / scale bar",
        "origin": "WebPlotDigitizer",
        "description": "地图、显微图等只有比例尺的图像。",
    },
    {
        "id": "image_pixel",
        "label": "Image pixels",
        "origin": "WebPlotDigitizer",
        "description": "不换算数据轴，直接恢复像素位置、距离、面积或周长。",
    },
    {
        "id": "circular_recorder",
        "label": "Circular recorder",
        "origin": "WebPlotDigitizer",
        "description": "圆形记录纸的时间与径向信号专用校准。",
    },
    {
        "id": "structure",
        "label": "Structure parser",
        "origin": "thu-digitizer extension",
        "description": "节点、边、扇区、层级和流带，不强行套用 XY 坐标。",
    },
    {
        "id": "semantic_router",
        "label": "Scientific router",
        "origin": "thu-digitizer extension",
        "description": "识别科研语义和面板结构，再路由到一个或多个校准/图元提取器。",
    },
]


def capability(
    id_: str,
    group: str,
    label: str,
    aliases: list[str],
    engine: str,
    demo: str,
    representation: str,
    case_id: str | None = None,
    crop: str | None = None,
    non_recoverable: str = "隐藏的作者原始数据与不可见统计过程",
    route: str | None = None,
) -> dict:
    return {
        "id": id_,
        "group": group,
        "label": label,
        "aliases": aliases,
        "engineStatus": engine,
        "demoStatus": demo,
        "recoverableRepresentation": representation,
        "nonRecoverable": non_recoverable,
        "caseId": case_id,
        "thumbnailKey": crop,
        "calibrationFamily": route or next(item["route"] for item in GROUPS if item["id"] == group),
    }


CAPABILITIES = [
    # Cartesian curves: one calibration family, several different visible representations.
    capability("line-time-series", "xy-curves", "Line / time series", ["折线图", "时间序列", "多系列曲线"], "stable", "oa_reference", "颜色可分的曲线中心线与校准坐标", "nature-nanopore-scatter", "signal", "不可见采样点、平滑参数与插值规则"),
    capability("step-curve", "xy-curves", "Step curve", ["阶梯图", "分段常数曲线"], "candidate", "oa_reference", "水平段、垂直跃迁和转折坐标", "nature-hypergraph-roc", "roc"),
    capability("connected-curve", "xy-curves", "Connected trajectory", ["连线轨迹", "相位轨迹"], "candidate", "oa_reference", "有序点或连续路径", "nature-xenopus-polar", "waveform"),
    capability("area-stream", "xy-curves", "Area / stacked area", ["面积图", "堆叠面积", "streamgraph"], "candidate", "no_case", "基线和每层可见上边界", non_recoverable="被遮挡层边界与原始样本"),
    capability("dose-model", "xy-curves", "Dose-response / fitted model", ["剂量反应", "模型曲线", "拟合线"], "candidate", "source_mapped", "可见模型曲线、拐点与标定轴", "nature-borneo-edge", "scatter", "作者未公开的拟合过程与残差"),
    capability("waveform", "xy-curves", "Waveform / signal trace", ["波形", "示波器", "生理信号"], "candidate", "oa_reference", "时间-幅值轨迹、事件边界与标尺", "nature-xenopus-polar", "waveform", "隐藏采样率、滤波与触发条件"),

    capability("scatter", "xy-points", "Scatter", ["散点图", "二维点图"], "stable", "source_mapped", "点中心、系列与校准坐标", "nature-borneo-edge", "scatter"),
    capability("bubble", "xy-points", "Bubble", ["气泡图", "大小编码点"], "candidate", "oa_reference", "点中心；有尺寸图例时估计面积编码", "nature-spatial-treemap", "dot_matrix", "没有图例时面积对应的绝对值"),
    capability("dense-marginal", "xy-points", "Dense scatter / marginal", ["密集散点", "边际分布", "joint plot"], "restricted", "oa_reference", "可分离点、密度轮廓与边际统计图", "nature-ribotie-multipanel", "marginal", "融合点簇中的逐点身份"),
    capability("connected-scatter", "xy-points", "Connected scatter", ["连线散点", "轨迹点"], "candidate", "oa_reference", "点中心、连接顺序与分组", "nature-nanopore-scatter", "signal"),
    capability("regression-scatter", "xy-points", "Regression scatter", ["回归散点", "拟合散点"], "stable", "source_mapped", "点、拟合线和可见参考线分层恢复", "nature-borneo-edge", "scatter", "作者模型的未公开参数与推断过程"),
    capability("volcano-manhattan", "xy-points", "Volcano / Manhattan", ["火山图", "曼哈顿图", "显著性散点"], "candidate", "oa_reference", "点中心、阈值线、显著点标签和轴变换", "nature-ribotie-multipanel", "volcano"),
    capability("embedding", "xy-points", "Embedding / UMAP / t-SNE", ["降维嵌入", "UMAP", "t-SNE"], "candidate", "oa_reference", "可见点位置、类别、聚类和局部轨迹", "nature-spatial-treemap", "spatial_map", "高维原始特征与真实距离语义"),

    capability("bar", "categorical-bars", "Vertical / horizontal bar", ["柱状图", "条形图", "正负柱"], "benchmark_only", "oa_reference", "分类、系列、基线与柱端值", "nature-ribotie-multipanel", "bar"),
    capability("grouped-bar", "categorical-bars", "Grouped bar", ["分组柱", "簇状柱"], "benchmark_only", "oa_reference", "组、子系列和各柱端值", "nature-xenopus-polar", "errorbar"),
    capability("stacked-bar", "categorical-bars", "Stacked / 100% bar", ["堆叠柱", "百分比堆叠"], "benchmark_only", "oa_reference", "每个可见分段边界与合计", "nature-ribotie-multipanel", "bar", "未展示的组内样本"),
    capability("diverging-bar", "categorical-bars", "Diverging bar", ["发散柱", "人口金字塔"], "benchmark_only", "no_case", "零基线两侧的类别和端值"),
    capability("waterfall", "categorical-bars", "Waterfall", ["瀑布图", "桥图"], "candidate", "no_case", "起点、增量、累计端点和连接线"),
    capability("lollipop-dot", "categorical-bars", "Lollipop / dot plot", ["棒棒糖图", "克利夫兰点图"], "candidate", "no_case", "类别位置、点值与连接线"),

    capability("histogram", "distribution", "Histogram", ["直方图", "频数分布"], "stable", "source_mapped", "连续轴下的 bin 边界与高度", "nature-borneo-edge", "histogram", "生成直方图的原始样本"),
    capability("boxplot", "distribution", "Boxplot", ["箱线图", "盒须图", "横向箱线图"], "stable", "oa_reference", "五数概括与可见离群点", "nature-ribotie-multipanel", "boxplot", "原始样本"),
    capability("violin-raincloud", "distribution", "Violin / raincloud", ["小提琴图", "雨云图"], "restricted", "oa_reference", "可见密度轮廓、内嵌箱线和样本点", "nature-violin-heatmap", "violin", "核密度参数与原始样本"),
    capability("strip-beeswarm", "distribution", "Strip / beeswarm", ["抖动点", "蜂群图"], "candidate", "oa_reference", "可分离点中心、组别和局部堆叠", "nature-ribotie-multipanel", "boxplot", "融合点簇中的隐藏样本"),
    capability("density-ridgeline", "distribution", "Density / ridgeline", ["密度曲线", "山脊图", "joyplot"], "restricted", "oa_reference", "每组可见密度轮廓", "nature-violin-heatmap", "violin", "生成曲线的原始样本和带宽"),
    capability("ecdf", "distribution", "ECDF / cumulative", ["经验累积分布", "累积分布"], "candidate", "no_case", "阶梯位置与可见累计概率", non_recoverable="重复值中的精确个体身份"),

    capability("error-point-range", "intervals", "Error bar / point range", ["误差棒", "点区间", "均值与误差"], "stable", "partial_visible", "点估计、上下端点和帽线，独立于主系列", "nature-xenopus-polar", "errorbar", "未说明的 SD、SEM 或置信区间语义"),
    capability("forest", "intervals", "Forest / coefficient", ["森林图", "系数图", "dot-whisker"], "candidate", "visible_geometry", "点估计、区间端点、参考线和行标签", "nature-blood-forest", "forest", "作者未展示的统计模型"),
    capability("confidence-band", "intervals", "Confidence / ribbon band", ["置信带", "预测带", "ribbon"], "candidate", "no_case", "上下边界和中心线", non_recoverable="误差带定义与原始拟合样本"),
    capability("funnel", "intervals", "Funnel plot", ["漏斗图", "发表偏倚图"], "candidate", "no_case", "研究点、中心线与显著性边界"),
    capability("candlestick", "intervals", "Candlestick / OHLC", ["蜡烛图", "K 线", "OHLC"], "candidate", "no_case", "开高低收与时间位置"),

    capability("heatmap", "matrix-fields", "Heatmap", ["热图", "颜色矩阵"], "candidate", "source_mapped", "行列网格、经色条标定的单元值与可见显著性标记", "nature-protaide-heatmap", "heatmap", "无色条时的绝对数值，以及色条端点之外被截断的精确幅度"),
    capability("correlogram-dotmatrix", "matrix-fields", "Correlogram / dot matrix", ["相关矩阵", "点阵矩阵", "气泡矩阵"], "candidate", "oa_reference", "矩阵索引、符号与可标定颜色/面积", "nature-spatial-treemap", "dot_matrix"),
    capability("contour", "matrix-fields", "Contour / isoline", ["等高线", "等值线", "相图边界"], "coordinate_specific", "oa_reference", "等值线几何、标签和标定坐标", "nature-autospill-flow", "flow_cytometry", "线间未显示的连续场"),
    capability("density-2d", "matrix-fields", "2D density", ["二维密度", "核密度场", "hex density"], "restricted", "oa_reference", "色条标定的密度场和可见轮廓", "nature-autospill-flow", "flow_cytometry", "原始二维事件全集"),
    capability("raster-field", "matrix-fields", "Raster / intensity field", ["强度场", "伪彩色图", "二维栅格"], "coordinate_specific", "oa_reference", "规则像元与经色条标定的强度", "nature-nagler-polar", "raster_field", "插值前的原始测量点"),
    capability("surface-mesh", "matrix-fields", "3D surface / mesh", ["三维曲面", "网格面", "瀑布谱"], "restricted", "no_case", "可见投影轮廓和网格交点", non_recoverable="单张透视图遮挡的背面与真实三维网格"),

    capability("polar-curve", "polar-radial", "Polar curve / scatter", ["极坐标曲线", "极坐标散点", "角度响应"], "coordinate_specific", "oa_reference", "角度、半径和系列轨迹", "nature-nagler-polar", "polar", route="polar"),
    capability("radar", "polar-radial", "Radar / spider", ["雷达图", "蜘蛛图"], "coordinate_specific", "no_case", "逐轴半径值和系列多边形", route="polar"),
    capability("rose-wind", "polar-radial", "Rose / wind rose", ["玫瑰图", "风向玫瑰", "极坐标直方图"], "coordinate_specific", "no_case", "角度 bin、径向长度和堆叠分段", route="polar"),
    capability("circular-bar", "polar-radial", "Circular bar", ["环形柱", "径向柱"], "coordinate_specific", "no_case", "角度类别和径向柱长", route="polar"),
    capability("radial-heatmap", "polar-radial", "Radial heatmap", ["环形热图", "径向矩阵"], "coordinate_specific", "no_case", "角度-半径网格与颜色值", route="polar"),
    capability("circular-recorder", "polar-radial", "Circular chart recorder", ["圆形记录纸", "圆盘记录仪"], "coordinate_specific", "no_case", "圆周时间和径向信号轨迹", route="circular_recorder", non_recoverable="记录纸转速与起始时间未标注时的绝对时间"),

    capability("ternary-scatter", "ternary", "Ternary scatter", ["三元散点", "simplex"], "coordinate_specific", "oa_reference", "三角坐标内点与三分量比例", "nature-graphddp-ternary", "ternary", route="ternary"),
    capability("ternary-contour", "ternary", "Ternary contour / heatmap", ["三元等高线", "三元热图"], "coordinate_specific", "no_case", "三元网格、等值线与颜色值", route="ternary"),
    capability("simplex-trajectory", "ternary", "Simplex trajectory", ["三元轨迹", "组成演化"], "coordinate_specific", "no_case", "三分量点序列和连接方向", route="ternary"),

    capability("raster-choropleth-map", "map-image", "Raster / choropleth map", ["栅格地图", "分级设色", "连续色标地图"], "coordinate_specific", "oa_reference", "有地理配准和色条时的像元或区域值", "nature-economic-map", "raster_map", "缺失投影时的精确地理坐标", "map_scale"),
    capability("point-bubble-map", "map-image", "Point / bubble map", ["点地图", "气泡地图", "空间点图"], "coordinate_specific", "oa_reference", "点位置、类别与可标定面积", "nature-sarscov2-phylogeny", "point_map", route="map_scale"),
    capability("grid-hexbin-map", "map-image", "Grid / hexbin map", ["规则栅格地图", "六边形地图"], "coordinate_specific", "oa_reference", "网格索引、边界和颜色值", "nature-economic-map", "grid_map", route="map_scale"),
    capability("connection-map", "map-image", "Connection map", ["迁徙线", "航线图", "流向地图"], "coordinate_specific", "no_case", "可见端点、路径和方向", route="map_scale"),
    capability("cartogram", "map-image", "Cartogram", ["变形地图"], "coordinate_specific", "no_case", "变形后的区域、标签和邻接", route="map_scale", non_recoverable="未提供底图时的原始地理面积"),
    capability("scale-microscopy", "map-image", "Scale-bar image / microscopy", ["显微图", "比例尺图像", "遥感影像"], "coordinate_specific", "oa_reference", "比例尺标定后的点、距离、面积和对象轮廓", "nature-nagler-polar", "microscopy", route="map_scale"),
    capability("pixel-measurement", "map-image", "Generic pixel measurement", ["像素坐标", "长度", "面积", "周长"], "candidate", "oa_reference", "像素位置、轮廓、距离、面积与周长", "nature-nagler-polar", "microscopy", route="image_pixel", non_recoverable="没有比例尺时的物理单位"),

    capability("pie-donut", "composition-hierarchy", "Pie / donut", ["饼图", "甜甜圈图"], "candidate", "visible_geometry", "双遍转录一致的可见百分比标签；扇区角度仅作独立验证", "nature-40822-fig1f", "donut", route="structure"),
    capability("treemap-voronoi", "composition-hierarchy", "Treemap / Voronoi treemap", ["矩形树图", "Voronoi treemap"], "coordinate_specific", "oa_reference", "可见区域面积、标签与显式层级", "nature-spatial-treemap", "treemap", route="structure", non_recoverable="未编码或被裁切的隐藏层级"),
    capability("sunburst-packing", "composition-hierarchy", "Sunburst / circle packing", ["旭日图", "圆堆积", "径向层级"], "coordinate_specific", "no_case", "可见嵌套、面积或角度", route="structure"),
    capability("dendrogram", "composition-hierarchy", "Dendrogram", ["树状图", "聚类树"], "coordinate_specific", "no_case", "可见叶、分支与合并高度", route="structure", non_recoverable="生成树的原始距离矩阵"),
    capability("waffle", "composition-hierarchy", "Waffle / unit grid", ["华夫图", "单位方格"], "candidate", "no_case", "单位格计数、类别和显式比例", route="structure"),

    capability("sankey-alluvial", "flow-network", "Sankey / alluvial", ["桑基图", "河流流向图", "alluvial"], "coordinate_specific", "oa_reference", "节点、层级、可见流带宽度和标签", "nature-sankey-flow", "sankey", route="structure", non_recoverable="遮挡流与未标定流量"),
    capability("network", "flow-network", "Network", ["网络图", "力导向图", "超图"], "coordinate_specific", "oa_reference", "可见节点、边、标签和布局坐标", "nature-graphddp-ternary", "network", route="structure", non_recoverable="遮挡边和隐藏拓扑"),
    capability("chord-circos", "flow-network", "Chord / Circos", ["弦图", "Circos", "环形连接图"], "coordinate_specific", "no_case", "扇区、连接带、方向和环形注释", route="structure"),
    capability("arc-bundle", "flow-network", "Arc / edge bundling", ["弧图", "边捆绑"], "restricted", "no_case", "可分离节点和可见路径", route="structure", non_recoverable="捆绑重叠中的完整边集合"),
    capability("phylogenetic-tree", "flow-network", "Phylogenetic tree", ["系统发育树", "cladogram", "进化树"], "coordinate_specific", "oa_reference", "分支拓扑、叶标签、分支长度和旁注轨道", "nature-sarscov2-phylogeny", "phylogeny", route="structure", non_recoverable="生成树的序列比对和模型"),

    capability("kaplan-meier", "scientific-specialty", "Kaplan–Meier + risk table", ["生存曲线", "KM 曲线", "风险表"], "candidate", "oa_reference", "阶梯曲线、删失标记、风险表和组别", "nature-phf6-survival", "kaplan_meier", route="semantic_router", non_recoverable="个体级生存记录"),
    capability("roc-pr", "scientific-specialty", "ROC / precision-recall", ["ROC", "PR 曲线", "AUC 曲线"], "candidate", "oa_reference", "多系列阶梯曲线、参考线和阈值路径", "nature-hypergraph-roc", "roc", route="semantic_router", non_recoverable="逐样本预测分数与精确阈值"),
    capability("mass-spectrum", "scientific-specialty", "Mass spectrum / stick spectrum", ["质谱", "棒状谱", "峰图"], "candidate", "oa_reference", "峰位、相对强度、基线和可读峰标注", "nature-acth-spectrum", "mass_spectrum", route="semantic_router", non_recoverable="仪器原始谱、峰宽和未显示低强度信号"),
    capability("spectrum-chromatogram", "scientific-specialty", "Spectrum / chromatogram", ["光谱", "Raman", "色谱", "衍射谱"], "candidate", "oa_reference", "连续曲线、峰位、峰高/面积和标注", "nature-nagler-polar", "spectrum", route="semantic_router", non_recoverable="仪器响应函数和原始采样"),
    capability("flow-cytometry", "scientific-specialty", "Flow cytometry gating", ["流式细胞术", "门控图", "FACS"], "coordinate_specific", "oa_reference", "二维密度场、门控多边形、簇中心和比例标注", "nature-autospill-flow", "flow_cytometry", route="semantic_router", non_recoverable="FCS 事件级数据与补偿矩阵"),
    capability("gel-blot", "scientific-specialty", "Gel / blot densitometry", ["凝胶", "Western blot", "条带灰度"], "restricted", "no_case", "泳道、条带轮廓、背景校正后的相对灰度", route="semantic_router", non_recoverable="饱和像素对应的真实信号"),
    capability("genome-track", "scientific-specialty", "Genome / sequence tracks", ["基因组轨道", "coverage track", "序列浏览图"], "restricted", "no_case", "共享坐标下的峰、区间、基因模型和标签", route="semantic_router", non_recoverable="未显示 reads 和碱基级原始数据"),
    capability("spatial-omics", "scientific-specialty", "Spatial omics / tissue embedding", ["空间转录组", "组织点阵", "空间聚类"], "coordinate_specific", "oa_reference", "组织坐标、点类别、强度和区域边界", "nature-spatial-treemap", "spatial_map", route="semantic_router", non_recoverable="表达矩阵与原始组织影像配准参数"),

    capability("multipanel", "composite", "Multi-panel routing", ["复合图", "多面板", "panel routing"], "candidate", "partial_visible", "面板边界、类型路由和逐面板证据状态", "nature-ribotie-multipanel", "marginal", route="semantic_router", non_recoverable="未处理面板的数值"),
    capability("small-multiples", "composite", "Small multiples / facet", ["小倍图", "facet", "重复面板"], "candidate", "oa_reference", "重复坐标系、面板变量、共享图例与逐面板图元", "nature-autospill-flow", "small_multiples", route="semantic_router"),
    capability("inset", "composite", "Inset / zoom panel", ["插图", "局部放大", "嵌入图"], "candidate", "oa_reference", "主图与插图边界、连接框和各自坐标系", "nature-hypergraph-roc", "network_inset", route="semantic_router"),
    capability("dual-axis", "composite", "Dual-axis / mixed scale", ["双 Y 轴", "混合尺度"], "candidate", "oa_reference", "系列到坐标轴的归属和两套校准", "nature-xenopus-polar", "errorbar", route="semantic_router"),
    capability("broken-axis", "composite", "Broken / discontinuous axis", ["断轴", "跳轴", "非连续坐标"], "candidate", "no_case", "每个连续区间的独立校准与拼接规则", route="semantic_router"),
    capability("marginal-plot", "composite", "Marginal plot", ["边际直方图", "边际密度", "joint plot"], "candidate", "oa_reference", "中心 XY 图与共享轴边际统计图", "nature-ribotie-multipanel", "marginal", route="semantic_router"),
    capability("chart-table-overlay", "composite", "Chart + table / mixed overlay", ["图表加表格", "风险表", "柱线混合", "图上注释"], "candidate", "oa_reference", "图层分解、表格 OCR、共享类别和系列归属", "nature-phf6-survival", "risk_table", route="semantic_router", non_recoverable="图例没有说明时的隐式语义"),
]


def build_crops() -> dict[str, dict[str, str]]:
    assets: dict[str, dict[str, str]] = {}
    for case in REFERENCE_CASES:
        case_id = case["id"]
        image_path = GALLERY / case["original"]
        if not image_path.exists():
            raise FileNotFoundError(image_path)
        image = Image.open(image_path).convert("RGB")
        case_assets = {}
        for key, box in CROPS.get(case_id, {}).items():
            left, top, right, bottom = box
            left = max(0, min(left, image.width - 1))
            top = max(0, min(top, image.height - 1))
            right = max(left + 1, min(right, image.width))
            bottom = max(top + 1, min(bottom, image.height))
            crop_path = image_path.parent / f"atlas-{key}.jpg"
            crop = image.crop((left, top, right, bottom))
            crop.thumbnail((720, 480), Image.Resampling.LANCZOS)
            crop.save(crop_path, quality=92, optimize=True)
            case_assets[key] = str(crop_path.relative_to(GALLERY)).replace("\\", "/")
        assets[case_id] = case_assets

        if "report" not in case:
            report_path = image_path.parent / "reference-report.json"
            write_json(
                report_path,
                {
                    "schema_version": 1,
                    "case_id": case_id,
                    "status": "oa_reference_identified",
                    "original_sha256": sha256(image_path),
                    "figure": case["figure"],
                    "doi": case["doi"],
                    "coverage": case["coverage"],
                    "scope": "Representative OA figure and panel crops only; no numeric values are accepted from this reference report.",
                    "limitations": [
                        "A routed or cropped panel is not a validated extraction.",
                        "Numeric support requires a dedicated coordinate model, calibration, overlay, and type-specific benchmark.",
                    ],
                },
            )
            case["report"] = str(report_path.relative_to(GALLERY)).replace("\\", "/")
    return assets


def main() -> None:
    crop_assets = build_crops()
    cases = []
    for case in REFERENCE_CASES:
        item = dict(case)
        item["license"] = "CC BY 4.0"
        item["licenseUrl"] = "https://creativecommons.org/licenses/by/4.0/"
        item["originalSha256"] = sha256(GALLERY / item["original"])
        item["thumbnails"] = crop_assets.get(item["id"], {})
        cases.append(item)

    case_lookup = {case["id"]: case for case in cases}
    enriched = []
    for item in CAPABILITIES:
        entry = dict(item)
        case = case_lookup.get(entry["caseId"])
        if case and entry["thumbnailKey"]:
            entry["thumbnail"] = case["thumbnails"].get(entry["thumbnailKey"], case["original"])
            entry["articleUrl"] = case["articleUrl"]
            entry["figure"] = case["figure"]
        else:
            entry["thumbnail"] = None
            entry["articleUrl"] = None
            entry["figure"] = None
        enriched.append(entry)

    payload = {
        "schemaVersion": 1,
        "generated": "2026-07-20",
        "taxonomySource": {
            "model": "digitization-layered-taxonomy",
            "primary": {
                "name": "WebPlotDigitizer axes and calibration types",
                "url": "https://automeris.io/docs/digitize/",
            },
            "secondary": {
                "name": "The R Graph Gallery chart vocabulary",
                "url": "https://r-graph-gallery.com/",
            },
            "note": "Top-level groups are designed for data recovery: calibration family plus visible mark plus scientific semantics. R Graph Gallery is vocabulary input, not the product hierarchy.",
        },
        "counts": {
            "groups": len(GROUPS),
            "types": len(enriched),
            "stableTypes": sum(item["engineStatus"] == "stable" for item in enriched),
            "wpdCalibrationFamilies": sum(item["origin"] == "WebPlotDigitizer" for item in CALIBRATION_FAMILIES),
            "extensionRoutes": sum(item["origin"] == "thu-digitizer extension" for item in CALIBRATION_FAMILIES),
            "oaRepresentatives": sum(item["demoStatus"] != "no_case" for item in enriched),
            "validatedDemos": sum(item["demoStatus"] in {"source_mapped", "visible_geometry", "partial_visible"} for item in enriched),
            "referenceFigures": len(cases),
        },
        "groups": GROUPS,
        "calibrationFamilies": CALIBRATION_FAMILIES,
        "capabilities": enriched,
        "referenceCases": cases,
        "statusDefinitions": {
            "engine": {
                "stable": "已有专用稳定提取器与回归测试",
                "candidate": "已有可执行路线或局部实现，尚未通过完整晋级门槛",
                "benchmark_only": "仅有确定性基准路线，不是稳定用户功能",
                "coordinate_specific": "需要该坐标/拓扑专用解析器，不能套用普通 XY 校准",
                "restricted": "只能恢复明确的可见表示，不能声称还原隐藏原始数据",
            },
            "demo": {
                "source_mapped": "官方源数据已映射",
                "visible_geometry": "真实图像几何已提取",
                "partial_visible": "复杂图局部提取",
                "oa_reference": "真实 OA 案例已定位，等待专用验证",
                "no_case": "尚未选定代表案例",
            },
        },
    }
    write_json(DATA / "capabilities.json", payload)
    print(
        f"gallery atlas built: {payload['counts']['groups']} groups, "
        f"{payload['counts']['types']} types, {payload['counts']['oaRepresentatives']} with OA representatives"
    )


if __name__ == "__main__":
    main()
