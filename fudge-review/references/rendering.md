# Rendering

Render from `findings.json` only, and leave out dropped findings. In orchestrated mode the root-approved set is the only source. The render pass never adds, removes, merges, splits, or reclassifies a finding.

## Layers

1. **Verdict.** One line, always, in the format from SKILL.md.
2. **List.** One line per finding: severity, ID, title, area. Add `SUSPECTED` or `pre-existing` after the title when they apply.
3. **Detail.** Cause, Impact (only when present), Fix, Rule (conventions only), Where. Where is always last. HTML uses the shared HTML plan claim tree with recorded evidence (see HTML below).

After the findings come two short blocks. **For the team** lists `team` findings, one line each (title, then fix), and is skipped when there are none. **Method** summarizes `method.md`, collapsed where the medium allows it and 2 to 4 lines in chat.

## Depth

For chat and other text media, depth depends on how many author findings you render. HTML always uses the shared HTML plan claim tree, including a single finding.

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

Resolve the unique default review directory through package-root `shared/artifacts.md`; place `review.html` there. A caller supplies its exact destination. Preserve existing artifacts unless deliberately re-rendering the identified review.

Use the actual bundled HTML plan renderer, not a review-specific imitation. Copy `assets/example-review.src.html`, replace only its recorded review content, and pack it with the shared runtime. `assets/example-review.html` is the portable packed example, generated from that source. HTML keeps the same numbered claim tree, parent rows, contents rail, comment controls and floating comment/response UI as HTML plan. Do not add custom CSS, layout overrides, separate statistics, filter rows, severity sections, flat field lists, or a second findings summary.

Resolve the shared runtime from the package root:

- Source checkout: `plan/runtime/` beside `fudge-review/`.
- Installed review package: `references/roots/plan/runtime/`.
- Review bundled inside another root: the same package-root `references/roots/plan/runtime/`.

The review root declares an `plan` root dependency so all three runtime files (`htmlplan.css`, `htmlplan.js`, `pack.mjs`) travel with the review package. Do not copy a fork of these files into review assets. The source template uses checkout-relative links `../../plan/runtime/htmlplan.css` and `../../plan/runtime/htmlplan.js`. For an unpacked installed preview or a source copied to a review output directory, replace only those two link paths with paths to the resolved shared runtime. The packer resolves linked basenames from its own runtime directory as a fallback, so it can also pack the unchanged bundled source inside an isolated installed package.

Source-checkout example:

```sh
node plan/runtime/pack.mjs fudge-review/assets/example-review.src.html -o fudge-review/assets/example-review.html
```

Installed-package example, run from the package root:

```sh
node references/roots/plan/runtime/pack.mjs assets/example-review.src.html -o /absolute/review/output/review.html
```

For a real report, pack the edited review source at its caller-resolved output location instead of overwriting the bundled example. The packed report inlines the exact shared CSS/JS and works offline. External PR links are navigation only. No reviewed repository files need to be available during rendering.

## HTML review tree

The first heading names the review. Immediately below it, render the complete recorded subject-aware verdict line and CI qualifications, then repository, PR or local scope, round, head/base and date metadata. Use the shared header typography and metadata classes. Do not replace the verdict with a planning goal.

Inside `doc-plan open="0"`, author findings are top-level `doc-claim` elements organized by affected behavior, never by files or implementation steps. A finding's first child is a `p` with stable `R<n>` ID text, its exact symptom title, severity, status, and applicable confidence/origin exceptions. Give the claim `id="R<n>"` so links and comments retain the finding identity. Use only shared runtime `span.pill` classes: `red` for blocker, `amber` for should-fix, neutral for nit, `green` for fixed. Exact shared UI takes precedence over the older review-specific fill/outline treatment. Keep `SUSPECTED` and `pre-existing` visible while the claim is closed; verified/introduced are implicit defaults.

Example shape:

