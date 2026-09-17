"""Office Math Markup Language (OMML) helpers for python-docx documents.

Builds Word-native editable OMML formulas from a lightweight text notation.
Supports Greek letters (bare name or backslash command), sub/superscripts,
fractions, n-ary operators (sum, product, integral), radicals, accents
(hat, bar, tilde), delimiters, styled text, and common math symbols.

Syntax examples::

    y_{it} = beta_0 + beta_1 x_{it} + epsilon_{it}
    \\frac{\\partial y}{\\partial x}
    \\sum_{i=1}^{N}{x_i}
    \\hat{\\beta}_{OLS}
    \\sqrt{n}  or  \\sqrt[3]{x}
    \\left( \\frac{a}{b} \\right)
    \\text{if } x \\geq 0
"""

from docx.oxml import OxmlElement
from docx.oxml.ns import qn


MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ε", "varepsilon": "ε", "zeta": "ζ", "eta": "η",
    "theta": "θ", "vartheta": "ϑ", "iota": "ι", "kappa": "κ",
    "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "varrho": "ϱ", "sigma": "σ",
    "tau": "τ", "upsilon": "υ", "phi": "φ", "varphi": "ϕ",
    "chi": "χ", "psi": "ψ", "omega": "ω",
    "Delta": "Δ", "Gamma": "Γ", "Lambda": "Λ", "Omega": "Ω",
    "Phi": "Φ", "Pi": "Π", "Psi": "Ψ", "Sigma": "Σ",
    "Theta": "Θ", "Xi": "Ξ", "Upsilon": "Υ",
}

# LaTeX-style symbol commands mapped to Unicode characters.
SYMBOLS = {
    "partial": "∂", "infty": "∞", "nabla": "∇",
    "leq": "≤", "geq": "≥", "neq": "≠", "ll": "≪", "gg": "≫",
    "approx": "≈", "sim": "∼", "simeq": "≃", "equiv": "≡", "propto": "∝",
    "in": "∈", "notin": "∉", "ni": "∋",
    "subset": "⊂", "subseteq": "⊆", "supset": "⊃", "supseteq": "⊇",
    "emptyset": "∅", "cap": "∩", "cup": "∪", "setminus": "∖",
    "forall": "∀", "exists": "∃", "neg": "¬", "wedge": "∧", "vee": "∨",
    "times": "×", "cdot": "·", "div": "÷", "circ": "∘",
    "otimes": "⊗", "oplus": "⊕",
    "pm": "±", "mp": "∓",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "leftrightarrow": "↔",
    "Rightarrow": "⇒", "Leftarrow": "⇐", "Leftrightarrow": "⇔",
    "mapsto": "↦", "uparrow": "↑", "downarrow": "↓",
    "ldots": "…", "cdots": "⋯", "vdots": "⋮", "ddots": "⋱",
    "prime": "′",
    "ell": "ℓ", "Re": "ℜ", "Im": "ℑ", "aleph": "ℵ",
    "perp": "⊥", "angle": "∠", "parallel": "∥",
    "star": "⋆", "dagger": "†",
}

# N-ary (big) operator commands mapped to their Unicode operator characters.
NARY_CHARS = {
    "sum": "∑", "prod": "∏", "coprod": "∐",
    "int": "∫", "iint": "∬", "iiint": "∭", "oint": "∮",
    "bigcup": "⋃", "bigcap": "⋂",
    "bigoplus": "⨁", "bigotimes": "⨂",
    "bigvee": "⋁", "bigwedge": "⋀",
}

# Accent commands mapped to their OMML accent characters.
ACCENTS = {
    "hat": "\u0302", "widehat": "\u0302",
    "bar": "\u0305", "overline": "\u0305",
    "tilde": "\u0303", "widetilde": "\u0303",
    "dot": "\u0307", "ddot": "\u0308",
    "vec": "\u20D7",
    "check": "\u030C", "breve": "\u0306",
    "acute": "\u0301", "grave": "\u0300",
}

