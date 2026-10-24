# Working on this repository

Follow [shared execution guidance](shared/execution.md) for task scope, delegation, authorization reuse, and verification. Use the tools and models available in the active host; no fixed model or Codex-only tool is required.

The thirteen public skill sources are `fudge-ship`, `fudge-review`, `fudge-design`, `fudge-ux`, `fudge-setup`, `plan`, `fudge-investigation`, `fudge-bug-fix`, `fudge-hillclimb`, `fudge-prototype`, `fudge-visual-parity`, `fudge-ticket`, and `fudge-retro`. Feature implementation and refactoring remain in ship. Internal capability guides live under `modules/`; common policies and rendering resources live under `shared/`.

Keep ownership and dependencies in `scripts/skill-manifest.json` current. Build with `bash scripts/build-root-skills.sh .fudge-build` and run `bash tests/install-smoke.sh` after packaging or installer changes. Behavioral scenarios are in `tests/evals/scenarios.json`; `bash scripts/run-evals.sh --generate-only` converts them for `Codex plugin eval` (running cases costs money; run only when asked).

Preserve existing user edits. Prior authorization remains valid; do not introduce another approval gate for routine implementation choices.
