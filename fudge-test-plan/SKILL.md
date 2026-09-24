---
name: fudge:test-plan
description: Produces a risk-based test case matrix for a feature, bug fix, or task, then optionally implements and runs an explicitly approved version. Use for test plans, edge cases, QA passes, pre-code test review, or execution of approved cases; fudge:ship uses its plan-only mode before product code.
---

# Test blueprint

A useful plan covers distinct ways the requested behavior could fail. Derive cases from the agreed behavior and the actual system around it, then give the user a concrete matrix they can correct before implementation. Keep meaningful coverage even when a feature needs many cases; merge only cases that prove the same thing.

The primary output is the plan: what to test, why it matters, and the observable result. Execution is a separate mode that consumes the approved plan. A plan is not code or permission to write code.

## Modes

Choose the mode before starting the workflow.

| Mode | Use when | Contract |
|---|---|---|
| `plan-only` | The user asks for cases, edge cases, or testing advice, or an implementation request has no approved case matrix yet. This is the standalone default and the mandatory pre-code mode under `fudge:ship`. | Complete steps 1–6 and 8. Write only the HTML plan. Create no source or test code and run no test, build, lint, or other project commands. Mark every case `NOT RUN` with the reason `PLANNED — awaiting approved execution`. |
| `execute` | The user explicitly approves a specific plan version and asks to write or run its cases, or a caller supplies that approval. | Consume that version, perform step 7, then update the HTML report with observed outcomes. A completed plan or a request to implement unseen cases is not approval. First produce the plan in `plan-only` mode and present it for review. |

A caller may supply the exact output path for the HTML report in either mode. When supplied, write the report exactly there, create only its parent directory as needed, and do not also write a default report. Otherwise use the default in Output location below.

## Output location

Write this skill's files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

For this skill, `<skill>` is `test-plan`. The default HTML report path is `.fudge/<branch>/test-plan/test-plan-<feature-slug>.html`. In standalone `execute` mode, update that same file with observed outcomes rather than writing a separate results file. Test files written in `execute` mode are product code and go where the project keeps its tests, not under `.fudge/`.

Under `fudge:ship`, split execution responsibility at the command boundary. The worker writes the approved test files and reports the exact targeted commands that should run, but runs no test, build, or lint command. The root orchestrator runs those targeted commands and every full gate, reads the raw output, and supplies the observed outcomes. The worker records the supplied outcomes at a separate caller-supplied results path, leaving the approved matrix file unchanged. A worker must not infer a result.

Under `fudge:ship`, the matrix is the user's pre-code acceptance contract. Show its full report and a short coverage summary at the test gate; wait for explicit approval of that version before any product or test code is generated. If implementation exposes a new behavior, changes an expected result, or needs a new case, revise the matrix and return it to that gate before related code proceeds. This amendment rule belongs to `fudge:ship`; standalone planning may be revised without a ship gate.

Outside `fudge:ship`, a `fudge:delegate` worker may run only the targeted checks named in its brief. The top-level orchestrator still owns full gates.

## Workflow

### 1. Understand what's actually changing

Before generating a case, establish what behavior the user expects and what evidence exists. For pre-code work, use the approved scope, acceptance criteria, ticket, mock, and relevant current code. For a change that already exists, use its diff or changed files as well. State assumptions where the requested behavior is still unsettled; ask about any uncertainty that would change an expected result.

If the available material does not reveal what the change does, who uses it, or the result they should see, ask one direct question before inventing cases.

If you have a bug report rather than a feature, identify the actual root cause (or best hypothesis) before planning tests — a regression test aimed at the symptom instead of the cause gives false confidence.

### 2. Trace the blast radius

Before listing test ideas, go find out what this actually touches — don't imagine it. This is the difference between a generic checklist and a plan specific to this change. Answer each of these with evidence:

