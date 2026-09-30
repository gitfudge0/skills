---
name: fudge:system-decomposition
description: Discover system responsibilities, capabilities, contracts, failures, and candidate work before tickets from a brief or product narrative. Use for system decomposition or explicit coaching in architectural decomposition; corpus reconciliation belongs to fudge:gap-analysis, choosing among directions to fudge:decision-room, and implementation to fudge:ship.
---

# fudge:system-decomposition

Turn an outcome into the smallest useful system model and a traceable candidate work breakdown. This is an optional specialist before ticket refinement; it does not implement the system or decide the user's product direction.

## Ground the model

Read the supplied brief or narrative. Preserve its terminology and cite source sections, pages, or code paths for material claims when available. Extract the outcome, scope, actors, critical journeys, constraints, authoritative data, and ownership boundaries.

For a change to an existing system, inspect the available architecture, relevant code, contracts, data ownership, and operational documentation before recommending components. Distinguish observed behavior from intended documentation. Reuse established boundaries when they fit; explain evidence for changing them. If access or evidence is missing, state that limitation and keep proposed changes conditional instead of inventing the current architecture.

Separate these labels throughout the analysis:

- **Known:** explicitly supported by the source or observed system; attach evidence.
- **Inferred:** a responsibility logically needed for the stated outcome; explain the derivation. This does not establish its implementation.
- **Assumption:** a provisional premise; state what fails if it is false.
- **Unknown:** missing or conflicting information that could change the model.
- **Proposal:** a design choice or recommendation, with the relevant tradeoff. A proposed component is not an inferred necessity.

For example, cross-system identity may require correlation; a dedicated identity service is a proposal. Do not turn a plausible solution into a source requirement.

## Discover responsibilities before work

Use this reasoning sequence, adapting depth to the request:

`Outcome → Journeys → Capabilities → System responsibilities → Contracts/states → Failure/operations concerns → Candidate work`

Read [architectural lenses](references/lenses.md) during decomposition. Apply relevant lenses, especially boundaries, identity, source of truth, permissions, lifecycle, partial failure, ordering/concurrency, migration, and operational ownership. A lens need not produce a work item.

For each consequential responsibility, consider what must be true, who guarantees it, what happens if it is false, how failure is detected, and how recovery or degradation works. Record unanswered questions instead of guessed guarantees. Keep volume, protocol, compliance requirements, retention, latency targets, and ownership unknown unless evidenced or agreed.

Trace candidate work to an outcome, responsibility, risk, or operational need. Group by capability; an investigation, migration, contract change, or operational stream can be a candidate item. Include dependencies, unresolved decisions, and observable acceptance evidence. If a decision blocks implementation, represent the investigation first and make subsequent work conditional. Candidate work is not a committed backlog or permission to implement.

Produce useful first-pass analysis before a long questionnaire. Rank questions by their ability to change boundaries, ownership, access, contracts, or major scope. Route sustained corpus reconciliation to `fudge:gap-analysis`, a requested comparison of alternative directions to `fudge:decision-room`, and authorized implementation to `fudge:ship`; retain the decomposition as the handoff context rather than silently expanding the task.

## Present or coach

Default to doing the analysis. Read [output guidance](references/output-contract.md) when composing the result. Start with the outcome and the issues that materially affect the model. A small brief may need only a short paragraph and a capability/work table; add diagrams and deeper contracts, states, failure, or operations detail when they improve understanding. There are no mandatory layers, row counts, or component quotas.

Every diagram must preserve provenance in its labels: identify source-supported or observed nodes, label every proposed node **Proposal**, and label every proposed edge **proposed**. Mark inferred relationships and assumptions explicitly too. Use a visible legend when helpful, but do not rely on color, dashed lines, or surrounding prose alone. Read the [worked example](references/example.md) when an ambiguous integration brief needs a model for distinguishing required responsibilities from design options.

Only when the user explicitly asks to practice, learn, or be coached, read [coaching protocol](references/coaching.md). The user can switch with `mode: fast`, `mode: training`, or `skip`. Do not add coaching exercises to ordinary analysis.

## Output location

Ordinary chat analysis needs no file writes. Save an artifact or learning log only when the user requests it or an authorized caller requires it. A supplied output path overrides the default; do not also write a second copy.

For saved output in a git repository, use `.fudge/<branch>/system-decomposition/` at the working-tree root from `git rev-parse --show-toplevel`. Obtain `<branch>` from `git branch --show-current`, replacing every `/` with `-`; on detached HEAD use `git rev-parse --short HEAD`. Outside git, use `.fudge/system-decomposition/` in the current directory unless the environment provides an artifact destination. Before the first default write in git, add `.fudge/` to the file named by `git rev-parse --git-path info/exclude` unless already listed. Never edit `.gitignore` for this.

Keep the saved output proportional to the request: a decomposition Markdown file is sufficient unless another format is requested. Do not create product code, tickets in external systems, or instruction-file pointers as a side effect of analysis.
