"""
SciPilot-cite :: insert_citations_latex.py
LaTeX 论文引用插入引擎
支持 thebibliography 和 BibTeX 两种模式
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

from format_citation import format_bibtex_entry, format_citation
from utils import assign_citation_numbers, extract_keywords, logger

SECTION_RE = re.compile(r"\\(?:section|subsection|subsubsection|paragraph|chapter)\*?\{([^}]*)\}")
CITE_RE = re.compile(r"\\cite\w*\{([^}]+)\}")
BIB_BLOCK_RE = re.compile(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.S)
BIBLIOGRAPHY_CMD_RE = re.compile(r"\\bibliography\{([^}]+)\}")
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\\])")


def parse_latex(tex_content: str) -> dict[str, Any]:
    """解析 LaTeX 源码。"""
    document_start = tex_content.find("\\begin{document}")
    document_end = tex_content.find("\\end{document}")
    preamble = tex_content[:document_start] if document_start > 0 else ""
    body_start = document_start + len("\\begin{document}") if document_start > 0 else 0
    body_end = document_end if document_end > 0 else len(tex_content)
    body = tex_content[body_start:body_end]

    sections = []
    matches = list(SECTION_RE.finditer(body))
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections.append(
            {
                "name": name,
                "start_pos": start + body_start,
                "end_pos": end + body_start,
                "content": body[start:end],
            }
        )

    existing_citations = list(set(CITE_RE.findall(tex_content)))

    bib_type = None
    if BIB_BLOCK_RE.search(tex_content):
        bib_type = "thebibliography"
    elif BIBLIOGRAPHY_CMD_RE.search(tex_content):
        bib_type = "bibtex"

    return {
        "preamble": preamble,
        "body": body,
        "body_start": body_start,
        "body_end": body_end,
        "sections": sections,
        "existing_citations": existing_citations,
        "bibliography_type": bib_type,
        "full_text": tex_content,
    }


def _split_sentences_with_offsets(text: str, offset: int = 0) -> list[tuple[int, int, str]]:
    """
    返回 [(abs_start, abs_end, sentence_text), ...]
    abs_end 指向句末标点之后一个位置（即正常 string slice 的右端）。
    使用 finditer 跟踪真实位置，不依赖 split 累加（split 会丢掉分隔空白）。
    """
    boundaries = [0]
    for m in SENTENCE_END_RE.finditer(text):
        boundaries.append(m.start())
    boundaries.append(len(text))

    out: list[tuple[int, int, str]] = []
    for i in range(len(boundaries) - 1):
        seg_start = boundaries[i]
        seg_end = boundaries[i + 1]
        s = seg_start
        while s < seg_end and text[s].isspace():
            s += 1
        e = seg_end
        while e > s and text[e - 1].isspace():
            e -= 1
        if e > s:
            out.append((offset + s, offset + e, text[s:e]))
    return out


def _section_keywords_for(paper: dict, section_name: str) -> set[str]:
    text = (paper.get("title", "") + " " + paper.get("abstract", "")).lower()
    return set(extract_keywords(text, top_n=8))


def _section_priority(section_name: str) -> int:
    n = section_name.lower()
    if "related" in n or "background" in n or "literature" in n:
        return 1
    if "introduction" in n or "intro" in n:
        return 2
    if "method" in n or "approach" in n or "model" in n:
        return 3
    if "experiment" in n or "result" in n or "evaluation" in n:
        return 4
    if "discussion" in n or "conclu" in n:
        return 5
    return 9


def find_insertion_points(parsed: dict, papers: list[dict]) -> list[dict]:
    """
    为每篇文献确定最佳插入位置。
    返回 [{paper_idx, section_name, position, sentence_offset_end, ...}, ...]
    """
    sections = parsed["sections"]
    if not sections:
        if parsed["body"].strip():
            sections = [
                {
                    "name": "body",
                    "start_pos": parsed["body_start"],
                    "end_pos": parsed["body_end"],
                    "content": parsed["body"],
                }
            ]
        else:
            logger.warning("No sections detected in LaTeX; falling back to end-of-document insertion")
            return []

    section_sentences: list[list[tuple[int, int, str]]] = []
    for sec in sections:
        section_sentences.append(_split_sentences_with_offsets(sec["content"], offset=sec["start_pos"]))

    used_positions: set[int] = set()
    plan: list[dict] = []

    for idx, paper in enumerate(papers):
        kws = _section_keywords_for(paper, "")
        best = None
        best_score = -1.0
        for sec_i, sec in enumerate(sections):
            base = 100 - _section_priority(sec["name"]) * 5
            for sent_start, sent_end, sent in section_sentences[sec_i]:
                if sent_end in used_positions:
                    continue
                if "\\section" in sent or "\\begin" in sent or "\\end{" in sent:
                    continue
                lower = sent.lower()
                overlap = sum(1 for k in kws if k in lower)
                score = base + overlap * 10
                if score > best_score:
                    best_score = score
                    best = (sec, sent_start, sent_end, sent)
        if not best:
            continue
        sec, s_start, s_end, sent = best
        used_positions.add(s_end)
        plan.append(
            {
                "paper_idx": idx,
                "section_name": sec["name"],
                "position": s_end,
                "sentence_preview": sent.strip()[:80],
            }
        )

    plan = assign_citation_numbers(plan)
    return plan


def _build_thebibliography(papers_by_number: dict[int, dict], style: str) -> str:
    keys = sorted(papers_by_number.keys())
    lines = ["\\begin{thebibliography}{99}"]
    for n in keys:
        paper = papers_by_number[n]
        entry = format_citation(paper, style, number=n)
        entry = entry.lstrip(f"[{n}]").lstrip(f"{n}.").strip()
        lines.append(f"\\bibitem{{{paper.get('bibtex_key', f'ref{n}')}}} {entry}")
    lines.append("\\end{thebibliography}")
    return "\n".join(lines)


def _build_bib_file(papers: list[dict]) -> str:
    return "\n\n".join(format_bibtex_entry(p) for p in papers) + "\n"


def insert_citations_to_latex(
    tex_content: str,
    papers: list[dict],
    style: str,
    insertion_plan: list[dict],
    use_bibtex: bool = False,
) -> tuple[str, str | None]:
    """
    在 LaTeX 内容中插入 \\cite{...} 并更新 bibliography。
    返回 (modified_tex, bib_file_content_or_None)
    """
    plan_by_pos: dict[int, list[dict]] = {}
    for item in insertion_plan:
        plan_by_pos.setdefault(item["position"], []).append(item)

    parsed = parse_latex(tex_content)
    inserted = tex_content

    sorted_positions = sorted(plan_by_pos.keys(), reverse=True)
    for pos in sorted_positions:
        items = plan_by_pos[pos]
        items.sort(key=lambda x: x["citation_number"])
        keys = [papers[it["paper_idx"]].get("bibtex_key", f"ref{it['citation_number']}") for it in items]
        cite_cmd = f"~\\cite{{{','.join(keys)}}}"
        insert_at = pos
        while insert_at > 0 and inserted[insert_at - 1] in ".!?":
            insert_at -= 1
        inserted = inserted[:insert_at] + cite_cmd + inserted[insert_at:]

    papers_by_number: dict[int, dict] = {}
    for item in insertion_plan:
        papers_by_number[item["citation_number"]] = papers[item["paper_idx"]]

    bib_content = None
    document_end_idx = inserted.rfind("\\end{document}")

    if use_bibtex:
        bib_content = _build_bib_file(list(papers_by_number.values()))
        if not BIBLIOGRAPHY_CMD_RE.search(inserted):
            if document_end_idx > 0:
                insertion = "\n\\bibliographystyle{plain}\n\\bibliography{scipilot_refs}\n"
                inserted = inserted[:document_end_idx] + insertion + inserted[document_end_idx:]
    else:
        thebib = _build_thebibliography(papers_by_number, style)
        if BIB_BLOCK_RE.search(inserted):
            inserted = BIB_BLOCK_RE.sub(thebib, inserted)
        else:
            if document_end_idx > 0:
                inserted = inserted[:document_end_idx] + "\n" + thebib + "\n" + inserted[document_end_idx:]
            else:
                inserted += "\n" + thebib + "\n"

    return inserted, bib_content


def run(
    tex_path: str,
    papers_json_path: str,
    style: str = "ieee",
    use_bibtex: bool = False,
    output_path: str | None = None,
    bib_output_path: str | None = None,
) -> dict:
    with open(tex_path, encoding="utf-8") as f:
        tex_content = f.read()
    with open(papers_json_path, encoding="utf-8") as f:
        papers = json.load(f)

    parsed = parse_latex(tex_content)
    plan = find_insertion_points(parsed, papers)
    if not plan:
        logger.error("No insertion points found")
        return {"ok": False, "reason": "no insertion points"}

    new_tex, bib_content = insert_citations_to_latex(tex_content, papers, style, plan, use_bibtex)

    out_path = output_path or tex_path.replace(".tex", "_scipilot.tex")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_tex)
    logger.info(f"Wrote {out_path}")

    if bib_content is not None:
        bp = bib_output_path or os.path.join(os.path.dirname(out_path), "scipilot_refs.bib")
        with open(bp, "w", encoding="utf-8") as f:
            f.write(bib_content)
        logger.info(f"Wrote {bp}")
    return {"ok": True, "output": out_path, "insertions": len(plan), "papers": len(set(it["paper_idx"] for it in plan))}


def _cli() -> int:
    p = argparse.ArgumentParser(description="SciPilot-cite LaTeX citation inserter")
    p.add_argument("tex_file")
    p.add_argument("papers_json")
    p.add_argument("--style", default="ieee")
    p.add_argument("--bibtex", action="store_true")
    p.add_argument("--output")
    p.add_argument("--bib-output")
    args = p.parse_args()
    r = run(args.tex_file, args.papers_json, args.style, args.bibtex, args.output, args.bib_output)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(_cli())
