---
name: fudge:design
description: Orchestrate a UI design draft and its project design documents, give an implementation agent design guidance, or build requested UI components. Use for a cohesive design pass across screens, flows, and component rules; use fudge:ui-mock for a standalone mock and fudge:design-system for a standalone visual system.
---

# fudge:design

Own the UI decision from the person's task to the requested endpoint. Use the project's existing language, patterns, and source-of-truth documents. Apply `fudge-design-for-recognition` throughout to make the information, choices, actions, and feedback understandable in context. Read that skill when this one runs.

## Choose one mode

| Request | Mode | Read |
|---|---|---|
| Design a screen, flow, or UI direction without a request to implement the product | **Design package** (default): visual draft, then settled project design documents | [Design package](references/design-package.md) |
| An implementation agent needs applicable design rules for its assigned work | **Guidance only**: return constraints and source paths; create no artifacts | This file |
| Build specific UI components now | **Component build only**: implement and verify those components | [Component build](references/component-build.md) |

Choose from the requested endpoint, not the mere presence of a UI task. A component request does not imply the whole design package. If called from `fudge:ship`, keep its approvals, test plan, review, and delivery gates with ship; this skill supplies design judgment or a bounded component task inside that run.

## Shared routing

1. Read the user's goal, relevant UI, project instructions, existing design documents, tokens, components, and vocabulary. Identify the person's task and the states that affect it.
2. Route only the questions this task raises to the specialists below. Carry their decisions, evidence, and open questions into the selected mode; do not run every specialist as a fixed sequence. Use `fudge:gap-analysis` only when scattered or conflicting source material obstructs a coherent design. Use `fudge:decision-room` only for a consequential unresolved product choice. The user owns naming, tone, and visual or interaction direction when those choices are not established by the brief or project.
3. Use `fudge:delegate` for artifact and code edits. Brief workers with the chosen direction, exact output paths, existing patterns, and bounded ownership. The orchestrator independently inspects their output, runs the relevant verification gates, and reads the raw results before reporting completion.
4. Return the requested endpoint with evidence: artifact paths and the settled decisions for a design package; cited project constraints for guidance; changed files and observed behavior for a component build.

| Question or risk | Specialist |
|---|---|
| User needs are unknown, or a task needs observation with participants | `fudge:ux-research`; without participants or supplied data, mark findings unobserved rather than inventing evidence. |
| Routes, navigation, labels, forms, error language, or content hierarchy are unclear | `fudge:content-architecture`. |
| Roles, multi-step transitions, async results, persistence, or recovery are unclear | `fudge:interaction-design`. |
| Accessibility guidance or criterion-level assessment is needed for the target UI | `fudge:accessible-ui`; scope the check and its evidence, and make no blanket conformance claim. |
| A static frame cannot answer a consequential interaction question | `fudge:ui-prototype` for a bounded runnable task at an exact unused path in the design artifact area. |
| Built UI needs comparison with its selected design, or a UI fix needs retesting | `fudge:design-qa`. |
| A launched UI needs outcome definitions, event checks, or an evidence-based iteration decision | `fudge:experience-measurement`. |

## Guidance only

Read the relevant parts of existing `DESIGN.md` and `COMPONENTS.md` or the project's authoritative equivalents, plus the mock, project instructions, and implementation patterns. Reach for a specialist above only when its specific question blocks useful guidance. Give the calling agent a short, task-specific brief: user task, applicable content, layout and interaction rules, exact tokens and components to reuse, required states, accessibility and responsive constraints, and source paths. Mark a missing or conflicting rule as unresolved rather than inventing a new project convention. Create no artifacts; the caller owns implementation and verification.

## Adjacent skills

- `fudge:ui-mock` owns a static visual board of flows, states, or variants. Call it in **artifact-only** mode from a design package, with the intended output path. A static mock is not a working UI.
- `fudge:design-system` owns the full `DESIGN.md`, `DESIGN.html`, `COMPONENTS.md`, `COMPONENTS.html`, and `screens.html` contract when the user supplies visual inspiration or asks for a system at that scale. Read and follow its contract rather than creating a second set of design rules.
- For a standalone mock or standalone design system request, use the owning skill directly. `fudge:design` earns its place when the work must connect the visual draft to project guidance, or when its guidance or component-build mode is requested.
