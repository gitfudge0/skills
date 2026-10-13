---
name: fudge:hillclimb
description: Improve a measured performance metric within a bounded workload, correctness contract and time or cost budget. Use for empirical optimization; preserve behavior and accept no improvement when evidence warrants it.
---

# fudge:hillclimb

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

For production-writing work, read `references/modules/engineering/guide.md` for bounded discovery and `references/modules/verification/guide.md` for acceptance and regression evidence. Follow PR delivery adjacent to `references/roots/ship/guide.md` selectively for Git isolation and the selected delivery endpoint. Preserve an explicitly local endpoint; do not invoke the ship router or expand authorization. Analysis and experiments stop at their own endpoint.

## Workflow

Before tuning, establish metric, representative workload, correctness constraints, useful target and time/cost boundary from the request or a proportionate explicit proposal. Read the authoritative measured optimization loop at `references/modules/engineering/references/performance.md` and verification's performance evidence rules. That reference owns harness validation, comparable measurements, attributable attempts and stopping conditions; do not create a competing loop.

Identify the observed limiter before choosing a hypothesis. Include completed work and errors in every comparison so faster failures or dropped work cannot win. Record workload, exact revisions or changed-state identity, environment, samples and confounds. Freeze the harness during comparisons or establish a new baseline after changing it.

Keep an attempt log with each hypothesis, attributable delta, correctness results, metric observations and keep/revert decision. Change one explanatory hypothesis at a time, preserving others' edits when reverting. Stop at target, budget or diminishing returns; no minimum attempts or manufactured speedup. Return retained changes, rejected attempts, measurement scope and limitations. Inconclusive results or no improvement are valid outcomes.
