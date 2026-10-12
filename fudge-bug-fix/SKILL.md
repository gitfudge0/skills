---
name: fudge:bug-fix
description: Diagnose and repair a bounded defect with reproduction, owning-layer cause tracing and relevant regression evidence. Use for requested bug fixes; explanation-only work belongs to investigation.
---

# fudge:bug-fix

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md` unless the manifest declares another source and entry (HTML planning uses `plan/SKILL.md`), root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

For production-writing work, read `references/modules/engineering/guide.md` for bounded discovery and `references/modules/verification/guide.md` for acceptance and regression evidence. Follow PR delivery adjacent to `references/roots/ship/guide.md` selectively for Git isolation and the selected delivery endpoint. Preserve an explicitly local endpoint; do not invoke the ship router or expand authorization. Analysis and experiments stop at their own endpoint.

## Workflow

Establish expected and observed behavior at the actual appropriate boundary: an HTTP request, persisted record, UI action or lowest faithful test layer. Read the engineering guide's authoritative bug diagnosis and regression procedure before editing. Record reproduction inputs, output and environment. If reproduction is unavailable, use an evidence-backed hypothesis with honest limits and a falsifying check; inspection alone is not a reproduced failure.

Trace the owning-layer cause and affected contracts before selecting the smallest cohesive fix. Reuse the engineering procedure for repeated failed fixes: reassess the premise, layer and boundary rather than piling on patches. Fix related occurrences only when they share the demonstrated cause and are in scope.

Use verification and `shared/test-effectiveness.md` for changed tests. Add a cheap meaningful regression when warranted, exercising the original failure rather than asserting implementation wording. Demonstrate that it fails on the defective baseline where feasible without disturbing others' work; verify the fix and relevant neighboring contracts. Record unavailable baseline evidence honestly.

Return the cause, bounded change, actual acceptance/regression results and remaining limits. Complete only the selected production delivery endpoint.
