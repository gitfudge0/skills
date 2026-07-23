#!/usr/bin/env python3
"""
mindie build script.

Injects a curated mindmap tree (JSON) and metadata into the renderer
template, producing a single standalone HTML file.

Usage:
    python build.py --data map.json --out mindmap.html \
        [--title "..."] [--subtitle "..."] [--glyph "*"]

The JSON file must contain the full node tree (the root node object).
Node shape:
    {
      "id": "root",
      "label": "Topic",
      "detail": { "tag": "...", "summary": "...", "points": ["...", "..."] },
      "children": [ { "id": "...", "label": "...", "color": "purple",
                      "detail": {...}, "children": [...] }, ... ]
    }

Rules the caller (Claude) is responsible for, not this script:
  - unique ids, sensible labels, 4-8 top branches, detail on most nodes.
This script only validates structure and injects. It does NOT invent content.
"""
import argparse, json, re, sys, os

TEMPLATE = os.path.join(os.path.dirname(__file__), "..", "assets", "template.html")

def validate(node, seen=None, depth=0, errs=None):
    if seen is None: seen = set()
    if errs is None: errs = []
    if not isinstance(node, dict):
        errs.append("node is not an object"); return errs
    nid = node.get("id")
    if not nid: errs.append(f"node at depth {depth} missing 'id'")
    elif nid in seen: errs.append(f"duplicate id: {nid}")
    else: seen.add(nid)
    if not node.get("label"): errs.append(f"node '{nid}' missing 'label'")
    d = node.get("detail")
    if d is not None and not isinstance(d, dict):
        errs.append(f"node '{nid}' has non-object 'detail'")
    for c in node.get("children", []) or []:
        validate(c, seen, depth+1, errs)
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to mindmap JSON (root node)")
    ap.add_argument("--out", required=True, help="output HTML path")
    ap.add_argument("--title", default=None, help="topbar title (defaults to root label)")
    ap.add_argument("--subtitle", default=None, help="topbar subtitle")
    ap.add_argument("--glyph", default="✦", help="single glyph/emoji for the brand mark")
    args = ap.parse_args()

    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)

    errs = validate(data)
    if errs:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errs: print("  -", e, file=sys.stderr)
        sys.exit(1)

    # derive counts for subtitle default
    n_nodes = 0
    def count(n):
        nonlocal n_nodes
        n_nodes += 1
        for c in n.get("children", []) or []: count(c)
    count(data)
    n_branches = len(data.get("children", []) or [])

    title = args.title or data.get("label", "Mindmap")
    subtitle = args.subtitle or f"Interactive map · {n_branches} branches · {n_nodes} nodes"

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()

    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    # inject — replace tokens. DATA last so title text can't collide.
    out = (tpl
           .replace("__TITLE__", esc_html(title))
           .replace("__SUBTITLE__", esc_html(subtitle))
           .replace("__GLYPH__", esc_html(args.glyph))
           .replace("__DATA__", data_json))

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK  wrote {args.out}  ({n_nodes} nodes, {n_branches} branches)")

def esc_html(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;"))

if __name__ == "__main__":
    main()
