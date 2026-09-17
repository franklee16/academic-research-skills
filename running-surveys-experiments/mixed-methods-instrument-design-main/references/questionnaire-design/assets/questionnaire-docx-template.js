#!/usr/bin/env node
"use strict";

/**
 * Generate academically reviewable questionnaire DOCX files from questionnaire-spec.json.
 *
 * Usage:
 *   node questionnaire-docx-template.js path/to/questionnaire-spec.json output-directory
 *
 * Outputs:
 *   01_问卷_研究者版_[title].docx
 *   02_问卷_实施版_[form]_[population]_[language]_[mode].docx
 *
 * One field document is generated for each entry in `forms`. The researcher version
 * contains provenance, RQ/construct mappings, routing, and validation status. Field
 * versions intentionally exclude those internal annotations.
 */

const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  Header,
  HeadingLevel,
  PageBreak,
  PageNumber,
  Packer,
  Paragraph,
  ShadingType,
  TabStopPosition,
  TabStopType,
  Table,
  TableCell,
  TableLayoutType,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require("docx");

const FONT_CN = "宋体";
const FONT_HEADING = "黑体";
const FONT_LATIN = "Times New Roman";
const BODY_FONT = { ascii: FONT_LATIN, hAnsi: FONT_LATIN, eastAsia: FONT_CN, cs: FONT_LATIN };
const HEADING_FONT = { ascii: FONT_LATIN, hAnsi: FONT_LATIN, eastAsia: FONT_HEADING, cs: FONT_LATIN };
const PAGE_WIDTH = 11906;
const PAGE_HEIGHT = 16838;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2;

const COLORS = {
  ink: "1F2937",
  muted: "667085",
  line: "B8C2CC",
  pale: "EEF4F8",
  paleBlue: "DCEAF3",
  blue: "28566F",
  warning: "FFF4CE",
  white: "FFFFFF",
};

const MISSING_LABELS = {
  dont_know: "不知道",
  not_applicable: "不适用",
  refused: "不愿回答",
  not_shown: "未展示（系统状态）",
  missing: "未回答",
};

const thinBorder = { style: BorderStyle.SINGLE, size: 4, color: COLORS.line };
const cellBorders = {
  top: thinBorder,
  bottom: thinBorder,
  left: thinBorder,
  right: thinBorder,
};

function value(value, fallback = "[待填写]") {
  if (value === null || value === undefined || value === "") return fallback;
  if (Array.isArray(value)) {
    if (!value.length) return fallback;
    return value.map((entry) => {
      if (entry && typeof entry === "object") {
        return Object.entries(entry).map(([key, item]) => `${key}=${valueString(item)}`).join("，");
      }
      return String(entry);
    }).join("；");
  }
  if (typeof value === "object") return JSON.stringify(value, null, 0);
  if (typeof value === "boolean") return value ? "是" : "否";
  return String(value);
}

function valueString(item) {
  if (item === null || item === undefined) return "";
  if (Array.isArray(item)) return item.join("/");
  if (typeof item === "object") return JSON.stringify(item, null, 0);
  return String(item);
}

