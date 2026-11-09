---
name: fudge:ship-pr
description: Ship a change on a new task branch and raise a verified, reviewed PR for human review. Use when a PR is requested without automatic merging.
---

# fudge:ship-pr

Delivery contract: **`pr-review`**.

Create a fresh task branch using repository naming and commit patterns. Fetch and integrate base changes immediately before raising the PR, then revalidate affected checks and review. Include the merge-risk assessment in the PR description. Stop at PR ready for human review; do not merge.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item reuses its task branch rather than creating a duplicate.
