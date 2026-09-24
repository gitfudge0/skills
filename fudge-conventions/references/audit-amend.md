# Audit and amend existing conventions

Use this reference only for audit or targeted amendment. The authoritative project instructions and project-specific conventions skill are the rule source. `fudge:conventions` coordinates the check; it does not become a competing rulebook.

## Audit a bounded change

1. Identify the exact change to inspect: a diff against a named baseline, a PR diff, or a supplied file set. Record the baseline and paths. Keep pre-existing code separate from code introduced or modified by this change.
2. Read the project's applicable instruction files, their pointers, and the relevant sections of its existing conventions skill. Read tooling configuration when a claimed rule is enforced there. If there is no actionable project rule source, report that gap to the caller; do not manufacture a rule from common code patterns.
3. Compare each applicable rule with the change. For every finding, give the rule and its source, the changed location and observed behavior, and the consequence. Classify it as:
   - **Violation:** the change conflicts with an unambiguous approved rule. State the smallest correction or exception decision needed.
   - **Ambiguity or gap:** the rule is missing, conflicting, or cannot decide this case. Present the options and a recommendation; do not present it as a violation.
   - **Improvement proposal:** evidence suggests a rule may need changing. Describe repeated examples or a concrete failure, the benefit, cost, and dependencies. One new code pattern is not evidence that the convention should change.
4. State which applicable rules were checked without findings. Mark any rules you could not assess and why. A clean audit means no observed violation within the stated scope, not a claim that the whole repository conforms.

The audit changes neither code nor conventions nor tooling. Return it in chat. Write a report only when the user requests one or an authorized calling workflow supplies a run-local path; default to `fudge:conventions`'s Output location (`.fudge/<branch>/conventions/`) unless the user or a calling workflow names another path. `fudge:ship` may supply that path without a second user approval. Keep the same read-only result and do not touch project rule files. When called by `fudge:ship`, send violations to its implementation/review loop and proposals to the user. Do not silently waive a violation, patch code, or amend a rule to make the change pass.

## Make a targeted amendment

Resolve the authoritative file first. If rules are split across `.claude/skills/`, `.codex/skills/`, `AGENTS.md`, `CLAUDE.md`, or other project documents, follow the project pointer and amend the actual rule source. If two sources conflict or the target is unclear, show that conflict and obtain the user's choice before editing. Never create a parallel conventions file as a shortcut.

Show the user a focused proposal before any write:

- Exact rule text or diff, with the old wording and proposed wording. Include `rationale.md` changes when its decision or dependency record must change.
- Evidence for the change, the alternatives considered, and why the new rule is worth enforcing. A single implementation detail does not establish a project-wide rule.
- Named dependent rules, related tooling or pointers, and the effect of leaving them unchanged. Separate any tooling or instruction-pointer change for its own approval.

Wait for explicit approval of the exact proposal. Approval of an audit, feature, or PR is not approval to change the project contract. If the proposal changes after feedback, show it again. Then edit only the approved rule source and its necessary rationale/dependency text; preserve unrelated rules and the existing skill location. Do not rerun the full setup interview. Do not alter source code. Do not commit, push, change tooling, or add instruction pointers unless separately authorized. Read the resulting diff to confirm that it matches what the user approved.
