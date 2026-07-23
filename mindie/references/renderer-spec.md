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
variable. Root edges are thicker (3px, opacity .55); others 2.2px, opacity .42.
Edge opacity is multiplied by the child's `_op` so links fade in/out in sync
with node reveal. Links have `pointer-events:none` and the `<svg>` overflows
visible.

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
template). Colors are referenced as `var(--c-purple)` etc. throughout; nothing
is hard-coded outside the variable blocks, so re-skinning means editing only
those two blocks. On load, theme is chosen from `prefers-color-scheme`; the
Theme button flips `data-theme` and calls `kick()` so link colors repaint.

### Palette (light)

```
--bg #f5f6fb  --surface #ffffff  --surface-2 #f0f1f7  --border #e3e5ef
--text #2a2d3a  --text-soft #6b7080
--root-bg #eef0ff  --root-border #c3c8ff  --root-text #4a3fb8
purple #7c6cf0 / bg #efedff    pink #f06ca8 / bg #ffeef6
orange #f2953f / bg #fff2e2    teal #2fb99a / bg #e4f7f2
blue   #4a9de8 / bg #e7f2fd
```

### Palette (dark)

```
--bg #14151c  --surface #1e2029  --surface-2 #262935  --border #333748
--text #e7e9f2  --text-soft #9096a8
--root-bg #2b2960  --root-border #5a55c0  --root-text #cfc9ff
purple #9a8cff / bg #2c2a4d    pink #ff8bbd / bg #45283a
orange #ffab5e / bg #43331f    teal #4fd6b6 / bg #1e3d38
blue   #6db6ff / bg #1f3448
```

## Node styling essentials

- Rounded pill: `border-radius:16px` (root 20px), `padding:11px 16px`
  (root `16px 24px`), 1.5px border in the node's color.
- **`width: max-content; max-width: 260px;`** — sizes to the label so short
  text stays on one line; only labels wider than 260px wrap. (This fixed the
  earlier unwanted-wrapping bug — keep it.)
- Color classes `.purple/.pink/.orange/.teal/.blue` set text = color var,
  background = color-bg var, border = 45%-mixed color. `.root` uses the root
  vars and has the pulsing `::before` ring. `.selected` adds a 3px color glow.
- Badge (child count) is a small pill; `.expanded .badge` rotates 180°.

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
