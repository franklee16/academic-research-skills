#!/usr/bin/env python
"""Objective layout gate for Beamer decks built by the paper-slides skill.

Checks (hard failures -> exit 1):
  - page count within [--min-pages, --max-pages]
  - overlapping text blocks (bbox intersection > 3pt in both dims)
  - text blocks outside page bounds
  - --takeaway gaps < 6pt (gap between the block containing the key and the
    block stacked directly above it -- catches takeaway-bullets pulled into
    tables by negative \\vspace, which the LaTeX log never reports)

Warnings (advisory):
  - vertical gaps < 5pt between stacked multi-word blocks on any page

Usage:
  python verify_slides.py deck.pdf --min-pages 35 --max-pages 45 \
      --takeaway "earns 1.33" --takeaway "spread remains"

Notes:
  - requires pymupdf (import fitz)
  - takeaway keys must be plain text WITHOUT inline math: pymupdf splits
    blocks at $...$, so a key spanning math never matches. Pick words
    outside the math (e.g. "spread remains", not "spread is 0.71% (t = 2.76)")
"""
import argparse
import sys

try:
    import fitz
except ImportError:
    sys.exit("pymupdf not installed: pip install pymupdf")


def page_blocks(page):
    return [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--min-pages", type=int, default=1)
    ap.add_argument("--max-pages", type=int, default=10**6)
    ap.add_argument("--takeaway", action="append", default=[],
                    help="plain-text key inside a takeaway bullet; repeatable")
    ap.add_argument("--min-gap", type=float, default=6.0,
                    help="minimum table-to-takeaway gap in pt (default 6)")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    hard = []
    warn = []

    n = len(doc)
    if n < args.min_pages or n > args.max_pages:
        hard.append(f"page count {n} outside [{args.min_pages}, {args.max_pages}]")
    print(f"pages: {n} (budget {args.min_pages}-{args.max_pages})")

    for i, page in enumerate(doc):
        pr = page.rect
        blocks = page_blocks(page)

        for b in blocks:
            x0, y0, x1, y1 = b[:4]
            if x1 > pr.width + 2 or y1 > pr.height + 2 or x0 < -2 or y0 < -2:
                hard.append(f"p{i+1}: out-of-bounds block {b[4][:40]!r}")

        for a in range(len(blocks)):
            for c in range(a + 1, len(blocks)):
                ax0, ay0, ax1, ay1 = blocks[a][:4]
                bx0, by0, bx1, by1 = blocks[c][:4]
                if min(ax1, bx1) - max(ax0, bx0) > 3 and min(ay1, by1) - max(ay0, by0) > 3:
                    hard.append(f"p{i+1}: OVERLAP {blocks[a][4][:25]!r} vs {blocks[c][4][:25]!r}")

        # advisory: tight stacking between multi-word blocks (may be dense table rows)
        for a in range(len(blocks)):
            for c in range(len(blocks)):
                if a == c:
                    continue
                ax0, ay0, ax1, ay1 = blocks[a][:4]
                bx0, by0, bx1, by1 = blocks[c][:4]
                if min(ax1, bx1) - max(ax0, bx0) > 20:
                    g = by0 - ay1
                    if 0 <= g < 5 and len(blocks[a][4].split()) > 4 and len(blocks[c][4].split()) > 4:
                        warn.append(f"p{i+1}: tight gap {g:.1f}pt between stacked blocks")

    for key in args.takeaway:
        found = False
        for i, page in enumerate(doc):
            blocks = page_blocks(page)
            tb = next((b for b in blocks if key in b[4]), None)
            if tb is None:
                continue
            above = [b for b in blocks
                     if b is not tb and b[3] <= tb[1] + 1
                     and min(b[2], tb[2]) - max(b[0], tb[0]) > 20]
            if not above:
                print(f"takeaway {key!r}: p{i+1} nothing above it (suspicious)")
                found = True
                break
            gap = tb[1] - max(b[3] for b in above)
            status = "OK" if gap >= args.min_gap else "FAIL"
            if gap < args.min_gap:
                hard.append(f"takeaway {key!r} on p{i+1}: gap {gap:.1f}pt < {args.min_gap}pt")
            print(f"takeaway {key!r}: p{i+1} gap {gap:.1f}pt {status}")
            found = True
            break
        if not found:
            hard.append(f"takeaway {key!r}: NOT FOUND in any page (check key: avoid inline math)")

    if warn:
        print("\nadvisory (review manually):")
        for w in dict.fromkeys(warn):
            print(" ", w)
    if hard:
        print("\nHARD FAILURES:")
        for h in hard:
            print(" ", h)
        sys.exit(1)
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
