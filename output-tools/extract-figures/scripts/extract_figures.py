"""Extract images from a Word .docx, convert vector formats to PNG, and write a manifest.

Usage:
    python extract_figures.py <docx_path> [<output_dir>]

Output directory defaults to <docx_dir>/figures/.
Output files:
    img_001.png, img_002.png, ...   # in document body XML order
    <original>.emf, .png, etc.       # originals preserved alongside
    _manifest.json                    # full mapping (rId, caption, position, etc.)
"""

import sys, os, io, re, json, zipfile, shutil
from pathlib import Path
from xml.etree import ElementTree as ET
from datetime import date

# Force UTF-8 on Windows CJK locales
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

P, T, PPR, PSTYLE = f"{{{W_NS}}}p", f"{{{W_NS}}}t", f"{{{W_NS}}}pPr", f"{{{W_NS}}}pStyle"
BLIP = f"{{{A_NS}}}blip"
EMBED = f"{{{R_NS}}}embed"

# Ext: (suffix, target_format)
VECTOR_EXTS = {".emf": (".png", "PNG"), ".wmf": (".png", "PNG"),
               ".emz": (".png", "PNG"), ".wmz": (".png", "PNG")}
RASTER_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}


def para_text(para):
    """Plain-text content of a <w:p>."""
    return "".join(t.text or "" for t in para.iter(T)).strip()


def find_captions(body_children):
    """Find all figure-caption paragraphs and their positions.

    Returns: list of (body_index, fig_number_str, caption_text)
    """
    captions = []
    for idx, child in enumerate(body_children):
        if child.tag != P:
            continue
        text = para_text(child)
        if not text:
            continue
        m = re.match(r"^(Figure|Fig\.?)\s*(\d+)", text, re.IGNORECASE)
        is_caption_style = False
        if not m:
            pPr = child.find(PPR)
            if pPr is not None:
                ps = pPr.find(PSTYLE)
                if ps is not None:
                    val = ps.get(f"{{{W_NS}}}val", "").lower()
                    if "caption" in val or "figure" in val:
                        is_caption_style = True
                        # Try to extract a trailing number
                        m2 = re.search(r"(\d+)", text)
                        if m2:
                            m = m2
        if m or is_caption_style:
            fig_num = m.group(2) if m else "0"
            captions.append((idx, fig_num, text))
    return captions


def extract_media(docx_path, out_dir):
    """Extract word/media/* files from the .docx zip."""
    extracted = []
    with zipfile.ZipFile(docx_path, "r") as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                fname = Path(name).name
                target = out_dir / fname
                with z.open(name) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append((name, fname, target))
    return extracted


def parse_rels(docx_path):
    """Parse word/_rels/document.xml.rels → {rId: Target path}."""
    rels = {}
    with zipfile.ZipFile(docx_path, "r") as z:
        with z.open("word/_rels/document.xml.rels") as f:
            root = ET.parse(f).getroot()
            for rel in root:
                if rel.tag.endswith("Relationship"):
                    rid = rel.get("Id")
                    target = rel.get("Target")
                    rtype = rel.get("Type", "")
                    if "image" in rtype.lower():
                        rels[rid] = target
    return rels


def parse_body_images(docx_path):
    """Walk document body, finding every image reference (rId).

    Returns list of dicts: [{rid, body_idx, embed_idx, para_text}]
    """
    with zipfile.ZipFile(docx_path, "r") as z:
        with z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()

    body = root.find(f"{{{W_NS}}}body")
    children = list(body)

    images = []
    for idx, child in enumerate(children):
        if child.tag != P:
            continue
        # Use namespace-aware attribute access instead of regex on serialized XML,
        # because ET.tostring() rewrites namespace prefixes (e.g. r:embed -> ns7:embed).
        embeds = []
        for elem in child.iter():
            if 'blip' in elem.tag:
                rid = elem.get(EMBED)
                if rid:
                    embeds.append(rid)
        if embeds:
            txt = para_text(child)
            for eidx, rid in enumerate(embeds):
                images.append({"rid": rid, "body_idx": idx, "embed_idx": eidx, "para_text": txt})
    return images


def convert_image(src_path, out_dir, dpi=300):
    """Convert EMF/WMF to PNG; return (target_path, ok). For rasters, just copy."""
    from PIL import Image
    ext = src_path.suffix.lower()
    if ext in VECTOR_EXTS:
        target = out_dir / (src_path.stem + ".png")
        try:
            img = Image.open(src_path)
            img.load()
            img.save(target, "PNG", dpi=(dpi, dpi))
            return target, True
        except Exception as e:
            print(f"WARN: Pillow failed on {src_path}: {e}", file=sys.stderr)
            return None, False
    elif ext in RASTER_EXTS:
        # Keep original name; it is already usable
        return src_path, True
    else:
        print(f"WARN: unknown format {src_path}", file=sys.stderr)
        return src_path, False


