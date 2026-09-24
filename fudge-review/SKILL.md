---
name: fudge:review
description: Reviews a PR or diff, then renders the findings in layers (verdict, one-line list, detail) for chat, Slack, GitHub, or an HTML report. Use for "review this PR", "look at this diff", "what do you think of these changes", "re-review after the new commits", or "post the review to Slack/GitHub". Also use to share or re-render findings from an earlier review.
---

# Review

fudge:review reviews a change, verifies every finding itself, stores the result in `findings.json`, and renders it for the chosen medium. The reader sees the verdict first and opens detail only when they want it.

When installed by the Fudge installer, the conventions audit uses the bundled `references/specialists/fudge-conventions/guide.md`. Follow its links relative to that guide. A separate `fudge:conventions` install is not required for this review.

## Modes

| Mode | When | What runs |
|---|---|---|
| standalone | The user asks for a review. Default. | Steps 0 to 8. |
| orchestrated | `fudge:ship` calls this skill. | The two passes below. Ship supplies every path. |
| re-review | A `findings.json` already exists for this branch. | Step 9. |

Orchestrated mode runs in two passes:

1. Candidate pass. The worker inspects the full supplied diff and source scope, plus the raw gate output the root supplies. It returns candidate findings in the `findings.json` finding shape and writes no final output.
2. The root revalidates each candidate and keeps the approved set.
3. Render pass. The worker renders only the approved set to the path ship supplies. It does not add, remove, merge, split, or reclassify findings.
4. The root checks that the rendered output matches the approved set before anyone reports or publishes it.

## Rules for every mode

- A worker's success claim is not evidence. The root re-reads the code behind every finding itself.
- Never report an unverified claim as fact. Tag it SUSPECTED or leave it out.
- Keep pre-existing issues apart from introduced ones. Don't blame the PR for a failure without evidence that it caused it.
- When a correct pattern already exists in the codebase, point the fix at it, and say so when the author wrote it. No generic praise.

## Steps

0. **Mode and size.** Pick the mode. Take the fast path when the diff is at most ~200 changed lines of non-test, non-generated code in one area: one reviewer pass covers every topic. Otherwise take the full path and fan out in step 4.
1. **Intake.** Read the ticket if one is referenced, the PR description, prior review threads, and the author's replies (`gh api repos/<o>/<r>/pulls/<n>/comments`, `gh pr view <n> --json reviews,comments`). Read the repo's rule sources: AGENTS.md, CLAUDE.md, and project conventions skills under `.claude/skills/`. List every prior comment. Each one gets a status in step 4.
2. **Source access, no checkout.** Work from the user's local clone of the PR's repo. If the current directory isn't it, find it or ask for its path. Run `git fetch origin <head-branch>`, then read the PR head from git objects with `git show <sha>:<path>`, `git grep -n <pattern> <sha>`, and `git diff <base>...<sha>`. Never check out, switch branches in, or modify the user's working tree. Don't create worktrees.
3. **CI status, read only.** Don't run builds, tests, or linters. Read `gh pr checks <n>` and put the result in the verdict line. If no checks exist, write "No CI ran". In orchestrated mode, use the gate output ship supplies.
4. **Review.** Cover these topics:
   - correctness and security
   - contracts: API shape, identifiers and columns and config keys shared across repos, deploy order and what breaks in the wrong order
   - conventions: when the repo has rule sources, run `fudge:conventions` in audit mode against them. Each finding cites its rule and source file.
   - tests
   - quality

   On the full path, dispatch parallel read-only reviewer subagents, one per topic, each with a self-contained brief. They return candidates in the finding shape. Mark each prior comment `agree`, `disagree`, or `rebuttal-checked`. For an author's rebuttal, check the reasoning against the code, because rebuttals can be wrong. Record which files were read fully, skimmed, or not read. When the repo can't settle an assumption, such as a third-party payload shape, check external docs. If it's still open, the finding is SUSPECTED.
5. **Verify. Root only, never delegated.** Re-read the lines behind every candidate yourself. Reproduce when it's cheap, by tracing code paths, not by running the app. Mark each finding `verified` and say how, or `suspected`, or drop it. Tag origin `introduced` or `pre-existing`. Tag audience `author` (fix it in this PR) or `team` (a decision for the team, such as amending a convention). Team findings render in their own short section, not in the findings list.
6. **Consolidate.** Merge duplicates across topics. Write `findings.json` and `method.md` to the output location, using the schema in `references/findings.md`. IDs run `R1, R2, …` and are never renumbered. A dropped finding keeps its ID.
7. **Triage, optional.** Run it only when the user asks or a caller requests it. Show the verdict and the one-line list in chat. The user drops, downgrades, or edits findings. Record each change with its reason in `findings.json` (`status: dropped`, `status_reason`). Otherwise go straight to step 8.
8. **Render.** Render from `findings.json` only and leave out dropped findings (see `references/rendering.md`). The medium is an argument: `chat` (the default), `slack`, `pr`, or `html`. Posting to Slack or GitHub is outward-facing. Show the user exactly what will be posted and wait for a yes. After rendering, check the output against `findings.json`: same IDs, same severities, same count.
9. **Re-review.** Load `findings.json`. Review only the commits after the recorded `head` sha, and re-read CI status. Each open finding becomes `fixed`, `open`, or `no-longer-applies`. New findings take the next IDs, with `round_found` set to the new round. Render only the delta: what got fixed, what's still open, what's new.

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

HTML shows severity as pills: filled for blocker, outlined for should-fix, muted outline for nit. The difference in form keeps severity readable in greyscale.

The verdict line:

```
<verdict> — N blockers · N should-fix · N nits · CI: <passed|failed|pending|No CI ran>
```

`<verdict>` is "Needs changes" when any blocker is open, "Mergeable after fixes" when a should-fix is open, and "Mergeable" otherwise.

## Output location

Write this skill's files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

For a PR review, `<branch>` is the PR's head branch name (same `/` → `-` rule), and the working tree is the user's local clone of the PR's repository. Files: `findings.json`, `method.md`, and `review.html` when rendered as HTML.

## References

- `references/findings.md`: the `findings.json` schema, what goes in `method.md`, re-review status rules, and two worked findings. Read it before step 6.
- `references/rendering.md`: depth rules and the chat, Slack, GitHub, and HTML renderers, with examples. Read it before step 8.
- `assets/design-system.md` and `assets/example-review.html`: the HTML design. Build HTML output by copying the example.
