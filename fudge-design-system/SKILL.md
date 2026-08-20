---
name: fudge:design-system
description: Use when the user supplies a moodboard, screenshots, brand assets, a UI mock or a written aesthetic brief and wants design tokens, a component library, theming or dark-mode architecture, a style guide, brand-to-UI translation, or anything they call a "design system" — including "make our product look like this" at more than one-screen scale, and including turning an existing low-fi wireframe board into hi-fi screens.
---

# Design System Forge

Turn an inspiration input plus the project's wireframe into five reference documents that every later coding agent reads: `DESIGN.md`, `DESIGN.html`, `COMPONENTS.md`, `COMPONENTS.html`, `screens.html`, all at the project root.

Each phase ships an **MD + HTML pair**. The MD is the greppable copy — facts, tables, code strings. The HTML is the visual truth — it renders the thing, so it cannot lie about what a token looks like. Both are needed; neither replaces the other.

## Cross-cutting rules

1. **Phases run in order.** Phase N's output is Phase N+1's input.
2. **Single token source.** `DESIGN.html`'s `:root` token block is authored once. `COMPONENTS.html` and `screens.html` copy it **verbatim**. Drift check = diff the blocks.
3. **Both themes, always.** The primary theme (`:root`) matches the inspiration — dark-first if the mock is dark. The other theme is a `[data-theme="…"]` override plus a small JS toggle. Same toggle mechanism in all three HTML files.
4. **Every non-extracted value is a recorded assumption.** A static image carries no opinion about motion, elevation, z-index or opacity. Defaulting is fine; defaulting silently is not. Every default and every regularisation goes in the Assumptions section, along with computed contrast notes for brand-on-background pairs.
5. **Verification is re-run by the orchestrator, not trusted from a worker.** A worker's "done, gates pass" is zero evidence. Grep for hex leaks yourself, count frames yourself, check the token block is present yourself, and report the numbers.
6. **Tokens carry their target-framework equivalent.** Not a separate mapping doc — the equivalent sits alongside the value in the same table.

## Phase 1 — Primitives → `DESIGN.md` + `DESIGN.html`

Colors and typography first, everything else second. Two passes so the palette gets full attention before the long tail.

**Pass A — colors + typography only.**
- Tier-1 primitives: brand ramp(s) + a neutral ramp, exact hexes. Eyeballing from an image is fine — say so in Assumptions.
- Tier-2 semantic tokens with **light and dark values side by side**: bg, bg-subtle, surface, surface-raised, three text tiers (primary/secondary/muted), brand + brand-hover, accent, tertiary, on-brand, inverse-CTA bg/text, border.
- Typography: display + body families (open substitutes named **as substitutes**), a rem scale with line-heights and weights, plus the weight tokens.

**Pass B — extend.** Radius, spacing (4px-grid regularised), gaps (named aliases onto spacing), border widths, shadows (light + dark variants), motion (durations + cubic-bezier easings + reduced-motion rule), z-index layers, icon sizes, opacity, blur.

Rule: extract what the input can actually answer (palette, type, radius, spacing, icon sizes); default the rest and record it.

Deliverable contracts and the extract-vs-default table: `references/token-extraction.md`.

## Phase 2 — Target-framework mapping

Added **into the same two files**, not a third one.

Detect the consuming stack from the project: `pubspec.yaml` → Flutter; `package.json` deps → React/Next/etc.; plain web → no mapping needed. Ambiguous? Ask the user **once**, then proceed.

Every token gains its exact code equivalent in the same row. In `DESIGN.html`, generate the code strings from the **same JS data arrays** that render the swatches, so the two cannot drift. The MD tables are hand-copied and therefore the copy that can go stale — say so in the doc.

Detection logic and the full Flutter profile: `references/framework-mappings.md`.

## Phase 3 — Components → `COMPONENTS.md` + `COMPONENTS.html`

Input: the project's low-fi wireframe board (Balsamiq-style `mock.html` or equivalent). Read **every** frame. Inventory each reusable component, grouped: Actions / Navigation & chrome / Containers & overlays / domain groups / Lists & rows / Inputs / Progress & data / feature-specific.

**Hard gate: components consume only tokens.** The token block is copied verbatim from `DESIGN.html`; zero raw hex (or `rgb()`/`hsl()`) anywhere outside it. Verify by grep and report the count.

Per component in the MD: one-line purpose, anatomy, variants, states, tokens consumed (names), wireframe frame refs, target-framework widget mapping. `COMPONENTS.html` renders live specimens of every variant and state with realistic product content.

Mining procedure, doc contract and the hex gate: `references/component-inventory.md`.

## Phase 4 — Hi-fi conversion → `screens.html`

**Hi-fi always starts from a low-fi design.** Look for one first — a wireframe board (`mock.html` or similar), sketches, or screenshots in the project. If none exists, do not invent screens from the tokens alone: stop and ask the user to supply or approve a low-fi first (offer to produce one as a separate step).

Reproduce the low-fi board **1:1** at high fidelity: same sections, frame IDs, frame names, captions, rows and row labels, connectors with their action labels, reference frames, sticky notes, pan/zoom chrome. Each screen is rendered with the Phase 1 tokens and the Phase 3 component patterns.

Wireframe placeholders (hatching, "image here") become token-built stand-ins: gradient covers from the brand ramp, token-colored shapes. Never a raw hex, never an external asset.

**Gates — the orchestrator runs these, not the worker:**
- Frame count parity with the wireframe (`grep -c 'frame-id'` on both).
- Zero raw hex outside the token block.

Flag every invented stand-in to the user for a visual pass — you guessed at content the wireframe did not specify.

Parity rules, stand-in guidance and board chrome: `references/hifi-conversion.md`.

## Verification commands

Run these yourself after each phase; paste the numbers into your report.

```bash
# hex leaks outside the token block (expect 0 after the :root block ends)
grep -nE '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(' COMPONENTS.html screens.html

# token block identical across files
sed -n '/^:root {/,/^}/p' DESIGN.html > /tmp/a; sed -n '/^:root {/,/^}/p' screens.html > /tmp/b; diff /tmp/a /tmp/b

# frame parity
grep -c 'frame-id' mock.html screens.html
```

A non-zero hex count outside the block, a non-empty diff, or unequal frame counts means the phase is not done. Fix, then re-run.

## Common mistakes

| Mistake | Fix |
|---|---|
| Light theme authored first because it's easier | Primary theme matches the inspiration. A dark mock gets a dark `:root`. |
| Motion/elevation "extracted" from a static image | It isn't there. Default it, record it in Assumptions. |
| A third file for framework mappings | Mappings live beside the token, in `DESIGN.md`/`DESIGN.html`. |
| Hand-writing the token block into `screens.html` | Copy verbatim, then diff. |
| Relaying a worker's "gates pass" | Re-run the greps and report actual numbers. |
| Hi-fi board drops "boring" frames | 1:1 means every frame, including duplicates and reference cards. |
