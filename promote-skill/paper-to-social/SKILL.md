---
name: paper-to-social
description: Turn an academic paper (working paper, published article, R&R manuscript, conference draft) into platform-native social media posts for public engagement. Produces LinkedIn posts, X/Twitter single tweets or threads, 小红书 posts in Chinese, and Substack long-form essays — each matching the specific platform's tone, length, and conventions. MUST trigger whenever the user wants to promote, share, repurpose, or publicize a research paper on social media; write a tweet thread about their research; create a 小红书 post for an academic paper; draft a LinkedIn post about a working paper; prepare public-engagement content for empirical research; turn a manuscript into blog/social content; or says things like "turn this paper into social posts", "write a thread for my paper", "promote my research", "public engagement posts", "repurpose this manuscript", "summarize my paper for [platform]". Also trigger when platform names (LinkedIn, X, Twitter, 小红书, Substack) appear in the context of an academic paper, even if the user does not explicitly say "social media".
---

# Paper to Social Media Posts

Turn an empirical research paper into platform-native social posts calibrated for public engagement. Tuned for empirical social science (economics, finance, marketing, accounting, management, public policy). Each post leads with the research puzzle, reports effect sizes with magnitudes, translates the identification strategy into plain language, and closes with the real-world implication.

The single biggest failure mode is producing four versions of the same post in the same voice. Each platform has a distinct register — a LinkedIn post is not a Substack essay is not a 小红书 card is not an X thread. Respect the differences.

## The workflow

### Step 1 — Read the paper and extract text

Accept `.docx`, `.tex`, `.pdf`, or `.md`.

**`.docx`** — the Read tool fails on binary .docx. Extract via Python zipfile + XML parse, and write UTF-8 explicitly (Windows defaults to cp1252 and crashes on curly quotes):

```python
import zipfile, io
from xml.etree import ElementTree as ET

with zipfile.ZipFile(path) as z:
    with z.open('word/document.xml') as f:
        xml = f.read().decode('utf-8')

ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root = ET.fromstring(xml)
out = []
for p in root.iter(ns+'p'):
    text = ''
    for t in p.iter(ns+'t'):
        text += t.text or ''
    out.append(text)

with io.open('paper_text.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
```

**CRITICAL — footnotes are not in document.xml.** They live in `word/footnotes.xml`. Parse it separately. Title-page footnote 1 almost always holds author affiliations and acknowledgments. If you skip this, you will hallucinate affiliations.

```python
with zipfile.ZipFile(path) as z:
    with z.open('word/footnotes.xml') as f:
        fn_xml = f.read().decode('utf-8')
fn_root = ET.fromstring(fn_xml)
for fn in fn_root.iter(ns+'footnote'):
    fid = fn.get(ns+'id')
    text = ''.join(t.text or '' for t in fn.iter(ns+'t'))
    print(f'[{fid}] {text}')
```

**`.tex`** — read directly; full file before editing tables.
**`.pdf`** — prefer `pymupdf` (`fitz`), then `pypdf`. The built-in Read tool struggles with image-based or AcroForm PDFs.

### Step 2 — Verify metadata (DO NOT SKIP)

These two mistakes are the most common and the most embarrassing. Verify both against the paper itself, never from memory.

**Author affiliations.** Extract from the title-page footnote. Do NOT infer from funding acknowledgments — a "financial support from X University" line is about a grant, not employment. Each author's affiliation is the institution where they sit, stated explicitly in the title footnote. If you previously drafted posts with affiliations from memory or from funding lines, treat that as a bug and fix it before shipping.

**Publication status.** Check the draft date on the paper, any cover letters in the same folder (`Cover letter to Editor*.docx`), and what the user has said. Map to the public-facing label:

| Evidence | Label |
|----------|-------|
| No journal involvement | "working paper" |
| Review/R&R underway | omit journal, or "under review" if user confirms |
| Editor signals acceptance path ("move closer to publication", "excited to see the paper move toward publication") | "forthcoming at [Journal]" |
| Formal acceptance letter | "accepted at [Journal]" |
| Published online | "[Journal] (year)" |

When unsure, ask the user. Never infer "forthcoming" from R&R status alone unless cover-letter language supports it.

