---
name: fudge:ux-research
description: Plan, conduct, or synthesize user research for a UI decision. Use for discovering user needs or observing people attempt tasks in a mock, prototype, or live interface; distinguish participant evidence from assumptions and expert inspection.
---

# UX research

Learn what people need or where they struggle in the actual task, then give design work a traceable basis. Scale the study to the decision. Do not turn a small question into a fixed research ceremony.

## Choose the mode

- **Discovery:** Learn about goals, context, current workarounds, language, constraints, and differences among the people who may use the product. Frame open questions before proposing interface solutions.
- **Task-based evaluation:** Observe people attempt realistic tasks on a mock, prototype, or live UI. Assess whether they can find, understand, decide, act, and recover. The fidelity of the test surface limits what can be concluded: a static mock cannot establish interaction success.
- **Existing research synthesis:** When the user supplies recordings, notes, survey responses, support evidence, or prior findings, synthesize those sources with provenance. State what the supplied evidence cannot answer and propose further research only where it would change a decision.

## Prepare the work

1. Name the design decision and the research question it needs answered. Identify what is already known, what is assumed, and what outcome would change the design.
2. Choose participant criteria from the people affected by the decision. Include relevant differences in roles, experience, abilities, devices, and context; recruit through an authorized channel. Do not treat a teammate or an agent as a representative participant by default. No fixed participant count is required.
3. For evaluation, write neutral tasks that state a plausible goal without naming the control or revealing the route. Include the starting context and a realistic success condition. For discovery, use open prompts about recent concrete experiences before asking for opinions about proposed features.
4. Obtain consent appropriate to the method and data collected. Tell participants what is recorded and how it will be used. Avoid unnecessary personal or sensitive data; follow the project's privacy and retention rules. Use test accounts, sample data, or a safe environment when a task could change permissions, money, records, or other consequential state.

## Observe and interpret

- Capture the task outcome, the route taken, hesitations, errors, recovery, and the participant's own explanation. Separate what happened from the researcher's interpretation. Note relevant context and limitations without exposing unnecessary identifying details.
- Ask non-leading follow-ups to learn why a choice made sense to the participant. Avoid coaching during a task unless the method explicitly calls for it; record any intervention because it changes the outcome.
- Link each finding to its supporting observation or supplied source. Describe the affected task, impact, and a specific design implication. Use severity to express consequence and frequency within the observed material; express confidence from the quality and breadth of evidence. Do not turn a small or unrepresentative sample into a population success rate.
- Keep contradictory observations visible. Distinguish needs shared across participants from differences by role or context. Mark hypotheses and unanswered questions as such.

Never invent participants, quotes, task outcomes, or success rates. An agent walkthrough or `fudge:design-qa` inspection can suggest what to test, but it is not participant evidence. If no participants or usable research data are available, deliver the research question, participant criteria, task or interview guide, capture plan, and decision rule; mark findings **unobserved**. Do not fill the gap with plausible findings.

## Feed the design

Give the design owner a short account of what was observed, the evidence and limits, recommended changes tied to findings, and what remains uncertain. When project `DESIGN.md`, `COMPONENTS.md`, or equivalent source-of-truth documents are in scope, update the affected decisions and cite the research evidence; do not silently turn a tentative result into a permanent rule. Re-test material changes when the unresolved risk warrants it.

Use `fudge:gap-analysis` for gaps across project documents and `fudge:decision-room` for simulated perspectives on a decision. Neither supplies observations of real users. Use `fudge:design-qa` for expert comparison of a built UI with its design; use this skill when the question requires evidence from people attempting the task.
