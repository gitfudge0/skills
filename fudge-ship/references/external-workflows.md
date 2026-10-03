# Optional issue and PR workflows

Read this when the work item includes issue tracking, a PR endpoint, or release/deploy, or when operational compatibility is relevant. These choices do not change the routine or comprehensive path selected by `fudge:ship`; each path keeps its own approval and verification requirements.

## Issue tracking

Issue mode is off by default. Select it explicitly and record the tracker, project, and existing issue or authorized new-issue destination. A supplied issue link is context, not permission to edit it. When selected, create or link the scoped work item and update it at meaningful milestones: behavior agreed where needed, implementation verified, PR opened, review or integration complete, and an actionable blocker. Keep updates factual and concise, with artifact or PR links where accessible. Do not post every internal iteration or close a larger release issue because one feature finished. If a tracker field, audience, or ownership is unclear, ask before changing it; log a failed update without pretending it succeeded.

## PR lifecycle

`verified locally` needs no branch, commit, push, or PR unless the user separately requested one. `PR opened` authorizes the in-scope branch, commit, push, and PR creation needed for this work item; it ends with a live PR link and local verification evidence, while pending remote checks are reported as pending. `PR integrated` additionally authorizes following remote checks and review, addressing feedback, seeking required approval, and merging only when the host's rules and the selected destination allow it. Record the target branch and merge method if they matter; ask instead of guessing a consequential choice. Never self-approve, bypass branch protection, or merge with failing required checks. For reviewer feedback that changes agreed behavior, resolve the new decision before related code; update the risk plan when expected behavior or consequential coverage decisions change; version a formal matrix if one is in use.

Use the repository's configured provider and available connector or CLI. Keep commits limited to work-owned files; inspect staged content before each commit so a dirty worktree cannot drag in user changes. Push only the selected branch. Once open, track the PR through checks and review as far as the selected endpoint requires; respond to actionable feedback, implement or delegate in-scope fixes, rerun relevant local checks, push updates, and recheck remote status. If approval, credentials, CI, or policy blocks integration, report the exact blocker and PR link; keep any durable run open. Do not convert a selected `PR opened` endpoint into an automatic merge.

Release/deploy is a separate explicit endpoint. Establish its target and prerequisites, then use the project's release/deployment instructions and checks. A feature may be integrated into a larger release and stop there; do not cut, tag, deploy, or announce a release merely because its feature run is complete. Stop before any irreversible or ambiguous production operation that the selected scope did not settle, and report what remains.

## Operational compatibility and recovery

Read this section when changes affect stored data, shared contracts, or rollout order, even if the endpoint is local verification. Apply only the risks the actual change introduces.

- Check existing rows and old configuration, not only freshly created data. For a migration, establish preconditions, data-preservation invariants, safe reruns, interruption behavior, and recovery. Exercise representative old data in an isolated environment; never use production as a test fixture without explicit authorization.
- Identify readers and writers that may run at different versions: application instances, clients, jobs, webhook handlers, and integrations. Verify compatibility during the transition and name any required deployment order. Use staged expansion/backfill/contraction when the system needs it; do not impose a multi-stage migration on a change that does not.
- For retried or concurrent effects, check the relevant transaction, uniqueness, or idempotency boundary. A request timeout can happen after a successful write; verify whether retry duplicates the effect and how partial work is recovered.
- Choose rollback or forward recovery based on what is actually reversible. Rolling back application code does not undo a data migration or external side effect. Preserve recovery prerequisites; a destructive or irreversible step needs the explicitly authorized scope and adequate recovery evidence.

## Verify delivery

Before deployment, identify the exact artifact/revision, target, configuration prerequisites, required checks, rollout method, recovery action, and evidence that will show success or failure. Use the project's established process. For material production risks, determine stop/rollback conditions and the relevant observation window before executing; do not invent arbitrary metric thresholds or a universal wait duration.

After deployment, observe the deployed revision and relevant critical behavior, health checks, logs or metrics. A deployment command exiting successfully is not proof that the application is healthy. Use the smallest meaningful smoke check against the intended environment and confirm relevant migration/data outcomes. Do not expose secrets in evidence or perform destructive smoke actions.

If observed checks fail, stop further rollout and follow the authorized recovery procedure. Do not retry deployment indefinitely or report completion while readiness is unresolved. If evidence is unavailable or its observation window remains pending, report the exact partial state and next check. Recovery success needs its own observed health evidence. Finish the release/deploy endpoint only when its applicable post-deployment checks have succeeded, or the user explicitly accepts a narrower endpoint with the remaining risk stated.
