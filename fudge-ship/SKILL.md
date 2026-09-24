---
name: fudge:ship
description: Take an idea, issue, feature, story, or task through implementation and delivery at a depth that matches its risk. Use for end-to-end building, "ship this," several fudge skills on one work item, or resuming a ship run. Route standalone code review to fudge:review.
---

# fudge:ship

During a ship run installed by the Fudge installer, stage names such as `fudge:test-plan`, `fudge:review`, and `fudge:design` refer to bundled guides. From this root `SKILL.md`, read `references/specialists/fudge-<specialist>/guide.md` for each selected stage or specialist, then follow links relative to that guide. The design and review guides are bundled so this root works when installed alone. The source skill folders remain available for separate manual installation.

Build one work item to its chosen endpoint. A finished feature may be one part of a larger release. Finishing this work never implies that a release was cut.

The user owns expected behavior and scope. The repository's `AGENTS.md`, `CLAUDE.md`, project-level skills, and existing conventions own implementation details. Use decisions and authorization already given in the conversation; ask only when a consequential choice remains unsettled. Do not make architecture or code structure a user approval gate.

## Choose the work and depth

Name the work item and its boundary. Use the endpoint already requested by the user; otherwise default to **verified locally**. Other endpoints are **PR opened**, **PR integrated**, or **release/deploy** when selected. An analysis-only route ends with its requested artifact or decision. Issue tracking is a separate opt-in; a linked issue does not itself authorize updates. Read [external workflows](references/external-workflows.md) before issue, PR, or release/deploy work.

Choose the smallest workflow that gives credible evidence for this change:

- **Routine:** bounded, reversible work with a clear requested behavior and limited blast radius. This is the default for a focused bug fix, local UI or installer change, documentation, or skill edit. Follow the routine path below.
- **Comprehensive:** consequential work with material security, privacy, financial, permission, migration, data-loss, or external-release risk; broad cross-system changes with unsettled behavior; or an explicit request for formal test planning, staged approvals, or a full audit. Follow the comprehensive path below.

An individual uncertainty may warrant one specialist without turning the whole work item into a comprehensive run. If scope or risk grows, switch paths and explain why. Preserve completed decisions and evidence rather than restarting or asking for the same approval again. A user correction narrows or changes the requested work; address that correction directly. For example, “we didn't need new tests” stops unnecessary test work but does not authorize deleting existing tests or other assets.

## Route only the needed stages

Use read-only recon to find the relevant behavior, dependencies, existing checks, and project instructions. Invoke a specialist only when its output serves this work item:

| Need | Owning skill | Trigger |
|---|---|---|
| Reconcile requirements | `fudge:gap-analysis` | Documents conflict or leave a material gap. |
| Decide product direction | `fudge:decision-room` | A consequential choice remains unsettled. |
| Shape UI | `fudge:design` | UI guidance or a reviewable visual decision is needed. |
| Plan distinct failure cases | `fudge:test-plan` | Risk or an explicit request warrants a separate test plan. |
| Implement | `fudge:delegate` | Product or test files will change. |
| Formal review | `fudge:review` | The change is comprehensive or the user requests this review. |

Read each selected skill and honor the contract for the chosen path. A named stage selects membership, not order. For standalone code review, use the `fudge:review` root without starting a ship run. If that root is unavailable, read the bundled `references/specialists/fudge-review/guide.md` and follow its standalone mode. Unknown stage names require clarification. If a required skill is unavailable, report the blocker instead of silently replacing it.

## Routine path

1. Confirm the requested behavior from the conversation and repository. Resolve only material uncertainty. Use existing governing rules; when no project-specific convention is defined, follow the repository's patterns. A consequential conflict between rules needs resolution before the affected work.
2. Brief one cohesive implementation worker through `fudge:delegate` unless independent work clearly benefits from separate workers. Protect pre-existing user edits. A user's request to remove newly added work does not imply removal of pre-existing files.
3. Verify the behavior with the smallest relevant checks that can catch a plausible regression: existing focused tests, a manual walk, syntax or build checks, as appropriate. Add or change automated tests when a meaningful failure mode needs durable coverage or the user asks for them. Multiple UI steps alone do not require a new end-to-end suite. The root reads raw check output before reporting a pass.
4. Read the final diff for scope, correctness, and unintended changes. Fix issues and recheck affected behavior. Give a concise result, verification evidence, and any material remaining risk. Complete the authorized endpoint.

Routine work needs no run directory, HTML matrix, separate test-case approval, blanket full-suite gates, two-pass review, or conventions audit. A direct request to commit or push remains authorization for that endpoint, subject to the repository's own safeguards. Do not re-ask a settled visual or behavior choice merely because implementation has begun.

## Comprehensive path

Create a unique `.fudge/<branch>/ship/<YYYY-MM-DD>-<slug>[-N]/` directory and durable `run.json`. Keep run artifacts there. Read [run state and recovery](references/run-state.md) when creating or resuming the run and before implementation touches a worktree. Confirm an implementation target is a Git repository. Record the original request, endpoint, decisions already approved, artifacts, gate responses, verification evidence, and blockers. Supply run-local paths to selected stages. For UI work, `fudge:design` may return concise guidance or a reviewable mock; a mock is required only when the visual decision needs to be seen.

Find and load actionable coding rules in project skills, `AGENTS.md`, `CLAUDE.md`, or equivalent sources, and record their paths and revisions. If consequential rules conflict, resolve the conflict before affected code. Offer `fudge:conventions` setup only when a missing project contract itself blocks the work; creating one requires separate authorization.

Before product or test code, have `fudge:test-plan` produce a risk-based, versioned HTML matrix in `plan-only` mode. Include concrete setups, actions, observable outcomes, priority, type, and meaningful gaps without padding case count. Present the matrix. Ask for approval of its **expected behavior and material coverage** only where those decisions remain unsettled; record prior explicit decisions that cover the same contents against this version. A behavior approval does not, by itself, require writing a test for every case. Revise the matrix and seek approval only when an expected result or material coverage decision changes. Implementation details that leave them intact do not reopen the gate.

After the applicable approval, establish the worktree baseline and planned ownership as [run state and recovery](references/run-state.md) specifies. Delegate implementation. Write new tests for meaningful regression risks and approved coverage where an automated harness is suitable; use existing checks or manual evidence where they suffice. The root runs targeted checks and the relevant project gates, reads raw output, and records commands and results. Mark matrix cases `PASS`, `FAIL`, or `NOT RUN` from observed evidence in a separate report; never infer a pass from code inspection. Fix failures in scope and rerun affected checks. Surface high-risk unrun cases for an explicit decision.

Review the full run diff with `fudge:review` in orchestrated two-pass mode. The root verifies candidate findings against source, diff, approved behavior, and gate output before fixes. Recheck applicable governing rules and use `fudge:conventions` in scoped audit mode when a project contract exists. Fix verified violations, then rerun affected verification, review, and audit. Only a separately approved amendment changes project rules. A later run-owned project-file edit invalidates the audit; run-local metadata does not.

Before each push, merge, or finish, recheck the exact full-run-diff content hash and governing source revisions as run state specifies. Finish when the approved behavior, relevant verification, review, and current applicable audit meet the selected endpoint. Report unrun cases, accepted risks, exceptions, and incomplete external steps plainly.

On `resume`, inspect open runs and saved state. If several match, let the user choose. Re-present only an awaiting or changed decision; retain prior approvals and verification evidence. Recheck the baseline and governing sources before retrying an interrupted stage. A plain resume reports a recorded blocker; retry only on an explicit corrective instruction.
