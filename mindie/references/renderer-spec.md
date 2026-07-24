# Renderer specification

This document specifies the mindie renderer completely enough to **rebuild
`assets/template.html` from scratch** if it is ever missing or needs a rewrite.
The template is a single self-contained HTML file — no external assets, no
network, no build step at runtime. Everything (CSS, JS, markup) lives inline.

Normally you do NOT rebuild it — you inject data via `scripts/build.py`. Use
this spec only to recreate or substantially modify the renderer. When
recreating, prefer copying `assets/template.html` verbatim; this spec is the
fallback and the explanation of *why* each piece exists.

## Injection contract

The template contains exactly four placeholder tokens, replaced by `build.py`:

- `__TITLE__` — topbar title (HTML-escaped). Appears in `<title>` and the `<h1>`.
- `__SUBTITLE__` — topbar subtitle line (HTML-escaped).
- `__GLYPH__` — single character in the brand mark square (HTML-escaped).
- `__DATA__` — the mindmap tree as a JSON object literal, injected as the
  right-hand side of `const DATA = __DATA__;`.

`__DATA__` must be replaced LAST so title/subtitle text cannot accidentally
contain a token. All four appear exactly once except this ordering concern.

## Node data shape (what the renderer consumes)

```
{ id, label, color?, detail?: { tag?, summary?, points?: [] }, children?: [] }
```

- `id` unique string; `label` short string.
- `color` optional on branches (`purple|pink|orange|teal|blue`); the root is
  forced to `"root"`. Leaves omit color and inherit their branch's.
- Positions are NEVER in the data — layout computes them.

## Layout algorithm (balanced left/right tree)

Constants: `H_GAP = 250` (px between depth levels), `V_GAP = 82` (px between
adjacent leaf slots).

1. `countLeaves(node)` — a leaf counts as 1; an internal node's leaf-count is
   the sum of its children's. This "slot count" drives vertical spacing so
   siblings never overlap regardless of subtree size.
2. Split top branches into two lists by index parity: even → right side
   (`dir = +1`), odd → left side (`dir = -1`). This balances the tree.
3. For each side, stack branches vertically centered on y=0: total height is
   `(sum of branch leaf-counts) * V_GAP`; walk a cursor down, placing each
   branch at the center of its own slot span.
4. `placeSubtree(node, dir, depth, cy)` sets `node.x = dir * H_GAP * depth`,
   `node.y = cy`, then recursively places children fanned in the SAME
   horizontal direction, each centered within its leaf-slot span.
5. Root sits at `(0, 0)`.

This is deterministic and pure — same tree always yields the same coordinates.

## Animation model (single rAF spring loop)

One `requestAnimationFrame` loop (`frame()`) drives all motion. Each node holds
mutable animation state, eased toward targets every frame:

- `_scale` → 1 if visible+revealed else 0. Ease factor **0.22**.
- `_op` (opacity) → 1/0 to match. Ease factor **0.25**.
- `_hs` (hover scale) → `_hsTarget` (1.05 on hover, 1 otherwise). Ease **0.2**.
- `_ax`,`_ay` (animated position) → target x/y. Ease **0.24**. When a node is
  hidden it targets its parent's position, so collapsing visibly flies children
  back into their parent and expanding springs them out.
- Rendered transform: `scale(_scale * _hs)`, positioned by `_ax/_ay` minus half
  the measured width/height. Opacity below 0.01 → `display:none`.

The loop self-parks: when nothing is animating it drops to an idle checker
(`idleCheck`) that only resumes on `kick()`. `kick()` is called on any state
change (hover, click, theme, resize).

**Visibility:** a node is visible iff no ancestor is in the `collapsed` set.
Everything starts collapsed except the root — on init, populate `collapsed`
with every internal node whose id ≠ root id.

**Intro:** on load every node starts at scale/opacity 0, position (0,0). A
per-node `_revealAt` timestamp gates the reveal: root at `t0 + 120ms`, each
branch at `t0 + 320 + i*90ms` (staggered). The spring only pulls a node up once
`performance.now() >= _revealAt`. A short `setInterval` calls `kick()` ~16×
to keep the loop awake through the intro.

## Links

Redrawn every frame from animated positions (`_ax/_ay`), as SVG cubic Béziers:
`M x1 y1 C mx y1, mx y2, x2 y2` where `mx` is the horizontal midpoint — giving
the smooth S-curve seen in the mood board. Stroke color = the child's color
variable — now unified, since all five color variables resolve to the same
single indigo ink, so every link reads as one consistent hue. Root edges are thicker (3px, opacity .55); others 2.2px, opacity .42.
Edge opacity is multiplied by the child's `_op` so links fade in/out in sync
with node reveal. Links have `pointer-events:none` and the `<svg>` overflows
visible. Links render as dashed leader-lines — `stroke-dasharray="1 7"` with
`stroke-linecap="round"` — in the child's color, giving the connective tissue a
crisper, more graphical dotted-dash look rather than a solid line.

## Interaction

