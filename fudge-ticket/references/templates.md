# Ticket templates

Use these when the project has no ticket template of its own. Keep the headings in order; write `None` for a section that does not apply rather than deleting it. Avoid untestable qualifiers such as "properly", "gracefully" or "as expected".

## Story list (first pass)

```
1. <Imperative user-facing outcome, ≤ 10 words> — <one line: what it delivers, what it defers>
2. ...
Deferred: <work intentionally left out of every story above, or None>
```

## Story

Title: ≤ 10 words, imperative, user-facing outcome. No component prefixes or ticket numbers.

```markdown
## Context
2–3 sentences: who has the problem, what happens today, why now. No implementation detail.

## Outcome
As a <actor>, I can <capability>.

## Acceptance criteria
1. Given <state>, when <action>, then <observable result>.
2. ...
(Prefer a short set. More than five signals a scope check, not an automatic split. Prefix with (Web) or (Mobile) only where clients diverge.)

## Out of scope
- <deferred path, rule, platform or data range a reader might assume is included>
```

Each criterion establishes an observable outcome for the story’s consumer. Visible failure behavior earns a criterion; include retries or timeouts here when they are part of the promised outcome. For technical stories, replace the actor/capability wording with the operational consumer and verifiable technical result.

## Subtask (when an implementation slice helps)

Title: `[Server|Web|Mobile] <technical outcome>`.

```markdown
## Goal
One sentence. Delivers AC <n–m>.

## Implementation notes
- <endpoint, model, migration, component; real paths only when read>
- <decisions left to the implementer>
(Or: > Needs developer detail — <why>. Open questions: <specific questions>.)

## Touch points
- API contract: <change, or None>
- Data: <migration/backfill, or None>
- Older clients: <what a client on the current release sees, or None>
- Flag / rollout: <flag, or None>

## Done when
- [ ] <verifiable condition>
- [ ] Tests covering <behavior>
```

## Reconcile diff

```markdown
## Reconciled with <PR links> (merged <date> into <branch>)

### Updated description
<rewritten Context / Outcome / Acceptance criteria matching the merged code>

### Deviations from the original ticket
| Original | As built | Evidence |
|---|---|---|
| <criterion or statement> | <what the code does> | <PR, file:line or commit> |

### Test notes
- <how QA exercises each built behavior; preconditions, accounts, flags>

### Related ticket drafts
- <Title> — <deferred or newly discovered work, one line>
```

## QA handoff comment

```markdown
Merged and ready for QA.

PRs:
- <repo>#<n> <title> — merged into <branch> <date>

What to test:
- <behavior 1, mapped to AC n>
- <behavior 2>

Environment / setup: <env, flag, test account, data needed, or None>
Known limits: <deferred items or follow-up tickets, or None>
```

Pair it with the exact transition name read from the tracker and the looked-up assignee.

## Comment reply drafts

```markdown
> <quoted comment, author, date>

Reply: <answer | agreed change and where it lands | question back>
Action: <none | code fix needed (hand to ship on request) | ticket update>
```

One block per open comment, in thread order.
