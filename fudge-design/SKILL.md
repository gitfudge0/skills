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
| Show or compare screens | `references/modules/ui-mock/guide.md` in artifact-only mode for a rendered static draft |
| Resolve an interaction, API, algorithm, or performance question empirically | `references/modules/design-experiment/guide.md` for an isolated runnable experiment and observed results |
| Establish tokens, theming, or reusable component rules | `references/modules/design-system/guide.md` for design systems |
| Implement specific UI components | [Component build](references/component-build.md) for the requested implementation and verification |
| Compare built UI with a chosen design | `references/modules/design-qa/guide.md` for fidelity, task completeness, and retests |
| Prepare a visual draft and durable project rules | [Design draft and project rules](references/design-package.md) |

## Work the decision

1. **Follow a real case.** Identify the person or caller, goal, starting context, realistic input, and observable result. Inspect relevant existing behavior, requirements, research, terminology, and visual primitives. Rehearse the key task through completion and include delay, error, interruption, or recovery when it could change the design.
2. **Find the decision.** Ask what the person needs to know or do at the consequential moment and which behavior or visual cue would make it possible. A cue shows what the design communicates. Check the source or running product for the rule behind it. Name the observable differences between viable options. Use established requirements and patterns for routine choices. Bring unsettled choices to the user or authorized owner when the consequences warrant it, and carry on with the parts that are settled.
3. **Use evidence that can change the design.** Match fidelity and effort to the question. Compare labels in their actual context, render hierarchy with realistic content, walk an uncertain transition, observe participants for comprehension, or run a harness for technical behavior. Before an experiment, name the observation that would change the choice. Revisit where the job belongs before adding another control, rule, or service.
4. **Deliver a checkable result.** Give the requested copy, critique, contract, mock, experiment, or component. For consequential behavior, state the trigger, visible outcome, and recovery rule as applicable. Check the selected output through the relevant states and report what you observed. Distinguish requirements, proposals, expert inspection, participant evidence, and simulated or live results. Record durable rules only when requested or when the work establishes a reusable contract.

For component work, inspect the result in context at relevant sizes and input methods. Include keyboard and focus behavior, feedback, and consequential empty or error states as applicable. For code changes, run relevant project checks and read their raw output.

For example, an icon that becomes **Send** once an AI draft has text opens two questions. Can someone switch to voice while keeping that draft, and what happens when they send it during a response? Inspect the empty, editing, and busy states before choosing the control. If queueing is proposed, a runnable draft can check what gets queued, what remains editable, and what survives cancellation. A participant task can establish what the person understood about those outcomes.

## Locate and use guidance

Resolve `references/modules/`, `references/roots/`, and `shared/` from the nearest ancestor containing `.fudge-package.json`, or from the source checkout containing `scripts/skill-manifest.json`. Use `shared/locate.md` for source mappings. Links to this guide’s own references stay relative to this file. Load only guidance that changes or verifies the selected decision.

Use `shared/execution.md` for implementation and verification, `shared/writing.md` for prose, and `shared/artifacts.md` for artifacts. For a requested durable HTML report, use `shared/report-deck/guide.md` with the host's presentation rules. Discuss or draft at the caller’s scope. Broader production integration and delivery use `fudge:ship`; controlled before/after appearance checks for behavior-preserving migrations use `fudge:visual-parity`. When called by shipping, honor the caller’s scope, settled decisions, and destination, and return evidence to the caller.
