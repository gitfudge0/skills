---
name: fudge:bug-fix
description: Diagnose and repair a bounded defect with reproduction, owning-layer cause tracing and relevant regression evidence. Use for requested bug fixes; explanation-only work belongs to investigation.
---

# fudge:bug-fix

## Locate guidance

Paths under `references/modules/`, `references/roots/` and `shared/` resolve from the package root: the nearest ancestor containing `.fudge-package.json`, or in a source checkout the ancestor containing `scripts/skill-manifest.json` (mapping in `shared/locate.md`). Links to this guide's own references stay relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

For production-writing work, read `references/modules/engineering/guide.md` for bounded discovery and `references/modules/verification/guide.md` for acceptance and regression evidence. Follow PR delivery adjacent to `references/roots/ship/guide.md` selectively for Git isolation and the selected delivery endpoint. Preserve an explicitly local endpoint; do not invoke the ship router or expand authorization. Analysis and experiments stop at their own endpoint. Read package-root `shared/working-defaults.md` before choosing an endpoint, committing or pushing, starting services, or posting externally.

## Workflow

Read and follow the engineering guide’s authoritative bug diagnosis and regression procedure before editing, then verification’s acceptance and regression evidence rules. Keep the fix bounded to the demonstrated cause and affected contracts; retain explicit reproduction limits. For changed tests, use `shared/test-effectiveness.md`.

Return the cause, bounded change, actual acceptance/regression results and remaining limits. Complete only the selected production delivery endpoint.
