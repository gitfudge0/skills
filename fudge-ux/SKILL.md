---
name: fudge:ux
description: "Resolve user needs, research, navigation, content, interaction states, accessibility, and experience measurement. Use for usability and task-flow questions; route visual composition and mocks to design."
---

# fudge:ux

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md`, root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

Own the experience question through a usable decision. Read existing behavior, language, research, product rules, and instructions. Separate participant observations, source facts, expert inference, and hypotheses. Select the smallest output that resolves the request; a label decision may need three lines, while a multi-role flow may need a durable contract.

## Route by question

| Question | Module from package root |
|---|---|
| User needs, context, language, task success with people | `references/modules/ux-research/guide.md` |
| Navigation, routes, labels, forms, errors, content hierarchy | `references/modules/content-architecture/guide.md` |
| Roles, transitions, asynchronous work, persistence, recovery | `references/modules/interaction-design/guide.md` |
| Accessibility behavior or criterion-level assessment | `references/modules/accessible-ui/guide.md` |
| Outcome definitions, events, experiments, iteration | `references/modules/experience-measurement/guide.md` |

## Work the task

1. Identify the person, goal, starting context, and decision. Trace the actual task through relevant screens and states. Inspect realistic content and failure/recovery paths.
2. Use only modules that can change this decision. Follow established vocabulary and patterns for routine choices. Present a concrete choice when a consequential behavior, tone, or product decision remains unsettled.
3. Return the requested plan, copy, contract, or evidence-linked findings. With no participants or supplied participant data, a walkthrough remains expert assessment; do not report observed user outcomes.
4. Inspect the proposed route against relevant states. For code or artifacts, follow shared execution guidance and read targeted verification output. State what was checked and what remains unobserved.

Read `references/roots/design/guide.md` for composition, reviewable visuals, design systems, prototypes, or component builds. A prototype may expose an experience problem; resume UX only for the consequential question it reveals. Use public `fudge:ship` for requirements reconciliation or pressure-testing a consequential decision when available; otherwise surface the bounded unresolved decision. These are scoped handoffs, not a sequence to run for every task.

Examples: “Give me three clearer button labels” enters content architecture and returns labels. “What happens if payment times out?” enters interaction design and returns states and recovery. “Show that flow” hands settled behavior to design. Research, mocks, and project documents are not default outputs.