- **What does it do** — the core behavior, in one or two sentences.
- **What data does it touch** — inputs, ranges, formats, persistence, anything that flows through it.
- **What does it depend on / what depends on it** — other functions, services, UI state, external APIs, other features that could break if this one changes shape.
- **Who's affected and how** — which users/roles/contexts exercise this, and whether some are higher-stakes than others (e.g. paying users, admins, first-time users mid-onboarding).
- **What's the blast radius if it breaks** — cosmetic annoyance, silent wrong data, crash, data loss, security/permissions leak. This single judgment drives most of the prioritization in step 4.

Probe moves — actually do these, don't just think about them:
- Search the changed functions/symbols/endpoints for their callers with `rg`, then open relevant matches.
- Find who else reads or writes the same table, cache key, queue, config value, or feature flag.
- If a response shape or payload changed, search for other consumers of that shape (other endpoints, the frontend client, mobile, exports, webhooks).
- Check migrations and column defaults for existing rows that predate the change — would a null/legacy value break the new logic?
- Look for background jobs, cron, webhooks, or retry logic that touch the same record and could race with or duplicate this change.

See the `Upstream / downstream` section of `references/test-design-heuristics.md` for the fuller prompt list to run these probe findings through.

Every claim in the impact write-up either names a file/symbol you actually looked at, or is explicitly marked as an assumption. No unsourced "this probably affects billing."

**A wider blast radius raises priority, it does not raise case count.** A probe finding earns its own case only when it represents a distinct failure mode — a way this could break that no existing case would catch. Stale-cache-after-write is distinct: the write can be correct while the cache refresh is broken, and they fail independently. "Billing also reads this column" is not distinct — the column is either right or wrong, and an existing case already checks that; it raises that case's priority instead. Step 4's filtering discipline still governs the final list; this step feeds it evidence, not volume.

One pass is enough: follow the direct dependencies you find, don't transitively map the whole repo. If the probe turns up nothing beyond the changed file, say so and move on — that's a valid result, not a failed search.

The output of this step is the short impact paragraph that goes in the report's overview section.

### 3. Decide which test types actually apply

Don't reach for unit + integration + e2e by default. The shape of the change tells you the shape of the coverage. Use this as a starting signal, then adjust with judgment:

| What changed | Lean toward |
|---|---|
| Pure function, calculation, data transform, isolated logic with no side effects | **Unit-heavy.** Boundary values, invalid input, edge cases. Maybe one integration test to confirm it's wired in correctly — rarely e2e. |
| New/changed API endpoint, service method, or cross-module contract | **Integration-heavy.** Contract correctness, auth/permission checks, error responses, downstream effects. Unit tests for any nontrivial new logic inside it. |
| UI component in isolation, no new user flow | **Unit/component-heavy.** Loading, error, empty, populated states. One integration test if it talks to real state/an API. |
| New or changed user-facing flow spanning multiple steps/screens | **E2E-heavy.** Cover the primary path and every distinct high-risk branch, backed by integration tests where a contract could fail independently. Don't unit-test the glue. |
| Bug fix | **Always start with a regression test that reproduces the exact reported failure.** Then boundary tests around the root cause. Then a quick check that nearby passing behavior didn't shift. |
| Refactor with no intended behavior change | The existing suite is the safety net. New tests only for any interface/behavior that actually changed shape — not the whole surface "just in case." |

Most real changes are a mix, but the mix should be lopsided toward whatever layer the risk actually lives in. If you find yourself writing a balanced 5/5/5 split by default, that's a sign you're pattern-matching to "three test types exist" instead of reasoning about this specific change.

### 4. Build the case matrix

Read `references/test-design-heuristics.md` now if you haven't already this session — it has the edge-case checklist, the risk-scoring rubric, and the oracle questions ("how would I actually know this is wrong?") that the rest of this step leans on.

Generate candidate cases, then check the behavior against these categories: primary success path, boundaries and empty states, malformed or missing input, error and recovery paths, role/permission boundaries, cross-component contracts, state transitions and repeated actions, and regressions. Add concurrency, accessibility, performance, security, or compatibility where the change makes them material. For each category, either include its distinct risks or name why it does not apply.