function safeFilePart(text) {
  return value(text, "未命名问卷")
    .replace(/[\\/:*?"<>|\[\]]/g, "")
    .replace(/\s+/g, "-")
    .slice(0, 72) || "未命名问卷";
}

function textRun(text, options = {}) {
  return new TextRun({
    text: value(text, ""),
    font: options.font || BODY_FONT,
    size: options.size || 21,
    bold: options.bold,
    italics: options.italics,
    color: options.color || COLORS.ink,
  });
}

function paragraph(text, options = {}) {
  const children = options.children || [textRun(text, options)];
  return new Paragraph({
    children,
    alignment: options.align,
    heading: options.heading,
    keepNext: options.keepNext,
    keepLines: options.keepLines,
    pageBreakBefore: options.pageBreakBefore,
    indent: options.indent,
    spacing: {
      before: options.before ?? 0,
      after: options.after ?? 90,
      line: options.line ?? 320,
    },
    border: options.border,
    tabStops: options.tabStops,
  });
}

function heading(text, level = HeadingLevel.HEADING_1) {
  const isH1 = level === HeadingLevel.HEADING_1;
  return paragraph(text, {
    heading: level,
    font: HEADING_FONT,
    size: isH1 ? 30 : 25,
    bold: true,
    color: COLORS.blue,
    before: isH1 ? 240 : 180,
    after: isH1 ? 150 : 100,
    keepNext: true,
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function cell(children, width, options = {}) {
  return new TableCell({
    children: Array.isArray(children) ? children : [paragraph(children, { after: 0 })],
    width: { size: width, type: WidthType.DXA },
    borders: options.borders || cellBorders,
    shading: options.fill
      ? { fill: options.fill, type: ShadingType.CLEAR }
      : undefined,
    margins: { top: 90, bottom: 90, left: 120, right: 120 },
    verticalAlign: options.verticalAlign || VerticalAlign.CENTER,
  });
}

function table(rows, widths, options = {}) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    rows: rows.map((row, rowIndex) =>
      new TableRow({
        cantSplit: true,
        tableHeader: Boolean(options.header && rowIndex === 0),
        children: row.map((entry, columnIndex) => {
          if (entry instanceof TableCell) return entry;
          const descriptor = typeof entry === "object" && !Array.isArray(entry)
            ? entry
            : { text: entry };
          const children = descriptor.children || [paragraph(descriptor.text, {
            after: 0,
            bold: descriptor.bold,
            color: descriptor.color,
            size: descriptor.size,
            font: descriptor.font,
          })];
          return cell(children, widths[columnIndex], {
            fill: descriptor.fill,
            verticalAlign: descriptor.verticalAlign,
          });
        }),
      })
    ),
  });
}

function labelValueTable(pairs) {
  const rows = pairs.map(([label, content]) => [
    { text: label, bold: true, fill: COLORS.pale },
    { text: value(content) },
  ]);
  return table(rows, [2100, CONTENT_WIDTH - 2100]);
}

function makeHeader(title, version, label) {
  return new Header({
    children: [
      paragraph("", {
        after: 80,
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.blue, space: 1 } },
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          textRun(value(title), { size: 18, color: COLORS.muted }),
          textRun(`\t${label} · ${value(version)}`, { size: 18, color: COLORS.muted }),
        ],
      }),
    ],
  });
}

function makeFooter(controlText) {
  return new Footer({
    children: [
      paragraph("", {
        before: 70,
        after: 0,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLORS.line, space: 1 } },
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          textRun(controlText, { size: 17, color: COLORS.muted }),
          textRun("\t第 ", { size: 17, color: COLORS.muted }),
          new TextRun({ children: [PageNumber.CURRENT], font: FONT_LATIN, size: 17, color: COLORS.muted }),
          textRun(" 页，共 ", { size: 17, color: COLORS.muted }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT_LATIN, size: 17, color: COLORS.muted }),
          textRun(" 页", { size: 17, color: COLORS.muted }),
        ],
      }),
    ],
  });
}

function documentStyles() {
  return {
    default: {
      document: { run: { font: BODY_FONT, size: 21, color: COLORS.ink } },
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: HEADING_FONT, size: 30, bold: true, color: COLORS.blue },
        paragraph: { spacing: { before: 240, after: 150 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: HEADING_FONT, size: 25, bold: true, color: COLORS.blue },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 },
      },
    ],
  };
}

function baseSection(children, title, version, label, controlText) {
  return {
    properties: {
      page: {
        size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN, header: 850, footer: 850 },
      },
    },
    headers: { default: makeHeader(title, version, label) },
    footers: { default: makeFooter(controlText) },
    children,
  };
}

