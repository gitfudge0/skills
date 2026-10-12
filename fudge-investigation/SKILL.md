---
name: fudge:investigation
description: Explain runtime behavior, causes, or design rationale through bounded read-only investigation, including history and trace forensics when relevant. Use for explanation and diagnosis without requested fixes.
---

# fudge:investigation

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md` unless the manifest declares another source and entry (HTML planning uses `plan/SKILL.md`), root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

## Workflow

Own one named question and its evidence boundary. Inspect governing instructions, the relevant entry point, current runtime flow, owning layer, direct callers and data/external boundaries. Follow dependencies only while they can change the answer; stop when evidence answers the question or further cost exceeds its value. Simple questions need no mandatory multi-agent routine.

Use history, blame, PR discussion or decision records when the question concerns rationale or a regression. Distinguish what current code does from what historical authors intended; missing history is a limit, not permission to invent intent. Cite exact source paths/lines and revisions, and link supplied records when available.

For live or captured trace forensics, first confirm access and a safe read-only collection method. Bound the time window and request/session identity; reduce noise to relevant events, timings and errors, then map signals to source and runtime boundaries. Keep confirmed observations separate from causal hypotheses; identify confounds and the evidence that would confirm or falsify each material hypothesis. Do not claim execution from code inspection or fabricate unavailable traces.

Return the explanation or cause, cited evidence, uncertainty, and the smallest useful next diagnostic step. No unrequested fixes, prototypes, product edits or external writes. Safe local read-only checks may corroborate the answer; do not trigger mutating jobs or live traffic merely to collect evidence.
