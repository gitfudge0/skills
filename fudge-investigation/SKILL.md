---
name: fudge:investigation
description: Explain runtime behavior, causes, or design rationale through bounded read-only investigation, including history and trace forensics when relevant. Use for explanation and diagnosis without requested fixes.
---

# fudge:investigation

## Locate guidance

Package addresses (`shared/`, `references/modules/`, `references/roots/`) resolve from the nearest ancestor with `.fudge-package.json`, or `scripts/skill-manifest.json` in source. Read `shared/locate.md` when resolving a source address or nested guide; this guide’s own references remain relative.

Use package-root `shared/execution.md` for scope, delegation, authorization and verification; use `shared/writing.md` for prose and `shared/artifacts.md` before writing artifacts. Read only guidance selected by the current task. Bundled roots are dependencies, not instructions to run their workflows.

## Workflow

Own one named question and its evidence boundary. Inspect governing instructions, the relevant entry point, current runtime flow, owning layer, direct callers and data/external boundaries. Follow dependencies only while they can change the answer; stop when evidence answers the question or further cost exceeds its value. Simple questions need no mandatory multi-agent routine.

Use history, blame, PR discussion or decision records when the question concerns rationale or a regression. Distinguish what current code does from what historical authors intended; missing history is a limit, not permission to invent intent. Cite exact source paths/lines and revisions, and link supplied records when available.

For live or captured trace forensics, first confirm access and a safe read-only collection method. Bound the time window and request/session identity; reduce noise to relevant events, timings and errors, then map signals to source and runtime boundaries. Keep confirmed observations separate from causal hypotheses; identify confounds and the evidence that would confirm or falsify each material hypothesis. Do not claim execution from code inspection or fabricate unavailable traces.

Return the explanation or cause, cited evidence, uncertainty, and the smallest useful next diagnostic step. No unrequested fixes, prototypes, product edits or external writes. Safe local read-only checks may corroborate the answer; do not trigger mutating jobs or live traffic merely to collect evidence.
