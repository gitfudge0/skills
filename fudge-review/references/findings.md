# findings.json and method.md

Both files live in the output location from SKILL.md. `findings.json` is the only source for every render. A renderer reads it and never adds to it.

## findings.json

```json
{
  "pr": { "repo": "owner/name", "number": 61, "url": "", "base": "main", "head_branch": "", "head": "<sha reviewed>" },
  "round": 1,
  "reviewed_at": "<ISO-8601>",
  "ci": "passed | failed | pending | none",
  "verdict": "needs-changes | mergeable-after-fixes | mergeable",
  "findings": [{
    "id": "R1", "severity": "blocker | should-fix | nit",
    "topic": "correctness | security | contract | conventions | tests | quality",
    "title": "", "cause": "", "impact": null, "fix": "", "where": ["path:line"],
    "confidence": "verified | suspected", "evidence": "how it was checked",
    "origin": "introduced | pre-existing", "audience": "author | team",
    "rule": null, "status": "open | dropped | fixed | no-longer-applies",
    "status_reason": null, "round_found": 1
  }],
  "prior_comments": [{ "author": "", "url": "", "summary": "", "status": "agree | disagree | rebuttal-checked", "note": "" }]
}
```

Field notes:

- `pr.head` is the sha this round reviewed. The next re-review starts after it.
- `ci` value `none` renders as "No CI ran".
- `verdict` and the counts in the verdict line come from open findings with audience `author`. Team findings don't change the verdict.
- `title`, `cause`, `impact`, and `fix` follow the word caps in SKILL.md. `impact` stays `null` unless the harm isn't visible in the title.
- `where` lists one or more locations. The first is the main one.
- `evidence` says what you read or traced, at which sha. For a suspected finding, it says what would settle it.
- `rule` is `null` unless `topic` is `conventions`. Then it holds the rule and its source file, e.g. `"Services return a Result, never raise (AGENTS.md)"`.
- `status_reason` is required for `dropped` and `no-longer-applies`. For a triage downgrade or edit, `status` stays `open` and `status_reason` records what changed and why.
- `prior_comments[].note` is one line. For `rebuttal-checked`, it says whether the author's reasoning held against the code.

## method.md

Plain markdown, short. It holds:

- CI status, as read from `gh pr checks` or supplied by ship.
- Files read fully, skimmed, and not read. Group them by directory when the list is long.
- One line per prior comment with its status.
- What was not checked, and why.

Example:

```markdown
CI: passed (4 checks).

Read fully: app/services/admin/*, app/controllers/admin/support_staff_controller.rb
Skimmed: spec/services/admin/*
Not read: db/schema.rb (generated)

Prior comments:
- @reviewer-a, missing index on email: agree.
- @author, "invite is sent by the callback": rebuttal-checked. No callback sends it at head.

Not checked: mailer templates, which this PR doesn't touch.
```

## Re-review status rules

Start from the stored file. Review only commits after `pr.head`.

- `open` becomes `fixed` when the code at the new head removes the cause. Update `evidence` with how you checked.
- `open` stays `open` when the cause is still there. Update `where` if the lines moved.
- `open` becomes `no-longer-applies` when the code it pointed at is gone or changed so the finding no longer makes sense. Say why in `status_reason`.
- A `fixed` finding that comes back returns to `open` and keeps its ID. Note the regression in `status_reason`.
- `dropped` stays `dropped`.
- New findings take the next unused ID. Set `round_found` to the new round.
- Add prior comments posted since the last round, with statuses.
- Update `pr.head`, `round`, `reviewed_at`, `ci`, and `verdict`.

## Worked examples

From a real review. Both are should-fix.

Rendered:

> 🟠 **R1 Admin creates staff → no invite arrives; staff can never sign in**
> Cause: the invite call is commented out, and nothing re-sends it later.
> Fix: hold the UI until the follow-up lands; the follow-up backfills accounts never sent an invite.
> Where: `app/services/admin/create_support_staff_service.rb:28`

> 🟠 **R2 Physician enters patient's email → form says 'taken'**
> Cause: the check searches every account type, with no rate limit.
> Impact: confirms that a person is a patient in the system.
> Fix: add `rate_limit`; leave patient accounts out of the check.
> Where: `app/controllers/admin/support_staff_controller.rb` (`validate_email`)

R2 carries an Impact line because its title shows a wrong message, not the privacy leak behind it. R1 has none, because "can never sign in" is already the harm.

As stored (the `evidence` text is illustrative):

```json
[
  {
    "id": "R1", "severity": "should-fix", "topic": "correctness",
    "title": "Admin creates staff → no invite arrives; staff can never sign in",
    "cause": "The invite call is commented out, and nothing re-sends it later.",
    "impact": null,
    "fix": "Hold the UI until the follow-up lands; the follow-up backfills accounts never sent an invite.",
    "where": ["app/services/admin/create_support_staff_service.rb:28"],
    "confidence": "verified",
    "evidence": "Read the service at head: line 28 is commented out. git grep at head finds no other caller of the invite.",
    "origin": "introduced", "audience": "author",
    "rule": null, "status": "open", "status_reason": null, "round_found": 1
  },
  {
    "id": "R2", "severity": "should-fix", "topic": "security",
    "title": "Physician enters patient's email → form says 'taken'",
    "cause": "The check searches every account type, with no rate limit.",
    "impact": "Confirms that a person is a patient in the system.",
    "fix": "Add `rate_limit`; leave patient accounts out of the check.",
    "where": ["app/controllers/admin/support_staff_controller.rb (validate_email)"],
    "confidence": "verified",
    "evidence": "Traced validate_email at head: the lookup has no account-type filter, and the controller has no rate_limit.",
    "origin": "introduced", "audience": "author",
    "rule": null, "status": "open", "status_reason": null, "round_found": 1
  }
]
```
