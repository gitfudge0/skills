#!/usr/bin/env python3
"""
Build and verify a generated design system.

Inlines the system stylesheet into every HTML consumer, then runs the
verification gates from references/generation.md and reports the numbers.

    python build.py <system-dir> [--out <dir>]

Expects, inside <system-dir>:
    src/<name>.css          the system stylesheet
    src/*.shell.html        HTML consumers containing the marker below
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
# build
# --------------------------------------------------------------------------
def build(system_dir: pathlib.Path, out_dir: pathlib.Path):
    src = system_dir / "src"
    css_files = list(src.glob("*.css"))
    if not css_files:
        sys.exit(f"no stylesheet found in {src}")
    css = css_files[0].read_text()
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

    (out_dir / css_files[0].name).write_text(css)
    print(f"  built  {css_files[0].name:<32} {len(css):>8,} bytes"
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

    # Gate 3 — scale adherence (advisory): px values should come from a
    # declared scale or a tier-3 dimension token, not appear ad hoc.
    declared = set(re.findall(r"--[\w-]+:\s*(\d+)px\s*;", css))
    used = set(re.findall(r":\s*(\d+)px", css)) - declared - {"0", "1", "2"}
    print(f"  off-scale px literals (advisory): {len(used)}"
          f"{' — ' + ', '.join(sorted(used, key=int)[:8]) if used else ''}")

    # Gate 4 — contrast, for any semantic pairs resolvable to literal hexes.
    prims = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", css))

    def resolve(token):
        m = re.search(rf"--{token}:\s*var\(--([\w-]+)\)", css)
        return prims.get(m.group(1)) if m else prims.get(token)

    # Inverse text never sits on the surface — it sits on the solid action
    # fill. Checking it against surface would fail every well-built system,
    # and a gate that always fails is a gate everyone learns to ignore.
    checks = []
    surface = resolve("color-surface")
    if surface:
        for name, _ in re.findall(r"--(color-text-(?!inverse)[\w-]+):\s*var\(--([\w-]+)\)", css):
            if resolve(name):
                checks.append((name, "color-surface", resolve(name), surface))
    action = resolve("color-action-solid")
    inverse = resolve("color-text-inverse")
    if action and inverse:
        checks.append(("color-text-inverse", "color-action-solid", inverse, action))

    if checks:
        print("  contrast:")
        for name, bg_name, fg, bg in checks:
            ratio = contrast(fg, bg)
            target = 3.0 if "tertiary" in name else 4.5
            ok = ratio >= target
            print(f"      {name:<22} on {bg_name:<20} {ratio:>5.2f}:1"
                  f"  target {target}  {'pass' if ok else 'FAIL'}")
            if not ok:
                failures.append(f"{name} on {bg_name}: {ratio:.2f}:1, below {target}")
    else:
        print("  contrast: no resolvable semantic pairs — check manually")

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
