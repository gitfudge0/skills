# Environment operations

Use for the everyday local and test-environment work that follows first-run readiness: bringing up a stack for a branch, stopping it, running a one-off task, loading a dump, or fixing a startup that fails. Run readiness in `SKILL.md` still governs detection, secrets, readiness signals and cleanup of what you started; this reference adds the per-operation boundaries.

## Ground rules

- **Use the project's own path.** Prefer existing scripts, Makefile/task targets, compose files, runbooks and README steps over ad hoc commands. Read a script before running it so its name does not hide a reset, deletion or remote call.
- **Honor working defaults.** Read the `## Working defaults` section (package-root `shared/working-defaults.md`). Under `runtime: docker-only`, run tools, migrations and services inside the project's containers and install nothing on the host; report a missing image or service instead.
- **Name the target.** Every operation states which environment it touches: local, a named local stack, or a named remote environment. When the request leaves it unclear and the choice matters, ask.
- **Propose, do not silently add, convenience scripts.** When the same sequence repeats or the documented steps have a gap, show the exact script or target and where it would live; add it only with authorization.
- **Never print secrets.** Report variable names, not values; redact logs.

## Confirmation boundaries

| Operation | Needs explicit confirmation |
|---|---|
| Start, restart, or stop local containers and processes | No, within the request |
| Remove stopped containers, networks, dangling images you or the stack created | No, within the request |
| Remove volumes, local databases, caches with data, or backups | Yes; name each volume/database and what data is lost |
| One-off task locally | No, unless it resets or deletes data |
| One-off task in a shared, staging or production environment | Yes; show the exact command, target environment and expected effect, then run only that command |
| Load a database dump | Only into an isolated local container; never into a shared environment |

A later "go ahead" covers the command that was shown, not a changed one.

## Bring up a stack for a branch or worktree

1. Identify the repos in the stack (for example a server repo and a web repo) from compose files, docs and env samples. For each, resolve the checkout to use: the given worktree, or the matching branch. Report a repo without a matching branch and say which ref you used instead.
2. Check for port, container-name and volume collisions with stacks already running for other branches or worktrees. Reuse the project's isolation mechanism (compose project name, port overrides, per-worktree env files) when one exists; otherwise report the collision rather than stopping another stack.
3. Start dependencies first (databases, queues), then apply pending migrations through the project's command, then start the apps. Seed only through documented seed tasks.
4. Verify readiness with a health endpoint or a representative page or API call per app, not just open ports.
5. Report, per app: URL, the branch/ref and worktree path, seeded logins only if the project documents them (never invent credentials), and the exact stop command. Leave the stack running.

## Stop and prune

Stop the named stack with the project's command (or `docker compose down` for its compose project). Prune only what belongs to that stack. Volumes, databases and backups follow the confirmation row above; list them with sizes when available before asking. Do not touch other branches' stacks or unrelated containers.

## Run a one-off task

Migrations, rake/manage/npm/make scripts, seeds and backfills:

1. Find the documented way to run it in the target environment (container exec, task runner, runbook, remote console script). Do not improvise a remote access path.
2. State the target environment and whether the task writes data. For backfills, prefer a dry-run or count mode if the task offers one, and report its result first.
3. Locally, run it. For a shared, staging or production target, show the exact command and wait for confirmation per the table above.
4. Report exit status, relevant output, and any rows or records changed when the task reports them.

## Restore a database dump for testing

Load a provided dump only into an isolated local database container: a fresh container or a database name that no other stack uses. Confirm the dump's format and source version match the local engine, and check that the target is not a shared host before loading. Report the container, database name, connection details without secrets, and the stop/remove command. Treat dump contents as sensitive: do not copy them into artifacts, logs or commits.

## Diagnose a failing startup

1. Capture the first real error from logs, not the last line.
2. Check the usual causes against the project's docs: missing directories or mounts, unset env variables (compare to the env sample), missing or stale images, unapplied migrations, port conflicts, wrong runtime versions.
3. Fix within the documented setup: create documented directories, copy env samples with placeholder values the user must fill, pull or build documented images, run documented migrations. Do not change application code, package versions or committed config to make startup pass.
4. If the documented setup itself is wrong or incomplete, report the gap and propose the doc or script change; apply it only with authorization.
5. Re-run startup and report the readiness signal, or the remaining blocker.
