---
name: fudge:ui-prototype
description: Build a bounded, runnable UI prototype to test an interaction question before production work. Use when a static mock cannot show branching, navigation, persistence, recovery, or another consequential behavior.
---

# UI prototype

Make a taskable, nonproduction draft that answers **one named interaction question**. Use the project's platform and conventions to choose a runnable artifact; use the least machinery that can express the behavior. A prototype tests a design assumption, not the completeness of the product.

## Define the test

1. State the person's task, the interaction question, and what observation would change the design. Identify the starting state, relevant branches, success condition, and failure or recovery path.
2. Check the project's design source, existing tokens, components, content, and platform constraints. Choose realistic sample content and only enough visual fidelity to make the task credible. Keep fabricated data safe and visibly synthetic where it could be mistaken for real records.
3. Choose an **exact unused output path** under this skill's Output location below. Keep prototype files and any run instructions there. Edit production components only when the user separately requests a component or product build.

## Output location

Write this skill's files to `.fudge/<branch>/<skill>/` at the root of the current working tree (`git rev-parse --show-toplevel`), where `<skill>` is this skill's name without the `fudge-` prefix.

- `<branch>` is `git branch --show-current` with every `/` replaced by `-`. On a detached HEAD, use `git rev-parse --short HEAD`. Outside a git repository, use `.fudge/<skill>/` in the current directory.
- Before the first write, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless it is already listed. Never edit `.gitignore` for this.
- A path supplied by a calling skill overrides this default.
- Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

For this skill, `<skill>` is `ui-prototype`, so the default is an exact unused path under `.fudge/<branch>/ui-prototype/<slug>/`.

## Build a runnable task

- Implement the transitions the question depends on. A path shown as clickable must respond to the action, including relevant branch choices, Back, save/resume, retry, cancellation, and feedback where they affect the task. Avoid decorative controls that imply unsupported behavior; label any intentional dead end.
- Model persistence and reset deliberately. Specify what survives navigation, reload, and a new session; give the reviewer a clear way to reset the scenario and repeat the task. If persistence is simulated, say where the simulated state lives and how it differs from the intended product behavior.
- Make the artifact easy to open or run with a short, exact instruction. Prefer minimal dependencies and follow the project's runtime conventions. Show the scope and limitations near the artifact, especially any simulated backend, authentication, data, permissions, or network behavior.

## Inspect and learn

Run or open the prototype. Perform the key task yourself through consequential branches and recovery, checking rendered states at relevant sizes and input methods. Verify save/resume and reset against the stated persistence contract. Fix broken or misleading behavior before review.

If the remaining uncertainty depends on a person's behavior, invite the user to try **one focused task** with a neutral prompt and a clear starting state. Capture what happened separately from the agent's walkthrough and from simulated behavior. Use `fudge:ux-research` when planning or conducting participant research; never present an agent walkthrough as participant evidence.

Keep the artifact labeled **exploratory**. Feed validated design decisions and outstanding questions into the project's authoritative `DESIGN.md`, `COMPONENTS.md`, or equivalent document when those documents are in scope. Report the artifact path, how to run and reset it, the question answered, observed behavior, and limits. Do not claim that a simulated flow proves backend integration.

## Boundaries

- Use `fudge:ui-mock` for a static canvas of states or visual variants; use this skill when executable transitions are necessary to answer the question.
- Use `fudge:design` to coordinate a broader design package and its source documents. Its component-build mode or `fudge:ship` owns production implementation and verification.
