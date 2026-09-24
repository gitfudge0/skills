---
name: fudge:design
description: "Route UI design work to the output the decision requires: task-specific guidance, a reviewable visual draft, durable project rules, or a requested component build. Use for design decisions across screens, flows, and components, including standalone mocks and design systems through bundled specialist guides."
---

# fudge:design

When installed by the Fudge installer, specialist names such as `fudge:ui-mock` refer to bundled guides, not separately installed skills. From the installed root skill's `SKILL.md`, read `references/specialists/fudge-<specialist>/guide.md` for each specialist selected below, then follow links relative to that guide. The source specialist folders remain available for separate manual installation. If this skill runs inside `fudge:ship`, follow its selected routine or comprehensive path.

Own the UI decision from the person's task to the requested endpoint. Use the project's existing language, patterns, and source-of-truth documents. Apply `fudge-design-for-recognition` throughout to make the information, choices, actions, and feedback understandable in context. Read `references/specialists/fudge-design-for-recognition/guide.md` from the installed root skill when this one runs.

## Choose the endpoint

| Request | Output | Read |
|---|---|---|
| Advice, critique, or implementation guidance | **Guidance**: concise, task-specific direction with source paths; no artifact by default | This file |
| Design or compare a screen, flow, or visual direction | **Visual draft**: a reviewable artifact showing the requested decision and consequential states | [Design draft and project rules](references/design-package.md) |
| Establish reusable rules across screens or components, or explicitly document the chosen design | **Project rules**: update the authoritative documents after the direction is chosen | [Design draft and project rules](references/design-package.md) |
| Build specific UI components now | **Component build**: implement and verify those components | [Component build](references/component-build.md) |

Choose enough output to let the user review or act on the requested decision. Increase effort for consequential uncertainty, affected states, or reuse across screens, not merely because the request concerns UI. A visual draft does not require project documents; a component request does not require a visual draft. In a comprehensive `fudge:ship` run, return guidance or an artifact-only mock at the supplied run-local path while behavior still needs agreement; component build follows the applicable approval. In a routine ship task, use the settled direction and return the guidance or draft the task needs, then let ship implement and verify it without a separate test-case gate.

## Shared routing

1. Read the user's goal, relevant UI, project instructions, existing design documents, tokens, components, and vocabulary. Identify the person's task and the states that affect it.
2. Route only the questions this task raises to the specialists below. Carry their decisions, evidence, and open questions into the selected mode; do not run every specialist as a fixed sequence. Use `fudge:gap-analysis` only when scattered or conflicting source material obstructs a coherent design. Use `fudge:decision-room` only for a consequential unresolved product choice. Let the user settle consequential naming, tone, visual, or interaction choices that the brief and project do not establish. Follow existing patterns for routine choices and mark remaining assumptions.
3. Use `fudge:delegate` for artifact and code edits. Brief workers with the chosen direction, exact output paths, existing patterns, and bounded ownership. The orchestrator inspects the result and runs relevant verification, reading the raw output before reporting completion. A visual draft needs rendered inspection; a component build also needs relevant project checks.
4. Return the requested output and its evidence: applicable constraints for guidance, the draft path and decisions for visual work, authoritative paths for project rules, or changed files and observed behavior for a component build. Keep open choices visible.

| Question or risk | Specialist |
|---|---|
| User needs are unknown, or a task needs observation with participants | `fudge:ux-research`; without participants or supplied data, mark findings unobserved rather than inventing evidence. |
| Routes, navigation, labels, forms, error language, or content hierarchy are unclear | `fudge:content-architecture`. |
| Roles, multi-step transitions, async results, persistence, or recovery are unclear | `fudge:interaction-design`. |
| Accessibility guidance or criterion-level assessment is needed for the target UI | `fudge:accessible-ui`; scope the check and its evidence, and make no blanket conformance claim. |
| A static frame cannot answer a consequential interaction question | `fudge:ui-prototype` for a bounded runnable task at an exact unused path under its own output location (`.fudge/<branch>/ui-prototype/`) unless `fudge:ship` supplies a run-local path. |
| Built UI needs comparison with its selected design, or a UI fix needs retesting | `fudge:design-qa`. |
| A launched UI needs outcome definitions, event checks, or an evidence-based iteration decision | `fudge:experience-measurement`. |

## Guidance

Read the relevant parts of existing `DESIGN.md` and `COMPONENTS.md` or the project's authoritative equivalents, plus the mock, project instructions, and implementation patterns. Reach for a specialist above only when its specific question affects the answer. Give the user or calling agent a short, task-specific brief: the task, applicable content and interaction rules, tokens and components to reuse, consequential states, accessibility and responsive constraints, and source paths. Mark a missing or conflicting rule as unresolved rather than inventing a new project convention. If the decision needs a visual to be reviewable, switch to the visual draft route. Guidance itself creates no artifact; the caller owns implementation and verification.

## Adjacent skills

- `fudge:ui-mock` owns a self-contained visual artifact with the frames the task needs. Read its bundled guide and use **artifact-only** mode for a visual draft, with the intended output path — its own default is `.fudge/<branch>/ui-mock/` unless `fudge:ship` supplies a run-local path. A static mock is not a working UI.
- `fudge:design-system` owns token and style rules, component contracts, and specimens when the user requests them. Read its bundled guide and follow its output contract, reusing the project's existing source of truth rather than creating competing rules or a fixed set of files.
- For a standalone mock with settled content and behavior, fulfill the request through the bundled `fudge:ui-mock` guide without a broader design package. For a standalone design system, use the bundled `fudge:design-system` guide. When the work also needs to resolve content, interaction, evidence, project rules, or implementation guidance, use the corresponding design route above. A separately installed specialist remains available for explicit direct invocation.
