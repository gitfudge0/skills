# Dimension bank

The full set of dimensions `fudge:conventions` can turn into rules, grouped and typed. Phase 0 prunes the archetype-gated dimensions before the interview starts. Phase 1 runs what survives across six or seven rounds.

## Legend

- **D** — detected from the repo, never asked.
- **A** — asked.
- **◇** — archetype-gated: pruned in Phase 0, before the interview starts.

Combined markers compose: **D+A** is detected first and confirmed or corrected with the user; **A◇** is asked, but only if the archetype survives the Phase 0 gate.

## Archetype gating

Archetype classification happens before any question is asked. It prunes roughly a third of the question bank — a library is never asked about health checks, a CLI tool is never asked about transaction boundaries. The table below is the full picture of which ◇ dimensions survive the gate for each archetype.

| Archetype | Enabled ◇ dimensions | Pruned ◇ dimensions | Notes |
|---|---|---|---|
| Library | Versioning and deprecation policy · Third-party SDKs and HTTP clients · Changelog and release process | Concurrency · Persistence · Snapshot/golden tests · Observability and operations (whole group) | Versioning and deprecation is dominant for libraries. Observability is pruned — a library is never asked about health checks. |
| CLI tool | Versioning and deprecation policy · Third-party SDKs and HTTP clients · Changelog and release process · Snapshot/golden tests | Concurrency · Persistence · Observability and operations (whole group) | Persistence is pruned — a CLI tool is never asked about transaction boundaries. Observability is pruned: not a service, web app, or data pipeline. |
| Long-running service | Concurrency · Persistence · Third-party SDKs and HTTP clients · Observability and operations (whole group) | Versioning and deprecation policy · Snapshot/golden tests · Changelog and release process | Versioning and deprecation is pruned — irrelevant for an internal service. Observability is enabled per the Phase 1 rule. |
| Web app | Concurrency · Persistence · Third-party SDKs and HTTP clients · Snapshot/golden tests · Observability and operations (whole group) | Versioning and deprecation policy · Changelog and release process | Observability is enabled per the Phase 1 rule. |
| Data pipeline | Concurrency · Persistence · Third-party SDKs and HTTP clients · Snapshot/golden tests · Observability and operations (whole group) | Versioning and deprecation policy · Changelog and release process | Observability is enabled per the Phase 1 rule. |
| Embedded | Concurrency · Versioning and deprecation policy · Changelog and release process | Persistence · Third-party SDKs and HTTP clients · Snapshot/golden tests · Observability and operations (whole group) | Observability is pruned: not a service, web app, or data pipeline. |
| Mobile | Concurrency · Third-party SDKs and HTTP clients · Snapshot/golden tests · Changelog and release process | Persistence · Versioning and deprecation policy · Observability and operations (whole group) | Observability is pruned: not a service, web app, or data pipeline. |

Only the library/versioning, service/versioning, library/observability, CLI/persistence, and the service-web app-pipeline observability calls come from the spec directly. The rest follow the obvious shape of each archetype — whether it holds persistent state, runs concurrent work, or has external consumers of a stable interface — and are not spelled out in the spec itself.

## The eight dimension groups

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

## Groups to interview rounds

The eight groups above do not map one-to-one onto interview rounds. Two fold into other rounds instead of running on their own.

1. **Structure** — Project structure.
2. **Architecture** — Architecture and patterns.
3. **Observability and operations** — its own group, inserted here only when the archetype is a long-running service, web app, or data pipeline. For every other archetype this round is skipped and the interview stays at six rounds.
4. **Testing** — Testing.
5. **Workflow** — Workflow, plus Tooling's two asked rows: pre-commit hooks, and the one command that checks everything. Both are about the loop around writing code rather than the code itself, so they run here rather than in a Tooling round of their own. The rest of Tooling is resolved by detection in Phase 0.5 and never reaches an interview round.
6. **Docs** — Documentation.
7. **Security** — Security. Asked in full even when the user says "keep it light" — never defaulted away.

Six rounds run on every project: structure, architecture, testing, workflow, docs, security. The seventh — observability — is archetype-gated and only ever inserted after architecture.
