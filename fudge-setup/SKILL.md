---
name: fudge:setup
description: "Set up a project’s coding rules and local run readiness, audit convention drift, or amend approved rules. Use for project setup, running an existing project, focused tooling setup, and project-rule changes."
---

# fudge:setup

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. All `references/modules/`, `references/roots/`, and `shared/` paths below are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; module guides are `modules/<name>/guide.md`, root guides are `fudge-<name>/SKILL.md`, and shared paths are unchanged. The primary installed root is package-root `SKILL.md`; other root guides are under `references/roots/<name>/guide.md`. Bundling rewrites a reference to the primary root to `SKILL.md`. Links to this guide's own references remain relative to this file. Read only the selected guidance.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing review artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read optional package-root `shared/report-deck/guide.md`; concise chat is the default.

Set up a usable project by reusing its existing authority and run instructions. `fudge:setup` is this public skill; `<project>-conventions` is the project-specific rule artifact it may create. Preserve that distinction and never create competing sources of authority.

## Choose the mode

| Request | Route |
|---|---|
| Establish project coding rules | [Rule setup interview](references/setup-interview.md) |
| Set up one concern, such as error handling or test conventions | Focused rule setup: inspect that concern, draft concrete rules, show the exact table, emit after applicable approval |
| Check a change against approved rules | [Audit and amendment](references/audit-amend.md), read-only audit |
| Change an approved rule | [Audit and amendment](references/audit-amend.md), exact-change approval |
| Install dependencies, prepare local prerequisites, start or explain how to run | Run readiness below |
| General project setup | Inspect both rules and readiness; address gaps within the requested scope |

Locate instructions, existing project skills, governing documents, tooling configs, and run documentation before acting. Ordinary patterns support a draft; they do not become approved rules by inference. If authority conflicts, surface the specific conflict before affected work. Prefer an existing project-skill directory or caller-supplied path; otherwise use the active host’s project location (`.codex/skills/` for Codex, `.claude/skills/` for Claude). For an unknown host, use its documented location or ask only if the choice affects loading.

## Rules and tooling

Read [writing rules](references/writing-rules.md) before proposing rules; use the [dimension bank](references/dimension-bank.md) only for relevant concerns. Inspect mechanically discoverable choices rather than asking the user to repeat them. Propose concrete alternatives for unsettled choices. A focused setup skips unrelated rounds.

Before creating or amending authoritative rules, show the exact rule table or amendment and obtain approval unless the conversation already explicitly approves those contents. Approval of summaries does not approve unseen rules. Read [emitting](references/emitting.md) before emission. Record contested choices and dependencies in the rationale. Audit returns findings; rule work does not refactor application code. Use ship for requested implementation fixes.

For recurring, demonstrated mistakes, consider a deterministic check or tool that catches the actual failure instead of accumulating repeated prose. This adapts a selected idea from Cursor’s [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md). Prefer an existing harness; justify a new check by recurrence, consequence, and maintenance cost, and avoid brittle checks that merely match wording. Propose only proportionate changes within scope, validate the check against the failure and a valid case, and preserve the rule and tooling authorization boundaries above and below.

Tooling configs and instruction-file pointers require authorization for their concrete changes; reuse prior authorization rather than asking again. Use `AGENTS.md` for Codex or `CLAUDE.md` for Claude, respecting existing host instructions. Do not assume creating rules authorizes a commit, push, or deployment.

## Run readiness

1. Detect the stack and intended local target from manifests, lockfiles, runtime/version files, scripts, README, environment samples, containers, and service configs. Prefer the existing documented commands. Identify prerequisites, dependencies, required variable names, local services, ports, start/check/stop commands, and unresolved requirements. Do not print secret values or copy real credentials into artifacts.
2. “How do I run it?” requests instructions and gap diagnosis. “Set it up and run it” authorizes the necessary local dependency installation and startup within this project. Use the declared package manager and lockfile; reuse existing environments and services where appropriate. Do not silently change package versions or invent missing credentials. Install global/system prerequisites only when they are within explicit scope; otherwise report the concrete missing prerequisite while completing independent work.
3. Start only the requested local target. Avoid production endpoints and destructive migrations, resets, data deletion, or deployment unless specifically authorized. Inspect commands before running them so a misleading script name does not hide those effects. Apply ordinary local preparation already authorized by the request.
4. Capture process/session identity, exit status, relevant logs, local URL or entry point, and the actual readiness signal. A listening port alone may not establish application readiness: check the documented health endpoint or a representative page/operation when available. Redact sensitive logs. Report startup failures and what remains missing; never equate command launch with run success.
5. For an interactive app the user wants running, leave the healthy process available and give the URL and exact stop command or session control. For temporary verification, stop only processes you started and remove only temporary resources you created. Preserve pre-existing services and data. Document any installed dependencies or config changes and the observed verification.

Examples: “Set up testing conventions” uses a focused rule draft. “Run this repo” checks instructions, installs missing local dependencies, starts the target, verifies readiness, and reports its URL. “Audit this diff” changes no rules or application code.
