---
name: fudge:setup
description: "Set up a project’s coding rules and local run readiness, audit convention drift, or amend approved rules. Use for project setup, running an existing project, focused tooling setup, project verification recipes, diagnosing failed project guidance, project-rule changes, working defaults, and everyday local stack operations (branch or worktree stacks, one-off tasks, dump restores, startup failures)."
---

# fudge:setup

## Locate guidance

Package addresses (`shared/`, `references/modules/`, `references/roots/`) resolve from the nearest ancestor with `.fudge-package.json`, or `scripts/skill-manifest.json` in source. Read `shared/locate.md` when resolving a source address or nested guide; this guide’s own references remain relative.

Use package-root `shared/execution.md` for implementation/delegation policy, `shared/writing.md` for prose, and `shared/artifacts.md` before writing run artifacts. Existing user decisions and authorization carry across handoffs. For a requested durable HTML report, read package-root `shared/report-deck/guide.md` for the shared plan runtime UI; concise chat is the default.

Set up a usable project by reusing its existing authority and run instructions. `fudge:setup` is this public skill; `<project>-conventions` is the project-specific rule artifact it may create. Preserve that distinction and never create competing sources of authority.

## Choose the mode

| Request | Route |
|---|---|
| Establish project coding rules | [Rule setup interview](references/setup-interview.md) |
| Set up one concern, such as error handling or test conventions | Focused rule setup: inspect that concern, draft concrete rules, show the exact table, emit after applicable approval |
| Check a change against approved rules | [Audit and amendment](references/audit-amend.md), read-only audit |
| Change an approved rule | [Audit and amendment](references/audit-amend.md), targeted amendment; exact-change approval or explicit standing review-learning grant |
| Set or change working defaults | [Working defaults](#working-defaults) below; show the exact section, write after approval |
| Install dependencies, prepare local prerequisites, start or explain how to run | [Run readiness](#run-readiness) below |
| Bring up a branch or worktree stack, stop or prune containers, run a one-off task, load a dump, fix a failing startup | [Environment operations](references/environment.md) |
| Create or maintain feature verification recipes | [Project verification](references/project-verification.md); reuse existing harnesses |
| Diagnose recurring failures of project guidance | [Guidance diagnosis](references/guidance-diagnosis.md), then targeted amendment if authorized |
| General project setup | Inspect both rules and readiness; address gaps within the requested scope |

Locate instructions, existing project skills, governing documents, tooling configs, and run documentation before acting. Ordinary patterns support a draft; they do not become approved rules by inference. If authority conflicts, surface the specific conflict before affected work. Prefer an existing project-skill directory or caller-supplied path; otherwise use the active host’s project location (`.codex/skills/` for Codex, `.claude/skills/` for Claude). For an unknown host, use its documented location or ask only if the choice affects loading.

## Rules and tooling

Read [writing rules](references/writing-rules.md) before proposing rules; use the [dimension bank](references/dimension-bank.md) only for relevant concerns. Inspect mechanically discoverable choices rather than asking the user to repeat them. Propose concrete alternatives for unsettled choices. A focused setup skips unrelated rounds.

Before creating or amending authoritative rules, show the exact rule table or amendment and obtain approval unless already authorized. An explicit standing grant to turn confirmed review gaps into gates or project-skill improvements covers narrow additive amendments that preserve established behavior: the coordinator must inspect the concrete delta, evidence, and verification within the reviewed work. It does not authorize new product decisions, weaker gates, changed approved policy, or broad new rulebooks. Otherwise approval of summaries does not approve unseen rules. Read [emitting](references/emitting.md) before emission. Record contested choices and dependencies in the rationale. Audit returns findings; rule work does not refactor application code. Use ship for requested implementation fixes.

For recurring, demonstrated mistakes, consider a deterministic check or tool that catches the actual failure instead of accumulating repeated prose. This adapts a selected idea from Cursor’s [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md). Prefer an existing harness; justify a new check by recurrence, consequence, and maintenance cost, and avoid brittle checks that merely match wording. Propose only proportionate changes within scope, validate the check against the failure and a valid case, and preserve the rule and tooling authorization boundaries above and below.

Tooling configs and instruction-file pointers require authorization for their concrete changes; reuse prior authorization rather than asking again. Use `AGENTS.md` for Codex or `CLAUDE.md` for Claude, respecting existing host instructions. Do not assume creating rules authorizes a commit, push, or deployment.

## Working defaults

Setup records and amends the project's working defaults (`endpoint`, `commit-push`, `external-writes`, `runtime`). Format, values, absent-key behavior and precedence live in package-root `shared/working-defaults.md`; follow it rather than restating it.

1. Find the governing rules: the `<project>-conventions` skill if one exists, else `AGENTS.md` or `CLAUDE.md`. Read any existing `## Working defaults` section.
2. Show the exact `## Working defaults` section as it will be written (full replacement text, or old and new lines for an amendment). Omit keys the user leaves unset.
3. Write only that section after approval, preserving everything else in the file. Prior approval of the exact contents applies.

The full rule interview asks about these once, in the workflow round ([setup interview](references/setup-interview.md)). Recording defaults is not a gate for routine work: absent keys fall back to skill defaults.

## Run readiness

1. Detect the stack and intended local target from manifests, lockfiles, runtime/version files, scripts, README, environment samples, containers, and service configs. Prefer the existing documented commands. Identify prerequisites, dependencies, required variable names, local services, ports, start/check/stop commands, and unresolved requirements. Do not print secret values or copy real credentials into artifacts.
2. “How do I run it?” requests instructions and gap diagnosis. “Set it up and run it” authorizes the necessary local dependency installation and startup within this project. Use the declared package manager and lockfile; reuse existing environments and services where appropriate. Do not silently change package versions or invent missing credentials. Install global/system prerequisites only when they are within explicit scope; otherwise report the concrete missing prerequisite while completing independent work. Under `runtime: docker-only` (working defaults), run toolchains and services in the project's containers and install nothing on the host.
3. Start only the requested local target. Avoid production endpoints and destructive migrations, resets, data deletion, or deployment unless specifically authorized. Inspect commands before running them so a misleading script name does not hide those effects. Apply ordinary local preparation already authorized by the request.
4. Capture process/session identity, exit status, relevant logs, local URL or entry point, and the actual readiness signal. A listening port alone may not establish application readiness: check the documented health endpoint or a representative page/operation when available. Redact sensitive logs. Report startup failures and what remains missing; never equate command launch with run success.
5. For an interactive app the user wants running, leave the healthy process available and give the URL and exact stop command or session control. For temporary verification, stop only processes you started and remove only temporary resources you created. Preserve pre-existing services and data. Document any installed dependencies or config changes and the observed verification.

Everyday stack operations beyond first run (branch or multi-repo stacks, one-off tasks, dumps, pruning) follow [environment operations](references/environment.md).

Examples: “Set up testing conventions” uses a focused rule draft. “Run this repo” checks instructions, installs missing local dependencies, starts the target, verifies readiness, and reports its URL. “Audit this diff” changes no rules or application code.
