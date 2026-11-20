---
name: fudge:design
description: "Shape, evaluate, and build designs from concrete tasks. Use for feature behavior, UX research, copy, navigation, accessibility, visual design, design systems, scoped UI components and design QA, or runnable experiments for interaction, API, algorithm, and performance questions."
---

# fudge:design

Use a concrete case to discover what the design needs to do. Give the idea enough form to inspect or try it, follow what happens, and revise the design in light of the evidence. Own the work through the requested endpoint.

## Choose the endpoint

Start at the level of the request. A label request can end with labels. A mock with settled requirements goes straight to the visual draft, and a named experiment goes straight to the runnable question. Move between guides when a finding changes the decision or the requested output.

| Request | Guidance and output |
|---|---|
| Research what people need or understand | `references/modules/ux-research/guide.md` for discovery, task-based evaluation, or synthesis |
| Shape or review behavior across roles, states, and recovery | `references/modules/interaction-design/guide.md` for a checkable behavior contract |
| Review or write copy, navigation, and forms | `references/modules/content-architecture/guide.md` for the path and language in context |
| Assess or improve accessibility | `references/modules/accessible-ui/guide.md` for scoped guidance, audit, or fix and retest |
| Define or assess task success | `references/modules/experience-measurement/guide.md` for measurement and comparison |
| Design or critique hierarchy, layout, typography, and controls | `references/modules/design-for-recognition/guide.md` for visual direction grounded in the task |
| Design motion or microinteractions | `references/modules/design-for-recognition/guide.md` for motion across state changes and rendered review |
| Show or compare screens | `references/modules/ui-mock/guide.md` in artifact-only mode for a rendered static draft |
| Resolve an interaction, API, algorithm, or performance question empirically | `references/modules/design-experiment/guide.md` for an isolated runnable experiment and observed results |
| Establish tokens, theming, or reusable component rules | `references/modules/design-system/guide.md` for design systems |
| Implement specific UI components | [Component build](references/component-build.md) for the requested implementation and verification |
| Compare built UI with a chosen design | `references/modules/design-qa/guide.md` for fidelity, task completeness, and retests |
| Prepare a visual draft and durable project rules | [Design draft and project rules](references/design-package.md) |

## Work the decision

1. **Start with intent and context.** Identify the person or caller, their goal, realistic input, and observable result. Use relevant evidence and constraints such as product rules, platform, language, input methods, and context of use. Follow the task from entry through completion and any interruption, error, or return that changes the design. Identify where naming, grouping, defaults, or contextual help could reduce unnecessary mental effort.
2. **Explore and choose a direction.** Ask what the person needs to know or do at the consequential moment. When the direction is materially open, compare approaches that organize the task or express its purpose in different ways. Name what each would make easier or harder and choose on the basis of the goal, context, and constraints. For visual work, let one idea guide the composition, type, color, and interaction. Use established patterns for routine decisions and bring consequential unsettled choices to the user or authorized owner while continuing settled work.
3. **Make the decision tangible.** Match fidelity to the question. Compare labels in context, render a composition with realistic content, walk a transition, observe participants, or run a technical harness. Before an experiment, name the observation that would change the choice. For each consequential interaction, make the trigger, immediate feedback, outcome, and recovery clear. Where automation matters, make its capabilities, limits, and uncertainty legible. State what it will do and when, and keep review, correction, cancellation, or recovery available where the contract supports them.
4. **Critique the result and refine it.** Check task effectiveness and, where the brief calls for visual work, creative quality on their own evidence. Use `references/modules/design-for-recognition/guide.md` to inspect rendered states and viewports, link findings to their effect on the task or chosen direction, and recheck material fixes. Deliver the requested copy, critique, contract, mock, prototype, or component. Distinguish requirements, proposals, expert inspection, participant evidence, and simulated or live results. Record durable rules only when the request or a reusable contract warrants them.

For user-facing mocks and UI prototypes, inspect the opening and consequential states with realistic content. When motion can clarify a change, design it alongside the state transition and verify how it behaves when interrupted and with reduced motion. Report observed behavior, rendered visual findings, and any gaps in coverage.

For component work, inspect the result in context at relevant sizes and input methods. Include keyboard and focus behavior, feedback, and consequential empty or error states as applicable. For code changes, run relevant project checks and read their raw output.

For example, an AI composer can keep the follow-up as a draft while a reply is pending or let the person queue it. Compare the effort of sending later with the risk of dispatching something unexpectedly. If the person queues a message, explain when it will send and what happens if the reply fails. Walk the pending, failure, and recovery states in the prototype. A participant task can establish whether someone understood those outcomes.

## Locate and use guidance

Resolve `references/modules/`, `references/roots/`, and `shared/` from the nearest ancestor containing `.fudge-package.json`, or from the source checkout containing `scripts/skill-manifest.json`. Use `shared/locate.md` for source mappings. Links to this guide’s own references stay relative to this file. Load only guidance that changes or verifies the selected decision.

Use `shared/execution.md` for implementation and verification, `shared/writing.md` for prose, and `shared/artifacts.md` for artifacts. For a requested durable HTML report, use `shared/report-deck/guide.md` with the host's presentation rules. Discuss or draft at the caller’s scope. Broader production integration and delivery use `fudge:ship`; controlled before/after appearance checks for behavior-preserving migrations use `fudge:visual-parity`. When called by shipping, honor the caller’s scope, settled decisions, and destination, and return evidence to the caller.
