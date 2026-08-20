# Phase 3 — Component inventory

Input: the project's low-fi wireframe board (`mock.html` or equivalent Balsamiq-style artefact). Output: `COMPONENTS.md` + `COMPONENTS.html` at the project root.

## Mining the wireframe

Read **every frame**, not a sample. For each frame, list the UI elements it contains. Then collapse the list: anything appearing in two or more frames, or appearing once but obviously reusable (a dialog, a snackbar), is a component. Anything that exists only as one screen's layout is not — it belongs in Phase 4.

While reading, record the **frame IDs** each component appears in. Those refs go in the doc and are what makes it auditable later.

### Grouping

Group by job, not alphabetically. A workable set — drop empty groups, add domain ones:

| Group | Typical members |
|---|---|
| Actions | Button, IconButton, control bars |
| Navigation & chrome | AppBar, section labels, page indicators, tab bars |
| Containers & overlays | Scrim, BottomSheet, Dialog, Snackbar, inline notes, toasts |
| Domain group(s) | Named after the product's own noun (e.g. "Library": tiles, grids, chips) |
| Lists & rows | ListItem, settings row, chapter row, folder row |
| Inputs | Slider, Stepper, Toggle, SegmentedControl, swatch picker |
| Progress & data | ProgressBar, scrub bar, stat cards, charts |
| Feature-specific | The one surface the product exists for (e.g. "Reader") |

Ten to thirty components is the normal range. If you have five you missed frames; if you have sixty you promoted layouts to components.

## Hard gate — tokens only

Components consume **only** tokens.

- The token block is copied **verbatim** from `DESIGN.html` into `COMPONENTS.html`.
- **Zero** raw `#hex`, `rgb()`, `rgba()`, `hsl()` anywhere outside that block.
- Verified by grep, with the count reported:

```bash
awk '/^:root \{/{inblock=1} inblock&&/^\}/{inblock=0;next} !inblock' COMPONENTS.html \
  | grep -cE '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\('
```

Expect `0`. Non-zero means a component invented a value — which means a token is missing. Add the token to `DESIGN.md`/`DESIGN.html` first, then use it; do not patch the component.

The same rule covers sizes and durations: if a padding is not a `--space-*`, a corner not a `--radius-*`, a transition not a `--duration-*`, it is a leak.

## `COMPONENTS.md` contract

A short preamble stating: what the product is, that this document is the contract and `COMPONENTS.html` is the live specimen sheet, that `DESIGN.md`/`DESIGN.html` define the tokens and nothing here introduces a value that isn't one. Then the rules that hold everywhere — the dominant shape, what each brand/accent colour *means* and which meanings must not swap, how depth is expressed, and where frame refs point.

Then, per component, a two-column table:

| Row | Content |
|---|---|
| **Purpose** | One line. What commitment or job it serves. |
| **Anatomy** | Structure as an arrow chain: container → leading icon → label. |
| **Variants** | Named variants and sizes. |
| **States** | default, hover, pressed/active, focus-visible, disabled, loading, error — whichever apply. A component missing states gets forked downstream, and forks are permanent. |
| **Tokens** | The token **names** consumed, comma-separated. Not values. |
| **Used in** | Wireframe frame refs (`A1 A3 B4 …`). |
| **Target framework** | The widget/element mapping and how it's themed (e.g. `FilledButton` via `FilledButtonThemeData` with `StadiumBorder()`). |

Data-bearing components additionally ship the four data states: loading, empty, partial, error — and empty must distinguish *nothing yet* from *nothing matched*.

## `COMPONENTS.html` contract

- Self-contained; same theme-toggle mechanism as `DESIGN.html` (`:root` = primary theme, `[data-theme="…"]` override, corner toggle).
- Verbatim token block at the top.
- One section per group, one specimen block per component, rendering **every variant and every state** side by side.
- **Realistic product content.** Real-looking book titles, real settings labels, real chapter names — not "Lorem" and not "Button". Placeholder copy hides the layout bugs that real strings expose.
- The page's own chrome is built from the same tokens.
