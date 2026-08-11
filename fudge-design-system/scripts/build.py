#!/usr/bin/env python3
"""
Build and verify a generated design system.

Inlines the system stylesheet into every HTML consumer, then runs the
verification gates from references/generation.md and reports the numbers.

    python build.py <system-dir> [--out <dir>]

Expects, inside <system-dir>:
    src/<name>.tokens.css   the emitted token layers (from emit.py)
    src/<name>.parts.css    the hand-authored stylesheet on those tokens
    src/*.shell.html        HTML consumers containing the marker below

A system that keeps everything in one stylesheet is still valid: a lone
src/<name>.css is taken as the whole thing.
"""

import argparse
import hashlib
import pathlib
import re
import sys

MARKER = "/*__SYSTEM_CSS__*/"


# --------------------------------------------------------------------------
# contrast
# --------------------------------------------------------------------------
def _srgb(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_str):
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------
# theme scopes
# --------------------------------------------------------------------------
# Ceiling: this is a brace-depth splitter, not a CSS parser. It only needs
# to separate top-level rulesets/at-rules from one another; the token
# regexes used against a block's raw text don't care about further nesting
# inside it (e.g. `@media (...) { :root { --x: #fff; } }` still yields
# `--x: #fff;`), so splitting one level deep is enough for every theme
# shape this gate is asked to recognise.
THEME_SELECTOR_PATTERNS = (
    r'\[data-theme=["\']?([\w-]+)["\']?\]',
    r'\.theme-([\w-]+)',
    r':root\.([\w-]+)',
    r'@media\s*\(\s*prefers-color-scheme:\s*(dark|light)\s*\)',
    # Print remaps tier 2 exactly the way a theme does, so it is a theme as
    # far as this gate is concerned. generation.md gives it its own
    # mandatory verification pass precisely because nothing about it is
    # visible in the browser.
    r'@media\s+(print)\b',
)


def top_level_blocks(css):
    """Split a stylesheet into (selector, content) pairs at brace depth 0."""
    blocks, depth, sel_start, block_start = [], 0, 0, None
    for i, ch in enumerate(css):
        if ch == "{":
            if depth == 0:
                block_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and block_start is not None:
                blocks.append((css[sel_start:block_start], css[block_start + 1:i]))
                sel_start = i + 1
                block_start = None
    return blocks


def theme_label(selector):
    """Name a theme from its selector, e.g. "dark" from [data-theme="dark"]."""
    for pattern in THEME_SELECTOR_PATTERNS:
        m = re.search(pattern, selector)
        if m:
            return m.group(1)
    return None


def theme_scopes(css):
    """Split a stylesheet into base tokens plus any scoped theme blocks.

    Returns (base_text, [(name, theme_text), ...]). theme_text holds only
    that theme's own declarations — callers layer it over base_text, since
    a theme typically redeclares just the semantic tier and inherits tier 1
    unchanged. Selectors that don't match a known theme shape (:root,
    body, ...) fall into base_text instead of being dropped.
    """
    base_chunks = []
    themes = {}
    for selector, content in top_level_blocks(css):
        label = theme_label(selector)
        if label is None:
            base_chunks.append(content)
        else:
            themes.setdefault(label, []).append(content)
    base_text = "\n".join(base_chunks)
    return base_text, [(name, "\n".join(chunks)) for name, chunks in themes.items()]


# --------------------------------------------------------------------------
# raw colour values
# --------------------------------------------------------------------------
# The line emit.py writes to mark where a literal colour stops being a
# primitive and starts being a leak. Held as text rather than imported:
# build.py verifies whatever stylesheet it is handed, including ones
# emit.py never wrote.
TIER_1_SENTINEL = "/* ---- end tier 1 · no raw values below this line ---- */"

# 3-, 4-, 6- and 8-digit hex, plus functional notation. `transparent`,
# `currentColor`, `inherit` and `none` are keywords and never match; the
# inner alternation lets one level of nesting through so a call like
# `rgb(var(--c) / 50%)` is matched whole and then exempted as an alias.
RAW_COLOUR = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b"
    r"|\b(?:rgba?|hsla?)\([^()]*(?:\([^()]*\)[^()]*)*\)"
)
BANNER = re.compile(r"/\* ---- (.*?) ---- \*/")


