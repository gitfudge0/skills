# Design QA

Internal capability: enter through the owning public skill. Resolve cross-module and shared paths from the package root (nearest ancestor containing `.fudge-package.json`): `references/modules/<module>/guide.md`, `references/roots/<root>/guide.md`, and `shared/`. In source, use the repository identified by `scripts/skill-manifest.json`, with `modules/`, `fudge-<root>/SKILL.md`, and `shared/`. Local assets and references remain relative to this guide.

Check whether the implemented UI delivers the selected design in the person's actual task. Review the rendered product when it can run. Code inspection can explain a result, but it cannot establish how the interface looks or behaves.

## Choose the endpoint

- **Audit:** inspect the current UI and report observed design gaps, coverage, and limits.
- **Verify:** retest named changes or prior findings against the same source and relevant conditions. Record what passed, failed, or remains untested.
- **Fix:** turn observed gaps into scoped UI changes, then inspect and retest them. Use the shared execution policy for edits and follow the repository's independent verification rules.

## Establish the comparison

1. Identify the person's task and the exact build, route, and environment to inspect. Read project instructions and the selected mock, `DESIGN.md`, `COMPONENTS.md`, or authoritative equivalents. Cite a frame, section, token, or contract for each expected result.
2. Resolve source order from the project's explicit decisions. If a mock, document, and current product disagree, record the conflict and its effect on the task. Ask the design owner for a consequential choice when no source settles it. Do not silently treat the current implementation or the newest file as the chosen design.
3. Select a small coverage matrix for the work's risks. Include every condition the request names, then consider task path, viewport, theme, UI state, content length or shape, and input method for remaining coverage. Include combinations that can change layout or behavior, such as a narrow screen with long labels, or an error after submission. A one-control change needs focused coverage; a new flow needs its critical path and recovery states.

## Inspect and record

Walk the task in the rendered UI. Capture the start, each consequential action and response, and the result. Inspect relevant empty, loading, error, success, and permission states; check responsive layout and visual details against the chosen source. Use browser or device screenshots and logs when available, and identify the environment and viewport. If the product cannot run, produce an inspection plan and mark findings **not observed**. Do not infer a rendered defect from a source diff alone.

For each coverage cell, record the task or screen, condition, expected source, method, and result: **PASS**, **FAIL**, or **NOT TESTED**. Support consequential passes with inspectable observed evidence, such as a screenshot for an affected viewport or theme and an interaction trace for a keyboard or state change. A trivial cell can cite a shared capture rather than repeat it. For a failure, give reproduction steps, expected and observed behavior, user impact, severity, and a screenshot or other inspectable evidence. Severity follows task impact: blocked completion or dangerous misdirection first, then serious friction, then cosmetic drift. Separate a confirmed defect from a design question or a hypothesis. State excluded combinations and why they were lower risk.

When fixing, brief the worker with the selected design source, exact affected files, failing conditions, and acceptance behavior. Inspect the changed UI yourself in each affected condition and rerun relevant project checks. Read the raw results before reporting a pass. If a fix changes the approved contract, update its authoritative document within the authorized scope; do not rewrite the design to excuse a defect.

Return a compact coverage summary, prioritized findings with evidence, unresolved source conflicts, fixes and retest results if requested, and the remaining untested scope. Do not claim overall design approval while a task-blocking failure or consequential source conflict remains.

## Output location

Follow package-root `shared/artifacts.md` for path resolution, caller overrides, collision handling, and repository exclusions. The default artifact category is `design-qa`. Product files retain their established project locations; a chat-only answer creates no artifact.

## Boundaries

Use the accessible-ui module for criterion-level accessibility guidance or audit, including assistive technology results. This QA pass can flag an observed keyboard or focus problem and route it there; it does not make a WCAG conformance claim. Use the ux-research module when the question is whether real people can understand or complete the task. Expert inspection is not participant evidence. If called from `fudge:design` or `fudge:ship`, return findings to that run and preserve its implementation and delivery gates.

## Build and evidence example

Identify the inspected revision/commit, URL or artifact, environment, viewport, theme, and fixture state. For uncommitted code, name the checked worktree and changed state rather than attaching an old commit as if it covered the change.

Example record: “Settings save-error state, local worktree after `<change>`, 390×844 dark theme, failed-response fixture. Screenshot `<path>` shows error copy clipped at the right edge. Expected: complete copy wraps beneath the field. Reproduced in `<browser>`; other browsers untested.” Keep the reference design and observed build separate.
