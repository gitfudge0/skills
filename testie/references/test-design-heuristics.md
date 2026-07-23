# Test design heuristics

Reference material for step 4 of the workflow. Use these as prompts to generate candidate cases, not as a checklist to mechanically exhaust — the filtering step in SKILL.md is what keeps the output right-sized.

## Edge-case checklist

Run the changed behavior through whichever of these actually apply. Most changes only trigger 3-5 of these, not all of them — that's expected.

- **Zero, one, many.** Anywhere something is counted (results, items, retries, characters): does it work at zero, exactly one, and a large number? Watch for off-by-one, divide-by-zero, and pluralization/grammar bugs at the boundaries.
- **Boundary values.** For any range (age 18-65, file size limits, timeouts, pagination): test the min, the max, and one step outside each. Defects cluster at edges far more than in the middle of a range.
- **Some, none, all.** Anywhere there's a set (permissions, selected items, tags, checkboxes): does "none selected" get treated differently from "all selected"? A common real bug is "no permissions" silently behaving like "all permissions" because of a falsy/undefined check gone wrong.
- **Too small, too big, just right (Goldilocks).** For any valued input — string length, upload size, numeric magnitude — check both extremes, not just a mid-range valid value.
- **Invalid / malformed / missing input.** Null, empty string, wrong type, malformed format (bad email, bad date), input that's technically valid but semantically nonsensical (negative quantity, end-date before start-date).
- **Never and always.** State the rules this code must never violate and must always uphold (a user must never see another user's data; a total must always equal the sum of its parts) — then write a case that tries to break each rule directly.
- **Follow the data.** If data moves through multiple steps (entered → validated → saved → displayed → exported), check integrity survives the whole path, not just entry. Bulk/import paths often skip validation that direct entry enforces — check both if both exist.
- **State and order.** If the feature is stateful (wizard, session, workflow, cache): test out-of-order actions, repeated actions, and interrupted sequences (navigate away mid-flow, resume later), not just the linear path.
- **Concurrency and interruption.** Where relevant: two actions racing (two updates to the same record), network loss or timeout mid-action, app backgrounded/killed mid-flow. Only include this where the feature is genuinely concurrent or interruptible — don't force it onto single-user synchronous logic.
- **Permission/role variation.** If different users see different things, test the boundary between roles, not just "logged in vs. logged out" — the interesting bugs are usually at the edge of a permission tier, not its center.
- **Disfavored use.** What does a careless or adversarial user do that a careful one wouldn't — double-submitting a form, pasting a huge string into a small field, replaying an old request? Include this when the blast radius of misuse is real (payments, auth, content that gets published); skip it for low-stakes internal tooling.

## Risk scoring (drives priority)

Score each candidate case on two axes, then combine:

**Likelihood** — how probable is it this exact condition occurs in real use?
- Common: happens in normal, expected usage
- Occasional: happens under specific but plausible conditions
- Rare: requires an unusual combination of circumstances

**Impact** — how bad is it if this fails?
- Critical: data loss/corruption, security/privacy leak, crash, money handled incorrectly
- Functional: a real feature doesn't work, wrong result shown, but contained and recoverable
- Cosmetic: visual/UX issue, no functional or data consequence

Combine into a priority:
- **Critical** — Critical impact regardless of likelihood, or Common × Functional
- **High** — Occasional × Critical, or Common × Functional (borderline), or anything touching auth/payments/data integrity
- **Medium** — Occasional × Functional, or Rare × Critical
- **Low** — Cosmetic impact, or Rare × Functional

Use this to decide depth (step 4 in SKILL.md), not just to label cases after the fact — if something scores Low, that's a signal to write one case and move on, not three.

## Oracle questions (how would you actually know it's wrong?)

Before finalizing a case's "expected result," check it against these — if you can't answer them, the case isn't concrete enough yet:

- Is this consistent with what the spec/ticket/design actually says (not what you assume it probably says)?
- Is this consistent with how a similar, already-working feature in this product behaves?
- Is this consistent with what a reasonable user would expect, given the labels/copy they see?
- Is this consistent with the product's own internal logic (does it contradict something else the product guarantees elsewhere)?

If the expected result only checks "the code did what the code does" (e.g. asserting the mock returned what you told it to return), it's not really testing anything — cut it or rewrite it against one of the oracles above.
