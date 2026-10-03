# Artifact paths and ownership

Locate the package root via the ancestor `.fudge-package.json`; in the source checkout use the ancestor containing `scripts/skill-manifest.json`. The helper is `<package-root>/shared/artifact_path.py` in both layouts. Product code, tests, authoritative project documents, and project skills stay in their existing project locations. This policy concerns review artifacts and run metadata.

Caller-supplied destinations take precedence exactly. Resolve relative paths from the caller's working directory. Never silently redirect an explicit destination or overwrite an existing file. If it exists, resume/update it only when that is explicitly intended; otherwise choose a new destination with the caller. For an explicit file path, reserve its parent as appropriate and create the file exclusively; the helper reserves directories, not files.

Default artifacts belong under `.fudge/<encoded-branch>/<skill>/<run-name>[-N]/` at the current worktree root. Outside Git, use `.fudge/<skill>/<run-name>[-N]/` beneath the caller's directory. Detached HEAD uses its full commit identity. A PR review uses the PR head branch as `--branch`. Encoding preserves branch identity: `feature/a` and `feature-a` cannot collide. Never guess the Git root or assume `.git` is a directory; worktrees use their own discovered paths.

Resolve read-only:

```sh
python3 <package-root>/shared/artifact_path.py --cwd <project> --skill ship --name 2026-10-03-feature
```

Reserve the unused default directory and locally exclude its artifacts:

```sh
python3 <package-root>/shared/artifact_path.py --cwd <project> --skill ship --name 2026-10-03-feature --mkdir --exclude
```

For an exact unused directory, add `--output <destination>`. The helper emits JSON containing `path`, `root`, `git`, `default`, and `created`. `--mkdir` reserves a directory atomically and refuses an existing explicit destination. Read-only resolution does not reserve it; re-resolve with `--mkdir` before writing to avoid a race. `--exclude` only changes the repository-local exclude file when a default artifact directory was created inside a Git worktree. It never edits `.gitignore` or changes exclusions for external/caller paths.

Use exclusive creation for new artifact files. Keep immutable versions for reviewed test matrices, snapshots, and reports when their earlier contents support a decision. Identified run indexes and re-review state may be deliberately updated; preserve history that remains relevant. Do not clean up another run or pre-existing artifacts. Report actual absolute paths and meaningful verification, and avoid including secrets or unrelated untracked content in snapshots.
