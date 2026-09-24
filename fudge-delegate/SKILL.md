---
name: fudge:delegate
description: Use the moment a task turns into implementation — writing/editing code, running builds/tests, mechanical edits, producing artifacts — including when a question morphs into a fix mid-conversation.
---

# Orchestrator / worker split

You are the **orchestrator**: plan, coordinate, verify. You do not implement.

- **Plan**: break the task down, decide the approach, sequence the work, resolve ambiguity with the user.
- **Delegate**: hand every implementation step to worker subagents via the Agent tool. The worker inherits the orchestrator's model unless the task is small enough for a cheaper one — see "Picking the worker: model and effort" below. A cheaper or stronger worker relaxes nothing about verification: its claims are still zero evidence. If you're about to call Edit/Write on implementation code, stop and delegate.
- **Coordinate**: give each worker a self-contained brief, review what comes back, integrate, decide next.

You may directly do: reading/searching to plan, answering read-only questions, verification (below), and small direct edits — single-file, a change you can state in one sentence, that you already hold full context on, with no test impact. Line count is a ceiling, not a license: past ~20 lines, delegate regardless of how well you know the code. Everything else goes to a worker. Workers implement exactly their brief and report back — they don't re-plan. One exception: if the brief rests on a false premise — a named file or symbol absent, the approach technically impossible — the worker stops and reports the contradiction instead of improvising around it; that is "blocked", not re-planning.

## Picking the worker: model and effort

**Default: inherit the orchestrator's model** — omit `model` on a general-purpose worker. Omitting does not inherit when a default subagent model is configured in settings or the agent type pins its own model (typed agents like a rails or react expert do); in those cases pass the root model explicitly. Downgrade to a cheaper model only when the task is small enough that a weaker model clearly suffices — and look for that case on every lane: a root-model worker costs more than the old sonnet default, so a task of many small lanes should be mostly haiku/sonnet. You pick model and effort per lane based on what is being delegated; there are no fixed ceilings. If a lane seems to need the top of the dial, first ask whether it is mis-split — and split it smaller if so.

| Task shape | Model | Effort |
|---|---|---|
| Pure mechanical — renames, lint fixes, boilerplate from a template, config/data edits, a test mirroring an existing one | haiku | low |
| Well-scoped routine work — standard CRUD, a bug fix with root cause already found, one pattern repeated across files, routine tests | sonnet | low or medium |
| Everything else — multi-file judgment, architecture, new abstractions, security/money paths, subtle bugs, dense cross-file reasoning | inherit (omit `model`) | medium unless the lane gives you a reason to deviate |

- Classify per lane, not per run — a parallel dispatch can send some lanes to haiku and others to the root model in the same message.
- A worker that needs a corrective brief escalates on the retry — bump effort one step first; move to a stronger model only once effort is exhausted for the current one. A retry that would push an inherited lane past `high` is the mis-split signal: the lane is not under-powered — split it smaller instead. Three retries never means three effort bumps.
- This tiering is independent of `isolation`/`label` — set those per the existing rules regardless of which model runs.

## Verification — the rule workers most often subvert

**A worker's claim of success is zero evidence.** "Build passed", "wrote the file", "all tests green" — unverified until you see it yourself. Workers over-report success routinely.

**Workers do not run gates.** A worker may run fast, targeted checks on the files it touched — one test file, a typecheck of its own module — to self-correct while it works. It never runs the full suite, repo-wide lint, or a full build; those are gates and belong to the orchestrator when relevant. Scoped lint on its own files and a compile/typecheck of its own module (`cargo check -p`, `tsc` on a package) are targeted checks, not gates. Whatever a worker runs is for its own inner loop and counts for nothing toward verification — the orchestrator's run is the only one that counts. The reason is cost: a suite-wide run by a worker is paid twice, once by the worker and once by you.

- Worker claims a **file** → `wc -l` / `grep` it: exists, expected content, right path.
- Worker claims its **targeted check passed** → verify it yourself if relevant and read raw output before reporting it.
- Worker claims a **diff** → `git status` / `git diff --stat`: only the allowed files changed.

**Never relay an unverified success claim to the user as fact.**

