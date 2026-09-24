---
name: fudge:interaction-design
description: Specify UI behavior across actions, states, roles, and failures so a flow can be implemented predictably. Use for multi-step tasks, async actions, save/resume, review cycles, or controls whose transitions and recovery rules are unclear.
---

# Interaction design

Define what happens when a person acts, including what they see while the result is uncertain. Start with their task, the relevant actors, and existing product policy. Inspect the current flow, domain rules, and authoritative project documents before specifying new behavior.

## Build the contract

1. Map the meaningful actions and events from entry to completion, interruption, and return. Include system events such as a response, timeout, or conflicting update when they affect the task.
2. Separate state dimensions that can vary independently. For example, a multi-step application may have an editing step, local changes, server save status, network status, submission status, and reviewer status. Do not compress them into one list of screens. Name which state is authoritative and what survives reload or a new session.
3. For each consequential event, specify its starting state and guard, allowed actor, resulting state, persisted effect or side effect, visible feedback, and failure or recovery path. Distinguish a local action from a server-confirmed result. Include what a second attempt does while the first is pending or after it succeeds.
4. Follow the actual paths through back, cancel, undo, save, resume, submit, return for changes, and retry as applicable. Cover pending, empty, invalid, error, and interrupted states. Where shared editing or repeated requests are possible, define conflict handling and duplicate-action behavior with the project's product and technical owners.
5. Trace the contract to the UI. Use `fudge:content-architecture` for labels, instructions, and recovery copy; use `fudge:ui-mock` to show the visible states; use `fudge:ui-prototype` when someone must attempt the task to validate the behavior. A visual frame alone does not define its transition.

Record behavior in the project's existing design or product source of truth. Use a separate linked flow document only when the number of events or actors would make the existing document hard to use. A small control can be specified in a few lines; no diagram, schema, or new file is required by default. Keep event names and state names consistent with related mocks and implementation work.

## Decisions and handoff

Mark an unsettled product rule as a question for the user or authorized owner, with the affected transitions. Do not invent autosave, offline availability, permission, data retention, or reviewer behavior to make a flow look complete. State any temporary design assumption and its consequence until the owner decides.

`fudge-design-for-recognition` supplies broad usability judgment; this skill owns the transition and feedback contract. `fudge:ui-mock` supplies static visual evidence, and `fudge:ship` owns code delivery and verification. Finish when every user-visible action and consequential failure path has predictable behavior an implementer can trace to the specification, and unverified assumptions remain explicit.
