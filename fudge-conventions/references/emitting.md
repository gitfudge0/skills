# Emitting the artifact

What Phase 3 writes, where it goes, and what it is never allowed to do on the way. `fudge:conventions` is the generator; `<project>-conventions` is the artifact described here. Say which one you mean every time either is named.

---

## Directory layout

```
.claude/skills/<project>-conventions/
  SKILL.md          # ~80 lines: the hard rules that apply to every file, plus when to consult which reference
  references/
    structure.md
    architecture.md
    testing.md
    tooling.md
    workflow.md
    security.md
    rationale.md    # every contested call + the alternatives rejected + why
```

`<project>` is derived from the project name. The reference set is fixed at seven files — do not add an eighth because a round produced more material than expected.

## SKILL.md is short and always-read

It carries the rules that apply to every file the agent touches, plus a pointer to which reference file to open for depth on a given topic. **Depth lives in the references, not in `SKILL.md`.** Target roughly 80 lines.

The discipline is that `SKILL.md` is loaded on every task in that repo, so every line in it is paid for on every task. A rule that only applies when touching the database layer is not an always-read rule — it is a line in `architecture.md` and a routing pointer in `SKILL.md`.

## rationale.md is a register, not a changelog

It is not a transcript of the interview. It records:

- Every contested call.
- The alternatives that were on the table.
- Why the chosen one won.
- **Rule dependencies, by name.** When a rule exists only because another rule created its precondition, that link is recorded — so reversing the upstream rule surfaces what depends on it instead of quietly invalidating it.

Its job is to stop a future agent — human or otherwise — from reopening a settled argument from scratch. Every conflict resolved during Phase 2 lands here for the same reason: so it isn't re-argued later.

## Which round lands where

| Round | Reference |
|---|---|
| structure | `structure.md` |
| architecture | `architecture.md` |
| observability and operations (services, web apps, data pipelines only) | `architecture.md` |
| testing | `testing.md` |
| workflow | `workflow.md` |
| security | `security.md` |

Observability does not get a file of its own. When the archetype gate opens that seventh round, its rules fold into `architecture.md` — logging boundaries, what must never be logged, metrics and tracing, health checks and rollback discipline are all statements about the shape of the system, and splitting them off strands them where nobody looks.

`tooling.md` receives no round. Tooling is resolved in Phase 0.5 by detection, and the file carries **the check-command spec and any linter config delta** — not prose restating what the linter already enforces. Its two asked rows are put during the workflow round (pre-commit hooks, and the one command that checks everything) but the answers are written here, because that is where an agent looks for how to verify its own work.

The documentation round has no reference of its own — none of the seven is a `docs.md`. Route its rules by the surface they govern: comment density with `architecture.md`, doc comments on the public API with `structure.md` (which already owns the public-versus-internal line), and the ADR question with `rationale.md`, which is where recorded reasoning already lives.

---

## Template — the generated SKILL.md

Angle-bracket slots are project-specific. Everything outside them is structural and stays.

```markdown
---
name: <project>-conventions
description: Use whenever writing, editing, refactoring, or reviewing code in the <project> repo — new files, new functions, bug fixes, tests, or config. Read before the first edit, not after. Covers how this project structures code, handles errors, tests, and gates merges.
---

# <project> conventions

Generated <YYYY-MM-DD> by `fudge:conventions`. `fudge:conventions` is the generator and lives elsewhere; this file is the artifact and lives in this repo. Editing this file changes this project's rules; it does not change the generator.

## The rules that matter most

These apply to every file. Everything else is in the references.

1. **<rule>.** <One sentence on what goes wrong without it.>
2. **<rule>.** <One sentence on what goes wrong without it.>
3. **<rule>.** <One sentence on what goes wrong without it.>
4. **<rule>.** <One sentence on what goes wrong without it.>
5. **<rule>.** <One sentence on what goes wrong without it.>

## Adding or moving code

<One or two lines on where a new feature starts and what the import direction is.>

Read `references/structure.md` before creating a package, a top-level directory, or anything exported.

## Errors, boundaries, and state

<One or two lines on the error model and where untrusted input stops being untrusted.>

Read `references/architecture.md` before adding an interface, a seam, or a call to a third-party client.

## Tests and the check command

<The test floor in one line.> The one command that checks everything is `<command>`.

Read `references/testing.md` for shape, doubles, and determinism; `references/tooling.md` for what that command runs.

## Definition of done

- [ ] <check>
- [ ] <check>
- [ ] `<command>` passes locally, output read, not assumed.
- [ ] Rules touched by this change are still true; if one had to bend, say so rather than bending it silently.

## When this file doesn't cover it

Name the ambiguity and ask. Do not improvise a rule, and do not treat silence as permission. An uncovered case is a question for the user, not a gap to fill with judgement — the invented rule becomes precedent nobody agreed to.

Why a rule is what it is: `references/rationale.md`, which also records which rules depend on which.
```

The description slot is the load-bearing one. Write it to fire on code-writing activity in that repo — the verbs a user actually types before code gets written — not as a summary of the file's contents.

---

## What Phase 3 does and does not do

**Tooling configs are shown before they are written.** Where Phase 0.5 found a gap, show the exact config and exactly what it would enforce, then write it **only on the user's approval**. Each config needs its own yes. A yes to the formatter is not a yes to the pre-commit hook.

**Source code is never written or refactored.** This skill produces documentation of rules, not code that follows them. That holds even when a violation is one line away from fixed and even when the user would obviously want it fixed — fixing it is a separate request.

**Start-clean runs get a conformance report.** Option B promised the user they'd be told where existing code doesn't match the new rules, and this is where that promise is paid. The report describes; it changes nothing. It names the rule, the places that violate it, and nothing else.

Keep two things apart in that report. A **style gap** is code that predates the rule and is now non-conforming — that is the expected output of a start-clean run and it is not urgent. A **defect** is code that is wrong on its own terms, which the sweep happened to surface. Flag defects separately, as bugs, and do not bury them in a conformance list — they are the most valuable thing the pass produced and the list is the one place nobody reads twice.

---

## Residual risk: a generated skill only helps if it triggers

The emitted `SKILL.md` description is written to fire hard on code-writing activity in that repo. The only thing that makes loading *certain* — rather than probable — is a one-line pointer in the project's `CLAUDE.md`.

Offer to add that pointer at the end of a run. **Never add it by default.**

A project that declines the pointer is trusting description-based triggering alone, which can misfire. That is a real gap, and it is the user's call to accept — say so plainly when offering, and do not re-litigate a no.