Then apply this filter before anything goes in the final plan:

- **Every case earns its place.** It should catch a failure mode nothing else in the list catches. If two cases only differ by a value that exercises the same code path (e.g. testing age=17 and age=16 when both just need to hit the "under minimum" branch), merge them into one.
- **Depth matches risk, not enthusiasm.** Critical/high-risk areas (from your step 2 blast-radius judgment) get real coverage: boundaries, invalid input, concurrency if relevant. Low-risk areas get representative coverage or a stated exclusion.
- **No case for signal you don't own.** Don't write a case that's really testing the framework, the OS, or a third-party library's internals rather than your code.

Do not stop at a case-count target. A feature with many independent behaviors needs many cases. A small change does not need a padded matrix.

Before finalizing, do one more pass and ask: if I deleted this case, would anything actually go unverified? If not, cut it.

### 5. Structure each case

Every test case gets:
- **ID** — short, typed prefix (U1, I1, E1, R1 for regression).
- **Title** — one line, states the specific condition being verified, not just the feature name.
- **Type** — unit / integration / e2e / regression.
- **Priority** — Critical / High / Medium / Low, from the risk rubric in the references file.
- **Protects** — the specific dependency or blast-radius finding from step 2 that this case guards (e.g. "billing report reads the same `invoices.status` column"). Omit for cases that only cover the changed code itself.
- **Scenario** — concrete setup and action, including relevant role, state, and real-ish values. Someone should be able to implement it without asking what "invalid input" means.
- **Expected result** — the observable, checkable outcome, including what must remain unchanged after a rejected or interrupted action. If you cannot state this concretely, the case is not ready for approval.
- **Execution** — whether the case is automatable in the available harness, needs manual observation or live infrastructure, or is currently blocked. Name the dependency instead of implying it will run.

### 6. Name what's explicitly out of scope

List every meaningful excluded risk or untestable case and why, including deferred performance/security work, missing infrastructure, third-party behavior, and unchanged behavior outside scope. Separate "not applicable" from "not covered." Give each gap an impact so the user can decide whether to accept it.

### 7. Execute approved cases and mark PASS/FAIL (`execute` mode only)

In `plan-only` mode, skip this step and go directly to step 8. In standalone `execute` mode, load the approved plan version and run it. Under `fudge:ship`, the worker prepares test files and commands while the root runs every command. Preserve case IDs and expected results from the approved version; an amendment needs fresh user approval before related code or tests change.

- **Decide where each case can actually run.** Unit/component and most integration cases belong in the repo's existing test framework (vitest, pytest, jest — whatever the project already uses); write them in the appropriate existing test files (or a new file following the repo's naming conventions) next to the code they cover. Cases needing live infrastructure the session can provide (a local DB for a migration round-trip, a dev server) can be run directly. E2E/manual cases with no available harness stay unexecuted.
- **Run everything allowed and record the real outcome.** In standalone execution, run the relevant test files and normal verification gates for the task. Under `fudge:ship`, the worker runs no test, build, or lint commands; it gives the root exact targeted commands and records the root's supplied raw outcomes. Under other `fudge:delegate` use, the worker follows its brief and the top-level orchestrator runs full gates. A case is **PASS** only after its assertion was observed passing; **FAIL** if it ran and failed, with a pointer to the raw failure; **NOT RUN** if it could not execute, with a concrete reason. If a later authorized fix makes a failed case pass, keep the earlier failure evidence in the run history and report the latest observed result.
- **Never mark from inference.** "The code obviously handles this" is not a PASS. In standalone execution, record only commands whose raw output you read. Under `fudge:ship`, record only the fresh raw outcomes supplied by the root; do not rerun or reinterpret them.
- Statuses go in the report (step 8) as a Status badge per case row, and the stat strip should reflect the tally (test cases / passed / failed / not run).

