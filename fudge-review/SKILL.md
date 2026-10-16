---
name: fudge:review
description: "Review a PR or local diff, re-review changed code, and render or share verified findings. Use for correctness, security, contracts, conventions, and test coverage review."
---

# Review

fudge:review reviews a change, verifies every finding itself, keeps one structured result, and renders it for the chosen medium. Persist `findings.json`, `method.md` and a bounded snapshot for CI, re-review, requested durable output or a caller requirement; a one-off chat review keeps the same structure in memory and writes no artifacts. The reader sees the verdict first and opens detail only when they want it.

## Locate guidance

Package addresses (`shared/`, `references/modules/`, `references/roots/`) resolve from the nearest ancestor with `.fudge-package.json`, or `scripts/skill-manifest.json` in source. Read `shared/locate.md` when resolving a source address or nested guide; this guide’s own references remain relative.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

## Modes

| Mode | When | What runs |
|---|---|---|
| standalone | The user asks for a review. Default. | Steps 0–8. |
| orchestrated | A `fudge:ship` run requests review of a scoped change. | Steps 0–6 once on ship's diff, scope and gate evidence; chat by default. Ship supplies artifact paths. |
| re-review | The user or caller requests updating an identified prior review. | Step 9. |
| CI | A CI job runs the review on every PR. | Steps 0–9 non-interactively per `references/ci.md`. |

**Orchestrated.** Delegated reviewers return candidates in the finding shape; the coordinator verifies and consolidates one result (or reviews directly, with the same discipline, when subagents are unavailable or add overhead). A separate render pass is only for a requested artifact; it keeps approved IDs, severities and content, and the coordinator checks fidelity before reporting or posting.

## Rules for every mode

- [ ] A worker's success claim is not evidence. The root re-reads the code behind every finding.
- [ ] Never report an unverified claim as fact. Tag it SUSPECTED or leave it out.
- [ ] Keep pre-existing issues apart from introduced ones. Don't blame the change for a failure without evidence it caused it.
- [ ] When a correct pattern exists in the codebase, point the fix at it, and say so when the author wrote it. No generic praise.
- [ ] Static verification means traced in code, not that runtime behavior passed.

## Steps

**0. Mode and scope.** Pick the mode; assess behavioral risk, affected contracts and independent review areas. Default: one pass over all topics for a cohesive change. Fan out to parallel reviewers when independent areas or specialist risks make that faster or more reliable and subagents exist. Line count alone neither mandates fanout nor makes a security or migration change low-risk.

**1. Intake.** Identify a PR, committed range, or local uncommitted change. Read the repo's rule sources: AGENTS.md, CLAUDE.md and project conventions skills (active host or existing project location).
- PR: read the referenced ticket, description, prior review threads and the author's replies (`gh api repos/<o>/<r>/pulls/<n>/comments`, `gh pr view <n> --json reviews,comments`). List every prior comment; each gets a status in step 4.
- Local: read the request and governing sources. Don't request PR metadata or call GitHub.

**2. Source access, no checkout.**

| Subject | Do |
|---|---|
| PR | Work from the user's local clone (find it or ask for its path). `git fetch origin <head-branch>`, then read the head from git objects: `git show <sha>:<path>`, `git grep -n <pattern> <sha>`, `git diff <base>...<sha>`. |
| Local diff | Record the base (default HEAD), staged and unstaged patches, and contents/hashes of in-scope untracked files; capture a bounded snapshot only when persisting the review for later comparison. Ask for a range only when intent can't be inferred. |
| Committed branch | Use the supplied base/range. |

Never check out, switch branches, create worktrees, or modify the user's working tree. Don't omit untracked changes, blame this change for pre-existing work without evidence, or invent PR metadata for a local review. CI mode differs (`references/ci.md`).

**3. CI status, read only.** Don't run builds, tests or linters.
- PR: `gh pr checks <n>`; the result goes in the verdict line. No checks → "No CI ran".
- Local: `none`, unless the caller supplies observed checks for this exact change. Never call GitHub.
- Orchestrated: use the gate output ship supplies.

**4. Review.** Cover every applicable topic:
- [ ] Correctness and security.
- [ ] Contracts: API shape; identifiers, columns and config keys shared across repos; deploy order and what breaks in the wrong order.
- [ ] Conventions: when the repo has rule sources, run package-root `references/roots/setup/guide.md` in audit mode against them. Reuse a supplied audit only when its scope, source/rule versions and attributable evidence match the current change; revalidate affected rules and files after changes and keep unaffected evidence. Missing, stale or ambiguous coverage needs review. Each finding cites its rule and source file.
- [ ] Tests: for changed tests, read package-root `shared/test-effectiveness.md` for a bounded test-oracle check. Separate static reasoning from executed evidence and assess material coverage of the changed contract.
- [ ] Quality.

Then:
- [ ] With justified fanout, dispatch independent read-only reviewers with self-contained scopes and briefs; they return candidates in the finding shape. Otherwise review directly, including on hosts without subagents.
- [ ] Mark each prior comment `agree`, `disagree` or `rebuttal-checked`. Check an author's rebuttal against the code; rebuttals can be wrong.
- [ ] Record files read fully, skimmed and not read.
- [ ] When the repo can't settle an assumption (e.g. a third-party payload shape), check external docs. Still open → SUSPECTED.

