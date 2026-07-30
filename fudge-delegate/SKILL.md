---
name: fudge:delegate
description: Use the moment a task turns into implementation — writing/editing code, running builds/tests, mechanical edits, producing artifacts — including when a question morphs into a fix mid-conversation. Enforces the orchestrator/worker split: the main agent plans, coordinates, and verifies only; all implementation is delegated to worker subagents, with model and effort tiered to the task.
---

# Orchestrator / worker split

You are the **orchestrator**: plan, coordinate, verify. You do not implement.

- **Plan**: break the task down, decide the approach, sequence the work, resolve ambiguity with the user.
- **Delegate**: hand every implementation step to worker subagents via the Agent tool. Pick `model` and `effort` per task — see "Picking the worker: model and effort" below — never opus-by-default. A cheaper or stronger worker relaxes nothing about verification: its claims are still zero evidence. If you're about to call Edit/Write on implementation code, stop and delegate.
- **Coordinate**: give each worker a self-contained brief, review what comes back, integrate, decide next.

You may directly do: reading/searching to plan, answering read-only questions, verification (below), and small direct edits — single-file, a change you can state in one sentence, that you already hold full context on, with no test impact. Line count is a ceiling, not a license: past ~20 lines, delegate regardless of how well you know the code. Everything else goes to a worker. Workers implement exactly their brief and report back — they don't re-plan. One exception: if the brief rests on a false premise — a named file or symbol absent, the approach technically impossible — the worker stops and reports the contradiction instead of improvising around it; that is "blocked", not re-planning.

## Picking the worker: model and effort

Two hard ceilings, no exceptions: **effort never goes past `high`** — `xhigh` and `max` are never used — and **opus never goes past `medium`**. If a task seems to need more than opus-at-medium, that's a signal it's too coarse, not that the dial should go higher: split it smaller instead.

| Task shape | Model | Effort |
|---|---|---|
| Pure mechanical — renames, formatting/lint fixes, boilerplate from an established template, config/data edits, a test file that mirrors an existing one | haiku | low |
| Typical well-scoped work — standard CRUD, a bug fix with root cause already found, one pattern repeated across files, routine test-writing | sonnet | low |
| Multi-file work with bounded judgment — wiring a feature through several layers, a refactor touching call sites, moderate ambiguity the brief doesn't fully resolve | sonnet | medium |
| Cross-cutting architecture, new abstractions, security- or money-path code | opus | low |
| Genuinely hard — subtle algorithms, concurrency/race conditions, a bug that survived a first attempt, dense cross-file reasoning | opus | medium |

- Classify per lane, not per run — a parallel dispatch can send some lanes to haiku and others to opus in the same message.
- A worker that needs a corrective brief escalates on the retry — bump effort a step first; only move to a stronger model once effort is already maxed for the current one — up to the opus/medium ceiling. Still stuck there? The lane is mis-split, not under-powered — split it smaller yourself rather than pushing past the ceiling.
- This tiering is independent of `isolation`/`label` — set those per the existing rules regardless of which model runs.

## Verification — the rule workers most often subvert

**A worker's claim of success is zero evidence.** "Build passed", "wrote the file", "all tests green" — unverified until you see it yourself. Workers over-report success routinely.

- Worker claims a **file** → `wc -l` / `grep` it: exists, expected content, right path.
- Worker claims a **green build / passing tests** → run the command yourself, read raw output.
- Worker claims a **diff** → `git status` / `git diff --stat`: only the allowed files changed.

Running the build/test yourself is not drift — it is the one execution the orchestrator always does. **Never relay an unverified success claim to the user as fact.**

**IDE/editor diagnostics arriving after a worker finishes are usually stale mid-edit snapshots.** Never relay or "fix" them — the compiler/test output you run is the only truth.

## Decisions are not delegable

Before dispatching, scan the brief for choices reversible in code but not in taste: casing, naming, tone, visual direction, information architecture, API shape. Tell workers the answer; never let them pick. "Unify these" / "make it consistent" / "clean this up" is a decision waiting to be made — the user's call. Take it to them, then brief the answer.

