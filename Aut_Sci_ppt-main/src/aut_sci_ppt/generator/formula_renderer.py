"""
formula_renderer.py — LaTeX-level Formula Rendering Engine for Scientific PPTs.

Features:
1. Detect local LaTeX environment (pdflatex, pdftoppm).
2. Fallback chain: Local LaTeX -> Offline Matplotlib -> Online Cloud API.
3. Automatic hashing and caching of formula images.

Original author: ShuoClaw
Integrated into Aut_Sci_PPt for open-source.
"""

import os
import subprocess
import tempfile
import hashlib
from typing import Optional, List, Tuple, Dict
from pathlib import Path
import requests

class FormulaRenderer:
    """
    LaTeX Formula Renderer with multi-stage fallback.
    """

    def __init__(self, dpi: int = 300, output_dir: Optional[str] = None):
        from ..config import Config
        self.dpi = dpi
        self.output_dir = output_dir or Config.FORMULA_CACHE_DIR
        self.latex_available = self._check_latex()

        os.makedirs(self.output_dir, exist_ok=True)

    def _check_latex(self) -> bool:
        """Detect if pdflatex is available in the system."""
        try:
            result = subprocess.run(
                ["pdflatex", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def render_formula(
        self,
        latex_code: str,
        color: str = "000000",
        background: str = "FFFFFF"
    ) -> Optional[str]:
        """
        Render LaTeX formula to PNG.

        Returns:
            Absolute path to the PNG image, or None if all methods fail.
        """
        # Generate cache filename based on content hash
        hash_obj = hashlib.mdsafe_hash(f"{latex_code}_{color}_{background}".encode())
        formula_id = hash_obj.hexdigest()[:12]
        output_path = os.path.join(self.output_dir, f"formula_{formula_id}.png")

        if os.path.exists(output_path):
            return output_path

        # 1. Local LaTeX (Best Quality)
        if self.latex_available:
            result = self._render_local(latex_code, output_path, color, background)
            if result: return result

        # 2. Hybrid/Fallback (Matplotlib for offline safety, API for convenience)
        return self._render_fallback(latex_code, output_path, color, background)

    def _render_local(self, latex_code, output_path, color, background) -> Optional[str]:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tex_file = os.path.join(tmpdir, "formula.tex")
                self._create_tex_file(tex_file, latex_code, color, background)

                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file],
                    capture_output=True, timeout=20
                )

                pdf_file = os.path.join(tmpdir, "formula.pdf")
                if os.path.exists(pdf_file):
                    # Try pdftoppm (fastest)
                    cmd = ["pdftoppm", "-png", "-r", str(self.dpi), "-singlefile", pdf_file, output_path.replace(".png", "")]
                    if subprocess.run(cmd, capture_output=True).returncode == 0:
                        return output_path
        except Exception:
            pass
        return None

    def _create_tex_file(self, tex_file, latex_code, color, background):
        tex_content = f"""\\documentclass[12pt]{{article}}
\\usepackage{{amsmath,amssymb,xcolor}}
\\usepackage[margin=0.1in]{{geometry}}
\\pagecolor[HTML]{{{background}}}
\\color[HTML]{{{color}}}
\\begin{{document}}
\\thispagestyle{{empty}}
\\[ {latex_code} \\]
\\end{{document}}"""
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(tex_content)

    def _render_fallback(self, latex_code, output_path, color, background) -> Optional[str]:
        # Offline: Matplotlib mathtext
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            fig = plt.figure(figsize=(0.1, 0.1), dpi=self.dpi)
            fig.text(0.5, 0.5, f"${latex_code}$", ha="center", va="center", fontsize=18, color=f"#{color}")
            fig.savefig(output_path, bbox_inches="tight", pad_inches=0.05, facecolor=f"#{background}", transparent=True)
            plt.close(fig)
            if os.path.exists(output_path): return output_path
        except Exception:
            pass

        # Online: CodeCogs (Last resort)
        try:
            encoded = requests.utils.quote(latex_code)
            url = f"https://latex.codecogs.com/png.image?\\dpi{{300}}\\bg_white\\inline\\color{{black}}{encoded}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return output_path
        except Exception:
            pass
        return None
