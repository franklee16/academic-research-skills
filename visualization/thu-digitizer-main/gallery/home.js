const typeGrid = document.querySelector("#type-grid");
const catalogCount = document.querySelector("#catalog-count");
const caseDialog = document.querySelector("#case-dialog");
const detailTitle = document.querySelector("#detail-title");
const detailKicker = document.querySelector("#detail-kicker");
const detailStatus = document.querySelector("#detail-status");
const detailDescription = document.querySelector("#detail-description");
const detailOriginalImage = document.querySelector("#detail-original-image");
const detailRecreatedImage = document.querySelector("#detail-recreated-image");
const originalSource = document.querySelector("#original-source");
const metricGrid = document.querySelector("#metric-grid");
const metricNote = document.querySelector("#metric-note");
const detailLinks = document.querySelector("#detail-links");
const rowCount = document.querySelector("#row-count");
const csvDownload = document.querySelector("#csv-download");
const dataViewport = document.querySelector("#data-table-viewport");
const dataTable = document.querySelector("#data-table");
const dataChart = document.querySelector("#data-chart");
const interactiveChart = document.querySelector("#interactive-chart");
const chartTooltip = document.querySelector("#chart-tooltip");
const ASSET_REVISION = "20260728-china-mining-contour-v01";
const interactiveReadout = document.querySelector("#interactive-readout");
const interactiveNote = document.querySelector("#interactive-note");
const interactiveTitle = document.querySelector("#interactive-title");
const styleFidelity = document.querySelector("#style-fidelity");

const SVG_NS = "http://www.w3.org/2000/svg";
const CHART_WIDTH = 920;
const CHART_HEIGHT = 500;
const PLOT = { left: 78, right: 28, top: 28, bottom: 62 };

// Source and target rectangles use their respective native raster canvases.
// These bounds were retained with the paper-case extraction evidence so the
// comparison view aligns plotted axes, rather than merely aligning outer cards.
const comparisonAxisBounds = {
  "nature-00142-fig3a": { source: [176, 63, 945, 252], target: [176, 63, 945, 252] },
  "nature-00142-fig4a": { source: [88, 39, 408, 223], target: [88, 39, 408, 223] },
  "nature-02571-fig1d": { source: [103, 45, 591, 265], target: [103, 45, 591, 265] },
  "nature-63786-fig1c": { source: [96, 52, 728, 430], target: [108, 14, 588, 518] },
  "nature-21043-fig6a": { source: [300, 38, 1010, 390], target: [347, 5, 1096, 296] },
};

const familyById = {
  line: "scatter",
  scatter: "scatter",
  "dose-response": "scatter",
  bar: "bar",
  "grouped-bar-dot": "bar",
  "bar-horizontal": "bar",
  "bar-stacked": "bar",
  "bar-percent-stacked": "bar",
  pie: "other",
  forest: "bar",
  histogram: "distribution",
  boxplot: "distribution",
  "boxplot-horizontal": "distribution",
  heatmap: "matrix",
  "nature-21043-fig6a": "matrix",
  "nature-00142-fig3a": "scatter",
  "nature-00142-fig4a": "scatter",
  "nature-02571-fig1d": "scatter",
  "nature-19006-fig2b": "matrix",
  "nature-63786-fig1c": "bar",
  "nature-67353-fig1": "distribution",
  "nature-62086-fig5": "scatter",
  "nature-28348-fig6": "bar",
  "nature-28348-fig7": "matrix",
  "nature-27341-fig1": "matrix",
  "nature-70099-fig5e": "scatter",
  "nature-37200-fig8e": "bar",
  "nature-31408-fig2d": "matrix",
  "nature-06199-fig1": "matrix",
  "nature-60895-fig4c": "bar",
  "nature-20563-fig6f": "distribution",
  "nature-51329-fig5a": "spatial",
};

const familyLabels = {
  spatial: "\u7a7a\u95f4\u70b9\u4f4d\u56fe",
  scatter: "\u6563\u70b9\u56fe",
  bar: "\u67f1\u72b6\u56fe",
  distribution: "\u5206\u5e03\u56fe",
  matrix: "\u77e9\u9635\u4e0e\u590d\u5408\u56fe",
  other: "\u5176\u4ed6",
};

const familyOrder = ["scatter", "spatial", "map", "bar", "distribution", "matrix", "other"];

familyById["nature-56055-fig3c"] = "scatter";
familyById["china-mining-gakedaban-dt-300m"] = "map";
familyLabels.map = "\u7a7a\u95f4\u573a / \u7b49\u503c\u56fe";

// The gallery is an index of extraction grammars, not an article bibliography.
// Paper title/figure provenance stays directly beneath the original image.
const typeNameById = {
  line: "\u65f6\u95f4\u5e8f\u5217\u56fe",
  scatter: "散点图",
  "dose-response": "剂量—反应曲线",
  bar: "双轴柱形折线图",
  "grouped-bar-dot": "柱状图与散点",
  "bar-horizontal": "水平柱状图",
  "bar-stacked": "堆叠柱状图",
  "bar-percent-stacked": "堆叠柱状图",
  pie: "环形饼图",
  histogram: "直方图",
  heatmap: "热力图",
  boxplot: "箱线图",
  "boxplot-horizontal": "横向箱线图",
  forest: "森林图",
  "nature-21043-fig6a": "气泡矩阵",
  "nature-00142-fig3a": "\u65f6\u95f4\u5e8f\u5217\u56fe",
  "nature-00142-fig4a": "\u65f6\u95f4\u5e8f\u5217\u56fe",
  "nature-02571-fig1d": "\u65f6\u95f4\u5e8f\u5217\u56fe",
  "nature-19006-fig2b": "UpSet 复合图",
  "nature-63786-fig1c": "分组柱状图",
  "nature-67353-fig1": "\u591a\u9762\u677f\u7bb1\u7ebf\u56fe",
  "nature-62086-fig5": "\u6298\u7ebf\u56fe",
  "nature-28348-fig6": "\u6c34\u5e73\u67f1\u5f62\u56fe",
  "nature-28348-fig7": "UpSet \u590d\u5408\u56fe",
  "nature-27341-fig1": "UpSet \u590d\u5408\u56fe",
  "nature-70099-fig5e": "\u6563\u70b9\u56fe",
  "nature-37200-fig8e": "\u5206\u7ec4\u67f1\u5f62\u56fe",
  "nature-31408-fig2d": "\u70ed\u529b\u56fe",
  "nature-06199-fig1": "\u70ed\u529b\u56fe",
  "nature-60895-fig4c": "\u5806\u53e0\u67f1\u72b6\u56fe",
  "nature-20563-fig6f": "极坐标直方图",
};

Object.assign(typeNameById, {
  line: "\u6563\u70b9\u6298\u7ebf\u56fe",
  "nature-00142-fig3a": "\u6563\u70b9\u6298\u7ebf\u56fe",
  "nature-02571-fig1d": "\u591a\u5e8f\u5217\u6563\u70b9\u6298\u7ebf\u56fe",
  "nature-56055-fig3c": "\u591a\u9762\u677f\u6563\u70b9\u6298\u7ebf\u56fe",
  "china-mining-gakedaban-dt-300m": "\u586b\u8272\u7b49\u503c\u7ebf\u5730\u56fe",
});

const seriesColors = {
  red: "#cf5449",
  gray: "#9b9f9f",
  blue: "#376fc1",
  green: "#468967",
  ADR: "#7b4b88",
  NA: "#28796f",
  DA: "#c75849",
  CER: "#da6848",
  TCX: "#2777b5",
  Retrain: "#ffffff",
  Finetune: "#3154c7",
};

const viewLabels = {
  original: "原图",
  overlay: "提取覆盖",
  recreated: "复现",
};

let samples = [];
let activeSample = null;
let currentTable = { headers: [], rows: [] };

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function statusTone(status) {
  if (["candidate", "visible_geometry_candidate", "partial_visible", "low_confidence"].includes(status)) return "geometry";
  if (status === "visible_geometry_extracted") return "geometry";
  return "stable";
}

function publicStatusLabel(status) {
  const labels = {
    validated_local_stable: "已完成基准核验",
    candidate: "可见几何提取",
    visible_geometry_candidate: "可见几何提取",
    visible_geometry_extracted: "可见几何提取",
    partial_visible: "部分可见提取",
    low_confidence: "低置信候选",
  };
  return labels[status] || "提取结果";
}

function displayType(sample) {
  return typeNameById[sample.id] || sample.subtitle || "图表";
}

function displayFamily(sample) {
  return familyLabels[familyById[sample.id] || "other"] || familyLabels.other;
}

function cardCaption(sample) {
  if (sample.journal && sample.figure) return `${sample.journal} · ${sample.figure}`;
  return sample.subtitle || "";
}

function renderCards(items) {
  const groups = new Map();
  items.forEach((sample) => {
    const family = familyById[sample.id] || "other";
    if (!groups.has(family)) groups.set(family, []);
    groups.get(family).push(sample);
  });
  let cardIndex = 0;
  typeGrid.innerHTML = Array.from(groups.entries())
    .sort(([left], [right]) => familyOrder.indexOf(left) - familyOrder.indexOf(right))
    .map(([family, groupItems]) => {
      const cards = groupItems
        .map((sample) => {
          cardIndex += 1;
          return `
        <button
          class="type-card"
          id="basic-${escapeHtml(sample.id)}"
          type="button"
          data-case-id="${escapeHtml(sample.id)}"
          data-family="${escapeHtml(familyById[sample.id] || "other")}"
          aria-label="查看${escapeHtml(displayType(sample))}提取详情"
        >
          <span class="card-number">${String(cardIndex).padStart(2, "0")}</span>
          <span class="card-image">
            <img src="${escapeHtml(sample.assets.original)}" alt="${escapeHtml(displayType(sample))}原图" loading="lazy" />
          </span>
          <span class="card-meta">
            <span>
              <h3>${escapeHtml(displayType(sample))}</h3>
              <p>${escapeHtml(cardCaption(sample))}</p>
            </span>
            <span class="status-dot ${statusTone(sample.status)}">${escapeHtml(publicStatusLabel(sample.status))}</span>
          </span>
        </button>`;
        })
        .join("");
      return `
        <section class="type-group" data-type-group="${escapeHtml(family)}" aria-labelledby="type-group-${escapeHtml(groupItems[0].id)}">
          <h3 class="type-group-title" id="type-group-${escapeHtml(groupItems[0].id)}">${escapeHtml(familyLabels[family] || familyLabels.other)}</h3>
          <div class="type-group-grid">${cards}</div>
        </section>`;
    })
    .join("");
}

function applyFilter(filter) {
  let visible = 0;
  document.querySelectorAll(".type-card").forEach((card) => {
    const show = filter === "all" || card.dataset.family === filter;
    card.hidden = !show;
    if (show) visible += 1;
  });
  document.querySelectorAll(".type-group").forEach((group) => {
    group.hidden = !group.querySelector(".type-card:not([hidden])");
  });
  catalogCount.textContent = `${visible} 个案例`;
}

function setImageView(view) {
  if (!activeSample) return;
  document.querySelectorAll(".view-tab").forEach((button) => {
    const selected = button.dataset.view === view;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-selected", String(selected));
  });
  detailOriginalImage.src = assetUrl(activeSample.assets[view]);
  detailOriginalImage.alt = `${displayType(activeSample)} — ${viewLabels[view]}`;
  detailRecreatedImage.src = assetUrl(activeSample.assets.recreated);
  detailRecreatedImage.alt = `${displayType(activeSample)} — ${viewLabels.recreated}`;
}

function setRecreationView(view) {
  if (!activeSample) return;
  const interactive = view === "interactive" && Boolean(activeSample.styleSpec);
  document.querySelectorAll(".recreation-tab").forEach((button) => {
    const selected = interactive ? button.dataset.recreationView === "interactive" : button.dataset.recreationView === "recreated";
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-selected", String(selected));
  });
  detailRecreatedImage.hidden = interactive;
  interactiveChart.hidden = !interactive;
  interactiveReadout.hidden = !interactive;
  interactiveTitle.textContent = interactive ? "交互式图" : "复现";
  chartTooltip.classList.remove("is-visible");
}

function detailLink(label, href, options = {}) {
  const attrs = [
    `href="${escapeHtml(href)}"`,
    options.download ? "download" : 'target="_blank" rel="noreferrer"',
  ].join(" ");
  return `<a ${attrs}>${escapeHtml(label)}</a>`;
}

function updateOriginalSource(sample) {
  const sourceUrl = sample.figureUrl || sample.articleUrl;
  const citation = [sample.journal, sample.articleTitle, sample.figure].filter(Boolean).join(" · ");
  if (!sourceUrl || !citation) {
    originalSource.hidden = true;
    originalSource.removeAttribute("href");
    originalSource.textContent = "";
    return;
  }
  originalSource.hidden = false;
  originalSource.href = sourceUrl;
  originalSource.textContent = citation;
  originalSource.title = "在论文原页查看原图";
}

async function openCase(sample, updateHash = true) {
  activeSample = sample;
  detailKicker.textContent = `${displayFamily(sample)} / ${publicStatusLabel(sample.status)}`;
  detailTitle.textContent = displayType(sample);
  detailStatus.innerHTML = `<span class="status-dot ${statusTone(sample.status)}">${escapeHtml(publicStatusLabel(sample.status))}</span>`;
  detailDescription.textContent = sample.description;
  updateOriginalSource(sample);
  metricGrid.innerHTML = (sample.metrics || [])
    .map(
      (metric) => `
        <div class="metric">
          <span>${escapeHtml(metric.label)}</span>
          <strong>${escapeHtml(metric.value)}</strong>
        </div>`,
    )
    .join("");
  metricNote.textContent = sample.metricNote || (sample.articleUrl
    ? "精度只在已完成官方源数据或独立矢量几何映射的对应点上报告。"
    : "精度来自确定性合成真值；它不等同于真实论文图上的泛化精度。");
  detailLinks.innerHTML = [
    detailLink("完整报告 ↗", sample.assets.report),
    sample.articleUrl ? detailLink("论文原文 ↗", sample.articleUrl) : "",
    sample.figureUrl ? detailLink(`${sample.figure || "图"} ↗`, sample.figureUrl) : "",
    sample.validationDataUrl ? detailLink("验证数据 ↗", sample.validationDataUrl) : "",
  ].join("");
  csvDownload.href = sample.assets.data;
  const hasStyleSpec = Boolean(sample.styleSpec);
  document.querySelector('[data-recreation-view="interactive"]').hidden = !hasStyleSpec;
  styleFidelity.textContent = sample.styleSpec?.label || "独立数据重绘";
  styleFidelity.classList.toggle("is-evidence", hasStyleSpec);
  interactiveChart.classList.toggle("has-paper-style", hasStyleSpec);
  interactiveChart.dataset.styleMode = hasStyleSpec ? "evidence-backed" : "data-redraw";
  interactiveChart.dataset.renderer = sample.styleSpec?.renderer || sample.id;
  styleFidelity.title = hasStyleSpec
    ? "样式参数来自原图像素或官方 PDF 矢量几何证据"
    : "只保证提取数值和图形语义，图形样式为独立重绘";
  interactiveNote.textContent = sample.styleSpec?.note || "这是基于提取数据生成的独立交互图，不声称逐像素复现论文原图样式。";
  setImageView("original");
  setRecreationView("recreated");
  const originalImageReady = waitForImage(detailOriginalImage);
  dataTable.innerHTML = "<tbody><tr><td>正在装入 CSV…</td></tr></tbody>";
  rowCount.textContent = "loading";
  clearChart("正在装入提取数据…");

  if (!caseDialog.open) caseDialog.showModal();
  if (updateHash && location.hash !== `#basic-${sample.id}`) {
    history.pushState({ caseId: sample.id }, "", `#basic-${sample.id}`);
  }

  try {
    const layerEntries = Object.entries(sample.interactiveLayers || {});
    const geometryPath = sample.styleSpec?.geometryAsset;
    const [parsed, loadedLayers, geometry] = await Promise.all([
      fetchCsv(sample.assets.data),
      Promise.all(layerEntries.map(async ([name, path]) => [name, await fetchCsv(path)])),
      geometryPath ? fetchJson(geometryPath) : Promise.resolve(null),
      originalImageReady,
    ]);
    if (activeSample?.id !== sample.id) return;
    if (geometry) sample.styleSpec = { ...sample.styleSpec, ...geometry };
    currentTable = parsed;
    renderTable(parsed);
    renderInteractiveChart(sample, parsed, Object.fromEntries(loadedLayers));
    applyComparisonAlignment(sample);
  } catch (error) {
    dataTable.innerHTML = `<tbody><tr><td>CSV 载入失败：${escapeHtml(error.message)}</td></tr></tbody>`;
    rowCount.textContent = "0 rows";
    clearChart(`交互图载入失败：${error.message}`);
  }
}

