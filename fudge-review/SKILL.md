---
name: fudge:review
description: "Review a PR or local diff, re-review changed code, and render or share verified findings. Use for correctness, security, contracts, conventions, and test coverage review."
---

# Review

fudge:review reviews a change, verifies every finding itself, stores the result in `findings.json`, and renders it for the chosen medium. The reader sees the verdict immediately and opens detail only when they want it.

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md`, root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

## Modes

| Mode | When | What runs |
|---|---|---|
| standalone | The user asks for a review. Default. | Steps 0 to 8. |
| orchestrated | A `fudge:ship` run requests review of a scoped change. | Inspect, verify, and consolidate once; chat is the default. Ship supplies artifact paths. |
| re-review | A `findings.json` already exists for this branch. | Step 9. |

In orchestrated mode, inspect the supplied diff, source scope, and current raw gate evidence. A delegated reviewer returns candidate findings in the `findings.json` finding shape; the coordinator verifies and consolidates them into one result. If subagents are unavailable or would add overhead, perform that review directly with the same coverage and verification discipline. Produce chat from the verified result by default. A separate render worker/pass is useful only when a requested artifact warrants it; that renderer must preserve the approved IDs, severity, and content, and the coordinator checks fidelity before reporting or posting.

## Rules for every mode

- A worker's success claim is not evidence. The root re-reads the code behind every finding itself.
- Never report an unverified claim as fact. Tag it SUSPECTED or leave it out.
- Keep pre-existing issues apart from introduced ones. Don't blame the PR for a failure without evidence that it caused it.
- When a correct pattern already exists in the codebase, point the fix at it, and say so when the author wrote it. No generic praise.

## Steps

0. **Mode and review scope.** Pick the mode and assess behavioral risk, affected contracts, and independent review areas. One pass covering all topics is the default for a cohesive change. Use parallel reviewers when independent areas or specialist risks make that faster or more reliable and subagents are available. Line count alone neither mandates fanout nor makes a security or migration change low-risk.
1. **Intake.** Identify a PR, committed range, or local uncommitted change. For a PR, read the ticket if referenced, description, prior review threads, and the author's replies (`gh api repos/<o>/<r>/pulls/<n>/comments`, `gh pr view <n> --json reviews,comments`). Read the repo's rule sources: AGENTS.md, CLAUDE.md, and project conventions skills in the active host or existing project location. For PRs list every prior comment; each gets a status in step 4. For local reviews read the supplied request and governing sources without requesting PR metadata or invoking GitHub.
2. **Source access, no checkout.** For a PR, work from the user's local clone of its repository. If the current directory isn't it, find it or ask for its path. Run `git fetch origin <head-branch>`, then read the PR head from git objects with `git show <sha>:<path>`, `git grep -n <pattern> <sha>`, and `git diff <base>...<sha>`. These PR fetch/object steps do not apply to a local diff. Never check out, switch branches in, or modify the user's working tree. Don't create worktrees.
For a local diff, record the explicit base commit (default current HEAD for uncommitted changes), staged and unstaged patches, and the contents/hashes of in-scope untracked files. Do not omit untracked changes or attribute pre-existing work to this task without evidence. Ask for a comparison range only when intent cannot be inferred. Read current working files without changing them, and store a bounded snapshot of reviewed paths for re-review. For a committed branch review use the supplied base/range. Do not invent PR metadata for a local review.
3. **CI status, read only.** Don't run builds, tests, or linters. For PRs read `gh pr checks <n>` and put the result in the verdict line. Local reviews do not fetch or call GitHub for CI; use `none` unless the caller supplies observed checks for this exact change. If no checks exist, write "No CI ran". In orchestrated mode, use the gate output ship supplies.
4. **Review.** Cover these topics:
   - correctness and security
   - contracts: API shape, identifiers and columns and config keys shared across repos, deploy order and what breaks in the wrong order
   - conventions: when the repo has rule sources, use package-root `references/roots/setup/guide.md` in audit mode against them. Reuse a supplied audit only when its exact reviewed scope, source/rule versions, and attributable evidence match the current change. Revalidate affected rules and files after changes; preserve unaffected evidence. Missing, stale, or ambiguous coverage needs review. Each finding cites its rule and source file.
   - tests
   - quality

   When fanout is justified, dispatch independent read-only reviewer subagents with self-contained scopes and briefs. They return candidates in the finding shape. Otherwise review all applicable topics directly, including on hosts without subagents. Mark each prior comment `agree`, `disagree`, or `rebuttal-checked`. For an author's rebuttal, check the reasoning against the code, because rebuttals can be wrong. Record which files were read fully, skimmed, or not read. When the repo can't settle an assumption, such as a third-party payload shape, check external docs. If it's still open, the finding is SUSPECTED.
5. **Verify. Coordinator or direct reviewer.** Re-read the lines behind every candidate yourself. Reproduce when it's cheap, by tracing code paths, not by running the app. Mark each finding `verified` and say how, or `suspected`, or drop it. Tag origin `introduced` or `pre-existing`. Tag audience `author` (fix it in this PR) or `team` (a decision for the team, such as amending a convention). Team findings render in their own short section, not in the findings list.
6. **Consolidate.** Merge duplicates across topics. Write `findings.json` and `method.md` to the output location, using the schema in `references/findings.md`. IDs run `R1, R2, …` and are never renumbered. A dropped finding keeps its ID.
7. **Triage, optional.** Run it only when the user asks or a caller requests it. Show the verdict and the one-line list in chat. The user drops, downgrades, or edits findings. Record each change with its reason in `findings.json` (`status: dropped`, `status_reason`). Otherwise go straight to step 8.
8. **Render.** Render from `findings.json` only and leave out dropped findings (see `references/rendering.md`). The medium is an argument: `chat` (the default), `slack`, `pr`, or `html`. Posting to Slack or GitHub is outward-facing. If the user already explicitly requested posting to the destination, prepare, verify, and post within that authorization. Otherwise show the exact content and destination and obtain authorization before posting. After rendering, check the output against `findings.json`: same IDs, same severities, same count.
9. **Re-review.** Load `findings.json`. Compare the stored reviewed snapshot with the current scoped change, and re-read CI status. Use commits after the recorded head only if it remains an ancestor and the base/scope are unchanged. After force-pushes, rebases, base changes, or local edits, recompute the full current scoped diff and compare old/new snapshots; reassess existing findings against final code rather than trusting ancestry. If the old object/snapshot is missing, state the limit and perform a full scoped review. Each open finding becomes `fixed`, `open`, or `no-longer-applies`. New findings take the next IDs, with `round_found` set to the new round. Revalidate changed behavior and affected contracts against the current scope; retain prior evidence only where unchanged inputs, sources, and dependencies make it valid. Render only the delta: what got fixed, what's still open, what's new.

## Finding format

Direct, with as few words as the point needs. A finding says how the problem shows up and what causes it.

- **Title.** The symptom, written trigger → result, at most 12 words. The one-line list alone must tell the author what breaks. No code identifiers. Example: "Admin creates staff → no invite arrives; staff can never sign in".
- **Cause.** One clause on what makes it happen. At most 25 words.
- **Impact.** Only when the harm isn't visible in the symptom, such as a privacy exposure. At most 25 words. Omit it otherwise.
- **Fix.** One imperative line. Point at an existing correct pattern in the same codebase when there is one. At most 25 words.
- **Where.** `path:line`. Always last.

Identifiers go in Cause, Fix, or Where, and only when needed. Three tags print by exception: `SUSPECTED` when the finding is unverified, `pre-existing` when the PR didn't introduce it, and the rule citation when the topic is conventions.

## Severity

| Label | Means |
|---|---|
| 🔴 blocker | A security hole, data loss or corruption, or a production break. |
| 🟠 should-fix | A bug users would see, a broken API or cross-repo contract, or a broken repo rule with real consequences. |
| ⚪ nit | Everything else. |

HTML uses the shared HTML plan runtime pills, with explicit severity text. See the HTML design guidance; do not create a separate review skin.

The verdict line:

```
<verdict> — N blockers · N should-fix · N nits · CI: <passed|failed|pending|No CI ran>
```

For a local review, `<verdict>` is "Needs changes" when any actionable author finding is an open blocker or should-fix, and "No blocking findings" otherwise; local reviews never use either mergeable label. For a PR, `<verdict>` is "Needs changes" when any blocker is open, "Mergeable after fixes" when a should-fix is open, and "No blocking findings" otherwise. Use "Mergeable" only for a PR with passing applicable CI and no blocking findings. Failed CI adds "CI failed; readiness unresolved"; pending CI adds "awaiting CI"; absent CI adds "runtime/build checks not verified". A local review never makes a merge-readiness claim. Static verification means the finding was traced in code, not that runtime behavior passed.

## Output location

Use package-root `shared/artifacts.md`, with skill `review` and the PR head branch override for PR reviews. Caller-supplied paths take precedence. Keep `findings.json`, `method.md`, and any snapshot/render together in a unique run directory; re-review explicitly updates that identified review rather than overwriting another run.

## References

- `references/findings.md`: the `findings.json` schema, what goes in `method.md`, re-review status rules, and two worked findings. Read it before step 6.
- `references/rendering.md`: depth rules and the chat, Slack, GitHub, and HTML renderers, with examples. Read it before step 8.
- `assets/design-system.md`, `assets/example-review.src.html`, and generated `assets/example-review.html`: the HTML design using the actual shared HTML plan runtime. Copy the source, replace recorded review content, and pack with the bundled shared runtime.
