# Rendering

Render from `findings.json` only, and leave out dropped findings. In orchestrated mode the root-approved set is the only source. The render pass never adds, removes, merges, splits, or reclassifies a finding.

## Layers

1. **Verdict.** One line, always, in the format from SKILL.md.
2. **List.** One line per finding: severity, ID, title, area. Add `SUSPECTED` or `pre-existing` after the title when they apply.
3. **Detail.** Cause, Impact (only when present), Fix, Rule (conventions only), Where. Where is always last.

After the findings come two short blocks. **For the team** lists `team` findings, one line each (title, then fix), and is skipped when there are none. **Method** summarizes `method.md`, collapsed where the medium allows it and 2 to 4 lines in chat.

## Depth

Depth depends on how many author findings you render.

- **Up to 4.** Flat. Verdict, then each finding with its detail. No separate list.
- **5 to 14.** Verdict, the one-line list, then detail on demand (collapsed, threaded, or below the list).
- **15 or more.** Same as 5 to 14, plus a "Fix these first" list of the few that matter most, in order, and a "Not worth your time" note naming what the author can skip.

Grouping is a separate choice, driven by the PR's shape. One repo and one area gets no headings. One repo with several areas groups by area. A cross-repo change groups by repo. A 40-file PR with 2 findings renders flat with repo labels. A 3-file PR with 12 findings renders fully layered with no headings.

On a re-review, render only the delta, in three groups: fixed, still open, new.

## Chat

The default medium. Verdict, the one-line table when depth calls for it, detail, then Method. At 15 or more findings, give nits a table line only and add their detail when asked.

Example with the two worked findings (2 findings, so flat):

```
Mergeable after fixes — 0 blockers · 2 should-fix · 0 nits · CI: passed

🟠 R1 Admin creates staff → no invite arrives; staff can never sign in
Cause: the invite call is commented out, and nothing re-sends it later.
Fix: hold the UI until the follow-up lands; the follow-up backfills accounts never sent an invite.
Where: app/services/admin/create_support_staff_service.rb:28

🟠 R2 Physician enters patient's email → form says 'taken'
Cause: the check searches every account type, with no rate limit.
Impact: confirms that a person is a patient in the system.
Fix: add rate_limit; leave patient accounts out of the check.
Where: app/controllers/admin/support_staff_controller.rb (validate_email)

Method: CI passed. Read 6 files fully, skimmed 3, skipped 1 generated.
2 prior comments: 1 agree, 1 rebuttal-checked (the callback doesn't send the invite).
Not checked: mailer templates.
```

With 5 or more findings, put a table between the verdict and the detail:

```
|    | ID | Finding | Area |
|----|----|---------|------|
| 🟠 | R1 | Admin creates staff → no invite arrives; staff can never sign in | admin staff |
```

## Slack

Show the full message and thread to the user and wait for a yes before posting.

The message holds the verdict and the one-line list, then stops. Show the area, not file paths. Slack has no collapse, so the thread holds the detail at every depth:

- one reply per blocker
- then one reply with every should-fix, then every nit, with the Method lines at the end

```
Mergeable after fixes — 0 blockers · 2 should-fix · 0 nits · CI: passed
example-org/admin-portal #61

🟠 R1 Admin creates staff → no invite arrives; staff can never sign in · admin staff
🟠 R2 Physician enters patient's email → form says 'taken' · admin staff

Detail in thread
```

Thread reply:

```
🟠 R1 Admin creates staff → no invite arrives; staff can never sign in
Cause: the invite call is commented out, and nothing re-sends it later.
Fix: hold the UI until the follow-up lands; the follow-up backfills accounts never sent an invite.
Where: create_support_staff_service.rb:28

🟠 R2 Physician enters patient's email → form says 'taken'
Cause: the check searches every account type, with no rate limit.
Impact: confirms that a person is a patient in the system.
Fix: add rate_limit; leave patient accounts out of the check.
Where: support_staff_controller.rb (validate_email)

Method: CI passed · 6 read fully, 3 skimmed · 2 prior comments checked
```

## GitHub (`pr`)

Show the summary comment and every inline comment to the user and wait for a yes before posting.

Post one summary comment. It holds the verdict as a heading, the one-line list as a table, one `<details>` block per finding, the team section, and Method in its own `<details>` block. Then post one inline review comment per blocker, anchored to its line. The inline comment is one sentence plus a pointer to the summary. Never copy the full finding inline.

````markdown
## Mergeable after fixes — 0 blockers · 2 should-fix · 0 nits · CI: passed

|    | ID | Finding | Area |
|----|----|---------|------|
| 🟠 | R1 | Admin creates staff → no invite arrives; staff can never sign in | admin staff |
| 🟠 | R2 | Physician enters patient's email → form says 'taken' | admin staff |

<!-- one <details> block per finding; R1's is left out here -->
<details>
<summary>🟠 R2 Physician enters patient's email → form says 'taken'</summary>

**Cause.** The check searches every account type, with no rate limit.
**Impact.** Confirms that a person is a patient in the system.
**Fix.** Add `rate_limit`; leave patient accounts out of the check.
**Where.** `app/controllers/admin/support_staff_controller.rb` (`validate_email`)
</details>

<details>
<summary>Method</summary>

CI passed. Read 6 files fully, skimmed 3, skipped 1 generated. ...
</details>
````

An inline comment for a blocker:

```
🔴 R3: the refund is issued before the order is locked. Detail in the summary comment.
```

## HTML

Default path: `.fudge/<branch>/review/review.html`. A path from a calling skill overrides it; write there and create only its parent directory.

Build the page by copying `assets/example-review.html` and replacing its content. Follow `assets/design-system.md` for tokens, type, and components. These bundled assets win over any report or template that happens to exist in the repo under review. HTML suits cross-repo reviews, 15 or more findings, and constraints a chat message would bury, such as deploy order.

What goes where:

```
header           eyebrow (repo, PR, round), headline = verdict sentence,
                 meta line (branch · commit vs base · PR link · date · CI)
stats row        open blockers / should-fix / nits, plus fixed (re-review)
filter row       severity + status, combinable
.erow sections   findings grouped by status or severity, or by area/repo
                 when grouping calls for it; each finding an .item with
                 its ID, the title, then cause / impact / fix / rule / where
For the team     one line per team finding, when there are any
Method           divider pill, then a collapsed <details> block
```

Severity renders as pills, never emoji. `SUSPECTED` and `pre-existing` render as muted pills next to the severity pill.
