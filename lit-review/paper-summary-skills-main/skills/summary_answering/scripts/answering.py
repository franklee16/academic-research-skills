#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
answering.py — 文献问答工具

子命令：
  dump --root .
      检测 keyword_summary.xlsx / paper_archiving.xlsx 是否存在，并输出其内容 JSON：
      {"has_keyword":bool, "has_archiving":bool,
       "keyword": {"papers":[{"文献名","keywords":[...]}]},
       "archiving": {"columns":[...], "rows":[{...}]}}
      （供 Claude 据问题语义筛选文献）

  scandocx --folder note
      无表时的兜底：递归读取 docx 全文，输出 [{"filename","stem","text"},...]

  gendoc --out 关键词.docx --data names.json
      names.json = {"question":str, "direct":[文件名...], "related":[文件名...]}
      生成文献名单 docx。

  filter --archiving paper_archiving.xlsx --names names.json --out 关键词_文献总结筛选.xlsx
      从文献总结表中筛出这些文献名对应的行，另存为新表（保留表头与格式）。
"""
import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path

# Windows 控制台默认 GBK，docx 中的非 GBK 字符会导致 print 崩溃 —— 强制 UTF-8。
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _ensure(pip_name, mod_name):
    try:
        importlib.import_module(mod_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name, "-q"])


_ensure("python-docx", "docx")
_ensure("openpyxl", "openpyxl")

import docx  # noqa: E402
from openpyxl import Workbook, load_workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402


def norm(s):
    return str(s).strip()


def stem_key(name):
    return norm(Path(str(name)).stem)


def docx_to_text(path):
    d = docx.Document(str(path))
    parts = []
    for p in d.paragraphs:
        if p.text.strip():
            parts.append(p.text)
    for t in d.tables:
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells]
            if any(cells):
                parts.append(" | ".join(cells))
    return "\n".join(parts)


def list_docx(folder):
    root = Path(folder)
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("*.docx") if not p.name.startswith("~$"))


def read_keyword(xlsx):
    wb = load_workbook(str(xlsx))
    ws = wb.active
    header = [c.value for c in ws[1]]
    kws = [h for h in header[1:] if h]
    papers = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        hit = [h for h, v in zip(header[1:], r[1:]) if h and v]
        papers.append({"文献名": r[0], "keywords": hit})
    wb.close()
    return {"keywords": kws, "papers": papers}


def read_archiving(xlsx):
    wb = load_workbook(str(xlsx))
    ws = wb.active
    header = [c.value for c in ws[1]]
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        rows.append({h: v for h, v in zip(header, r)})
    wb.close()
    return {"columns": header, "rows": rows}


def _emit(obj, json_out, summary):
    if json_out:
        Path(json_out).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        summary = dict(summary)
        summary["json_out"] = json_out
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def cmd_dump(args):
    root = Path(args.root)
    kw_path = root / "keyword_summary.xlsx"
    ar_path = root / "paper_archiving.xlsx"
    out = {"has_keyword": kw_path.exists(), "has_archiving": ar_path.exists()}
    if kw_path.exists():
        out["keyword"] = read_keyword(kw_path)
    if ar_path.exists():
        out["archiving"] = read_archiving(ar_path)
    _emit(out, args.json_out,
          {"has_keyword": out["has_keyword"], "has_archiving": out["has_archiving"]})


def cmd_scandocx(args):
    res = [{"filename": p.name, "stem": p.stem, "text": docx_to_text(p)}
           for p in list_docx(args.folder)]
    _emit(res, args.json_out, {"count": len(res)})


def item_name(it):
    """条目可为字符串（仅文件名）或 {"name","note"}。"""
    return it.get("name", "") if isinstance(it, dict) else str(it)


def item_note(it):
    return it.get("note", "") if isinstance(it, dict) else ""


def _add_section(d, heading, items, note_label):
    d.add_heading(heading, level=1)
    if not items:
        d.add_paragraph("（无）")
        return
    for it in items:
        name = item_name(it)
        note = item_note(it)
        p = d.add_paragraph(style="List Bullet")
        p.add_run(name).bold = True
        if note:
            d.add_paragraph("%s%s" % (note_label, note))


def cmd_gendoc(args):
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    d = docx.Document()
    d.add_heading(data.get("question", "文献名单"), level=0)
    direct = data.get("direct", [])
    related = data.get("related", [])
    _add_section(d, "可直接回答的文献", direct, "如何回答：")
    _add_section(d, "话题相关的文献", related, "相关之处：")
    d.save(args.out)
    print(json.dumps({"out": args.out, "direct": len(direct), "related": len(related)},
                     ensure_ascii=False))


def cmd_filter(args):
    names = json.loads(Path(args.names).read_text(encoding="utf-8"))
    if isinstance(names, dict):
        items = names.get("direct", []) + names.get("related", [])
        wanted = set(stem_key(item_name(it)) for it in items)
    else:
        wanted = set(stem_key(item_name(it)) for it in names)
    src = load_workbook(str(args.archiving))
    sws = src.active
    header = [c.value for c in sws[1]]
    wb = Workbook()
    ws = wb.active
    ws.title = "筛选结果"
    ws.append(header)
    kept = 0
    for r in sws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        if stem_key(r[0]) in wanted:
            ws.append(list(r))
            kept += 1
    # 复用总结表的排版
    header_fill = PatternFill("solid", fgColor="D9E1F2")
    for ci in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(ci)].width = 30
        hc = ws.cell(row=1, column=ci)
        hc.font = Font(bold=True)
        hc.fill = header_fill
        hc.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for rr in range(2, ws.max_row + 1):
        for cc in range(1, len(header) + 1):
            ws.cell(row=rr, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    src.close()
    wb.save(args.out)
    print(json.dumps({"out": args.out, "kept": kept}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description="文献问答工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dump")
    d.add_argument("--root", default=".")
    d.add_argument("--json-out", dest="json_out", default=None)
    d.set_defaults(func=cmd_dump)

    s = sub.add_parser("scandocx")
    s.add_argument("--folder", default="note")
    s.add_argument("--json-out", dest="json_out", default=None)
    s.set_defaults(func=cmd_scandocx)

    g = sub.add_parser("gendoc")
    g.add_argument("--out", required=True)
    g.add_argument("--data", required=True)
    g.set_defaults(func=cmd_gendoc)

    f = sub.add_parser("filter")
    f.add_argument("--archiving", default="paper_archiving.xlsx")
    f.add_argument("--names", required=True)
    f.add_argument("--out", required=True)
    f.set_defaults(func=cmd_filter)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
