---
name: fudge:ui-mock
description: Create a static, self-contained HTML mock when the user asks to see a UI screen, flow, state, or design options before building. Use for visual review; use fudge:ui-prototype for a runnable interaction and an implementation workflow for product changes.
---

# UI mocks

Make a reviewable visual answer to the user's design question. The output is one self-contained HTML file. It may show a single frame, a few consequential states, or alternatives side by side. A mock request authorizes edits to the mock artifact. Choosing a variant records a design decision; product changes require an explicit build request or an implementation caller that already has that scope.

## Scope the artifact

1. Identify the screen, control, flow, or decision the user needs to judge. Read the relevant product UI, copy, and design tokens when they exist. Match the project's visual language. If no system exists, use a restrained neutral style.
2. Choose the smallest set of frames that answers that question. A single frame is enough for a focused visual direction. Add context when placement changes the judgment. Add states when they change layout, available actions, comprehension, or risk, such as empty versus populated, pending versus error, or a destructive confirmation. Show before and after when the old design is needed to assess a replacement. Do not turn a narrow mock into an inventory of every possible state.
3. If the user asks to compare options, make distinct approaches to the same target state. Use the requested count or the smallest useful set, usually two to four. Keep each in enough context to judge it and give each a short, concrete tradeoff. Record a selection if the user makes one. End the mock task after sharing the artifact and obtaining any requested choice; a selection alone does not start implementation.

## Output and review

- Write one HTML file with inline CSS and only the small amount of inline JavaScript needed to inspect the static design, such as pan, zoom, or a theme toggle. Include assets inline or use CSS; the mock must render without network access or a build step. It does not implement product behavior. For behavior that must be tried, use `fudge:ui-prototype`.
- Use the user's exact output path when provided. A caller such as `fudge:design` or `fudge:ship` may supply one; create its parent directory if needed. Otherwise use `mock.html` in the working directory or repo root. Keep artifact-only callers' writes inside that file and its required parent directory.
- Size frames to the real target viewport or component where scale affects the decision. Use a simple document for one or a few frames. Use a pan and zoom board when many or large frames need spatial comparison. Labels, connectors, callouts, and sections should clarify an actual relationship; omit chrome that adds no information. `references/canvas-scaffold.html` is an optional starting point for a board, not a required structure.
- Show each relevant project theme when the choice depends on it or the user requests it. A theme toggle is useful when both themes need review; do not add one solely because the scaffold contains it.
- Check that the file exists, renders locally, and shows the intended frames at readable scale. Inspect the result and fix unclear copy, misleading context, or missing consequential states. Open the resolved output path for the user when done, then give that path and any decision still needed. If a caller owns the later implementation handoff, return the path and selection or open decision to it.

## Boundaries

The mock is a visual review artifact. Keep production components, routes, and data untouched during this skill, including after a variant is chosen. Do not run product build or test commands for the mock. If the same request explicitly includes implementation, pass the selected direction and relevant design decisions to the implementation workflow under that request's scope.
