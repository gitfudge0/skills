# Project verification recipes

Use when asked to create or maintain reusable application verification, or when a ship run has a demonstrated harness gap. Adapted from [create-verification-skill](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill). This mode may create scoped verification instructions, helpers, and checks within authorization; audit and rule-emission modes retain their own restrictions. Product fixes belong to ship.

## Reuse and prove

Inspect existing project verification skills, scripts, tests, run documentation, and local service controls first. Maintain the authoritative existing recipe rather than creating another harness or host-specific duplicate. Use the project's skill location/pointer; settle only consequential loading ambiguities. Map the selected feature to its real product entry point and acceptance signals. A repository-wide feature inventory is useful only for a request of that scope; a PR does not require verifying every feature.

A reusable recipe should identify:

- **Launch:** exact observed commands, prerequisites and variable names, local target, process/session identity, and service ownership.
- **Doctor:** readiness and dependency checks that establish usable application state, not just an open port.
- **Drive:** concrete user/API operations through the actual product path, scoped fixtures, starting state, and expected observable results. Internal setters or mocks do not establish a user flow.
- **Evidence:** checked revision/environment, commands or interaction observations, errors, and durable artifact locations. Never capture secrets; state any external dependency or unverified boundary.
- **Cleanup:** exact stop/remove operations for resources the verification owns. Preserve existing services and data; retain evidence outside disposable fixture directories.

Use small per-feature entries linked to shared launch/doctor/cleanup instructions, keeping commands in one source. Include only supported host operations; do not require unavailable browser, trace, or live instrumentation tools. If a tool is missing, report the gap or use an available method that proves the same acceptance signal.

Exercise each new or changed recipe end to end, including cleanup, against the intended local target before describing it as verified. Capture actual observations and confirm evidence survives cleanup. If execution is blocked, label the recipe unverified and name the missing step. An invented command or an unrun scripted path is not reusable evidence.

## Diagnose drift before editing

Separate **documentation drift** (the supported application/harness works but the recipe is stale), **harness gap** (the relevant behavior lacks a reliable observable path or helper), and **product regression** (the intended behavior itself fails). Update observed documentation for drift; repair or add a proportionate harness for a proven gap; route product defects into ship's scoped fix/review loop. Do not change expected behavior to excuse a failing product. Recheck the affected recipe after changes, retaining unrelated current recipes.
