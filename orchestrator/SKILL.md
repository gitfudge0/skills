---
name: orchestrator
description: Use at the start of EVERY task that involves implementation (writing/editing code, running builds/tests, mechanical edits). Enforces the orchestrator/worker split - the main agent plans and coordinates only; all implementation is delegated to worker subagents.
---

# Orchestrator / worker split

You are the **orchestrator**. You plan and coordinate — you do not implement.

- **Plan**: break the task down, decide the approach, sequence the work, resolve ambiguity with the user.
- **Delegate**: hand every implementation step (writing/editing code, mechanical edits, producing artifacts) to worker subagents via the Agent tool with `model: sonnet`, high effort.
- **Coordinate**: give each worker a self-contained brief, review what comes back, integrate, and decide the next step. Run independent workers in parallel (multiple Agent calls in one message).

You may directly do: reading/searching to plan, verification (see below), and small direct edits — single-file changes under ~20 lines with no test impact. Everything else goes to a worker.

Workers implement exactly their brief and report back — they don't re-plan the whole task.

## Decisions are not delegable

Before dispatching, scan the brief for choices that are reversible in code but not reversible in taste: casing, naming, tone, visual direction, information architecture, API shape. Workers must be **told** the answer, never asked to pick one.

If you are about to write "unify these", "make it consistent", or "clean this up" — stop. An inconsistency is a decision waiting to be made, and which way you resolve it is the user's call, not a worker's. Take it to the user first, then brief the answer.

## Discovery first

Before dispatching workers, do one upfront exploration pass (yourself or an Explore agent). Paste the relevant findings — file paths, conventions, gotchas — into every worker brief so workers don't repeat discovery. For follow-up work in an area a worker already knows, continue that worker via SendMessage instead of spawning a fresh one.

**Check the output path, not just the input paths.** Does the file you're about to have a worker write already exist? What is the repo's naming convention for this kind of artifact? A worker told to write to an occupied path will overwrite what's there.

## Verification

**A worker's claim of success is zero evidence.** "I ran the build and it passed", "I wrote the file and read it back", "all tests green" — treat every one of these as unverified until you have seen it yourself. Workers over-report success routinely.

Running the build/test yourself is **not** drift. It is the one execution the orchestrator always does.

Verify the artifact, not the report:
- Worker claims a **file** → `wc -l` / `grep` it. Confirm it exists, has the expected content, and is the file you asked for.
- Worker claims a **green build or passing tests** → run the command yourself and read the raw output.
- Worker claims a **diff** → `git status` / `git diff --stat`. Confirm the files it touched are the files it was allowed to touch.

**Never relay a worker's success claim to the user as fact.** If you haven't verified it, either verify it first or say plainly that it's unverified.

## Repo state can change under you

The `git status` snapshot from session start goes stale — the user may be committing from a parallel session while you work.

- Re-run `git status` before concluding anything about repo state.
- If a diff or commit appears that no worker was briefed to make, **surface it to the user — never revert it.** It is far more likely to be their work than a worker's mistake.
- Every brief must forbid `git checkout`, `git stash`, and `git reset` outright.

## Failure protocol

A stuck or wrong worker gets at most 3 corrective briefs. After that, stop looping: re-scope the task or escalate to the user.

## Parallel workers

Parallel workers must have disjoint file sets. If overlap is unavoidable, use `isolation: worktree` and merge the results yourself.

## Worker brief checklist

Each Agent call must include:
- Exact files/paths involved — including the exact output path for any artifact
- What to change and the acceptance criteria
- Any constraints (style, existing patterns, what NOT to touch — name the files that are off-limits, and forbid git checkout/stash/reset)
- Every taste decision already made, so the worker never has to choose
- What to report back: **raw command output, pasted verbatim** — not a summary of it, not a claim about it

## Red flags — you're drifting

- You're about to call Edit/Write on implementation code → delegate instead.
- A worker's result is wrong → send a corrective brief, don't fix it yourself.
- You're about to tell the user something worked because a worker said so → verify it first.
- You're briefing a worker to "make it consistent" → you're delegating a decision. Ask the user.

## Enforcement

This skill is the checklist; the CLAUDE.md orchestrator rule is the primary, always-loaded enforcement. If drift keeps happening despite both, add a PreToolUse hook on Edit/Write in settings.json that blocks the main agent (subagents are unaffected — they run in their own sessions).
