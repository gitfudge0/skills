# UI prototype

Internal capability: enter through the owning public skill. Resolve cross-module and shared paths from the package root (nearest ancestor containing `.fudge-package.json`): `references/modules/<module>/guide.md`, `references/roots/<root>/guide.md`, and `shared/`. In source, use the repository identified by `scripts/skill-manifest.json`, with `modules/`, `fudge-<root>/SKILL.md`, and `shared/`. Local assets and references remain relative to this guide.

Make a taskable, nonproduction draft that answers **one named interaction question**. Use the project's platform and conventions to choose a runnable artifact; use the least machinery that can express the behavior. A prototype tests a design assumption, not the completeness of the product.

## Define the test

1. State the person's task, the interaction question, and what observation would change the design. Identify the starting state, relevant branches, success condition, and failure or recovery path.
2. Check the project's design source, existing tokens, components, content, and platform constraints. Choose realistic sample content and only enough visual fidelity to make the task credible. Keep fabricated data safe and visibly synthetic where it could be mistaken for real records.
3. Choose an **exact unused output path** under this skill's Output location below. Keep prototype files and any run instructions there. Edit production components only when the user separately requests a component or product build.

## Output location

Follow package-root `shared/artifacts.md` for path resolution, caller overrides, collision handling, and repository exclusions. The default artifact category is `ui-prototype`. Product files retain their established project locations; a chat-only answer creates no artifact.

## Build a runnable task

- Implement the transitions the question depends on. A path shown as clickable must respond to the action, including relevant branch choices, Back, save/resume, retry, cancellation, and feedback where they affect the task. Avoid decorative controls that imply unsupported behavior; label any intentional dead end.
- Model persistence and reset deliberately. Specify what survives navigation, reload, and a new session; give the reviewer a clear way to reset the scenario and repeat the task. If persistence is simulated, say where the simulated state lives and how it differs from the intended product behavior.
- Make the artifact easy to open or run with a short, exact instruction. Prefer minimal dependencies and follow the project's runtime conventions. Show the scope and limitations near the artifact, especially any simulated backend, authentication, data, permissions, or network behavior.

## Inspect and learn

Run or open the prototype. Perform the key task yourself through consequential branches and recovery, checking rendered states at relevant sizes and input methods. Verify save/resume and reset against the stated persistence contract. Fix broken or misleading behavior before review.

If the remaining uncertainty depends on a person's behavior, invite the user to try **one focused task** with a neutral prompt and a clear starting state. Capture what happened separately from the agent's walkthrough and from simulated behavior. Use the ux-research module when planning or conducting participant research; never present an agent walkthrough as participant evidence.

Keep the artifact labeled **exploratory**. Feed validated design decisions and outstanding questions into the project's authoritative `DESIGN.md`, `COMPONENTS.md`, or equivalent document when those documents are in scope. Report the artifact path, how to run and reset it, the question answered, observed behavior, and limits. Do not claim that a simulated flow proves backend integration.

## Boundaries

- Use the ui-mock module for a static canvas of states or visual variants; use this skill when executable transitions are necessary to answer the question.
- Use `fudge:design` to coordinate a broader design package and its source documents. Its component-build mode or `fudge:ship` owns production implementation and verification.

## Minimal runnable example

For a three-step form recovery question, prefer one HTML file with synthetic records and a reset button. State the contract: navigation preserves in-memory input, reload clears it, and no real account or backend is used. If reload persistence is part of the question, use a namespaced session-storage key and make Reset remove only that key. Never store credentials or real personal data.

Open the file directly when possible. If a server is required, serve only the artifact directory on loopback (for example `python3 -m http.server 8765 --bind 127.0.0.1 --directory <prototype-directory>`), record the process/session, and stop only that process after verification unless keeping the preview running is part of the handoff. Isolate new dependencies inside the prototype directory; do not change the product lockfile to run a prototype. Report the exact run command, URL, reset behavior, and any remaining preview process.
