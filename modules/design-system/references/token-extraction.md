# Token extraction

Use this route when visual or written source material needs to become reusable style rules. Start with the requested property groups. For a full design system, cover the groups used across the agreed product surfaces; do not populate groups with arbitrary defaults merely to make a catalog look complete.

## What the source can establish

| Source | Strong evidence | Treat as estimate or assumption |
|---|---|---|
| Existing theme or CSS | Actual values and names | Intended meanings if undocumented |
| Brand assets with specifications | Specified color and type values | Product UI usage beyond the brand guide |
| Screenshots or moodboard | Color and type character, relative scale, shape and spacing rhythm | Exact sampled values, unseen states, behavior, second theme |
| Written aesthetic brief | Direction and constraints | Every concrete value chosen to realize it |

Record which source supplied a value. Label visual estimates as estimates, including eyed or sampled hex colors. Say when spacing or radius values were regularized. Never present motion, elevation, focus treatment, z-index, opacity, or contrast as measured from a static picture.

## Build the needed vocabulary

Use primitives when multiple semantic values share a palette or scale. Semantic names describe purpose, such as `color-text-primary` or `color-surface-raised`; record their intended use so two colors with different meanings do not become interchangeable. A narrow palette request may need only a few colors. A full system usually needs a coherent set for background, surfaces, text, actions, borders, and feedback, but the product determines the actual set.

For typography, specify the chosen families, sizes, weights, and line heights that will be used. If an unavailable face is replaced, name the substitute and the quality it preserves. Define spacing, radius, shadow, icon, motion, and layer values as those patterns arise. Prefer the project's existing naming and units. Avoid adding a token for a one-off decoration unless it represents a reusable rule.

Add another theme when the brief, existing product, or explicit request calls for it. Make the source-supported theme primary. Mark the derived theme as designed or proposed, not extracted from a screenshot of the primary theme. Where colors will carry text or critical indicators, calculate the relevant contrast ratio and state any usage limit. If motion rules are provided, include reduced-motion behavior.

## Source and presentation

Identify one authoritative token/rule source: an existing theme file, generated CSS, or a design document. A Markdown table can be authoritative for a static guide; a runtime theme file may be authoritative for an app. If a visual HTML specimen is useful, render the requested groups at actual size and make clear whether its values are generated from, linked to, or copied from the authority. Check any copy for drift.

A full design guide can include primitive and semantic colors, type, spacing, radius, and other product-specific groups, with examples and assumptions. A small request can be a compact table plus one specimen. Use only the sections needed to explain and hand off the choices.