function cover(title, subtitle, metadata, note) {
  const children = [
    paragraph(title, {
      align: AlignmentType.CENTER,
      font: HEADING_FONT,
      size: 36,
      bold: true,
      color: COLORS.blue,
      before: 1200,
      after: 160,
      keepNext: true,
    }),
    paragraph(subtitle, {
      align: AlignmentType.CENTER,
      size: 23,
      color: COLORS.muted,
      after: 600,
    }),
    labelValueTable(metadata),
  ];
  if (note) {
    children.push(paragraph(note, {
      before: 240,
      after: 0,
      size: 19,
      color: COLORS.muted,
      italics: true,
      align: AlignmentType.CENTER,
    }));
  }
  children.push(pageBreak());
  return children;
}

function optionText(item, includeCodes) {
  const options = Array.isArray(item.response_options) ? item.response_options : [];
  if (!options.length) return "[无预设选项]";
  return options.map((option) => {
    const code = includeCodes ? `${value(option.code, "NA")}: ` : "";
    return `${code}${value(option.label)}`;
  }).join("；");
}

function visibleMissingOptions(item, includeCodes = false) {
  const missing = item.missing_codes && typeof item.missing_codes === "object" ? item.missing_codes : {};
  const display = Array.isArray(item.missing_display) ? item.missing_display : [];
  return display
    .filter((key) => Object.prototype.hasOwnProperty.call(missing, key))
    .map((key) => {
      const label = MISSING_LABELS[key] || key;
      return includeCodes ? `${value(missing[key], "NA")}: ${label}` : label;
    });
}

function requirementLabel(item) {
  if (item.required === false) return "选答";
  if (Array.isArray(item.missing_display) && item.missing_display.includes("refused")) {
    return "请作答（可选不愿回答）";
  }
  return "必答";
}

function internalItemTable(item) {
  const rows = [
    [
      { text: `${value(item.id)}　${value(item.variable_name)}`, bold: true, fill: COLORS.paleBlue },
      { text: `${value(item.response_type)} · ${requirementLabel(item)}`, fill: COLORS.paleBlue },
    ],
    ["正式题面", value(item.question_text)],
    ["受访者说明", value(item.instruction, "无")],
    ["响应选项/编码", optionText(item, true)],
    ["RQ / 构念", `${value(item.rq_ids)} / ${value(item.construct_ids)}`],
    ["人群 / universe", `${value(item.population_ids)} / ${value(item.universe)}`],
    ["回忆期 / 参照", `${value(item.recall_period)} / ${value(item.referent)}`],
    ["显示 / 跳题", `${value(item.display_logic)} / ${value(item.skip_logic)}`],
    ["校验 / 错误提示", `${value(item.validation_rule, "未设置")} / ${value(item.error_message, "未设置")}`],
    ["缺失编码", value(item.missing_codes)],
    ["现场显示的缺失选项", value(visibleMissingOptions(item, true), "无")],
    ["随机化 / piping", `${value(item.randomization, "none")} / ${value(item.piping, "none")}`],
    ["来源 / 许可", `${value(item.source_status)}；${value(item.source, "无外部来源")}；${value(item.license_status)}`],
    ["验证状态", value(item.validation_status)],
    ["计分 / 派生", `${value(item.scoring, "not-applicable")} / ${value(item.derived_variable, "none")}`],
    ["分析用途", value(item.analysis_use)],
    ["变更记录", value(item.change_log, "尚无")],
  ];
  return table(rows, [2100, CONTENT_WIDTH - 2100], { header: true });
}

