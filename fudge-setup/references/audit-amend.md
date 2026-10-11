# Audit and amend existing conventions

Use this reference only for audit or targeted amendment. The authoritative project instructions and project-specific conventions skill are the rule source. `fudge:setup` coordinates the check; it does not become a competing rulebook.

## Audit a bounded change

1. Identify the exact change to inspect: a diff against a named baseline, a PR diff, or a supplied file set. Record the baseline and paths. Keep pre-existing code separate from code introduced or modified by this change.
2. Read the project's applicable instruction files, their pointers, and the relevant sections of its existing conventions skill. Read tooling configuration when a claimed rule is enforced there. If there is no actionable project rule source, report that gap to the caller; do not manufacture a rule from common code patterns.
3. Compare each applicable rule with the change. For every finding, give the rule and its source, the changed location and observed behavior, and the consequence. Classify it as:
   - **Violation:** the change conflicts with an unambiguous approved rule. State the smallest correction or exception decision needed.
   - **Ambiguity or gap:** the rule is missing, conflicting, or cannot decide this case. Present the options and a recommendation; do not present it as a violation.
   - **Improvement proposal:** evidence suggests a rule may need changing. Describe repeated examples or a concrete failure, the benefit, cost, and dependencies. One new code pattern is not evidence that the convention should change.
4. State which applicable rules were checked without findings. Mark any rules you could not assess and why. A clean audit means no observed violation within the stated scope, not a claim that the whole repository conforms.

The audit changes neither code nor conventions nor tooling. Return it in chat. Write a report only when the user requests one or an authorized calling workflow supplies a run-local path; default to the setup artifact location resolved through package-root `shared/artifacts.md` unless the user or a calling workflow names another path. `fudge:ship` may supply that path without a second user approval. Keep the same read-only result and do not touch project rule files. When called by `fudge:ship`, send violations to its implementation/review loop. Send proposals to the user unless the targeted amendment route is already authorized; an audit itself remains read-only. Do not silently waive a violation, patch code, or amend a rule to make the change pass.

For recurring guidance failures, first use [guidance diagnosis](guidance-diagnosis.md) to distinguish missing instructions from placement, routing, or noncompliance before proposing another rule.

## Make a targeted amendment

Resolve the authoritative file first. If rules are split across `.claude/skills/`, `.codex/skills/`, `AGENTS.md`, `CLAUDE.md`, or other project documents, follow the project pointer and amend the actual rule source. If two sources conflict or the target is unclear, show that conflict and obtain the user's choice before editing. Never create a parallel conventions file as a shortcut.

Prepare a concrete focused proposal before any write; show it to the user when new approval is required:

- Exact rule text or diff, with the old wording and proposed wording. Include `rationale.md` changes when its decision or dependency record must change.
- Evidence for the change, the alternatives considered, and why the new rule is worth enforcing. A single implementation detail does not establish a project-wide rule.
- Named dependent rules, related tooling or pointers, and the effect of leaving them unchanged. Assess authorization for each concrete tooling or instruction-pointer change separately. A narrow tooling gate may fall under an explicit review-learning grant; instruction-pointer changes require specific authorization. Obtain new approval only when the change falls outside existing authorization.

Require explicit approval of the exact proposal unless the conversation already approves its contents or explicitly grants an ongoing review-learning loop. Under that standing grant, the coordinator may authorize a narrowly scoped additive gate or existing project-skill amendment backed by a confirmed reusable gap, preserving established behavior and policy; inspect the exact diff and include it in the same review and verification cycle. Record the finding, cause, delta, and verification. New product decisions, weakening gates, changed approved policy, or broad new rules still require the user’s decision. Approval of an audit, feature, or PR is not approval to change the project contract. If the proposal changes after feedback, reassess authorization and show it again when a new user decision is required. Then edit only the authorized rule source and its necessary rationale/dependency text; preserve unrelated rules and the existing skill location. Do not rerun the full setup interview. Do not alter source code. Do not commit, push, change tooling, or add instruction pointers unless separately authorized. Read the resulting diff to confirm that it matches the authorized scope and concrete proposal.
