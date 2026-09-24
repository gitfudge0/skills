---
name: fudge:design-system
description: Use when the user wants design tokens, a component library, theming rules, a style guide, brand-to-UI translation, or a design system from visual or written source material. Also use for a requested high-fidelity conversion of existing wireframes.
---

# Design system

Turn source material into the design rules and specimens the requested work needs. Keep the source's identity, distinguish observed values from inferred choices, and stop at the requested scope.

## Choose the deliverable

| Request | Appropriate output |
|---|---|
| Audit, advice, or direction only | Findings in the requested format; no files by default. |
| Tokens or visual style | A design document or token artifact, informed by the project's existing theme where available. Add a visual specimen when seeing the values would help assess them or the user asks for one. |
| A component or bounded component set | Contracts and specimens for those components and their relevant states. Reference existing tokens where available; record proposed shared values in the design deliverable. |
| Full design system | A coherent token/rule source, component contracts, and visual specimens covering the agreed product scope. `DESIGN.md`, `DESIGN.html`, `COMPONENTS.md`, and `COMPONENTS.html` are one useful form, not a mandatory file set. |
| High-fidelity screens from a wireframe | The requested screens or board, using the applicable tokens and component rules. A full design system is not a prerequisite. |

Use the project's established artifact names and locations when present. For a design-only request, inspect and reference the app's theme as needed; change production theme or code only when the user requests application or implementation. A new design token artifact can hold proposed values without changing the app. Do not create a second source of truth merely to fill a template. For a full system, inventory the product surfaces and reusable patterns before deciding coverage; for a narrow request, inspect only the source needed to avoid inconsistency.

## Rules that apply at every size

1. **One authority for each value or rule.** Identify the existing theme, CSS, token file, or design document that owns implemented values. Design proposals may have their own declared authority until applied. A specimen or framework mapping references its declared source; a necessary self-contained copy is checked against it. If both `DESIGN.md` and `DESIGN.html` are made from scratch, state which owns values and which is a rendered or copied view.
2. **Evidence stays visible.** Separate exact extraction, visual estimates, normalization, and defaults. A static image cannot establish interaction states, motion, shadows, focus behavior, or a second theme. Record material assumptions beside the relevant rule or in a concise assumptions section.
3. **Coverage follows use.** Define themes, token groups, components, variants, states, and framework mappings that the request and product actually need. Add a second theme when requested or supported by the product brief or existing system. Include accessibility and reduced-motion behavior where the relevant component or motion is specified; do not invent an exhaustive catalog to complete a checklist.
4. **Verify produced outputs.** Check that referenced tokens exist, copies agree with their authority, and rendered specimens show the relevant behavior. Run conditional checks only for files and properties actually produced. A reviewer reruns checks rather than relying on a producer's claim.

## Routes

- For extracting tokens and style rules from an image, brand material, brief, or existing product, read [token extraction](references/token-extraction.md).
- For mapping chosen tokens or components into a target stack, read [framework mappings](references/framework-mappings.md). Map only when the target is known and the request needs implementation guidance.
- For reusable component coverage, read [component inventory](references/component-inventory.md). A wireframe is useful evidence, not a universal prerequisite.
- For converting an existing wireframe into high-fidelity screens, read [high-fidelity conversion](references/hifi-conversion.md). Apply 1:1 parity only when that conversion is the task.

## Verification

Inspect the actual deliverables. For HTML using copied token CSS, compare the copied block with its declared source. Check raw color values outside that block only when the artifact is meant to consume tokens exclusively; inspect CSS declarations, not documentation text or specimen labels. If a screen conversion promises parity with a wireframe, compare the actual frame IDs, labels, and actions in the relevant scope, not a raw substring count. Report observed mismatches and checks performed, without treating absent optional files as failures.