function researcherDocument(spec) {
  const instrument = spec.instrument || {};
  const participants = spec.participant_materials || {};
  const children = [];

  children.push(...cover(
    `${value(instrument.title)}（研究者设计版）`,
    "问卷方法、题项来源、编程逻辑与验证状态的受控主文档",
    [
      ["工具类型", instrument.instrument_type],
      ["版本 / 状态", `${value(instrument.version)} / ${value(instrument.status)}`],
      ["目标人群", instrument.target_population_ids],
      ["语言 / 模式", `${value(instrument.languages)} / ${value(instrument.modes)}`],
      ["抽样路径", instrument.sampling_approach],
      ["伦理状态", instrument.ethics_review_status],
      ["隐私模型", instrument.privacy_model],
    ],
    "研究者内部使用。正式实施前须完成适用的伦理审查、目标人群认知访谈、可用性测试、pilot 与测量验证。"
  ));

  children.push(heading("1. 边界与推论范围"));
  children.push(table([
    [{
      children: [
        paragraph("方法边界", { bold: true, color: COLORS.blue, after: 60 }),
        paragraph("本文件记录问卷设计和实施规格，不证明抽样代表性，也不表示题项已经通过认知测试、pilot 或正式测量验证。", { after: 0 }),
      ],
      fill: COLORS.warning,
    }],
  ], [CONTENT_WIDTH]));
  children.push(paragraph("预期推论及边界", { bold: true, before: 140, keepNext: true }));
  children.push(paragraph(value(instrument.inference_scope)));

  children.push(heading("2. 参与者材料与实施版本"));
  children.push(labelValueTable([
    ["研究机构/团队", participants.organization],
    ["面向参与者的研究目的", participants.study_purpose],
    ["预计完成时间", participants.estimated_minutes],
    ["参与方式", participants.voluntary_statement],
    ["隐私说明", participants.privacy_statement],
    ["同意方式", participants.consent_mode],
    ["联系信息", participants.contact],
    ["结束语", participants.completion_message],
  ]));

  children.push(heading("3. 研究问题"));
  const rqRows = [[
    { text: "RQ", bold: true, fill: COLORS.paleBlue },
    { text: "研究问题", bold: true, fill: COLORS.paleBlue },
  ]];
  for (const rq of spec.research_questions || []) rqRows.push([value(rq.id), value(rq.text)]);
  children.push(table(rqRows, [1300, CONTENT_WIDTH - 1300], { header: true }));

  children.push(heading("4. 总体、回答者与分析单位"));
  const populationRows = [[
    { text: "ID", bold: true, fill: COLORS.paleBlue },
    { text: "目标人群", bold: true, fill: COLORS.paleBlue },
    { text: "回答者角色", bold: true, fill: COLORS.paleBlue },
    { text: "观察/分析单位", bold: true, fill: COLORS.paleBlue },
  ]];
  for (const population of spec.populations || []) {
    populationRows.push([
      value(population.id),
      value(population.label),
      value(population.respondent_role),
      `${value(population.observation_unit)} / ${value(population.analysis_unit)}`,
    ]);
  }
  children.push(table(populationRows, [900, 2800, 1900, CONTENT_WIDTH - 5600], { header: true }));

  children.push(heading("5. 构念与变量域"));
  const constructRows = [[
    { text: "ID / 名称", bold: true, fill: COLORS.paleBlue },
    { text: "操作性定义", bold: true, fill: COLORS.paleBlue },
    { text: "类型 / RQ", bold: true, fill: COLORS.paleBlue },
  ]];
  for (const construct of spec.constructs || []) {
    constructRows.push([
      `${value(construct.id)} / ${value(construct.label)}`,
      value(construct.definition),
      `${value(construct.kind)} / ${value(construct.rq_ids)}`,
    ]);
  }
  children.push(table(constructRows, [2200, 4300, CONTENT_WIDTH - 6500], { header: true }));

  children.push(heading("6. 实施分版"));
  const formRows = [[
    { text: "Form", bold: true, fill: COLORS.paleBlue },
    { text: "人群", bold: true, fill: COLORS.paleBlue },
    { text: "语言 / 模式", bold: true, fill: COLORS.paleBlue },
    { text: "说明", bold: true, fill: COLORS.paleBlue },
  ]];
  for (const form of normalizedForms(spec)) {
    formRows.push([
      value(form.id),
      value(form.population_id),
      `${value(form.language)} / ${value(form.mode)}`,
      `${value(form.title)}；${value(form.instructions)}`,
    ]);
  }
  children.push(table(formRows, [1100, 1200, 2300, CONTENT_WIDTH - 4600], { header: true }));

  children.push(heading("7. 逐题规格与证据状态"));
  for (const item of spec.items || []) {
    children.push(heading(`${value(item.id)}　${value(item.question_text)}`, HeadingLevel.HEADING_2));
    children.push(internalItemTable(item));
    children.push(paragraph("", { after: 80 }));
  }

  children.push(heading("8. 测试、验证与数据治理"));
  const testing = spec.testing || {};
  const measurement = spec.measurement_validation || {};
  const quality = spec.data_quality || {};
  const governance = spec.governance || {};
  children.push(labelValueTable([
    ["专家审查", testing.expert_review],
    ["认知访谈", testing.cognitive_interviewing],
    ["可用性测试", testing.usability_testing],
    ["Field pilot", testing.field_pilot],
    ["路径测试", testing.path_test_cases],
    ["测量验证是否需要", measurement.required],
    ["验证理由", measurement.rationale],
    ["计划证据", measurement.planned_evidence],
    ["预定义质量规则", quality.predefined_rules],
    ["敏感性分析", quality.sensitivity_analysis],
    ["最小必要审查", governance.data_minimization_review],
    ["联系信息分离", governance.contact_data_separated],
    ["保存与删除", governance.retention_plan],
  ]));

  children.push(heading("9. 发布签署与实施前闸门"));
  for (const text of [
    "逐题来源、原文、许可、翻译与改编状态已经核验并记录。",
    "所有目标人群、语言与模式已经完成适用的认知访谈和可用性测试。",
    "全部显示、跳题、回流、随机化、校验与导出路径已经通过测试。",
    "抽样、无应答、在线质量、伦理、隐私、保存和删除方案已经批准。",
    "如涉及量表、测验、筛查、阈值或跨群体比较，已完成用途所需的测量证据计划。",
  ]) children.push(paragraph(`□ ${text}`, { indent: { left: 260 }, after: 85 }));
  children.push(paragraph("方法负责人：________________　伦理/治理复核：________________　批准日期：________________", { before: 180 }));

  return new Document({
    styles: documentStyles(),
    sections: [baseSection(
      children,
      instrument.title,
      instrument.version,
      "研究者设计版",
      `内部受控文件 · ${value(instrument.status)}`
    )],
  });
}

