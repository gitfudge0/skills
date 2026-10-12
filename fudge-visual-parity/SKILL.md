---
name: fudge:visual-parity
description: Verify matched renderings or preserve existing appearance through an implementation change. Use for before/after visual parity; approving a new design belongs to design QA.
---

# fudge:visual-parity

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md` unless the manifest declares another source and entry (HTML planning uses `plan/SKILL.md`), root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

For production-writing work, read `references/modules/engineering/guide.md` for bounded discovery and `references/modules/verification/guide.md` for acceptance and regression evidence. Follow PR delivery adjacent to `references/roots/ship/guide.md` selectively for Git isolation and the selected delivery endpoint. Preserve an explicitly local endpoint; do not invoke the ship router or expand authorization. Analysis and experiments stop at their own endpoint.

## Workflow

Choose audit/verification (read-only) or the explicitly requested implementation/fix endpoint. Establish the exact before and after builds or changed states, fixtures, routes, viewport dimensions, themes and UI states. Preserve existing appearance as the reference; do not silently substitute a new design. Resolve only consequential unsettled intentional differences with the user.

Use `references/modules/design-qa/guide.md` for rendered inspection, evidence and coverage recording; parity adds a controlled before/after comparison rather than new-design approval. Stabilize random seeds, clocks, fixture content, fonts, animation, loading and capture timing where they affect rendering. Record browser/device, scaling and capture tooling. If a baseline or candidate cannot run, mark affected cells NOT TESTED; source inspection cannot establish parity.

Use deterministic image comparison where tooling exists with the same capture conditions. Record the comparison method, configured tolerances, rationale and accepted intentional differences. Inspect meaningful differences as well as numerical results: alignment errors, clipping, content or missing states can be hidden by a summary score. Do not invent a blanket threshold or erase meaningful drift with oversized tolerance. When comparison tooling is absent, qualify manual visual inspection instead of claiming a pixel pass.

Record PASS, FAIL or NOT TESTED for the bounded matrix and retain baseline/candidate captures and meaningful diffs. Pixel similarity does not prove interactions or accessibility; select separate relevant verification only when requested or affected by implementation. Avoid whole-product checks by default. Audit requests do not authorize fixes. For requested implementation, use shared engineering/verification and the chosen delivery endpoint, then recapture affected cells.

Return matched and differing conditions, intentional differences, inspectable evidence and honest untested scope.
