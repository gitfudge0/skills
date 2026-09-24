---
name: fudge:ship
description: Take an idea, issue, feature, story, or task through a complete software-factory run. Use for end-to-end building, "ship this," several fudge skills on one work item, or resuming a ship run. Route standalone code review through the bundled review guide.
---

# fudge:ship

When installed by the Fudge installer, names such as `fudge:test-plan`, `fudge:review`, and `fudge:design` refer to bundled guides, not separately installed skills. From this root `SKILL.md`, read `references/specialists/fudge-<specialist>/guide.md` for each selected stage or specialist, then follow links relative to that guide. The design guide is bundled so this root works when installed alone. The source skill folders remain available for separate manual installation. Keep every test-case approval, verification, review, and delivery gate below when following a bundled guide.

Build one work item to its chosen endpoint. A finished feature may be one part of a larger release. Finishing this run never implies that a release was cut.

The user owns expected behavior and scope. The repository's `AGENTS.md`, `CLAUDE.md`, project-level skills, and existing conventions own implementation details. Do not make architecture or code structure a user approval gate.

## Choose the run

Name the work item and its boundary. Choose an endpoint before implementation: **verified locally** by default, **PR opened**, **PR integrated**, or **release/deploy** only when explicitly selected. An analysis-only route ends with its requested artifact or decision instead. Issue tracking is a separate opt-in. A linked issue does not by itself authorize updates. State the choices and exclusions to the user; ask only about a choice that would materially change the outcome.

For a new run, create a unique `.fudge/<branch>/ship/<YYYY-MM-DD>-<slug>[-N]/` directory and a durable `run.json`. Keep run artifacts there. Read [run state and recovery](references/run-state.md) when creating or resuming a run, and again before implementation touches a worktree. If the endpoint includes a PR or issue updates, read [external workflows](references/external-workflows.md) before the first external write. Do not create a branch, commit, push, issue, PR, merge, release, or deployment outside the selected mode.

Confirm that an implementation target is a Git repository. Analysis-only work may proceed outside Git. Preserve the original request, chosen endpoint, optional modes, approved behavior, artifact paths, gate response, verification evidence, and blockers in `run.json`.

## Output location

Write this skill's files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

Ship's run directory is `.fudge/<branch>/ship/<run>/`; it supplies run-local paths under that directory to every stage it calls.

## Route

Use only stages that serve this work item, in this order:

| Stage | Owning skill | When it earns its place |
|---|---|---|
| Understand | `fudge:gap-analysis` | A document corpus or conflicting requirements need reconciliation. |
| Decide | `fudge:decision-room` | A consequential product choice remains unsettled. |
| Design | `fudge:design` | UI guidance is needed, or a requested or consequential visual choice needs review. |
| Test cases | `fudge:test-plan` in `plan-only` mode | **Every implementation run.** |
| Implement | `fudge:delegate` | Product or test files will change. |
| Review | `fudge:review` | Every implementation run, unless the user explicitly waives review and accepts the reduced assurance. |

Read each selected skill and honor its output contract. Give `understand` the run-local output root and `decide` an exact run-local HTML path. Before the test-case gate, `design` may return concise guidance with source paths, or call `fudge:ui-mock` in artifact-only mode at an exact run-local HTML path. Choose a mock when the requested or consequential direction needs to be seen; do not require one for every UI task. This stage may not enter `fudge:design` component build, change project design documents, or write product or test code before test-case approval. Give `test-plan` a versioned run-local HTML path. Each stage that produces an artifact renders its own. Do not call `fudge:report-deck` to reformat it. A named stage selects membership, not order. For a standalone code review, read the bundled `references/specialists/fudge-review/guide.md` and follow its standalone mode without starting a ship run; a separately installed `fudge:review` may also be invoked explicitly. Unknown stage names require clarification. If a required skill is unavailable, record a blocker and stop instead of replacing it silently.

Use read-only recon to find the relevant behavior, dependencies, test setup, and project instructions. Put only what later stages need in a short run-local recon note. Ask for a decision or mock review only when the choice cannot be made from the user's brief and repository context. Feedback on either returns to that stage; do not treat the original request as approval of an unseen artifact. A confirmed "do not build" decision ends the run without implementation.

For an implementation run, find and load the governing, actionable coding rules in the project's skills, `AGENTS.md`, `CLAUDE.md`, or equivalent sources; record their paths and revisions. If none are usable, or consequential rules conflict, pause before product or test code and offer `fudge:conventions` setup or a user resolution. Await a separate choice; no endpoint alone authorizes creating or committing a project conventions skill.

