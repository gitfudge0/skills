# Design draft and project rules

Match the output to the decision. A single screen may need one reviewable mock and a short decision note. A cross-screen direction may need updated project rules. Do not produce the full set by default.

## Visual draft

1. Read the project's existing design source and inspect the relevant UI. Identify the person's task, content, actions, and states that could change the design choice. Use the bundled package-root `references/modules/design-for-recognition/guide.md` guide for the visual treatment. Read the bundled package-root `references/roots/ux/guide.md` guide when an unresolved need, content structure, or behavior question could change the draft; route criterion-level accessibility questions to package-root `references/modules/accessible-ui/guide.md`. Mark untested assumptions. Do not run guides as a sequence.
2. Use package-root `references/modules/ui-mock/guide.md` in **artifact-only** mode at an exact output path — resolve its default through package-root `shared/artifacts.md` unless the caller supplies a path. Show the requested screen, flow, or variants in the project's visual language. Include context and consequential states needed to judge the choice; do not add every theoretical state to a narrow draft. Inspect the rendered artifact at relevant sizes and revise unclear labels, grouping, affordances, or feedback.
3. Let the user decide consequential naming, tone, visual direction, and interaction tradeoffs when the brief or project does not settle them. Record a selected direction and its evidence in the draft or response. Keep open choices visible. A mock selection does not authorize production wiring.

When a static frame cannot answer a consequential interaction question, use package-root `references/modules/ui-prototype/guide.md` for a bounded runnable task at an exact unused path — resolve its default through package-root `shared/artifacts.md` unless the caller supplies a path. Inspect its branches and recovery, label it exploratory, and use participant research only when observation is needed. Neither draft route implies a production build or project-wide documentation.

## Durable project rules

Write or revise project documents only when the user requests them or the chosen decision establishes reusable rules across screens or components. First locate the existing authoritative source and naming conventions. Update it in place; do not create competing documents. If none exists, use `DESIGN.md` for reusable visual and interaction rules and `COMPONENTS.md` only for reusable component contracts. Add a separate source only when a distinct concern needs a durable home.

Document chosen behavior, not a menu of variants. Include the rule, where it applies, its supporting evidence or design artifact reference, and any untested assumption. Keep a one-off screen decision with its draft or task handoff unless it truly changes project guidance. Check each new rule against the selected visual and existing patterns.

If the brief and supplied visual direction call for project-wide tokens, theming, and a component library, route to package-root `references/modules/design-system/guide.md`. It owns its named outputs and verification. Treat its documents as the source of truth; do not create parallel rules here.

## Completion

Report the draft path when one was requested, the chosen direction, and any open decision. Report authoritative document paths only when they were changed. Describe the inspection performed and its limit. Do not call a direction settled while a consequential choice remains open.
