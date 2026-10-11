# Preserve behavior while refactoring

Read when restructuring existing implementation while preserving its contract. Adapted from poteto-mode's [refactoring playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md) and [architect](https://github.com/cursor/plugins/tree/main/pstack/skills/architect).

Pin the starting revision/file state and representative behavior before restructuring. Reuse existing tests; add characterization or capture old outputs only where an otherwise unprotected contract matters. Record which quirks are contractual and which are known defects; do not silently fix behavior during a behavior-preserving request.

Inventory internal callers, configuration/import references, data readers/writers, and relevant external consumers. Sketch realistic caller usage before changing an interface; keep ownership clear instead of adding shallow wrappers or leaking internals. Migrate owned callers together and remove obsolete internal paths/references when compatibility permits. Preserve externally supported APIs and staged migration paths until their documented compatibility conditions are met; an internal census does not prove there are no external consumers.

Compare old/new outcomes on representative accepted inputs, errors, and meaningful state transitions, using isolated baselines when needed. Verify unchanged observable contracts and affected callers, not just the new structure. Report incomplete equivalence evidence. Limit cleanup to obsolete task-owned paths; do not make unrelated architecture or whole-repo testing a requirement.
