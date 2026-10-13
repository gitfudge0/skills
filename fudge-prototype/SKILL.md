---
name: fudge:prototype
description: Build a disposable runnable experiment to answer one interaction, API, algorithm or performance question. Use for exploratory prototypes; production features and refactoring remain in ship.
---

# fudge:prototype

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows. For non-UI experiments, measurement guidance is bundled through engineering and verification; read only those references.

## Workflow

Name one empirical question, the observation that would change the decision, and the bounded experiment. Use minimal machinery and an isolated unused artifact directory under shared artifact guidance (default category `prototype`). Label the artifact exploratory and data synthetic. Keep dependencies, simulated services and state inside the experiment; do not alter production files or lockfiles.

For an interaction experiment, use `references/modules/ui-prototype/guide.md` as the authoritative UI prototype procedure, including its caller path override, transitions, persistence, reset and rendered inspection. Preserve design callers of that module. For API or algorithm experiments, build the smallest runnable harness that exercises the disputed contract or representative inputs; record actual outputs and errors. For performance experiments, use engineering's authoritative `references/modules/engineering/references/performance.md` with verification's measurement rules, without turning exploration into a production optimization.

Provide exact run, reset and cleanup instructions. Run the experiment and observe the decisive cases; identify synthetic behavior, mocks and untested integration. Track any task-owned processes and stop only those unless a running preview is requested. Do not mistake an agent walkthrough for participant research.

Return artifact path, empirical question, observed answer and limitations. Default to artifact only, with no automatic PR, production feature or promotion. A request to promote the experiment is a separately scoped implementation through ship.
