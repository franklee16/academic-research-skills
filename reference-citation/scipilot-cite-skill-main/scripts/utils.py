"""
SciPilot-cite :: utils.py
共享工具函数库
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.parse import urlparse

import requests

try:
    from Levenshtein import ratio as _lev_ratio
except ImportError:
    from difflib import SequenceMatcher

    def _lev_ratio(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

logger = logging.getLogger("scipilot-cite")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[SciPilot-cite] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

_LAST_REQUEST_TIME: dict[str, float] = {}
_LOG_LOCK = threading.Lock()

_STOPWORDS = set(
    """a an the and or but is are was were be been being have has had do does did
    will would could should may might can shall must of in on at to for with from by
    as into during including until against among throughout despite towards upon
    concerning regarding considering than such this that these those which who whom
    whose what when where why how all any both each few more most other some no nor
    not only own same so too very can will just don should now i me my we us our you
    your he him his she her it its they them their however therefore thus while
    although also we propose method approach paper present results show study
    research using based via through over under between""".split()
)


def title_similarity(title1: str, title2: str) -> float:
    """计算两个标题的相似度，忽略大小写、空格、标点。返回 0-1 之间的浮点数。"""

    def normalize(s: str) -> str:
        s = (s or "").lower()
        s = re.sub(r"[^\w\s]", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    n1, n2 = normalize(title1), normalize(title2)
    if not n1 or not n2:
        return 0.0
    return _lev_ratio(n1, n2)


def rate_limited_request(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    min_interval: float = 0.5,
    max_retries: int = 3,
    timeout: int = 20,
) -> Any:
    """
    带速率限制和自动重试的 HTTP GET 请求。
    返回解析后的 JSON 字典 / 文本字符串；失败返回 None。
    """
    domain = urlparse(url).netloc or url
    last = _LAST_REQUEST_TIME.get(domain, 0.0)
    elapsed = time.time() - last
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)

    for attempt in range(max_retries):
        try:
            _LAST_REQUEST_TIME[domain] = time.time()
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            ctype = resp.headers.get("content-type", "")
            if resp.status_code == 200:
                if "application/json" in ctype or url.endswith(".json"):
                    return resp.json()
                return resp.text
            if resp.status_code == 429:
                wait = 2 ** attempt * 2
                logger.warning(f"Rate limited ({domain}), waiting {wait}s")
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                wait = 2 ** attempt
                logger.warning(f"HTTP {resp.status_code} from {domain}, retry in {wait}s")
                time.sleep(wait)
                continue
            logger.warning(f"HTTP {resp.status_code} for {url}")
            return None
        except requests.RequestException as e:
            wait = 2 ** attempt
            logger.warning(f"Request failed: {e}, retry {attempt + 1}/{max_retries} in {wait}s")
            time.sleep(wait)
    logger.error(f"Giving up on {url} after {max_retries} retries")
    return None


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """基于频率的简单关键词抽取（剔除停用词）。"""
    if not text:
        return []
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]{2,}\b", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w in _STOPWORDS or len(w) <= 2:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:top_n]]


def assign_citation_numbers(insertion_plan: list[dict]) -> list[dict]:
    """
    根据插入位置的文档顺序分配编号 [1], [2], ...
    insertion_plan 项至少包含 'paper_idx' 和可比较的 'position' 字段。
    """
    sorted_plan = sorted(insertion_plan, key=lambda x: (x.get("position", 0), x.get("paper_idx", 0)))
    paper_to_num: dict[int, int] = {}
    out: list[dict] = []
    next_num = 1
    for item in sorted_plan:
        pid = item["paper_idx"]
        if pid not in paper_to_num:
            paper_to_num[pid] = next_num
            next_num += 1
        new_item = dict(item)
        new_item["citation_number"] = paper_to_num[pid]
        out.append(new_item)
    return out


def make_bibtex_key(paper: dict) -> str:
    """生成 BibTeX key: FirstAuthorLastName_Year_FirstKeyword"""
    authors = paper.get("authors", []) or []
    first_last = "Unknown"
    if authors:
        a0 = authors[0]
        name = a0 if isinstance(a0, str) else a0.get("name", "")
        parts = re.split(r"[\s,]+", name.strip())
        parts = [p for p in parts if p]
        if parts:
            last = parts[-1] if "," not in name else parts[0]
            first_last = re.sub(r"[^A-Za-z]", "", last) or "Unknown"
    year = paper.get("year") or "XXXX"
    title = paper.get("title", "") or ""
    keyword = "paper"
    for w in re.findall(r"\b[A-Za-z]+\b", title):
        if len(w) >= 4 and w.lower() not in _STOPWORDS:
            keyword = w.lower()
            break
    return f"{first_last}_{year}_{keyword}"


def normalize_author(name_or_obj: Any) -> str:
    """把任意作者表示统一成 'First Middle Last' 字符串。"""
    if isinstance(name_or_obj, str):
        return name_or_obj.strip()
    if isinstance(name_or_obj, dict):
        if "name" in name_or_obj:
            return str(name_or_obj["name"]).strip()
        given = name_or_obj.get("given", "")
        family = name_or_obj.get("family", "")
        return f"{given} {family}".strip()
    return str(name_or_obj)


def first_author_last_name(authors: Iterable) -> str:
    """提取首作者的姓（最后一个空格后的词）。"""
    authors = list(authors or [])
    if not authors:
        return ""
    name = normalize_author(authors[0])
    if "," in name:
        return name.split(",", 1)[0].strip()
    parts = name.split()
    return parts[-1] if parts else ""


def initials(given_name: str) -> str:
    """'John Quincy' -> 'J. Q.'"""
    parts = re.split(r"[\s\-]+", given_name.strip())
    return " ".join(f"{p[0].upper()}." for p in parts if p)


def author_initials_first(name: str) -> str:
    """'John Smith' -> 'J. Smith'；已经是姓在前则原样。"""
    name = name.strip()
    if "," in name:
        last, given = [p.strip() for p in name.split(",", 1)]
        return f"{initials(given)} {last}"
    parts = name.split()
    if len(parts) < 2:
        return name
    last = parts[-1]
    given = " ".join(parts[:-1])
    return f"{initials(given)} {last}"


def utc_now_iso() -> str:
    """ISO 8601 timestamp in UTC with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def paper_id_hash(paper: dict) -> str:
    """
    Stable 16-char hex id from DOI (preferred) or (normalized_title|year|first_author_last).
    Used to bind a paper across search → verify → audit stages.
    """
    doi = (paper.get("doi") or "").lower().strip()
    if doi:
        seed = f"doi:{doi}"
    else:
        raw_title = (paper.get("title") or "").lower()
        norm_title = re.sub(r"[^\w\s]", " ", raw_title)
        norm_title = re.sub(r"\s+", " ", norm_title).strip()
        year = str(paper.get("year") or "")
        first_last = first_author_last_name(paper.get("authors") or []).lower()
        seed = f"title:{norm_title}|year:{year}|author:{first_last}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def append_jsonl(path: str, record: dict) -> None:
    """Thread-safe append of one JSON record to a JSONL file."""
    if not path:
        return
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    with _LOG_LOCK:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def author_last_initials(name: str) -> str:
    """'John Smith' -> 'Smith, J.'"""
    name = name.strip()
    if "," in name:
        last, given = [p.strip() for p in name.split(",", 1)]
        return f"{last}, {initials(given)}"
    parts = name.split()
    if len(parts) < 2:
        return name
    last = parts[-1]
    given = " ".join(parts[:-1])
    return f"{last}, {initials(given)}"


if __name__ == "__main__":
    print("=== utils.py smoke test ===")
    s = title_similarity("Attention is all you need", "Attention Is All You Need.")
    print(f"title_similarity: {s:.4f}")
    assert s > 0.95

    kw = extract_keywords(
        "This paper proposes a novel reinforcement learning approach for "
        "large language model alignment and instruction tuning."
    )
    print(f"keywords: {kw}")

    key = make_bibtex_key(
        {"authors": ["Ashish Vaswani", "Noam Shazeer"], "year": 2017, "title": "Attention Is All You Need"}
    )
    print(f"bibtex_key: {key}")

    plan = [
        {"paper_idx": 5, "position": 200},
        {"paper_idx": 3, "position": 100},
        {"paper_idx": 5, "position": 300},
        {"paper_idx": 7, "position": 150},
    ]
    numbered = assign_citation_numbers(plan)
    for n in numbered:
        print(n)

    print(f"author_initials_first: {author_initials_first('John Quincy Adams')}")
    print(f"author_last_initials: {author_last_initials('John Quincy Adams')}")
    print("OK")
