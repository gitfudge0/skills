# Fudge skills

Six public skills cover project setup, requirements discovery, implementation, design, UX, review, and interactive planning. Specialist capabilities are bundled as internal guides so each installed root works independently.

| Public skill | Purpose | Internal capabilities |
|---|---|---|
| `fudge:ship` | Discover requirements, implement, verify, deliver | Engineering, verification, PR delivery and review learning, gap analysis, system decomposition, interactive HTML planning, test planning, decision pressure-testing; routes to design, UX, review, setup |
| `fudge:review` | Review a PR or local diff | Findings, re-review, conventions checks |
| `fudge:design` | Shape and build the visual experience | Visual craft, design systems, static mocks, prototypes, design QA |
| `fudge:ux` | Shape the experience people need | Research, content architecture, interaction design, accessibility, measurement |
| `fudge:setup` | Establish project rules and make a project runnable | Conventions setup, audit, amendment, startup readiness, project verification recipes, guidance diagnosis |
| `fudge:plan` | Create interactive HTML implementation plans | Runtime, block references, and examples; also bundled into ship |

Ship is a router with a task-to-guide map: focused engineering and verification modules, native PR delivery guidance, and conditional comprehensive/recovery references. Shared execution remains the single delegation and integration policy. Git implementation defaults to an isolated worktree and PR-ready delivery; explicit local-only and analysis endpoints remain available. A narrow request goes directly to its module. Asking for button labels does not start a mock workflow; asking what's missing before building can stop at requirements analysis. Rendering a report deck is optional. Mindmap has been removed.

## Install

Requires Python 3.9+ and Bash. Clone this repository, then run:

```sh
./install.sh
./install.sh -a codex -y
./install.sh -a claude -a codex --all -y
./install.sh -a codex --root ship --copy -y
./install.sh -a codex --root plan -y
./install.sh list
./install.sh remove -a codex --all -y
```

Supported terminals use a four-step keyboard installer: agents → roots → method → review. Use arrows to move, Space to select, Enter to continue, Esc to go back, and q to cancel. Back preserves selections. Narrow or unsupported terminals use numbered choices. Conflicts appear before applying changes. Defaults select all six roots. Supported targets: Claude, Codex, Cursor, OpenCode. Non-interactive installation requires an explicit target (`-a`); it applies without a prompt. `-y` bypasses interactive confirmation. Non-interactive removal requires `-y`.

The installer offers six public roots. Each package includes its dependency closure, internal guides, and shared policies. Symlinks point to generated `.fudge-build` packages; copies include an installer ownership marker and can be updated by rerunning the installer.

### Migration

`--root conventions` selects `setup`. Legacy `--skill` names select their owning root: for example, `--skill ui-mock` selects `design`, and `--skill gap-analysis` and `--skill system-decomposition` select `ship`. `--no-roots --skill NAME` remains a migration form. `--skill plan` selects the standalone public skill. Legacy `html-plan` and `fudge-html-plan` selections remain migration aliases for `plan`. `--skill mindmap` and explicit `write` selections report their removal.

Installation removes retired entries only when they are owned by this checkout's installer and their owning root was selected. Explicitly removed mindmap entries are also cleaned up; removed Write entries are cleaned up on default/all installations. Selecting standalone `plan` migrates owned legacy `html-plan` and `fudge-html-plan` entries to `fudge-plan`; selecting `ship` preserves them. Review lists planned cleanup before confirmation. Recognized ownership is an exact installer link target (including old dangling links), or a copy marker containing this checkout's path. Foreign directories, manual copies, and unrelated dangling links are preserved. A foreign entry at a selected public destination blocks installation without overwriting it.

## Source and package layout

```text
fudge-{ship,review,design,ux,setup}/SKILL.md
modules/<capability>/guide.md
plan/SKILL.md                  # standalone public skill, also bundled into ship
shared/{execution.md,writing.md,artifacts.md,artifact_path.py}
shared/report-deck/
scripts/skill-manifest.json
```

The manifest declares module ownership, optional source entry filenames, root dependencies, and optional package names. Existing Fudge roots keep their `fudge-` package names; standalone HTML planning installs to `fudge-plan` and is invoked with `/fudge:plan`. HTML planning reuses the standalone `plan/` source as a ship module, including its runtime, block reference, and examples; it is also available as the standalone `fudge-plan` package through `--root plan` or `--skill plan`. Node.js is required only to pack an HTML plan. The builder computes a closure with no recursive root copies. An installed package contains:

```text
SKILL.md
references/                         # public root's native resources
references/modules/<name>/guide.md  # internal modules and their resources
references/roots/<name>/guide.md    # routed roots and their native resources
shared/
.fudge-package.json
```

Package addresses resolve from the directory containing `.fudge-package.json`; local guide resources resolve relative to that guide. In a source checkout, the manifest identifies the repository and maps package addresses to source guides. Routes to the primary root become package-root `SKILL.md`; other roots use `references/roots/<name>/guide.md`. Public roots are not copied into their own `references/roots` directory.

## Checks

```sh
bash scripts/build-root-skills.sh .fudge-build
bash tests/install-smoke.sh
```

The builder validates manifest ownership, dependency closure, package addresses, and local Markdown links before replacing generated packages. It refuses to replace unmarked output directories. Installer tests cover defaults, standalone roots, copy updates, migration, foreign-entry protection, and invalid references. Behavioral scenarios in `tests/evals/scenarios.json` define routing, scope, verification, and recovery checks against observable outcomes rather than wording. They are declarative evaluation cases; the build and smoke suite do not execute agent behavior evaluations. Ship uses cause tracing, contract-aware implementation, and risk-based verification; formal reporting and durable recovery are selected independently of engineering risk. It reuses current check and audit evidence and requires observed post-deployment checks for a deploy endpoint.

Shipping behavior fixtures and the independent evaluation protocol are in [tests/evals/ship-behavior.md](tests/evals/ship-behavior.md). Generate a fresh isolated fixture tree and run its external acceptance checks; these checks supplement transcript review and do not establish a speed benchmark.

Write is retired as a public skill. Shared prose guidance remains bundled for every skill. A default/all install removes only this checkout’s installer-owned legacy `fudge-write` entries; manual and foreign entries remain untouched.

Conditional capabilities stay with their owners: setup maintains project verification recipes and diagnoses failed guidance; ship engineering handles behavior-preserving refactors and measured optimization; verification and review check test effectiveness; verification exercises relevant retry/restart risks; durable ship runs preserve auditable attempts. These references load only for the applicable work, not for every task. Behavioral scenarios describe expected decisions; they are not executed agent evaluation results.