- **Click a node:** toggles its `collapsed` state (if it has children; the badge
  rotates 180° via the `.expanded` class), marks it `.selected` (colored glow
  ring), and opens the reading panel if it has `detail`.
- **Reading panel:** fixed top-right glass card. Shows `tag` (colored pill),
  `label` as `<h2>`, `summary` as `<p>`, `points` as a bullet list. Header
  elements fade-up staggered; list items slide in staggered from the right
  (animation-delay per index). Closes on the × button or on clicking empty
  canvas (but not after a drag — track a `moved` flag).
- **Pan:** drag empty canvas. **Zoom:** wheel (anchored at cursor), pinch
  (two-finger), or the control dock. Zoom clamped to **[0.3, 2.6]**.
- **Fit:** computes the bounding box of visible nodes with 120px padding, caps
  scale at 1.4, and animates there via `tweenView` (520ms cubic ease-out).
- **View transform** applied as `translate(tx,ty) scale(scale)` on `#world`.

## Micro-animations inventory (all present in the reference build)

Topbar drop-in; control dock + hint rise-in; brand glyph rotate on hover; button
lift/press + click ripple; theme-icon rotate, fit-icon scale on hover; node
spring hover pop composed with reveal scale; ripple on node click; selection
glow ring; slow ambient pulse ring around root; expand/collapse fly-from-parent;
link grow/fade synced to nodes; panel slide+scale in with staggered contents;
close-button 90° spin; animated (tweened) zoom and fit; theme cross-fade of
background/text/link colors. All wrapped by a `prefers-reduced-motion` media
query that collapses every duration to ~0.

## Theming

Two palettes via `html[data-theme="light"|"dark"]`, expressed entirely as CSS
custom properties (see the `:root` and `html[data-theme="dark"]` blocks in the
template). The five `--c-*`/`--c-*-bg` variables are all set to the same
single indigo value per theme (deep indigo ink on warm cream in light; cream
ink on indigo-navy in dark) — this is a strict monochromatic design, not a
multi-hue one. Colors are referenced as `var(--c-purple)` etc. throughout;
nothing is hard-coded outside the variable blocks, so re-skinning means
editing only those two blocks (change all five pairs together to keep the
monochrome intact). On load, theme defaults to **light** (no `prefers-color-scheme` detection); the
Theme button flips `data-theme` and calls `kick()` so link colors repaint.

### Palette (light)

```
--bg #f4f1e9  --surface #fffdf7  --surface-2 #ece7d8  --border rgba(43,53,160,0.22)
--text #23265e  --text-soft #5b5f95
--root-bg #2b35a0  --root-border #232c86  --root-text #f7f3e6
purple/pink/orange/teal/blue all: #2b35a0 / bg #eae9f6 (one indigo ink, one cream tint)
```

### Palette (dark)

```
--bg #1b1c20  --surface #242529  --surface-2 #2d2e34  --border rgba(235,235,240,0.14)
--text #ececf0  --text-soft #a3a5b3
--root-bg #4650c9  --root-border #6670e0  --root-text #fbf7ea
purple/pink/orange/teal/blue all: #a9b2f0 / bg #2a2c3a (periwinkle ink on neutral gray paper)
```

## Node styling essentials

- Rounded pill: `border-radius:16px` (root 20px), `padding:11px 16px`
  (root `16px 24px`), 1.5px border in the node's color.
- **`width: max-content; max-width: 260px;`** — sizes to the label so short
  text stays on one line; only labels wider than 260px wrap. (This fixed the
  earlier unwanted-wrapping bug — keep it.)
- Color classes `.purple/.pink/.orange/.teal/.blue` all now alias to the same
  single indigo ink variable/bg — they remain distinct selectors (for JS
  compatibility) but resolve to identical values. Hierarchy is no longer
  expressed via hue at all; it comes from the `depth-N` classes set alongside
  the color class: `.root` is a solid filled ink block with the pulsing
  `::before` ring; `.depth-1` gets a heavier 2px border and bold (800) weight;
  `depth-2` and deeper get a thin, low-opacity (42%-mixed) border on plain
  `--surface` fill, reading as the lightest/quietest tier. `.selected` adds a
  3px glow (still ink-colored, just via `currentColor`).
- Badge (child count) is a small pill filled with the root ink color
  (`--root-bg`/`--root-text`), with a lighter root-specific fill on `.root`
  badges and darker/lighter overrides on `.expanded`; `.expanded .badge` also
  rotates 180°.

## Layout of the HTML file

`<head>`: meta + one `<style>` block (all CSS). `<body>`: `.topbar` (brand +
Fit/Theme buttons), `#stage > #world > svg#links`, `.panel` (reading card),
`.controls` (zoom dock), `.hint`, then one `<script>` block holding, in order:
DATA + color assignment → layout → node render → collapse/visibility → spring
loop → links → view transform/pan/zoom → interaction/panel → theme → intro →
init. Sections are commented; keep the ordering since later code references
earlier definitions.

## Escaping

All user/content strings rendered into the DOM go through an `esc()` helper
(`& < > "`), and `build.py` independently escapes the three metadata tokens.
Never inject raw source text into markup without escaping.
