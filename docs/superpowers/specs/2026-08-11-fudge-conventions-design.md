# fudge:conventions — design spec

**Status:** Design settled, ready for implementation
**Date:** 2026-08-11
**Skill:** `fudge:conventions` (directory: `fudge-conventions/`)

---

## 1. Identity and purpose

`fudge:conventions` is an interview that ends in a committed project skill encoding the rules an agent obeys when writing code in that project.

It is a **generator only**. There is no drift-check mode and no amend mode. Re-running it later redoes the interview from scratch against current code and overwrites what's there — it does not diff, reconcile, or merge.

Two names are in play and the skill must never let them blur:

- **`fudge:conventions`** — the generator. This skill. Lives in this repo, invoked once (or re-run) to produce the artifact below.
- **`<project>-conventions`** — the artifact. The project skill this generator emits into the target repo, named after that project. Whenever the running skill refers to either, it says which one it means.

### Closest neighbors

- **`fudge:rust-arch`** — static and language-specific. It ships one language's opinions, pre-written, to every Rust project that loads it.
- **`fudge:design-system`** — interrogates the user, locks a direction, emits artifacts.

`fudge:conventions` is the generative counterpart of `fudge:rust-arch`: instead of shipping one language's fixed opinions, it interviews the user and emits *that project's own* rules — for any language, any archetype.

---

## 2. The emitted artifact

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

`SKILL.md` is short and always-read — the rules that apply to every file the agent touches, plus a pointer to which reference file to open for depth on a given topic. Depth lives in the references, not in `SKILL.md`. `<project>` is derived from the project name.

`rationale.md` is not a changelog of the interview. It is a register: every contested call, the alternatives that were on the table, and why the chosen one won. Its job is to stop a future agent — human or otherwise — from reopening a settled argument from scratch, and to record rule dependencies: when a rule exists only because another rule created its precondition, that link is recorded by name, so reversing the upstream rule surfaces what depends on it instead of quietly invalidating it.

---

## 3. The flow

### Phase 0 — Ground it

**Archetype classification comes first**, before any question is asked. The project is classified as one of: library, CLI tool, long-running service, web app, data pipeline, embedded, mobile. The archetype prunes roughly a third of the question bank up front — a library is never asked about health checks, a CLI is never asked about transaction boundaries. Questions tagged `◇` in the dimension bank (Section 4) are the ones this gate controls.

**If the repo already has code**, the user is asked which starting point they want, phrased plainly:

> **This repo already has code. Two ways to start:**
> **A — Build on what's here.** I read the code first, work out the habits it already follows, and bring you those as a starting draft. You keep what you like and change what you don't. Faster, and the rules will match code that already exists.
> **B — Start clean.** Ignore current habits and decide the rules from scratch. Slower, but nothing carries over by accident. Existing code may end up not matching the rules — I'll tell you where.

**Greenfield projects skip this question entirely** — there is no code to read, so there is no choice to offer.

For **"build on what's here"**, repo reading is done with parallel read-only Explore agents, each answering a specific question rather than doing an open-ended pass:

- How are errors handled at seams?
- What is the actual test habit — not the stated one?
- What's homegrown versus pulled in as a dependency?
- What's the typical file size?
- Where does validation happen?
- What's the import/layering shape?

The output of this phase is a **draft contract inferred from observed reality**, not a blank questionnaire. Phase 1 opens from that draft.

### Phase 0.5 — Detect, don't ask

Everything mechanically discoverable — formatter, linter, type-checker strictness, lockfile presence, branch naming already in use, commit message shape already in use — is read from the repo, never asked as a question. It is presented as a **single findings block** the user corrects in bulk.

Gaps become proposals, not questions. "No formatter is configured. I'd add one and make it a merge gate. Fine?" is the shape — a proposal with a stance, not an open question.

### Phase 1 — Six interview rounds

The rounds are: **structure, architecture, testing, workflow, docs, security.**

The eight groups in the dimension bank (Section 4) do not map one-to-one onto rounds. Two fold in:

