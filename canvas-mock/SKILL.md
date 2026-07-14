---
name: canvas-mocks
description: Use whenever the user asks for a mock, mockup, UI mock, design mock, "mock.html", or to visualize a UI flow/states before building. Produces a Figma-like canvas — one self-contained HTML file laying out every state and flow of the feature as labeled frames on a board, styled to match the project's real design system, then opens it.
---

# Canvas Mocks

The user's preferred output for any mock request: a **single self-contained HTML file** rendered as a **Figma-like canvas** — a light board holding multiple labeled UI "frames" (cards), one per state/flow, so every state and the transitions between them are visible at a glance. This is a design-review artifact, not a working app.

## When to use

Any request to "do a mock", "make a mockup", "mock this up", "show me the flows/states", "mock.html", or to visualize UI before implementing. Also proactively when a UI feature is being brainstormed and the user needs to verify flows.

## The output contract (non-negotiable)

1. **One file**, default name `mock.html` (or as the user specifies), written to the working directory or repo root unless told otherwise.
2. **Fully self-contained**: plain HTML + inline `<style>`; minimal inline vanilla JS only if a state genuinely needs a toggle/hover demo. **No external URLs** — no CDN, web fonts, or remote images. Inline SVGs for icons. System font stack. It must render the instant it's opened.
3. **No horizontal page scroll**: `overflow-x: hidden` on body; frames wrap onto new rows on narrow widths.
4. **Open it when done** (`open mock.html`) — per the user's global "open reports/mocks when done" rule. Don't just leave it on disk.

## Do design discovery FIRST

Before writing, find the project's real design system so the mock reads like the actual product, not a generic wireframe:
- Design tokens (colors, spacing, radius, typography) — e.g. a `colors.css` / theme file / Tailwind config.
- The component library in use (shadcn/Radix, MUI, Chakra, custom) and representative components (button, dialog/modal, badge/chip, select, checkbox).
- Existing copy/labels for the surface being mocked.

Reproduce those tokens as CSS variables at `:root` and hand-write CSS that matches the real components. Match the project — do NOT invent a new visual language. (If there is genuinely no design system, use the neutral defaults in the scaffold.)

## Canvas anatomy

Copy the structure and chrome from `references/canvas-scaffold.html` (swap the `:root` tokens for the project's). Every canvas has:

- **Page header**: `<h1>` title ("<Feature> — Flows & States"), a one-line subtitle stating who it's for, and a **legend** explaining the frame-label conventions (e.g. BEFORE = to remove, AFTER = new).
- **Sections** (`A`, `B`, `C`, …): group related states under a heading with a lettered badge. Suggested grouping: in-context (the whole screen/modal so placement is clear) → the component zoomed in → lifecycle (loading/success/error) → edge cases (confirm dialogs, empty/all/overflow, permission-denied).
- **Frame rows**: flex-wrap rows of frames with subtle `→` connectors between states that flow into each other.
- **Frame** = a caption bar ABOVE the card (an ID chip like `A1`/`B3`, a short name, and a one-line description of the state) + the mock **card** itself (white surface, border, soft shadow).
- **Sticky-note callouts** (rotated, distinct from frames) for implementation/schema/decision notes that inform the viewer but aren't part of the UI.

## Coverage rules — render EVERY state

A mock is only useful if it shows the full space. For the feature, enumerate and render frames for:
- **Empty** state and **populated** state.
- **In-context** (the feature inside its real screen/modal) AND **zoomed** (the component alone, larger, for detail).
- **Interactions**: opened dropdowns/popovers, search/filter-applied, hover/active affordances, selected vs unselected.
- **Dirty / unsaved** state where relevant.
- **Lifecycle**: loading/pending, success, error.
- **Edge cases**: confirm-on-close/discard, all-selected/nothing-available, overflow/long content, permission-denied.
- **Before → After** when replacing existing UI: show the old thing tagged for removal next to the new design.

Give each frame a stable ID (`A1`, `A2`, `B1`…) and reference related frames in captions ("see B2"). Err toward more frames — completeness of the state space is the point.

## Quality bar

Restrained, product-accurate, real-feeling copy — not lorem ipsum, not a rough wireframe. Consistent iconography (one inline-SVG set), correct spacing rhythm, faithful colors. This goes in front of a PM/reviewer to verify flows before implementation, so clarity of each state and how states connect matters most.

## When delegating to a worker

If building via a subagent, paste the discovered design tokens + component specs, the full enumerated frame list (by ID), and this contract into the brief. Then **verify the file yourself** — confirm it exists, has real byte size, contains no external URLs (`grep -nE "https?://|cdn|<link|src="`), and spot-check the frame markers — before opening it. Never trust the worker's self-report.

## Reference

- `references/canvas-scaffold.html` — copy-paste boilerplate: the full canvas chrome (page/header/legend/section/frame/connector/sticky-note) plus generic component styles (button, field, input, chip, banner, modal), with neutral placeholder tokens to swap for the project's.