### Step 3 — Extract the research story

Pull these six elements before drafting. Different posts will use different subsets.

1. **The puzzle** — what question, and why was it hard to answer before? (This is the hook.)
2. **Data** — what is novel about the dataset: source, scale, granularity, coverage.
3. **Headline finding** — with magnitude. "1.2% drop", not "a significant decrease".
4. **Identification** — what rules out confounders (fixed effects, natural experiment, instrument, exogenous shock). Translate the econometric move into one plain sentence.
5. **Heterogeneity** — where/for whom the effect is strongest. This is where the "why it matters" lives; it carries more narrative weight than the headline coefficient.
6. **Real-world implication** — what should a practitioner, policymaker, or informed citizen take away?

A paper usually has one or two findings that carry the story. Resist listing every result — the public audience needs the through-line, not the regression catalogue.

### Step 4 — Confirm platforms

Default behavior: ask the user which platforms. The user may say "all four", "just X and LinkedIn", "Chinese platforms", or specify a subset. If the prompt already specifies, skip the ask.

Supported platforms and their files:
- LinkedIn → `posts/linkedin.md`
- X / Twitter → `posts/x.md`
- 小红书 → `posts/xiaohongshu.md`
- Substack → `posts/substack.md`

### Step 5 — Draft per platform

Each platform has a distinct register. The conventions below are the baseline. For annotated real examples of each, read `references/example-posts.md` — it shows the structural moves that distinguish a LinkedIn post from a Substack essay from a 小红书 card.

#### LinkedIn

