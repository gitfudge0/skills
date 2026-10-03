# Test blueprint

Internal capability: enter through the owning public skill. Resolve cross-module and shared paths from the package root (nearest ancestor containing `.fudge-package.json`): `references/modules/<module>/guide.md`, `references/roots/<root>/guide.md`, and `shared/`. In source, use the repository identified by `scripts/skill-manifest.json`, with `modules/`, `fudge-<root>/SKILL.md`, and `shared/`. Local assets and references remain relative to this guide.

A useful plan covers distinct ways the requested behavior could fail. Derive cases from the agreed behavior and the actual system around it. Keep meaningful coverage even when a feature needs many cases; merge only cases that prove the same thing.

The primary output is the plan: what to test, why it matters, and the observable result. A plan is not code or permission to write tests. Approval of expected behavior also does not require an automated test for every case.

## Modes

Choose the mode and format before starting. Use a concise risk-based plan by default, including comprehensive `fudge:ship` work. Use a versioned HTML matrix when the user or caller requests a formal artifact, or an established reporting requirement needs it. Engineering risk determines coverage; it does not determine presentation format. The caller may supply an exact HTML path.

| Mode | Use when | Contract |
|---|---|---|
| `plan-only` | The user asks for cases, edge cases, or testing advice, or a ship run deliberately requests a separate plan. | Complete steps 1–6 at a depth matching risk. Present a concise plan in chat, or complete step 8 for formal HTML. Create no source or test code and run no project commands. In formal HTML, mark cases `NOT RUN` with the reason `PLANNED — not executed`; identify a pending decision only if one actually remains. |
| `execute` | The user asks to implement or run the selected cases, or an authorized caller supplies them. Resolve unsettled expected behavior or consequential coverage decisions, using prior authorization where applicable; a formal format does not create a new gate. | Use the selected cases and perform step 7. For a formal matrix, update results without changing agreed outcomes; a ship run keeps its immutable plan and results separate. For a concise plan, report observations in chat. A standalone plan-only request does not authorize execution; an existing implementation request can. |

A caller may supply the exact output path for a formal HTML report in either mode. When supplied, write the report exactly there, create only its parent directory as needed, and do not also write a default report. Otherwise use the default in Output location below.

## Output location

Follow package-root `shared/artifacts.md` for path resolution, caller overrides, collision handling, and repository exclusions. The default artifact category is `test-plan`. Product files retain their established project locations; a chat-only answer creates no artifact.

For delegated execution, follow package-root `shared/execution.md`. Assign each check an owner. Workers may write justified test files and run the targeted checks in their brief; the coordinator owns any remaining gates and verifies accessible raw evidence against the current revision, environment, and scope. Reuse sufficient current evidence rather than repeating an identical command merely to change its runner. Rerun checks whose coverage was invalidated by later changes, and preserve unaffected evidence. Without subagents, perform the same bounded work directly. Never infer an observed result.

When a formal plan has agreed expected behavior and material coverage, preserve that version and record execution at a separate caller-supplied results path. Show the plan and a short coverage summary only when consequential decisions remain unsettled; reuse explicit decisions already made. If implementation changes an agreed expected result or material coverage decision, revise the plan before related code proceeds and obtain only the missing decision. New implementation details do not reopen settled decisions.

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

**A wider blast radius raises priority and may reveal independent coverage.** Deduplicate only when existing evidence proves the same behavior. A correct write can coexist with a stale cache or a broken reader. For example, a new invoice status may be stored correctly while billing rejects it because its accepted values differ. Check that consumer interpretation separately when material; another reader with the same proven contract may only raise priority. Step 4 filters duplicate evidence, not independently failing contracts.

Trace only the relevant contract and failure propagation. Follow another hop when the changed behavior can materially affect it, such as a shared status reaching a billing job through a service. Stop when the contract is understood and unaffected boundaries are supported by evidence; do not map the whole repository or stop solely because one hop was reached. If the probe finds no affected boundary beyond the changed file, record that bounded result.

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

In `plan-only` mode, skip this step; continue to step 8 only for formal HTML. In standalone formal `execute` mode, load the approved plan version and run the selected cases. Under `fudge:ship`, follow the assigned check ownership and shared evidence policy. Without delegation, execute directly. Preserve case IDs and expected results from an approved formal version; seek a new decision only if one of those results or material coverage choices changes.

- **Choose evidence for each case.** Use an existing test, a focused manual check, or a new automated test when it offers durable signal for a meaningful failure mode. A planned case does not automatically become a new test file. Cases needing unavailable infrastructure can remain unexecuted with a reason.
- **Run relevant checks and record the real outcome.** In standalone execution, run focused checks and any project gate needed for the risk. For delegated work, workers follow their brief and the coordinator verifies current raw evidence and records or supplies observed outcomes without duplicating valid checks. A case is **PASS** only after its outcome was observed; **FAIL** if it ran and failed; **NOT RUN** if it could not execute, with a concrete reason. Preserve earlier failure evidence when a later fix passes.
- **Never mark from inference.** "The code obviously handles this" is not a PASS. Record only commands or manual observations whose evidence was read by the person responsible for verification.
- In a formal report, show each case status and a tally. In a concise plan, report only the outcomes and gaps that matter.

For the concise format, finish with the short plan or observed outcomes in chat; do not create an HTML file.

### 8. Build the HTML report (formal format only)

Read [HTML report construction](references/html-report.md) and adapt the complete `assets/example.html` document. Preserve case IDs, expected outcomes, actual evidence, and not-run reasons. Verify local rendering and report the resolved path.
