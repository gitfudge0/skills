---
name: fudge:ship
description: Take an idea, issue, feature, story, or task through implementation and delivery at a depth that matches its risk. Use for end-to-end building, "ship this," several fudge skills on one work item, resuming a ship run, or decomposing a system before building. Route standalone code review to fudge:review.
---

# fudge:ship

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md`, root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

Build one work item to its chosen endpoint. A finished feature may be one part of a larger release. Finishing this work never implies that a release was cut.

The user owns expected behavior and scope. The repository's `AGENTS.md`, `CLAUDE.md`, project-level skills, and existing conventions own implementation details. Use decisions and authorization already given in the conversation; ask only when a consequential choice remains unsettled. Do not make architecture or code structure a user approval gate.

## Choose the work and depth

Name the work item and its boundary. Use the endpoint already requested by the user; otherwise default to **verified locally**. Other endpoints are **PR opened**, **PR integrated**, or **release/deploy** when selected. An analysis-only route ends with its requested artifact or decision. Issue tracking is a separate opt-in; a linked issue does not itself authorize updates. Read [external workflows](references/external-workflows.md) before issue, PR, or release/deploy work.

Choose the smallest workflow that gives credible evidence for this change:

- **Routine:** bounded, reversible work with clear behavior and limited blast radius. A focused bug fix, UI change, documentation, or skill edit usually fits, unless its actual consequences warrant comprehensive assurance.
- **Comprehensive:** material security, privacy, financial, permission, migration, data-loss, or production-release risk; broad cross-system changes with unsettled contracts; or an explicit request for a full audit. A small diff can still have high consequences. Follow the comprehensive path below.

Choose reporting and recovery needs separately from engineering risk. Use a concise risk-based plan by default, including for a narrow comprehensive change. Generate a formal HTML matrix only when requested or needed by an established project process. Use durable run state when work spans sessions, has multiple coordinated stages, needs recovery, or the user requests it; higher risk alone does not require HTML or a run directory. An explicit test-plan request selects that capability without automatically adding every comprehensive stage.

An individual uncertainty may warrant one specialist without turning the whole work item into a comprehensive run. If scope or risk grows, switch paths and explain why. Preserve completed decisions and evidence rather than restarting or asking for the same approval again. A user correction narrows or changes the requested work; address that correction directly. For example, “we didn't need new tests” stops unnecessary test work but does not authorize deleting existing tests or other assets.

## Route only the needed stages

Every work item begins with bounded requirements discovery: inspect the request, relevant behavior, dependencies, project instructions, existing checks, and acceptance signals. Determine what is already known, what the repository can settle, and which missing decisions could change the implementation or outcome. Resolve routine choices with existing patterns and bounded judgment. Continue independent work while consequential questions are pending.

Read `references/modules/gap-analysis/guide.md` only when missing or conflicting requirements warrant deeper reconciliation. Retain every valid gap and its evidence; summaries may be shorter than the register. “What is missing before we build?” is an analysis-only request: return the scoped gaps, concrete decisions, and next actions without starting implementation. Clear requests need a small discovery pass, not a workshop.

Use selected guidance only when its output serves this work item:

| Need | Owning skill | Trigger |
|---|---|---|
| Reconcile requirements | `references/modules/gap-analysis/guide.md` | Documents conflict or leave a material gap. |
| Decompose a system | `references/modules/system-decomposition/guide.md` | A broad brief needs responsibilities, contracts, or candidate work before implementation; decomposition-only requests stop at analysis. |
| Pressure-test a decision | `references/modules/decision-room/guide.md` | A consequential choice remains unsettled. |
| Shape the experience | `references/roots/ux/guide.md` | User needs, content structure, task flow, state behavior, or usability needs a decision. |
| Shape the interface | `references/roots/design/guide.md` | Visual expression, UI guidance, a reviewable mock, or component direction is needed. |
| Plan distinct failure cases | `references/modules/test-plan/guide.md` | Risk or an explicit request warrants a separate test plan. |
| Make the project runnable | `references/roots/setup/guide.md` | Dependencies, environment, or startup readiness block implementation or verification; use focused run setup. |
| Implement | `shared/execution.md` | Product or test files will change. |
| Formal review | `references/roots/review/guide.md` | The change is comprehensive or the user requests this review. |

Read each selected skill and honor the contract for the chosen path. A named stage selects membership, not order; UX and design can inform each other in either direction. Use one or both when the task calls for them, carrying settled decisions across the guides without restating their rules. For standalone code review, use the `fudge:review` root without starting a ship run. If that root is unavailable, read package-root `references/roots/review/guide.md` and follow its standalone mode. A pressure-test supplies simulated perspectives and arguments, not independent corroboration. Judge the arguments against evidence; agreement between personas is not stronger evidence. Unknown stage names require clarification. If a required skill is unavailable, report the blocker instead of silently replacing it.

## Routine path

1. Establish acceptance conditions, affected contracts, and the implementation approach using the engineering loop below. Resolve only material uncertainty. Use governing rules and existing patterns; resolve consequential rule conflicts before affected work.
2. Implement under `shared/execution.md`, directly or with cohesive workers when useful and available. Protect pre-existing user edits; an authorized change to a file preserves unrelated edits in that file. A request to remove newly added work does not authorize deleting pre-existing files.
3. Verify the acceptance conditions and plausible regressions using the evidence rules below. Add automated coverage when a meaningful failure mode needs durable protection and a suitable harness exists, or when requested. Multiple UI steps alone do not require a new end-to-end suite.
4. Read the final diff and working state for correctness, contracts, scope, and unintended changes. Fix issues and recheck affected behavior. Complete the authorized endpoint and report what changed, evidence, and material gaps.

Routine work needs no run directory, HTML matrix, separate test-case approval, blanket full-suite gates, two-pass review, or conventions audit. A direct request to commit or push remains authorization for that endpoint, subject to the repository's own safeguards. Do not re-ask a settled visual or behavior choice merely because implementation has begun.

## Engineering loop for both paths

Before editing, trace the changed behavior to its owning layer, direct callers, data readers/writers, and external boundaries. Follow further dependencies only while a relevant contract or failure remains unresolved. Identify invariants that must survive the change: for example tenant isolation, unchanged response compatibility, or one effect per retried event. Use concrete source evidence; do not map unrelated parts of the repository.

Choose the smallest cohesive change that addresses the cause and preserves these contracts. Reuse an existing sound implementation rather than introducing a second mechanism. Consider alternatives when compatibility, maintenance, performance, security, or recovery materially differs. For a narrow task, a brief rationale is enough; broader work may need a short design note. Avoid speculative abstractions and unrelated cleanup. Established patterns inform the choice but do not justify copying a demonstrated defect.

For a bug, establish a reproduction or an evidence-backed hypothesis before changing behavior. Trace why the failure occurs; distinguish the cause from the visible symptom. If reproduction is unavailable, state the limit and identify the evidence that would confirm or falsify the hypothesis. Do not claim an observed reproduction from inspection alone. When adding a regression test, demonstrate that it catches the original defect where feasible, using an isolated baseline or temporary change that preserves user work; then verify the fix and nearby behavior. Fix related occurrences only when they share the proven cause and fall within scope.

## Verification and completion

Connect each material acceptance condition and independently failing risk to an existing test, justified new test, focused manual observation, or explicit unverified gap. Use the cheapest layer that actually exercises the risk. A build proves compilation; it does not prove authorization, persisted data, or a user flow. A mock proves the behavior exercised with that mock, not the external service contract. Observe meaningful success, rejection, and recovery paths where applicable; do not generate every test type by habit.

Run required project gates and risk-relevant checks. Start with focused checks for fast feedback; coordinate expensive suites once when their coverage is needed. Reuse current, attributable worker evidence under `shared/execution.md`; the coordinator reads accessible raw output and owns completion, without rerunning merely to change the operator. Record the command, result, checked revision or file state, and relevant environment; concise work can report this in chat. A later edit invalidates evidence for affected behavior and dependencies. Rerun those checks and retain unaffected evidence with a reason. If the impact cannot be bounded, broaden verification.

Classify a failed check as introduced, pre-existing, infrastructure-blocked, or flaky only with evidence. Compare against an isolated baseline when needed; do not erase user work to establish one. Preserve failure output and investigate before retrying. A later pass does not by itself resolve an unexplained intermittent failure. Fix in-scope defects; report unrelated failures without silently expanding scope or claiming a clean gate.

Finish only when the requested behavior has relevant observed evidence, no known unresolved in-scope material defect remains, and required gates for the endpoint are satisfied. If infrastructure prevents verification, report partial completion and the specific missing evidence. A material unverified risk needs a scoped decision before a consequential external step; prior explicit risk acceptance remains valid. Never describe static review, unrun cases, or accepted risks as a runtime pass. Keep the final answer proportional to the work.

## Comprehensive path

Apply the engineering loop and verification rules above, with deeper coverage of the consequential risks. Before implementation, capture the relevant starting state and planned ownership to distinguish task work from existing edits. Use Git status and scoped diffs in a repository; use bounded file snapshots otherwise. A local implementation does not require initializing Git. When recovery or coordination warrants durable state, read [run state and recovery](references/run-state.md), reserve a unique directory through `shared/artifacts.md`, and record the request, endpoint, decisions, artifacts, evidence, and blockers in `run.json`. Supply chosen artifact paths to selected stages. For UI work, a mock is required only when a visual decision needs to be seen.

Find and load actionable coding rules in project skills, `AGENTS.md`, `CLAUDE.md`, or equivalent sources, and record their paths and revisions. If consequential rules conflict, resolve the conflict before affected code. Offer `fudge:setup` rule setup only when a missing project contract itself blocks the work; creating one requires separate authorization.

Before implementation, use the test-plan module in `plan-only` mode to identify concrete failure cases, observable outcomes, and meaningful gaps. Keep the plan concise unless formal HTML is selected. Resolve unsettled product behavior or consequential coverage tradeoffs; use prior decisions and engineering judgment for settled behavior and routine test selection. A new plan does not create an approval gate. Preserve agreed expected outcomes in any formal version and execution results separately. A behavior decision does not require automating every case.

Implement directly or delegate cohesive work under the shared execution policy. Workers may run targeted checks; coordinate broad gates and reuse valid raw evidence. When tracking cases, mark `PASS`, `FAIL`, or `NOT RUN` from observations with concrete reasons; never infer a pass from code inspection. Fix failures and recheck affected behavior. Evaluate stored-data compatibility, permission boundaries, retries/concurrency, and partial failure where relevant. For migrations or changes requiring coordinated rollout, read the operational guidance in [external workflows](references/external-workflows.md), even when stopping at local verification.

Review the full task diff with `fudge:review` in orchestrated mode, using an independent reviewer when available and useful; otherwise perform a distinct direct review pass. Verify candidate findings against source, diff, agreed behavior, and check output before fixes. Assign the conventions audit once: reuse the review's audit when it covers the current diff and governing sources; call setup in scoped audit mode only for missing coverage. After fixes, revalidate affected behavior, findings, and rules, preserving unaffected coverage. A separate rendering handoff is needed only when the requested output benefits from it. Only an explicitly authorized amendment changes project rules.

Before each push, merge, or finish, confirm that the final task diff and governing sources match the verification and review evidence. Changed content needs affected revalidation; staging unchanged content does not. For a durable run, record the current snapshot and coverage as run state specifies. Finish under the completion rules above and the selected endpoint. Report unrun cases, accepted risks, exceptions, and incomplete external steps plainly.

On `resume`, inspect open runs and saved state. If several match, let the user choose. Re-present only an awaiting or changed decision; retain prior approvals and verification evidence. Recheck the baseline and governing sources before retrying an interrupted stage. A resume reports the recorded blocker and continues authorized work when the blocking condition is resolved; do not invent a new approval gate for recovery.