function blankAnswerLines(count = 4) {
  const rows = [];
  for (let index = 0; index < count; index += 1) {
    rows.push(paragraph("　", {
      after: 90,
      border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: COLORS.line, space: 1 } },
    }));
  }
  return rows;
}

function responseControls(item) {
  const type = item.response_type;
  const options = Array.isArray(item.response_options) ? item.response_options : [];
  const missing = visibleMissingOptions(item).map((label) =>
    paragraph(`□ ${label}`, { after: 65, indent: { left: 180 }, color: COLORS.muted })
  );
  if (["single-choice", "multiple-choice", "ordinal-rating"].includes(type)) {
    const substantive = options.length
      ? options.map((option) => paragraph(`□ ${value(option.label)}`, { after: 65, indent: { left: 180 } }))
      : [paragraph("□ [选项待填写]", { indent: { left: 180 } })];
    return [...substantive, ...missing];
  }
  if (type === "ranking" || type === "constant-sum") {
    const header = type === "ranking" ? "排序" : "分配值";
    const substantive = options.length
      ? options.map((option) => paragraph(`${value(option.label)}　　${header}：________`, { after: 70, indent: { left: 180 } }))
      : [paragraph(`[选项待填写]　　${header}：________`, { indent: { left: 180 } })];
    return [...substantive, ...missing];
  }
  if (type === "open-text") return [...blankAnswerLines(4), ...missing];
  if (type === "date-or-time") return [paragraph("日期/时间：________年____月____日　____时____分", { indent: { left: 180 } }), ...missing];
  if (type === "numeric") return [paragraph("填写数值：____________________", { indent: { left: 180 } }), ...missing];
  return [paragraph("作答：____________________________", { indent: { left: 180 } }), ...missing];
}

