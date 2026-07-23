---
name: testie
description: Analyzes a feature, bug fix, or task and produces a right-sized test plan — specific unit, integration, and e2e test cases, prioritized by risk, delivered as a clean minimal HTML report. Use whenever the user wants to know how to test something they're building or fixing, what test cases to write, what edge cases they're missing, or wants confidence before merging/shipping — even without the phrase "test plan." Triggers include "what should I test for this", "what edge cases am I missing", "write test cases for X", "how would QA approach this", or pasting a diff/PR and asking for a test pass. Produces the plan only, not test code — if the user wants tests implemented, use this to decide what's needed, then write the actual test code separately.
---

# Test Blueprint

A test plan is only as good as the thinking behind it. Most bad test plans fail in one of two directions: too thin (only the happy path, because that's what's easiest to imagine) or too thick (a wall of near-identical cases that pad the count without adding coverage). This skill exists to do the thinking a senior QA engineer does *before* writing a single test — understand what changed, model what it touches, and derive the smallest set of cases that would actually catch the ways this could break — and then hand it back as a report the user can act on.

The output is a plan, not code. Resist the urge to write test implementations, even in pseudocode — the value here is the reasoning trail: what to test, why it matters, and how bad it'd be if it broke.

## Workflow

### 1. Understand what's actually changing

Before generating a single test idea, establish what you're testing. Look for, in order of preference:
- A git diff or set of changed files already in context or in the working directory (`git diff`, `git status`, recently edited files)
- A pasted code snippet, PR description, or ticket
- The user's plain-language description of the feature/bug/task

If none of these give you enough to reason about concretely — you don't know what the change does, what it touches, or who's affected — ask one direct question rather than guessing broadly. Something like "what does this do, and what part of the app does it touch?" is usually enough. Don't interrogate; one good question beats five.

If you have a bug report rather than a feature, identify the actual root cause (or best hypothesis) before planning tests — a regression test aimed at the symptom instead of the cause gives false confidence.

### 2. Map the impact

Before listing test ideas, spend a moment modeling what this actually touches. This is the difference between a generic checklist and a plan specific to this change. Work through, briefly:

- **What does it do** — the core behavior, in one or two sentences.
- **What data does it touch** — inputs, ranges, formats, persistence, anything that flows through it.
- **What does it depend on / what depends on it** — other functions, services, UI state, external APIs, other features that could break if this one changes shape.
- **Who's affected and how** — which users/roles/contexts exercise this, and whether some are higher-stakes than others (e.g. paying users, admins, first-time users mid-onboarding).
- **What's the blast radius if it breaks** — cosmetic annoyance, silent wrong data, crash, data loss, security/permissions leak. This single judgment drives most of the prioritization in step 4.

Keep this to a short paragraph in your own head (and later, in the report) — this isn't a deliverable in itself, it's what makes the test list that follows actually targeted instead of generic.

### 3. Decide which test types actually apply

Don't reach for unit + integration + e2e by default. The shape of the change tells you the shape of the coverage. Use this as a starting signal, then adjust with judgment:

| What changed | Lean toward |
|---|---|
| Pure function, calculation, data transform, isolated logic with no side effects | **Unit-heavy.** Boundary values, invalid input, edge cases. Maybe one integration test to confirm it's wired in correctly — rarely e2e. |
| New/changed API endpoint, service method, or cross-module contract | **Integration-heavy.** Contract correctness, auth/permission checks, error responses, downstream effects. Unit tests for any nontrivial new logic inside it. |
| UI component in isolation, no new user flow | **Unit/component-heavy.** Loading, error, empty, populated states. One integration test if it talks to real state/an API. |
| New or changed user-facing flow spanning multiple steps/screens | **E2E-heavy.** The primary path plus the one or two branches that actually matter (error, alternate route), backed by a couple of integration tests for the trickiest step. Don't unit-test the glue. |
| Bug fix | **Always start with a regression test that reproduces the exact reported failure.** Then boundary tests around the root cause. Then a quick check that nearby passing behavior didn't shift. |
| Refactor with no intended behavior change | The existing suite is the safety net. New tests only for any interface/behavior that actually changed shape — not the whole surface "just in case." |

Most real changes are a mix, but the mix should be lopsided toward whatever layer the risk actually lives in. If you find yourself writing a balanced 5/5/5 split by default, that's a sign you're pattern-matching to "three test types exist" instead of reasoning about this specific change.

### 4. Generate the right cases — not all the cases

Read `references/test-design-heuristics.md` now if you haven't already this session — it has the edge-case checklist, the risk-scoring rubric, and the oracle questions ("how would I actually know this is wrong?") that the rest of this step leans on.

