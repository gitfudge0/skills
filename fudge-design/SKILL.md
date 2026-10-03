---
name: fudge:design
description: "Shape visual hierarchy, screens, components, design systems, static mocks, prototypes, or rendered UI checks. Use for interface expression; route consequential user needs and behavior questions to UX."
---

# fudge:design

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md`, root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

Own the visual question through its requested endpoint. Inspect existing UI, project instructions, vocabulary, authoritative design documents, tokens, and components. Use established patterns for routine choices; resolve only consequential unsettled product choices with the user. Read `references/modules/design-for-recognition/guide.md` for task-specific hierarchy, typography, color, surfaces, controls, and feedback.

## Choose the endpoint

| Request | Route and output |
|---|---|
| Advice or critique | Concise direction tied to the task and source evidence; no artifact by default |
| Show or compare screens | `references/modules/ui-mock/guide.md`, artifact-only mode; inspect the rendered static frames |
| Test an interaction that static frames cannot answer | `references/modules/ui-prototype/guide.md`; bounded runnable exploration |
| Tokens, theming, component library, reusable rules | `references/modules/design-system/guide.md`; reuse authoritative sources |
| Implement specific components | [Component build](references/component-build.md); build and verify the requested scope |
| Compare built UI with selected design | `references/modules/design-qa/guide.md`; record observed differences and retests |
| Draft plus durable project rules | [Design draft and project rules](references/design-package.md) |

A mock request with settled content enters the mock module directly. A component request does not require a mock. Create durable documents only when requested or when the chosen scope establishes reusable rules. Keep one-off decisions with the task.

## Work the decision

1. Identify the person's task, content priority, constraints, and consequential states. Mark assumptions and distinguish observed behavior from recommendations.
2. Read `references/roots/ux/guide.md` only when needs, content, flow, or state behavior could change the visual decision. Pass the specific question and retain settled decisions. Read `references/modules/accessible-ui/guide.md` for scoped accessibility guidance or assessment. For conflicting requirements or consequential tradeoffs, hand the bounded discovery or pressure-test question to public `fudge:ship` when available; otherwise surface the concrete unresolved decision.
3. Produce the selected output using shared execution and artifact guidance. Supply exact output paths and bounded ownership to any worker. UX and design can inform each other; neither is a mandatory prerequisite.
4. Inspect rendered artifacts at relevant sizes and states. For code, also run relevant project checks and read raw output. A mock is evidence of appearance, not working behavior; inspection is not participant research or blanket accessibility conformance.
5. Return the decision, output or changed paths, verification evidence, and material open questions. When called by ship, honor its supplied path and already settled behavior; let ship own delivery.
