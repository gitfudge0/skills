---
name: fudge:ship-auto
description: Ship a change on a new task branch, raise a PR and automatically squash merge into main after required checks and approvals. Use when automatic PR integration is requested.
---

# fudge:ship-auto

Delivery contract: **`pr-squash-main`**.

Create a fresh task branch using repository naming and commit patterns. Target main. Fetch and integrate base changes immediately before raising the PR and check freshness again before merging. Include the merge-risk assessment in the PR description. An explicit invocation or user request for automatic merging authorizes scoped commits, push, PR creation and automatic squash merge; implicit skill selection alone does not authorize merging. Do not ask for the same authorization again. Respect required approvals and protections; queued auto-merge is pending, not completion.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item reuses its task branch rather than creating a duplicate.