async function fetchCsv(path) {
  const response = await fetch(assetUrl(path), { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return parseCsv(await response.text());
}

async function fetchJson(path) {
  const response = await fetch(assetUrl(path), { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

function assetUrl(path) {
  if (!path) return "";
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}v=${ASSET_REVISION}`;
}

function closeCase(updateHash = true) {
  if (caseDialog.open) caseDialog.close();
  activeSample = null;
  if (updateHash && location.hash.startsWith("#basic-")) {
    history.pushState({}, "", `${location.pathname}${location.search}`);
  }
}

function parseCsv(text) {
  const source = text.startsWith("\uFEFF") ? text.slice(1) : text;
  const matrix = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    if (quoted) {
      if (char === '"' && source[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field.replace(/\r$/, ""));
      matrix.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    matrix.push(row);
  }

  const headers = matrix.shift() || [];
  const rows = matrix
    .filter((values) => values.some((value) => value !== ""))
    .map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])));
  return { headers, rows };
}

function renderTable(table) {
  rowCount.textContent = `${table.rows.length} rows`;
  dataTable.innerHTML = `
    <thead><tr>${table.headers.map((header) => `<th scope="col">${escapeHtml(header)}</th>`).join("")}</tr></thead>
    <tbody>
      ${table.rows
        .map(
          (row) => `<tr>${table.headers
            .map((header) => `<td title="${escapeHtml(row[header] || "—")}">${escapeHtml(row[header] || "—")}</td>`)
            .join("")}</tr>`,
        )
        .join("")}
    </tbody>`;
  dataViewport.scrollTo({ top: 0, left: 0 });
}

function number(value) {
  if (value === null || value === undefined || String(value).trim() === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function unique(values) {
  return [...new Set(values)];
}

function extent(values, includeZero = false) {
  const finite = values.filter(Number.isFinite);
  let low = Math.min(...finite);
  let high = Math.max(...finite);
  if (includeZero) {
    low = Math.min(0, low);
    high = Math.max(0, high);
  }
  if (!Number.isFinite(low) || !Number.isFinite(high)) return [0, 1];
  if (low === high) {
    const delta = Math.abs(low || 1) * 0.1;
    return [low - delta, high + delta];
  }
  const pad = (high - low) * 0.06;
  return [low - pad, high + pad];
}

function svgElement(name, attributes = {}, text = null) {
  const element = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => {
    if (value !== null && value !== undefined) element.setAttribute(key, String(value));
  });
  if (text !== null) element.textContent = text;
  return element;
}

function appendSvg(name, attributes = {}, text = null, parent = dataChart) {
  const element = svgElement(name, attributes, text);
  parent.append(element);
  return element;
}

function makeMark(name, attributes, tooltip) {
  const { tabindex = 0, ...markAttributes } = attributes;
  const mark = appendSvg(name, {
    ...markAttributes,
    "pointer-events": markAttributes["pointer-events"] || "all",
    tabindex,
    role: "img",
    "aria-label": tooltip.replaceAll("\n", "，"),
  });
  mark.dataset.tooltip = tooltip;
  mark.addEventListener("pointerenter", (event) => showTooltip(mark, event.clientX, event.clientY));
  mark.addEventListener("pointermove", (event) => showTooltip(mark, event.clientX, event.clientY));
  mark.addEventListener("pointerleave", () => chartTooltip.classList.remove("is-visible"));
  return mark;
}

function clearChart(message = "") {
  dataChart.replaceChildren();
  setChartCanvas(CHART_WIDTH, CHART_HEIGHT);
  dataChart.style.removeProperty("font-family");
  dataChart.setAttribute("aria-label", message || "提取数据交互图");
  if (message) {
    appendSvg("text", { x: 460, y: 250, "text-anchor": "middle", class: "axis-label" }, message);
  }
  chartTooltip.classList.remove("is-visible");
  interactiveReadout.textContent = "\u79fb\u52a8\u5230\u6570\u636e\u6807\u8bb0\uff0c\u67e5\u770b\u7cbe\u786e\u63d0\u53d6\u503c";
}

function setChartCanvas(width, height, fontFamily = "") {
  dataChart.setAttribute("viewBox", `0 0 ${width} ${height}`);
  dataChart.setAttribute("preserveAspectRatio", "xMidYMid meet");
  if (fontFamily) dataChart.style.fontFamily = fontFamily;
}

function waitForImage(image) {
  if (image.complete && image.naturalWidth && image.naturalHeight) return Promise.resolve();
  return new Promise((resolve) => {
    image.addEventListener("load", resolve, { once: true });
    image.addEventListener("error", resolve, { once: true });
  });
}

function chartViewBox() {
  const values = (dataChart.getAttribute("viewBox") || `0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`)
    .trim()
    .split(/\s+/)
    .map(Number);
  return { width: values[2], height: values[3] };
}

function applyComparisonAlignment(sample) {
  const targetWidth = detailOriginalImage.naturalWidth;
  const targetHeight = detailOriginalImage.naturalHeight;
  if (!targetWidth || !targetHeight || !dataChart.childElementCount) return;

  const { width: sourceWidth, height: sourceHeight } = chartViewBox();
  const bounds = comparisonAxisBounds[sample.id];
  const [sourceLeft, sourceTop, sourceRight, sourceBottom] = bounds?.source || [0, 0, sourceWidth, sourceHeight];
  const [targetLeft, targetTop, targetRight, targetBottom] = bounds?.target || [0, 0, targetWidth, targetHeight];
  const scaleX = (targetRight - targetLeft) / (sourceRight - sourceLeft);
  const scaleY = (targetBottom - targetTop) / (sourceBottom - sourceTop);
  const offsetX = targetLeft - sourceLeft * scaleX;
  const offsetY = targetTop - sourceTop * scaleY;
  const group = svgElement("g", {
    transform: `matrix(${scaleX} 0 0 ${scaleY} ${offsetX} ${offsetY})`,
  });

  Array.from(dataChart.children).forEach((element) => group.append(element));
  dataChart.append(group);
  dataChart.setAttribute("viewBox", `0 0 ${targetWidth} ${targetHeight}`);
  dataChart.dataset.comparisonAlignment = bounds ? "axis-aligned" : "canvas-aligned";
}

function tickLabel(value) {
  if (Math.abs(value) >= 10000) return value.toExponential(1);
  if (Math.abs(value) >= 100) return value.toFixed(0);
  if (Math.abs(value) >= 10) return value.toFixed(1).replace(/\.0$/, "");
  return value.toFixed(2).replace(/0+$/, "").replace(/\.$/, "");
}

function numericFrame(xRange, yRange, options = {}) {
  const [xMin, xMax] = xRange;
  const [yMin, yMax] = yRange;
  const plotWidth = CHART_WIDTH - PLOT.left - PLOT.right;
  const plotHeight = CHART_HEIGHT - PLOT.top - PLOT.bottom;
  const x = (value) => PLOT.left + ((value - xMin) / (xMax - xMin || 1)) * plotWidth;
  const y = (value) => PLOT.top + ((yMax - value) / (yMax - yMin || 1)) * plotHeight;

  if (options.numericY !== false) {
    for (let index = 0; index <= 5; index += 1) {
      const value = yMin + ((yMax - yMin) * index) / 5;
      const py = y(value);
      appendSvg("line", { x1: PLOT.left, y1: py, x2: CHART_WIDTH - PLOT.right, y2: py, class: "grid-line" });
      appendSvg("text", { x: PLOT.left - 10, y: py + 3, "text-anchor": "end", class: "axis-label" }, tickLabel(value));
    }
  }
  if (options.numericX !== false) {
    for (let index = 0; index <= 5; index += 1) {
      const value = xMin + ((xMax - xMin) * index) / 5;
      const px = x(value);
      appendSvg("line", { x1: px, y1: PLOT.top, x2: px, y2: CHART_HEIGHT - PLOT.bottom, class: "grid-line" });
      appendSvg("text", { x: px, y: CHART_HEIGHT - PLOT.bottom + 19, "text-anchor": "middle", class: "axis-label" }, tickLabel(value));
    }
  }
  appendSvg("line", { x1: PLOT.left, y1: PLOT.top, x2: PLOT.left, y2: CHART_HEIGHT - PLOT.bottom, class: "axis-line" });
  appendSvg("line", { x1: PLOT.left, y1: CHART_HEIGHT - PLOT.bottom, x2: CHART_WIDTH - PLOT.right, y2: CHART_HEIGHT - PLOT.bottom, class: "axis-line" });
  return { x, y, plotWidth, plotHeight, xMin, xMax, yMin, yMax };
}

function addLegend(labels) {
  let x = PLOT.left;
  labels.forEach((label) => {
    appendSvg("circle", { cx: x + 5, cy: 13, r: 4, fill: seriesColors[label] || "#555" });
    appendSvg("text", { x: x + 14, y: 16, class: "legend-label" }, label);
    x += Math.max(72, label.length * 8 + 34);
  });
}

function exactTooltip(entries) {
  return entries
    .filter(([, value]) => value !== "" && value !== null && value !== undefined)
    .map(([label, value]) => `${label}: ${value}`)
    .join("\n");
}

function renderLineChart(table) {
  const series = table.headers.filter((header) => !["x", "x_pixel"].includes(header));
  const values = table.rows.flatMap((row) => series.map((name) => number(row[name])).filter(Number.isFinite));
  const frame = numericFrame(extent(table.rows.map((row) => number(row.x))), extent(values));
  addLegend(series);
  series.forEach((name) => {
    const points = table.rows
      .map((row) => ({ row, x: number(row.x), y: number(row[name]) }))
      .filter((point) => point.x !== null && point.y !== null);
    const path = points.map((point, index) => `${index ? "L" : "M"}${frame.x(point.x)},${frame.y(point.y)}`).join(" ");
    appendSvg("path", { d: path, fill: "none", stroke: seriesColors[name] || "#333", "stroke-width": 2.4 });
    points.forEach((point) => {
      makeMark(
        "circle",
        { cx: frame.x(point.x), cy: frame.y(point.y), r: 4.6, fill: seriesColors[name] || "#333", stroke: "#fff", "stroke-width": 1 },
        exactTooltip([["系列", name], ["x", point.row.x], ["y", point.row[name]]]),
      );
    });
  });
  interactiveNote.textContent = "按提取采样点连接的交互数据图；误差线若未进入 CSV，不在此补画。";
}

function renderScatterChart(table) {
  const xs = table.rows.map((row) => number(row.x));
  const ys = table.rows.map((row) => number(row.y));
  const frame = numericFrame(extent(xs), extent(ys));
  const series = unique(table.rows.map((row) => row.series));
  addLegend(series);
  table.rows.forEach((row) => {
    const x = number(row.x);
    const y = number(row.y);
    if (x === null || y === null) return;
    makeMark(
      "circle",
      { cx: frame.x(x), cy: frame.y(y), r: 5, fill: seriesColors[row.series] || "#444", opacity: 0.92 },
      exactTooltip([["系列", row.series], ["x", row.x], ["y", row.y]]),
    );
  });
  interactiveNote.textContent = "每个交互点对应 CSV 中一个可分离的可见标记。";
}

function renderDoseResponse(table) {
  const rows = table.rows.filter((row) => row.segment === "main" && number(row.log10_molar) !== null && number(row.digitized_value) !== null);
  const frame = numericFrame(extent(rows.map((row) => number(row.log10_molar))), extent(rows.map((row) => number(row.digitized_value)), true));
  const series = unique(rows.map((row) => row.series));
  addLegend(series);
  series.forEach((name) => {
    const points = rows.filter((row) => row.series === name).sort((a, b) => number(a.log10_molar) - number(b.log10_molar));
    appendSvg("path", {
      d: points.map((row, index) => `${index ? "L" : "M"}${frame.x(number(row.log10_molar))},${frame.y(number(row.digitized_value))}`).join(" "),
      fill: "none",
      stroke: seriesColors[name] || "#333",
      "stroke-width": 1.5,
      "stroke-dasharray": "4 4",
      opacity: 0.72,
    });
    points.forEach((row) => {
      const x = frame.x(number(row.log10_molar));
      const y = frame.y(number(row.digitized_value));
      const lower = number(row.digitized_error_lower);
      const upper = number(row.digitized_error_upper);
      if (lower !== null && upper !== null) {
        appendSvg("line", { x1: x, y1: frame.y(lower), x2: x, y2: frame.y(upper), stroke: seriesColors[name] || "#333", "stroke-width": 1 });
      }
      makeMark(
        "circle",
        { cx: x, cy: y, r: 5, fill: seriesColors[name] || "#333", stroke: "#fff", "stroke-width": 1 },
        exactTooltip([
          ["系列", name],
          ["log10(M)", row.log10_molar],
          ["提取值", row.digitized_value],
          ["误差下端", row.digitized_error_lower],
          ["误差上端", row.digitized_error_upper],
        ]),
      );
    });
  });
  interactiveNote.textContent = "虚线只连接提取点，不是作者拟合曲线；断轴上的 vehicle 点未强行映射到浓度轴。";
}

function addCategoryLabels(categories, xPosition, y = CHART_HEIGHT - PLOT.bottom + 22, rotate = false) {
  categories.forEach((category, index) => {
    const x = xPosition(index);
    const attributes = { x, y, "text-anchor": rotate ? "end" : "middle", class: "axis-label" };
    if (rotate) attributes.transform = `rotate(-35 ${x} ${y})`;
    appendSvg("text", attributes, category.length > 18 ? `${category.slice(0, 16)}…` : category);
  });
}

function renderVerticalBars(table, stacked = false) {
  const valueKey = table.headers.includes("value") ? "value" : "extracted_value";
  const rows = table.rows.filter((row) => number(row[valueKey]) !== null);
  const categories = unique(rows.map((row) => row.category));
  const series = unique(rows.map((row) => row.series));
  const totals = categories.map((category) => rows.filter((row) => row.category === category).reduce((sum, row) => sum + number(row[valueKey]), 0));
  const rawValues = rows.map((row) => number(row[valueKey]));
  const yRange = extent(stacked ? totals : rawValues, true);
  const frame = numericFrame([0, categories.length], yRange, { numericX: false });
  const categoryWidth = frame.plotWidth / categories.length;
  addLegend(series);

  categories.forEach((category, categoryIndex) => {
    const categoryRows = rows.filter((row) => row.category === category);
    if (stacked) {
      let cumulative = 0;
      categoryRows.forEach((row) => {
        const value = number(row[valueKey]);
        const x = PLOT.left + categoryIndex * categoryWidth + categoryWidth * 0.2;
        const width = categoryWidth * 0.6;
        const top = frame.y(cumulative + value);
        const bottom = frame.y(cumulative);
        makeMark(
          "rect",
          { x, y: Math.min(top, bottom), width, height: Math.max(1, Math.abs(bottom - top)), fill: seriesColors[row.series] || "#555" },
          exactTooltip([["类别", category], ["系列", row.series], ["提取值", row[valueKey]], ["状态", row.status || row.mark_status]]),
        );
        cumulative += value;
      });
    } else {
      const groupWidth = categoryWidth * 0.76;
      const barWidth = groupWidth / Math.max(series.length, 1);
      categoryRows.forEach((row) => {
        const seriesIndex = series.indexOf(row.series);
        const value = number(row[valueKey]);
        const zero = frame.y(0);
        const valueY = frame.y(value);
        const x = PLOT.left + categoryIndex * categoryWidth + categoryWidth * 0.12 + seriesIndex * barWidth;
        makeMark(
          "rect",
          { x, y: Math.min(zero, valueY), width: Math.max(2, barWidth - 2), height: Math.max(1, Math.abs(zero - valueY)), fill: seriesColors[row.series] || "#555" },
          exactTooltip([["类别", category], ["系列", row.series], ["提取值", row[valueKey]], ["置信度", row.confidence]]),
        );
      });
    }
  });
  addCategoryLabels(categories, (index) => PLOT.left + (index + 0.5) * categoryWidth, undefined, categories.length > 7);
  interactiveNote.textContent = stacked
    ? "每个色段直接对应 CSV 中的可见分段值；这里没有反推段内原始记录。"
    : "柱高按提取值独立绘制；配色用于区分系列，不声称逐像素复制论文样式。";
}

function renderHorizontalBars(table, percent = false) {
  const valueKey = percent ? "extracted_value" : "value";
  const rows = table.rows.filter((row) => number(row[valueKey]) !== null);
  const categories = unique(rows.map((row) => row.category));
  const series = unique(rows.map((row) => row.series));
  const values = rows.map((row) => number(row[valueKey]));
  const xRange = percent ? [0, 100] : extent(values, true);
  const frame = numericFrame(xRange, [0, categories.length], { numericX: true, numericY: false });
  addLegend(series);
  const rowHeight = frame.plotHeight / categories.length;

  categories.forEach((category, categoryIndex) => {
    const categoryRows = rows.filter((row) => row.category === category);
    if (percent) {
      let cumulative = 0;
      categoryRows.forEach((row) => {
        const value = number(row[valueKey]);
        const left = frame.x(cumulative);
        const right = frame.x(cumulative + value);
        const y = PLOT.top + categoryIndex * rowHeight + rowHeight * 0.2;
        makeMark(
          "rect",
          { x: left, y, width: Math.max(1, right - left), height: rowHeight * 0.6, fill: seriesColors[row.series] || "#555" },
          exactTooltip([["类别", category], ["系列", row.series], ["提取比例", row[valueKey]], ["真值", row.truth_value]]),
        );
        cumulative += value;
      });
    } else {
      const barHeight = rowHeight * 0.72 / series.length;
      categoryRows.forEach((row) => {
        const seriesIndex = series.indexOf(row.series);
        const value = number(row[valueKey]);
        const zero = frame.x(0);
        const valueX = frame.x(value);
        const y = PLOT.top + categoryIndex * rowHeight + rowHeight * 0.14 + seriesIndex * barHeight;
        makeMark(
          "rect",
          { x: Math.min(zero, valueX), y, width: Math.max(1, Math.abs(valueX - zero)), height: Math.max(2, barHeight - 2), fill: seriesColors[row.series] || "#555" },
          exactTooltip([["类别", category], ["系列", row.series], ["提取值", row[valueKey]], ["误差下端", row.error_lower], ["误差上端", row.error_upper]]),
        );
      });
    }
    appendSvg("text", { x: PLOT.left - 10, y: PLOT.top + (categoryIndex + 0.52) * rowHeight, "text-anchor": "end", class: "axis-label" }, category);
  });
  interactiveNote.textContent = percent
    ? "各色段按提取比例绘制；悬停同时显示提取值和合成真值。"
    : "横向柱从零基线绘制，负值与正值保留方向。";
}

function renderHistogram(table) {
  const rows = table.rows.filter((row) => number(row.x_left) !== null && number(row.x_right) !== null && number(row.height) !== null);
  const frame = numericFrame(
    extent(rows.flatMap((row) => [number(row.x_left), number(row.x_right)])),
    extent(rows.map((row) => number(row.height)), true),
  );
  rows.forEach((row) => {
    const left = frame.x(number(row.x_left));
    const right = frame.x(number(row.x_right));
    const top = frame.y(number(row.height));
    const bottom = frame.y(0);
    makeMark(
      "rect",
      { x: left, y: top, width: Math.max(1, right - left), height: bottom - top, fill: "#548e87", opacity: 0.86, stroke: "#fff", "stroke-width": 1 },
      exactTooltip([["箱", row.bin], ["左边界", row.x_left], ["右边界", row.x_right], ["高度", row.height]]),
    );
  });
  interactiveNote.textContent = "交互矩形表示可见箱边界与箱高，不代表箱内原始观测。";
}

function renderHeatmap(table) {
  clearChart();
  const rows = unique(table.rows.map((row) => row.embedding));
  const columns = unique(table.rows.map((row) => row.biomarker));
  const margin = { left: 108, right: 22, top: 22, bottom: 96 };
  const width = CHART_WIDTH - margin.left - margin.right;
  const height = CHART_HEIGHT - margin.top - margin.bottom;
  const cellWidth = width / columns.length;
  const cellHeight = height / rows.length;
  table.rows.forEach((row) => {
    const rowIndex = rows.indexOf(row.embedding);
    const columnIndex = columns.indexOf(row.biomarker);
    const fill = row.fill_rgb ? `rgb(${row.fill_rgb})` : "#ddd";
    makeMark(
      "rect",
      {
        x: margin.left + columnIndex * cellWidth,
        y: margin.top + rowIndex * cellHeight,
        width: cellWidth + 0.25,
        height: cellHeight + 0.25,
        fill,
      },
      exactTooltip([
        ["行", row.embedding],
        ["列", row.biomarker],
        ["提取相关值", row.digitized_correlation],
        ["值状态", row.value_status],
        ["区间", row.value_interval],
        ["可见显著性", row.significant_visible],
      ]),
    );
  });
  rows.forEach((label, index) => {
    if (rows.length > 24 && index % 2) return;
    appendSvg("text", { x: margin.left - 7, y: margin.top + (index + 0.72) * cellHeight, "text-anchor": "end", class: "axis-label" }, label);
  });
  columns.forEach((label, index) => {
    const x = margin.left + (index + 0.5) * cellWidth;
    const y = CHART_HEIGHT - margin.bottom + 8;
    appendSvg("text", { x, y, transform: `rotate(-55 ${x} ${y})`, "text-anchor": "end", class: "axis-label" }, label);
  });
  dataChart.setAttribute("aria-label", "热力图提取数据交互视图");
  interactiveNote.textContent = "色块来自提取颜色；端点色单元格仍按区间截尾解释，悬停可查看 value_status。";
}

function parseOutliers(value) {
  return String(value || "")
    .split(/[;|]/)
    .map((item) => item.trim())
    .filter(Boolean)
    .map(number)
    .filter(Number.isFinite);
}

function renderVerticalBoxplot(table) {
  const rows = table.rows.filter((row) => number(row.median) !== null);
  const labels = rows.map((row) => [row.panel, row.category, row.series].filter(Boolean).join(" · "));
  const allValues = rows.flatMap((row) => [row.lower_whisker, row.q1, row.median, row.q3, row.upper_whisker].map(number));
  const frame = numericFrame([0, rows.length], extent(allValues), { numericX: false });
  const slot = frame.plotWidth / rows.length;
  addLegend(unique(rows.map((row) => row.series).filter(Boolean)));
  rows.forEach((row, index) => {
    const center = PLOT.left + (index + 0.5) * slot;
    const boxWidth = Math.max(5, slot * 0.58);
    const lower = frame.y(number(row.lower_whisker));
    const upper = frame.y(number(row.upper_whisker));
    const q1 = frame.y(number(row.q1));
    const q3 = frame.y(number(row.q3));
    const median = frame.y(number(row.median));
    const color = seriesColors[row.series] || "#71898b";
    const tooltip = exactTooltip([
      ["组", labels[index]],
      ["下须", row.lower_whisker],
      ["Q1", row.q1],
      ["中位数", row.median],
      ["Q3", row.q3],
      ["上须", row.upper_whisker],
      ["可见离群点", row.visible_outliers],
    ]);
    appendSvg("line", { x1: center, y1: upper, x2: center, y2: lower, stroke: "#222", "stroke-width": 1.2 });
    makeMark(
      "rect",
      { x: center - boxWidth / 2, y: Math.min(q1, q3), width: boxWidth, height: Math.max(2, Math.abs(q1 - q3)), fill: color, "fill-opacity": row.series === "Retrain" ? 0.08 : 0.68, stroke: color, "stroke-width": 1.5 },
      tooltip,
    );
    appendSvg("line", { x1: center - boxWidth / 2, y1: median, x2: center + boxWidth / 2, y2: median, stroke: "#111", "stroke-width": 1.5 });
    parseOutliers(row.visible_outliers).forEach((value) => {
      makeMark("circle", { cx: center, cy: frame.y(value), r: 3.2, fill: "#fff", stroke: color, "stroke-width": 1.2 }, exactTooltip([["组", labels[index]], ["可见离群点", value]]));
    });
  });
  addCategoryLabels(labels, (index) => PLOT.left + (index + 0.5) * slot, undefined, true);
  interactiveNote.textContent = "箱体仅表示可见五数概括与可分离离群点，不恢复原始样本。";
}

function renderHorizontalBoxplot(table) {
  const rows = table.rows.filter((row) => number(row.median) !== null);
  const allValues = rows.flatMap((row) => [row.lower_whisker, row.q1, row.median, row.q3, row.upper_whisker].map(number));
  const frame = numericFrame(extent(allValues), [0, rows.length], { numericX: true, numericY: false });
  const slot = frame.plotHeight / rows.length;
  rows.forEach((row, index) => {
    const center = PLOT.top + (index + 0.5) * slot;
    const boxHeight = slot * 0.48;
    const tooltip = exactTooltip([
      ["组", row.group],
      ["下须", row.lower_whisker],
      ["Q1", row.q1],
      ["中位数", row.median],
      ["Q3", row.q3],
      ["上须", row.upper_whisker],
      ["可见离群点", row.visible_outliers],
    ]);
    appendSvg("line", { x1: frame.x(number(row.lower_whisker)), y1: center, x2: frame.x(number(row.upper_whisker)), y2: center, stroke: "#222", "stroke-width": 1.2 });
    makeMark(
      "rect",
      { x: frame.x(number(row.q1)), y: center - boxHeight / 2, width: frame.x(number(row.q3)) - frame.x(number(row.q1)), height: boxHeight, fill: "#6f9993", "fill-opacity": 0.55, stroke: "#446d68", "stroke-width": 1.3 },
      tooltip,
    );
    appendSvg("line", { x1: frame.x(number(row.median)), y1: center - boxHeight / 2, x2: frame.x(number(row.median)), y2: center + boxHeight / 2, stroke: "#111", "stroke-width": 1.4 });
    appendSvg("text", { x: PLOT.left - 10, y: center + 3, "text-anchor": "end", class: "axis-label" }, row.group);
    parseOutliers(row.visible_outliers).forEach((value) => {
      makeMark("circle", { cx: frame.x(value), cy: center, r: 3.2, fill: "#fff", stroke: "#446d68", "stroke-width": 1.2 }, exactTooltip([["组", row.group], ["可见离群点", value]]));
    });
  });
  interactiveNote.textContent = "横向交互箱体展示 CSV 中的五数概括与可见离群点。";
}

function renderForest(table) {
  const rows = table.rows.filter((row) => number(row.estimate) !== null && number(row.ci_low) !== null && number(row.ci_high) !== null);
  const frame = numericFrame(extent(rows.flatMap((row) => [number(row.ci_low), number(row.ci_high)])), [0, rows.length], { numericX: true, numericY: false });
  const slot = frame.plotHeight / rows.length;
  rows.forEach((row, index) => {
    const y = PLOT.top + (index + 0.5) * slot;
    const tooltip = exactTooltip([["指标", row.trait], ["估计值", row.estimate], ["区间下界", row.ci_low], ["区间上界", row.ci_high], ["置信度", row.confidence]]);
    appendSvg("line", { x1: frame.x(number(row.ci_low)), y1: y, x2: frame.x(number(row.ci_high)), y2: y, stroke: row.sampled_rgb || "#5f453f", "stroke-width": 2 });
    makeMark("circle", { cx: frame.x(number(row.estimate)), cy: y, r: 4.2, fill: row.sampled_rgb || "#5f453f" }, tooltip);
    appendSvg("text", { x: PLOT.left - 10, y: y + 3, "text-anchor": "end", class: "axis-label" }, row.trait.length > 18 ? `${row.trait.slice(0, 17)}…` : row.trait);
  });
  interactiveNote.textContent = "交互区间仅表示图中可见估计值与区间端点；区间统计语义以原文为准。";
}

function linearScale(domainMin, domainMax, rangeMin, rangeMax) {
  return (value) => rangeMin + ((value - domainMin) / (domainMax - domainMin || 1)) * (rangeMax - rangeMin);
}

function paperText(text, x, y, attributes = {}) {
  const classes = ["paper-text", attributes.class].filter(Boolean).join(" ");
  return appendSvg("text", { x, y, ...attributes, class: classes }, text);
}

function paperLine(x1, y1, x2, y2, attributes = {}) {
  return appendSvg("line", { x1, y1, x2, y2, "vector-effect": "non-scaling-stroke", ...attributes });
}

function makePaperMarker(shape, cx, cy, size, style, tooltip) {
  const shared = {
    fill: style.fill || "#fff",
    stroke: style.stroke,
    "stroke-width": style.strokeWidth || 2,
    "vector-effect": "non-scaling-stroke",
  };
  if (shape === "square") {
    return makeMark("rect", { x: cx - size, y: cy - size, width: size * 2, height: size * 2, ...shared }, tooltip);
  }
  if (shape === "triangle") {
    const points = `${cx},${cy - size * 1.12} ${cx - size},${cy + size * 0.88} ${cx + size},${cy + size * 0.88}`;
    return makeMark("polygon", { points, ...shared }, tooltip);
  }
  return makeMark("circle", { cx, cy, r: size, ...shared }, tooltip);
}

function renderPaperDoseResponse(sample, table, layers) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  const x = linearScale(axes.xDomain[0], axes.xDomain[1], plot.mainLeft, plot.mainRight);
  const y = linearScale(axes.yDomain[0], axes.yDomain[1], plot.bottom, plot.top);

  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperText("d", 21, 62, { "font-size": 49, "font-weight": 700, fill: "#292929" });
  paperText("D₅R", 114, 80, { "font-size": 39, fill: "#050505" });
  paperText("V345N/S124V/W349Y", 215, 73, { "font-size": 40, fill: "#ff00a9" });
  paperText("K98G/E102I/D342I/A164V", 186, 118, { "font-size": 40, fill: "#ff00a9" });
  paperText("(M74)", 346, 162, { "font-size": 39, fill: "#050505" });

  paperLine(plot.axisLeft, plot.top, plot.axisLeft, plot.bottom, { stroke: "#050505", "stroke-width": 2.4 });
  paperLine(plot.axisLeft, plot.bottom, plot.breakLeft, plot.bottom, { stroke: "#050505", "stroke-width": 2.4 });
  paperLine(plot.breakRight, plot.bottom, plot.mainRight, plot.bottom, { stroke: "#050505", "stroke-width": 2.4 });
  paperLine(plot.breakLeft, plot.bottom - 9, plot.breakLeft, plot.bottom + 9, { stroke: "#050505", "stroke-width": 2.4 });
  paperLine(plot.breakRight, plot.bottom - 9, plot.breakRight, plot.bottom + 9, { stroke: "#050505", "stroke-width": 2.4 });

  axes.yTicks.forEach((tick) => {
    const py = y(tick);
    paperLine(plot.axisLeft - 11, py, plot.axisLeft, py, { stroke: "#050505", "stroke-width": 2.1 });
    paperText(String(tick), plot.axisLeft - 15, py + 10, { "font-size": 33, "text-anchor": "end", fill: "#050505" });
  });
  axes.xTicks.forEach((tick) => {
    const px = x(tick);
    paperLine(px, plot.bottom, px, plot.bottom + 15, { stroke: "#050505", "stroke-width": 2.1 });
    paperText(String(tick), px, plot.bottom + 44, { "font-size": 31, "text-anchor": "middle", fill: "#050505" });
  });
  paperText("0", plot.vehicleX, plot.bottom + 44, { "font-size": 31, "text-anchor": "middle", fill: "#050505" });
  paperText(axes.xLabel, 356, 506, { "font-size": 34, "text-anchor": "middle", fill: "#050505" });
  paperText(axes.yLabel, 68, 279, { "font-size": 34, "text-anchor": "middle", transform: "rotate(-90 68 279)", fill: "#050505" });

  const curveTable = layers.curves;
  Object.keys(series).forEach((name) => {
    const style = series[name];
    const curveRows = (curveTable?.rows || [])
      .filter((row) => row.series === name && number(row.log10_molar) !== null && number(row.plotted_value) !== null)
      .sort((a, b) => number(a.sample_index) - number(b.sample_index));
    if (curveRows.length) {
      const path = curveRows
        .map((row, index) => `${index ? "L" : "M"}${x(number(row.log10_molar))},${y(number(row.plotted_value))}`)
        .join(" ");
      makeMark(
        "path",
        { d: path, fill: "none", stroke: style.color, "stroke-width": 2.35, "vector-effect": "non-scaling-stroke" },
        exactTooltip([["系列", name], ["几何", "作者 OA PDF 曲线路径"], ["状态", "curve_path_traced"]]),
      );
    }
    const vehicle = table.rows.find((row) => row.series === name && row.segment === "vehicle");
    if (vehicle && number(vehicle.digitized_value) !== null) {
      paperLine(plot.vehicleX, y(number(vehicle.digitized_value)), plot.breakLeft, y(number(vehicle.digitized_value)), {
        stroke: style.color,
        "stroke-width": 2.35,
      });
    }
  });

  table.rows.forEach((row) => {
    const style = series[row.series];
    if (!style || number(row.digitized_value) === null) return;
    const px = row.segment === "vehicle" ? plot.vehicleX : x(number(row.log10_molar));
    const py = y(number(row.digitized_value));
    const lower = number(row.digitized_error_lower);
    const upper = number(row.digitized_error_upper);
    if (lower !== null && upper !== null) {
      paperLine(px, y(lower), px, y(upper), { stroke: style.color, "stroke-width": 1.45 });
      paperLine(px - 5, y(lower), px + 5, y(lower), { stroke: style.color, "stroke-width": 1.45 });
      paperLine(px - 5, y(upper), px + 5, y(upper), { stroke: style.color, "stroke-width": 1.45 });
    }
    makePaperMarker(
      style.marker,
      px,
      py,
      6.2,
      { fill: "#fff", stroke: style.color, strokeWidth: 2.2 },
      exactTooltip([
        ["系列", row.series],
        ["区段", row.segment],
        ["log10(M)", row.log10_molar || "vehicle"],
        ["提取值", row.digitized_value],
        ["误差下端", row.digitized_error_lower],
        ["误差上端", row.digitized_error_upper],
      ]),
    );
  });
  interactiveNote.textContent = `${spec.note} 悬停标记可读取由图像提取的数值；悬停曲线路径可查看逐点坐标。`;
}

function renderPaperHeatmap(sample, table) {
  const spec = sample.styleSpec;
  const { colorbar } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperText("c", 29, 38, { "font-size": 39, "font-weight": 700, fill: "#050505" });
  paperText("Correlation (embeddings, biomarkers)", 81, 38, { "font-size": 28, fill: "#050505" });

  const rows = [...table.rows].sort((a, b) => number(a.row_index) - number(b.row_index) || number(a.column_index) - number(b.column_index));
  rows.forEach((row) => {
    const left = number(row.cell_left_pixel);
    const top = number(row.cell_top_pixel);
    const right = number(row.cell_right_pixel);
    const bottom = number(row.cell_bottom_pixel);
    const fill = `rgb(${row.fill_rgb})`;
    makeMark(
      "rect",
      {
        x: left,
        y: top,
        width: right - left + 1,
        height: bottom - top + 1,
        fill,
        stroke: "#292929",
        "stroke-width": 0.8,
        "vector-effect": "non-scaling-stroke",
      },
      exactTooltip([
        ["embedding", row.embedding],
        ["biomarker", row.biomarker],
        ["提取相关系数", row.digitized_correlation],
        ["值状态", row.value_status],
        ["区间", row.value_interval],
        ["可见显著性", row.significant_visible],
        ["原图 RGB", row.fill_rgb],
      ]),
    );
    if (String(row.significant_visible).toLowerCase() === "true") {
      paperText("*", (left + right) / 2, (top + bottom) / 2 + 8, {
        "font-size": 25,
        "font-weight": 700,
        "text-anchor": "middle",
        fill: "#fff",
      });
    }
  });

  const rowLabels = unique(rows.map((row) => row.embedding));
  rowLabels.forEach((label) => {
    const row = rows.find((item) => item.embedding === label);
    const center = (number(row.cell_top_pixel) + number(row.cell_bottom_pixel)) / 2 + 7;
    paperText(label, 70, center, { "font-size": 19, "text-anchor": "end", fill: "#111" });
  });
  const columnLabels = unique(rows.map((row) => row.biomarker));
  columnLabels.forEach((label) => {
    const row = rows.find((item) => item.biomarker === label);
    const center = (number(row.cell_left_pixel) + number(row.cell_right_pixel)) / 2 + 6;
    paperText(label, center, 733, {
      "font-size": 18,
      "text-anchor": "end",
      transform: `rotate(-90 ${center} 733)`,
      fill: "#111",
    });
  });

  const defs = appendSvg("defs");
  const gradient = appendSvg("linearGradient", { id: "paper-heat-gradient", x1: "0%", y1: "100%", x2: "0%", y2: "0%" }, null, defs);
  appendSvg("stop", { offset: "0%", "stop-color": colorbar.low }, null, gradient);
  appendSvg("stop", { offset: "50%", "stop-color": colorbar.mid }, null, gradient);
  appendSvg("stop", { offset: "100%", "stop-color": colorbar.high }, null, gradient);
  appendSvg("rect", {
    x: colorbar.left,
    y: colorbar.top,
    width: colorbar.right - colorbar.left,
    height: colorbar.bottom - colorbar.top,
    fill: "url(#paper-heat-gradient)",
  });
  paperText("0.3", colorbar.left - 12, colorbar.top + 8, { "font-size": 21, "text-anchor": "end", fill: "#111" });
  paperText("0", colorbar.left - 12, (colorbar.top + colorbar.bottom) / 2 + 7, { "font-size": 21, "text-anchor": "end", fill: "#111" });
  paperText("−0.3", colorbar.left - 12, colorbar.bottom + 7, { "font-size": 21, "text-anchor": "end", fill: "#111" });
  paperText("Correlation", 864, (colorbar.top + colorbar.bottom) / 2, {
    "font-size": 24,
    "text-anchor": "middle",
    transform: `rotate(90 864 ${(colorbar.top + colorbar.bottom) / 2})`,
    fill: "#111",
  });
  interactiveNote.textContent = `${spec.note} 悬停任一格可读取未四舍五入的提取值、截尾状态、显著性与采样 RGB。`;
}

function renderPaperBoxplot(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperText("b", 7, 38, { "font-size": 42, "font-weight": 700, fill: "#050505" });
  paperText("Generalization on BioFINDER-2", 57, 38, { "font-size": 29, fill: "#111" });

  appendSvg("rect", { x: 327, y: 53, width: 20, height: 20, fill: "#fff", stroke: "#263b43", "stroke-width": 1.6 });
  paperText("Retrain", 357, 71, { "font-size": 27, fill: "#111" });
  appendSvg("rect", { x: 559, y: 53, width: 20, height: 20, fill: series.Finetune.fill, stroke: "#263b43", "stroke-width": 1.6 });
  paperText("Finetune", 589, 71, { "font-size": 27, fill: "#111" });

  const panelConfig = {
    BCA: { left: plot.leftPanelX, right: plot.leftPanelX + plot.panelWidth, labelX: 54 },
    AUC: { left: plot.rightPanelX, right: plot.rightPanelX + plot.panelWidth, labelX: 557 },
  };
  const valueToY = linearScale(axes.yDomain[0], axes.yDomain[1], plot.bottom, plot.top);
  Object.entries(panelConfig).forEach(([panel, panelPlot]) => {
    paperLine(panelPlot.left, plot.top, panelPlot.left, plot.bottom, { stroke: "#222", "stroke-width": 1.25 });
    paperLine(panelPlot.left, plot.bottom, panelPlot.right, plot.bottom, { stroke: "#222", "stroke-width": 1.25 });
    axes.yTicks.forEach((tick) => {
      const py = valueToY(tick);
      paperLine(panelPlot.left - 10, py, panelPlot.left, py, { stroke: "#222", "stroke-width": 1.15 });
      paperText(tick.toFixed(1), panelPlot.left - 18, py + 7, { "font-size": 21, "text-anchor": "end", fill: "#111" });
    });
    paperText(panel, panelPlot.labelX, (plot.top + plot.bottom) / 2, {
      "font-size": 24,
      "text-anchor": "middle",
      transform: `rotate(-90 ${panelPlot.labelX} ${(plot.top + plot.bottom) / 2})`,
      fill: "#111",
    });
    const panelRows = table.rows.filter((row) => row.panel === panel);
    unique(panelRows.map((row) => row.category)).forEach((category) => {
      const categoryRows = panelRows.filter((row) => row.category === category);
      const center = categoryRows.reduce((sum, row) => sum + number(row.category_center_pixel), 0) / categoryRows.length;
      paperText(category, center + 7, plot.bottom + 20, {
        "font-size": 22,
        "text-anchor": "end",
        transform: `rotate(-90 ${center + 7} ${plot.bottom + 20})`,
        fill: "#111",
      });
    });
  });

  table.rows.forEach((row) => {
    const style = series[row.series];
    const center = number(row.category_center_pixel);
    const q1 = number(row.q1_pixel);
    const q3 = number(row.q3_pixel);
    const median = number(row.median_pixel);
    const lower = number(row.lower_whisker_pixel);
    const upper = number(row.upper_whisker_pixel);
    const width = 20;
    const tooltip = exactTooltip([
      ["面板", row.panel],
      ["类别", row.category],
      ["系列", row.series],
      ["Q1", row.q1],
      ["中位数", row.median],
      ["Q3", row.q3],
      ["下须", row.lower_whisker],
      ["上须", row.upper_whisker],
      ["可见离群点", row.visible_outliers],
    ]);
    paperLine(center, upper, center, lower, { stroke: style.stroke, "stroke-width": 2.2 });
    paperLine(center - 7, upper, center + 7, upper, { stroke: style.stroke, "stroke-width": 2.2 });
    paperLine(center - 7, lower, center + 7, lower, { stroke: style.stroke, "stroke-width": 2.2 });
    makeMark(
      "rect",
      {
        x: center - width / 2,
        y: Math.min(q1, q3),
        width,
        height: Math.max(2, Math.abs(q1 - q3)),
        fill: style.fill,
        stroke: style.stroke,
        "stroke-width": 2.1,
        "vector-effect": "non-scaling-stroke",
      },
      tooltip,
    );
    paperLine(center - width / 2, median, center + width / 2, median, { stroke: style.stroke, "stroke-width": 2.2 });
    parseOutliers(row.visible_outliers).forEach((value) => {
        makeMark(
          "circle",
          { cx: center, cy: valueToY(value), r: 4.1, fill: "#fff", stroke: style.stroke, "stroke-width": 1.7, "vector-effect": "non-scaling-stroke" },
          exactTooltip([["面板", row.panel], ["类别", row.category], ["系列", row.series], ["可见离群点", value]]),
        );
      });
  });
  interactiveNote.textContent = `${spec.note} 悬停箱体读取可见五数概括，悬停空心圆读取离群点；不推断底层原始样本。`;
}

function renderPaperMultiPanelBoxplot(sample, table) {
  const spec = sample.styleSpec;
  const panels = {
    A: { left: 145, right: 690, top: 40, bottom: 604, color: "#f2b04e" },
    B: { left: 814, right: 1356, top: 40, bottom: 604, color: "#20908f" },
    C: { left: 145, right: 690, top: 812, bottom: 1376, color: "#6f0026" },
    D: { left: 814, right: 1356, top: 812, bottom: 1376, color: "#6c6c6c" },
  };
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const yPixel = (panel, value) => panel.bottom - (value - 0.05) * (panel.bottom - (panel.top + 14)) / 0.5;
  Object.entries(panels).forEach(([code, panel]) => {
    const rows = table.rows.filter((row) => row.panel === code);
    for (let tick = 0.05; tick <= 0.55001; tick += 0.05) {
      const y = yPixel(panel, tick);
      paperLine(panel.left, y, panel.right, y, { stroke: "#ececea", "stroke-width": 2 });
      if (code === "A" || code === "C") {
        if (tick >= 0.1 && tick <= 0.5 && Math.abs(tick * 10 - Math.round(tick * 10)) < 0.001) {
          paperText(tick.toFixed(1), panel.left - 16, y + 9, { "font-size": 26, "text-anchor": "end", fill: "#696969" });
        }
      }
    }
    rows.forEach((row) => paperLine(number(row.category_center_pixel), panel.top, number(row.category_center_pixel), panel.bottom, { stroke: "#ececea", "stroke-width": 2 }));
    paperLine(panel.left, panel.top, panel.left, panel.bottom, { stroke: "#5e5e5e", "stroke-width": 4 });
    paperLine(panel.left, panel.bottom, panel.right, panel.bottom, { stroke: "#5e5e5e", "stroke-width": 4 });
    paperText(code, panel.left + 52, panel.top + 74, { "font-size": 55, "text-anchor": "middle", fill: "#080808" });
    const stat = rows[0];
    const report = spec.panelStats[code];
    const statY = panel.top < 100 ? 25 : panel.top - 39;
    paperText(`X² = ${report.chi2}, η² = ${report.eta2}, p-val = ${report.pValue}`, (panel.left + panel.right) / 2, statY, { "font-size": 27, "font-style": "italic", "text-anchor": "middle", fill: "#171717" });
    rows.forEach((row) => {
      const center = number(row.category_center_pixel);
      const left = number(row.box_left_pixel);
      const right = number(row.box_right_pixel);
      const q1 = number(row.q1_pixel);
      const median = number(row.median_pixel);
      const q3 = number(row.q3_pixel);
      const lower = number(row.lower_whisker_pixel);
      const upper = number(row.upper_whisker_pixel);
      const tooltip = exactTooltip([
        ["panel", row.panel],
        ["group", row.category],
        ["n", row.n],
        ["Q1", row.q1],
        ["median", row.median],
        ["Q3", row.q3],
        ["lower whisker", row.lower_whisker],
        ["upper whisker", row.upper_whisker],
        ["visible outliers", row.visible_outliers || "none"],
        ["evidence", "visible chart geometry"],
      ]);
      paperLine(center, upper, center, q3, { stroke: "#353535", "stroke-width": 3 });
      paperLine(center, q1, center, lower, { stroke: "#353535", "stroke-width": 3 });
      makeMark("rect", { x: left, y: q3, width: right - left, height: q1 - q3, fill: row.fill_color, stroke: "#353535", "stroke-width": 4, "vector-effect": "non-scaling-stroke" }, tooltip);
      paperLine(left, median, right, median, { stroke: "#353535", "stroke-width": 4 });
      parseOutliers(row.visible_outliers).forEach((value) => {
        makeMark("circle", { cx: center, cy: yPixel(panel, value), r: 7, fill: "#363636", stroke: "#363636", "stroke-width": 2, "vector-effect": "non-scaling-stroke" }, exactTooltip([["panel", row.panel], ["group", row.category], ["visible outlier", value], ["evidence", "visible chart geometry"]]));
      });
      paperText(row.significance_letter, center, number(row.letter_y_pixel) + 13, { "font-size": 37, "font-weight": 700, "text-anchor": "middle", fill: "#050505" });
      String(row.plot_label || row.category).split("\n").forEach((line, index) => {
        paperText(line, center, panel.bottom + 43 + index * 29, { "font-size": 26, "text-anchor": "middle", fill: "#141414" });
      });
    });
    if (code === "A" || code === "C") {
      paperText("Multifunctionality", 25, (panel.top + panel.bottom) / 2, { "font-size": 38, "text-anchor": "middle", transform: `rotate(-90 25 ${(panel.top + panel.bottom) / 2})`, fill: "#050505" });
    }
  });
  [["Land use", "#f2b04e"], ["Climatic region", "#20908f"], ["Soil texture", "#6f0026"], ["Soil pH", "#6c6c6c"]].forEach(([label, color], index) => {
    const y = 44 + index * 64;
    appendSvg("rect", { x: 1452, y, width: 43, height: 43, fill: color, stroke: "#222", "stroke-width": 4 });
    paperText(label, 1514, y + 31, { "font-size": 34, fill: "#111" });
  });
  interactiveNote.textContent = spec.note;
}

function renderPaperGroupedBar(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const y = linearScale(axes.yDomain[0], axes.yDomain[1], plot.baseline, plot.top);
  axes.yTicks.forEach((tick) => {
    const py = y(tick);
    paperLine(plot.left, py, plot.right, py, { stroke: "#e9e9e9", "stroke-width": 2.2 });
    paperText(String(tick), plot.left - 10, py + 7, { "font-size": 19, "text-anchor": "end", fill: "#4a4a4a" });
  });
  const categories = unique(table.rows.map((row) => row.category));
  categories.forEach((category) => {
    const categoryRows = table.rows.filter((row) => row.category === category);
    const center = categoryRows.reduce((sum, row) => sum + number(row.category_center_pixel), 0) / categoryRows.length;
    paperLine(center, plot.top, center, plot.baseline, { stroke: "#eeeeee", "stroke-width": 2.2 });
  });
  appendSvg("rect", {
    x: plot.left,
    y: plot.top,
    width: plot.right - plot.left,
    height: plot.bottom - plot.top,
    fill: "none",
    stroke: "#333",
    "stroke-width": 1.2,
    "vector-effect": "non-scaling-stroke",
  });
  table.rows.forEach((row) => {
    const style = series[row.series];
    const left = number(row.bar_left_pixel);
    const top = number(row.bar_top_pixel);
    const right = number(row.bar_right_pixel);
    const bottom = number(row.bar_bottom_pixel);
    makeMark(
      "rect",
      { x: left, y: top, width: right - left + 1, height: bottom - top + 1, fill: style.color },
      exactTooltip([
        ["类别", row.category],
        ["系列", row.series],
        ["提取值", row.value],
        ["单位", row.unit],
        ["置信度", row.confidence],
        ["原图柱边界", `${row.bar_left_pixel}, ${row.bar_top_pixel}, ${row.bar_right_pixel}, ${row.bar_bottom_pixel}`],
      ]),
    );
  });
  categories.forEach((category) => {
    const categoryRows = table.rows.filter((row) => row.category === category);
    const center = categoryRows.reduce((sum, row) => sum + number(row.category_center_pixel), 0) / categoryRows.length;
    paperText(category, center + 8, 526, {
      "font-size": 17,
      "text-anchor": "end",
      transform: `rotate(-28 ${center + 8} 526)`,
      fill: "#444",
    });
  });
  paperText("B)", 8, 38, { "font-size": 38, fill: "#050505" });
  paperText(axes.yLabel, 17, (plot.top + plot.bottom) / 2, {
    "font-size": 20,
    "text-anchor": "middle",
    transform: `rotate(-90 17 ${(plot.top + plot.bottom) / 2})`,
    fill: "#111",
  });
  paperText(axes.xLabel, (plot.left + plot.right) / 2, 645, { "font-size": 23, "text-anchor": "middle", fill: "#111" });

  appendSvg("rect", { x: 105, y: 39, width: 99, height: 126, fill: "#fff", opacity: 0.96 });
  paperText("tissue", 114, 70, { "font-size": 28, "font-weight": 700, fill: "#111" });
  appendSvg("rect", { x: 114, y: 84, width: 32, height: 32, fill: series.CER.color });
  paperText("CER", 158, 110, { "font-size": 26, fill: "#111" });
  appendSvg("rect", { x: 114, y: 120, width: 32, height: 32, fill: series.TCX.color });
  paperText("TCX", 158, 146, { "font-size": 26, fill: "#111" });
  interactiveNote.textContent = `${spec.note} 悬停柱体可读取未四舍五入的校准值、置信度与原图矩形边界。`;
}

function renderPaperDualAxisBarLine(sample, table) {
  const spec = sample.styleSpec;
  const { crop, panels } = spec;
  const scale = number(crop.scale) || 1;
  const toCanvas = (xPt, yPt) => ({
    x: (number(xPt) - number(crop.x)) * scale,
    y: (number(yPt) - number(crop.y)) * scale,
  });
  const rowTooltip = (row) => exactTooltip(table.headers.map((field) => [field, row[field]]));

  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", {
    x: 0,
    y: 0,
    width: spec.canvas.width,
    height: spec.canvas.height,
    fill: "#fff",
    "pointer-events": "none",
  });

  panels.forEach((panel) => {
    const [leftPt, topPt, rightPt, bottomPt] = panel.plotBoundsPt;
    const topLeft = toCanvas(leftPt, topPt);
    const bottomRight = toCanvas(rightPt, bottomPt);
    const left = topLeft.x;
    const top = topLeft.y;
    const right = bottomRight.x;
    const bottom = bottomRight.y;
    const panelRows = table.rows
      .filter((row) => row.panel_id === panel.id)
      .sort((a, b) => number(a.year) - number(b.year));

    panel.barTicks.forEach((tick) => {
      const y = bottom - ((tick - panel.barDomain[0]) / (panel.barDomain[1] - panel.barDomain[0])) * (bottom - top);
      paperLine(left, y, right, y, {
        stroke: "#ececec",
        "stroke-width": 2,
        "pointer-events": "none",
      });
      paperText(String(tick), left - 18, y + 9, {
        "font-size": 27,
        "text-anchor": "end",
        fill: "#444",
        "pointer-events": "none",
      });
    });
    panel.lineTicks.forEach((tick) => {
      const y = bottom - ((tick - panel.lineDomain[0]) / (panel.lineDomain[1] - panel.lineDomain[0])) * (bottom - top);
      paperText(String(tick), right + 18, y + 9, {
        "font-size": 27,
        "text-anchor": "start",
        fill: "#444",
        "pointer-events": "none",
      });
    });

    appendSvg("rect", {
      x: left,
      y: top,
      width: right - left,
      height: bottom - top,
      fill: "none",
      stroke: "#353535",
      "stroke-width": 3,
      "vector-effect": "non-scaling-stroke",
      "pointer-events": "none",
    });

    panelRows.forEach((row) => {
      const center = toCanvas(row.bar_x_center_pt, row.bar_top_y_pt);
      const baseline = toCanvas(row.bar_x_center_pt, row.bar_bottom_y_pt);
      const width = number(spec.barWidthPt) * scale;
      makeMark(
        "rect",
        {
          x: center.x - width / 2,
          y: center.y,
          width,
          height: Math.max(1, baseline.y - center.y),
          fill: spec.barColor,
          tabindex: 0,
        },
        rowTooltip(row),
      );
    });

    const markerPoints = panelRows.map((row) => {
      const position = toCanvas(row.line_marker_x_pt, row.line_marker_y_pt);
      return { row, ...position };
    });
    appendSvg("path", {
      d: markerPoints.map((point, index) => `${index ? "L" : "M"}${point.x},${point.y}`).join(" "),
      fill: "none",
      stroke: spec.lineColor,
      "stroke-width": 9,
      "stroke-linejoin": "round",
      "stroke-linecap": "round",
      "vector-effect": "non-scaling-stroke",
      "pointer-events": "none",
    });
    markerPoints.forEach((point) => {
      makeMark(
        "circle",
        {
          cx: point.x,
          cy: point.y,
          r: 13,
          fill: spec.markerFill,
          stroke: spec.markerStroke,
          "stroke-width": 5,
          "vector-effect": "non-scaling-stroke",
          tabindex: 0,
        },
        rowTooltip(point.row),
      );
      paperText(point.row.year, point.x, bottom + 84, {
        "font-size": 27,
        "text-anchor": "middle",
        transform: `rotate(-90 ${point.x} ${bottom + 84})`,
        fill: "#333",
        "pointer-events": "none",
      });
    });

    const axisY = (top + bottom) / 2;
    paperText(`Bars: ${panel.statistic} link's mean RT transmission market value ($/MWh)`, left - 86, axisY, {
      "font-size": 29,
      "text-anchor": "middle",
      transform: `rotate(-90 ${left - 86} ${axisY})`,
      fill: "#222",
      "pointer-events": "none",
    });
    paperText(`Lines: ${panel.statistic} wholesale electricity RT price ($/MWh)`, right + 91, axisY, {
      "font-size": 29,
      "text-anchor": "middle",
      transform: `rotate(-90 ${right + 91} ${axisY})`,
      fill: "#222",
      "pointer-events": "none",
    });
  });
  interactiveNote.textContent = `${spec.note} 折线路径、坐标轴和文字均为装饰层，不拦截数据标记的悬停。`;
}

