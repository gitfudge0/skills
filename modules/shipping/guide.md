# Shared shipping workflow

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

- Delegation and integration: package-root `shared/execution.md`, including the swarm loop (frame completion, dispatch owned slices, drain workers, aggregate evidence) and its model-and-effort-per-stage section where the host allows choosing.
- Project working defaults (endpoint, commit/push, external writes, runtime): `shared/working-defaults.md`. Precedence: this conversation > working defaults > skill defaults.
- Worktrees: [worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination).
- Prose: `shared/writing.md`; review artifacts: `shared/artifacts.md`; a requested durable HTML report: `shared/report-deck/guide.md` for the shared plan runtime UI (concise chat is the default).

Build one work item to its chosen endpoint; finishing a feature never implies a release was cut. The user owns behavior and scope; `AGENTS.md`, `CLAUDE.md`, project skills and conventions own implementation details. Architecture is not a user approval gate. Prior decisions and authorization carry across handoffs; ask only about unsettled consequential choices.

## 1. Classify the request

Do this before choosing depth. Preserve the caller’s delivery contract when routing implementation to a specialist.

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

The caller must supply a delivery contract before implementation. Public entry points set it explicitly; this module never selects an endpoint independently or routes back to an entry point. A specialist calling this module retains its own explicitly selected endpoint. Explicit conversation instructions may narrow or override a contract; project endpoint defaults must not silently change a named entry point's outcome.

| Contract | Delivery |
|---|---|
| `merge-current` (`fudge:ship`) | Implement, verify, review and commit directly on the captured current branch and checkout; no new task branch or worktree. No push or PR unless explicitly requested. |
| `pr-review` (`fudge:ship-pr`) | Fresh task branch, verified and reviewed PR against the captured original branch; stop for human review without merging. |
| `pr-squash-current` (`fudge:ship-auto`) | Fresh task branch, PR against the captured original branch, automatic squash merge after required checks and approvals; finish only on confirmed merge. |
| Explicit narrower endpoint | Analysis only, verified locally, or PR opened when requested; report its actual completion conditions. |

- Invoking a PR entry point authorizes scoped commits, push and PR creation. Explicitly invoking the auto entry point (or explicitly requesting automatic merging) also authorizes squash merging that PR into the captured original branch, without another confirmation. Stronger host/repository safeguards still apply. Neither authorizes release/deploy, unrelated writes, or history rewriting. All shipping contracts retain the [shipping verification isolation](references/pr-delivery.md#shipping-verification-isolation) boundary: no implicit local app or host prerequisite installation; application checks use isolated QA apps or CI. Carry it through setup and verification routing.
- Capture the original checkout, branch and HEAD. For PR contracts, create the task branch before implementation; for `merge-current`, work directly in the captured checkout and branch without creating a task branch or worktree. Follow repository branch naming, commit conventions and PR templates.
- Missing Git, remote, credentials, the captured remote base or forge required by the selected endpoint never authorizes initializing, publishing or changing the target. Report the precise unavailable endpoint; never silently fall back to another delivery mode.
- Issue tracking is separate opt-in; a linked issue is not permission to update it.
- Read [delivery](references/pr-delivery.md) before branch integration, Git isolation or a PR endpoint. Release/deploy requires separate explicit selection under [external operations](references/external-workflows.md).

| Depth | Fits |
|---|---|
| Routine | Bounded, reversible, clear behavior, limited blast radius (focused fix, UI change, docs, skill edit) |
| Comprehensive | Material security, privacy, financial, permission, migration, data-loss or release risk; broad cross-system work with unsettled contracts; a full-audit request. Small diffs can qualify. Read [comprehensive assurance](references/comprehensive.md) before affected work. |

Reporting and recovery are separate from risk:

- Concise risk-based plan by default, even for narrow comprehensive changes. Formal HTML matrix only when requested or required by project process.
- Every PR run requires the compact [minimum PR checkpoint](references/run-state.md#minimum-pr-checkpoint); fuller durable run state is for multi-session or multi-stage work, recovery, or on request. Local routine work needs no run directory.
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
| Worktree implementation | [Worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination) | Task needs a worktree |
| Deploy or compatibility | [External operations](references/external-workflows.md) | Explicit deploy, stored data, shared contracts, rollout order |
| Comprehensive assurance | [Comprehensive assurance](references/comprehensive.md) | Comprehensive path |
| Recover durable work | [Run state](references/run-state.md) | Every PR run (minimum checkpoint); cross-session work, long unattended attempts, recovery |
| Formal review | `references/roots/review/guide.md` | Comprehensive change or request |

- Gap analysis keeps every valid gap with evidence. "What is missing before we build?" is analysis-only: return gaps, decisions and next actions. Clear requests need a small discovery pass, not a workshop.
- A named stage sets membership, not order; UX and design inform each other either way and carry settled decisions across.
- A pressure-test simulates perspectives; judge arguments by evidence, not persona agreement.
- Read each selected guide and honor its contract for the chosen path.
- Unknown stage names need clarification. A missing required skill is a reported blocker, not a silent substitute.

**HTML planning.** Use the bundled guide, runtime, block reference and examples (source `plan/`, installed `references/modules/plan/`); prefer `examples/sample-plan.html` (contents rail, grouped expand/collapse, light/dark switch). Routine clear work stays in a concise plan. For review-before-build, hand over the packed page and wait for the user before affected implementation (existing authorization and settled decisions still apply); planning-only ends with the page.

## 5. Routine path

1. **Frame** acceptance conditions, contracts, approach and the smallest-version line under engineering. Resolve only material uncertainty and consequential rule conflicts. For PR work, capture and fetch the selected base before branching; for an existing task branch, use the [restack check](references/pr-delivery.md#restack-check). `merge-current` works directly on the captured branch without task branch or worktree creation and must not rewrite its history.
2. **Implement.** For a worktree task the coordinator reuses a task-owned worktree or creates one, then starts or resumes one main worker there per [worktree coordination](references/pr-delivery.md#worktree-and-worker-coordination): native `git worktree add` plus the host's subagent (or direct implementation without subagents). The coordinator owns scope, decisions and independent verification; the worker owns implementation and integration and may delegate within agreed concurrency. A worker loading this skill keeps its role. Non-worktree tasks follow `shared/execution.md`. Authorized edits preserve unrelated user edits in the same file; removing new work never authorizes deleting pre-existing files.
3. **Verify** acceptance and plausible regressions under verification, in Docker when `runtime: docker-only` is set. Add automated coverage only for a meaningful failure mode with a suitable harness, or on request; several UI steps alone do not need a new end-to-end suite.
4. **Review and finish.** Read the final diff for correctness, contracts, scope and stray changes; fix and recheck. For either PR contract, run the [review loop](references/pr-delivery.md#review-fix-and-learn) through a fresh final review. Reach the endpoint, [clean up](references/pr-delivery.md#clean-up-after-the-pr-endpoint) task-created resources, and report changes, evidence and gaps.

Routine local work needs no run directory; PR work keeps only the required compact checkpoint unless more recovery detail is needed. Routine work needs no HTML matrix, test-case approval, blanket full-suite gates or conventions audit. Never re-ask a settled visual or behavior choice once implementation starts.

## Recovery

On `resume`: inspect open runs (let the user choose among several), recheck baseline and governing sources before retrying, re-present only awaiting or changed decisions, keep prior approvals and evidence, and continue authorized work once the recorded blocker clears. Recovery adds no approval gate.
