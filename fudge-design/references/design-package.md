# Design package

Produce a reviewable UI draft, then capture the **chosen** design as project guidance. Scale the package to the requested surface. The design documents describe the project, not this skill's process.

## Route and outputs

1. Locate existing project design documents and naming conventions. Decide which files are authoritative before creating new ones. Preserve one source of truth for each rule; update an existing document in place rather than silently adding a duplicate.
2. Map the user's task, content hierarchy, actions, feedback, and relevant states with `fudge-design-for-recognition`. When needed, use `fudge:ux-research` for user evidence, `fudge:content-architecture` for routes and language, and `fudge:interaction-design` for the transition contract. Mark untested assumptions as such. Use `fudge:accessible-ui` for design guidance where the target or risk calls for it. Use `fudge:ui-mock` in **artifact-only** mode to render the flow or variants at the real platform size, in the project's visual language. Give it a precise output path. Inspect the opened mock and revise unclear labels, grouping, affordances, and missing states.
3. Settle consequential variants or choices with the user before recording a final direction. When a static frame cannot answer a consequential interaction question, use `fudge:ui-prototype` for a bounded runnable task at an exact unused output path in the project's design artifact area. Inspect its task, branches, recovery, and relevant viewport states; keep it labeled exploratory. Use `fudge:ux-research` if participant observation is needed. Record selected decisions with their evidence and validation status in project documents; keep untested assumptions visible. This mode has no full production build or test gate unless separately selected.
4. Translate the settled design into the project's existing source-of-truth documents. If none exist, use `DESIGN.md` for visual and interaction rules and `COMPONENTS.md` for reusable component contracts. Add another document only when a distinct project concern needs its own durable home. Keep references to the mock's frame IDs where useful; write the chosen behavior, not a menu of unresolved variants.

## Design-system branch

When the brief and supplied moodboard, screenshots, assets, or aesthetic direction call for project-wide tokens, theming, and a component library, route that work to `fudge:design-system`. It owns its five named outputs and verification. Coordinate its low-fi input and user decisions, then treat its resulting documents as the project's design source. Do not produce parallel `DESIGN.md` or `COMPONENTS.md` files with competing rules.

## Document content

- `DESIGN.md`: audience and core tasks; chosen information hierarchy and navigation; visual rules and token references; responsive and accessibility decisions; interaction and feedback rules; evidence for consequential decisions and unresolved assumptions.
- `COMPONENTS.md`: inventory of components the draft actually needs; each component's purpose, anatomy, variants, states, behavior, tokens or patterns consumed, and where it appears in the mock. Keep it specific enough for implementation without reciting generic component advice.
- A separate source document only for a genuinely distinct concern, such as a complex content model or multi-step flow whose contract would obscure the two primary documents. Link it from the primary source.

## Completion

Inspect the rendered draft at relevant sizes, trace the user's key task and consequential states, and verify that every recorded rule agrees with the selected mock and existing project patterns. Report the visual artifact and authoritative document paths, the chosen direction, and any remaining open decision. If a decision remains open, keep it explicit and do not describe the package as settled.