### 8. Build the HTML report

Read `assets/example.html` for the exact structure, tone, and information density to match, and read `assets/styles.css` for the design system. `assets/example.html` is a fragment — it starts directly at `<title>` and ends after the closing `</script>`, with no `<!doctype>`, `<html>`, `<head>`, or `<body>` wrapper (that's the convention for artifact fragments elsewhere, but it is **not** what you deliver here). Build the final report as a single self-contained, standalone HTML **document**:

- Wrap the content in a proper `<!doctype html><html><head>...</head><body>...</body></html>` shell when you save the file locally — move the `<title>` and inlined `<style>` into `<head>`, and put the `.page` markup, theme-toggle button, and `<script>` in `<body>`. This is required because the file must open correctly as a local file in a browser and via `open <path>`, unlike an artifact fragment that gets wrapped by the artifact host.
- Inline the CSS from `assets/styles.css` into a `<style>` tag in `<head>` (don't link it externally — the file needs to work standalone if emailed, moved, or opened offline).
- Include the full light/dark theme token setup (the `:root` custom properties, the `prefers-color-scheme` media query, and the `:root[data-theme="dark"]`/`[data-theme="light"]` overrides) and the fixed top-right circular sun/moon theme-toggle button with its inline script, exactly as in `assets/example.html` — don't drop the toggle or hardcode a single theme.
- Follow the section order and component patterns in the example: two-line title (line 1 ink, line 2 blue ending with a period), an overview section with strategy paragraphs on the left and a numbered big-numeral bug/feature list on the right, a 4-block stat strip (Test cases | Passed | Failed | Not run, accent block inverted on Passed), then one `case-table` per test tier (six columns — ID | Priority | Test Case | Scenario | Expected | Status — uppercase letter-spaced headers over a 2px ink rule, hairline row separators — no boxes or zebra striping), a numbered gaps section (one blue circle for the top item), an out-of-scope numbered list, and a small footer line. In plan-only mode, title or subtitle the report "Test case matrix" and show a version (`v1`, `v2`, etc.) so the user can approve an exact revision.
- Apply priority color-coding using the `--pri-critical`/`--pri-high` tokens (with their dark-mode variants) plus the medium (ink) and low (gray) treatments from `styles.css` — Critical gets the colored dot. Case IDs are blue. The tier heading and typed ID make each case's type explicit; never mix types in a tier. Protects and Execution are not columns. Render them inside the Scenario cell as smaller gray lines below the setup/action; omit Protects when it does not apply.
- Render Status as a compact uppercase badge per row: **PASS** in green (`--status-pass: #1a7f37` light, `#3fb950` dark), **FAIL** reusing the `--pri-critical` red with the colored dot treatment, **NOT RUN** in the low/gray treatment with its one-line reason in smaller text beneath. FAIL rows should also carry a one-line pointer to the failing output or the bug it exposed.
- In `plan-only` mode, every Status badge is **NOT RUN** and its reason is `PLANNED — awaiting approved execution`; the stat strip therefore reports zero passed, zero failed, and every planned case as not run.
- In the overview, summarize which coverage categories apply and which do not. Make the matrix the report's main event, not a footnote to implementation notes. Give excluded risks and blocked cases enough detail for the user to accept or challenge them.
- Write real content, not placeholder-style text — the strategy paragraphs and case descriptions should read like a person who actually looked at this change wrote them, not like generic boilerplate ("This feature is important and should be tested thoroughly").
- Keep it visually restrained per the design system — the point is fast scanning (ID, priority, and case title visible per row), not a dense wall of prose.

Do **not** publish the report as an artifact. If no output-path override was supplied, save the standalone HTML file locally at the default in Output location above (`.fudge/<branch>/test-plan/test-plan-<feature-slug>.html`). Open the resolved path in the browser with `open <path>` (macOS) once it's written, and present that path to the user in your final message — don't paste the full HTML into the chat.
