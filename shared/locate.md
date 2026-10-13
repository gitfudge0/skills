# Locating guidance

Every guide addresses bundled guidance by package address: `references/modules/<name>/guide.md`, `references/roots/<name>/guide.md`, or `shared/<path>`. Resolve those addresses from the package root before opening them, even when the referring guide is nested.

## Find the package root

1. Walk ancestors of the referring guide to the nearest directory containing `.fudge-package.json`. That directory is the installed package root.
2. If there is none, you are in a source checkout: the root is the ancestor containing `scripts/skill-manifest.json`.

## Map addresses

| Address | Installed package | Source checkout |
|---|---|---|
| Primary root (the installed skill itself) | package-root `SKILL.md` | `fudge-<name>/SKILL.md` |
| `references/roots/<name>/guide.md` | same path under the package root | the root's source `SKILL.md` (`fudge-<name>/SKILL.md`, or the manifest's declared `source`) |
| `references/modules/<name>/guide.md` | same path under the package root | `modules/<name>/guide.md`, unless the manifest declares another `source` and `entry` (HTML planning uses `plan/SKILL.md`) |
| `shared/<path>` | same path under the package root | unchanged: `shared/<path>` |

Bundling rewrites a reference to the package's own primary root to `SKILL.md`; public roots are never copied into their own `references/roots` directory.

## Local references

Links to a guide's own resources (for example `references/<file>.md` beside a root's `SKILL.md`, or a module's own `references/`) stay relative to that guide's file, not the package root. Read only the guidance selected for the current task.