def blank_comments(css):
    """The same text with comment bodies blanked to spaces, offsets intact.

    A hex in a comment is a note, not a leak. Blanking rather than deleting
    keeps every index and line number reported downstream honest.
    """
    return re.sub(r"/\*.*?\*/",
                  lambda m: re.sub(r"[^\n]", " ", m.group(0)), css, flags=re.S)


def enclosing_rule(css, index):
    """The selectors open around `index`, outermost first."""
    stack, start = [], 0
    for i, ch in enumerate(css[:index]):
        if ch == "{":
            stack.append(css[start:i])
            start = i + 1
        elif ch == "}":
            if stack:
                stack.pop()
            start = i + 1
    return " › ".join(" ".join(s.split()) for s in stack if s.strip())


def enclosing_prop(css, index):
    """The property whose value `index` sits in, if it sits in one."""
    start = max(css.rfind(ch, 0, index) for ch in "{};")
    m = re.match(r"\s*([\w-]+)\s*:", css[start + 1:index])
    return m.group(1) if m else ""


def raw_colours_below_tier_1(css):
    """Every raw colour value below the tier 1 boundary.

    Returns a list of (line, layer, where, value), empty when the layers
    below tier 1 are clean — or None when the boundary itself is nowhere in
    the stylesheet, which leaves the question open rather than answering it
    in either direction.

    Ceiling: the *first* boundary is the one that counts. A system emitted
    into several tokens files would carry one per file, and this reads the
    primitives of the second and later ones as downstream — strict rather
    than lax, which is the right way round for a gate to be wrong.
    """
    cut = css.find(TIER_1_SENTINEL)
    if cut < 0:
        return None
    masked = blank_comments(css)
    found = []
    for m in RAW_COLOUR.finditer(masked, cut + len(TIER_1_SENTINEL)):
        # A colour function reading a custom property is plumbing, not a raw
        # value: the channels still come from tier 1.
        if "var(" in m.group(0):
            continue
        # A colour is a value, so it lives in a declaration. Without one the
        # match is something else wearing the same characters — an id
        # selector such as `#faded` is spelled entirely in hex digits.
        prop = enclosing_prop(masked, m.start())
        if not prop:
            continue
        banners = [b.group(1) for b in BANNER.finditer(css, 0, m.start())]
        rule = enclosing_rule(masked, m.start())
        found.append((css.count("\n", 0, m.start()) + 1,
                      banners[-1] if banners else "",
                      f"{rule} · {prop}" if rule else prop, m.group(0)))
    return found


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def stylesheet(src: pathlib.Path):
    """The system stylesheet: emitted tokens first, hand-authored parts after.

    Returns (name, css). The order is load-bearing — a custom property has
    to be declared before the rules that consume it, and every gate below
    reads tier 1 as the block standing ahead of everything downstream. The
    parts layers are taken in sorted order so the same src/ always
    concatenates to the same bytes.
    """
    sheets = sorted(src.glob("*.css"))
    if not sheets:
        sys.exit(f"no stylesheet found in {src}")

    tokens = [f for f in sheets if f.name.endswith(".tokens.css")]
    parts = [f for f in sheets if not f.name.endswith(".tokens.css")]
    if not tokens:
        # One stylesheet is a whole system on its own and needs no ordering.
        # Several, with nothing named for the emitted layer, is a coin toss:
        # picking one would silently drop the rest, which is the bug this
        # function exists to remove.
        if len(sheets) == 1:
            return sheets[0].name, sheets[0].read_text()
        sys.exit(f"cannot tell which stylesheet in {src} holds the tokens — "
                 f"name the emitted layer <system>.tokens.css "
                 f"({', '.join(f.name for f in sheets)})")

    css = "\n".join(f"/* ---- {f.name} ---- */\n{f.read_text().rstrip()}\n"
                    for f in tokens + parts)
    # Name the built sheet for the system, not for one of its inputs.
    return tokens[0].name.replace(".tokens.css", ".css"), css