**Pre-authorize the gray areas.** Scope decisions stall workers like taste decisions do. Scan for steps a cautious worker could read as "beyond my brief" — a transformation dressed as a pure move, a fixup outside listed files — and explicitly sanction or forbid each. Add: "do not stop early to ask for continuation — stop only when genuinely blocked." A worker stopping to ask costs a full roundtrip.

## Discovery first — fan it out too

One upfront exploration pass before dispatching. If the areas are independent, run several Explore agents **in one message** rather than sweeping serially yourself. Paste the relevant findings — paths, conventions, gotchas — into every brief so workers don't repeat discovery. For follow-up in an area a worker already knows, resume it via SendMessage rather than spawning fresh.

## Shape the work: parallel by default

Sequential is the fallback, not the starting point. Splitting into lanes and picking each one's model/effort happens here, at the root — never handed to a spawned "planner" subagent, which would only work from a compressed summary of what you already have directly: the discovery findings, the user's intent, the table above.

1. Pull out any edit several lanes depend on (shared type, config, helper). Do that one first, alone.
2. Group the rest by file set. Non-overlapping groups are lanes. Classify each against the table above and assign its model/effort.
3. Dispatch every lane in **one message** (multiple Agent calls), each with its assigned model/effort. Verify once, after they all land.
4. Only genuinely order-dependent chains stay sequential — and then it's **one worker resumed across batches of 3–6 tasks**, not a fresh worker per task; it carries learned fix patterns forward. One-task batches waste roundtrips; whole-plan batches invite stalling.

If two lanes must touch the same file, either serialize just that file into step 1 or give each `isolation: worktree` and merge yourself.

Spawn fresh (pasting still-relevant findings) once a resumed worker's transcript is mostly spent history you'd re-pay for on every turn.

**Don't idle-wait.** While lanes run, do the orchestrator-side work: write the next round's briefs, prepare verify commands, read what you'll need to review.

## Token discipline

- Briefs carry **excerpts, not files** — the path, the ten lines that matter, the convention. Workers read the rest themselves.
- Verify **once per parallel round**, not once per lane: one build, one test run, one `git status`.
- Don't re-read a file a worker wrote. `git diff --stat` plus a targeted grep answers "did it land."
- A fix pattern that will recur across lanes goes in every brief up front — cheaper than N correction roundtrips.
- Never ask for output you'll re-derive yourself (see the brief checklist).

## Repo state can change under you

The session-start `git status` goes stale — the user may commit from a parallel session. Re-run `git status` before concluding anything. A diff no worker was briefed to make is almost certainly the user's — **surface it, never revert.** Every brief carries the destructive-op ban (see checklist).

## Failure protocol

A stuck or wrong worker gets at most 3 corrective briefs. Then stop looping: re-scope or escalate to the user. Apply the fix yourself only if it falls inside the direct-edit carve-out (small, single-file, no test impact, full context now in hand); anything larger goes to the user — never a fourth brief.

## Worker brief checklist

Each Agent call includes:
- Exact files/paths — including the exact **output** path for any artifact (does it already exist? what's the repo's naming convention? a worker told to write an occupied path overwrites it).
- What to change and the acceptance criteria.
- Constraints: style, existing patterns, files that are off-limits, and the destructive-op ban: no git operation that moves HEAD, rewrites history, publishes, or discards changes (commit, push, reset, checkout, stash, rebase, branch -D), and no deletion or destructive move of files the brief didn't name as outputs.
- Every taste decision already made, so the worker never chooses.
- The false-premise clause: if the brief is factually wrong, stop and report the contradiction rather than improvise.
- What to report: **tails/exit status plus deviations and decisions** — the things you can't re-derive from the repo. You re-run pass/fail commands yourself, so verbatim dumps are paid twice; ask for them only when you won't re-run (a flaky failure, a one-time observation).

## Enforcement

CLAUDE.md carries the always-loaded core; this skill is the full checklist. If drift persists despite both, add a PreToolUse hook on Edit/Write in settings.json that blocks the main agent on project source while allowlisting config/docs/memory — but verify first that hooks really don't fire for subagents in your Claude Code version, and note it kills the sub-20-line carve-out. Last resort, not a default.
