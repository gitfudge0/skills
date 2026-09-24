---
name: fudge:test-plan
description: Plan distinct failure cases for a feature, bug fix, or task, then execute cases when requested. Use for test plans, edge cases, QA passes, formal pre-code review, or execution; fudge:ship calls it when risk or an explicit request warrants a separate plan.
---

# Test blueprint

A useful plan covers distinct ways the requested behavior could fail. Derive cases from the agreed behavior and the actual system around it. Keep meaningful coverage even when a feature needs many cases; merge only cases that prove the same thing.

The primary output is the plan: what to test, why it matters, and the observable result. A plan is not code or permission to write tests. Approval of expected behavior also does not require an automated test for every case.

## Modes

Choose the mode and format before starting. Use a concise in-chat plan for an ordinary standalone request or a routine `fudge:ship` call. Use the versioned HTML matrix for an explicit formal artifact or a comprehensive `fudge:ship` run. The caller may supply an exact HTML path.

| Mode | Use when | Contract |
|---|---|---|
| `plan-only` | The user asks for cases, edge cases, or testing advice, or a ship run deliberately requests a separate plan. | Complete steps 1–6 at a depth matching risk. Present a concise plan in chat, or complete step 8 for formal HTML. Create no source or test code and run no project commands. In formal HTML, mark cases `NOT RUN` with the reason `PLANNED — awaiting approved execution`. |
| `execute` | The user asks to implement or run the selected cases, or a caller supplies authorization. A formal matrix also requires agreement on its expected behavior and material coverage, which may already be recorded. | Use the selected cases and perform step 7. For a formal matrix, update the HTML results without changing approved expected outcomes. For a concise plan, report observed outcomes in chat. A prior plan alone does not authorize execution. |

A caller may supply the exact output path for a formal HTML report in either mode. When supplied, write the report exactly there, create only its parent directory as needed, and do not also write a default report. Otherwise use the default in Output location below.

## Output location

For an HTML report, write files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix. A concise in-chat plan needs no file or output directory.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

For this skill, `<skill>` is `test-plan`. The default formal HTML report path is `.fudge/<branch>/test-plan/test-plan-<feature-slug>.html`. In standalone formal `execute` mode, update that same file with observed outcomes rather than writing a separate results file. Test files written in `execute` mode are product code and go where the project keeps its tests, not under `.fudge/`.

Under comprehensive `fudge:ship`, split execution responsibility at the command boundary. The worker writes justified test files and reports the targeted commands; the root runs the relevant checks and gates, reads raw output, and supplies observed outcomes. The worker records those outcomes at a separate caller-supplied results path, leaving the approved matrix unchanged. Under routine `fudge:ship`, use `fudge:delegate`'s targeted-check allowance and let the root verify the relevant results. No worker may infer a result.

Under comprehensive `fudge:ship`, the formal matrix records the expected behavior and material coverage decisions. Show its report and a short coverage summary when those decisions still need approval. Reuse explicit decisions already made in the conversation. If implementation changes an expected result or a material coverage decision, revise the matrix and return to that gate before related code proceeds. New implementation details do not reopen the gate.

Outside comprehensive `fudge:ship`, a `fudge:delegate` worker may run the targeted checks named in its brief. The top-level orchestrator verifies results with the checks relevant to the change.

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

Probe the relevant dependency boundary, then stop when it is bounded:
- Search changed functions, symbols, or endpoints for callers when code behavior changes.
- Check other readers or writers when shared data, config, or state changes.
- Check consumers when a response shape or payload changes.
- Check existing rows when a migration or new column changes stored data.
- Check jobs, webhooks, or retries when they touch the same changed record.

See the `Upstream / downstream` section of `references/test-design-heuristics.md` for the fuller prompt list to run these probe findings through.

Every claim in the impact write-up either names a file/symbol you actually looked at, or is explicitly marked as an assumption. No unsourced "this probably affects billing."

**A wider blast radius raises priority, it does not raise case count.** A probe finding earns its own case only when it represents a distinct failure mode — a way this could break that no existing case would catch. Stale-cache-after-write is distinct: the write can be correct while the cache refresh is broken, and they fail independently. "Billing also reads this column" is not distinct — the column is either right or wrong, and an existing case already checks that; it raises that case's priority instead. Step 4's filtering discipline still governs the final list; this step feeds it evidence, not volume.

One pass is enough: follow the direct dependencies you find, don't transitively map the whole repo. If the probe turns up nothing beyond the changed file, say so and move on — that's a valid result, not a failed search.

The output of this step is a short impact paragraph for a formal report, or a brief risk note in a concise plan.

### 3. Decide which test types actually apply

Don't reach for unit + integration + e2e by default. The shape of the change tells you the shape of the coverage. Use this as a starting signal, then adjust with judgment:

