# Shared execution policy

Use the host's available tools and current model choices. This policy does not assume a particular agent API, model vendor, editor, or isolation feature.

## Decide and scope

Read the relevant project instructions and perform one bounded discovery pass. Carry forward the user's scope, choices, and authorization. Follow existing naming, casing, API, and implementation patterns; exercise bounded judgment for routine reversible decisions. Escalate only consequential choices that remain unsettled and cannot be resolved from evidence. A narrow task does not need a new interview.

## Delegate when useful and available

Delegate cohesive implementation work when the host supports subagents and independent ownership saves time or improves review. Prefer one worker for a bounded change. Parallelize only independent files and decisions; serialize shared dependencies first. Use the current inherited model by default and select supported alternatives only when justified and permitted by the host. If delegation is unavailable, complete bounded work directly with the same scope and verification discipline.

Give each worker a self-contained brief with:

- Exact owned files, off-limits paths, requested behavior, and acceptance criteria.
- Settled decisions and authority to follow established patterns and resolve routine implementation details.
- Artifact destination and whether it is unused or an authorized edit.
- Targeted check commands and which broader gates the coordinator owns.
- No unauthorized publishing, history rewriting, discarding changes, or deleting unrelated files.
- A request to report genuine blockers or false premises, deviations, check commands, exit status, and accessible raw evidence.

Workers may adapt mechanical details within their scope. A false premise that invalidates the approach should be reported with evidence; do not invent a replacement scope. Resume the same worker for related corrections. Repeated failure calls for re-scoping or another approach, not indefinite retries.

## Verify outcomes

A success claim alone is not evidence. Inspect actual changed files, scope, and relevant observed outcomes before reporting success. Raw command output or recorded manual observations from a worker can count when accessible, attributable to the current revision and environment, and sufficient to verify the result. Do not rerun an expensive identical check solely to change who ran it. Rerun when evidence is missing, stale, ambiguous, or invalidated by later changes.

Workers may run fast targeted checks to self-correct. Coordinate full suites, builds, and other broad gates once when their coverage is needed. Select checks by the failures they can catch rather than habit. Current native editor diagnostics can be evidence; confirm their file revision and scope before acting. Stale diagnostics are not proof of a current defect.

After integration, verify the relevant outcomes, inspect the final diff and working state, and report material gaps plainly. Keep source facts, worker claims, raw observations, and judgments distinct. Never present inferred behavior as an observed pass.

## Protect collaboration

Keep ownership explicit and avoid concurrent edits to the same file unless isolation and integration are managed. Record commands against the revision or changed state they checked. Recheck repository status before concluding; investigate unexpected changes without reverting another person's work. While workers run, prepare review and verification. Report useful findings and next steps without narrating routine tool operations.