function renderPaperBarDot(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const valueToY = linearScale(axes.yDomain[0], axes.yDomain[1], plot.baseline, plot.top);
  const seriesNames = Object.keys(series);
  const categories = [...table.rows]
    .sort((a, b) => number(a.category_index) - number(b.category_index))
    .map((row) => row.category)
    .filter((category, index, all) => all.indexOf(category) === index);
  const slot = (plot.right - plot.left) / Math.max(categories.length, 1);
  const groupWidth = Math.min(102, slot * 0.76);
  const barWidth = groupWidth / Math.max(seriesNames.length, 1);

  axes.yTicks.forEach((tick) => {
    const py = valueToY(tick);
    paperLine(plot.left, py, plot.right, py, { stroke: "#e8e8e8", "stroke-width": 1.1 });
    paperText(String(tick), plot.left - 11, py + 6, { "font-size": 16, "text-anchor": "end", fill: "#444" });
  });
  paperLine(plot.left, plot.top, plot.left, plot.baseline, { stroke: "#555", "stroke-width": 1.2 });
  paperLine(plot.left, plot.baseline, plot.right, plot.baseline, { stroke: "#555", "stroke-width": 1.2 });
  paperText("Fig. 1", 20, 32, { "font-size": 19, fill: "#222" });
  paperText(axes.yLabel, 22, (plot.top + plot.baseline) / 2, {
    "font-size": 17,
    "text-anchor": "middle",
    transform: `rotate(-90 22 ${(plot.top + plot.baseline) / 2})`,
    fill: "#222",
  });

  seriesNames.forEach((name, seriesIndex) => {
    const style = series[name] || {};
    const legendX = 104 + seriesIndex * 202;
    appendSvg("rect", { x: legendX, y: 14, width: 13, height: 13, fill: style.color || "#888", stroke: style.stroke || "#666", "stroke-width": 1 });
    paperText(name, legendX + 20, 26, { "font-size": 14, fill: "#222" });
  });

  categories.forEach((category, categoryIndex) => {
    const center = plot.left + (categoryIndex + 0.5) * slot;
    const categoryRows = table.rows.filter((row) => row.category === category);
    categoryRows.forEach((row) => {
      const seriesIndex = number(row.series_index) ?? seriesNames.indexOf(row.series);
      const style = series[row.series] || {};
      const value = number(row.value);
      const sd = number(row.sd);
      if (value === null || seriesIndex < 0) return;
      const barCenter = center + (seriesIndex - (seriesNames.length - 1) / 2) * barWidth;
      const left = barCenter - barWidth * 0.43;
      const top = valueToY(value);
      const bottom = valueToY(0);
      const tooltip = exactTooltip([
        ["类别", category],
        ["系列", row.series],
        ["均值 (%)", row.value],
        ["s.d. (%)", row.sd],
        ["可见点 (%)", row.points],
        ["提取状态", row.visible_geometry_status || "image_extracted"],
      ]);
      makeMark("rect", {
        x: left,
        y: Math.min(top, bottom),
        width: Math.max(2, barWidth * 0.86),
        height: Math.max(1, Math.abs(bottom - top)),
        fill: style.color || "#888",
        stroke: style.stroke || "#666",
        "stroke-width": 1.1,
        "vector-effect": "non-scaling-stroke",
      }, tooltip);
      if (sd !== null) {
        const errorTop = valueToY(value + sd);
        const errorBottom = valueToY(Math.max(0, value - sd));
        paperLine(barCenter, errorTop, barCenter, errorBottom, { stroke: "#5c5c5c", "stroke-width": 1.1 });
        paperLine(barCenter - 4, errorTop, barCenter + 4, errorTop, { stroke: "#5c5c5c", "stroke-width": 1.1 });
        paperLine(barCenter - 4, errorBottom, barCenter + 4, errorBottom, { stroke: "#5c5c5c", "stroke-width": 1.1 });
      }
      const points = String(row.points || "").split(";").map(number).filter((point) => point !== null);
      points.forEach((point, pointIndex) => {
        const pointX = barCenter + (pointIndex - (points.length - 1) / 2) * Math.min(7, barWidth * 0.18);
        makeMark("circle", {
          cx: pointX,
          cy: valueToY(point),
          r: 3.4,
          fill: "#fff",
          stroke: "#4c4c4c",
          "stroke-width": 1.15,
          "vector-effect": "non-scaling-stroke",
        }, exactTooltip([["类别", category], ["系列", row.series], ["可见点 (%)", point], ["点序", pointIndex + 1], ["提取状态", row.visible_geometry_status || "image_extracted"]]));
      });
    });
    paperText(category, center, plot.baseline + 24, { "font-size": 13, "text-anchor": "middle", fill: "#444" });
  });
  paperText(axes.xLabel, (plot.left + plot.right) / 2, spec.canvas.height - 13, { "font-size": 15, "text-anchor": "middle", fill: "#222" });
  interactiveNote.textContent = spec.note;
}

