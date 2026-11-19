---
name: fudge:ux
description: "Find the questions a feature or interface must answer for users, then turn the answers into buildable, checkable behavior. Use for shaping feature ideas, reviewing screens or flows, and resolving questions about user needs, copy, navigation, interaction states, accessibility, or measurement. Use fudge:design for visual styling and mockups."
---

# fudge:ux

Start with what a person needs to know, decide, or do at a particular moment. For each question that affects their next step, work out what the design should communicate or enable and what behavior makes that answer reliable.

## Discover the questions

Find the person, goal, starting context, and moment of choice. Trace what happens before and after that moment when it changes the decision. Inspect relevant product rules, existing behavior, terminology, and research.

- **Feature idea.** Walk through a realistic use of the feature. Ask what each person needs to understand or do to begin, proceed, recognize the outcome, and recover where applicable. For teammate invitations, the sender needs to know what access they are granting. The recipient needs to know which workspace they can join and what to do if they open the invite under a different account.
- **Existing screen, mock, or component.** Trace meaningful labels, controls, and indicators back to the questions they answer. Look for unanswered questions, cues that compete or repeat, and answers that may become inaccurate in another state. A screenshot shows visible cues. Confirm behavior and transition rules from a product source or a running flow when available.
- **Focused question.** Work at the scale asked for. A request for clearer button labels can start with what the person needs to predict before pressing the button and end with the labels.

Distinguish questions the interface answers for the person from product decisions about how it answers them. Keep questions that can change a user's next action, interpretation, or ability to finish the task. Use established patterns and requirements to settle routine choices. If plausible answers would materially change the build and the evidence leaves the choice open, explain the observable consequences and surface the specific decision. Continue with the parts that can be resolved.

## Turn answers into behavior

For each material question, connect the user-facing answer to the rule behind it. Describe what the person sees or can do, when that changes, and what they see afterward. Specify triggers, state, persistence, permissions, or recovery where they affect the answer. Keep observed behavior, stated requirements, proposed rules, and hypotheses distinct. Treat a walkthrough without participant evidence as expert assessment.

For example, a Grove sidebar session item showing **Review · unread** raises “Is there something new for me to review?” The screenshot shows the cue. The product decision is what counts as seeing the review. Under a proposed rule where viewing the review clears unread, selecting the session highlights the row and leaves **unread** visible. Viewing the review clears **unread** and leaves **Review** visible for a session still in review. Those two cases give implementation and verification concrete expectations. A **3/3** indicator raises a different question about what is complete. Establish what the count measures and whether that answer helps the person choose a session.

## Use relevant guidance

Paths under `references/` and `shared/` resolve from the package root, identified by `.fudge-package.json` or, in source, `scripts/skill-manifest.json`. See `shared/locate.md` for source mappings. Load only the guides that can change or validate an answer.

| What needs an answer | Guide |
|---|---|
| What do people need, understand, or do in context? | `references/modules/ux-research/guide.md` |
| Where do they go and what words or information help them act? | `references/modules/content-architecture/guide.md` |
| What happens across roles, states, delays, or recovery? | `references/modules/interaction-design/guide.md` |
| Can people perceive the answer and act with their input method or assistive technology? | `references/modules/accessible-ui/guide.md` |
| How will we know the experience works or improves? | `references/modules/experience-measurement/guide.md` |

## Deliver and check

Return the requested output at the smallest useful scale. Give copy with its context, findings linked to evidence, or a behavior specification. For a stateful feature, a table can connect each material user question to the interface answer, the behavior rule, and a scenario that would verify it. Identify unresolved decisions separately from settled rules.

Walk through the proposed behavior with realistic content and relevant starting, success, and recovery states. Check whether the person can still answer the question after each consequential transition. Report what you inspected and any material behavior or user outcome still unobserved. Follow `shared/execution.md` for implementation and verification, `shared/writing.md` for prose, and `shared/artifacts.md` for review artifacts. For a requested durable HTML report, see `shared/report-deck/guide.md` and follow the host's presentation rules.

Use `references/roots/design/guide.md` for visual composition, mockups, or design systems. Use `fudge:ship` when requested implementation is in scope or when requirements reconciliation or decision pressure-testing is needed and available. Carry settled behavior, evidence, open decisions, and existing authorization across the handoff.
