---
name: mindie
description: "Turn a document, article, notes, transcript, book summary, or any body of text into an interactive, animated HTML mindmap that renders in light and dark mode. Use whenever someone wants to visualize, map, diagram, or 'make sense of' information as a mind map, concept map, or node graph — including phrasings like 'mindmap this', 'turn this into a mindmap', 'map out these notes', 'visualize this doc', or 'break this down visually'. Also reach for it when a user hands over dense material and asks to make it easier to understand or explore, even if they don't say the word 'mindmap'."
---

# mindie

mindie turns source material into a single self-contained HTML file: an
interactive mindmap with a central topic, colored branches, expandable nodes, a
reading panel, pan/zoom, spring micro-animations, and automatic light/dark
theming.

**The goal is comprehension of the entire source, with nothing left out.** A
reader explores the finished map *instead of* opening the original, so any idea
missing from the map is lost to them. Completeness is therefore the top
priority: every claim, fact, example, rule, and caveat that carries meaning must
live somewhere in the tree. When completeness and tidiness conflict, completeness
wins. The map is a faithful, navigable summary, not a highlight reel — and
"faithful" here means *complete*. Getting the tree right *is* the job; the
rendering is mechanical.

## Workflow

Three phases: **ingest → curate → render.**

### 1. Ingest

Get the source in front of you. Use pasted/uploaded text directly (read
uploaded files with the right tool first); fetch a URL or connected doc if
that's what they gave you; if they named only a topic with no source, you are
the source — draw on what you know and search if it's current or uncertain. For
long material, skim for structure rather than reading every word.

### 2. Curate — the important part

Build a **tree of nodes** that includes *all* of the source, organized so the
hierarchy itself explains the material. Completeness is non-negotiable; the
craft is fitting everything in while keeping the map readable (the answer is
always *organize and use detail panels*, never *drop content*).

**Read `references/curation.md` before curating** — it lays out the method and
the fidelity rules, and it is where the completeness discipline lives. The
method is a build-then-verify loop:

1. **Segment the source** into atomic units (one idea/fact/example each) and
   list them in a coverage file.
2. **Build the tree** so every unit lands somewhere — as a label, a summary, or
   a point. Group with intermediate nodes when a branch gets crowded; never cut.
3. **Verify coverage** and make it pass before rendering:

   ```bash
   python3 scripts/check_coverage.py --coverage cov.txt --data map.json
   ```

   This fails loudly on any source unit that isn't either mapped to a real node
   or explicitly marked `[OMIT: reason]` (reserved for non-substance chrome like
   nav widgets or author meta-remarks). **Curation is not done until this check
   passes with zero unaccounted units**, and you should be able to defend every
   recorded omission. Don't rely on a mental "I think I covered it all" pass —
   that is exactly how content gets dropped.

Node shape:

```json
{
  "id": "root",
  "label": "Central topic",
  "detail": { "tag": "Core idea", "summary": "1-3 sentences.", "points": ["optional", "..."] },
  "children": [
    { "id": "branch-1", "label": "A theme", "color": "purple",
      "detail": { "tag": "Theme", "summary": "..." },
      "children": [ { "id": "leaf-1a", "label": "A point", "detail": { "tag": "Point", "summary": "..." } } ] }
  ]
}
```

Every `id` is unique. Don't set positions (layout is automatic) and don't color
leaves (they inherit their branch color). You may set a branch `color`
(`purple|pink|orange|teal|blue`); otherwise branches are auto-colored.

### 3. Render

Only after the coverage check passes: write the tree to a JSON file, then inject
it — this is deterministic, so don't hand-edit HTML:

```bash
python3 scripts/build.py \
  --data /path/to/map.json \
  --out /mnt/user-data/outputs/<name>-mindmap.html \
  --title "Human-readable title" \
  --subtitle "optional subtitle" \
  --glyph "✦"
```

`--title` defaults to the root label; `--subtitle` to a node/branch count;
`--glyph` is the brand-mark character (pick something evocative of the subject).
The script validates the tree and fails loudly on bad input — fix the JSON and
re-run. Then present the HTML file with a short message; note the branches and
that clicking expands nodes and the theme toggles. Don't over-describe it.

## What the rendered map does

Opens fully collapsed (root + branches; leaves hidden). Clicking a branch
springs its children out; clicking again collapses them. Clicking any node opens
a reading panel with its tag, summary, and points. Pan by dragging, zoom by
scroll/pinch/dock, Fit button reframes. Light/dark auto-detected with a manual
toggle. Micro-animated throughout, and respects `prefers-reduced-motion`.

## Files and references

- `scripts/check_coverage.py` — verifies every source unit is accounted for in
  the tree. Run it during curation; it must pass before rendering.
- `scripts/build.py` — validates the tree and injects it into the template.
- `assets/template.html` — the renderer. Content-agnostic; only the injected
  `DATA` tree and three metadata tokens change per map.
- `references/curation.md` — **how to build a complete, faithful tree.** Read
  before curating; the completeness discipline lives here.
- `references/renderer-spec.md` — complete spec of the renderer: layout math,
  animation constants, palette, structure. Read this only if you need to
  **recreate or modify `template.html`** (e.g. the asset is missing, or the user
  wants design/behavior changes). For a normal map you never touch it.
- `examples/ikigai.json` — a reference tree showing the target quality and shape.
- `examples/ikigai-coverage.txt` — its coverage file, showing the format and a
  passing check (55 units: 51 mapped, 4 justified omissions).

To re-skin the map (palette, spacing, fonts), edit the CSS custom-property
blocks at the top of `template.html`; see `references/renderer-spec.md` for the
variable map.
