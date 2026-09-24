---
name: fudge:conventions
description: Set up project coding conventions, audit a change for convention drift and gaps, or amend approved rules. Use for "set up conventions," "check this change against our conventions," and "update our project rules." Setup interviews the user and emits a project-specific conventions skill; audit is read-only; amendment requires approval of the exact rule change.
---

# fudge:conventions

The steward for a project's coding conventions. It can set up a project-specific contract, audit a change against that contract, or propose a targeted amendment. Any language, any archetype. The opinions come from the user, not this file.

**Two names are in play and they must never blur.** `fudge:conventions` is this skill. `<project>-conventions` is the project-specific skill it can create or amend. Name the one you mean. The existing project rules are authoritative; never create a second conventions source to work around them.

## Choose the mode

- **Setup:** No actionable project conventions exist, or the user explicitly wants to replace them. Follow the interview below. If rules already exist, read them first and resolve whether to amend or replace; do not overwrite them just because setup was invoked.
- **Audit:** The user or another skill supplies a change, diff, or bounded file set to check against existing project rules. Read `references/audit-amend.md`. Return findings, not code or changed rules.
- **Amend:** The user wants a specific project rule changed, or approves a proposal from an audit. Read `references/audit-amend.md`. Show the exact change before writing it.

Locate the authoritative source before any mode: inspect project instructions, their pointers, and project skills. Follow an existing `.claude/skills/` or `.codex/skills/` location or a caller-supplied path. If sources conflict or authority is unclear, identify the conflict and ask; ordinary code patterns do not become rules by inference. Keep setup, audit, and amendment distinct so a ship run can check conventions without rerunning the interview.

## The core principle: rules and findings, never source code

Nothing here writes or refactors source. Setup and amendment produce approved rules and rationale; audit produces findings. Making code conform is separate work, owned by the caller when this skill runs inside `fudge:ship`.

The second half of the principle is the one that gets violated: **never ask an open-ended question where a draft can be shown instead.** Read the repo, take a stance, propose it, let the user push back. "What are your preferences for error handling?" is a failure. A described situation with two named options and a recommendation is the job.

## What this skill will not do

- **No source code.** Not written, not refactored, not "just this one file to match the rule."
- **No replacing a linter.** If a formatter or linter can enforce it mechanically, it is a config line, not a prose rule. Tooling produces configuration, not prose.
- **No touching the project's `CLAUDE.md` without asking.** The pointer that guarantees the emitted skill loads is offered at the end of a run and added only on a yes. Never by default.
- **No open-ended questions where a draft would do.** See above.
- **No implicit side effects.** Creating or amending a project skill does not authorize a git commit, push, config change, or instruction-file pointer. Each needs its own authorization. A local-only `fudge:ship` run stays local.

## References

- `references/dimension-bank.md` — the full dimension bank, the D / A / ◇ markers, and the archetype gating table. Open it at Phase 0 to prune, and again at the head of each round.
- `references/writing-rules.md` — question style (plain language, situation-first, the worked example) and the rule admissibility bar. Open it before drafting any question or any rule.
- `references/emitting.md` — the shape of the emitted `<project>-conventions` artifact, including the template for its `SKILL.md`. Open it at Phase 3.
- `references/audit-amend.md` — evidence and approval rules for audit and targeted amendment. Open it for either mode; the setup interview does not need it.

## Output location

Write this skill's files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

For this skill, `<skill>` is `conventions`. The start-clean conformance report and any requested audit report default to `.fudge/<branch>/conventions/`. The emitted `<project>-conventions` skill, `rationale.md`, tooling configs, and the `CLAUDE.md` pointer stay product and keep their existing project locations — none of them move under `.fudge/`.

## Setup interview

### Phase 0 — Ground it

