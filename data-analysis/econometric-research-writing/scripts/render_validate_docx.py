import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def renderer_candidates_from_root(root):
    root = Path(root).expanduser()
    candidates = [
        root / "render_docx.py",
        root / "documents/render_docx.py",
        root / "skills/documents/render_docx.py",
    ]
    candidates.extend(sorted(root.glob("*/skills/documents/render_docx.py"), reverse=True))
    return candidates


def find_renderer():
    for env_name in ["DOCX_RENDER_SCRIPT", "DOCUMENTS_RENDER_SCRIPT"]:
        value = os.environ.get(env_name)
        if value:
            path = Path(value).expanduser()
            if path.exists():
                return path

    for env_name in ["DOCUMENTS_SKILL_ROOT", "DOCUMENT_RENDERER_SEARCH_ROOTS"]:
        value = os.environ.get(env_name)
        if not value:
            continue
        for part in value.split(os.pathsep):
            if not part:
                continue
            for path in renderer_candidates_from_root(part):
                if path.exists():
                    return path

    for command in ["render_docx.py", "render_docx"]:
        value = shutil.which(command)
        if value:
            return Path(value)

    return None


def choose_python():
    for value in [
        os.environ.get("WORKSPACE_PYTHON"),
        os.environ.get("PYTHON"),
        sys.executable,
        shutil.which("python3"),
    ]:
        if not value:
            continue
        path = Path(value).expanduser()
        if path.exists():
            return str(path)
    return sys.executable


def render_env():
    env = os.environ.copy()
    bin_value = os.environ.get("WORKSPACE_BIN") or os.environ.get("DOCUMENT_RENDERER_BIN")
    if bin_value and Path(bin_value).expanduser().exists():
        current = env.get("PATH", "")
        env["PATH"] = str(Path(bin_value).expanduser()) + (os.pathsep + current if current else "")
    return env


def main():
    parser = argparse.ArgumentParser(description="Render a DOCX for visual QA using the bundled document renderer.")
    parser.add_argument("docx")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--emit-pdf", action="store_true")
    args = parser.parse_args()

    renderer = find_renderer()
    if renderer is None:
        raise SystemExit(
            "Error: visual QA was not run because documents/render_docx.py could not be found. "
            "Load the document-rendering dependency or set DOCX_RENDER_SCRIPT."
        )

    cmd = [choose_python(), str(renderer), args.docx, "--output_dir", args.output_dir]
    if args.emit_pdf:
        cmd.append("--emit_pdf")
    try:
        subprocess.check_call(cmd, env=render_env(), timeout=300)
    except subprocess.TimeoutExpired:
        raise SystemExit("Error: rendering process timed out after 300 seconds.")
    pngs = sorted(Path(args.output_dir).glob("page-*.png"))
    if not pngs:
        raise SystemExit("render produced no page PNGs")
    print(f"rendered_pages: {len(pngs)}")
    for p in pngs:
        print(p)


if __name__ == "__main__":
    main()
