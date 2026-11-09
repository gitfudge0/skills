---
name: merge-risk
description: "Assess how risky a PR or scoped local change is to merge, using code, verification evidence, blast radius, rollback cost, and production error detection. Use for merge-readiness or rollout-risk questions. This read-only assessment does not merge changes; a full defect review belongs to fudge:review."
---

# Merge risk

Give a concise, evidence-backed assessment of what could go wrong when this change lands. This is read-only analysis, not permission to merge or a substitute for a full code review.

## Scope and evidence

Use package-root `shared/execution.md` for scope and evidence policy and `shared/writing.md` for prose. Package root is the nearest ancestor with `.fudge-package.json`, or `scripts/skill-manifest.json` in source.

- Identify the PR, supplied range or local diff. Record the base and head SHA; for local work include staged, unstaged and nonignored untracked changes and identify the checked working state. Read project rules and the intended behavior from the request, PR description and linked issue when available.
- Read the diff and trace affected callers, contracts and deployment paths far enough to substantiate material risks. Use available forge tools or CLI for PR metadata and current CI. For local work, use local evidence; do not invent PR metadata or call a forge without a PR subject.
- Reuse supplied review and check evidence only when attributable to this change. Distinguish code tracing, observed checks and author claims. CI success alone does not prove the changed behavior.
- Do not change branches, edit code, run builds/tests/the app, merge, publish or post comments. Missing access or evidence becomes an explicit gap. Ask for scope only when it cannot be inferred.

## Assess five dimensions

For each dimension give a short verdict, supporting evidence and any material gap. Link to relevant code, checks or artifacts. Use **unknown** where evidence cannot support a verdict, and **N/A** only with a reason.

| Dimension | Assess |
|---|---|
| Alignment | Does the behavior match the request and issue? Identify undocumented assumptions and unrelated changes. Missing intent is unknown, not proof of misalignment. |
| Impact | Bound affected users, consumers and contracts. Inspect sensitive paths such as authorization, payments, private data, migrations, dependencies and infrastructure regardless of diff size. Distinguish touching a sensitive area from demonstrating an unsafe change. |
| Verification | Does current evidence exercise the changed behavior and plausible failures? Identify coverage gaps. UI changes need relevant rendered or interaction evidence when appearance or flow matters; performance claims need relevant measurements. Select evidence by risk rather than requiring every test type. |
| Rollback cost | Can the change be reversed safely after rollout? Consider persistent writes, destructive migrations, compatibility and deploy order; reverting code may not restore data or consumers. |
| Error detection | Would failures in critical flows be detected promptly? Inspect relevant error propagation, monitoring and alerts when available, including silent fallbacks. Unavailable production configuration is unknown. |

## Overall judgment

Use **low**, **medium**, **high** or **unknown** with the decisive reasons. Do not compute a weighted average: a serious risk cannot be canceled by favourable dimensions.

- **High:** evidence supports a material security, data-loss or production-break risk, or a consequential hard-to-reverse operation lacks a credible recovery path. State the concrete trigger and consequence; sensitive filenames alone do not establish high risk.
- **Medium:** meaningful blast radius, recovery cost or verification/detection gaps warrant precautions, with no demonstrated high-risk condition.
- **Low:** affirmative evidence supports bounded impact, relevant verification and feasible recovery, with no unresolved material risk or gap. Small diff size and green CI alone are insufficient.
- **Unknown:** missing scope or material evidence prevents a defensible overall judgment. State what is missing. A demonstrated high risk remains high even if other dimensions are unknown.

Separate merge risk from approval, CI state and blocking defect findings. Preserve accepted risks as attributed decisions, not evidence that a hazard disappeared. A local assessment describes integration risk, never PR mergeability. If the assessed snapshot changes, revalidate affected conclusions.

## Output

Lead with `Merge risk: <low|medium|high|unknown>` and the decisive reason. Identify the assessed snapshot and CI state (passed, failed, pending, absent or not read). Give one concise line per dimension, expanding only material risks and unknowns into bullets. End with specific evidence or precautions that would reduce risk, when needed. Do not claim checks ran unless observed, or claim approval or merge readiness from this assessment.

Inspired by [Warp's merge-risk skill](https://github.com/warpdotdev/common-skills/blob/main/.agents/skills/merge-risk/SKILL.md), which credits [Matt Pocock's PR skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/pr/SKILL.md). This adaptation uses explicit unknowns and risk overrides instead of numerical scoring.
