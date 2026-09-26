---
name: fudge:ux
description: Shape the experience people need to understand and complete a task. Use for user needs, navigation and content structure, flow and state decisions, or usability questions; route visual expression and mocks to fudge:design when needed.
---

# fudge:ux

When installed by the Fudge installer, names such as `fudge:content-architecture` refer to bundled guides. From this root `SKILL.md`, read `references/specialists/fudge-<specialist>/guide.md` for each selected specialist, then follow links relative to that guide. The source specialist folders remain available for separate manual installation. `fudge:design` is bundled at `references/specialists/fudge-design/guide.md` for a consequential visual question. If this skill runs inside `fudge:ship`, follow its selected routine or comprehensive path.

Own the experience question from the person's task to a decision someone can use. Inspect existing product behavior, language, research, project instructions, and authoritative documents before proposing change. Distinguish observed evidence, project rules, and design hypotheses. UX and visual design can inform each other in either order; choose the next question that could change the decision.

## Choose the endpoint

| Request | Output | Read |
|---|---|---|
| Clarify a user need or evaluate task success with people | Research question, plan, or evidence-linked findings | `fudge:ux-research` |
| Improve findability, navigation, language, or content structure | Proposed route, content hierarchy, and task-specific copy | `fudge:content-architecture` |
| Define behavior across actions, roles, async results, or recovery | Interaction and state contract | `fudge:interaction-design` |
| Review an experience without participant evidence | Task walkthrough with precise friction points, proposed corrections, and stated evidence limits | This file; read specialists for the questions found |

Select the smallest output that resolves the request. A narrow label decision may need only a few lines; a flow spanning roles and failures may need a durable contract. Do not create a mock, research study, or project document by default. If a visual draft would make a consequential choice reviewable, read the bundled `fudge:design` guide and use its visual route. A mock or prototype can expose a UX problem; revise the experience decision when it does.

## Work the task

1. Name the person, their goal, the starting context, and the decision that needs to be made. Trace the actual route through relevant screens and states. Separate what is known from participant evidence, product rules, and expert inference.
2. Route each unresolved question to its owner below. Use only the guides that can change this decision. For consequential naming, tone, behavior, or visual direction not settled by the user or project, bring a concrete choice to the user. Follow existing patterns for routine choices and keep material assumptions visible.
3. Produce the selected output in the project's vocabulary. Show how the person reaches the right place, understands the choice and consequence, acts, and recovers when the task does not go as expected. Connect recommendations to evidence or mark them as hypotheses.
4. Inspect the proposed path with realistic content and relevant states. Use participant observation only when the claim requires it. For an artifact or code edit, use `fudge:delegate` under the project's instructions; the orchestrator inspects the result and reads raw targeted verification output before reporting completion. Return the decision, evidence, open questions, and any changed authoritative paths.

| Question or risk | Specialist |
|---|---|
| Needs, context, language, or task success require observation with people | `fudge:ux-research`; without participants or supplied data, findings remain unobserved. |
| Routes, navigation, labels, forms, error language, or content hierarchy are unclear | `fudge:content-architecture`. |
| Roles, multi-step transitions, async results, persistence, or recovery are unclear | `fudge:interaction-design`. |
| Accessibility guidance or criterion-level assessment is needed | `fudge:accessible-ui`; scope the check and evidence, and make no blanket conformance claim. |
| A static frame cannot answer a consequential interaction question | `fudge:ui-prototype` for a bounded runnable task at an exact unused path under `.fudge/<branch>/ui-prototype/`, unless `fudge:ship` supplies a run-local path. |
| A launched experience needs outcome definitions, event checks, or an iteration decision | `fudge:experience-measurement`. |
| Sources conflict or a consequential product choice remains open | `fudge:gap-analysis` for source gaps; `fudge:decision-room` for a decision, never as user evidence. |

## Boundary with visual design

Read `references/specialists/fudge-design/guide.md` when composition, a reviewable mock, reusable visual rules, or component build is the actual decision. Pass the specific settled experience decision and receive a visual proposal or finding; resume UX work only if that result exposes a new consequential experience question. Its bundled `fudge-design-for-recognition` guide owns visual expression of grouping, hierarchy, typography, color, surfaces, affordances, and feedback. This root owns the experience question; `fudge:content-architecture` owns the route and words, and `fudge:interaction-design` owns transitions. `fudge:design-system` records reusable tokens and component contracts; `fudge:design-qa` checks a built UI against its selected design. Neither root is a mandatory prerequisite for the other.