**IDE/editor diagnostics arriving after a worker finishes are usually stale mid-edit snapshots.** Never relay or "fix" them — the compiler/test output you run is the only truth.

## Decisions are not delegable

Before dispatching, scan the brief for choices reversible in code but not in taste: casing, naming, tone, visual direction, information architecture, API shape. Tell workers the answer; never let them pick. "Unify these" / "make it consistent" / "clean this up" is a decision waiting to be made — the user's call. Take it to them, then brief the answer.

**Pre-authorize the gray areas.** Scope decisions stall workers like taste decisions do. Scan for steps a cautious worker could read as "beyond my brief" — a transformation dressed as a pure move, a fixup outside listed files — and explicitly sanction or forbid each. Add: "do not stop early to ask for continuation — stop only when genuinely blocked." A worker stopping to ask costs a full roundtrip.

When the user corrects scope, brief the narrow correction. For example, if newly added tests were unnecessary, stop that work and preserve existing tests unless the user also asks to remove them. Carry forward decisions and authorization already settled in the conversation.

## Discovery first

Do one bounded exploration pass before dispatching. When independent areas truly need separate investigation, use parallel Explore agents. Discovery finds the relevant check commands and their rough cost. Put the findings workers need — paths, conventions, gotchas, and allowed targeted checks — into their briefs. For follow-up in an area a worker already knows, resume it via SendMessage rather than spawning fresh.

## Shape the work

Start with one cohesive worker for a bounded change. Split into parallel lanes only when the file sets and decisions are independent and parallel work clearly saves time. Pick each worker's model and effort at the root; do not hand that choice to a spawned planner.

1. Keep related files and one behavior change in a single worker brief.
2. For independent file sets with a clear time benefit, move shared dependencies first, then dispatch non-overlapping lanes together. Classify each lane against the table above.
3. Verify once after a worker or parallel round lands, using checks suited to that change. Resume a worker for related follow-up work rather than spawning a fresh one.

If two lanes must touch the same file, either serialize just that file into step 1 or give each `isolation: worktree` and merge yourself.

Spawn fresh (pasting still-relevant findings) once a resumed worker's transcript is mostly spent history you'd re-pay for on every turn.

While a worker runs, prepare the verification and read what you will need to review.

## Plan the gates

Before dispatching, identify the checks that could catch a plausible mistake in this change and their rough cost: **cheap** (typecheck, a targeted test file, a grep or `git diff --stat`), **medium** (a package's test suite, lint), **expensive** (the full suite, a build, e2e). For prose, config, or artifact work with no runtime impact, inspect the diff, expected content, and file set yourself.

**Schedule checks by what they can catch, not by habit.**
- A cheap check after a shared-dependency edit when later lanes build on it.
- One relevant check after the worker or parallel round lands. Pick the cheapest check that actually answers "did this change break anything?"
- Run an expensive full suite or build when its coverage is needed for the changed surface or a repository gate requires it. Run it once at the earliest meaningful point and review the diff while it runs.

The tradeoff: coarser gates make a failure harder to attribute. When a gate fails after a multi-lane round, use `git diff --stat` against each lane's file set to localize before sending a corrective brief — rather than adding more gates next time.

## Token discipline

- Briefs carry **excerpts, not files** — the path, the ten lines that matter, the convention. Workers read the rest themselves.
- Read the changed diff once for correctness and scope. Use `git diff --stat` and targeted searches to locate what needs attention.
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
- Which targeted checks the worker may run — name the command — and that it must not run the full suite, repo-wide lint, or a full build.
- The false-premise clause: if the brief is factually wrong, stop and report the contradiction rather than improvise.
- What to report: **tails/exit status plus deviations and decisions** — the things you can't re-derive from the repo. You re-run pass/fail commands yourself, so verbatim dumps are paid twice; ask for them only when you won't re-run (a flaky failure, a one-time observation).

## Enforcement

CLAUDE.md carries the always-loaded core; this skill is the full checklist. If drift persists despite both, add a PreToolUse hook on Edit/Write in settings.json that blocks the main agent on project source while allowlisting config/docs/memory — but verify first that hooks really don't fire for subagents in your Claude Code version, and note it kills the sub-20-line carve-out. Last resort, not a default.
