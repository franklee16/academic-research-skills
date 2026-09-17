#!/usr/bin/env node
"use strict";

/**
 * Generate one complete Word document containing all questionnaire forms and
 * semi-structured interview guides for the same study.
 *
 * Usage:
 *   node mixed-instruments-docx-template.js questionnaire-spec.json interview-guide.json output.docx
 */

const fs = require("fs");
const path = require("path");
const { AlignmentType, Document, Packer } = require("docx");
const q = require("../references/questionnaire-design/assets/questionnaire-docx-template.js");

function assertObject(value, message) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(message);
}

function assertInputs(questionnaire, interview) {
  assertObject(questionnaire, "questionnaire spec must be an object");
  assertObject(questionnaire.instrument, "questionnaire instrument is required");
  if (!Array.isArray(questionnaire.items) || !questionnaire.items.length) {
    throw new Error("questionnaire items must be non-empty");
  }
  const forms = q.normalizedForms(questionnaire);
  if (!forms.length) throw new Error("at least one questionnaire form is required");
  for (const form of forms) {
    if (!q.formItems(questionnaire, form).length) {
      throw new Error(`questionnaire form ${form.id} has no items for ${form.population_id}`);
    }
  }

  assertObject(interview, "interview guide spec must be an object");
  if (!Array.isArray(interview.guides) || !interview.guides.length) {
    throw new Error("interview guides must be non-empty");
  }
  for (const guide of interview.guides) {
    if (!guide.id || !guide.title || !guide.target_population) {
      throw new Error("each interview guide needs id, title, and target_population");
    }
    if (!Array.isArray(guide.sections) || !guide.sections.length) {
      throw new Error(`interview guide ${guide.id} needs sections`);
    }
    for (const section of guide.sections) {
      if (!section.title || !Array.isArray(section.questions) || !section.questions.length) {
        throw new Error(`each section in ${guide.id} needs a title and questions`);
      }
      for (const question of section.questions) {
        if (!question.id || !question.text) throw new Error(`each interview question in ${guide.id} needs id and text`);
      }
    }
  }
}

function questionnaireIntroduction(questionnaire, form, appendixNumber) {
  const instrument = questionnaire.instrument || {};
  const participants = questionnaire.participant_materials || {};
  const population = (questionnaire.populations || []).find((entry) => entry.id === form.population_id) || {};
  const children = [
    q.heading(`附表${appendixNumber}　调查问卷——${q.value(form.title, instrument.title)}`),
    q.labelValueTable([
      ["适用对象", q.value(population.label, form.population_id)],
      ["实施方式", `${q.value(form.language)} / ${q.value(form.mode)}`],
      ["版本", instrument.version],
      ["预计用时", participants.estimated_minutes],
      ["问卷编号", "________________"],
    ]),
    q.heading("研究说明与参与同意", "Heading2"),
    q.paragraph(`研究机构/团队：${q.value(participants.organization)}`),
    q.paragraph(q.value(participants.study_purpose)),
    q.paragraph(q.value(form.introduction)),
    q.paragraph(q.value(participants.voluntary_statement)),
    q.paragraph(q.value(participants.privacy_statement)),
    q.paragraph(`如有疑问，请联系：${q.value(participants.contact)}`),
  ];
  if (participants.consent_mode === "explicit") {
    children.push(q.table([[{
      text: `□ ${q.value(participants.consent_prompt)}`,
      bold: true,
      fill: q.COLORS.warning,
    }]], [q.CONTENT_WIDTH]));
  } else {
    children.push(q.table([[{
      text: q.value(participants.consent_prompt),
      bold: true,
      fill: q.COLORS.warning,
    }]], [q.CONTENT_WIDTH]));
  }
  children.push(q.heading("填写/访员说明", "Heading2"));
  children.push(q.paragraph(q.value(form.instructions)));
  children.push(q.paragraph("日期：________年____月____日　开始时间：____:____　结束时间：____:____", {
    color: q.COLORS.muted,
  }));
  return children;
}

function questionnaireContent(questionnaire, form) {
  const items = q.formItems(questionnaire, form);
  const sections = Array.isArray(questionnaire.sections) ? questionnaire.sections : [];
  const visibleSections = sections.filter((section) =>
    !section.population_ids || section.population_ids.includes(form.population_id)
  );
  const rendered = new Set();
  const children = [];

  for (const section of visibleSections) {
    const sectionItems = items.filter((item) => item.section_id === section.id);
    if (!sectionItems.length) continue;
    children.push(q.heading(q.value(section.title)));
    if (section.introduction) children.push(q.paragraph(q.value(section.introduction), { color: q.COLORS.muted }));
    for (const item of sectionItems) {
      children.push(q.fieldQuestion(item, form.mode));
      children.push(q.paragraph("", { after: 90 }));
      rendered.add(item.id);
    }
  }

  const remaining = items.filter((item) => !rendered.has(item.id));
  if (remaining.length) {
    children.push(q.heading("其他题目"));
    for (const item of remaining) {
      children.push(q.fieldQuestion(item, form.mode));
      children.push(q.paragraph("", { after: 90 }));
    }
  }

  const participants = questionnaire.participant_materials || {};
  children.push(q.heading("问卷结束"));
  children.push(q.paragraph("请检查是否存在漏答或误填。您可以按照研究说明中载明的方式决定是否提交或中止。"));
  children.push(q.paragraph(q.value(participants.completion_message), {
    bold: true,
    align: AlignmentType.CENTER,
    before: 180,
  }));
  return children;
}