# Mapping for \left / \right delimiter characters.
_DELIM_MAP = {
    "(": "(", ")": ")", "[": "[", "]": "]",
    "{": "{", "}": "}",
    "|": "|", ".": "",
}


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _m(tag):
    return OxmlElement(f"m:{tag}")


def _m_val(tag, val):
    """Create an ``m:*`` element with an ``m:val`` attribute."""
    el = _m(tag)
    el.set(qn("m:val"), str(val))
    return el


def normalize_formula_token(text):
    return GREEK.get(text, text)


def _text_run(text):
    run = _m("r")
    text_el = _m("t")
    text_el.text = normalize_formula_token(text)
    run.append(text_el)
    return run


def _styled_run(text, style):
    """Create a math run with ``m:rPr`` style.

    Common styles: *p* = plain text, *b* = bold, *i* = italic, *bi* = bold-italic.
    """
    run = _m("r")
    rpr = _m("rPr")
    rpr.append(_m_val("sty", style))
    run.append(rpr)
    t = _m("t")
    t.text = text
    run.append(t)
    return run


# ---------------------------------------------------------------------------
# OMML structure builders
# ---------------------------------------------------------------------------

def _script_node(base, sub=None, sup=None):
    """Build sSub, sSup, or sSubSup from plain-text base/sub/sup values.

    Retained for backward compatibility with callers that pass simple strings.
    """
    if sub is not None and sup is not None:
        node = _m("sSubSup")
        for tag_name, content in [("e", base), ("sub", sub), ("sup", sup)]:
            child = _m(tag_name)
            child.append(_text_run(content))
            node.append(child)
        return node
    if sub is not None:
        node = _m("sSub")
        for tag_name, content in [("e", base), ("sub", sub)]:
            child = _m(tag_name)
            child.append(_text_run(content))
            node.append(child)
        return node
    if sup is not None:
        node = _m("sSup")
        for tag_name, content in [("e", base), ("sup", sup)]:
            child = _m(tag_name)
            child.append(_text_run(content))
            node.append(child)
        return node
    return _text_run(base)


def _wrap_elements(tag_name, elements):
    """Wrap a list of OMML elements inside ``m:<tag_name>``."""
    parent = _m(tag_name)
    for el in (elements or []):
        parent.append(el)
    return parent


def _script_node_rich(base_elements, sub_elements=None, sup_elements=None):
    """Build sSub/sSup/sSubSup where children are lists of OMML elements."""
    if sub_elements is not None and sup_elements is not None:
        node = _m("sSubSup")
        node.append(_wrap_elements("e", base_elements))
        node.append(_wrap_elements("sub", sub_elements))
        node.append(_wrap_elements("sup", sup_elements))
        return node
    if sub_elements is not None:
        node = _m("sSub")
        node.append(_wrap_elements("e", base_elements))
        node.append(_wrap_elements("sub", sub_elements))
        return node
    if sup_elements is not None:
        node = _m("sSup")
        node.append(_wrap_elements("e", base_elements))
        node.append(_wrap_elements("sup", sup_elements))
        return node
    return base_elements


def _fraction_node(num_elements, den_elements):
    """Build ``m:f`` (fraction)."""
    node = _m("f")
    node.append(_wrap_elements("num", num_elements))
    node.append(_wrap_elements("den", den_elements))
    return node


def _nary_node(char, sub_elements=None, sup_elements=None, operand_elements=None):
    """Build ``m:nary`` for summation, product, integral, etc."""
    node = _m("nary")
    pr = _m("naryPr")
    pr.append(_m_val("chr", char))
    node.append(pr)
    node.append(_wrap_elements("sub", sub_elements))
    node.append(_wrap_elements("sup", sup_elements))
    node.append(_wrap_elements("e", operand_elements))
    return node