function renderPaperSourceLine(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const x = linearScale(axes.xDomain[0], axes.xDomain[1], plot.left, plot.right);
  const y = linearScale(axes.yDomain[0], axes.yDomain[1], plot.bottom, plot.top);
  const ticks = axes.yTicks || [axes.yDomain[0], (axes.yDomain[0] + axes.yDomain[1]) / 2, axes.yDomain[1]];
  ticks.forEach((tick) => {
    const py = y(tick);
    paperLine(plot.left, py, plot.right, py, { stroke: "#e7e7e7", "stroke-width": 1 });
    paperText(String(tick), plot.left - 10, py + 5, { "font-size": 14, "text-anchor": "end", fill: "#444" });
  });
  paperLine(plot.left, plot.top, plot.left, plot.bottom, { stroke: "#222", "stroke-width": 1.2 });
  paperLine(plot.left, plot.bottom, plot.right, plot.bottom, { stroke: "#222", "stroke-width": 1.2 });
  unique(table.rows.map((row) => row.series)).forEach((name, seriesIndex) => {
    const color = series[name]?.color || seriesColors[name] || "#111";
    const points = table.rows.filter((row) => row.series === name && number(row.x) !== null && number(row.value) !== null).sort((a, b) => number(a.x) - number(b.x));
    if (!points.length) return;
    const path = points.map((row, index) => `${index ? "L" : "M"}${x(number(row.x))},${y(number(row.value))}`).join(" ");
    appendSvg("path", { d: path, fill: "none", stroke: color, "stroke-width": sample.id === "nature-02571-fig1d" ? 2.4 : 2.8, "vector-effect": "non-scaling-stroke" });
    points.forEach((row) => makeMark("circle", { cx: x(number(row.x)), cy: y(number(row.value)), r: sample.id === "nature-02571-fig1d" ? 2.1 : 2.8, fill: color, stroke: "#fff", "stroke-width": 0.7 }, exactTooltip([["series", row.series], ["x", row.x], ["value", row.value], ["pixel y", row.pixel_y], ["uncertainty", row.uncertainty_value], ["confidence", row.confidence], ["status", row.value_status || "visible geometry"]])));
    appendSvg("line", { x1: plot.right - 150, y1: plot.top + 18 + seriesIndex * 22, x2: plot.right - 125, y2: plot.top + 18 + seriesIndex * 22, stroke: color, "stroke-width": 3 });
    paperText(name, plot.right - 118, plot.top + 23 + seriesIndex * 22, { "font-size": 13, fill: color });
  });
  paperText(axes.xLabel || "x", (plot.left + plot.right) / 2, spec.canvas.height - 16, { "font-size": 15, "text-anchor": "middle", fill: "#222" });
  paperText(axes.yLabel || "y", 18, (plot.top + plot.bottom) / 2, { "font-size": 15, "text-anchor": "middle", transform: `rotate(-90 18 ${(plot.top + plot.bottom) / 2})`, fill: "#222" });
  interactiveNote.textContent = spec.note;
}

