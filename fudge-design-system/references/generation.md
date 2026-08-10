# Generation

File contracts, token architecture, and the checks that run before anything is presented.

## Contents

- [Token architecture](#token-architecture)
- [File contracts](#file-contracts)
- [The anti-default guard](#the-anti-default-guard)
- [Signature element](#signature-element)
- [Code conventions](#code-conventions)
- [Verification](#verification)
- [Adapting to other targets](#adapting-to-other-targets)

---

## Token architecture

Three tiers. The indirection is the entire reason theming and density are configuration rather than rewrites.

**Tier 1 — primitives.** Raw values with no meaning. `--ink-900`, `--jade-500`, `--space-4`. Never referenced by product code; a primitive in a product file should fail lint.

**Tier 2 — semantic.** The theming seam. `--color-text-primary`, `--color-surface`, `--severity-critical-fg`. Dark mode and any alternate brand remap *only* this tier.

**Tier 3 — component.** The density seam. `--control-height-md`, `--table-row-height`, `--panel-pad`. Density modes remap only this tier.

Rules worth stating in the generated docs, because they are the ones teams get wrong:

- **Tier 3 is for dimensions, not colour.** Component-scoped colour tokens multiply endlessly without earning anything. Colour stops at tier 2 unless a component provably needs to diverge.
- **New primitives need review; new semantics need a use case.** Adding `--ink-350` because a mock looked slightly off is how a system ends up with forty greys.
- **Renaming a tier-2 token is a breaking change.** It ships with a codemod and a deprecation window.
- **Nothing downstream is hand-edited.** `tokens.json` is the source; the CSS, the type definitions, and the design tool variables are all emitted.

Make the tiering *visible* in the documentation rather than merely described. A provenance trail — primitive → semantic → component → the rendered control — with live theme and density toggles proves the architecture in about four seconds. Description of tiering convinces nobody; watching one link in the chain change while the others hold convinces immediately.

---

## File contracts

### tokens.json
DTCG-shaped source of truth. Group by tier. Every token carries a `$value`, a `$type`, and a short `$description` saying what it is *for* — the description is what stops the set from drifting into synonyms.

### `<system>.css`
Emitted, in this order: tier 1 block, tier 2 block, theme overrides, print overrides, tier 3 block, density overrides, reset and base, type roles, component classes, minimal layout utilities. Print overrides sit beside theme overrides because both remap tier 2 only, and tier 3 needs the final values before it renders.

Keep utilities deliberately few. A system that ships a hundred utilities has outsourced its decisions to whoever is writing markup.

### docs.html
Sections in this order: principles, token architecture with a live provenance demo, foundations, components with full state matrices, patterns, content, accessibility, governance. Every component gets its contract table. Theme and density toggles live in the header so every section can be checked in every mode.

Documentation chrome must itself be built from the system's tokens. A docs site that uses raw values to describe a token system undermines its own argument, and it is an easy thing to check.

### demo-`<surface>`.html
One real product screen from the archetype's busiest surface — real content, real density, real edge cases. Include at least one empty or error state somewhere on the page.

This file is the proof, and it earns its place by being where you discover what the token set is missing. If the demo needed a value the system does not have, the system was incomplete; add it and regenerate rather than patching the demo.

### DECISIONS.md
Short entries, each with: the decision, what was rejected, why, and what would make you revisit. Include every defaulted assumption from the interrogation, and every open question the user punted on.

This is what makes the system arguable later. "Why is there no brand colour in the interface?" gets asked by every new team, and it should be answered once, in writing.

### build.py
Emits the CSS from tokens where applicable, inlines the stylesheet into each HTML consumer, and reports whether their token blocks match. Shipping the build step is what makes "the demo uses the same system" verifiable instead of asserted.

---

## The anti-default guard

Generated design converges hard. Before locking a direction, check it against these and revise anything that matches without a reason from the brief:

- Cream or warm off-white background (near `#F4F1EA`) with a high-contrast serif display and a terracotta accent near `#D97757`
- Near-black background with a single acid-green or vermilion accent
- Broadsheet layout: hairline rules, zero radius, dense newspaper columns
- Purple-to-blue gradients anywhere
- A hero built from one big number, a small label, supporting stats, and a gradient accent
- Inter, or a geometric sans, chosen by default rather than for a property the brief needs
- 8px radius on everything
- Colour scales generated by mechanical lightness steps rather than tuned per hue

Each is legitimate for *some* brief. None is legitimate as a default, and they show up regardless of subject, which is the tell.

**The test:** work through a plausibly different brief and see whether you arrive somewhere similar. If you would, the direction is a reflex rather than a decision. Revise it and say what changed and why.

The reliable escape is the vernacular axis from `reading-inputs.md`. Systems whose vocabulary comes from the subject's own world do not look like other systems. Systems whose vocabulary comes from other design systems look like all of them.

---

## Signature element

Every system should have one element it is remembered by — a device that encodes something true about the subject and appears nowhere else. Spend boldness here and keep everything around it quiet.

A signature is not decoration. It should carry information:

- A severity spine on the leading edge of table rows, so scanning the left rail alone is enough — and so severity survives colour blindness positionally
- A time gutter running down a log view, making duration legible without reading timestamps
- A confidence band behind numeric values, showing uncertainty inline rather than in a tooltip
- A provenance mark on records, distinguishing what the system inferred from what a human entered

Derive it from the vernacular. Then apply Chanel's rule before shipping: look at the whole thing and remove one accessory. Usually the second-boldest idea is the one to cut, because it is competing with the signature rather than supporting it.

---

## Code conventions

- Namespace component classes with a short prefix so system classes are distinguishable from application classes at a glance.
- Product and demo code references tier 2 and tier 3 only. No raw values.
- Use logical properties (`inset-inline-start`, `padding-block`) so RTL works without a second stylesheet.
- One global `:focus-visible` rule in the reset, built from `semantic.focus.ring-width` and `ring-offset`. Removing an outline requires a written exception.
- One global `prefers-reduced-motion` block. Never per-component.
- Tabular figures on anything numeric that appears in a column.
- Never encode meaning in colour alone — pair it with a label, an icon, or a positional device.
- Set `aria-*` attributes in the component markup, not as an afterthought in the docs.

---

## Verification

Run all of these before presenting. Report the numbers rather than claiming compliance.

**Single source.** Extract the token block from every generated HTML file and assert they are byte-identical. If they are not, the demo is not built from the system.

**No raw values downstream.** Grep every stylesheet block outside tier 1 for hex, rgb, and hsl literals. The count must be zero.

**Contrast.** Compute the ratio for every semantic foreground/background pair, in every theme. Assert 4.5:1 for body text, 3:1 for large text and UI boundaries. List any failures rather than quietly adjusting — a failure often means the palette needs a decision, not a nudge.

**State completeness.** For each interactive component, confirm every state in the contract is implemented, not just described.

**Four states.** Confirm the demo surface handles loading, empty, partial, and error.

**Scale adherence.** Every spacing, radius, font-size, weight, leading, tracking, border-width, easing curve, opacity, icon grid and stroke, breakpoint, and container value in the output appears in the declared scales. Off-scale values mean the scale is wrong or the discipline slipped; either way, resolve it rather than shipping both.

**Print, if in scope.** Apply the `$print` overrides and check computed values, not intent: every semantic background resolves to none or white, every remapped foreground still clears 4.5:1 against it, and nothing below the declared hairline width survives.

**Keyboard pass.** Tab through the demo. Every interactive element reachable, focus visible on every one, order matching visual order, nothing trapped except deliberately in a modal.

A quick script covers the first three and is worth writing once, since it reruns on every regeneration.

---

## Adapting to other targets

The architecture holds; the emission changes.

**React or Vue** — emit tokens as a typed module plus CSS custom properties, and components with the same contracts. Props map to variants and sizes; state remains CSS-driven so it survives without JavaScript.

**Tailwind** — emit the theme config from tier 1 and tier 2, with semantic names as the utility names. The tiering must survive; a Tailwind config full of primitives has thrown away the theming seam.

**Native (iOS / Android)** — the source of truth emits platform formats. The component layer cannot assume the DOM, so contracts are specified in terms of behaviour and accessibility rather than markup.

**Figma-first** — variable names must match token names exactly. Parity is a naming discipline problem, not a tooling problem, and it is the hardest thing in the system to sustain.

**Email** — no custom properties, no flexbox. Emit an inlined subset and be explicit about which components exist there, rather than pretending the whole system does.

**Print** — remap the semantic tier rather than writing a parallel stylesheet; that seam is what makes print cheap. Backgrounds, elevation, hover and focus, and anything below hairline weight do not survive the transition, and the type scale runs in points, not pixels. Nothing about this target is visible on screen, so it gets its own verification pass rather than a glance in the browser.
