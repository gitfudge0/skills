# Component build only

Implement requested UI components within the existing project. Keep scope to those components and the wiring needed to make their stated behavior usable. Make a visual draft only when requested or when a consequential choice needs review before code. Change project-wide rules only when the user requests them or the component establishes a reusable contract.

Use the owning `fudge:design` guide’s discovery, specialist routing, and verification requirements; read its “Work the decision” section if this reference was reached directly.

1. Specify the component contract for the worker: purpose, anatomy, variants, states, interactions, responsive behavior, accessibility, real copy, and exact editable files. Reuse established primitives and tokens under package-root `shared/execution.md`.
2. Compare against a selected mock or design contract through package-root `references/modules/design-qa/guide.md`; otherwise use the owning guide’s in-context component inspection. Fix observed failures within scope and verify again.
3. If the component changes an existing documented contract, update its authoritative source to match the implemented behavior within this component's scope. Do not invent broader project direction. Report changed files, what the component does, the checks and visual inspection performed, and any material limit.

When nested in `fudge:ship`, follow its selected path: routine work uses the behavior already settled with the user; comprehensive work starts component build after its applicable behavior and coverage approval. Give ship the implementation evidence and let it govern verification, review, and delivery.
