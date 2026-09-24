---
name: fudge:accessible-ui
description: Design, build, or audit a UI for accessibility with criterion-level evidence. Use for accessibility reviews, keyboard or screen-reader behavior, inclusive component guidance, and remediation; use fudge:design-qa for general design fidelity.
---

# Accessible UI

Make the requested task usable across the input, perception, and comprehension needs relevant to its users. Determine the platform, product requirements, target content, and requested endpoint before choosing an assessment standard. Inspect existing components and project conventions. For web work, use the current [WCAG standard](https://www.w3.org/TR/WCAG22/) and the relevant [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/patterns/) for a custom widget; prefer native semantics and behavior when they meet the task. For web work without a specified target level, WCAG 2.2 AA can be a stated **assessment baseline**, not an inferred legal obligation. For native or other platforms, identify the applicable platform guidance and project requirement instead of assuming a web conformance claim.

## Choose the endpoint

- **Design guidance:** specify accessible structure, operation, feedback, and risks for the requested flow or component. Show how the task works with keyboard or other relevant input, focus, labels, announcements, and error recovery. A static mock reveals design risks but cannot prove runtime behavior.
- **Audit:** define the exact pages, states, components, tasks, environments, and target criteria. Select relevant manual checks, assistive technology and browser or device combinations for that scope. An automated scan supplements these checks; it does not replace them.
- **Fix:** turn observed failures into scoped changes using project conventions, then rerun the failed checks and affected task paths. Follow the project's implementation and delegation instructions. Preserve unresolved product choices for the user or authorized owner.

## Assess with evidence

For each applicable criterion, record a compact row with its identifier, evaluated scope, method and environment, observed **PASS**, **FAIL**, or **NOT TESTED**, and evidence. A failure also needs user impact, reproduction steps, severity, proposed fix, and retest result. Record why a criterion is inapplicable rather than silently omitting it. State any untested scope and environmental limits. Scale the matrix to the actual UI; do not copy the standard into the report.

Choose checks based on the interface, including as relevant:

- Keyboard operation, focus order and visibility, focus movement into and out of overlays, escape and return behavior, and absence of keyboard traps.
- Semantics and accessible name, role, value, state, relationships, and status messages; inspect what assistive technology actually announces for consequential changes.
- Text and nontext contrast, text resizing, zoom and reflow, orientation and responsive variants.
- Pointer alternatives, target size and spacing, gesture and drag alternatives, and input modality changes.
- Motion, timing, interruption, reduced-motion behavior, and content that may trigger adverse reactions.
- Form instructions, required fields, validation, error identification, correction, and successful completion.
- Relevant media alternatives and captions, or mobile screen-reader, touch, and platform control patterns when the scope contains them.

For a custom combobox and dialog, first determine whether they are separate controls or one combined interaction. Check each component's relevant labeling, value or state, keyboard behavior, focus handling, and announcements; check the dialog's name, modality, and close behavior. If the combobox opens the dialog, also check their popup relationship, focus transfer, selection or cancellation, and return focus across the complete task. Use the applicable WAI-ARIA patterns to choose expected behavior; test the actual implementation rather than treating an ARIA attribute as proof.

Prioritize fixes by blocked tasks and user impact, then retest with the same method and environment where possible. A result for one component does not cover its host page or other responsive states. Report exactly what was assessed and what remains untested. Claim WCAG conformance only when the required full-page scope, complete processes where applicable, and all applicable criteria have been evaluated and satisfied; never infer it from a scan, a static mock, or a single component. [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/) explains the limits of any one tool.

Use `fudge:ux-research` when a design question requires observation with disabled participants or lived experience; an expert audit cannot substitute for that evidence. Use `fudge:design-qa` for broad design fidelity and responsive polish; this skill owns accessibility criteria and verification.