def assign_figures(images, captions):
    """Assign each image to the closest figure caption; then sort by body order.

    Returns list of dicts with extra keys: fig_num, pos_in_fig, caption_text.
    """
    if not captions:
        # No captions found — everything goes to Figure 1
        return [{**img, "fig_num": "1", "pos_in_fig": i + 1, "caption_text": "(no caption found)"}
                for i, img in enumerate(sorted(images, key=lambda x: (x["body_idx"], x["embed_idx"])))]

    result = []
    for img in images:
        # Find caption with minimum distance, preferring preceding over following
        best = None
        best_score = None
        for cidx, cnum, ctext in captions:
            dist = abs(img["body_idx"] - cidx)
            # Preceding captions are slightly preferred (usually figure caption is below image in Word)
            # Actually in many papers it's below.
            direction = -1 if cidx > img["body_idx"] else 1  # caption after = "below" = preferred
            score = (dist, direction)
            if best_score is None or score < best_score:
                best_score = score
                best = (cidx, cnum, ctext)
        result.append({**img, "fig_num": best[1], "pos_in_fig": 0, "caption_text": best[2]})

    # Sort by (fig_num, body_idx) and assign pos_in_fig
    result.sort(key=lambda x: (int(x["fig_num"]) if x["fig_num"].isdigit() else x["fig_num"],
                               x["body_idx"], x["embed_idx"]))

    fig_counter = {}
    for item in result:
        fn = item["fig_num"]
        fig_counter[fn] = fig_counter.get(fn, 0) + 1
        item["pos_in_fig"] = fig_counter[fn]
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_figures.py <docx_path> [<output_dir>]")
        sys.exit(1)

    docx_path = Path(sys.argv[1]).resolve()
    if not docx_path.exists():
        print(f"ERROR: {docx_path} does not exist", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else docx_path.parent / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting from: {docx_path}")
    print(f"Output folder:   {out_dir}")

    media = extract_media(docx_path, out_dir)
    print(f"Extracted {len(media)} media files")

    rels = parse_rels(docx_path)

    # Build a map rId -> source file path in output dir
    rid_to_src = {}
    rid_to_original_name = {}
    for rid, target in rels.items():
        original_name = Path(target).name
        rid_to_original_name[rid] = original_name
        src = out_dir / original_name
        if src.exists():
            rid_to_src[rid] = src
        else:
            # Some targets may be nested (media/dir/img.png)
            for _, fname, fpath in media:
                if fname == original_name or str(target).endswith(fname):
                    rid_to_src[rid] = fpath
                    rid_to_original_name[rid] = fname
                    break

    # Convert vectors to PNG
    rid_to_png = {}
    for rid, src in rid_to_src.items():
        out, ok = convert_image(src, out_dir)
        if ok and out:
            rid_to_png[rid] = out

    body_images = parse_body_images(docx_path)
    # Only keep images that have a matching rId in our map
    body_images = [img for img in body_images if img["rid"] in rid_to_png]

    # Find captions
    with zipfile.ZipFile(docx_path, "r") as z:
        with z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()
    body_children = list(root.find(f"{{{W_NS}}}body"))
    captions = find_captions(body_children)

    assignments = assign_figures(body_images, captions)

    # Copy/move to neutral sequential names in body order
    manifest = []
    for i, a in enumerate(assignments, start=1):
        rid = a["rid"]
        src = rid_to_png[rid]
        seq_name = f"img_{i:03d}.png"
        dst = out_dir / seq_name

        # Copy rather than move, so originals stay
        shutil.copy2(src, dst)
        if not (out_dir / rid_to_original_name[rid]).exists():
            # Original not in out_dir (shouldn't happen), skip
            pass

        manifest.append({
            "filename": seq_name,
            "original": rid_to_original_name[rid],
            "rid": rid,
            "body_idx": a["body_idx"],
            "embed_idx": a["embed_idx"],
            "fig_num": a["fig_num"],
            "pos_in_fig": a["pos_in_fig"],
            "caption_text": a["caption_text"],
        })

    manifest_path = out_dir / "_manifest.json"
    manifest_path.write_text(json.dumps({
        "source": str(docx_path),
        "output_dir": str(out_dir),
        "extracted_at": date.today().isoformat(),
        "images": manifest,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Done. {len(manifest)} images saved to {out_dir}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
