---
name: fudge:hillclimb
description: Improve a measured performance metric within a bounded workload, correctness contract and time or cost budget. Use for empirical optimization; preserve behavior and accept no improvement when evidence warrants it.
---

# fudge:hillclimb

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md` unless the manifest declares another source and entry (HTML planning uses `plan/SKILL.md`), root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

For production-writing work, read `references/modules/engineering/guide.md` for bounded discovery and `references/modules/verification/guide.md` for acceptance and regression evidence. Follow PR delivery adjacent to `references/roots/ship/guide.md` selectively for Git isolation and the selected delivery endpoint. Preserve an explicitly local endpoint; do not invoke the ship router or expand authorization. Analysis and experiments stop at their own endpoint.

## Workflow

Before tuning, establish metric, representative workload, correctness constraints, useful target and time/cost boundary from the request or a proportionate explicit proposal. Read the authoritative measured optimization loop at `references/modules/engineering/references/performance.md` and verification's performance evidence rules. That reference owns harness validation, comparable measurements, attributable attempts and stopping conditions; do not create a competing loop.

Identify the observed limiter before choosing a hypothesis. Include completed work and errors in every comparison so faster failures or dropped work cannot win. Record workload, exact revisions or changed-state identity, environment, samples and confounds. Freeze the harness during comparisons or establish a new baseline after changing it.

Keep an attempt log with each hypothesis, attributable delta, correctness results, metric observations and keep/revert decision. Change one explanatory hypothesis at a time, preserving others' edits when reverting. Stop at target, budget or diminishing returns; no minimum attempts or manufactured speedup. Return retained changes, rejected attempts, measurement scope and limitations. Inconclusive results or no improvement are valid outcomes.