**5. Verify** (coordinator or direct reviewer). Re-read the lines behind every candidate. Reproduce when cheap by tracing code paths, not by running the app. Tag each finding:
- confidence: `verified` (say how) or `suspected`, or drop it;
- origin: `introduced` or `pre-existing`;
- audience: `author` (fix in this change) or `team` (a team decision, e.g. amending a convention). Team findings render in their own short section.

**6. Consolidate.** Merge duplicates across topics. Consolidate the structured result and method per `references/findings.md`; persist files only under the persistence rule above. IDs run `R1, R2, …`, remain stable within an identified review, and a dropped finding keeps its ID. A continuity-limited CI full review follows `references/ci.md`.

**7. Triage (optional).** Only when the user or caller asks. Show the verdict and one-line list in chat. Record each drop, downgrade or edit with its reason in the consolidated result (`status: dropped`, `status_reason`). Otherwise go to step 8.

**8. Render.** From the consolidated structured result (persisted as `findings.json` when required), leaving out dropped findings (`references/rendering.md`). Medium: `chat` (default), `slack`, `pr` or `html`.
- [ ] Posting to Slack or GitHub follows the authorization policy in package-root `shared/working-defaults.md`; preserve prior authorization. CI: `references/ci.md`.
- [ ] Check the output against the consolidated result: same IDs, same severities, same count as the consolidated result.

**9. Re-review.** Load `findings.json`, compare the stored snapshot with the current scoped change, and re-read CI status.
- [ ] Use commits after the recorded head only when it's still an ancestor and base/scope are unchanged.
- [ ] After force-pushes, rebases, base changes or local edits, recompute the full scoped diff, compare old/new snapshots, and reassess findings against final code rather than trusting ancestry.
- [ ] Old object/snapshot missing → state the limit and do a full scoped review.
- [ ] Each open finding becomes `fixed`, `open` or `no-longer-applies`. New findings take the next IDs with `round_found` set to the new round.
- [ ] Revalidate changed behavior and affected contracts; keep prior evidence only where inputs, sources and dependencies are unchanged.
- [ ] Render only the delta: fixed, still open, new.

## Finding format

Direct and short: how the problem shows up and what causes it.

| Field | Rule |
|---|---|
| Title | The symptom, trigger → result, ≤12 words, no code identifiers. The one-line list alone tells the author what breaks. E.g. "Admin creates staff → no invite arrives; sign-in remains blocked". |
| Cause | One clause on what makes it happen. ≤25 words. |
| Impact | Only when the harm isn't visible in the symptom (e.g. privacy exposure). ≤25 words. |
| Fix | One imperative line, pointing at an existing correct pattern when there is one. ≤25 words. |
| Where | `path:line`. Always last. |

Identifiers go only in Cause, Fix or Where, and only when needed. Three tags print by exception: `SUSPECTED` (unverified), `pre-existing` (not introduced by the change), and the rule citation (conventions topic).

## Severity and verdict

| Label | Means |
|---|---|
| 🔴 blocker | A security hole, data loss or corruption, or a production break. |
| 🟠 should-fix | A bug users would see, a broken API or cross-repo contract, or a broken repo rule with real consequences. |
| ⚪ nit | Everything else. |

HTML uses the shared HTML plan runtime pills with explicit severity text (see the HTML design guidance); no separate review skin.

```
<verdict> — N blockers · N should-fix · N nits · CI: <passed|failed|pending|No CI ran|CI status not read>
```

| Subject | Verdict |
|---|---|
| Local | "Needs changes" if any actionable author finding is an open blocker or should-fix; else "No blocking findings". Never a mergeable label or merge-readiness claim. |
| PR | "Needs changes" if a blocker is open; "Mergeable after fixes" if a should-fix is open; else "No blocking findings". "Mergeable" only with passing applicable CI and no blocking findings. |

CI qualifiers: failed adds "CI failed; readiness unresolved"; pending adds "awaiting CI"; absent adds "runtime/build checks not verified".

## Output location

When persistence is required, use package-root `shared/artifacts.md` with skill `review` and, for PRs, the head-branch override. Caller-supplied paths win. Keep `findings.json`, `method.md` and any snapshot/render together in a unique run directory; re-review updates that identified review and never overwrites another run.

## References

| File | Holds | Read |
|---|---|---|
| `references/findings.md` | `findings.json` schema, `method.md` contents, re-review status rules, two worked findings | Before step 6 |
| `references/rendering.md` | Depth rules; chat, Slack, GitHub and HTML renderers with examples | Before step 8 |
| `references/ci.md` | CI contract, posting markers, re-run updates | CI mode |
| `assets/ci-review.yml` | Sample GitHub Actions workflow for CI mode | Setting up CI |
| `assets/design-system.md`, `assets/example-review.src.html`, generated `assets/example-review.html` | HTML design on the shared HTML plan runtime. Copy the source, replace the recorded review content, and pack with the bundled shared runtime. | HTML render |