def build(system_dir: pathlib.Path, out_dir: pathlib.Path):
    src = system_dir / "src"
    css_name, css = stylesheet(src)
    out_dir.mkdir(parents=True, exist_ok=True)

    shells = sorted(src.glob("*.shell.html"))
    if not shells:
        sys.exit(f"no *.shell.html consumers found in {src}")

    built = []
    for shell in shells:
        html = shell.read_text()
        if MARKER not in html:
            sys.exit(f"{shell.name} is missing the {MARKER} marker")
        name = shell.name.replace(".shell", "")
        target = out_dir / name
        target.write_text(html.replace(MARKER, css))
        built.append(target)
        print(f"  built  {name:<32} {target.stat().st_size:>8,} bytes")

    (out_dir / css_name).write_text(css)
    print(f"  built  {css_name:<32} {len(css):>8,} bytes"
          f"   sha256:{hashlib.sha256(css.encode()).hexdigest()[:12]}")
    return built, css


# --------------------------------------------------------------------------
# verification gates
# --------------------------------------------------------------------------
def verify(built, css):
    failures = []

    # Gate 1 — single source: every consumer carries an identical token block.
    blocks = []
    for f in built:
        text = f.read_text()
        if MARKER in text:
            failures.append(f"{f.name}: marker was not replaced")
        m = re.search(r"<style>(.*?)</style>", text, re.S)
        blocks.append(m.group(1) if m else "")
    same = len(set(blocks)) == 1 and blocks[0].strip() != ""
    print(f"  single source of truth across {len(built)} consumers: {'pass' if same else 'FAIL'}")
    if not same:
        failures.append("consumers do not share an identical token block")

    # Gate 2 — no raw values downstream of tier 1.
    for f in built:
        text = f.read_text()
        chrome = "".join(re.findall(r"<style>(.*?)</style>", text, re.S)[1:])
        raw = re.findall(r"(?:#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\()", chrome)
        status = "pass" if not raw else f"FAIL ({len(raw)})"
        print(f"  no raw colour values in {f.name}: {status}")
        if raw:
            failures.append(f"{f.name}: {len(raw)} raw colour values outside tier 1")

    # Gate 2b — the same rule, turned on the stylesheet itself. Gate 2 reads
    # every <style> block *after* the first, and gate 1 requires the inlined
    # system CSS to be the first, so the whole stylesheet sits outside gate
    # 2's window: it polices the shell's own chrome and nothing else. The
    # layer likeliest to carry a stray hex — the hand-authored parts file —
    # is exactly the one it cannot see. Tier 1 is the only layer allowed a
    # literal, and emit.py marks where it ends, so everything past that line
    # must reach its colour through a token.
    leaks = raw_colours_below_tier_1(css)
    if leaks is None:
        # A stylesheet emit.py never wrote has no boundary to check against.
        # Passing it would be a lie and failing it would punish a shape the
        # rest of this script accepts, so say what is actually true.
        print("  no raw colour values below tier 1: unverified — "
              "no tier boundary in this stylesheet, check manually")
    else:
        print(f"  no raw colour values below tier 1: "
              f"{'pass' if not leaks else f'FAIL ({len(leaks)})'}")
        for line, layer, where, value in leaks:
            print(f"      line {line:>4}  {layer:<20} {where:<36} {value}")
        if leaks:
            shown = ", ".join(value for *_, value in leaks[:4])
            failures.append(f"{len(leaks)} raw colour values below the tier 1 "
                            f"boundary: {shown}{' …' if len(leaks) > 4 else ''}")

    # Gate 3 — scale adherence (advisory): px values should come from a
    # declared scale or a tier-3 dimension token, not appear ad hoc.
    # Every px value in a declaration value counts, not just the first one
    # after the colon: `padding: 4px 10px` hid its 10px, and a fractional
    # `1.5px` was invisible entirely.
    PX = r"(\d*\.?\d+)px"
    declared = set(re.findall(rf"--[\w-]+:\s*{PX}\s*;", css))
    used = {v for value in re.findall(r":\s*([^;{}]*)", css)
            for v in re.findall(PX, value)} - declared - {"0", "1", "2"}
    print(f"  off-scale px literals (advisory): {len(used)}"
          f"{' — ' + ', '.join(sorted(used, key=float)[:8]) if used else ''}")

    # Gate 4 — contrast, for any semantic pairs resolvable to literal hexes,
    # checked once per theme so a dark-mode override can't silently mix
    # into the light palette (or vice versa) the way a single flat dict did.
    TOKEN_RE = r"--([\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;"
    base_text, theme_blocks = theme_scopes(css)

    def layered_prims(theme_text):
        # dict() keeps the *last* match per key, so theme entries (added
        # second) override base entries for the same token name.
        return dict(re.findall(TOKEN_RE, base_text) + re.findall(TOKEN_RE, theme_text))

    def layered_resolver(theme_text, prims):
        # A layer's own declaration wins outright, alias or literal hex alike.
        # Falling through to the base is only correct when the layer never
        # mentions the token at all — searching the base whenever the *alias*
        # search missed is what let a dark theme's literal hex go unread, so
        # a broken dark palette got scored against the light primitives.
        def own(text, token):
            """(value, declared) for one layer. value is None if unresolvable."""
            if not text or not re.search(rf"--{token}:", text):
                return None, False
            alias = re.search(rf"--{token}:\s*var\(--([\w-]+)\)", text)
            if alias:
                return prims.get(alias.group(1)), True
            literal = re.search(rf"--{token}:\s*(#[0-9a-fA-F]{{3,8}})", text)
            return (literal.group(1) if literal else None), True

        def resolve(token):
            value, declared = own(theme_text, token)
            # `transparent`, `none` and colour functions land here as declared
            # but unresolvable — right for print, where a background genuinely
            # is nothing, and the pair is skipped rather than mis-scored.
            return value if declared else own(base_text, token)[0]
        return resolve

    # Inverse text never sits on the surface — it sits on the solid action
    # fill. Checking it against surface would fail every well-built system,
    # and a gate that always fails is a gate everyone learns to ignore.
    VALUE = r"(?:var\(--[\w-]+\)|#[0-9a-fA-F]{3,8})"
    TEXT_PAT = rf"--(color-text-(?!inverse)[\w-]+):\s*{VALUE}"
    # Backgrounds are discovered by name rather than listed, so canvas,
    # sunken, elevated and any other surface variant a system invents all
    # get checked. Anything that doesn't resolve to a hex is skipped.
    BG_PAT = rf"--(color-(?:canvas|surface|elevated)[\w-]*):\s*{VALUE}"

    def contrast_checks(theme_text, resolve):
        checks = []

        def declared_names(pattern):
            return list(dict.fromkeys(re.findall(pattern, base_text)
                                      + re.findall(pattern, theme_text)))

        backgrounds = [(n, resolve(n)) for n in declared_names(BG_PAT)]
        backgrounds = [(n, bg) for n, bg in backgrounds if bg]
        for name in declared_names(TEXT_PAT):
            fg = resolve(name)
            if not fg:
                continue
            for bg_name, bg in backgrounds:
                checks.append((name, bg_name, fg, bg))
        action = resolve("color-action-solid")
        inverse = resolve("color-text-inverse")
        if action and inverse:
            checks.append(("color-text-inverse", "color-action-solid", inverse, action))
        return checks

    print("  contrast:")
    for theme_name, theme_text in [("default", "")] + theme_blocks:
        prims = layered_prims(theme_text)
        resolve = layered_resolver(theme_text, prims)
        checks = contrast_checks(theme_text, resolve)
        if checks:
            for name, bg_name, fg, bg in checks:
                ratio = contrast(fg, bg)
                target = 3.0 if "tertiary" in name else 4.5
                ok = ratio >= target
                # Disabled text is the one place the 4.5:1 rule is formally
                # exempt (assets/tokens.template.json says so), so asserting
                # it here would fail every correctly built system. The ratio
                # is still measured and printed — exempt, not hidden.
                exempt = name == "color-text-disabled"
                verdict = "exempt" if exempt else ("pass" if ok else "FAIL")
                print(f"      {theme_name:<10} {name:<22} on {bg_name:<20} {ratio:>5.2f}:1"
                      f"  target {target}  {verdict}")
                if not ok and not exempt:
                    failures.append(f"[{theme_name}] {name} on {bg_name}: {ratio:.2f}:1, below {target}")
        else:
            print(f"      {theme_name:<10} no resolvable semantic pairs — check manually")

    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("system_dir")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    system_dir = pathlib.Path(args.system_dir)
    out_dir = pathlib.Path(args.out) if args.out else system_dir / "dist"

    print("build")
    built, css = build(system_dir, out_dir)
    print("\nverify")
    failures = verify(built, css)

    print()
    if failures:
        print(f"{len(failures)} gate failure(s):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("all gates passed")


if __name__ == "__main__":
    main()
