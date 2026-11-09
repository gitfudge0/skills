# Content architecture

Internal capability: enter through the owning public skill. For package addresses, use `shared/locate.md` at the ancestor containing `.fudge-package.json` (installed) or `scripts/skill-manifest.json` (source). This guide’s own references stay relative to it.

Make the right information findable and the next action understandable. Own the structure and words across the person's task, not just the copy on one screen. Preserve the product's established voice and the project's authoritative design documents.

## Shape the path

1. Establish the person's task, starting point, relevant roles and context. Inventory the existing routes, navigation, search entry points, page content, instructions, forms, and states that affect that task. Follow links and transitions instead of assuming the sitemap reflects the experience.
2. Identify the concepts people need to distinguish and the language they use for them. Trace known terms to user research, support records, search queries, or supplied domain material. Mark an untested label as a hypothesis; never fabricate a user quote or call an agent's guess user evidence.
3. Decide where each piece of information belongs, how related items are grouped, and how people can reach them through navigation, search, and contextual links. Make the route and destination names distinct enough to support a choice. Account for wayfinding and a return path when a task crosses sections or steps.
4. Write the interface language that carries the task: page and section names, action labels, field labels and help, instructions, confirmation and success messages, empty states, and errors. State the action, its consequence, and a recovery step where those matter. Use terms consistently without forcing different concepts under one familiar label.
5. Check the proposed path with realistic content and relevant states. For a consequential or disputed terminology choice, ask the ux-research module to test findability or comprehension with a neutral task. An expert walkthrough can expose a likely problem, but cannot establish that users will find or understand the result.

Scale the work to the request. A route/content inventory, a taxonomy or navigation decision, and a label/content matrix can be useful working forms; do not require separate files or a fixed method for every task. Record the decisions, their evidence or confidence, and unresolved assumptions in the project's existing source of truth. Update only the requested artifacts and avoid a second, competing set of content rules.

Do not invent product policy, eligibility, deadlines, prices, clinical advice, financial consequences, or other consequential facts to make copy sound complete. Surface missing facts and use approved source material. Keep proposed copy distinguishable from verified product rules.

## Remove uncertainty in the copy

Apply these checks to the controls and content in scope:

- Name the action and object where the consequence would otherwise be unclear: “Confirm purchase” rather than “Let’s go.” Put helper text beside the decision when people need to know who can see a note, where it appears, or what a submission changes.
- Make errors specific enough to act on: identify the affected input or operation, what is known about the failure, and the available correction or recovery. Preserve uncertainty when the outcome is unknown; avoid exposing sensitive information or blaming the person without evidence.
- Keep information needed for a decision available in context. Prefer wrapping or a usable expansion over truncating prices, conditions, distinguishing names, or recovery instructions. Check realistic long and localized text at relevant widths; hover-only disclosure is insufficient for touch and keyboard users.
- Identify applicable disclosures from approved product or policy sources and place them at the relevant decision. Check their destinations. Do not add generic terms, consent claims, or privacy assurances merely to make a screen feel trustworthy; surface missing authoritative copy.

## Boundary and completion

The design-for-recognition module applies broad hierarchy and usability judgment; this skill owns content placement, navigation vocabulary, and interface wording. The interaction-design module owns the behavior and state transitions behind an action. the ui-mock module owns the visual board; the design-system module owns visual tokens and component contracts. Give those modules the settled content decisions when they need them.

Finish when the intended person has a plausible route to the right place, can understand the next action and its consequence, and can recover from an error. Show the chosen route and key copy in context, note what was validated versus inferred, and leave any unresolved product facts visible to the implementation owner.

## Cross-surface terminology example

If the domain uses “workspace” for a shared collection, apply that meaning across navigation (“Workspaces”), creation (“Create workspace”), membership (“Invite to workspace”), and errors (“You no longer have access to this workspace”). Record any intentional distinction from “project”; do not alternate terms merely for variety.

For localization, give translators the concept, audience, action, and space constraint. Avoid concatenated sentence fragments and assumptions about plural forms or word order. Verify localized labels in their actual layout; a glossary entry alone does not prove comprehension.
