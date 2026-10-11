# Diagnose failed project guidance

Read for a confirmed recurring guidance failure, including a reusable PR review gap. Adapted from [reflect](https://github.com/cursor/plugins/tree/main/pstack/skills/reflect) and [correct](https://github.com/cursor/plugins/tree/main/pstack/skills/correct). A finding is not automatically a reason to add a rule.

Trace the concrete failure, applicable instruction, its authoritative location, and evidence of what was loaded or followed. Distinguish:

| Cause | Proportionate response |
|---|---|
| Missing guidance | Add the narrow judgment or contract that would have prevented the demonstrated failure. |
| Buried or conflicting guidance | Move, shorten, or reconcile the existing source; avoid a duplicate rule. |
| Missed trigger or routing | Repair the description, pointer, or conditional route so the needed guidance is discovered. |
| Noncompliance despite available guidance | Address execution or enforcement; more copies of the rule are unlikely to help. |

If loading evidence is unavailable, keep the diagnosis uncertain; do not claim a missed trigger from the final mistake alone. Prefer removing the structural cause, then suitable types, existing automated checks, or a meaningful regression test when they prevent the failure reliably. Use skill guidance for the residual judgment. Balance consequence, recurrence, maintenance cost, and scope; a one-off typo does not require a permanent gate.

Record finding → evidenced cause → chosen prevention → verification. Test a new check against a failing and valid case; for guidance, inspect realistic routing/decision cases and distinguish an authored scenario from an executed evaluation. Use the targeted amendment authorization rules in [audit and amendment](audit-amend.md). A standing learning grant covers only the narrow allowed changes; it does not authorize changing product behavior, weakening gates, or adding a broad rulebook.