function renderNativeTraceLine(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperLine(plot.left, plot.top, plot.left, plot.bottom, { stroke: "#222", "stroke-width": 1.2 });
  paperLine(plot.left, plot.bottom, plot.right, plot.bottom, { stroke: "#222", "stroke-width": 1.2 });
  const x = linearScale(axes.xDomain[0], axes.xDomain[1], plot.left, plot.right);
  const y = linearScale(axes.yDomain[0], axes.yDomain[1], plot.bottom, plot.top);
  (axes.xTicks || []).forEach((tick) => {
    const px = x(tick);
    paperLine(px, plot.bottom, px, plot.bottom + 7, { stroke: "#222", "stroke-width": 1.1 });
    paperText(String(tick), px, plot.bottom + 24, { "font-size": spec.tickFontSize || 12, "text-anchor": "middle", fill: "#222" });
  });
  (axes.yTicks || []).forEach((tick) => {
    const py = y(tick);
    paperLine(plot.left - 7, py, plot.left, py, { stroke: "#222", "stroke-width": 1.1 });
    paperText(String(tick), plot.left - 11, py + 4, { "font-size": spec.tickFontSize || 12, "text-anchor": "end", fill: "#222" });
  });
  if (axes.xLabel) paperText(axes.xLabel, (plot.left + plot.right) / 2, spec.canvas.height - (spec.xLabelOffset || 10), { "font-size": spec.labelFontSize || 14, "text-anchor": "middle", fill: "#222" });
  if (axes.yLabel) paperText(axes.yLabel, spec.yLabelX || 16, (plot.top + plot.bottom) / 2, { "font-size": spec.labelFontSize || 14, "text-anchor": "middle", transform: `rotate(-90 ${spec.yLabelX || 16} ${(plot.top + plot.bottom) / 2})`, fill: "#222" });
  if (spec.panelLabel) paperText(spec.panelLabel, spec.panelLabelX || 16, spec.panelLabelY || 25, { "font-size": spec.panelLabelSize || 20, "font-weight": 700, fill: "#111" });

  unique(table.rows.map((row) => row.series)).forEach((name, seriesIndex) => {
    const color = series[name]?.color || seriesColors[name] || "#111";
    const rows = table.rows
      .filter((row) => row.series === name)
      .sort((a, b) => number(a.pixel_x) - number(b.pixel_x));
    let drawing = false;
    const commands = [];
    rows.forEach((row) => {
      const px = number(row.pixel_x);
      const py = number(row.pixel_y);
      if (px === null || py === null || String(row.value_status || "").startsWith("not_")) {
        drawing = false;
        return;
      }
      commands.push(`${drawing ? "L" : "M"}${px},${py}`);
      drawing = true;
    });
    if (commands.length) appendSvg("path", { d: commands.join(" "), fill: "none", stroke: color, "stroke-width": series[name]?.lineWidth || spec.lineWidth || 1.7, "stroke-linejoin": "round", "stroke-linecap": "round", "vector-effect": "non-scaling-stroke" });

    const markerRows = rows.filter((row, index) => {
      const px = number(row.pixel_x);
      const py = number(row.pixel_y);
      const cadence = series[name]?.hitCadence || spec.hitCadence || 1;
      return px !== null && py !== null && index % cadence === 0 && !String(row.value_status || "").startsWith("not_");
    });
    markerRows.forEach((row, index) => {
      const px = number(row.pixel_x);
      const py = number(row.pixel_y);
      const tooltip = exactTooltip([["series", row.series], ["x", row.x], ["value", row.value], ["pixel x", row.pixel_x], ["pixel y", row.pixel_y], ["uncertainty", row.uncertainty_value], ["confidence", row.confidence], ["status", row.value_status || "visible geometry"]]);
      const marker = series[name]?.marker;
      if (marker === "plus") {
        const radius = series[name]?.markerRadius || 3;
        paperLine(px - radius, py, px + radius, py, { stroke: color, "stroke-width": series[name]?.markerWidth || 1.3 });
        paperLine(px, py - radius, px, py + radius, { stroke: color, "stroke-width": series[name]?.markerWidth || 1.3 });
      }
      makeMark("circle", { cx: px, cy: py, r: marker === "plus" ? 5 : 4.5, fill: "rgba(0,0,0,0.001)", stroke: "transparent", "stroke-width": 0, tabindex: index % 8 === 0 ? 0 : -1 }, tooltip);
    });
    const label = series[name]?.label;
    if (label) paperText(label.text || name, label.x, label.y, { "font-size": label.size || 12, fill: label.color || color, "text-anchor": label.anchor || "start" });
  });
  interactiveNote.textContent = spec.note;
}

