---
name: fudge:retro
description: Review a coding session for evidenced workflow friction, identify causes, and propose small durable improvements to guidance, tooling, checks, and skill orchestration. Use when explicitly asked for a retrospective; code defects belong to review and unresolved diagnosis to investigation.
---

# fudge:retro

## Locate guidance

Package addresses (`shared/`, `references/modules/`, `references/roots/`) resolve from the nearest ancestor with `.fudge-package.json`, or `scripts/skill-manifest.json` in source. Read `shared/locate.md` when resolving a source address or nested guide; this guide's own references remain relative.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

Inspired by Matt Pocock's [retro skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md), with session learning and routing for this collection.

## Bound the evidence

Run only on an explicit retrospective request. Default to the current session; honor a specified session or work item. Name the scope and available evidence. Read relevant conversation, user corrections, diffs, command failures, review findings and governing instructions. Inspect only records that can change the conclusion. Do not trawl unrelated sessions, account histories or logs; omit secrets and unnecessary personal details from evidence excerpts. When a requested transcript is unavailable, say what is missing and limit conclusions to accessible evidence rather than inventing a session history.

## Find what changes the next session

Prioritize consequential friction: repeated exploration, avoidable user corrections, redundant approval requests, ineffective delegation, missed defects, weak verification and expensive tool loops. Preserve successful approaches worth repeating. One incident can justify a narrow fix when its consequence is clear; do not turn every inconvenience into permanent policy.

Separate observed events from causal hypotheses. Cite a transcript event, command result, review finding, or exact file location for each material observation. Distinguish missing guidance, ignored guidance, conflicting guidance, broken tooling, unavailable information and legitimate requirement changes. More instructions will not fix guidance that was already clear and ignored. A changed requirement is not evidence of an earlier mistake. State causal uncertainty and the evidence that would resolve it; route substantial unresolved diagnosis instead of speculating.

Choose the smallest durable improvement that would prevent the observed failure. Inspect the proposed destination before recommending an amendment. Repair an existing check before adding one. Prefer automation for mechanical errors, focused guidance for judgment, navigation pointers for discovery, and skill changes for workflow failures. Weigh recurrence, consequence, confidence, maintenance and added process. Merge proposals with the same cause; drop generic advice and changes whose cost exceeds their likely value. Allow no durable change warranted.

## Return proposals

Return a short ranked set, sized to the evidence, with these fields for each proposal:

| Field | Content |
|---|---|
| Observation | What happened, its consequence, and cited evidence. |
| Cause | Supported explanation, confidence, and unresolved hypotheses. |
| Change | The exact smallest improvement and the failure it would prevent. |
| Destination | Existing file, check, tool or owning skill; name any unconfirmed destination. |
| Validation | An observable failure/valid case or future outcome that would show the change works. |

Include useful successes and evidence gaps briefly. Do not manufacture a quota of findings, a mandatory report artifact or a new process. Keep proposed changes distinct from changes actually applied; static inspection and unrun behavioral scenarios are not passing execution evidence.

## Ownership and application

Proposals are the default endpoint. A request to run a retro alone does not authorize editing project rules, skills or global configuration. When the user requests application, carry forward the accepted scope and prior permissions without adding a redundant approval gate. Apply only authorized improvements through their existing owner and verify the relevant outcome. Project evidence does not justify automatic global edits.

- Change correctness or security review: `references/roots/review/guide.md`.
- Deeper unresolved causal questions: `references/roots/investigation/guide.md`.
- Project guidance, conventions, verification recipes or tooling: `references/roots/setup/guide.md`.
- Implementation of accepted code, check or skill improvements: `references/roots/ship/guide.md`.

Keep the retro's proposal endpoint when consulting an owner for context. Read its implementation workflow only when application is requested; do not let a bundled dependency expand the task.