## The test-case gate

Before generating **any product or test code**, have `fudge:test-plan` produce a comprehensive, risk-based matrix in `plan-only` mode. This step may write only its run-local report. It may inspect the repository but may not run project commands or edit product or test files. The matrix must make each distinct case reviewable: case ID, concrete setup and action, observable expected result, risk/priority, test type, and what will remain untested with a reason. Cover relevant normal, boundary, failure, permission, integration, lifecycle, and regression behavior without padding the count. Include meaningful manual or environment-dependent cases even if they may later be `NOT RUN`.

Present the matrix as a distinct, prominent artifact and summarize the highest-risk cases and coverage gaps in the message. Ask the user to approve the **expected behavior and test cases**, not the implementation approach. Stop here. Only a later, explicit response to this version approves it. Questions, partial feedback, and conditional answers request a revision; show the revised matrix and ask again. Preserve each version, the exact approval response, and its time in run state.

No implementation worker receives a code-writing brief until that approval is recorded. If implementation or review reveals a new case or changes an approved expected result, revise the matrix, return to this gate, and await approval **before** related product or test code changes. This includes a code fix that would alter agreed behavior. New implementation detail that leaves behavior and coverage unchanged does not reopen the gate.

## Build, verify, review

After approval, establish the worktree baseline and planned ownership before dispatch. Protect dirty or untracked user files as [run state and recovery](references/run-state.md) specifies. Apply `fudge:delegate`: workers own non-overlapping files and follow repository/project instructions for architecture. One worker may invoke `fudge:test-plan` in `execute` mode to write the approved tests. It reports commands but runs no test, build, or lint gate under this skill.

The root orchestrator runs the targeted cases and the relevant full test, build, and lint gates, reads their raw output, and stores commands and output under the run. Give the observed results to the test-plan worker to mark every approved case `PASS`, `FAIL`, or `NOT RUN` with evidence or a reason in a separate results report; keep the approved matrix immutable. Never infer a pass from code inspection. Fix failures in scope, rerun affected and full gates, and update the results report. A failing or high-risk unrun case is not a clean completion; surface the blocker or obtain an explicit user decision about the remaining risk.

Review the full run diff against its protected baseline with `fudge:review` in orchestrated two-pass mode. Supply fresh raw gate output. The review worker returns candidates; the root checks each against source, diff, approved behavior, and evidence; the worker then renders only the approved findings at the run-local review path. Delegate deterministic fixes that preserve approved behavior, rerun verification, update case results, and re-review. Escalate product judgment, inseparable external edits, or a blocker still present after two automatic fix rounds. Never silently accept a finding or change the approved behavior to make a test pass.

Recheck the governing rule sources, then invoke `fudge:conventions` in scoped audit mode over the **full run diff against the protected baseline**, using a run-local report path. The root rechecks its evidence and separates rule violations, ambiguous or uncovered cases, and evidence-backed improvement proposals. Fix in-scope violations through delegation and rerun affected verification, review, and audit; otherwise record an explicit user decision about the exception. Proposals are advisory. Only a separately approved, targeted `fudge:conventions` amendment changes project rules; never rewrite a rule to bless the implementation. Any later run-owned project-file edit, including a PR-feedback edit, invalidates the audit, however small. Run-local metadata and report writes do not.

## Finish or resume

Before each push, merge, or finish, recheck governing source revisions and the exact full run-diff content hash. Resolve a changed rule source and rerun the audit; rerun it whenever the diff hash changed. Finish only when the implementation, approved cases, root-run gates, review, and a current conventions audit meet the selected endpoint. Local completion means a verified work item, not a release. For selected issue or PR work, follow [external workflows](references/external-workflows.md) and record links, checks, feedback, and final state. Report any unrun case, accepted risk, conventions exception or proposal, skipped review, or incomplete external step plainly. Do not label an opened PR as integrated or a merged PR as deployed.

On `resume`, inspect open runs and their saved state. If several match, let the user choose. Re-present an awaiting matrix or other consequential decision; do not infer approval from an old request. Recheck governing convention sources and their revisions. An interrupted implementation, review, or conventions audit needs a fresh baseline/recovery check before retrying. A plain resume reports a recorded blocker; retry only on an explicit corrective instruction. Preserve prior approval history and verification evidence.
