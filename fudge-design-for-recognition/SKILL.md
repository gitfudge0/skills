---
name: fudge-design-for-recognition
description: Shape or critique an interface so its hierarchy, grouping, typography, controls, and feedback make the person's task understandable. Use for focused UI craft and rendered visual revision; use the UX or design roots when the wider experience or a deliverable needs routing.
---

# Design for recognition

Make the next useful thing apparent from the interface itself. Start with the person's task, existing product language and patterns, and the decision the interface must support. Work on the specific control, screen, or flow in scope; inspect the result in context when a rendered surface exists. This guide is the shared source for interface composition in the bundled `fudge:design` root and for separate invocation.

## Read the interface

Trace what a person must notice, distinguish, decide, and do. Identify the first point where the visual presentation could mislead or slow them. Read the intended content priority and grouping from the brief or product, then identify the visual cues for related items, available actions, selection, inactivity, progress, and result. Inspect hover and focus cues where those inputs apply; use a tooltip when a meaningful action or term still needs explanation after clearer labeling or icon treatment. If content priority or grouping is consequential and unsettled, send that specific question to `fudge:ux` for a scoped decision. For a critique, point to the visual ambiguity and its likely effect on the task. For a draft or implementation, change the smallest coherent part of the interface and inspect it again.

## Compose for the task

- **Grouping and hierarchy:** Express the chosen relationships and priority through proximity, position, scale, alignment, contrast, whitespace, imagery, and containers. Give important items emphasis relative to their surroundings; use a tighter range on dense screens when large display treatments would crowd the task. Make distinct choices visually distinguishable and leave enough space to show which elements belong together. Columns and a four-point spacing rhythm can help consistency and responsive behavior when they fit the product; neither decides the composition.
- **Typography:** Choose type roles from the content hierarchy and make scan targets distinct while body text remains readable. For font selection, anatomy, pairings, scale, line height, letter spacing, and responsive type, read [Typography decisions](references/typography.md) when those choices affect the task.
- **Color and depth:** Start from the product's established brand color and surface language when present. Use color to clarify priority and meaning, pairing semantic colors with text, shape, or another cue. In dark themes, compare surface steps, border contrast, and accent brightness in context; in light themes, tune shadows to the layer and background. Cards may need less depth than popovers above other content, but the rendered context decides. Check readable contrast rather than relying on opacity percentages. When color ramps or theme values become reusable rules, route their tokens and contracts to `fudge:design-system`.
- **Controls and feedback:** Make the affordance and current state visible. Size and align icons with adjacent text, then tune button padding for the target, label, and surrounding density. A ghost or secondary button can show a lower-emphasis action beside a primary one when the distinction is clear. Show task-relevant default, hover, focus, pressed, selected, disabled, pending, success, and error states. Feedback should tell the person whether an action started, completed, failed, or can be retried; `fudge:interaction-design` defines the transition and recovery contract. A micro interaction can clarify a change of state when its movement adds information.
- **Imagery and overlays:** Use an image when it helps recognition or gives meaningful context. If text sits on imagery, inspect actual images and crops; use a gradient, surface, or optional progressive blur when it improves text readability without obscuring useful image content.

Compare real interfaces serving a similar task for patterns worth testing, including their less visible states and responsive behavior. Inspiration suggests possibilities; it is not evidence about this product's users. Treat familiar recipes as options to evaluate, not rules to apply: one font, a modular ratio, fixed spacing counts, prescribed opacity, icon size, button padding, or heading leading can all be wrong for the actual content and screen. The relation between elements matters more than an isolated number.

## Inspect and revise

Use realistic content, including long names, missing data, and consequential states. Inspect the rendered result at relevant widths, themes, and input modes, then follow the person's task through the available interactions. Check whether the chosen priority reads as intended, cues remain distinguishable, text stays readable, actions look actionable, and feedback explains the result. Fix observed visual gaps and report the inspection's limits. An expert walkthrough supplies a design judgment, not evidence that participants succeeded.

## Specialist boundaries

`fudge:content-architecture` owns routes, content placement, labels, and interface words. `fudge:interaction-design` owns the transition and recovery contract behind actions. `fudge:design-system` owns reusable tokens and component contracts. `fudge:accessible-ui` owns criterion-level accessibility guidance and assessment. `fudge:design-qa` owns comparison of a built UI with its selected design. Use `fudge:ux-research` when the question needs observation with people. Carry those decisions into the visual treatment and flag consequential conflicts rather than writing a competing rule here.