def _radical_node(content_elements, degree_elements=None):
    """Build ``m:rad`` (radical / square root / nth root)."""
    node = _m("rad")
    pr = _m("radPr")
    if not degree_elements:
        pr.append(_m_val("degHide", "1"))
    node.append(pr)
    node.append(_wrap_elements("deg", degree_elements))
    node.append(_wrap_elements("e", content_elements))
    return node


def _accent_node(char, content_elements):
    """Build ``m:acc`` (accent mark such as hat, bar, tilde)."""
    node = _m("acc")
    pr = _m("accPr")
    pr.append(_m_val("chr", char))
    node.append(pr)
    node.append(_wrap_elements("e", content_elements))
    return node


def _delimiter_node(beg_char, end_char, content_elements):
    """Build ``m:d`` (delimiter pair such as parentheses, brackets)."""
    node = _m("d")
    pr = _m("dPr")
    pr.append(_m_val("begChr", beg_char))
    pr.append(_m_val("endChr", end_char))
    node.append(pr)
    node.append(_wrap_elements("e", content_elements))
    return node


# ---------------------------------------------------------------------------
# Tokeniser / parser helpers
# ---------------------------------------------------------------------------

def _is_name_char(char):
    return char.isalnum() or char in {".", "'"}


def _read_base(text, start):
    if _is_name_char(text[start]):
        end = start + 1
        while end < len(text) and _is_name_char(text[end]):
            end += 1
        return text[start:end], end
    return text[start], start + 1


def _read_brace_group(text, start):
    """Read a ``{…}`` group.  If *text[start]* is not ``{``, read one token."""
    if start >= len(text):
        return "", start
    if text[start] == "{":
        depth = 1
        end = start + 1
        while end < len(text) and depth > 0:
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
            end += 1
        return (text[start + 1 : end - 1] if depth == 0 else text[start + 1 : end]), end
    if text[start] == "\\":
        cmd, end = _read_command_name(text, start)
        return "\\" + cmd, end
    return _read_base(text, start)


def _read_command_name(text, start):
    """Read ``\\name`` starting at the backslash.  Returns *(name, end)*."""
    if start >= len(text) or text[start] != "\\":
        return "", start
    end = start + 1
    while end < len(text) and text[end].isalpha():
        end += 1
    return text[start + 1 : end], end


def _read_script_value(text, start):
    """Read a sub/superscript value (single token or ``{…}`` group)."""
    if start >= len(text):
        return "", start
    return _read_brace_group(text, start)


def _skip_spaces(text, index):
    while index < len(text) and text[index] == " ":
        index += 1
    return index


def _read_delim_char(text, index):
    """Read one delimiter character (or ``\\{`` / ``\\}``) after
    ``\\left`` or ``\\right``."""
    if index >= len(text):
        return "", index
    if text[index] == "\\" and index + 1 < len(text) and text[index + 1] in {"{", "}"}:
        return text[index + 1], index + 2
    return text[index], index + 1


def _read_math_atom(text, index):
    """Read a single *math atom* — a complete unit including a command or token,
    its brace/bracket arguments, and any trailing sub/superscripts.

    Used to consume the operand of n-ary operators when the operand is not
    wrapped in explicit braces.  Returns *(atom_text, end_index)*.
    """
    if index >= len(text):
        return "", index
    start = index
    if text[index] == "{":
        _, index = _read_brace_group(text, index)
    elif text[index] == "\\":
        _, index = _read_command_name(text, index)
        # Optional [] argument (e.g. \sqrt[3]{x}).
        if index < len(text) and text[index] == "[":
            bracket_end = text.find("]", index)
            index = bracket_end + 1 if bracket_end >= 0 else len(text)
        # Consecutive brace-group arguments.
        while index < len(text) and text[index] == "{":
            _, index = _read_brace_group(text, index)
    else:
        _, index = _read_base(text, index)
    # Include trailing sub/superscripts.
    while index < len(text) and text[index] in {"_", "^"}:
        _, index = _read_script_value(text, index + 1)
    return text[start:index], index


