# Run state and recovery

Read this when starting or resuming a `fudge:ship` run, and before implementation changes a Git worktree. It holds the mechanics omitted from the main route.

## Run identity and record

Choose a two-to-five-word kebab-case slug. Resolve an unused `.fudge-ship/<YYYY-MM-DD>-<slug>[-N]/` path before writing; append `-2`, `-3`, and so on on collision. Never rename the chosen run. Keep reports, verification output, baselines, and recovery snapshots beneath it. For Git runs, add `.fudge-ship/` to the repository-local exclude file from `git rev-parse --git-path info/exclude` if not already effective. Do not edit `.gitignore` just for run metadata.

`run.json` is the durable index, not a substitute for the artifacts. Record at least the original request, run ID, work-item boundary, selected endpoint, issue/PR mode, active stage, stage/artifact statuses, blocker, and `open | done | abandoned` run status. Save it after every stage, approval, mode change, failure, or resume decision. Finish as `done` at the selected endpoint, when the last stage of an analysis-only route completes, on an accepted "do not build" decision, or when the user explicitly accepts a narrower result. Mark `abandoned` only on explicit abandonment.

For the test gate, save each proposed matrix at an immutable versioned path such as `test-matrix-v1.html`; revisions get new paths. Record the current path, SHA-256, `pending | approved` status, the user's exact response, timestamp, and history of prior versions and responses. Never turn a conditional answer into a Boolean approval. A revision makes the new version pending. Save execution outcomes to a separate results report so the approved matrix remains inspectable. Preserve completed stages and old approvals when a route changes. A single response advances at most one awaiting gate.

For implementation, record the planned touch set and worker ownership, baseline bundle, each verification command with raw output path and exit status, per-case totals, full-diff review path, fix rounds, external exclusions, and any recovery checkpoint. If an older open run uses a different state shape, read its existing keys and artifacts; migrate without inventing an approval or discarding history.

## Protect the worktree

After test approval and before any worker writes code, enumerate the planned touch set. Capture `HEAD`, porcelain status, staged and unstaged binary patches, and content plus SHA-256 for each untracked file in that set. Store this baseline beneath the run; do not snapshot unrelated untracked files. If scope cannot be bounded, or an overlapping untracked file is sensitive, special, or too large to copy safely, pause for a narrower scope, an isolated worktree, or an explicit snapshot policy. A new worktree does not carry uncommitted user changes, so confirm that its starting state includes what the work item needs.

Recheck `HEAD`, status, patches, and relevant untracked hashes immediately before worker dispatch. If they changed, refresh the baseline and classify overlaps before work begins. Keep the original baseline for attribution once implementation starts. Never overwrite, commit, restore, or discard pre-existing user work. If later external edits occur, identify and snapshot them as explicit exclusions with the user's classification; measure the run diff against the original baseline minus only those approved exclusions. If run and external edits overlap inseparably, pause for a narrower scope or isolated worktree rather than guessing ownership.

## Interruption and failure

Before marking implementation or review blocked, save a checkpoint with `HEAD`, status, full staged and unstaged binary patches, relevant untracked hashes, active stage, and blocker. Store its path in `run.json`; leave the run `open`. On plain `resume`, show the blocker and wait. On explicit retry, compare the worktree with the checkpoint. If unchanged, retain the original baseline and retry the blocked stage. If changed, show the deltas and ask which are run work and which are external. Persist snapshots for external changes and require the user to approve that separation before retry. Do not discard the original baseline or rerun a blocked stage against an unexplained worktree.
