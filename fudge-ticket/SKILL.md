---
name: fudge:ticket
description: Draft, reconcile and update issue-tracker tickets, drafts first. Use to turn mocks, plans or conversations into small user-facing stories, reconcile a ticket with what was built, comment on or transition a ticket after merge, or draft replies to ticket comments. Works with Jira, GitHub Issues, Linear or paste-ready text; implementation belongs to ship.
---

# fudge:ticket

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

Read package-root `shared/working-defaults.md` for the project's `external-writes` setting. Body templates are in `references/templates.md`.

## Tracker

Use whatever tracker access the host provides: an Atlassian/Jira connector, `gh issue`, a Linear connector or CLI. Discover the project's issue types, required fields and transitions at runtime instead of assuming them. With no tracker access, produce paste-ready drafts and say which fields the user must set on paste. If a project skill, template or conventions file defines ticket structure, follow it over the templates here.

## Modes

| Mode | When | Output |
|---|---|---|
| draft | Mocks, a plan, a description or a conversation should become stories. | Small user-facing stories with acceptance criteria; platform work as subtasks. |
| reconcile | A ticket should match what was actually built. | Updated description and test notes, a deviation list, drafts for related tickets. |
| update | Comment, transition, assign or relink a ticket, e.g. after merge. | The exact change, then the applied result with links. |
| reply | A ticket has comments that need answers. | One drafted reply per open comment. |

### Draft

1. Play the source back in one sentence; ask only what would change the stories.
2. Split into the smallest independently shippable, user-facing stories. Slice 1 is the thinnest end-to-end path. Backend, web and mobile splits are subtasks of a story, never separate stories.
3. More than five acceptance criteria, or a title that needs "and", means split again. Name what each story defers in its out-of-scope section.
4. When the user asks for a list, give titles and one-line descriptions first; write full bodies on request.
5. Write implementation notes only from code actually read. Otherwise mark the subtask as needing developer detail with specific open questions.

### Reconcile

What was implemented is the truth. Read the ticket, its linked PRs (merged state, final diff, review threads) and the merged code. Draft the updated description and test notes from the code, list each deviation from the original ticket with its evidence, and draft related tickets for deferred or newly discovered work. Do not rewrite the ticket to match intent the code does not carry.

### Update

Verify each linked PR is actually merged (and into which branch) before commenting that work is done. Read the ticket's available transitions and pick the matching one; never guess a status name. Look up assignees by account rather than typing a name. Use the QA handoff comment template for post-merge moves.

### Reply

Read the full thread and the code or PR each comment refers to. Draft one reply per open comment: answer, agreed change, or question back. When a comment needs a code fix, say so in the reply draft; hand the fix to `fudge:ship` only when the user asks for it. This skill does not implement.

## Rules

- **Draft first.** Show the exact content (title, body, fields, comment, transition, assignee) and wait. Approval covers that content only; changed content needs a fresh look. An explicit "create it" or "post it" in the request authorizes the write. Precedence follows `shared/working-defaults.md`.
- **Ask only for what cannot be inferred:** project, issue type, sprint, assignee, parent. Reuse answers already settled in the conversation or working defaults ("assign to me, current sprint, no parent").
- **Never invent** ticket keys, statuses, transitions, sprints, fields or people. Look them up; when lookup fails, say so and leave a placeholder.
- **Factual and concise.** Tracker updates state what changed, with links. Post milestones, not every internal iteration.
- **Ask before changing** a field, audience or ownership whose intended value is unclear.
- **Failures stay visible.** Log a failed update and never present it as succeeded; if a multi-ticket write fails midway, report exactly what was created and what was not.
- **Report links** to every ticket, comment and transition created or changed, in hierarchy order.