function renderNativeGeometry(sample, table) {
  const spec = sample.styleSpec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: spec.background || "#fff" });
  (spec.polygons || []).forEach((polygon) => appendSvg("polygon", { points: polygon.points.map(([x, y]) => `${x},${y}`).join(" "), fill: polygon.fill || "#dceaf7", stroke: polygon.stroke || "none", "stroke-width": polygon.strokeWidth || 0, "pointer-events": "none" }));
  (spec.rects || []).forEach((rect) => appendSvg("rect", { x: rect.x, y: rect.y, width: rect.width, height: rect.height, fill: rect.fill || "#fff", stroke: rect.stroke || "none", "stroke-width": rect.strokeWidth || 0, "pointer-events": "none" }));
  (spec.lines || []).forEach((lineSpec) => paperLine(lineSpec.x1, lineSpec.y1, lineSpec.x2, lineSpec.y2, { stroke: lineSpec.stroke || "#222", "stroke-width": lineSpec.width || 1, "stroke-dasharray": lineSpec.dash || null, "pointer-events": "none" }));
  (spec.annotations || []).forEach((annotation) => {
    const attributes = { "font-size": annotation.size || 12, "font-weight": annotation.bold ? 700 : 400, "font-style": annotation.italic ? "italic" : "normal", "text-anchor": annotation.anchor || "start", "dominant-baseline": annotation.dominantBaseline || null, fill: annotation.fill || "#222", transform: annotation.rotate ? `rotate(${annotation.rotate} ${annotation.x} ${annotation.y})` : null, "pointer-events": "none" };
    const parts = String(annotation.text).split("\n");
    if (parts.length === 1) paperText(parts[0], annotation.x, annotation.y, attributes);
    else {
      const text = paperText("", annotation.x, annotation.y, attributes);
      parts.forEach((part, index) => appendSvg("tspan", { x: annotation.x, dy: index ? "1.04em" : 0 }, part, text));
    }
  });
  table.rows.forEach((row, index) => {
    const tooltip = exactTooltip([["kind", row.kind], ["series", row.series], ["category", row.category], ["x", row.x], ["y", row.y], ["value", row.value], ["pixel x", row.pixel_x], ["pixel y", row.pixel_y], ["status", row.value_status || "visible geometry"]]);
    const attrs = { fill: row.fill || row.color || "#555", stroke: row.stroke || "none", "stroke-width": row.stroke_width || 0, tabindex: index % 8 === 0 ? 0 : -1 };
    if (row.kind === "point") makeMark("circle", { ...attrs, cx: number(row.pixel_x), cy: number(row.pixel_y), r: number(row.radius) || 4 }, tooltip);
    else if (row.kind === "line") makeMark("line", { ...attrs, x1: number(row.pixel_x), y1: number(row.pixel_y), x2: number(row.x2), y2: number(row.y2), "stroke-width": row.stroke_width || 1.5, fill: "none" }, tooltip);
    else makeMark("rect", { ...attrs, x: number(row.pixel_x), y: number(row.pixel_y), width: number(row.width), height: number(row.height) }, tooltip);
  });
  interactiveNote.textContent = spec.note;
}

function renderRasterEvidenceInteractive(sample, table) {
  const spec = sample.styleSpec || {};
  const width = spec.canvas?.width || detailRecreatedImage.naturalWidth || CHART_WIDTH;
  const height = spec.canvas?.height || detailRecreatedImage.naturalHeight || CHART_HEIGHT;
  setChartCanvas(width, height, spec.fontFamily || "");
  appendSvg("image", {
    href: assetUrl(sample.assets.recreated),
    x: 0,
    y: 0,
    width,
    height,
    preserveAspectRatio: "none",
    "pointer-events": "none",
  });

  table.rows.forEach((row, index) => {
    const px = number(row.hit_x) ?? number(row.pixel_x);
    const py = number(row.hit_y) ?? number(row.pixel_y);
    if (px === null || py === null) return;
    const shape = row.shape || row.kind;
    const tooltip = exactTooltip([
      ["kind", row.kind || "visible mark"],
      ["set", row.set],
      ["intersection", row.intersection],
      ["column", row.column_id],
      ["members", row.members],
      ["count", row.count],
      ["present", row.present],
      ["series", row.series],
      ["category", row.category],
      ["x", row.x],
      ["y", row.y],
      ["value", row.value],
      ["error lower", row.error_lower],
      ["error upper", row.error_upper],
      ["error status", row.error_status],
      ["pixel x", row.pixel_x],
      ["pixel y", row.pixel_y],
      ["x uncertainty", row.x_uncertainty],
      ["y uncertainty", row.y_uncertainty],
      ["confidence", row.confidence],
      ["value uncertainty", row.value_uncertainty],
      ["component peaks", row.component_peak_count],
      ["status", row.value_status || "visible geometry"],
    ]);
    const shared = { fill: "rgba(0,0,0,0.001)", stroke: "transparent", "stroke-width": 0, tabindex: index % 8 === 0 ? 0 : -1 };
    if (shape === "rect" || row.kind === "cell") {
      makeMark("rect", { ...shared, x: px, y: py, width: Math.max(8, number(row.width) || 8), height: Math.max(8, number(row.height) || 8) }, tooltip);
    } else if (shape === "line") {
      makeMark("line", { ...shared, x1: px, y1: py, x2: number(row.x2) ?? px, y2: number(row.y2) ?? py, stroke: "rgba(0,0,0,0.001)", "stroke-width": Math.max(10, number(row.stroke_width) || 10) }, tooltip);
    } else {
      makeMark("circle", { ...shared, cx: px, cy: py, r: Math.max(8, number(row.radius) || 5) }, tooltip);
    }
  });
  interactiveNote.textContent = "同一份提取复现底图作为画布；悬停命中层只返回 CSV 中的可见图形数据。";
}

function renderPaperVisibleBars(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const y = linearScale(axes.yDomain[0], axes.yDomain[1], plot.baseline, plot.top);
  const categories = unique(table.rows.map((row) => row.category));
  const seriesNames = Object.keys(series);
  axes.yTicks.forEach((tick) => {
    const py = y(tick);
    paperLine(plot.left, py, plot.right, py, { stroke: "#e6e6e6", "stroke-width": 1 });
    paperText(String(tick), plot.left - 10, py + 5, { "font-size": 14, "text-anchor": "end", fill: "#444" });
  });
  paperLine(plot.left, plot.top, plot.left, plot.baseline, { stroke: "#222", "stroke-width": 1.2 });
  paperLine(plot.left, plot.baseline, plot.right, plot.baseline, { stroke: "#222", "stroke-width": 1.2 });
  const slot = (plot.right - plot.left) / Math.max(1, categories.length);
  const width = Math.min(92, slot * 0.72) / Math.max(1, seriesNames.length);
  categories.forEach((category, categoryIndex) => {
    const center = plot.left + (categoryIndex + 0.5) * slot;
    seriesNames.forEach((name, seriesIndex) => {
      const row = table.rows.find((candidate) => candidate.category === category && candidate.series === name);
      if (!row || number(row.value) === null) return;
      const barCenter = center + (seriesIndex - (seriesNames.length - 1) / 2) * width;
      const top = y(number(row.value));
      makeMark("rect", { x: barCenter - width * 0.43, y: top, width: width * 0.86, height: plot.baseline - top, fill: series[name]?.color || "#777" }, exactTooltip([["category", category], ["series", name], ["value", row.value], ["error lower", row.error_lower], ["error upper", row.error_upper], ["status", row.value_status || "visible geometry"]]));
      if (number(row.error_lower) !== null && number(row.error_upper) !== null) {
        const upper = y(number(row.error_upper));
        const lower = y(number(row.error_lower));
        paperLine(barCenter, upper, barCenter, lower, { stroke: "#333", "stroke-width": 1.1 });
        paperLine(barCenter - 4, upper, barCenter + 4, upper, { stroke: "#333", "stroke-width": 1.1 });
        paperLine(barCenter - 4, lower, barCenter + 4, lower, { stroke: "#333", "stroke-width": 1.1 });
      }
    });
    paperText(category, center, plot.baseline + 23, { "font-size": 14, "text-anchor": "middle", fill: "#333" });
  });
  seriesNames.forEach((name, index) => {
    const lx = plot.right - 170;
    const ly = plot.top + 18 + index * 20;
    appendSvg("rect", { x: lx, y: ly - 11, width: 13, height: 13, fill: series[name]?.color || "#777" });
    paperText(name, lx + 20, ly, { "font-size": 13, fill: "#333" });
  });
  paperText(axes.xLabel, (plot.left + plot.right) / 2, spec.canvas.height - 14, { "font-size": 15, "text-anchor": "middle", fill: "#222" });
  paperText(axes.yLabel, 19, (plot.top + plot.baseline) / 2, { "font-size": 15, "text-anchor": "middle", transform: `rotate(-90 19 ${(plot.top + plot.baseline) / 2})`, fill: "#222" });
  interactiveNote.textContent = spec.note;
}

function renderPaperBubbleMatrix(sample, table) {
  const spec = sample.styleSpec;
  const { grid, axes } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const rows = unique(table.rows.map((row) => row.row));
  const columns = unique(table.rows.map((row) => row.column));
  const x = linearScale(0, Math.max(1, columns.length - 1), grid.left, grid.right);
  const y = linearScale(0, Math.max(1, rows.length - 1), grid.top, grid.bottom);
  const sourceGrid = { left: 347, top: 5, right: 1096, bottom: 296 };
  const xFor = (row) => {
    const pixel = number(row.pixel_x);
    if (pixel === null) return x(columns.indexOf(row.column));
    return grid.left + ((pixel - sourceGrid.left) / (sourceGrid.right - sourceGrid.left)) * (grid.right - grid.left);
  };
  const yFor = (row) => {
    const pixel = number(row.pixel_y);
    if (pixel === null) return y(rows.indexOf(row.row));
    return grid.top + ((pixel - sourceGrid.top) / (sourceGrid.bottom - sourceGrid.top)) * (grid.bottom - grid.top);
  };
  appendSvg("rect", { x: grid.left, y: grid.top, width: grid.right - grid.left, height: grid.bottom - grid.top, fill: "none", stroke: "#333", "stroke-width": 1 });
  table.rows.forEach((row) => {
    const pixelX = number(row.pixel_x);
    const pixelY = number(row.pixel_y);
    if (pixelX === null || pixelY === null || row.visible_marker === "false") return;
    const measuredRadius = number(row.visible_radius_px);
    if (measuredRadius === null) return;
    const radius = Math.max(1.4, measuredRadius * (grid.right - grid.left) / (sourceGrid.right - sourceGrid.left));
    const tooltip = [["row", row.row], ["interaction", row.column], ["visible mark", row.visible_mark || "marker"], ["pixel radius", row.visible_radius_px], ["visible colour", row.visible_color], ["geometry status", row.visible_geometry_status || "visible geometry"], ["confidence", row.confidence]];
    makeMark("circle", { cx: xFor(row), cy: yFor(row), r: radius, fill: row.visible_color || "#777", stroke: "none" }, exactTooltip(tooltip));
  });
  rows.forEach((label, index) => paperText(label, grid.left - 9, y(index) + 4, { "font-size": 11, "text-anchor": "end", fill: "#222" }));
  columns.forEach((label, index) => paperText(label, x(index), grid.bottom + 14, { "font-size": 10, "text-anchor": "start", transform: `rotate(-72 ${x(index)} ${grid.bottom + 14})`, fill: "#222" }));
  paperText(axes.meanLabel || "visible marker colour and radius", (grid.left + grid.right) / 2, spec.canvas.height - 22, { "font-size": 14, "text-anchor": "middle", fill: "#333" });
  interactiveNote.textContent = spec.note;
}

