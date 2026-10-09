# Run state and recovery

Read this when a ship run needs durable recovery or coordination, or when resuming an existing run. Routine and comprehensive work can both use it; engineering risk alone does not require a run directory. Without durable state, still inspect the starting files, protect user work, and keep verification attributable to the current change.

## Run identity and record

Read package-root `shared/artifacts.md` and reserve a unique directory with `shared/artifact_path.py --skill ship --name <date-slug> --mkdir --exclude`. Caller-supplied paths take precedence. A run that later creates worktrees keeps its directory where it started. Keep reports, evidence, baselines, and recovery snapshots beneath it.

`run.json` indexes the actual artifacts. Record the request, run ID, work boundary, endpoint, active stage, decisions and authorization, artifacts, evidence, blocker, and `open | done | abandoned` status. For Git/PR work, include canonical worktree root, branch and ownership, starting dirty state, configured target and fetched SHA, published remote head, review rounds and finding dispositions, learning deltas, and pending approval/mergeability conditions. Save at meaningful stage transitions, decisions, failures, and checkpoints. Mark `done` only at the selected endpoint, a completed analysis-only result, or an explicitly accepted narrower result. Mark `abandoned` only on explicit abandonment. An unresolved blocker leaves the run open.

Record actionable governing sources and their revisions or hashes. Resolve consequential conflicts before affected code. Offer setup only if missing rules actually block the work; changing project rules requires its own authorization. On resume, re-read changed sources and apply their authority without inventing approval or discarding prior decisions. Preserve older run records and migrate their shape only as needed.

Keep a concise risk plan and its observed outcomes in the run record or a linked Markdown file unless formal HTML is selected. Record unsettled behavior or consequential coverage decisions, their resolution, and any prior authorization that applies. Do not label an engineering plan as awaiting approval when no user decision is needed. For a formal plan, save immutable versions such as `test-matrix-v1.html`, their hashes, agreed expected outcomes, and decision history. Save results separately. Only changed behavior or a consequential tradeoff reopens its decision; mechanical changes do not.

## Protect the starting state

Before implementation, enumerate the planned touch set and ownership. In Git, record `HEAD`, status, and scoped staged/unstaged binary patches; copy and hash relevant untracked files. Outside Git, snapshot the affected existing files and record missing paths. Capture only what is needed for attribution and recovery; do not copy unrelated or sensitive data. If a necessary snapshot cannot be taken safely, use isolation or resolve a narrower snapshot policy.

Recheck the starting state before dispatch or direct implementation. Classify changed or overlapping paths before writing. Keep the original baseline once implementation begins. Authorized edits can modify files with pre-existing work while preserving unrelated changes. Never discard, commit, or restore another person's edits. A worktree does not carry uncommitted changes, so ensure its starting state includes the inputs the task needs.

Compare the baseline with the current task-owned committed, staged, unstaged, and untracked changes. Include resulting contents, deletions, and relevant file modes; do not let staging or committing unchanged content create a new apparent change. Keep external edits separate with evidence of attribution. Ask only when overlap cannot be resolved reliably; do not require classification approval for clearly unrelated external edits. If ownership is inseparable, pause affected work or isolate it rather than guessing.

## Current evidence and audits

Record each check's command, exit status, raw output or manual observation, environment, checked file state or revision, and the acceptance conditions/risks it covers. Record review findings, dispositions, and any applicable conventions audit with scope, governing-source revisions, and checked snapshot. Evidence from a worker counts under the shared execution policy when governing instructions permit reuse; mandatory coordinator reruns still apply.

Identify snapshots with path/content hashes or an equivalently exact revision plus dirty-file snapshot. Recheck the current task diff and governing sources before push, merge, or finish. A changed snapshot means prior evidence needs impact assessment; it does not require throwing away all earlier coverage. Revalidate changed behavior and dependent contracts. Preserve unaffected evidence only with a stated reason; broaden verification if dependencies cannot be bounded.

Reuse one conventions audit across ship and review. If task content or rule sources change, mark the audit `needs-revalidation`; inspect the delta and changed rules against the full task context. The updated audit can combine retained coverage and new checks when every applicable rule and task change remains covered, recording the new snapshot and source revisions as `current`. If prior scope or authority is unclear, re-audit the full task diff. Run-local report edits and Git metadata-only operations do not invalidate product evidence.

## Interruption and failure

Before stopping at a blocker, save the active stage, blocker, current task diff/snapshot, check outcomes, and next action. In Git, include `HEAD`, status, scoped patches and relevant untracked hashes. Leave the run open.

On resume, read the checkpoint and compare the current files and governing sources. Retain prior authorization and unaffected evidence. Continue already authorized work when the blocker is resolved. Explain material changes; classify external edits from available evidence and ask only about consequential ambiguity or inseparable overlap. Re-present only an awaiting or changed decision. Do not retry against an unexplained overlapping worktree or silently replace the original baseline.