**Classify the archetype first, before a single question.** One of: library, CLI tool, long-running service, web app, data pipeline, embedded, mobile. The archetype prunes roughly a third of the bank up front — a library is never asked about health checks, a CLI is never asked about transaction boundaries. The `◇` rows in `references/dimension-bank.md` are the ones this gate controls.

**If the repo already has code**, ask which starting point the user wants, in these words:

> **This repo already has code. Two ways to start:**
> **A — Build on what's here.** I read the code first, work out the habits it already follows, and bring you those as a starting draft. You keep what you like and change what you don't. Faster, and the rules will match code that already exists.
> **B — Start clean.** Ignore current habits and decide the rules from scratch. Slower, but nothing carries over by accident. Existing code may end up not matching the rules — I'll tell you where.

**Greenfield skips this question entirely.** There is no code to read, so there is no choice to offer.

On **build on what's here**, read the repo with parallel read-only Explore agents, each answering one specific question rather than doing an open-ended pass:

- How are errors handled at seams?
- What is the actual test habit — not the stated one?
- What's homegrown versus pulled in as a dependency?
- What's the typical file size?
- Where does validation happen?
- What's the import/layering shape?

The output of this phase is a draft contract inferred from observed reality, not a blank questionnaire. Phase 1 opens from that draft.

### Phase 0.5 — Detect, don't ask

Everything mechanically discoverable is read from the repo and never asked: formatter, linter, type-checker strictness, lockfile presence, the branch naming already in use, the commit message shape already in use. Present it as a **single findings block** the user corrects in bulk — not as a run of questions with known answers.

**Gaps become proposals with a stance, not questions.** "No formatter is configured. I'd add one and make it a merge gate. Fine?" is the shape.

### Phase 1 — The rounds

See the table below. Each round opens with a plain-language paragraph proposing the whole round's default and saying what it costs. The user accepts the round wholesale in one word, or names the part to drill into.

That wholesale-accept is what makes a bank this size survivable. Most users accept four rounds outright and spend real attention on the two they care about. Do not undermine it by walking every dimension aloud after an accept.

On a **build on what's here** run, order the rounds by where the codebase is most inconsistent, so a user who quits halfway still leaves with the decisions that mattered most rather than whichever round came first.

### Phase 2 — Confirm

Before showing anything, check the accumulated rules across rounds for **conflicts and silent dependencies**. A conflict is resolved with the user, never papered over and never quietly decided. Every resolution is recorded in `rationale.md`. Dependencies found here become the named rule links in the emitted artifact.

The shape of a real one: one round declared everything past the controller to be trusted input, while another required background jobs to authorize. Resolved by redefining "entry point" to include jobs, rake tasks, and console scripts — jobs are boundaries, not downstream code.

**Past 60 accumulated rules, offer a re-filter** at a harder admissibility bar — keep what is both violable today *and* costly when broken, challenge what is true but rarely load-bearing. Offer it; never apply it automatically. The user may ship the full set. 60 is a tunable starting threshold, not a law. Start-clean runs are the ones that hit it: every round proposes a full default set and accepting them all compounds, where build-on-what's-here is bounded by the habits actually in the code.

Then present the full rule set as a **compact table**. Everything upstream of that table is drafting. Everything downstream is emission after approval, not a git commit.

### Phase 3 — Emit

Write `<project>-conventions` into the existing project-skill location, the caller-supplied project-skill path, or `.claude/skills/<project>-conventions/` if neither exists. Follow `references/emitting.md`. Do not duplicate an existing authority at a new path.

`rationale.md` ships alongside the rules and is not a transcript of the interview. It is a register: every contested call, the alternatives that were on the table, why the chosen one won, and the named dependency links from Phase 2. Its job is to stop a future agent from reopening a settled argument, and to make reversing an upstream rule surface what depended on it instead of quietly invalidating it.

Where Phase 0.5 found tooling gaps, show the exact config that would be added and what it would enforce, and write it **only on an explicit yes for that config**. A blanket approval of the rule table is not approval of a config file.

