---
name: fudge:ship-pr
description: "Implement and deliver a change on a task branch with verification, review, and a PR for human review. Use when asked to build a feature or prepare existing changes and open a pull request without automatic merging. Reviewing an existing PR belongs to fudge:review; automatic integration belongs to fudge:ship-auto."
---

# fudge:ship-pr

Delivery contract: **`pr-review`**.

Capture the current branch before creating the task branch and use that original branch as the PR base. Before implementation, create a fresh task branch using repository naming and commit patterns in a task-owned checkout or linked worktree; leave the original checkout on its existing branch. Resume the same task branch for the same work item. Fetch and integrate base changes immediately before raising the PR, then revalidate affected checks and review. Include the merge-risk assessment as a visible Markdown section in the PR description, using the shared PR delivery guide’s **PR description format** (overall verdict, five-dimension table, snapshot, CI, gaps and precautions). Stop at PR ready for human review; do not merge. After PR creation and every subsequent push, follow the shared PR delivery guide’s CI wait and repair loop: wait for all triggered CI, diagnose and fix in-scope failures, push and watch the new head until checks succeed, then continue this skill’s endpoint. Pending CI is not completion; report genuine blockers with evidence.

PR delivery does not include installing the changed app locally or replacing, restarting, or relaunching the user’s running app. Run application verification only in isolated QA app instances with separate identity, data, configuration and services. Do not install host runtimes, global tools or dependencies as an implicit prerequisite; use existing tooling, isolated QA environments or CI. If isolation is unavailable, report the verification gap and PR’s actual readiness rather than falling back to the user’s app. Carry this boundary through setup, verification and delegated work; a project install recipe is not authorization to install. A separate explicit user request can authorize local installation.

Load package-root `references/modules/shipping/guide.md` and follow it with this contract. This entry point selects delivery only; the shared module owns discovery, implementation, verification, review and delivery mechanics. Questions, standalone reviews and other nonimplementation work retain the shared router's focused route.

Resolve package addresses from the nearest ancestor containing `.fudge-package.json`, or in source the ancestor containing `scripts/skill-manifest.json`; see `shared/locate.md`. Existing authorization and explicit conversation constraints carry forward. Project endpoint defaults do not override this entry point. Resuming the same work item reuses its task branch rather than creating a duplicate.