- **Length:** 200–400 words (~1,900–3,000 chars). Goes under the "see more" fold cleanly.
- **Voice:** Professional first-person research voice. Evidence-led. Ends with a business/practitioner takeaway.
- **Opener:** Hook first — often a contrarian framing, a stark number, or the research question. Never open with "I'm excited to share…" or "I'm thrilled to announce…".
- **Structure:** Hook → data/scale → numbered findings (use 1️⃣ 2️⃣ 3️⃣ or "1.", "2.") → identification/causality note → takeaway → paper credit with affiliations → SSRN/DOI link → hashtags.
- **Emojis:** Minimal. Numbered list glyphs (1️⃣) and arrows (→) are conventional; avoid decorative emoji.
- **Hashtags:** 3–5 at the bottom, no more. Platform-conventional (e.g., #ESG #EmpiricalFinance), not invented.
- **Closing line:** Paper credit with verified affiliations, then the link, then an invitation to discuss ("Happy to discuss", "Comments welcome").

#### X / Twitter

- **Single tweet option (~280 chars):** Punchy contrarian opener → headline finding with magnitude → one causal/identification beat → "Forthcoming at [Journal]" → SSRN link. No hashtags — finance-academic Twitter uses zero.
- **Thread option (4–5 tweets):**
  - `1/` Hook + data scale
  - `2/` Headline finding with magnitude + the key asymmetry that rules out the naive read
  - `3/` Heterogeneity (where the effect concentrates)
  - `4/` Causality — the identification move in plain language
  - `5/` Bottom line + paper credit + SSRN link
- **Voice:** Terse, first-person, contrarian-friendly. Each tweet stands alone but the arc builds.
- **Hashtags:** None (or at most one). This is the opposite of LinkedIn.
- **Emojis:** Essentially none. A single 🧵 to signal a thread is acceptable.
- **Bonus:** Suggest attaching a figure from the paper (the dynamic event-study plot or coefficient figure) to tweet 2 of the thread — visual proof lifts engagement.
- **Follow-ups:** Offer 1–2 standalone tweets the user can post in the following days to keep the paper visible without re-announcing.

#### 小红书 (Xiaohongshu)

- **Length:** 400–600 字 Chinese.
- **Voice for academic accounts:** Professional academic. First-person research voice ("我们团队", "本研究"). Use research vocabulary (因果识别, 外生冲击, 替代解释, 稳健性检验, 非对称性).
- **Forbidden for academic accounts:** 姐妹们, 家人们, 巨, 超, 真的, 没想到, 灵魂问题, 粉转黑/黑转粉, "你下次…可能比你想的更有力量". These read as lifestyle-influencer voice and mismatch a researcher's account.
- **Structure:** First-person hook → 📌 **研究方法/数据** (data) → 📌 **主要发现** (numbered ①②③④) → 📌 **因果识别策略** → 📌 **最重要的结论** → 📌 **论文发表信息** (forthcoming status if known) → hashtag list.
- **Emojis:** Used as section dividers and visual markers (📌 📊 📰 🔬 ✨), not as emotional decoration. One or two per section header, not one per sentence.
- **Hashtags:** 6–8 at the bottom, mix of Chinese and English research tags (#ESG研究 #可持续金融 #实证研究 #公司金融).
- **End:** Do NOT add "欢迎同行交流/私信" unless the user asks — that's a separate decision. If the user requests a more casual tone (e.g., for a book review or teaching post), relax the academic register.

#### Substack

- **Length:** 800–1,500 words. Sweet spot is ~1,100.
- **Voice:** Long-form narrative essay. First-person reflective. Walks the reader through the puzzle, the data, the findings, and what it all means.
- **Opening:** Either the academic puzzle (why was this question so hard to answer?) or a clearly-hypothetical illustrative scene that frames the data question. If using a scene, mark it as illustrative so readers don't think it's a specific case from your data.
- **Structure:** Open → data breakthrough → headline finding → heterogeneity → causality → real-world implication → broader reflection on why it matters beyond this paper.
- **Paragraphs:** Short (1–4 sentences). Sub-headings (`## Section`) are fine for breaking up longer pieces.
- **Emojis:** None.
- **Footer:** Italicized block with paper credit, verified affiliations, data sources, SSRN link, and contact email (wrapped in `<>` for markdown cleanliness).
- **Closing beat:** End on the bigger meaning — what does this paper suggest about the world, not just about the firm/sector studied?

### Step 6 — Save and quality-check

Save to a `posts/` folder at the working-directory root:

- `posts/README.md` — index with a platform / length / tone table, co-author list, source file, and any caveat the user should remember when posting.
- One file per platform (`linkedin.md`, `xiaohongshu.md`, `substack.md`, `x.md`).

Each file opens with a short metadata header (target audience, character budget, tone notes) above the post body, so the user can see the design choices at a glance. The post body sits below a `---` separator.

**Anti-overclaim checklist — run before reporting done:**

- [ ] Effect sizes match the paper exactly (no rounding up, no direction reversal)
- [ ] Author affiliations verified from paper footnotes, not memory or funding lines
- [ ] Publication status verified from cover letter / metadata / user statement
- [ ] No causal language ("causes", "proves", "drives") unless the identification strategy supports it — otherwise use "plausibly causal", "associated with", or "correlated with"
- [ ] No AI-slop phrases (global rule: no "leverage", "robust", "delve", "navigate the complexities", "tapestry", "intricate", "pivotal", "crucial", "underscores", rule-of-three for emphasis, em-dash piles, "It's worth noting", "It's important to mention")
- [ ] SSRN / DOI / arXiv link included if the user provided one; render as markdown link in the file
- [ ] 小红书 post in professional-academic Chinese (no lifestyle-influencer markers for academic accounts)
- [ ] X post has no hashtags (or at most one); LinkedIn has 3–5

## What "platform tone" really means

The reason each platform gets its own conventions is that each audience reads with a different posture:

- **LinkedIn** readers are scanning for professional signal. They want the takeaway, the evidence, and the business implication, fast. Hashtags and structure help them triage.
- **X** readers are doomscrolling. You have one sentence to earn the next one. Terse, contrarian, no friction.
- **小红书** readers are in discovery mode, but academic-account followers expect substance, not lifestyle performance. The platform's visual-card structure still applies, but the voice is professional.
- **Substack** readers have opted into long-form. They want the story, the reasoning, and the meaning. They will read 1,200 words if you earn them.

Calibrate to the reader's posture, not just to the platform's surface conventions.

## Bundled reference

`references/example-posts.md` contains four annotated real posts (one per platform) generated from a finance paper on ESG and consumer behavior. Read it when you need to calibrate tone, length, or structural moves for a specific platform. The annotations explain what makes each post match its platform's register.
