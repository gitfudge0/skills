# Interaction design

Internal capability: enter through the owning public skill. For package addresses, use `shared/locate.md` at the ancestor containing `.fudge-package.json` (installed) or `scripts/skill-manifest.json` (source). This guide’s own references stay relative to it.

Define what happens when a person acts, including what they see while the result is uncertain. Start with their task, the relevant actors, and existing product policy. Inspect the current flow, domain rules, and authoritative project documents before specifying new behavior.

## Build the contract

1. Map the meaningful actions and events from entry to completion, interruption, and return. Include system events such as a response, timeout, or conflicting update when they affect the task.
2. Separate state dimensions that can vary independently. For example, a multi-step application may have an editing step, local changes, server save status, network status, submission status, and reviewer status. Do not compress them into one list of screens. Name which state is authoritative and what survives reload or a new session.
3. For each consequential event, specify its starting state and guard, allowed actor, resulting state, persisted effect or side effect, visible feedback, and failure or recovery path. Distinguish a local action from a server-confirmed result. Include what a second attempt does while the first is pending or after it succeeds.
4. Follow the actual paths through back, cancel, undo, save, resume, submit, return for changes, and retry as applicable. Cover pending, empty, invalid, error, and interrupted states. Where shared editing or repeated requests are possible, define conflict handling and duplicate-action behavior with the project's product and technical owners.
5. Trace the contract to the UI. Use the content-architecture module for labels, instructions, and recovery copy; use the ui-mock module to show the visible states; use the ui-prototype module when someone must attempt the task to validate the behavior. A visual frame alone does not define its transition.

Record behavior in the project's existing design or product source of truth. Use a separate linked flow document only when the number of events or actors would make the existing document hard to use. A small control can be specified in a few lines; no diagram, schema, or new file is required by default. Keep event names and state names consistent with related mocks and implementation work.

## Resolve uncertainty and preserve control

Select only checks that apply to the changed task; keep the contract in its existing source of truth:

- **Empty and filtered results:** distinguish first use, no matches, and unavailable data. Offer an appropriate next action, such as creating an item, changing a query, clearing filters, or retrying. For filter reset, specify which controls it affects and whether it restores defaults or removes all restrictions; preserve unrelated settings and make the resulting selection visible.
- **Known information and interrupted input:** reuse appropriate values already available for the current person and account, show their source when ambiguity matters, and allow correction. Preserve entered values through recoverable errors according to product policy. Check account changes and stale values; convenience must not expose another account’s information or imply unauthorized retention.
- **Permissions:** request necessary access when its purpose becomes relevant, explain that purpose, and define denial or revocation behavior and any available alternative. Follow platform and product policy; do not promise a fallback the service cannot support.
- **Waiting and completion:** choose feedback proportionate to the operation. A brief spinner can suffice; a longer wait may need truthful status, a skeleton for known content structure, or supported progress and cancellation. Never invent stages or percentages. Confirm the actual outcome through an updated result, status, or message; a fast save with an obvious updated result need not add a toast or success screen. Define how the person can find the result and recover if completion remains uncertain.

## Decisions and handoff

Mark an unsettled product rule as a question for the user or authorized owner, with the affected transitions. Do not invent autosave, offline availability, permission, data retention, or reviewer behavior to make a flow look complete. State any temporary design assumption and its consequence until the owner decides.

The design-for-recognition module supplies broad usability judgment; this skill owns the transition and feedback contract. The ui-mock module supplies static visual evidence, and `fudge:ship` owns code delivery and verification. Finish when every user-visible action and consequential failure path has predictable behavior an implementer can trace to the specification, and unverified assumptions remain explicit.

## Recovery transition example

| Starting state | Event | Next state and observable contract |
|---|---|---|
| Editing | Submit | Pending; retain input and show feedback |
| Pending | Submit again | Remain pending; reuse the same submission identity |
| Pending | Network timeout | Outcome unknown; retain input and explain uncertainty |
| Outcome unknown | Retry | Resolve/reuse the original operation identity; avoid duplicate records |
| Pending | Navigate away | Follow the stated interruption policy; returning reveals actual outcome |
| Rejected | Correct and submit | Pending with corrected input; preserve other fields |
| Confirmed | Back or reload | Show the saved result according to the persistence contract |

These are proposed contracts, not claims about an implementation. Confirm service support for deduplication and unknown outcomes before promising this behavior.
