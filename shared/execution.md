# Shared execution policy

Use the host's available tools and current model choices. This policy does not assume a particular agent API, model vendor, editor, or isolation feature.

## Decide and scope

Read the relevant project instructions and perform one bounded discovery pass. Carry forward the user's scope, choices, and authorization. Follow existing naming, casing, API, and implementation patterns; exercise bounded judgment for routine reversible decisions. Escalate only consequential choices that remain unsettled and cannot be resolved from evidence. A narrow task does not need a new interview.

## Delegate when useful and available

Before implementation dispatch or direct editing, make a proportionate decomposition pass. Identify settled contracts, shared prerequisites, candidate independent lanes and their exact file ownership, order-dependent work, an integration owner, and the coordinator's verification gates. For a small change, a brief rationale and ownership/check list is enough; this does not require a separate system-decomposition stage or artifact.

Resolve shared prerequisites and consequential unsettled contracts before dependent lanes start. When the host supports subagents and independent ownership saves time or improves review, dispatch useful independent lanes in parallel. Do not prescribe an agent count or automatically split by architectural layer: disjoint files alone do not make work independent if interfaces or decisions remain unsettled. Use one cohesive worker when coordination overhead outweighs the benefit, and briefly explain why. Serialize dependent work and overlapping file ownership unless the host supports managed isolation and integration.

Assign integration explicitly to the coordinator or a worker: reconcile wiring and shared contracts after lanes land, inspect the combined result, then apply the coordinator-owned project and risk-relevant verification gates. Targeted worker checks do not replace verification of the integrated behavior. Use the current inherited model by default and select supported alternatives only when justified and permitted by the host. Honor the host's concurrency and tool constraints. If delegation is unavailable, complete bounded work directly with the same decomposition, scope, and verification discipline.

Give each worker a self-contained brief with:

- Exact owned files, off-limits paths, requested behavior, and acceptance criteria.
- Shared contracts and prerequisites, lane dependencies, and who owns integration; workers must preserve other contributors' edits.
- Settled decisions and authority to follow established patterns and resolve routine implementation details.
- Artifact destination and whether it is unused or an authorized edit.
- Targeted check commands and which broader gates the coordinator owns.
- No unauthorized publishing, history rewriting, discarding changes, or deleting unrelated files.
- A request to report genuine blockers or false premises, deviations, check commands, exit status, and accessible raw evidence.

Workers may adapt mechanical details within their scope. A false premise that invalidates the approach should be reported with evidence; do not invent a replacement scope. Resume the same worker for related corrections. Repeated failure calls for re-scoping or another approach, not indefinite retries.

## Frame, fan out, and aggregate

Adapted from Cursor's [swarm skill](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md). Apply this loop to delegated implementation using the active host's tools and limits.

Before dispatch, state the done condition and the artifact or report to return. Prefer independent slices for ordinary implementation. Use identical-brief races or a mix of slices and races only when comparing alternatives is useful or requested. Declare the race rule before launching: **first pass** selects the first candidate meeting acceptance conditions, **rank all** compares every completed candidate against stated criteria, and **best-of** selects the strongest candidate against those criteria. Assign each writing worker distinct owned files or isolated writable outputs; racing implementations must not edit the same working files.

Choose the total worker count from the useful slices or race arms, separately from the host's concurrency limit. Dispatch ready independent work up to that limit, queue the rest, and keep dependent work ordered. Each self-contained brief identifies its slice or race arm and the evidence required. For commit verification or comparisons, name exact revisions; for measurements, also define the method, sample count, what one sample measures, and execution order. Workers must record those details with their observations.

Drain every launched worker to a terminal result before aggregating; a first-pass winner does not leave other workers running unmanaged. Collect `PASS`, `ISSUES`, or `BLOCKED`, accessible evidence, all proven in-scope issues, and any deviations. A dropout is an explicit gap. If a result omits mandated evidence such as revisions or measurement method, exclude it from passing coverage and ask the same worker once to supply the missing evidence. A second miss remains a gap; do not retry indefinitely.

Aggregate the results against acceptance conditions and the declared race rule. Every required slice needs sufficient evidence; worker agreement and missing slices do not count as passes. Inspect and integrate the chosen outputs under the coordinator's verification gates. Return one concise report of evidenced outcomes, issues, and gaps or dropouts, including the race rule when used; use a compact result table when it aids comparison rather than pasting worker transcripts.

## Verify outcomes

A success claim alone is not evidence. Inspect actual changed files, scope, and relevant observed outcomes before reporting success. Raw command output or recorded manual observations from a worker can count when accessible, attributable to the current revision and environment, and sufficient to verify the result. Do not rerun an expensive identical check solely to change who ran it. Rerun when evidence is missing, stale, ambiguous, or invalidated by later changes.

Workers may run cheap focused checks while implementing to self-correct; do not impose separate per-lane verification gates or duplicate full suites across workers. After integration, the coordinator runs the required broad build, test, lint, and other project gates once per integrated round when their coverage is needed. Later fixes require relevant rechecks for affected behavior and dependencies, while unaffected current evidence remains valid. Select checks by the failures they can catch rather than habit. Current native editor diagnostics can be evidence; confirm their file revision and scope before acting. Stale diagnostics are not proof of a current defect.

After integration, verify the relevant outcomes, inspect the final diff and working state, and report material gaps plainly. Keep source facts, worker claims, raw observations, and judgments distinct. Never present inferred behavior as an observed pass.

## Protect collaboration

Keep ownership explicit and avoid concurrent edits to the same file unless isolation and integration are managed. Record commands against the revision or changed state they checked. Recheck repository status before concluding; investigate unexpected changes without reverting another person's work. While workers run, prepare review and verification. Report useful findings and next steps without narrating routine tool operations.
