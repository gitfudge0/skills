---
name: fudge:ship
description: "Implement features, refactor code, or complete an agreed change with verification and local integration into the current branch. Use for production implementation without a requested PR. Bounded defect repair belongs to fudge:bug-fix; PR delivery belongs to fudge:ship-pr or fudge:ship-auto."
---

# fudge:ship

Delivery contract: **`merge-current`**.

Capture the current branch and checkout. Implement, verify, review and commit scoped changes directly in that checkout on that branch; do not create a task branch or worktree. A detached HEAD is a blocker until a destination is established. No push or PR by default. The invocation authorizes scoped commits; an explicit no-commit instruction takes precedence.

Shipping does not authorize local app installation, replacement, restart or relaunch, or host prerequisite installation. Use existing tooling for source checks and builds, and isolated QA apps or CI for application verification, with separate identity, data, configuration and services. If QA is unavailable, report the evidence gap rather than installing locally. Carry this boundary through setup and delegated work; only a separate explicit user request authorizes local installation.

Routine source-check dependency setup in task-owned local environments is allowed under the shared shipping guide’s task-local source dependency rules; it does not authorize installing the app or global tooling.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item retains the captured current branch and checkout.