On a **start-clean** run, finish with a conformance report: where existing code does not match the rules just agreed. That was promised in the Phase 0 question and it is a report, not a work order — no file is edited to close a gap. Write it to this skill's Output location below unless the user or a calling workflow names another path.

Last, offer the one-line pointer in the project's `CLAUDE.md`. Description-based triggering is probable; the pointer is what makes loading certain. Offer it, name the tradeoff, add it only on a yes.

## The rounds

Six rounds baseline. Groups in the dimension bank do not map one-to-one onto rounds — two fold in.

| # | Round | Covers |
|---|---|---|
| 1 | structure | Repo topology, layering and import direction, directory organization, where a new feature starts, public vs. internal surface, config, the `utils/` junk-drawer rule |
| 2 | architecture | Error model, trust boundaries, abstraction threshold, DI posture, state and mutation, domain types vs. primitives, plus the archetype-gated rows (concurrency, persistence, SDK wrapping, versioning) |
| — | observability | **Inserted after architecture only for long-running service, web app, or data pipeline.** Logging, what must never be logged, metrics and tracing, health checks and rollback discipline. Pruned entirely for every other archetype |
| 3 | testing | Framework and location, test floor, shape, doubles, determinism, coverage stance, test-first or tests-with, flaky test policy |
| 4 | workflow | Branching, commits, PR discipline, what blocks merge, definition of done, release process — **plus tooling's two asked rows**: pre-commit hooks, and the one command that checks everything. Both are about the loop around writing code, not the code itself |
| 5 | docs | Comment density and what earns one, doc comments on public API, whether decisions are recorded as ADRs |
| 6 | security | Secret handling, where authn/authz checks live, input sanitization at trust boundaries, vulnerability response |

The rest of **tooling** is resolved in Phase 0.5 by detection and never reaches a round.

**Security is never defaulted away silently.** Even when the user says "keep it light," the security round is asked in full.

## Phase 2 is the setup gate

**In setup mode, nothing is written to disk before the user approves the rule table** — not the artifact, not a reference file, not a tooling config, not a scratch draft in the target repo. Audit may write only a run-local report, defaulting to this skill's Output location below, when the user requests it or an authorized calling workflow supplies its path; a `fudge:ship` run needs no second approval for that report. Amendment has its own exact-change approval gate in `references/audit-amend.md`.

An approval covers the table that was shown. If the user's response would change a rule, change it and re-present; do not carry it as an unwritten amendment into Phase 3.

| Rationalization | Counter |
|---|---|
| "They accepted every round, so they've effectively approved the set." | They approved a handful of round summaries, not every rule underneath them. The table is the first time they see the set together. |
| "It's only writing a doc, not code." | It's writing rules every future agent will follow. Wrong rules are worse than no rules. |
| "The rules are obviously reasonable." | You wrote them. You are the last party qualified to judge that. |
| "I'll write the files and they can edit after." | A file on disk gets ratified, not reviewed. |

## Red flags

If you catch yourself doing any of these, you are mid-violation. Stop.

- About to ask "what are your preferences for X" — you owe a draft, not a question.
- Writing a rule containing "write clean code", "keep it simple", "follow SOLID", or "use meaningful names". Not admissible, full stop.
- Restating in prose something the linter already enforces.
- In setup, writing any file before the Phase 2 gate is answered.
- Treating one observed pattern as an approved rule or a reason to change one.
- Editing source code to conform to a rule you just wrote.
- Recording a contested call in the rules without recording the rejected alternative in `rationale.md`.

## Delegation

This repo's `CLAUDE.md` splits orchestration from implementation, and it applies here.

- **Phase 0's codebase read fans out** to parallel read-only Explore agents, one per question above.
- **Phase 3's emit and approved amendments are delegated** to a worker. Verify what comes back by reading the written files, not by trusting the report.
- **The interview is never delegated.** The answers belong to the user and the questions must be asked directly, in this conversation.