- **Tooling** is resolved in Phase 0.5 by detection. Its two asked rows — pre-commit hooks, and the one command that checks everything — belong to the **workflow** round, since both are about the loop around writing code rather than the code itself.
- **Observability and operations** becomes a **seventh round, inserted after architecture, only when the archetype is a long-running service, web app, or data pipeline.** For every other archetype the whole group is pruned and the interview stays at six rounds.

Each round opens with a **plain-language paragraph** stating the proposed default for the whole round and what it costs. The user accepts the round wholesale in one word, or names which part to drill into. This wholesale-accept is the mechanism that makes ~50 dimensions survivable — most users accept four rounds outright and spend real attention on the two that matter to them.

In a "build on what's here" run, **rounds are ordered by where the codebase is most inconsistent**, so a user who quits halfway still walks away with the decisions that mattered most, not whichever came first alphabetically.

**Security is never defaulted away silently.** Even when the user says "keep it light," the security round is still asked in full.

### Phase 2 — Confirm

Before the table is shown, the accumulated rules are checked across rounds for conflicts and for rules that silently depend on each other. A conflict is resolved with the user, not papered over or silently decided. Every resolution is recorded in `rationale.md`, so the same conflict is not re-argued later. Dependencies found here feed the dependency links described in Section 2.

For example: one round declared everything past the controller to be trusted input, while another round required background jobs to authorize. Resolved by redefining "entry point" to include jobs, rake tasks, and console scripts — jobs are boundaries, not downstream code.

If the accumulated set exceeds **60 rules**, Phase 2 offers a re-filter at a harder admissibility bar before the table is presented. The harder bar keeps rules that are both violable today *and* costly when broken; it challenges anything that is true but rarely load-bearing. The re-filter is offered, never applied automatically — the user can ship the full set. 60 is a starting threshold, tunable, not a hard law. The asymmetry is real: start-clean runs are the ones that hit this, since build-on-what's-here is limited by the habits actually present in the code — every round in a start-clean run proposes a full default set, and accepting them all compounds.

The full rule set is presented as a **compact table** before anything is written. This is the real approval gate — everything upstream of it is drafting, everything downstream is committing.

### Phase 3 — Emit

Write the project skill to `.claude/skills/<project>-conventions/`. Where tooling gaps were found in Phase 0.5, show the exact configs that would be added and what they'd enforce, and write them **only on the user's approval**.

Two things are never done unapproved and never done at all as a side effect of running this skill:

- Writing tooling config without an explicit yes for that config.
- Writing or refactoring source code — this skill produces documentation of rules, not code that follows them.

---

## 4. The dimension bank

Legend — **D** = detected from the repo, never asked · **A** = asked · **◇** = archetype-gated (pruned before the interview starts, per Phase 0).

### Project structure

| Dimension | Type |
|---|---|
| Repo topology (single package, workspace, monorepo; what earns a new package) | A |
| Layering and import direction (what may depend on what) | A |
| Directory organization — by layer vs. by feature | A |
| Where a new feature starts ("I'm adding X, where does it go" must have an answer) | A |
| Public vs. internal surface — what's exported, what's private by default | A |
| Config — where it lives, env vs. file vs. flags, how secrets get in | D+A |
| The `utils/` junk-drawer rule | A |
| Generated and vendored code placement | D |

### Architecture and patterns