function fieldQuestion(item, mode) {
  const top = paragraph("", {
    after: 0,
    keepNext: true,
    children: [
      textRun(value(item.id), { bold: true, color: COLORS.white, size: 22 }),
      textRun(`　${requirementLabel(item)}`, { color: COLORS.white, size: 17 }),
    ],
  });
  const body = [];
  if (item.instruction) body.push(paragraph(value(item.instruction), { size: 19, color: COLORS.muted, italics: true, after: 55 }));
  body.push(paragraph(value(item.question_text), { bold: true, size: 23, after: 100, keepNext: true, keepLines: true }));
  body.push(...responseControls(item));
  if (item.help_text) body.push(paragraph(`说明：${value(item.help_text)}`, { size: 18, color: COLORS.muted, before: 50 }));
  if (/paper|phone|interview|capi|cati|访员/i.test(value(mode, "")) && item.skip_logic && item.skip_logic !== "next") {
    body.push(paragraph(`跳转提示：${value(item.skip_logic)}`, { size: 18, bold: true, color: COLORS.blue, before: 50 }));
  }
  return table([
    [cell([top], CONTENT_WIDTH, { fill: COLORS.blue })],
    [cell(body, CONTENT_WIDTH)],
  ], [CONTENT_WIDTH]);
}

function normalizedForms(spec) {
  if (Array.isArray(spec.forms) && spec.forms.length) return spec.forms;
  const instrument = spec.instrument || {};
  const population = (instrument.target_population_ids || ["P1"])[0];
  const language = (instrument.languages || ["zh-CN"])[0];
  const mode = (instrument.modes || ["paper-self-administered"])[0];
  console.warn("WARNING: forms is missing; generated one fallback form from the first population/language/mode.");
  return [{
    id: "F1",
    population_id: population,
    language,
    mode,
    title: instrument.title,
    introduction: "[请填写该实施版本的导语]",
    instructions: "[请填写该实施版本的作答或访员说明]",
  }];
}

function formItems(spec, form) {
  return (spec.items || []).filter((item) =>
    Array.isArray(item.population_ids) && item.population_ids.includes(form.population_id)
  );
}

function fieldDocument(spec, form) {
  const instrument = spec.instrument || {};
  const participants = spec.participant_materials || {};
  const population = (spec.populations || []).find((entry) => entry.id === form.population_id) || {};
  const items = formItems(spec, form);
  const sections = Array.isArray(spec.sections) && spec.sections.length
    ? spec.sections.filter((entry) => !entry.population_ids || entry.population_ids.includes(form.population_id))
    : [{ id: "DEFAULT", title: "正式问卷", introduction: "" }];
  const sectionIds = new Set(sections.map((entry) => entry.id));
  const children = [];

  children.push(...cover(
    value(form.title, instrument.title),
    "调查问卷 · 受访者/访员实施版",
    [
      ["适用对象", value(population.label, form.population_id)],
      ["语言 / 模式", `${value(form.language)} / ${value(form.mode)}`],
      ["版本 / 日期", `${value(instrument.version)} / [YYYY-MM-DD]`],
      ["预计用时", participants.estimated_minutes],
      ["问卷编号", "________________"],
    ],
    "请确认本问卷的适用对象和版本；如有疑问，请在开始前联系研究团队。"
  ));

  children.push(heading("研究说明与参与同意"));
  children.push(paragraph(`研究机构/团队：${value(participants.organization)}`));
  children.push(paragraph(value(participants.study_purpose)));
  children.push(paragraph(value(form.introduction)));
  children.push(paragraph(value(participants.voluntary_statement)));
  children.push(paragraph(value(participants.privacy_statement)));
  children.push(paragraph(`如有疑问，请联系：${value(participants.contact)}`));
  if (participants.consent_mode === "explicit") {
    children.push(table([[{
      children: [paragraph(`□ ${value(participants.consent_prompt)}`, { bold: true, after: 0 })],
      fill: COLORS.warning,
    }]], [CONTENT_WIDTH]));
  } else if (participants.consent_mode === "implied-by-submission") {
    children.push(table([[{
      children: [paragraph(value(participants.consent_prompt), { bold: true, after: 0 })],
      fill: COLORS.warning,
    }]], [CONTENT_WIDTH]));
  } else {
    children.push(table([[{
      children: [paragraph("[本版本采用审批或豁免文件规定的参与者告知方式，请在实施前替换本提示。]", { bold: true, after: 0 })],
      fill: COLORS.warning,
    }]], [CONTENT_WIDTH]));
  }

  children.push(heading("填写/访员说明"));
  children.push(paragraph(value(form.instructions)));
  children.push(paragraph("日期：________年____月____日　开始时间：____:____　结束时间：____:____", { size: 20, color: COLORS.muted }));

  const rendered = new Set();
  for (const section of sections) {
    const sectionItems = items.filter((item) => item.section_id === section.id || (!item.section_id && section.id === "DEFAULT"));
    if (!sectionItems.length) continue;
    children.push(heading(value(section.title), HeadingLevel.HEADING_1));
    if (section.introduction) children.push(paragraph(value(section.introduction), { color: COLORS.muted }));
    for (const item of sectionItems) {
      children.push(fieldQuestion(item, form.mode));
      children.push(paragraph("", { after: 90 }));
      rendered.add(item.id);
    }
  }
  const unsectioned = items.filter((item) => !rendered.has(item.id) && (!item.section_id || !sectionIds.has(item.section_id)));
  if (unsectioned.length) {
    children.push(heading("其他题目"));
    for (const item of unsectioned) {
      children.push(fieldQuestion(item, form.mode));
      children.push(paragraph("", { after: 90 }));
    }
  }

  children.push(heading("提交前确认"));
  children.push(paragraph("请检查是否存在漏答或误填。您可以按照研究说明中载明的方式决定是否提交或中止。"));
  children.push(paragraph(value(participants.completion_message), { bold: true, align: AlignmentType.CENTER, before: 220, after: 220 }));

  return new Document({
    styles: documentStyles(),
    sections: [baseSection(
      children,
      form.title || instrument.title,
      instrument.version,
      "实施版",
      `${value(form.id)} · ${value(form.population_id)} · ${value(form.language)} · ${value(form.mode)}`
    )],
  });
}