```html
<doc-plan open="0">
  <doc-claim id="R2">
    <p>R2 · Slow charge outlasts the job timeout → customer is charged twice
      <span class="pill red">blocker</span>
      <span class="pill">open · still open</span></p>
    <doc-note><strong>Fix.</strong> Recorded fix text.</doc-note>
    <doc-claim id="R2-cause">
      <p>Recorded cause text.</p>
      <doc-code lang="text" title="Recorded evidence · R2">
<script type="text/plain">
Recorded evidence text.
</script>
</doc-code>
      <doc-claim id="R2-where" at="retry-worker/src/queue-consumer.ts:41-63">
        <p><code>retry-worker/src/queue-consumer.ts:41-63</code></p>
        <doc-code lang="text" title="Recorded locations · R2">
<script type="text/plain">
retry-worker/src/queue-consumer.ts:41-63
</script>
</doc-code>
      </doc-claim>
    </doc-claim>
  </doc-claim>
</doc-plan>
```

Opening a top-level claim uses the shared runtime's behavior: it opens descendants too. The numbered tree is navigation; the recorded R IDs are review identity. Do not substitute separate native disclosures or customize runtime numbering. Level 2 states the recorded cause and shows one exhibit containing the existing `evidence` string verbatim. Put block source inside the shared runtime's inert `script type="text/plain"` wrapper, as the template does. Level 3 shows the recorded Where locations last, with an `at` attribute for the main location. A plain-text `doc-code` can display evidence or recorded locations; its use does not assert an executable source excerpt. A real code excerpt is allowed only if already present in approved evidence. Never add `src`, `ref`, source-reading `doc-calls`, fabricated code, or fresh source retrieval during packing.

Colocate the recorded Fix in a `doc-note` under the finding. Include optional Impact when recorded, optional conventions Rule when recorded, and `status_reason` when needed to explain a recorded status outcome. Preserve suspected evidence and what would settle it. Keep one recorded exhibit per claim and at most three levels. Do not change findings or the schema to satisfy the visual tree.

End with auxiliary `doc-claim` blocks labelled “For the team” (`aux="team"`, omitted when empty) and “Method and coverage” (`aux="method"`). The runtime accepts arbitrary auxiliary labels and uses an asterisk instead of numbered behavior claims. Use the existing team title/fix and method coverage content, with stable IDs. For zero author findings, place “No author findings in this review” before the tree; omit an empty `doc-plan` if there are no auxiliary claims either.

Re-review keeps stable IDs and renders only the recorded delta. Label fixed / still open / new inline on finding rows, rather than creating a second status hierarchy. An open finding is new when `round_found` equals this round; status remains the recorded `open`. Keep `no-longer-applies` distinct with its recorded reason. Omit dropped findings. Counts always describe the complete recorded open author set.

The shared packer also checks planning conventions. Reviews can legitimately emit warnings about trigger → result titles, title/tag word counts, more than five findings, missing `aux="scope"`, or a `doc-note` auxiliary block that the exhibit linter does not count. Inspect and report such warnings; do not rewrite approved findings, relabel Method as scope, suppress lint, or add build decisions just to clear them. Packing errors must be fixed.

## HTML comments and fidelity

Keep the actual comment buttons and floating comment/response UI. Comments and copied responses are feedback data, not approval, merge readiness, or triage changes. Re-verify user feedback before changing the recorded findings. Do not add `doc-ask` planning questions, schema editing, or runnable mock controls. The runtime's compact sans dark/gold default UI, built-in persisted Light mode / Dark mode control, and light print behavior are inherited unchanged. Open parent rows stay in document flow. Review does not add bespoke filters, theme scripts, or print state hooks.

Escape recorded prose and attributes. Evidence inside inert `script type="text/plain"` is raw source text, not HTML entities or executable JavaScript. If recorded evidence contains a closing script tag, use the runtime-supported `textarea class="src"` wrapper with HTML-escaped text instead; this preserves the evidence without ending the inert source wrapper or altering its characters. Validate navigation URLs. Preserve the approved IDs, content, severity, status, confidence and origin. Compare the source and packed report content and verify inline CSS/JS match the resolved shared runtime before sharing. Regenerate the packed example after source or shared runtime changes; never hand-edit the packed runtime.

## Readiness wording

Use the subject-aware, CI-aware verdict rules in the review root. A local review with any open actionable author blocker or should-fix says “Needs changes” (`needs-changes`); otherwise it says “No blocking findings” (`no-blocking-findings`). Neither mergeable label applies to local reviews. The “Mergeable after fixes” examples above illustrate PR reviews only. For PRs, use “Mergeable” only when applicable CI passes and no blocking findings remain. Failed or pending checks qualify readiness explicitly; no checks means runtime/build verification is absent. Render only recorded evidence and never imply static tracing executed the application.
