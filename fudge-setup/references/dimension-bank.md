# Dimension bank

The full set of dimensions `fudge:setup` can turn into rules, grouped and typed. Phase 0 selects capability-dependent dimensions from observed code, planned architecture and project scope. Phase 1 groups the relevant dimensions into rounds.

## Legend

- **D** — detected from the repo, never asked.
- **A** — asked.
- **◇** — capability-dependent: include when the observed or approved planned capability applies.

Combined markers compose: **D+A** is detected first and confirmed or corrected with the user; **A◇** is asked, but only when the capability applies.

## Capability applicability

Use archetypes as discovery hints, not exclusions. A repository may have several surfaces. Detect implemented capabilities and include approved planned capabilities for greenfield work; ask only where an unresolved capability changes the rules.

| Dimension | Include when |
|---|---|
| Concurrency | Parallel jobs, async work, shared state, cancellation or concurrent callers exist or are planned |
| Persistence | Local files, SQLite, offline mobile storage, databases or other durable state exist or are planned |
| Third-party SDKs and HTTP clients | External integrations exist or are planned |
| Versioning and deprecation | Public APIs, persisted formats, library exports or independently released consumers need compatibility |
| Snapshot/golden tests | Stable text, visual, protocol or serialization output makes these useful |
| Changelog and release process | The project delivers releases or changes consumed independently |
| Observability and operations | Long-running processes, jobs, deployed services or operational support require signals and recovery |

For example, a SQLite CLI needs transaction rules, an offline mobile app needs persistence rules, and a public web API needs versioning rules. Prune a dimension only after confirming that neither current scope nor approved intended architecture needs it.

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
| Versioning and deprecation policy (for interfaces or formats with compatibility obligations) | A◇ |
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

Capability-dependent; include operational needs across product types.

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
3. **Observability and operations** — its own group, inserted here when current or approved planned operational capabilities need it.
4. **Testing** — Testing.
5. **Workflow** — Workflow, plus Tooling's two asked rows: pre-commit hooks, and the one command that checks everything. Both are about the loop around writing code rather than the code itself, so they run here rather than in a Tooling round of their own. The rest of Tooling is resolved by detection in Phase 0.5 and never reaches an interview round.
6. **Docs** — Documentation.
7. **Security** — Security. Consider the applicable security implications in full-project setup; focused setup remains scoped to its concern.

A full-project setup considers structure, architecture, testing, workflow, docs and security, grouping short topics where useful. Add observability after architecture when operational capabilities need it; focused setups consider only their relevant concerns.
