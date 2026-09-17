#!/usr/bin/env python3
"""Compute lightweight style metrics for academic manuscripts.

The script intentionally uses only the Python standard library so a skill user
can run it in constrained workspaces. It accepts .txt, .md, and .tex files or
folders containing those files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_SUFFIXES = {".txt", ".md", ".tex"}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "their",
    "these",
    "this",
    "to",
    "was",
    "we",
    "were",
    "with",
}

CONNECTORS = [
    "however",
    "therefore",
    "thus",
    "moreover",
    "furthermore",
    "nevertheless",
    "whereas",
    "although",
    "because",
    "consequently",
    "in contrast",
    "in addition",
    "taken together",
]


@dataclass
class SectionMetrics:
    document: str
    section: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    avg_sentence_words: float
    avg_paragraph_words: float
    citation_count: int
    first_sentence: str
    last_sentence: str


@dataclass
class DocumentMetrics:
    path: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    avg_sentence_words: float
    avg_paragraph_words: float
    citation_count: int
    section_count: int
    frequent_terms: list[tuple[str, int]]
    connectors: dict[str, int]


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def iter_input_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(
                p
                for p in path.rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
            )
        elif path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.append(path)
    return sorted(set(files))


def strip_tex_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        cut = None
        for match in re.finditer(r"(?<!\\)%", line):
            cut = match.start()
            break
        lines.append(line if cut is None else line[:cut])
    return "\n".join(lines)


def normalize_tex(text: str) -> str:
    text = strip_tex_comments(text)
    text = re.sub(r"\\(section|subsection|subsubsection)\*?\{([^{}]*)\}", r"\n# \2\n", text)
    text = re.sub(r"\\(cite\w*|ref|autoref|cref|Cref)\*?(\[[^\]]*\])?\{([^{}]*)\}", r" [CITE] ", text)
    text = re.sub(r"\\(begin|end)\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}]", " ", text)
    return text


def normalize_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def normalized_text(path: Path, text: str) -> str:
    if path.suffix.lower() == ".tex":
        return normalize_tex(text)
    if path.suffix.lower() == ".md":
        return normalize_markdown(text)
    return text


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)?|\d+(?:\.\d+)?", text)


def sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", cleaned)
    return [part.strip() for part in parts if len(words(part)) > 2]


def paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n+", text)
    return [part.strip() for part in parts if len(words(part)) > 3]


def citation_count(raw: str, suffix: str) -> int:
    if suffix == ".tex":
        return len(re.findall(r"\\cite\w*\*?(?:\[[^\]]*\])?\{[^{}]+\}", raw))
    if suffix == ".md":
        return len(re.findall(r"\[[^\]]+\]\([^)]+\)|\[[0-9,\-\s]+\]", raw))
    return 0


def markdown_heading_offsets(raw: str) -> list[tuple[int, int, str]]:
    matches: list[tuple[int, int, str]] = []
    offset = 0
    in_fence = False
    for line in raw.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
        if not in_fence:
            match = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
            if match:
                matches.append((offset, offset + len(line), match.group(2).strip()))
        offset += len(line)
    return matches


def split_sections(path: Path, raw: str) -> list[tuple[str, str]]:
    if path.suffix.lower() == ".tex":
        raw = strip_tex_comments(raw)
        pattern = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^{}]+)\}")
        matches = [(m.start(), m.end(), m.group(2).strip()) for m in pattern.finditer(raw)]
    elif path.suffix.lower() == ".md":
        matches = markdown_heading_offsets(raw)
    else:
        return [("Full text", raw)]

    if not matches:
        return [("Full text", raw)]

    sections: list[tuple[str, str]] = []
    intro = raw[: matches[0][0]].strip()
    if intro:
        sections.append(("Front matter", intro))

    for index, match in enumerate(matches):
        title = match[2]
        start = match[1]
        end = matches[index + 1][0] if index + 1 < len(matches) else len(raw)
        body = raw[start:end].strip()
        sections.append((title, body))
    return sections


def average(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 2) if denominator else 0.0


def document_metrics(path: Path, raw: str, clean: str) -> DocumentMetrics:
    doc_words = words(clean)
    doc_sentences = sentences(clean)
    doc_paragraphs = paragraphs(clean)
    lower = clean.lower()
    terms = Counter(
        token.lower()
        for token in doc_words
        if len(token) > 3 and token.lower() not in STOPWORDS and not token.isdigit()
    )
    connector_counts = {item: lower.count(item) for item in CONNECTORS if lower.count(item)}
    return DocumentMetrics(
        path=str(path),
        word_count=len(doc_words),
        sentence_count=len(doc_sentences),
        paragraph_count=len(doc_paragraphs),
        avg_sentence_words=average(len(doc_words), len(doc_sentences)),
        avg_paragraph_words=average(len(doc_words), len(doc_paragraphs)),
        citation_count=citation_count(raw, path.suffix.lower()),
        section_count=len(split_sections(path, raw)),
        frequent_terms=terms.most_common(15),
        connectors=connector_counts,
    )


def section_metrics(path: Path, raw: str) -> list[SectionMetrics]:
    metrics: list[SectionMetrics] = []
    for title, body in split_sections(path, raw):
        clean = normalized_text(path, body)
        sec_words = words(clean)
        sec_sentences = sentences(clean)
        sec_paragraphs = paragraphs(clean)
        metrics.append(
            SectionMetrics(
                document=path.name,
                section=title,
                word_count=len(sec_words),
                sentence_count=len(sec_sentences),
                paragraph_count=len(sec_paragraphs),
                avg_sentence_words=average(len(sec_words), len(sec_sentences)),
                avg_paragraph_words=average(len(sec_words), len(sec_paragraphs)),
                citation_count=citation_count(body, path.suffix.lower()),
                first_sentence=sec_sentences[0] if sec_sentences else "",
                last_sentence=sec_sentences[-1] if sec_sentences else "",
            )
        )
    return metrics


def md_escape(value: object) -> str:
    text = str(value).replace("\n", " ").strip()
    text = text.replace("|", "\\|")
    return text[:220] + "..." if len(text) > 220 else text


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out)


def render_markdown(documents: list[DocumentMetrics], sections: list[SectionMetrics]) -> str:
    lines = ["# Style Metrics", ""]
    lines.append("## Documents")
    lines.append("")
    lines.append(
        markdown_table(
            [
                "Document",
                "Words",
                "Sentences",
                "Paragraphs",
                "Avg Sent Words",
                "Avg Para Words",
                "Citations",
                "Sections",
            ],
            [
                [
                    Path(doc.path).name,
                    doc.word_count,
                    doc.sentence_count,
                    doc.paragraph_count,
                    doc.avg_sentence_words,
                    doc.avg_paragraph_words,
                    doc.citation_count,
                    doc.section_count,
                ]
                for doc in documents
            ],
        )
    )
    lines.append("")
    lines.append("## Section Metrics")
    lines.append("")
    lines.append(
        markdown_table(
            [
                "Document",
                "Section",
                "Words",
                "Sentences",
                "Paragraphs",
                "Avg Sent Words",
                "Citations",
            ],
            [
                [
                    sec.document,
                    sec.section,
                    sec.word_count,
                    sec.sentence_count,
                    sec.paragraph_count,
                    sec.avg_sentence_words,
                    sec.citation_count,
                ]
                for sec in sections
            ],
        )
    )
    lines.append("")
    lines.append("## Openings And Closings")
    lines.append("")
    lines.append(
        markdown_table(
            ["Document", "Section", "First Sentence", "Last Sentence"],
            [[sec.document, sec.section, sec.first_sentence, sec.last_sentence] for sec in sections],
        )
    )
    lines.append("")
    lines.append("## Frequent Terms")
    lines.append("")
    for doc in documents:
        terms = ", ".join(f"{term} ({count})" for term, count in doc.frequent_terms)
        connectors = ", ".join(f"{key} ({value})" for key, value in doc.connectors.items())
        lines.append(f"### {Path(doc.path).name}")
        lines.append("")
        lines.append(f"- Terms: {terms or 'none'}")
        lines.append(f"- Connectors: {connectors or 'none'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Compute academic writing style metrics.")
    parser.add_argument("paths", nargs="+", type=Path, help="Files or folders to analyze.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--markdown", action="store_true", help="Emit Markdown (default).")
    args = parser.parse_args(argv)

    files = iter_input_files(args.paths)
    if not files:
        print("No supported files found (.txt, .md, .tex).", file=sys.stderr)
        return 2

    documents: list[DocumentMetrics] = []
    sections: list[SectionMetrics] = []
    for path in files:
        raw = read_text(path)
        clean = normalized_text(path, raw)
        documents.append(document_metrics(path, raw, clean))
        sections.extend(section_metrics(path, raw))

    if args.json:
        print(
            json.dumps(
                {
                    "documents": [asdict(doc) for doc in documents],
                    "sections": [asdict(sec) for sec in sections],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(render_markdown(documents, sections), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
