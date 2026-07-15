---
name: canvas-mock
description: Use whenever the user asks for a mock, mockup, UI mock, design mock, "mock.html", or to visualize a UI flow/states before building — and when they want to explore or compare design options and pick one ("show me options", "give me a few versions", "let me pick", "what could this look like"). Produces a Figma-like canvas — one self-contained HTML file laying out every state and flow of the feature as labeled frames on a board, styled to match the project's real design system, then opens it. An optional variants mode instead renders several distinct designs of ONE state side-by-side to choose from, then wires the winner into the real components.
---

# Canvas Mocks

The user's preferred output for any mock request: a **single self-contained HTML file** rendered as a **Figma-like canvas** — a light board holding multiple labeled UI "frames" (cards), one per state/flow, so every state and the transitions between them are visible at a glance. This is a design-review artifact, not a working app.

## When to use

Any request to "do a mock", "make a mockup", "mock this up", "show me the flows/states", "mock.html", or to visualize UI before implementing. Also proactively when a UI feature is being brainstormed and the user needs to verify flows.

## The output contract (non-negotiable)

1. **One file**, default name `mock.html` (or as the user specifies), written to the working directory or repo root unless told otherwise.
2. **Fully self-contained**: plain HTML + inline `<style>` + minimal inline vanilla JS (pan/zoom, theme toggle, per-state demos only). **No external URLs** — no CDN, web fonts, or remote images. Inline SVGs for icons. System font stack. It must render the instant it's opened.
3. **Pan/zoom infinite canvas, true-to-size frames**: a fixed full-screen `#viewport` (`overflow: hidden` both axes, no page scrolling) containing an absolutely-positioned `#canvas` with `transform: translate(x,y) scale(z); transform-origin: 0 0`. Wheel zooms toward the cursor (clamp ~0.1–2.5), drag-on-background pans (grab/grabbing cursors), fit-to-content on load, and a small fixed HUD bottom-right with zoom % and −/+/Fit buttons. Because the canvas zooms, frames are **actual size** at whatever dimensions fit the thing being mocked — size each frame to its real platform instead of forcing one canvas size: **mobile** screens use a phone viewport (~390×844, or the project's target device), **desktop/web** screens use a desktop viewport (~1280×800, up to 1440×900 for wide layouts), **tablet** ~834×1112, and **components** (pills, modals, sidebars, cards) stay natural size with no fixed frame. Full-page frames flex-column fill their height and inner panes clip with `overflow: hidden` rather than stretching the frame taller — never shrink content with per-frame `transform: scale()` or fake a narrowed page; pick the right true size instead. The scaffold ships `.mobile`/`.tablet`/`.desktop` presets (combine with `.screen`, e.g. `frame-card screen desktop`); set any other width/height inline.
4. **Light/dark toggle** when the project's design system has dark tokens: a fixed top-right pill button toggling `.dark` on `<html>`; everything restyles through the CSS variables.
5. **Open it when done** (`open mock.html`) — per the user's global "open reports/mocks when done" rule. Don't just leave it on disk.

## Do design discovery FIRST

Before writing, find the project's real design system so the mock reads like the actual product, not a generic wireframe:
- Design tokens (colors, spacing, radius, typography) — e.g. a `colors.css` / theme file / Tailwind config.
- The component library in use (shadcn/Radix, MUI, Chakra, custom) and representative components (button, dialog/modal, badge/chip, select, checkbox).
- Existing copy/labels for the surface being mocked.

Reproduce those tokens as CSS variables at `:root` and hand-write CSS that matches the real components. Match the project — do NOT invent a new visual language. (If there is genuinely no design system, use the neutral defaults in the scaffold.)

## Canvas anatomy

Copy the structure and chrome from `references/canvas-scaffold.html` (swap the `:root` tokens for the project's). All chrome below lives INSIDE `#canvas` so it pans/zooms with the frames; only the theme toggle and zoom HUD are fixed overlays. Every canvas has:

- **Page header**: `<h1>` title ("<Feature> — Flows & States"), a one-line subtitle stating who it's for, and a **legend** explaining the frame-label conventions (e.g. BEFORE = to remove, AFTER = new).
- **Sections** (`A`, `B`, `C`, …): group related states under a heading with a lettered badge. Suggested grouping: in-context (the whole screen/modal so placement is clear) → the component zoomed in → lifecycle (loading/success/error) → edge cases (confirm dialogs, empty/all/overflow, permission-denied).
- **Frame rows**: rows of frames with subtle `→` connectors between states that flow into each other. The canvas can be arbitrarily wide (8000px+ is fine) — rows don't need to wrap for narrow screens anymore; zoom handles that.
- **Frame** = a caption bar ABOVE the card (an ID chip like `A1`/`B3`, a short name, and a one-line description of the state) + the mock **card** itself (white surface, border, soft shadow).
- **Sticky-note callouts** (rotated, distinct from frames) for implementation/schema/decision notes that inform the viewer but aren't part of the UI.

## Coverage rules — render EVERY state

A mock is only useful if it shows the full space. For the feature, enumerate and render frames for:
- **Empty** state and **populated** state.
- **In-context** (the feature inside its real screen at its true platform size — phone, tablet, or desktop) AND **component-only** (the component alone at natural size, for detail).
- **Interactions**: opened dropdowns/popovers, search/filter-applied, hover/active affordances, selected vs unselected.
- **Dirty / unsaved** state where relevant.
- **Lifecycle**: loading/pending, success, error.
- **Edge cases**: confirm-on-close/discard, all-selected/nothing-available, overflow/long content, permission-denied.
- **Before → After** when replacing existing UI: show the old thing tagged for removal next to the new design.

Give each frame a stable ID (`A1`, `A2`, `B1`…) and reference related frames in captions ("see B2"). Err toward more frames — completeness of the state space is the point.

## Variants mode (optional)

Sometimes the direction is still open and the user wants to *compare and pick* between designs rather than review the states of one design ("show me options", "a few versions", "let me pick", "what could this look like", or reacting to a screenshot with "this needs X"). Same canvas, one extra move:

- Render **3-4 genuinely distinct variants** of the *single* target state as a row of frames in their own section (`Variant A`, `Variant B`, …). Vary the *approach* (e.g. two-button vs guided steps vs single hero vs quick-pick list), not just cosmetics — cover minimal → ambitious. Don't ship four near-identical cards.
- Frame each in the project's real tokens and in context (real width, surrounding chrome) so the choice is judged against the actual product. Both themes via the existing toggle — a design that only works in one mode is a bug to catch now.
- Give each variant a **one-line tradeoff note** (sticky-note or `frame-desc`): when to use it and its cost ("smallest change" / "most to build" / "best for first-timers"). The user is picking a tradeoff, not just a look.
- Default 3-4; honor a count the user gives. Scale: "a couple options" → 2-3; "explore this / not sure" → 4 spanning minimal → bold. A single named element (one CTA, one card) → tighter variants of just that element in context, not a whole-screen redesign.

Then, unlike a plain review mock, **close the loop**:
1. Open the file, then **AskUserQuestion** with one option per variant — don't pre-decide.
2. Wire the chosen variant into the real component(s) using the project's actual token classes / CSS modules / Tailwind — not the mock's inline styles. Preserve behavior and accessibility (roles, aria-*, focus states, contrast in both themes) and conditional logic; then typecheck/build. Leave `mock.html` in place unless the user asks to remove it.

If a variant's action targets something that doesn't exist yet (routes, features), don't silently invent it — note it and ask how the action should behave.

## Quality bar

Restrained, product-accurate, real-feeling copy — not lorem ipsum, not a rough wireframe. Consistent iconography (one inline-SVG set), correct spacing rhythm, faithful colors. This goes in front of a PM/reviewer to verify flows before implementation, so clarity of each state and how states connect matters most.

## When delegating to a worker

If building via a subagent, paste the discovered design tokens + component specs, the full enumerated frame list (by ID), and this contract into the brief. Then **verify the file yourself** — confirm it exists, has real byte size, contains no external URLs (`grep -nE "https?://|cdn|<link|src="`; static URL-like text inside readonly input values is fine), has the `#viewport`/`#canvas` pan-zoom structure, and spot-check the frame IDs — before opening it. Never trust the worker's self-report. For iterations, SendMessage the same worker (it keeps context) rather than spawning fresh.

## Reference

- `references/canvas-scaffold.html` — copy-paste boilerplate: the full canvas chrome (page/header/legend/section/frame/connector/sticky-note) plus generic component styles (button, field, input, chip, banner, modal), with neutral placeholder tokens to swap for the project's.