function interviewQuestion(question) {
  const body = [
    q.paragraph(q.value(question.text), { bold: true, size: 23, after: 80 }),
  ];
  for (const probe of question.probes || []) {
    body.push(q.paragraph(`追问/探测：${q.value(probe)}`, {
      size: 19,
      color: q.COLORS.muted,
      indent: { left: 240 },
      after: 55,
    }));
  }
  body.push(q.paragraph("记录：________________________________________________________________", {
    size: 18,
    color: q.COLORS.muted,
    before: 40,
  }));
  body.push(q.paragraph("　　　________________________________________________________________", {
    size: 18,
    color: q.COLORS.muted,
    after: 0,
  }));
  return q.table([
    [{ text: `${q.value(question.id)}　主问题`, bold: true, fill: q.COLORS.paleBlue }],
    [{ children: body }],
  ], [q.CONTENT_WIDTH], { header: true });
}

function interviewContent(guide, appendixNumber) {
  const children = [
    q.heading(`附表${appendixNumber}　${q.value(guide.title)}`),
    q.labelValueTable([
      ["访谈对象", guide.target_population],
      ["访谈方式", guide.mode],
      ["预计时长", guide.estimated_minutes],
      ["访谈编号", "________________"],
    ]),
    q.heading("开场白与知情同意", "Heading2"),
  ];
  for (const line of guide.opening || []) children.push(q.paragraph(q.value(line)));
  if (Array.isArray(guide.consent_items) && guide.consent_items.length) {
    children.push(q.table(guide.consent_items.map((item) => [{ text: q.value(item) }]), [q.CONTENT_WIDTH]));
  }

  children.push(q.heading("基本信息", "Heading2"));
  const info = (guide.basic_information || []).map((entry) => [q.value(entry.label), q.value(entry.value)]);
  if (info.length) children.push(q.labelValueTable(info));

  for (const section of guide.sections || []) {
    children.push(q.heading(q.value(section.title)));
    for (const question of section.questions || []) {
      children.push(interviewQuestion(question));
      children.push(q.paragraph("", { after: 80 }));
    }
  }

  children.push(q.heading("访谈结束"));
  for (const line of guide.closing || []) children.push(q.paragraph(q.value(line)));
  return children;
}

function buildDocument(questionnaire, interview) {
  const instrument = questionnaire.instrument || {};
  const forms = q.normalizedForms(questionnaire);
  const children = [];
  children.push(...q.cover(
    `${q.value(instrument.title)}研究工具`,
    "调查问卷与半结构化访谈提纲",
    [
      ["版本 / 状态", `${q.value(instrument.version)} / ${q.value(instrument.status)}`],
      ["问卷对象", forms.map((form) => form.population_id)],
      ["访谈对象", interview.guides.map((guide) => guide.target_population)],
      ["文档用途", "伦理/专家审查、现场实施、论文或报告附录"],
    ],
    "问卷和访谈属于同一研究场景，可以面向不同受访人群；各部分均须按其首页标注的适用对象实施。"
  ));

  let firstPart = true;
  let appendixNumber = 1;
  for (const form of forms) {
    if (!firstPart) children.push(q.pageBreak());
    children.push(...questionnaireIntroduction(questionnaire, form, appendixNumber));
    children.push(...questionnaireContent(questionnaire, form));
    firstPart = false;
    appendixNumber += 1;
  }
  for (const guide of interview.guides) {
    children.push(q.pageBreak());
    children.push(...interviewContent(guide, appendixNumber));
    appendixNumber += 1;
  }

  return new Document({
    styles: q.documentStyles(),
    sections: [q.baseSection(
      children,
      `${q.value(instrument.title)}研究工具`,
      instrument.version,
      "问卷与访谈提纲",
      "单文件受控版本"
    )],
  });
}

async function main() {
  const questionnairePath = process.argv[2];
  const interviewPath = process.argv[3];
  const outputPath = process.argv[4];
  if (!questionnairePath || !interviewPath || !outputPath) {
    console.error("Usage: node mixed-instruments-docx-template.js questionnaire-spec.json interview-guide.json output.docx");
    process.exitCode = 2;
    return;
  }
  const questionnaire = JSON.parse(fs.readFileSync(questionnairePath, "utf8"));
  const interview = JSON.parse(fs.readFileSync(interviewPath, "utf8"));
  assertInputs(questionnaire, interview);
  const target = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, await Packer.toBuffer(buildDocument(questionnaire, interview)));
  console.log(`written: ${target}`);
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exitCode = 1;
});
