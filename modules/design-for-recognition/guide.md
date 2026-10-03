# Design for recognition

Internal capability: enter through the owning public skill. Resolve cross-module and shared paths from the package root (nearest ancestor containing `.fudge-package.json`): `references/modules/<module>/guide.md`, `references/roots/<root>/guide.md`, and `shared/`. In source, use the repository identified by `scripts/skill-manifest.json`, with `modules/`, `fudge-<root>/SKILL.md`, and `shared/`. Local assets and references remain relative to this guide.

Make the next useful thing apparent from the interface itself. Start with the person's task, existing product language and patterns, and the decision the interface must support. Work on the specific control, screen, or flow in scope; inspect the result in context when a rendered surface exists. This guide is the shared source for interface composition in the bundled `fudge:design` root as an internal capability.

## Read the interface

Trace what a person must notice, distinguish, decide, and do. Identify the first point where the visual presentation could mislead or slow them. Read the intended content priority and grouping from the brief or product, then identify the visual cues for related items, available actions, selection, inactivity, progress, and result. Inspect hover and focus cues where those inputs apply; use a tooltip when a meaningful action or term still needs explanation after clearer labeling or icon treatment. If content priority or grouping is consequential and unsettled, send that specific question to `fudge:ux` for a scoped decision. For a critique, point to the visual ambiguity and its likely effect on the task. For a draft or implementation, change the smallest coherent part of the interface and inspect it again.

## Compose for the task

- **Grouping and hierarchy:** Express the chosen relationships and priority through proximity, position, scale, alignment, contrast, whitespace, imagery, and containers. Give important items emphasis relative to their surroundings; use a tighter range on dense screens when large display treatments would crowd the task. Make distinct choices visually distinguishable and leave enough space to show which elements belong together. Columns and a four-point spacing rhythm can help consistency and responsive behavior when they fit the product; neither decides the composition.
- **Typography:** Choose type roles from the content hierarchy and make scan targets distinct while body text remains readable. For font selection, anatomy, pairings, scale, line height, letter spacing, and responsive type, read [Typography decisions](references/typography.md) when those choices affect the task.
- **Color and depth:** Start from the product's established brand color and surface language when present. Use color to clarify priority and meaning, pairing semantic colors with text, shape, or another cue. In dark themes, compare surface steps, border contrast, and accent brightness in context; in light themes, tune shadows to the layer and background. Cards may need less depth than popovers above other content, but the rendered context decides. Check readable contrast rather than relying on opacity percentages. When color ramps or theme values become reusable rules, route their tokens and contracts to the design-system module.
- **Controls and feedback:** Make the affordance and current state visible. Size and align icons with adjacent text, then tune button padding for the target, label, and surrounding density. A ghost or secondary button can show a lower-emphasis action beside a primary one when the distinction is clear. Show task-relevant default, hover, focus, pressed, selected, disabled, pending, success, and error states. Feedback should tell the person whether an action started, completed, failed, or can be retried; the interaction-design module defines the transition and recovery contract. A micro interaction can clarify a change of state when its movement adds information.
- **Imagery and overlays:** Use an image when it helps recognition or gives meaningful context. If text sits on imagery, inspect actual images and crops; use a gradient, surface, or optional progressive blur when it improves text readability without obscuring useful image content.

Compare real interfaces serving a similar task for patterns worth testing, including their less visible states and responsive behavior. Inspiration suggests possibilities; it is not evidence about this product's users. Treat familiar recipes as options to evaluate, not rules to apply: one font, a modular ratio, fixed spacing counts, prescribed opacity, icon size, button padding, or heading leading can all be wrong for the actual content and screen. The relation between elements matters more than an isolated number.

## Inspect and revise

Use realistic content, including long names, missing data, and consequential states. Inspect the rendered result at relevant widths, themes, and input modes, then follow the person's task through the available interactions. Check whether the chosen priority reads as intended, cues remain distinguishable, text stays readable, actions look actionable, and feedback explains the result. Fix observed visual gaps and report the inspection's limits. An expert walkthrough supplies a design judgment, not evidence that participants succeeded.

## Specialist boundaries

the content-architecture module owns routes, content placement, labels, and interface words. the interaction-design module owns the transition and recovery contract behind actions. the design-system module owns reusable tokens and component contracts. the accessible-ui module owns criterion-level accessibility guidance and assessment. the design-qa module owns comparison of a built UI with its selected design. Use the ux-research module when the question needs observation with people. Carry those decisions into the visual treatment and flag consequential conflicts rather than writing a competing rule here.

## Worked visual change

Before: a dense order table gives customer names, timestamps, and “Needs action” badges equal weight. The operator must scan all columns to locate blocked orders. After: keep the existing table structure, emphasize the action-needed state with a readable label and consistent semantic color, reduce timestamp emphasis, and put the resolving action beside the blocked item.

The intended benefit is faster identification and resolution of blocked orders. That is a design hypothesis until measured; a prettier screenshot alone does not establish task improvement.
