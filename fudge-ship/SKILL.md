---
name: fudge:ship
description: Take an idea, issue, feature, story, or task through implementation and delivery at a depth that matches its risk. Use for end-to-end building, "ship this," several fudge skills on one work item, resuming a ship run, or decomposing a system before building. Route standalone code review to fudge:review.
---

# fudge:ship

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

- Delegation and integration: package-root `shared/execution.md`, including the swarm loop (frame completion, dispatch owned slices, drain workers, aggregate evidence) and its model-and-effort-per-stage section where the host allows choosing.
- Project working defaults (endpoint, commit/push, external writes, runtime): `shared/working-defaults.md`. Precedence: this conversation > working defaults > skill defaults.
- Worktrees: [worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination).
- Prose: `shared/writing.md`; review artifacts: `shared/artifacts.md`; a requested durable HTML report: optional `shared/report-deck/guide.md` (concise chat is the default).

Build one work item to its chosen endpoint; finishing a feature never implies a release was cut. The user owns behavior and scope; `AGENTS.md`, `CLAUDE.md`, project skills and conventions own implementation details. Architecture is not a user approval gate. Prior decisions and authorization carry across handoffs; ask only about unsettled consequential choices.

## 1. Classify the request

Do this before choosing depth.

| Request | Route |
|---|---|
| Question or explanation ("what does X do", "what happens if…") | `references/roots/investigation/guide.md`; no ship run |
| Review a PR or diff | `fudge:review`, else `references/roots/review/guide.md` standalone mode; no ship run |
| Issue-tracker work | `references/roots/ticket/guide.md`; no ship run |
| Run locally, manual testing, containers, a one-off task | `references/roots/setup/guide.md` run readiness; no ship run |
| Rebase or restack only | [Restack check](references/pr-delivery.md#restack-check) as its own endpoint |
| Build, fix, refactor or deliver a change | Continue below |

"Pull latest main and <X>" means: run the restack check, then route X. It does not start an implementation run by itself.

## 2. Endpoint and depth

| Endpoint | When |
|---|---|
| Analysis only | Requested; ends with the artifact or decision |
| Verified locally | Requested, or no forge configured |
| PR opened | Requested; stops at creation |
| **PR ready** | Default with a configured forge: pushed PR whose current diff passed the review loop and required checks |
| PR integrated, release/deploy | Explicit selection only; deploy via [external operations](references/external-workflows.md) |

- Use the user's endpoint, else the `endpoint` working default, else the table. Commit, push and external writes follow `commit-push` and `external-writes`; a direct request to commit or push authorizes it, subject to repository safeguards.
- Missing Git, remote, credentials or forge never authorizes initializing or publishing a repository; do the local work and report the unavailable endpoint.
- Issue tracking is a separate opt-in; a linked issue is not permission to update it.
- Read [PR delivery](references/pr-delivery.md) before Git isolation or a PR endpoint.

| Depth | Fits |
|---|---|
| Routine | Bounded, reversible, clear behavior, limited blast radius (focused fix, UI change, docs, skill edit) |
| Comprehensive | Material security, privacy, financial, permission, migration, data-loss or release risk; broad cross-system work with unsettled contracts; a full-audit request. Small diffs can qualify. Read [comprehensive assurance](references/comprehensive.md) before affected work. |

Reporting and recovery are separate from risk:

- Concise risk-based plan by default, even for narrow comprehensive changes. Formal HTML matrix only when requested or required by project process.
- Durable [run state](references/run-state.md) only for multi-session or multi-stage work, recovery, or on request.
- An explicit test-plan request adds that capability, not every comprehensive stage.

Adjusting course: one uncertainty may need one specialist, not a comprehensive run. If scope or risk grows, switch paths, say why, and keep completed decisions and evidence. A user correction narrows the work: "we didn't need new tests" stops new test work but does not authorize deleting existing tests or assets.

## 3. Keep it small

Every concise plan has a **smallest version** line: the minimum change that satisfies the request, and what is deliberately left out.

| Asked for | Over-built | Smallest version |
|---|---|---|
| Add an error-monitoring SDK whose docs show a one-file setup | Custom wrappers and config layers | The vendor's documented minimal setup first |
| A planning tab listing database changes | Rationale, risks and diagrams | Exactly the requested list |
| User stories | Stories split by backend and frontend | User-facing stories; platform splits are subtasks |
| A focused change | New abstractions, extra tests or docs "for completeness" | Leave out; one-line optional follow-up |

## 4. Route stages

Pick specialists from the work itself; never ask the user to choose a skill. Feature work and behavior-preserving refactoring stay in ship (refactoring uses engineering's adjacent reference). A specialist owns its endpoint and does not route back here; bundled dependency cycles are packaging only.

| Focused work | Specialist |
|---|---|
| Explain behavior, cause or rationale without edits | `references/roots/investigation/guide.md` |
| Repair a bounded defect | `references/roots/bug-fix/guide.md` |
| Improve a measured metric within a budget | `references/roots/hillclimb/guide.md` |
| Answer one empirical question with a disposable artifact | `references/roots/prototype/guide.md` |
| Match appearance or verify before/after renderings | `references/roots/visual-parity/guide.md` |
| Create or update tracker issues | `references/roots/ticket/guide.md` |

Every implementation starts with discovery under `references/modules/engineering/guide.md` and ends with observed evidence under `references/modules/verification/guide.md`. Analysis-only work loads only what its artifact needs.

| Need | Guidance | Trigger |
|---|---|---|
| Reconcile requirements | `references/modules/gap-analysis/guide.md` | Material gap or conflict |
| Decompose a system | `references/modules/system-decomposition/guide.md` | Broad brief needs responsibilities or contracts; decomposition-only stops at analysis |
| Pressure-test a decision | `references/modules/decision-room/guide.md` | Consequential choice unsettled |
| Shape the experience | `references/roots/ux/guide.md` | Needs, content, flow, states or usability need a decision |
| Shape the interface | `references/roots/design/guide.md` | Visual direction, UI guidance, a mock or components |
| Interactive plan | `references/modules/plan/guide.md` | HTML plan requested, or a complex multi-file change needs a reviewable tree |
| Plan failure cases | `references/modules/test-plan/guide.md` | Risk or request warrants a test plan |
| Make it runnable | `references/roots/setup/guide.md` | Dependencies, environment, startup or a verification recipe (focused mode) |
| Engineer the change | `references/modules/engineering/guide.md` | Discovery, cause tracing, state modeling, implementation |
| Coordinate implementation | `shared/execution.md` | Product or test files change |
| Verify completion | `references/modules/verification/guide.md` | Any implementation |
| Deliver a PR | [PR delivery](references/pr-delivery.md) | Git isolation or a PR endpoint |
| Restack branches | [Restack check](references/pr-delivery.md#restack-check) | Existing branch before work, before publishing, after a base PR merges, on request |
| Worktree implementation | [Worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination) | Task needs a worktree (Grove preferred, native fallback) |
| Deploy or compatibility | [External operations](references/external-workflows.md) | Explicit deploy, stored data, shared contracts, rollout order |
| Comprehensive assurance | [Comprehensive assurance](references/comprehensive.md) | Comprehensive path |
| Recover durable work | [Run state](references/run-state.md) | Cross-session work, long unattended attempts, recovery |
| Formal review | `references/roots/review/guide.md` | Comprehensive change or request |

- Gap analysis keeps every valid gap with evidence. "What is missing before we build?" is analysis-only: return gaps, decisions and next actions. Clear requests need a small discovery pass, not a workshop.
- A named stage sets membership, not order; UX and design inform each other either way and carry settled decisions across.
- A pressure-test simulates perspectives; judge arguments by evidence, not persona agreement.
- Read each selected guide and honor its contract for the chosen path.
- Unknown stage names need clarification. A missing required skill is a reported blocker, not a silent substitute.

**HTML planning.** Use the bundled guide, runtime, block reference and examples (source `plan/`, installed `references/modules/plan/`); prefer `examples/sample-plan.html` (contents rail, grouped expand/collapse, light/dark switch). Routine clear work stays in a concise plan. For review-before-build, hand over the packed page and wait for the user before affected implementation (existing authorization and settled decisions still apply); planning-only ends with the page.

## 5. Routine path

1. **Frame** acceptance conditions, contracts, approach and the smallest-version line under engineering. Resolve only material uncertainty and consequential rule conflicts. In an existing branch or worktree, run the [restack check](references/pr-delivery.md#restack-check) first.
2. **Implement.** For a worktree task the coordinator reuses a task-owned worktree or creates one, then starts or resumes one main worker there per [worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination): Grove when available, else native `git worktree add` plus the host's subagent (or direct implementation without subagents), telling the user once why Grove was not used. The coordinator owns scope, decisions and independent verification; the worker owns implementation and integration and may delegate within agreed concurrency. A worker loading this skill keeps its role. Non-worktree tasks follow `shared/execution.md`. Authorized edits preserve unrelated user edits in the same file; removing new work never authorizes deleting pre-existing files.
3. **Verify** acceptance and plausible regressions under verification, in Docker when `runtime: docker-only` is set. Add automated coverage only for a meaningful failure mode with a suitable harness, or on request; several UI steps alone do not need a new end-to-end suite.
4. **Review and finish.** Read the final diff for correctness, contracts, scope and stray changes; fix and recheck. For PR ready, run the [review loop](references/pr-delivery.md#review-fix-and-learn) through a fresh final review. Reach the endpoint, [clean up](references/pr-delivery.md#clean-up-after-the-pr-endpoint) task-created resources, and report changes, evidence and gaps.

Routine work needs no run directory, HTML matrix, test-case approval, blanket full-suite gates or conventions audit. Never re-ask a settled visual or behavior choice once implementation starts.

## Recovery

On `resume`: inspect open runs (let the user choose among several), recheck baseline and governing sources before retrying, re-present only awaiting or changed decisions, keep prior approvals and evidence, and continue authorized work once the recorded blocker clears. Recovery adds no approval gate.