function renderPaperUpset(sample, table) {
  const spec = sample.styleSpec;
  const { plot, axes, series } = spec;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const rows = [...table.rows].sort((a, b) => number(a.intersection) - number(b.intersection));
  const maxCount = Math.max(...rows.map((row) => number(row.count) || 0), 1);
  const x = linearScale(0, Math.max(1, rows.length - 1), plot.left, plot.right);
  const y = linearScale(0, maxCount, plot.barsBottom, plot.top);
  paperLine(plot.left, plot.barsBottom, plot.right, plot.barsBottom, { stroke: "#222", "stroke-width": 1.2 });
  paperLine(plot.left, plot.top, plot.left, plot.barsBottom, { stroke: "#222", "stroke-width": 1.2 });
  rows.forEach((row, index) => {
    const cx = x(index);
    const top = y(number(row.count));
    makeMark("rect", { x: cx - 18, y: top, width: 36, height: plot.barsBottom - top, fill: "#444" }, exactTooltip([["intersection", row.intersection], ["combination", row.combination], ["count", row.count], ["status", row.value_status || "visible printed value"]]));
    paperText(row.count, cx, top - 8, { "font-size": 11, "text-anchor": "middle", fill: "#555" });
  });
  const membership = ["FunC_1", "FunC_2", "FunC_3", "FunC_4"];
  membership.forEach((name, rowIndex) => {
    const py = plot.matrixTop + rowIndex * ((plot.matrixBottom - plot.matrixTop) / 3);
    paperText(name.replace("_", "-"), plot.left - 12, py + 4, { "font-size": 12, "text-anchor": "end", fill: "#333" });
    paperLine(plot.left, py, plot.right, py, { stroke: "#f1f1f1", "stroke-width": 1 });
  });
  rows.forEach((row, index) => {
    const cx = x(index);
    const active = membership.map((name) => number(row[name]) === 1);
    const activeIndices = active.map((on, i) => (on ? i : null)).filter((i) => i !== null);
    if (activeIndices.length > 1) paperLine(cx, plot.matrixTop + activeIndices[0] * ((plot.matrixBottom - plot.matrixTop) / 3), cx, plot.matrixTop + activeIndices[activeIndices.length - 1] * ((plot.matrixBottom - plot.matrixTop) / 3), { stroke: "#444", "stroke-width": 2.5 });
    active.forEach((on, rowIndex) => makeMark("circle", { cx, cy: plot.matrixTop + rowIndex * ((plot.matrixBottom - plot.matrixTop) / 3), r: on ? 5 : 4, fill: on ? "#444" : "#e5e5e5" }, exactTooltip([["intersection", row.intersection], ["combination", row.combination], ["member", membership[rowIndex]], ["present", on ? "yes" : "no"]])));
  });
  paperText(axes.yLabel || "Intersection size", 18, (plot.top + plot.barsBottom) / 2, { "font-size": 14, "text-anchor": "middle", transform: `rotate(-90 18 ${(plot.top + plot.barsBottom) / 2})`, fill: "#222" });
  interactiveNote.textContent = spec.note;
}