Generate candidate cases per type using those heuristics, then apply this filter before anything goes in the final plan:

- **Every case earns its place.** It should catch a failure mode nothing else in the list catches. If two cases only differ by a value that exercises the same code path (e.g. testing age=17 and age=16 when both just need to hit the "under minimum" branch), merge them into one.
- **Depth matches risk, not enthusiasm.** Critical/high-risk areas (from your step 2 blast-radius judgment) get real coverage — boundaries, invalid input, concurrency if relevant. Low-risk, low-blast-radius areas get one representative case, or get named in the "not covered" section instead of padded out.
- **No case for signal you don't own.** Don't write a case that's really testing the framework, the OS, or a third-party library's internals rather than your code.
- **Rough sizing as a sanity check, not a quota:** a small isolated change is usually well-served by 5–10 cases total; a typical feature by 10–20; a large multi-surface feature can reasonably go higher, but only if you can point to what each additional case catches. If you're past 25 and still going, you're probably vomiting — stop and check the merge rule above.

Before finalizing, do one more pass and ask: if I deleted this case, would anything actually go unverified? If not, cut it.

### 5. Structure each case

Every test case gets:
- **ID** — short, typed prefix (U1, I1, E1, R1 for regression).
- **Title** — one line, states the specific condition being verified, not just the feature name.
- **Type** — unit / integration / e2e / regression.
- **Priority** — Critical / High / Medium / Low, from the risk rubric in the references file.
- **Scenario** — the concrete setup and action. Specific enough that someone could implement it without asking follow-up questions — real-ish values, not "some invalid input."
- **Expected result** — the observable, checkable outcome. If you can't state this concretely, the case isn't ready yet.

### 6. Name what's explicitly out of scope

List anything you deliberately chose not to cover and why — subjective/design judgment calls, things deferred to a separate performance or security pass, third-party code you don't own, pre-existing behavior this change doesn't touch. This is as much a part of the plan as the cases themselves: it tells the reader the gap was a decision, not an oversight.

### 7. Build the HTML report

Read `assets/example.html` for the exact structure, tone, and information density to match, and read `assets/styles.css` for the design system. `assets/example.html` is a fragment — it starts directly at `<title>` and ends after the closing `</script>`, with no `<!doctype>`, `<html>`, `<head>`, or `<body>` wrapper (that's the convention for artifact fragments elsewhere, but it is **not** what you deliver here). Build the final report as a single self-contained, standalone HTML **document**:

- Wrap the content in a proper `<!doctype html><html><head>...</head><body>...</body></html>` shell when you save the file locally — move the `<title>` and inlined `<style>` into `<head>`, and put the `.page` markup, theme-toggle button, and `<script>` in `<body>`. This is required because the file must open correctly as a local file in a browser and via `open <path>`, unlike an artifact fragment that gets wrapped by the artifact host.
- Inline the CSS from `assets/styles.css` into a `<style>` tag in `<head>` (don't link it externally — the file needs to work standalone if emailed, moved, or opened offline).
- Include the full light/dark theme token setup (the `:root` custom properties, the `prefers-color-scheme` media query, and the `:root[data-theme="dark"]`/`[data-theme="light"]` overrides) and the fixed top-right circular sun/moon theme-toggle button with its inline script, exactly as in `assets/example.html` — don't drop the toggle or hardcode a single theme.
- Follow the section order and component patterns in the example: two-line title (line 1 ink, line 2 blue ending with a period), an overview section with strategy paragraphs on the left and a numbered big-numeral bug/feature list on the right, a 4-block stat strip (one inverted accent block), then one `case-table` per test tier (ID | Priority | Test Case | Scenario | Expected columns, uppercase letter-spaced headers over a 2px ink rule, hairline row separators — no boxes or zebra striping), a numbered gaps section (one blue circle for the top item), an out-of-scope numbered list, and a small footer line.
- Apply priority color-coding using the `--pri-critical`/`--pri-high` tokens (with their dark-mode variants) plus the medium (ink) and low (gray) treatments from `styles.css` — Critical gets the colored dot. Case IDs are blue.
- Write real content, not placeholder-style text — the strategy paragraphs and case descriptions should read like a person who actually looked at this change wrote them, not like generic boilerplate ("This feature is important and should be tested thoroughly").
- Keep it visually restrained per the design system — the point is fast scanning (ID, priority, and case title visible per row), not a dense wall of prose.

Do **not** publish the report as an artifact. Save the standalone HTML file locally (name it something like `test-plan-<feature-slug>.html`), then open it in the browser with `open <path>` (macOS) once it's written, and present the file path to the user in your final message — don't paste the full HTML into the chat.
