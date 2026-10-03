# Rule setup interview

## Setup interview

### Phase 0 — Ground it

**Classify the archetype first, before a single question.** One of: library, CLI tool, long-running service, web app, data pipeline, embedded, mobile. The archetype prunes roughly a third of the bank up front — a library is never asked about health checks, a CLI is never asked about transaction boundaries. The `◇` rows in `dimension-bank.md` are the ones this gate controls.

**If the repo already has code**, ask which starting point the user wants, in these words:

> **This repo already has code. Two ways to start:**
> **A — Build on what's here.** I read the code first, work out the habits it already follows, and bring you those as a starting draft. You keep what you like and change what you don't. Faster, and the rules will match code that already exists.
> **B — Start clean.** Ignore current habits and decide the rules from scratch. Slower, but nothing carries over by accident. Existing code may end up not matching the rules — I'll tell you where.

**Greenfield skips this question entirely.** There is no code to read, so there is no choice to offer.

On **build on what's here**, read the relevant code, using bounded read-only workers when available and appropriate, each answering a specific question:

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

Write `<project>-conventions` into the existing project-skill location, the caller-supplied project-skill path, or the active host’s project-skill location if neither exists (Codex: `.codex/skills/`; Claude: `.claude/skills/`). Follow `emitting.md`. Do not duplicate an existing authority at a new path.

`rationale.md` ships alongside the rules and is not a transcript of the interview. It is a register: every contested call, the alternatives that were on the table, why the chosen one won, and the named dependency links from Phase 2. Its job is to stop a future agent from reopening a settled argument, and to make reversing an upstream rule surface what depended on it instead of quietly invalidating it.

Where Phase 0.5 found tooling gaps, show the exact config that would be added and what it would enforce, and write it **only with explicit authorization for that concrete config, including prior authorization**. A blanket approval of the rule table is not approval of a config file.

On a **start-clean** run, finish with a conformance report: where existing code does not match the rules just agreed. That was promised in the Phase 0 question and it is a report, not a work order — no file is edited to close a gap. Write it to this skill's Output location below unless the user or a calling workflow names another path.

Show the exact pointer in the active host instruction file (`AGENTS.md` for Codex, `CLAUDE.md` for Claude). Add it when that exact change is authorized; prior authorization applies. Preserve existing instructions.

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

**Security is considered in every full-project setup.** A focused setup covers security implications of the requested concern without requiring unrelated rounds.

## Phase 2 is the setup gate

**In rule setup, no authoritative rules or proposed tooling changes are written before the user approves the exact rule table or config** — including the authoritative skill, its rule references, and tooling config. Drafts may be shown in chat or written to an authorized unused review-artifact path. Prior explicit approval of the exact contents applies. Audit may write only a run-local report, defaulting to the location resolved through package-root `shared/artifacts.md`, when the user requests it or an authorized calling workflow supplies its path; a `fudge:ship` run needs no second approval for that report. Amendment has its own exact-change approval gate in `audit-amend.md`.

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
- Writing authoritative rules before the Phase 2 gate is answered.
- Treating one observed pattern as an approved rule or a reason to change one.
- Editing source code to conform to a rule you just wrote.
- Recording a contested call in the rules without recording the rejected alternative in `rationale.md`.