| What changed | Lean toward |
|---|---|
| Pure function, calculation, data transform, isolated logic with no side effects | **Unit-heavy.** Boundary values, invalid input, edge cases. Maybe one integration test to confirm it's wired in correctly — rarely e2e. |
| New/changed API endpoint, service method, or cross-module contract | **Integration-heavy.** Contract correctness, auth/permission checks, error responses, downstream effects. Unit tests for any nontrivial new logic inside it. |
| UI component in isolation, no new user flow | **Unit/component-heavy.** Loading, error, empty, populated states. One integration test if it talks to real state/an API. |
| New or changed user-facing flow spanning multiple steps/screens | Use an end-to-end check when the risk crosses a real integration boundary and the harness gives reliable signal. Verify the primary path and distinct high-risk branches at the cheapest effective layer; step count alone is not a reason to create an E2E suite. |
| Bug fix | Prefer a regression test that reproduces the cause when recurrence risk and a stable harness justify it. Otherwise use a focused existing check or manual reproduction, then confirm nearby behavior did not shift. |
| Refactor with no intended behavior change | The existing suite is the safety net. New tests only for any interface/behavior that actually changed shape — not the whole surface "just in case." |

Most real changes are a mix, but the mix should be lopsided toward whatever layer the risk actually lives in. If you find yourself writing a balanced 5/5/5 split by default, that's a sign you're pattern-matching to "three test types exist" instead of reasoning about this specific change.

### 4. Build the case matrix

For a formal matrix or uncertain risk, read `references/test-design-heuristics.md` for its edge-case checklist, risk rubric, and oracle questions ("how would I actually know this is wrong?"). For a concise plan with clear risk, use the distinct failure modes already found.

Generate candidate cases, then check the behavior against the categories that apply: primary success path, boundaries and empty states, malformed or missing input, error and recovery paths, role/permission boundaries, cross-component contracts, state transitions and repeated actions, and regressions. Add concurrency, accessibility, performance, security, or compatibility where material. In a formal matrix, name meaningful exclusions. A concise plan can omit irrelevant categories.

Then apply this filter before anything goes in the final plan:

- **Every case earns its place.** It should catch a failure mode nothing else in the list catches. If two cases only differ by a value that exercises the same code path (e.g. testing age=17 and age=16 when both just need to hit the "under minimum" branch), merge them into one.
- **Depth matches risk, not enthusiasm.** Critical/high-risk areas (from your step 2 blast-radius judgment) get real coverage: boundaries, invalid input, concurrency if relevant. Low-risk areas get representative coverage or a stated exclusion.
- **No case for signal you don't own.** Don't write a case that's really testing the framework, the OS, or a third-party library's internals rather than your code.

Do not stop at a case-count target. A feature with many independent behaviors needs many cases. A small change does not need a padded matrix.

Before finalizing, do one more pass and ask: if I deleted this case, would anything actually go unverified? If not, cut it.

### 5. Structure each case

For a formal matrix, every test case gets:
- **ID** — short, typed prefix (U1, I1, E1, R1 for regression).
- **Title** — one line, states the specific condition being verified, not just the feature name.
- **Type** — unit / integration / e2e / regression.
- **Priority** — Critical / High / Medium / Low, from the risk rubric in the references file.
- **Protects** — the specific dependency or blast-radius finding from step 2 that this case guards (e.g. "billing report reads the same `invoices.status` column"). Omit for cases that only cover the changed code itself.
- **Scenario** — concrete setup and action, including relevant role, state, and real-ish values. Someone should be able to implement it without asking what "invalid input" means.
- **Expected result** — the observable, checkable outcome, including what must remain unchanged after a rejected or interrupted action. If you cannot state this concretely, the case is not ready for approval.
- **Execution** — whether the case is automatable in the available harness, needs manual observation or live infrastructure, or is currently blocked. Name the dependency instead of implying it will run.

For a concise plan, give each distinct case its setup/action, observable result, and why it matters. Add priority or execution notes only where they help the decision.

### 6. Name what's explicitly out of scope

In a formal matrix, list meaningful excluded risks or untestable cases and why, including missing infrastructure and relevant unchanged behavior. Separate "not applicable" from "not covered" and give consequential gaps an impact. In a concise plan, mention only material gaps.

### 7. Execute selected cases and record observed results (`execute` mode only)

In `plan-only` mode, skip this step; continue to step 8 only for formal HTML. In standalone formal `execute` mode, load the approved plan version and run the selected cases. Under comprehensive `fudge:ship`, the worker prepares justified test files and commands while the root runs the relevant checks. Preserve case IDs and expected results from an approved formal version; seek a new decision only if one of those results or material coverage choices changes.

- **Choose evidence for each case.** Use an existing test, a focused manual check, or a new automated test when it offers durable signal for a meaningful failure mode. A planned case does not automatically become a new test file. Cases needing unavailable infrastructure can remain unexecuted with a reason.
- **Run relevant checks and record the real outcome.** In standalone execution, run focused checks and any project gate needed for the risk. Under comprehensive `fudge:ship`, the root runs checks and gives the worker raw outcomes. Under routine `fudge:ship` or other `fudge:delegate` use, workers follow their brief and the root verifies relevant results. A case is **PASS** only after its outcome was observed; **FAIL** if it ran and failed; **NOT RUN** if it could not execute, with a concrete reason. Preserve earlier failure evidence when a later fix passes.
- **Never mark from inference.** "The code obviously handles this" is not a PASS. Record only commands or manual observations whose evidence was read by the person responsible for verification.
- In a formal report, show each case status and a tally. In a concise plan, report only the outcomes and gaps that matter.

For the concise format, finish with the short plan or observed outcomes in chat; do not create an HTML file.

### 8. Build the HTML report (formal format only)

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
