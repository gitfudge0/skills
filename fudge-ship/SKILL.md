---
name: fudge:ship
description: Take an idea, issue, feature, story, or task through implementation and delivery at a depth that matches its risk. Use for end-to-end building, "ship this," several fudge skills on one work item, resuming a ship run, or decomposing a system before building. Route standalone code review to fudge:review.
---

# fudge:ship

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md` unless the manifest declares another source and entry (HTML planning uses `plan/SKILL.md`), root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, including the swarm loop of framing completion, dispatching owned slices, draining workers, and aggregating evidence; use `shared/writing.md` for prose and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

Build one work item to its chosen endpoint. A finished feature may be one part of a larger release. Finishing this work never implies that a release was cut.

The user owns expected behavior and scope. The repository's `AGENTS.md`, `CLAUDE.md`, project-level skills, and existing conventions own implementation details. Use decisions and authorization already given in the conversation; ask only when a consequential choice remains unsettled. Do not make architecture or code structure a user approval gate.

## Choose the work and depth

Name the work item and its boundary. Use the endpoint already requested by the user. For implementation in a Git repository with a configured forge, default to **PR ready**: an open, pushed PR whose current diff has completed the review loop and required checks. **Verified locally** and analysis-only requests override that default. **PR opened** stops at creation; **PR integrated** and **release/deploy** require explicit selection. Missing Git, a remote, credentials, or forge access does not prevent useful local work or authorize initializing/publishing a repository; report the unavailable endpoint accurately. An analysis-only route ends with its requested artifact or decision. Issue tracking is a separate opt-in; a linked issue does not itself authorize updates. Read [PR delivery](references/pr-delivery.md) before Git implementation isolation or a PR endpoint, and [external operations](references/external-workflows.md) for issue tracking or release/deploy.

Choose the smallest workflow that gives credible evidence for this change:

- **Routine:** bounded, reversible work with clear behavior and limited blast radius. A focused bug fix, UI change, documentation, or skill edit usually fits, unless its actual consequences warrant comprehensive assurance.
- **Comprehensive:** material security, privacy, financial, permission, migration, data-loss, or production-release risk; broad cross-system changes with unsettled contracts; or an explicit request for a full audit. A small diff can still have high consequences. Read [comprehensive assurance](references/comprehensive.md) before affected implementation.

Choose reporting and recovery needs separately from engineering risk. Use a concise risk-based plan by default, including for a narrow comprehensive change. Generate a formal HTML matrix only when requested or needed by an established project process. Use durable run state when work spans sessions, has multiple coordinated stages, needs recovery, or the user requests it; higher risk alone does not require HTML or a run directory. An explicit test-plan request selects that capability without automatically adding every comprehensive stage.

An individual uncertainty may warrant one specialist without turning the whole work item into a comprehensive run. If scope or risk grows, switch paths and explain why. Preserve completed decisions and evidence rather than restarting or asking for the same approval again. A user correction narrows or changes the requested work; address that correction directly. For example, “we didn't need new tests” stops unnecessary test work but does not authorize deleting existing tests or other assets.

## Route only the needed stages

Every implementation begins with bounded discovery under `references/modules/engineering/guide.md`; every implementation ends with observed evidence under `references/modules/verification/guide.md`. Product intent and consequential tradeoffs remain user decisions. Analysis-only work loads only the guidance serving its requested artifact.

Read `references/modules/gap-analysis/guide.md` only when missing or conflicting requirements warrant deeper reconciliation. Retain every valid gap and its evidence; summaries may be shorter than the register. “What is missing before we build?” is an analysis-only request: return the scoped gaps, concrete decisions, and next actions without starting implementation. Clear requests need a small discovery pass, not a workshop.

Use selected guidance only when its output serves this work item:

| Need | Owning skill | Trigger |
|---|---|---|
| Reconcile requirements | `references/modules/gap-analysis/guide.md` | Documents conflict or leave a material gap. |
| Decompose a system | `references/modules/system-decomposition/guide.md` | A broad brief needs responsibilities, contracts, or candidate work before implementation; decomposition-only requests stop at analysis. |
| Pressure-test a decision | `references/modules/decision-room/guide.md` | A consequential choice remains unsettled. |
| Shape the experience | `references/roots/ux/guide.md` | User needs, content structure, task flow, state behavior, or usability needs a decision. |
| Shape the interface | `references/roots/design/guide.md` | Visual expression, UI guidance, a reviewable mock, or component direction is needed. |
| Make an interactive implementation plan | `references/modules/plan/guide.md` | The user requests an HTML plan, or a complex multi-file change needs a reviewable tree of behavior, exhibits, and decisions. |
| Plan distinct failure cases | `references/modules/test-plan/guide.md` | Risk or an explicit request warrants a separate test plan. |
| Make the project runnable | `references/roots/setup/guide.md` | Dependencies, environment, or startup readiness block implementation or verification; use focused run setup. |
| Engineer the change | `references/modules/engineering/guide.md` | Bounded discovery, cause tracing, state modeling, or implementation is needed. |
| Coordinate implementation | `shared/execution.md` | Product or test files will change; single owner for delegation and integration. |
| Verify completion | `references/modules/verification/guide.md` | Any implementation needs acceptance evidence and current checks. |
| Isolate and deliver a PR | [PR delivery and learning](references/pr-delivery.md) | Git implementation isolation or a PR endpoint. |
| Track issues or deploy | [External operations](references/external-workflows.md) | Explicit issue tracking, deployment, or compatibility risk. |
| Add comprehensive assurance | [Comprehensive assurance](references/comprehensive.md) | Comprehensive risk path. |
| Recover durable work | [Run state](references/run-state.md) | Cross-session coordination or recovery. |
| Formal review | `references/roots/review/guide.md` | The change is comprehensive or the user requests this review. |

When HTML planning is selected, use the bundled guide and its adjacent runtime, block reference, and examples. The source is `plan/`; the installed directory is package-root `references/modules/plan/`. Prefer `examples/sample-plan.html` for the contents rail, grouped expand/collapse, and light/dark switch. Keep clear routine work in a concise plan. For a review-before-build request, hand over the packed page and wait for the user response before affected implementation; existing authorization and settled decisions still apply. A planning-only request ends with the page.

Read each selected skill and honor the contract for the chosen path. A named stage selects membership, not order; UX and design can inform each other in either direction. Use one or both when the task calls for them, carrying settled decisions across the guides without restating their rules. For standalone code review, use the `fudge:review` root without starting a ship run. If that root is unavailable, read package-root `references/roots/review/guide.md` and follow its standalone mode. A pressure-test supplies simulated perspectives and arguments, not independent corroboration. Judge the arguments against evidence; agreement between personas is not stronger evidence. Unknown stage names require clarification. If a required skill is unavailable, report the blocker instead of silently replacing it.

## Routine path

1. Establish acceptance conditions, affected contracts, and the implementation approach using `references/modules/engineering/guide.md`. Resolve only material uncertainty. Use governing rules and existing patterns; resolve consequential rule conflicts before affected work.
2. Check and reuse an existing linked worktree, or create an isolated task worktree from the primary checkout, under the isolation rules in [PR delivery](references/pr-delivery.md). Implement under `shared/execution.md` for decomposition, delegation, ownership, and integration. Protect pre-existing user edits; an authorized change to a file preserves unrelated edits in that file. A request to remove newly added work does not authorize deleting pre-existing files.
3. Verify the acceptance conditions and plausible regressions using `references/modules/verification/guide.md`. Add automated coverage when a meaningful failure mode needs durable protection and a suitable harness exists, or when requested. Multiple UI steps alone do not require a new end-to-end suite.
4. Read the final diff and working state for correctness, contracts, scope, and unintended changes. Fix issues and recheck affected behavior. For a PR-ready endpoint, complete the repeated review and learning loop in [PR delivery](references/pr-delivery.md), including a fresh final review. Complete the authorized endpoint and report what changed, evidence, and material gaps.

Routine work needs no run directory, HTML matrix, separate test-case approval, blanket full-suite gates, or conventions audit. PR-ready work requires initial and final review passes under its delivery guide, scaled to risk. A direct request to commit or push remains authorization for that endpoint, subject to the repository's own safeguards. Do not re-ask a settled visual or behavior choice merely because implementation has begun.

## Recovery

On `resume`, inspect open runs and saved state. If several match, let the user choose. Re-present only an awaiting or changed decision; retain prior approvals and verification evidence. Recheck the baseline and governing sources before retrying an interrupted stage. A resume reports the recorded blocker and continues authorized work when the blocking condition is resolved; do not invent a new approval gate for recovery.