| Dimension | Type |
|---|---|
| Error model (exceptions vs. result types, wrapping at seams, what's fatal, retry stance) | A |
| Validation and trust boundaries (where untrusted input stops being untrusted) | A |
| Abstraction threshold (how many real implementations before an interface earns its keep) | A |
| Dependency injection posture (constructor, container, or just pass it) | A |
| State and mutation (immutability default, globals/singletons stance) | A |
| Domain types vs. raw primitives (is a user ID a `String` or a `UserId`) | A |
| Concurrency (async at the edges or everywhere, blocking calls, shared state, cancellation) | A◇ |
| Persistence (repository pattern vs. direct queries, transaction boundaries) | A◇ |
| Third-party SDKs and HTTP clients — wrapped or used directly | A◇ |
| Versioning and deprecation policy (dominant for libraries, irrelevant for an internal service) | A◇ |
| Performance posture (when optimizing is allowed, what gets measured) | A |

### Testing

| Dimension | Type |
|---|---|
| Framework and where tests live | D+A |
| Test floor (what must have a test before "done") | A |
| Shape — unit-heavy, integration-heavy, or e2e-heavy, and why | A |
| Doubles — mocks, hand-written fakes, or real dependencies in containers | A |
| Determinism — how time, randomness, network get controlled | A |
| Coverage — hard gate number, advisory, or untracked | A |
| Test-first expected or tests-with | A |
| Flaky test policy (quarantine, fix, delete) | A |
| Snapshot/golden tests allowed or banned | A◇ |

### Tooling

Almost entirely detected; gaps are proposed, not asked.

| Dimension | Type |
|---|---|
| Formatter (which, config, is it a merge gate) | D |
| Linter (which, ruleset, warnings-as-errors) | D |
| Type checking strictness and escape-hatch policy (`any`, `unwrap`, `unsafe`, `# type: ignore`) | D |
| Dependency hygiene (lockfile, vuln audit, unused-dep detection, licence policy) | D |
| The one command that checks everything | D+A |
| Pre-commit hooks — what runs locally vs. CI-only | A |

### Workflow

| Dimension | Type |
|---|---|
| Branching model and naming | D+A |
| Commit conventions | D+A |
| PR discipline (one concern per PR, size ceiling) | A |
| What blocks merge | A |
| Definition of done (the checklist an agent runs before claiming completion) | A |
| Changelog and release process | A◇ |

### Observability and operations

Archetype-gated; mostly skipped outside services.

| Dimension | Type |
|---|---|
| Logging (structured or plain, levels, at which boundaries) | A◇ |
| What must never be logged (PII, secrets, tokens) | A◇ |
| Metrics and tracing | A◇ |
| Health checks, graceful shutdown, migration and rollback discipline | A◇ |

### Documentation

| Dimension | Type |
|---|---|
| Comment density and what earns one (the why, never the what) | A |
| Doc comments on public API — required or optional | A |
| Whether architecture decisions are recorded (ADRs) or the reasoning lives only in the contract | A |

### Security

Never defaulted away, regardless of how light the rest of the interview runs.

| Dimension | Type |
|---|---|
| Secret handling and what guarantees they aren't committed | A |
| Where authentication and authorization checks live | A |
| Input sanitization at every trust boundary | A |
| Vulnerability response policy | A |

---

## 5. Question style

**Never ask an open-ended question when a draft can be shown instead.** Every question describes the actual situation and what's at stake in plain language before offering choices.

**No jargon. No counts-as-shorthand.** "You catch-and-log at 14 sites and propagate at 3" is exactly the phrasing to avoid — it assumes vocabulary the user may not share and states a statistic instead of a situation. Describe what's actually happening in the code, not a tally of it.

The worked example below is the model of the required voice — reproduced verbatim, not paraphrased, because the phrasing itself is the spec:

> **When something fails partway through — a database call times out, a file isn't there — the code has to decide who deals with it.**
> Right now this repo does both things. In most places, the failure is written to a log and the function quietly returns nothing, so whatever called it can't tell the difference between "no results" and "it broke." In a few places, the failure is handed back to the caller to decide.
>
> Doing both is how a bug hides for a week. Pick one:
>
> **A — Hand failures back to the caller.** Only the outer layer (the request handler, the CLI entry point) decides what the user sees. Nothing gets swallowed. More plumbing to write.
> **B — Deal with it where it happens.** Log it and carry on with a fallback. Less plumbing, but a failure can pass unnoticed.
>
> Most of this repo does B today. A is the safer default and what I'd suggest, but B is defensible if these failures are genuinely routine.

**Rules in the emitted artifact get the same treatment.** State the rule, then one sentence on what goes wrong without it — the same situation-first, plain-language discipline that governs the interview questions applies to the document they produce.

---

## 6. What makes a rule admissible

This is the load-bearing quality bar. It is what separates the output from a generic best-practices dump, and it is non-negotiable per rule — a rule that fails any test below does not ship.

- **Violable today.** If no code in this repo could break it, cut it.
- **Checkable.** A reviewer can point at a line and say violated / not violated.
- **Carries a because.** The rationale is what lets an agent generalize to the case the rule didn't anticipate.
- **Counter-example from this codebase**, where one exists.
- **Not lintable.** If a formatter or linter can enforce it mechanically, it is a config line, not a prose rule. Prose rules duplicating tooling are how a conventions doc rots. Standing rule: tooling produces configuration, not prose.
- **Dependencies named.** A rule that only holds because another rule established its precondition says which rule, and `rationale.md` carries the link.

**Banned strings** — a rule containing any of the following is not admissible, full stop: "write clean code", "keep it simple", "follow SOLID", "use meaningful names".

Two things travel with the rules in the emitted artifact:

- A **rejected-alternatives register** (`rationale.md`), so a future agent does not reopen a settled call.
- An **escalation clause**: when a situation isn't covered, name the ambiguity and ask. Don't improvise a rule, and don't treat silence as permission.

---

## 7. Non-goals

- Does not write or refactor source code.
- Does not replace a linter.
- Does not touch the project's `CLAUDE.md` without asking.
- Does not ask an open-ended question where it could show a draft instead.
- Does not have a drift-check or amend mode.

---

## 8. Known residual risk

A generated skill only helps if it triggers. The emitted `SKILL.md` description is written to fire hard on code-writing activity in that repo, but the only thing that makes loading *certain* — rather than probable — is a one-line pointer in the project's `CLAUDE.md`. `fudge:conventions` offers to add that pointer at the end of a run; **it never adds it by default.**

This is a real gap: a project that declines the `CLAUDE.md` pointer is trusting description-based triggering alone, which can misfire. The user explicitly chose the generated-skill output over a `CLAUDE.md`-based one, accepting this tradeoff — see decision 1 below.

---

## 9. Decision log

Design decisions made explicitly, with what was rejected and why.

Entries 6–8 came out of a dry run of the skill against a hypothetical Rails application, not from the original design conversation.

1. **Output location** — generated project skill under `.claude/skills/`.
   Rejected: writing rules directly into the project's `CLAUDE.md` with a reference file (guaranteed loading, but costs baseline context every session).
   Rejected: doing both.

2. **Scope** — started as cross-cutting "how code is written" only; expanded to the full surface including project structure, tooling, testing, and workflow. The final scope is the full surface, not the narrower starting frame.

3. **Modes** — generator only.
   Rejected: a drift-check mode reporting where code violates the contract and where the contract has fallen behind reality.
   Rejected: a lightweight amend mode folding in decisions made during real work.

4. **Tooling gaps** — propose the exact config and write it on approval.
   Rejected: recommend-only, never write (risks a contract that claims "formatter is a gate" while no formatter actually exists).
   Rejected: write configs automatically without per-run approval.

5. **Name** — `fudge:conventions`, chosen for the most obvious trigger words a user would type, accepting the collision with the emitted `<project>-conventions` artifact.
   Rejected: `fudge:house-rules`.
   Rejected: `fudge:code-charter`.
   Rejected: `fudge:groundwork`.

6. **Rule dependencies** — recorded by name in `rationale.md`: when a rule exists only because another rule created its precondition, that link is recorded, so reversing the upstream rule surfaces what depends on it instead of quietly invalidating it.

7. **Cross-round consistency check** — Phase 2 checks the accumulated rules across rounds for conflicts and silent dependencies before the table is shown. A conflict is resolved with the user, never papered over, and every resolution is recorded in `rationale.md` so it isn't re-argued later.

8. **Rule-count ceiling** — past 60 accumulated rules, Phase 2 offers a re-filter at a harder admissibility bar; 60 is a tunable starting threshold, not a hard law.
   Rejected: applying the re-filter automatically above the threshold.
   Rejected: a hard rule cap.
