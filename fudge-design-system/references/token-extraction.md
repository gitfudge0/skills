# Phase 1 — Token extraction

Two passes over the inspiration input. Pass A buys the identity; Pass B buys the long tail. Doing them together produces a palette that got 20% of the attention.

## Inputs this handles

| Input | What you can pull |
|---|---|
| Moodboard / screenshot / UI mock image | Palette (eyeballed hexes), type character, radius character, rough spacing rhythm, icon sizes, which theme is primary |
| Brand assets (logo, deck) | Exact brand hexes, exact faces |
| Written brief ("warm, calm, dark, rounded") | Direction only — everything becomes a recorded assumption |
| Existing product | Audit the CSS/theme file; extract real values |

If the input is a dark mock, **dark is the primary theme**. `:root` carries dark; light is the `[data-theme="light"]` override. Inverting that reads as not having looked at the input.

---

## Pass A — colors and typography

### Tier 1 — primitives

Name ramps by hue, number by lightness (`raspberry-300/500/600`, `neutral-0/50/100/300/500/700/800/900/950`). Give exact hexes. A brand ramp needs at least three steps (base, darker press/hover, lighter dark-mode hover). The neutral ramp needs enough steps to build both themes without inventing values later — typically 8–10.

Eyeballing hexes off an image is acceptable and normal. Record it: *hexes are eyeballed from the inspiration, not sampled from a source file — expect small drift.*

### Tier 2 — semantic tokens

One table, **light and dark columns side by side**. Minimum set:

| Group | Tokens |
|---|---|
| Background | `color-bg`, `color-bg-subtle` |
| Surface | `color-surface`, `color-surface-raised` |
| Text | `color-text-primary`, `color-text-secondary`, `color-text-muted` |
| Brand | `color-brand`, `color-brand-hover` |
| Support | `color-accent`, `color-tertiary`, `color-on-brand` |
| Inverse CTA | `color-cta-inverse-bg`, `color-cta-inverse-text` |
| Line | `color-border` |

`color-brand-hover` usually differs between themes: darker in light, lighter in dark. The inverse-CTA pair is the high-contrast slab button that flips against the page — spell out what it is for.

Give each semantic token a **meaning**, and say which meanings must not swap (e.g. brand = "now / in progress", accent = "done / trend").

### Typography

- Families: `font-display` and `font-body`, each with a full CSS stack. If the mock's faces are commercial, pick open substitutes and **name them as substitutes**, saying what pairing you matched (e.g. geometric-rounded + neutral-grotesque).
- Scale in `rem` with a line-height and default weight per step. A workable ladder: `display-xl`, `display`, `heading`, `title`, `body`, `body-sm`, `caption`.
- Weight tokens: `weight-regular/medium/semibold/bold`.
- State the rem base (1rem = 16px) — Phase 2 depends on it.

---

## Pass B — the rest

| Group | Tokens | Source |
|---|---|---|
| Radius | `radius-none/sm/md/lg/xl/full` | Extracted (measure corners in the mock) |
| Spacing | `space-1…space-16` on a 4px grid | Extracted rhythm, regularised |
| Gaps | `gap-xs/sm/md/lg` as aliases onto spacing | Derived, named for the layout job |
| Border widths | `border-thin` (1px), `border-medium` (2px) | Extracted |
| Shadows | `shadow-sm/md/lg`, **separate light and dark values** | Partly default |
| Motion | `duration-fast/base/slow`; `ease-standard/decelerate/accelerate` as cubic-beziers | Default |
| Z-index | `z-base/raised/sticky/overlay/modal/toast` | Default |
| Icon sizes | `icon-sm/md/lg/xl` | Extracted |
| Opacity | `opacity-disabled/muted/scrim/hover/pressed` | Default |
| Blur | `blur-sm/md/lg` | Default |

Note the shadow subtlety: if the mock separates layers by surface colour rather than by shadow, dark-theme shadows should be near-invisible **by design** — write that down so nobody later "fixes" it.

Motion always ships the reduced-motion rule: under `prefers-reduced-motion: reduce`, collapse durations to `0ms` **and skip transform-based transitions**, not merely shorten them.

---

## Extract vs default

| Can be extracted from a static image | Cannot — default it |
|---|---|
| Palette, both themes' direction | Motion durations and easings |
| Type character, relative scale | Elevation/shadow depth |
| Radius character | Z-index layering |
| Spacing rhythm (to be regularised) | Opacity/state-layer values |
| Icon sizes | Blur radii |
| Which theme is primary | Focus-ring treatment |

## Assumptions section — mandatory

`DESIGN.md` ends with an Assumptions list. Every one of these gets a line when it applies:

- rem→px conversion basis, and any logical-pixel mapping claim.
- Which token groups are defaults rather than extractions.
- Radius/spacing regularisation onto the grid ("tidy rather than faithful").
- Eyeballed hexes.
- Substitute typefaces and what they substitute for.
- Which theme got the scrutiny and which was derived by inversion.
- **Computed contrast** for brand-on-bg and any borderline pair, with the ratio and the resulting usage restriction ("~4.0:1 — large text and fills only, not body copy"). Compute it; do not claim compliance you did not calculate.

---

## `DESIGN.md` contract

Tables, in this order: Primitives → Semantic (light/dark) → Typography (families, scale, weights) → Radius → Spacing → Gaps → Border widths → Shadows → Motion → Z-index → Icon sizes → Opacity → Blur → Assumptions. Every table carries the target-framework column from Phase 2.

## `DESIGN.html` contract

One self-contained page. A Google Fonts `<link>` is allowed; nothing else external.

- All tokens as CSS custom properties. `:root` = primary theme; `[data-theme="…"]` = the other; a small JS toggle in the corner.
- The page styles **itself** with its own tokens — background, text, cards, spacing. A token page that doesn't eat its own cooking hides the errors.
- A section per token group with a **live specimen**: colour swatches with hex + code string, the type scale rendered at real size, radius squares, spacing bars, shadow cards, a hover-driven motion demo per duration/easing, a stacked z-index diagram, opacity and blur demos.
- Specimens render from JS data arrays. The same arrays produce the framework code strings shown beneath each swatch, so value and code cannot diverge.
