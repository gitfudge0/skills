---
name: fudge:ship-auto
description: "Implement and deliver a change through a task branch and PR, then automatically squash merge into main after required checks and approvals. Use only when the user requests this automatic PR integration endpoint. Opening a PR for human review belongs to fudge:ship-pr; assessing merge safety belongs to merge-risk."
---

# fudge:ship-auto

Delivery contract: **`pr-squash-main`**.

Before implementation, create a fresh task branch using repository naming and commit patterns in a task-owned checkout or linked worktree; leave the original checkout on its existing branch. Resume the same task branch for the same work item. Target main. Fetch and integrate base changes immediately before raising the PR and check freshness again before merging. Include the merge-risk assessment in the PR description. An explicit invocation or user request for automatic merging authorizes scoped commits, push, PR creation and automatic squash merge; implicit skill selection alone does not authorize merging. Do not ask for the same authorization again. Respect required approvals and protections; queued auto-merge is pending, not completion.

Shipping does not authorize local app installation, replacement, restart or relaunch, or host prerequisite installation. Use existing tooling for source checks and builds, and isolated QA apps or CI for application verification, with separate identity, data, configuration and services. If QA is unavailable, report the evidence gap rather than installing locally or claiming merge readiness. Carry this boundary through setup and delegated work; only a separate explicit user request authorizes local installation.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item reuses its task branch rather than creating a duplicate.
