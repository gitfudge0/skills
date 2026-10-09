# External operations

Read this for authorized issue tracking, release/deploy, or operational compatibility. For Git implementation isolation and PR endpoints, use [PR delivery](pr-delivery.md). These choices do not change the routine or comprehensive path selected by `fudge:ship`; each path keeps its own approval and verification requirements.

## Issue tracking

Issue mode is off by default. Select it explicitly and record the tracker, project, and existing issue or authorized new-issue destination. A supplied issue link is context, not permission to edit it. When selected, create or link the scoped work item and update it at meaningful milestones: behavior agreed where needed, implementation verified, PR opened, review or integration complete, and an actionable blocker. Keep updates factual and concise, with artifact or PR links where accessible. Do not post every internal iteration or close a larger release issue because one feature finished. If a tracker field, audience, or ownership is unclear, ask before changing it; log a failed update without pretending it succeeded.

## Release/deploy endpoint

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
