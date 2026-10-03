# Working on this repository

Follow [shared execution guidance](shared/execution.md) for task scope, delegation, authorization reuse, and verification. Use the tools and models available in the active host; no fixed model or Claude-only tool is required.

The five public skill sources are `fudge-ship`, `fudge-review`, `fudge-design`, `fudge-ux`, and `fudge-setup`. Internal capability guides live under `modules/`; common policies and rendering resources live under `shared/`.

Keep ownership and dependencies in `scripts/skill-manifest.json` current. Build with `bash scripts/build-root-skills.sh .fudge-build` and run `bash tests/install-smoke.sh` after packaging or installer changes. Behavioral scenarios are in `tests/evals/scenarios.json`.

Preserve existing user edits. Prior authorization remains valid; do not introduce another approval gate for routine implementation choices.