function assertUsable(spec) {
  if (!spec || typeof spec !== "object") throw new Error("questionnaire spec must be a JSON object");
  if (!spec.instrument || !spec.instrument.title) throw new Error("instrument.title is required");
  if (!Array.isArray(spec.items) || !spec.items.length) throw new Error("items must contain at least one question");
  for (const form of normalizedForms(spec)) {
    if (!form.id || !form.population_id || !form.language || !form.mode) {
      throw new Error("each form needs id, population_id, language, and mode");
    }
    if (!formItems(spec, form).length) throw new Error(`form ${form.id} has no items for population ${form.population_id}`);
  }
}

async function writeDocument(document, outputPath) {
  const buffer = await Packer.toBuffer(document);
  fs.writeFileSync(outputPath, buffer);
  console.log(`written: ${outputPath}`);
}

async function main() {
  const specPath = process.argv[2];
  const outputDirectory = process.argv[3];
  if (!specPath || !outputDirectory) {
    console.error("Usage: node questionnaire-docx-template.js questionnaire-spec.json output-directory");
    process.exitCode = 2;
    return;
  }
  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  assertUsable(spec);
  fs.mkdirSync(outputDirectory, { recursive: true });

  const title = safeFilePart(spec.instrument.title);
  await writeDocument(
    researcherDocument(spec),
    path.join(outputDirectory, `01_问卷_研究者版_${title}.docx`)
  );
  for (const form of normalizedForms(spec)) {
    const suffix = [form.id, form.population_id, form.language, form.mode].map(safeFilePart).join("_");
    await writeDocument(
      fieldDocument(spec, form),
      path.join(outputDirectory, `02_问卷_实施版_${suffix}.docx`)
    );
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(`ERROR: ${error.message}`);
    process.exitCode = 1;
  });
}

module.exports = {
  COLORS,
  CONTENT_WIDTH,
  baseSection,
  cell,
  cover,
  documentStyles,
  fieldQuestion,
  formItems,
  heading,
  labelValueTable,
  normalizedForms,
  pageBreak,
  paragraph,
  requirementLabel,
  safeFilePart,
  table,
  textRun,
  value,
};
