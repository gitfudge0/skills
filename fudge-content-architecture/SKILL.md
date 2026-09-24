---
name: fudge:content-architecture
description: Organize UI content and write task-specific interface language. Use when people struggle to find a destination, understand labels or instructions, complete a form, or recover from an error across a product flow.
---

# Content architecture

Make the right information findable and the next action understandable. Own the structure and words across the person's task, not just the copy on one screen. Preserve the product's established voice and the project's authoritative design documents.

## Shape the path

1. Establish the person's task, starting point, relevant roles and context. Inventory the existing routes, navigation, search entry points, page content, instructions, forms, and states that affect that task. Follow links and transitions instead of assuming the sitemap reflects the experience.
2. Identify the concepts people need to distinguish and the language they use for them. Trace known terms to user research, support records, search queries, or supplied domain material. Mark an untested label as a hypothesis; never fabricate a user quote or call an agent's guess user evidence.
3. Decide where each piece of information belongs, how related items are grouped, and how people can reach them through navigation, search, and contextual links. Make the route and destination names distinct enough to support a choice. Account for wayfinding and a return path when a task crosses sections or steps.
4. Write the interface language that carries the task: page and section names, action labels, field labels and help, instructions, confirmation and success messages, empty states, and errors. State the action, its consequence, and a recovery step where those matter. Use terms consistently without forcing different concepts under one familiar label.
5. Check the proposed path with realistic content and relevant states. For a consequential or disputed terminology choice, ask `fudge:ux-research` to test findability or comprehension with a neutral task. An expert walkthrough can expose a likely problem, but cannot establish that users will find or understand the result.

Scale the work to the request. A route/content inventory, a taxonomy or navigation decision, and a label/content matrix can be useful working forms; do not require separate files or a fixed method for every task. Record the decisions, their evidence or confidence, and unresolved assumptions in the project's existing source of truth. Update only the requested artifacts and avoid a second, competing set of content rules.

Do not invent product policy, eligibility, deadlines, prices, clinical advice, financial consequences, or other consequential facts to make copy sound complete. Surface missing facts and use approved source material. Keep proposed copy distinguishable from verified product rules.

## Boundary and completion

`fudge-design-for-recognition` applies broad hierarchy and usability judgment; this skill owns content placement, navigation vocabulary, and interface wording. `fudge:interaction-design` owns the behavior and state transitions behind an action. `fudge:ui-mock` owns the visual board; `fudge:design-system` owns visual tokens and component contracts. Give those skills the settled content decisions when they need them.

Finish when the intended person has a plausible route to the right place, can understand the next action and its consequence, and can recover from an error. Show the chosen route and key copy in context, note what was validated versus inferred, and leave any unresolved product facts visible to the implementation owner.
