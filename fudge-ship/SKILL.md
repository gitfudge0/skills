---
name: fudge:ship
description: Ship a change into the current branch locally. Use for implementation and refactoring without a PR; PR delivery belongs to fudge:ship-pr or fudge:ship-auto.
---

# fudge:ship

Delivery contract: **`merge-current`**.

Capture the current branch and checkout before any isolation. Implement, verify and review, then integrate into that captured branch. Work directly there when requested or appropriate; otherwise integrate a task-owned branch. No push or PR by default. The invocation authorizes scoped commits needed for integration; an explicit no-commit instruction takes precedence.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item reuses its task branch rather than creating a duplicate.
