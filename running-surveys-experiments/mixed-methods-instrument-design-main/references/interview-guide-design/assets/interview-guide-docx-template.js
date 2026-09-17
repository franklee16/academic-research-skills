const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel, PageBreak
} = require("docx");

const CN = "宋体", HEI = "黑体";

// ---- helpers ----
function P(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after ?? 90, before: opts.before ?? 0, line: 320 },
    alignment: opts.align,
    children: [new TextRun({ text, bold: opts.bold, italics: opts.italics, size: opts.size ?? 22, font: opts.font ?? CN, color: opts.color })],
  });
}
function H(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 220, after: 120 },
    children: [new TextRun({ text, bold: true, font: HEI, size: level === HeadingLevel.HEADING_1 ? 30 : 26 })] });
}
function section(title) { return H(title, HeadingLevel.HEADING_2); }
// 主问题：加粗编号 + 题面，下方留手写记录行
// ⚠ note = 访谈者私用的现场提示（如「关键题，务必问到」「可与文档/统计三角验证」），
//   现场版禁写「服务 RQ1」「构念=X」等方法论术语——研究问题/映射矩阵只留在研究者版 Markdown，
//   否则受访者一瞥见会被语域带偏（见 SKILL.md 第1步雷区）。用低调灰、勿用刺眼红。
function mainQ(num, text, note) {
  const kids = [ new Paragraph({ spacing: { before: 120, after: 40, line: 320 },
    children: [ new TextRun({ text: `${num}. `, bold: true, size: 23, font: CN }),
                new TextRun({ text, size: 23, font: CN }),
                ...(note ? [new TextRun({ text: `  〔${note}〕`, size: 18, font: CN, color: "808080" })] : []) ] }) ];
  return kids;
}
// 追问/探测：灰色缩进小字
function probe(text) {
  return new Paragraph({ spacing: { after: 40, line: 300 }, indent: { left: 480 },
    children: [ new TextRun({ text: "› 追问/探测：", size: 19, font: CN, color: "808080" }),
                new TextRun({ text, size: 19, font: CN, color: "808080" }) ] });
}
// 记录留白
function blank(lines = 2) {
  const arr = [];
  for (let i = 0; i < lines; i++) arr.push(new Paragraph({ spacing: { after: 60, line: 320 }, indent: { left: 240 },
    children: [new TextRun({ text: "________________________________________________________________", size: 20, font: CN, color: "BFBFBF" })] }));
  return arr;
}

// ---- content ----
const kids = [];
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "[研究主题] 访谈提纲（现场详版）", bold: true, font: HEI, size: 32 })] }));
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: "（半结构化 · 关键知情人 · 匿名化呈现）", size: 20, font: CN, color: "666666" })] }));

// 开场白 + 知情同意
kids.push(section("开场白与知情同意"));
kids.push(P("尊敬的 ×× 领导/老师：您好！我们是 ×× 研究团队，正在了解 ×× 方面的情况。非常感谢您抽时间接受访谈。"));
kids.push(P("本次访谈内容严格保密、匿名化（去标识化）呈现，仅用于学术研究，不会单独披露，也不会用于任何评估或商业目的；若因您的岗位/案例较特殊仍可能被识别，我们会就化名或模糊化处理与您协商。访谈没有标准答案，请您根据实际情况放心谈。"));
kids.push(P("为保证记录准确，访谈拟全程录音，录音仅研究团队加密留存、约定期限后销毁；您可随时中止、对任何问题不作回答，事后也可要求删除您已说的内容；若内容需用于本研究之外，我们会另行征得您同意。", { after: 60 }));
kids.push(P("☐ 已知情同意参与　☐ 单独同意录音　☐ 同意后续回访确认（成员核验）", { color: "808080", size: 20 }));

// 基本信息
kids.push(section("一、基本信息"));
kids.push(P("受访者岗位/职责：____________________　从业年限：__________　访谈时间地点：____________________", { size: 21 }));

// 过渡/大游览
kids.push(section("二、总体情况（大游览开场）"));
kids.push(...mainQ("Q1", "能不能先请您介绍一下，[案例/对象] 在 [主题] 方面，总体上是个什么情况？"));
kids.push(probe("能举一两个具体的例子吗？"));
kids.push(...blank(3));

// 核心板块1
kids.push(section("三、[核心主题板块 1：举措/做法]"));
kids.push(...mainQ("Q2", "在 [主题] 方面，你们主要采取了哪些做法？", "关键题，务必问到"));
kids.push(probe("当初是怎么决定这样做的？过程中遇到过什么困难？"));
kids.push(...blank(3));
kids.push(...mainQ("Q3", "请具体讲讲其中某一项做法是怎么落地的？", "追问到具体过程/阶段"));
kids.push(probe("从开始到现在，大致经历了哪几个阶段？"));
kids.push(...blank(3));

// 核心板块2
kids.push(section("四、[核心主题板块 2：成效与机制]"));
kids.push(...mainQ("Q4", "这些做法带来了哪些变化或成效？", "可与文档/统计三角验证"));
kids.push(probe("您是怎么判断有没有成效的？有没有数据/案例能说明？〔向其索取对应材料〕"));
kids.push(...blank(3));
kids.push(...mainQ("Q5", "回过头看，是什么在起关键作用？又是什么把事情卡住了？", "关键题，追问到具体事例"));
kids.push(probe("能讲一件最近印象深的具体事例吗？"));
kids.push(...blank(3));

// 敏感题靠后
kids.push(section("五、[现存问题与挑战（较敏感，靠后）]"));
kids.push(...mainQ("Q6", "其实这方面的困难各家多少都会碰到、很正常——在你们这儿，目前还有哪些没解决的困难或顾虑？", "敏感题，先常态化再问"));
kids.push(probe("如果可以改一件事，您最想改什么？"));
kids.push(...blank(3));

// 收尾兜底
kids.push(section("六、收尾"));
kids.push(...mainQ("Q7", "还有什么是我没问到、但您觉得对理解这件事很重要的吗？"));
kids.push(...blank(3));
kids.push(P("【访谈者备注：是否需回访做成员核验？需补充的其他证据源（文件/数据/观察）？】", { color: "808080", size: 19, italics: true }));
kids.push(P("感谢您的时间与分享！", { bold: true }));

const doc = new Document({
  styles: { default: { document: { run: { font: CN, size: 22 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: kids,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = process.argv[2];
  fs.writeFileSync(out, buf);
  console.log("written:", out);
});