function renderPaperFourPanelLine(sample, table) {
  const spec = sample.styleSpec;
  const panels = {
    A_tuning: { left: 128, top: 62, right: 497, bottom: 448, xMax: 1.2, xLabel: "tuning dissimilarity", title: "" },
    A_distance: { left: 609, top: 62, right: 977, bottom: 448, xMax: 1.6, xLabel: "RF distance (deg)", title: "centered pairs" },
    B_tuning: { left: 128, top: 621, right: 497, bottom: 1004, xMax: 1.2, xLabel: "tuning dissimilarity", title: "" },
    B_distance: { left: 609, top: 621, right: 977, bottom: 1004, xMax: 1.6, xLabel: "RF distance (deg)", title: "mixed pairs" },
  };
  const colors = { "small image": "#0874bc", "large image": "#d95319" };
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperText("A", 1, 1, { "font-size": 66, "font-weight": 700, fill: "#111" });
  paperText("B", 1, 554, { "font-size": 66, "font-weight": 700, fill: "#111" });
  Object.entries(panels).forEach(([panelId, panel]) => {
    const x = linearScale(0, panel.xMax, panel.left, panel.right);
    const y = linearScale(0, 0.3, panel.bottom, panel.top);
    paperLine(panel.left, panel.top, panel.left, panel.bottom, { stroke: "#222", "stroke-width": 4 });
    paperLine(panel.left, panel.bottom, panel.right, panel.bottom, { stroke: "#222", "stroke-width": 4 });
    [0, 0.1, 0.2, 0.3].forEach((tick) => {
      const py = y(tick);
      paperLine(panel.left - 5, py, panel.left, py, { stroke: "#222", "stroke-width": 2 });
      paperText(tick === 0 ? "0" : tick.toFixed(1), panel.left - 12, py, { "font-size": 29, "text-anchor": "end", "dominant-baseline": "middle", fill: "#292929" });
    });
    const xTicks = panel.xMax === 1.2 ? [0, 0.3, 0.6, 0.9, 1.2] : [0, 0.4, 0.8, 1.2];
    xTicks.forEach((tick) => {
      const px = x(tick);
      paperLine(px, panel.bottom, px, panel.bottom + 6, { stroke: "#222", "stroke-width": 2 });
      paperText(tick === 0 ? "0" : tick.toFixed(1), px, panel.bottom + 18, { "font-size": 28, "text-anchor": "middle", "dominant-baseline": "hanging", fill: "#292929" });
    });
    paperText(panel.xLabel, (panel.left + panel.right) / 2, panel.bottom + 56, { "font-size": 31, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#292929" });
    if (panel.title) paperText(panel.title, (panel.left + panel.right) / 2, panel.top - 40, { "font-size": 30, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#292929" });
    if (panelId === "A_tuning" || panelId === "B_tuning") paperText("correlations (r_sc)", 38, (panel.top + panel.bottom) / 2, { "font-size": 29, "text-anchor": "middle", transform: `rotate(-90 38 ${(panel.top + panel.bottom) / 2})`, fill: "#292929" });
    ["small image", "large image"].forEach((series, seriesIndex) => {
      const selected = table.rows.filter((row) => row.panel === panelId && row.series === series).sort((a, b) => number(a.x) - number(b.x));
      if (!selected.length) return;
      const color = colors[series];
      const path = selected.map((row, index) => `${index ? "L" : "M"}${x(number(row.x))},${y(number(row.value))}`).join(" ");
      appendSvg("path", { d: path, fill: "none", stroke: color, "stroke-width": 5, "vector-effect": "non-scaling-stroke" });
      selected.forEach((row) => {
        const px = x(number(row.x)); const py = y(number(row.value)); const sem = number(row.sem) || 0;
        const high = y(number(row.value) + sem); const low = y(number(row.value) - sem);
        paperLine(px, high, px, low, { stroke: color, "stroke-width": 2.5 });
        paperLine(px - 5, high, px + 5, high, { stroke: color, "stroke-width": 2 });
        paperLine(px - 5, low, px + 5, low, { stroke: color, "stroke-width": 2 });
        makeMark("circle", { cx: px, cy: py, r: 8, fill: "#fff", stroke: color, "stroke-width": 4, "vector-effect": "non-scaling-stroke" }, exactTooltip([["panel", row.panel], ["series", row.series], ["display bin centre", row.x], ["correlation", row.value], ["SEM", row.sem], ["source", "official Source Data"]]));
      });
      if (panelId === "A_tuning") {
        const yy = seriesIndex ? 129 : 86;
        paperLine(222, yy, 281, yy, { stroke: color, "stroke-width": 5 });
        appendSvg("circle", { cx: 252, cy: yy, r: 8, fill: "#fff", stroke: color, "stroke-width": 4 });
        paperText(series, 291, yy, { "font-size": 29, "dominant-baseline": "middle", fill: "#222" });
      }
    });
    if (panelId === "A_tuning") paperText("ncase = 41,043", (panel.left + panel.right) / 2, panel.bottom - 28, { "font-size": 25, "text-anchor": "middle", fill: "#222" });
    if (panelId === "B_tuning") paperText("ncase = 5,654", (panel.left + panel.right) / 2, panel.bottom - 28, { "font-size": 25, "text-anchor": "middle", fill: "#222" });
  });
  interactiveNote.textContent = spec.note;
}

function renderPaperClinicalBars(sample, table) {
  const spec = sample.styleSpec;
  const colors = { Combined: "#303030", ChEMBL: "#5d9e20", "ChEMBL+": "#5d9e20", "Disease Ontology": "#cc650c", "Disease Ontology+": "#cc650c", DrugBank: "#dd2c8c", "DrugBank+": "#dd2c8c", "FDA SRS": "#1ab6bc", NCIt: "#7471ad", "NCIt+": "#7471ad", OncoTree: "#e4a607" };
  const panelSpecs = { drug: { left: 140, top: 58, right: 550, bottom: 712, max: 1, title: "a. Drug Terms" }, disease: { left: 638, top: 58, right: 1049, bottom: 712, max: .66, title: "b. Disease Terms" } };
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  Object.entries(panelSpecs).forEach(([name, panel]) => {
    const x = linearScale(0, panel.max, panel.left, panel.right);
    paperLine(panel.left, panel.top, panel.left, panel.bottom, { stroke: "#222", "stroke-width": 2 });
    paperLine(panel.left, panel.bottom, panel.right, panel.bottom, { stroke: "#222", "stroke-width": 2 });
    const ticks = panel.max === 1 ? [0, .25, .5, .75, 1] : [0, .2, .4, .6];
    ticks.forEach((tick) => { const px = x(tick); paperLine(px, panel.bottom, px, panel.bottom + 6, { stroke: "#222", "stroke-width": 2 }); paperText(tick === 0 || tick === 1 ? String(tick) : tick.toFixed(2), px, panel.bottom + 18, { "font-size": 24, "text-anchor": "middle", "dominant-baseline": "hanging", fill: "#222" }); });
    paperText(panel.title, (panel.left + panel.right) / 2, 20, { "font-size": 30, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#222" });
    const selected = table.rows.filter((row) => row.panel === name);
    let y = panel.top + 15;
    [1, 10, 100].forEach((frequency) => {
      selected.filter((row) => number(row.frequency) === frequency).forEach((row) => {
        const right = x(number(row.value)); const color = colors[row.series] || "#777";
        makeMark("rect", { x: panel.left, y, width: Math.max(1, right - panel.left), height: 18, fill: color }, exactTooltip([["panel", row.panel], ["resource", row.series], ["term frequency", row.frequency], ["term coverage", row.value], ["number of terms", row.number_of_terms], ["source", "official Source Data"]]));
        if (String(row.series).endsWith("+")) for (let xx = panel.left - 20; xx < right + 18; xx += 13) paperLine(xx, y + 18, xx + 18, y, { stroke: "#fff", "stroke-width": 2 });
        paperText(Number(row.value).toFixed(2), panel.left - 10, y + 9, { "font-size": 18, "text-anchor": "end", "dominant-baseline": "middle", fill: "#222" });
        y += 22;
      });
      y += 38;
    });
    paperText("Term Coverage", (panel.left + panel.right) / 2, panel.bottom + 63, { "font-size": 26, "text-anchor": "middle", fill: "#222" });
  });
  paperText("Term Frequency (Min Clinical Trials)", 15, 382, { "font-size": 26, "text-anchor": "middle", transform: "rotate(-90 15 382)", fill: "#222" });
  [["1", 150], ["10", 374], ["100", 599]].forEach(([label, y]) => paperText(label, 68, y, { "font-size": 25, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#222" }));
  const legend = ["Combined", "ChEMBL", "ChEMBL+", "Disease Ontology", "Disease Ontology+", "DrugBank", "DrugBank+", "FDA SRS", "NCIt", "NCIt+", "OncoTree"];
  legend.forEach((label, index) => { const y = 225 + index * 33; appendSvg("rect", { x: 1068, y: y - 13, width: 42, height: 16, fill: colors[label] }); if (label.endsWith("+")) for (let x = 1058; x < 1115; x += 11) paperLine(x, y + 3, x + 16, y - 13, { stroke: "#fff", "stroke-width": 2 }); paperText(label, 1129, y - 5, { "font-size": 25, "dominant-baseline": "middle", fill: "#222" }); });
  interactiveNote.textContent = spec.note;
}

function renderPaperSourceUpset(sample, table) {
  const spec = sample.styleSpec; const layout = spec.layout;
  const sets = table.rows.filter((row) => row.kind === "set_total");
  const order = spec.setOrder || sets.map((row) => row.set);
  const totals = Object.fromEntries(sets.map((row) => [row.set, row]));
  const rows = [...table.rows.filter((row) => row.kind === "intersection")].sort((a, b) => number(a.intersection) - number(b.intersection));
  const colors = spec.colors || {}; const typeColors = spec.typeColors || {};
  const maxCount = Math.max(...rows.map((row) => number(row.count) || 0), 1);
  const fallbackX = (index) => layout.left + (index + 1) * (layout.right - layout.left) / Math.max(rows.length + 1, 1);
  const xForRow = (row, index) => number(row.pixel_x) ?? fallbackX(index);
  const y = linearScale(0, maxCount, layout.barsBottom, layout.barsTop);
  const fallbackSetY = (index) => layout.matrixTop + index * (layout.matrixBottom - layout.matrixTop) / Math.max(1, order.length - 1);
  const yForSet = (name, index) => number(totals[name]?.pixel_y) ?? fallbackSetY(index);
  const yValues = order.map((name, index) => yForSet(name, index));
  const rowSteps = yValues.slice(1).map((value, index) => value - yValues[index]).sort((a, b) => a - b);
  const rowStep = rowSteps[Math.floor(rowSteps.length / 2)] || 21;
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  const step = spec.yTickStep || Math.max(1, Math.ceil(maxCount / 6 / 10) * 10);
  for (let tick = 0; tick <= 900; tick += step) { const py = y(tick); paperLine(layout.left - 9, py, layout.left, py, { stroke: "#333", "stroke-width": 2 }); paperText(String(tick), layout.left - 15, py, { "font-size": spec.tickFontSize || 22, "text-anchor": "end", "dominant-baseline": "middle", fill: "#333" }); }
  paperLine(layout.left, 0, layout.left, layout.barsBottom, { stroke: "#333", "stroke-width": 2 });
  paperLine(layout.left, layout.barsBottom, layout.right, layout.barsBottom, { stroke: "#333", "stroke-width": 2 });
  rows.forEach((row, index) => {
    const cx = xForRow(row, index); const top = number(row.bar_top_y_px) ?? y(number(row.count)); const bottom = number(row.bar_bottom_y_px) ?? layout.barsBottom; const barWidth = spec.barWidth || 25;
    makeMark("rect", { x: cx - barWidth / 2, y: top, width: barWidth, height: bottom - top, fill: "#3b3b3b" }, exactTooltip([["intersection", row.intersection], ["members", row.members], ["count", row.count], ["pixel x", row.pixel_x], ["status", "visible printed count + original-pixel geometry"]]));
    paperText(row.count, cx + 4, top - 18, { "font-size": spec.countFontSize || 21, "text-anchor": "start", "dominant-baseline": "middle", transform: `rotate(45 ${cx + 4} ${top - 18})`, fill: "#333" });
  });
  order.forEach((name, rowIndex) => { if (rowIndex % 2) appendSvg("rect", { x: layout.left, y: yValues[rowIndex] - rowStep / 2, width: layout.right - layout.left, height: rowStep, fill: "#f3f3f3" }); });
  rows.forEach((row, index) => { const cx = xForRow(row, index); order.forEach((name, rowIndex) => appendSvg("circle", { cx, cy: yValues[rowIndex], r: spec.inactiveRadius || 8.2, fill: "#e9e9e9" })); });
  rows.forEach((row, index) => {
    const cx = xForRow(row, index); const members = new Set(String(row.members || "").split(";").filter(Boolean)); const active = order.map((name, rowIndex) => members.has(name) ? rowIndex : null).filter((value) => value !== null);
    if (active.length > 1) paperLine(cx, yValues[active[0]], cx, yValues[active[active.length - 1]], { stroke: "#3b3b3b", "stroke-width": spec.connectorWidth || 4.2 });
    active.forEach((rowIndex) => makeMark("circle", { cx, cy: yValues[rowIndex], r: spec.activeRadius || 8.5, fill: colors[order[rowIndex]] || "#3b3b3b" }, exactTooltip([["intersection", row.intersection], ["set", order[rowIndex]], ["present", "yes"], ["count", row.count], ["source", "original-pixel dark-node support"]])));
  });
  const leftScale = (value) => layout.leftBarsRight - value * (layout.leftBarsWidth || 368) / 1250;
  order.forEach((name, rowIndex) => {
    const py = yValues[rowIndex]; const total = totals[name];
    paperText(name, layout.left - 15, py, { "font-size": spec.setFontSize || 20, "text-anchor": "end", "dominant-baseline": "middle", fill: "#333" });
    if (!total) return;
    const left = number(total.left_bar_left_px) ?? leftScale(number(total.value)); const right = number(total.left_bar_right_px) ?? layout.leftBarsRight;
    makeMark("rect", { x: left, y: py - (spec.setBarHeight || 11) / 2, width: right - left, height: spec.setBarHeight || 11, fill: colors[name] || spec.setBarColor || "#56b4e9" }, exactTooltip([["set", name], ["tumour type", total.tumour_type], ["total from visible intersections", total.value], ["left-bar pixel estimate", total.left_bar_pixel_estimate], ["pixel error", total.pixel_error], ["status", total.visible_geometry_status]]));
  });
  const leftAxisY = yValues[yValues.length - 1] + rowStep / 2 + 6;
  paperLine(leftScale(1250) - 14, leftAxisY, leftScale(0), leftAxisY, { stroke: "#333", "stroke-width": 2 });
  (spec.leftTicks || [1250, 1000, 750, 500, 250, 0]).forEach((tick) => { const px = leftScale(tick); paperLine(px, leftAxisY, px, leftAxisY + 8, { stroke: "#333", "stroke-width": 2 }); paperText(String(tick), px, leftAxisY + 24, { "font-size": 20, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#333" }); });
  paperText("number of mutations in each region", (leftScale(1250) + leftScale(0)) / 2, leftAxisY + 56, { "font-size": 24, "text-anchor": "middle", "dominant-baseline": "middle", fill: "#333" });
  order.forEach((name, rowIndex) => { const total = totals[name]; const tumourType = total?.tumour_type; if (!tumourType) return; const color = typeColors[tumourType] || "#777"; appendSvg("rect", { x: layout.typeStripX, y: yValues[rowIndex] - rowStep / 2, width: layout.typeStripWidth, height: rowStep, fill: color }); paperText(tumourType === "NSCLC-NOS" ? "NSCLC–NOS" : tumourType, layout.typeTextX, yValues[rowIndex], { "font-size": 20, "text-anchor": "start", "dominant-baseline": "middle", fill: color }); });
  if (spec.yLabel) paperText(spec.yLabel, spec.yLabelX || 35, layout.barsBottom / 2, { "font-size": spec.yLabelSize || 25, "text-anchor": "middle", transform: `rotate(-90 ${spec.yLabelX || 35} ${layout.barsBottom / 2})`, fill: "#222" });
  interactiveNote.textContent = spec.note;
}

function renderPaperPolarHistogram(sample, table) {
  const spec = sample.styleSpec;
  const color = spec.color || "#0b72b9";
  const gridColor = spec.gridColor || "#e0e1e2";
  const textColor = spec.textColor || "#303030";
  const panelEntries = Object.entries(spec.panels || {});
  setChartCanvas(spec.canvas.width, spec.canvas.height, spec.fontFamily);
  appendSvg("rect", { x: 0, y: 0, width: spec.canvas.width, height: spec.canvas.height, fill: "#fff" });
  paperText("f", 0, 31, { "font-size": 34, "font-weight": 700, fill: textColor });
  paperText("Orientation of the force w.r.t extrusion site (angle θ)", spec.canvas.width / 2, 34, {
    "font-size": 35,
    "text-anchor": "middle",
    fill: textColor,
  });

  const point = (panel, value, angle) => {
    const radians = (angle * Math.PI) / 180;
    return [
      panel.cx + panel.xPxPerUnit * value * Math.cos(radians),
      panel.cy - panel.yPxPerUnit * value * Math.sin(radians),
    ];
  };
  const arcPath = (panel, value) => {
    const points = Array.from({ length: 61 }, (_, index) => point(panel, value, index * 3));
    return points.map(([x, y], index) => `${index ? "L" : "M"}${x.toFixed(2)},${y.toFixed(2)}`).join(" ");
  };

  panelEntries.forEach(([panelId, panel]) => {
    [...panel.radialTicks, panel.radialMax].forEach((tick) => {
      appendSvg("path", {
        d: arcPath(panel, tick),
        fill: "none",
        stroke: gridColor,
        "stroke-width": 2,
        "vector-effect": "non-scaling-stroke",
        "pointer-events": "none",
      });
    });
    for (let angle = 0; angle <= 180; angle += 30) {
      const [x, y] = point(panel, panel.radialMax, angle);
      paperLine(panel.cx, panel.cy, x, y, { stroke: gridColor, "stroke-width": 2, "pointer-events": "none" });
      const radians = (angle * Math.PI) / 180;
      const labelX = panel.cx + (panel.xPxPerUnit * panel.radialMax + 24) * Math.cos(radians);
      const labelY = panel.cy - (panel.yPxPerUnit * panel.radialMax + 20) * Math.sin(radians);
      paperText(String(angle), labelX, labelY + 5, {
        "font-size": 18,
        "text-anchor": "middle",
        fill: "#4c4c4c",
        "pointer-events": "none",
      });
    }
    paperText("0", panel.cx, panel.cy + 24, { "font-size": 18, "text-anchor": "middle", fill: "#4c4c4c", "pointer-events": "none" });
    panel.radialTicks.forEach((tick) => {
      paperText(String(tick), panel.cx + panel.xPxPerUnit * tick, panel.cy + 24, {
        "font-size": 18,
        "text-anchor": "middle",
        fill: "#4c4c4c",
        "pointer-events": "none",
      });
    });

    table.rows.filter((row) => row.panel_id === panelId).forEach((row, index) => {
      const value = number(row.radial_value);
      const start = number(row.theta_start_deg);
      const end = number(row.theta_end_deg);
      if (value === null || start === null || end === null) return;
      const [x1, y1] = point(panel, value, start);
      const [x2, y2] = point(panel, value, end);
      const tooltip = exactTooltip([
        ["panel", row.panel_id],
        ["patch diameter (μm)", row.patch_diameter_um],
        ["theta interval (deg)", `${row.theta_start_deg}–${row.theta_end_deg}`],
        ["theta midpoint (deg)", row.theta_mid_deg],
        ["direction", row.direction_class],
        ["radial value", row.radial_value],
        ["approx uncertainty", row.radial_uncertainty_approx],
        ["radial unit", row.radial_unit],
        ["chord p1 original px", `${row.chord_x1_px}, ${row.chord_y1_px}`],
        ["chord p2 original px", `${row.chord_x2_px}, ${row.chord_y2_px}`],
        ["support pixels", row.support_pixels],
        ["status", row.reason_code],
      ]);
      makeMark("path", {
        d: `M${panel.cx},${panel.cy} L${x1},${y1} L${x2},${y2} Z`,
        fill: "rgba(11, 114, 185, 0.035)",
        stroke: color,
        "stroke-width": 3,
        "vector-effect": "non-scaling-stroke",
        tabindex: index % 2 === 0 ? 0 : -1,
      }, tooltip);
    });
    paperText(panel.label, panel.cx, spec.panelLabelY || 298, {
      "font-size": 26,
      "text-anchor": "middle",
      fill: textColor,
      "pointer-events": "none",
    });
  });
  interactiveNote.textContent = spec.note;
}

function renderInteractiveChart(sample, table, layers = {}) {
  clearChart();
    dataChart.setAttribute("aria-label", `${displayType(sample)}的交互式图`);
  if (sample.styleSpec?.rasterEvidenceInteractive) {
    renderRasterEvidenceInteractive(sample, table);
    dataChart.setAttribute("aria-label", `${displayType(sample)}的交互式原图风格复现`);
    return;
  }
  const styleRenderers = {
    "paper-dose-response": () => renderPaperDoseResponse(sample, table, layers),
    "paper-heatmap": () => renderPaperHeatmap(sample, table),
    "paper-boxplot": () => renderPaperBoxplot(sample, table),
    "paper-multifacet-boxplot": () => renderPaperMultiPanelBoxplot(sample, table),
    "paper-grouped-bar": () => renderPaperGroupedBar(sample, table),
    "paper-dual-axis-bar-line": () => renderPaperDualAxisBarLine(sample, table),
    "paper-bar-dot": () => renderPaperBarDot(sample, table),
    "paper-source-line": () => renderPaperSourceLine(sample, table),
    "paper-native-trace-line": () => renderNativeTraceLine(sample, table),
    "paper-native-geometry": () => renderNativeGeometry(sample, table),
    "paper-visible-bars": () => renderPaperVisibleBars(sample, table),
    "paper-four-panel-line": () => renderPaperFourPanelLine(sample, table),
    "paper-clinical-bars": () => renderPaperClinicalBars(sample, table),
    "paper-bubble-matrix": () => renderPaperBubbleMatrix(sample, table),
    "paper-upset": () => renderPaperUpset(sample, table),
    "paper-visible-upset": () => renderPaperSourceUpset(sample, table),
    "paper-polar-histogram": () => renderPaperPolarHistogram(sample, table),
  };
  const styleRenderer = styleRenderers[sample.styleSpec?.renderer];
  if (styleRenderer) {
    styleRenderer();
    dataChart.setAttribute("aria-label", `${displayType(sample)}的交互式原图风格复现`);
    return;
  }
  const renderers = {
    line: () => renderLineChart(table),
    scatter: () => renderScatterChart(table),
    "dose-response": () => renderDoseResponse(table),
    bar: () => renderVerticalBars(table, false),
    "bar-horizontal": () => renderHorizontalBars(table, false),
    "bar-stacked": () => renderVerticalBars(table, true),
    "bar-percent-stacked": () => renderHorizontalBars(table, true),
    histogram: () => renderHistogram(table),
    heatmap: () => renderHeatmap(table),
    boxplot: () => renderVerticalBoxplot(table),
    "boxplot-horizontal": () => renderHorizontalBoxplot(table),
    forest: () => renderForest(table),
  };
  const renderer = renderers[sample.id];
  if (renderer) renderer();
  else clearChart("此类型暂不提供交互数据图；CSV 仍可查看和下载。");
}

function tooltipTarget(event) {
  return event.target.closest?.("[data-tooltip]");
}

function positionTooltip(clientX, clientY) {
  const bounds = interactiveChart.getBoundingClientRect();
  const left = Math.max(8, Math.min(clientX - bounds.left + 14, bounds.width - 324));
  const top = Math.max(8, Math.min(clientY - bounds.top + 14, bounds.height - 90));
  chartTooltip.style.left = `${left}px`;
  chartTooltip.style.top = `${top}px`;
}

function showTooltip(target, clientX, clientY) {
  chartTooltip.textContent = target.dataset.tooltip;
  interactiveReadout.textContent = target.dataset.tooltip;
  chartTooltip.classList.add("is-visible");
  positionTooltip(clientX, clientY);
}

interactiveChart.addEventListener("pointermove", (event) => {
  const target = tooltipTarget(event);
  if (!target) {
    chartTooltip.classList.remove("is-visible");
    return;
  }
  showTooltip(target, event.clientX, event.clientY);
});

interactiveChart.addEventListener("pointerleave", () => chartTooltip.classList.remove("is-visible"));
interactiveChart.addEventListener("focusin", (event) => {
  const target = tooltipTarget(event);
  if (!target) return;
  const bounds = target.getBoundingClientRect();
  showTooltip(target, bounds.left + bounds.width / 2, bounds.top + bounds.height / 2);
});
interactiveChart.addEventListener("focusout", () => chartTooltip.classList.remove("is-visible"));

let dragState = null;
dataViewport.addEventListener("pointerdown", (event) => {
  if (event.pointerType !== "mouse" || event.button !== 0) return;
  dragState = {
    pointerId: event.pointerId,
    x: event.clientX,
    y: event.clientY,
    left: dataViewport.scrollLeft,
    top: dataViewport.scrollTop,
  };
  dataViewport.setPointerCapture(event.pointerId);
  dataViewport.classList.add("is-dragging");
});

dataViewport.addEventListener("pointermove", (event) => {
  if (!dragState || event.pointerId !== dragState.pointerId) return;
  dataViewport.scrollLeft = dragState.left - (event.clientX - dragState.x);
  dataViewport.scrollTop = dragState.top - (event.clientY - dragState.y);
});

function endDrag(event) {
  if (!dragState || event.pointerId !== dragState.pointerId) return;
  dragState = null;
  dataViewport.classList.remove("is-dragging");
}

dataViewport.addEventListener("pointerup", endDrag);
dataViewport.addEventListener("pointercancel", endDrag);

document.addEventListener("click", (event) => {
  const filter = event.target.closest(".filter-button");
  if (filter) {
    document.querySelectorAll(".filter-button").forEach((button) => button.classList.toggle("is-active", button === filter));
    applyFilter(filter.dataset.filter);
    return;
  }

  const card = event.target.closest(".type-card");
  if (card) {
    const sample = samples.find((item) => item.id === card.dataset.caseId);
    if (sample) openCase(sample);
    return;
  }

  const viewTab = event.target.closest(".view-tab");
  if (viewTab) setImageView(viewTab.dataset.view);

  const recreationTab = event.target.closest(".recreation-tab");
  if (recreationTab) setRecreationView(recreationTab.dataset.recreationView);
});

caseDialog.querySelector(".close-button").addEventListener("click", () => closeCase());
caseDialog.addEventListener("click", (event) => {
  if (event.target === caseDialog) closeCase();
});
caseDialog.addEventListener("cancel", (event) => {
  event.preventDefault();
  closeCase();
});

window.addEventListener("popstate", () => {
  const id = location.hash.replace(/^#basic-/, "");
  const sample = samples.find((item) => item.id === id);
  if (sample) openCase(sample, false);
  else if (caseDialog.open) closeCase(false);
});

fetch("data/basics.json")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((manifest) => {
    // Every public recreation is driven only by geometry read from the image.
    samples = manifest.samples;
    renderCards(samples);
    applyFilter("all");
    const id = location.hash.replace(/^#basic-/, "");
    const sample = samples.find((item) => item.id === id);
    if (sample) requestAnimationFrame(() => openCase(sample, false));
  })
  .catch((error) => {
    typeGrid.innerHTML = `<p class="error-message">基础证据载入失败：${escapeHtml(error.message)}</p>`;
    catalogCount.textContent = "0 个案例";
  });
