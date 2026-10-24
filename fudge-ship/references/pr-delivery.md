# PR delivery and review learning

Read for Git implementation isolation, a restack, or a PR endpoint. The caller picks scope and depth; this guide owns worktrees, restacking, review learning and PR completion. Delegation and coordinator verification: package-root `shared/execution.md`. Evidence: `references/modules/verification/guide.md`. Project defaults: `shared/working-defaults.md`.

## Worktree isolation

1. Inspect the checkout root, `git rev-parse --git-dir --git-common-dir` and `git worktree list --porcelain`; compare resolved paths (a `.git` file alone does not prove a linked worktree).
2. Record root, branch/HEAD, dirty state and task ownership.
3. Reuse an existing task-owned linked worktree (verify its branch and changes); never nest or duplicate one.
4. Otherwise, from the primary checkout, create a collision-free task branch and worktree per [coordination](#worktree-and-worker-coordination), honoring stronger host or project rules. Record its starting SHA and location.

Protect existing work:

- An occupied branch or unrelated edits never authorize switching, resetting, stashing or discarding.
- New worktrees lack uncommitted changes: transfer only scoped, attributable, non-sensitive inputs already covered by authorization. Never copy credentials or unrelated data.
- Resolve inseparable ownership or missing inputs before affected work; continue independent work.
- No Git repository means bounded local snapshots, not `git init`.
- Keep a worktree while work or review is pending.

### Worktree and worker coordination

| Role | Owns |
|---|---|
| Coordinator (user-facing agent) | Scope, user decisions, launching and observing work, reviewing the integrated diff, rerunning required checks itself before reporting success |
| Main implementation worker (one per task worktree) | Implementation, subtask coordination, integration |

Coordinator check runs do not transfer ownership. A worker that loads ship keeps its assigned role and does not launch another main worker. A worker's claim or task status never establishes success.

**Mechanism.** Create the task worktree with `git worktree add` and run the host's own subagent there as main worker; implement directly if subagents are unavailable. Record the worktree path, branch and base SHA. Roles, endpoint, publishing, verification and cleanup rules do not change when work runs directly.

**Worker prompt** (self-contained UTF-8, written outside worker-owned paths):

- Role, scope, acceptance conditions, owned and off-limits paths, integration duty, preserving others' edits.
- Settled decisions, governing instructions, relevant ship guidance, base SHA, target branch, endpoint with its publishing and cleanup limits.
- Delegation allowance: total concurrency and lane ownership; each extra writing worker gets its own worktree and session via the same mechanism. Read-only subagents may investigate or review; respect host limits and avoid needless recursion.
- Required checks, raw evidence and revisions to return, blockers to report, and the return path (the subagent's final report).

**During the run.** Follow `shared/execution.md` (decomposition, dependency order, one writer per worktree, collect every worker's terminal result). The coordinator keeps consequential decisions and reruns build, test, lint and other required checks on the integrated state. After a failed or ambiguous operation, inspect state before retrying.

## Restack check

Part of ship, run whenever needed. A standalone restack request is its own small endpoint.

**Runs:** before implementation in an existing branch or worktree; before publishing; after a base PR merges; when the user asks to "pull latest main and rebase" (then route the rest of the request).

1. Fetch and record the target's remote SHA.
2. Declare the selected work item’s branch and only the stack branches explicitly necessary to integrate it. Inspect their targets and ownership; order this bounded set base-first. Other branches remain read-only, even if task-owned from earlier work.
3. Rebase only clean, committed, task-owned branches in that declared set, in order onto the fetched SHA of its parent; after a base PR merges, rebase its child onto the target with `git rebase --onto`, dropping merged commits.
4. Resolve conflicts against agreed contracts; inspect the integrated diff.
5. Rerun affected checks and review.
6. Push only with history-rewrite authorization and verified ownership, using `--force-with-lease=<branch>:<expected sha>`, never plain force. A user's request to rebase and push a branch they own counts.
7. Report the new head per branch, the target SHA and any blocker.

Never rewrite a shared or unowned branch; without rewrite authorization, use a permitted non-rewriting integration or report the blocker.

## PR lifecycle and endpoints

| Endpoint | Adds | Ends with |
|---|---|---|
| Verified locally | Nothing published unless requested | Observed evidence |
| PR opened | Scoped branch, commit, push, PR | Live link and accurate pending checks |
| PR ready (default) | Remote checks and repeated review | [Finish conditions](#finish-pr-ready) on the current head |
| PR integrated | Merge when approvals, checks, protection and host rules allow | Merged |

None authorizes release/deploy, self-approval, bypassing protection or changing agreed behavior. Issue updates and external messages are separate opt-ins.

1. Use the configured forge and available connector or CLI.
2. Target: the user's request, repository configuration or stack parent; `main` only if it exists and nothing more specific applies. Record target, remote and branch ownership.
3. Inspect staged content before each commit; commit only task-owned changes.
4. Push only the selected branch; the PR title and description reflect final behavior, verification and limitations.

### Synchronize the target

- Run the [restack check](#restack-check) before publishing and again before declaring readiness.
- Resync on meaningful drift, conflicts or project freshness policy; record the checked target revision and time instead of chasing unrelated commits.
- Separate unrelated baseline failures with evidence; do not fix them silently or call them green.

### Review, fix, and learn

**Passes.** An initial substantive review of the full task diff and a fresh final review of the final diff (including rebase or learning changes). Use independent reviewers when available and useful, else distinct direct passes. Comprehensive changes keep the formal orchestrated `fudge:review` contract; routine PRs get risk-relevant correctness, contracts, security, scope and regression review without formal artifacts. Include existing remote feedback.

**Findings loop.**

1. Verify each candidate finding against source, agreed behavior, governing instructions and raw check output.
2. Fix confirmed actionable in-scope issues, rerun affected checks, push, review again.
3. Dismiss false positives with evidence; label accepted risks, duplicates and out-of-scope items rather than inventing work.
4. Consequential new product decisions go to the user.
5. After repeated failed fixes, reassess the hypothesis. Later reviews get current revisions, prior dispositions and a focus, not the same blind prompt.
6. A clean review needs no manufactured findings or extra rounds.

**Learning from reusable gaps.**

1. Diagnose first with setup's guidance-diagnosis reference (adjacent to `references/roots/setup/guide.md`): missing, buried/conflicting, missed-trigger or noncompliant instructions.
2. Prefer: remove the structural cause > suitable types > a narrow existing-harness check or regression test > residual judgment guidance. Fix the authoritative source or routing; no duplicate rulebooks or generic prose.
3. Record `finding → cause → gate or skill delta → verification`, with a failing and a valid case for any new check.
4. An explicit standing review-learning grant covers additive, evidence-backed changes that keep established behavior; apply via setup's targeted amendment guidance and review the deltas in this PR. Product decisions, weaker gates or policy changes need the user. Without a grant, propose the improvement.

### Finish PR ready

For the pushed current head:

- [ ] Verified initial and fresh final reviews recorded for the full diff, repeated after fixes that affect them.
- [ ] No unresolved confirmed actionable in-scope issues.
- [ ] All required checks green.
- [ ] Local and remote heads agree; checked target SHA reported.

Name pending human approvals or mergeability; never claim approved or mergeable. If credentials, CI or policy block, report the precise partial state, the PR link when available, and keep recovery state. Never merge automatically.

### Clean up after the PR endpoint

After the endpoint (PR opened: on creation; PR ready: after checks and review), clean up only task-created worktrees and designated sessions. Keep pre-existing or reused user resources, anything needed for active review, unresolved work or recovery, and the branch backing the PR.

1. Confirm ownership, that required commits are in the pushed branch, and local/remote head agreement.
2. Inspect uncommitted, relevant untracked and ignored files; preserve dirty or unpushed work and report the blocker.
3. Save evidence and recovery details outside the checkout being removed.
4. Stop only the task's sessions or subagents, after collecting their results.
5. Remove with `git worktree remove <path>` (no `--force` over dirty state), then `git worktree prune`.

Report removed and retained resources and any failures. Cleanup never authorizes extra publishing or deleting unrelated resources.