def _apply_trailing_scripts(element, text, index):
    """If *text[index]* starts with ``_`` or ``^``, wrap *element* in a
    script node and return *(result, new_index)*.  Otherwise return
    *(element, index)* unchanged."""
    sub = sup = None
    while index < len(text) and text[index] in {"_", "^"}:
        marker = text[index]
        val, index = _read_script_value(text, index + 1)
        if marker == "_":
            sub = val
        else:
            sup = val
    if sub is not None or sup is not None:
        return _script_node_rich(
            [element],
            _parse_elements(sub) if sub is not None else None,
            _parse_elements(sup) if sup is not None else None,
        ), index
    return element, index


# ---------------------------------------------------------------------------
# Recursive descent parser
# ---------------------------------------------------------------------------

def _parse_elements(text):
    """Parse formula *text* into a list of OMML XML elements.

    The parser is recursive: brace-delimited arguments are themselves parsed
    via ``_parse_elements``, enabling arbitrarily nested constructs such as
    ``\\frac{\\hat{beta}_{1}}{\\sqrt{n}}``.
    """
    elements = []
    index = 0
    while index < len(text):
        char = text[index]

        # ---- whitespace ---------------------------------------------------
        if char.isspace():
            start = index
            while index < len(text) and text[index].isspace():
                index += 1
            elements.append(_text_run(text[start:index]))
            continue

        # ---- backslash command --------------------------------------------
        if char == "\\":
            cmd, index = _read_command_name(text, index)
            if not cmd:
                # Bare backslash — render literally.
                elements.append(_text_run("\\"))
                continue

            # --- simple symbol replacement ---------------------------------
            if cmd in SYMBOLS:
                el = _text_run(SYMBOLS[cmd])
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- Greek letter (via backslash: \beta) -----------------------
            if cmd in GREEK:
                el = _text_run(GREEK[cmd])
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- fraction: \frac{num}{den} ---------------------------------
            if cmd == "frac":
                index = _skip_spaces(text, index)
                num_text, index = _read_brace_group(text, index)
                index = _skip_spaces(text, index)
                den_text, index = _read_brace_group(text, index)
                el = _fraction_node(
                    _parse_elements(num_text),
                    _parse_elements(den_text),
                )
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- radical: \sqrt{x} or \sqrt[n]{x} -------------------------
            if cmd == "sqrt":
                index = _skip_spaces(text, index)
                degree_text = None
                if index < len(text) and text[index] == "[":
                    bracket_end = text.find("]", index)
                    if bracket_end < 0:
                        bracket_end = len(text)
                    degree_text = text[index + 1 : bracket_end]
                    index = min(bracket_end + 1, len(text))
                index = _skip_spaces(text, index)
                content_text, index = _read_brace_group(text, index)
                el = _radical_node(
                    _parse_elements(content_text),
                    _parse_elements(degree_text) if degree_text else None,
                )
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- accent: \hat{x}, \bar{x}, \tilde{y}, … -------------------
            if cmd in ACCENTS:
                index = _skip_spaces(text, index)
                content_text, index = _read_brace_group(text, index)
                el = _accent_node(
                    ACCENTS[cmd],
                    _parse_elements(content_text),
                )
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- n-ary operator: \sum, \prod, \int, … ---------------------
            if cmd in NARY_CHARS:
                index = _skip_spaces(text, index)
                sub = sup = None
                while index < len(text) and text[index] in {"_", "^"}:
                    marker = text[index]
                    val, index = _read_script_value(text, index + 1)
                    if marker == "_":
                        sub = val
                    else:
                        sup = val
                    index = _skip_spaces(text, index)
                # Read the operand: explicit brace group or next math atom.
                operand_text = None
                if index < len(text):
                    if text[index] == "{":
                        operand_text, index = _read_brace_group(text, index)
                    else:
                        operand_text, index = _read_math_atom(text, index)
                elements.append(_nary_node(
                    NARY_CHARS[cmd],
                    _parse_elements(sub) if sub is not None else None,
                    _parse_elements(sup) if sup is not None else None,
                    _parse_elements(operand_text) if operand_text else None,
                ))
                continue

            # --- \left … \right delimiter pair ----------------------------
            if cmd == "left":
                open_char, index = _read_delim_char(text, index)
                # Scan forward to find the matching \right.
                depth = 1
                content_start = index
                content_end = len(text)
                close_char = ""
                scan = index
                while scan < len(text) and depth > 0:
                    if text[scan] == "\\":
                        pcmd, pend = _read_command_name(text, scan)
                        if pcmd == "left":
                            depth += 1
                            _, scan = _read_delim_char(text, pend)
                        elif pcmd == "right":
                            depth -= 1
                            if depth == 0:
                                content_end = scan
                                close_char, scan = _read_delim_char(text, pend)
                                break
                            _, scan = _read_delim_char(text, pend)
                        else:
                            scan = pend
                    else:
                        scan += 1
                index = scan
                beg = _DELIM_MAP.get(open_char, open_char)
                end = _DELIM_MAP.get(close_char, close_char)
                el = _delimiter_node(
                    beg, end,
                    _parse_elements(text[content_start:content_end]),
                )
                el, index = _apply_trailing_scripts(el, text, index)
                elements.append(el)
                continue

            # --- \text{…} — plain (upright) text inside math ---------------
            if cmd == "text":
                index = _skip_spaces(text, index)
                content, index = _read_brace_group(text, index)
                elements.append(_styled_run(content, "p"))
                continue

            # --- \mathbf{…} — bold math ------------------------------------
            if cmd == "mathbf":
                index = _skip_spaces(text, index)
                content, index = _read_brace_group(text, index)
                elements.append(_styled_run(content, "b"))
                continue

            # --- \mathit{…} — italic math (explicit) ----------------------
            if cmd == "mathit":
                index = _skip_spaces(text, index)
                content, index = _read_brace_group(text, index)
                elements.append(_styled_run(content, "i"))
                continue

            # --- unknown command — render name as plain text ---------------
            el = _text_run(cmd)
            el, index = _apply_trailing_scripts(el, text, index)
            elements.append(el)
            continue

        # ---- regular token with optional sub/superscripts -----------------
        base, index = _read_base(text, index)
        el = _text_run(normalize_formula_token(base))
        el, index = _apply_trailing_scripts(el, text, index)
        elements.append(el)

    return elements


# ---------------------------------------------------------------------------
# Public API (backward-compatible signatures)
# ---------------------------------------------------------------------------

def omath_text(text):
    """Build an ``m:oMath`` element from formula *text*."""
    omath = _m("oMath")
    for el in _parse_elements(text):
        omath.append(el)
    return omath


def omath_para_text(text):
    """Build an ``m:oMathPara`` (display-mode) element from formula *text*."""
    para = _m("oMathPara")
    para.append(omath_text(text))
    return para


def append_display_equation(document, text):
    """Append a display equation paragraph to *document*."""
    paragraph = document.add_paragraph()
    paragraph._p.append(omath_para_text(text))
    return paragraph


def append_inline_equation(paragraph, text):
    """Append an inline equation to *paragraph*."""
    paragraph._p.append(omath_text(text))
    return paragraph


def count_omml(document_element):
    """Count ``m:oMath`` elements using proper XML namespace search."""
    ns = f"{{{MATH_NS}}}"
    try:
        return len(document_element.findall(f".//{ns}oMath"))
    except Exception:
        # Fallback for elements without findall support.
        import re
        xml_text = getattr(document_element, "xml", "")
        return len(re.findall(r"<m:oMath[\s>]", xml_text))
