---
name: gf-layered-review
description: Use when reviewing a PR, reviewing code changes, reporting review findings, or sharing review feedback — including phrasings like "review this PR", "what do you think of this diff", "give me feedback on these changes", or "post this review to Slack/GitHub". Conducts the actual code review, then renders the findings in layered form — verdict, one-line list, drill-down detail — for Slack, GitHub, or an HTML report, so the reader never faces a wall of text.
---

# Review for dummies

Two jobs, in sequence: conduct the code review, then render the findings in layers so a reader gets the high-level picture immediately and drills into detail only as needed. The whole point is the reader should never face a wall of text.

## Part 1 — Conducting the review

- **Establish context first**: read the ticket/issue if referenced, and the PR description, before reading code.
- **Fan out for anything beyond a trivial diff**: dispatch read-only reviewer subagents over disjoint scopes (by layer or by repo) rather than reading everything serially. Give each a self-contained brief.
- **Verification is mandatory and non-delegable**: a subagent's claim of success is zero evidence. Re-run builds/tests/lint yourself and read the raw output. Re-read the specific lines behind any claimed finding before it is reported.
- **Establish a baseline before blaming a PR for a failure**: if the repo already fails typecheck/lint/tests on the base branch, compare against that baseline and report only the delta.
- **Verify cross-repo contracts explicitly**: identifier strings, column names/types/nullability, config key paths, payload field names. Determine the required deploy order and what breaks in the wrong order.
- **Check external documentation when an assumption can't be checked from the repo alone** (e.g. a third-party webhook payload shape). If it still can't be settled, the finding is SUSPECTED, not a fact.

## Part 2 — The finding schema

Every finding has four fields, in this fixed order — never rearrange it:

1. **What's happening** — plain English mechanism. No code identifiers, no file paths, no function names in this field. Explain it the way you'd explain it out loud.
2. **Why it matters** — the concrete failure and who is affected.
3. **The fix** — what to do, not merely what is wrong. Point at an existing correct pattern in the same codebase where one exists.
4. **Where** — file:line. Always last. Leading with locations is what makes a review read as code-driven and hard to absorb; this ordering is deliberate and must not be rearranged.

Three further fields render by exception — print only when they carry information, silent otherwise. This is the core rule that keeps reviews short.

| Field | Prints only when | Silent default |
|---|---|---|
| Confidence | the finding is SUSPECTED | verified |
| Origin | the issue is pre-existing | introduced by this PR |
| Effort | the review has 15+ findings | omitted |

Plus **Coverage** — a short list of what was checked and found clean. Render it as one collapsed block at the end, only for reviews with 5+ findings; omit entirely below that.

**Severity vocabulary** — use exactly these three, with these exact emoji and bold labels: 🔴 **blocker**, 🟠 **should-fix**, ⚪ **nit**.

Use the emoji literally in Slack and GitHub — neither can style text. In HTML, render severity as a styled chip (semantic colour plus the word) instead: same vocabulary, better executed. Distinguish the three by form as well as colour — filled, outlined, muted-outlined — so severity survives greyscale and colour-blindness.

Marking a finding SUSPECTED is a feature, not a weakness — unverified suspicions reported as fact waste the author's time and damage trust in the whole review.

## Part 3 — The adaptive layer model

Two independent knobs: depth and grouping.

**Depth is driven by finding count:**
- **≤4 findings** → flat list, detail inline. Do not layer; layering this few findings adds friction.
- **5–14** → three layers: verdict line, one-line-per-finding list, detail on demand.
- **15+** → same three layers, plus priority ordering ("fix these first") and an explicit note of what is not worth their time.

**Grouping is driven by PR shape, independently:**
- One repo, one area → no headings.
- One repo, several areas → group by area.
- Cross-repo → group by repo.

These two knobs are independent — shape doesn't dictate depth. Example: a 40-file PR yielding 2 findings renders as a flat list with repo labels; a 3-file PR yielding 12 findings renders fully tiered with no headings.

**The three layers:**
- **Layer 1 — verdict.** One line, always. Merge recommendation plus counts.
- **Layer 2 — the list.** One line per finding: severity, short label, location hint.
- **Layer 3 — detail.** The four fields above, on demand.

## Part 4 — The three renderers

The review is produced once as a structured finding list, then projected into the chosen medium. This single-source rule is what stops the artifacts drifting when a review is updated after a re-review pass.

**Slack** — layers 1 and 2 in the message, hard stop. Layer 3 goes into thread replies: one reply per blocker, all should-fixes batched into one further reply. Slack has no collapse, so the thread IS the collapse mechanism. In layer 2, drop file paths and show only the area — paths are noise in a chat client.

**GitHub** — layers 1 and 2 as a table in a single summary comment; layer 3 in `<details><summary>` blocks below it. Additionally post each blocker as an inline review comment anchored to its line, containing one sentence and a pointer up to its details block. Never duplicate full finding text inline — that is what makes PR reviews unreadable.

**HTML** — all layers, filterable by severity/repo/status, written into the project's existing `.reports/` directory. Best for cross-repo reviews or 15+ findings, and it doubles as a durable artifact for things like a deploy-ordering constraint that a chat message would bury.

Use the **indigo editorial design language**, bundled with this skill so it never depends on files in other projects. The spec is `assets/design-system.md` and a complete, copyable reference page is `assets/example-review.html` — HTML output from this skill MUST follow the design system doc, and SHOULD be built by copying `example-review.html` and replacing its content rather than inventing new markup or CSS. This is not optional: if the target repo already has an existing report or template sitting in its own `.reports/` directory, do not copy that report's style instead of the skill's bundled one — the bundled assets are authoritative regardless of what else is lying around in the repo being reviewed.

Its grammar, briefly: self-contained page, no external CSS — an indigo body background (`#2D2DD6`) framing a near-white panel with 2px radius, content column max-width 960px; CSS custom properties for every color across three theme blocks (light `:root`, a `prefers-color-scheme: dark` block scoped to `:root:not([data-theme])`, and explicit `data-theme` overrides) with a persisted, working theme toggle; a centered header whose headline IS the verdict sentence; a stats row of outlined SVG circle icons (solid/dashed/dotted/check for blockers/should-fix/nits/clean); `.erow` sections (27%/73% label/content split) grouping findings; each finding as a numbered `.item` with the four-field schema as micro-label pairs (`where` always last); severity/status pills (red/amber/muted/teal, tinted only for red and teal); and a `.divider-pill` before the coverage block. See `assets/design-system.md` for exact tokens, sizes, and the full component-by-component breakdown — do not re-derive these from scratch.

Severity still uses the standard vocabulary; in this design it renders as pills, not emoji.

*Optional, secondary reference only, and only if the bundled assets are ever unavailable*: the design language originated in `/Users/digvijaymahapatra/globus/.gapworkshop/questions.html` (fuller component set) and a review-shaped example at `careconvoy-ai-core/.reports/ava-191-review.html`. Both live outside this skill in unrelated projects that may move or change — treat `assets/design-system.md` and `assets/example-review.html` as authoritative if the two ever disagree.

**Choosing the medium**: it is an argument at invocation — `slack`, `pr`, or `html`. If not supplied, ask the user rather than guessing, and volunteer a suggestion based on finding count and whether the change is cross-repo.

## Part 5 — Worked example

### The prose rule, before and after

Same finding, written twice. The first version is what a review naturally produces and what readers bounce off:

> `getCallTranscriptAction` in `transcripts/actions.ts:15-57` calls `callTranscriptService.getCallTranscript()` without resolving `resolveCallEscalationsAccess`, so `CallTranscriptDto.transferDestination` is serialised into the payload regardless of the `DATA_CALL_ESCALATIONS` feature flag. `TranscriptPageClient.tsx:184` gates rendering client-side only.

The second says the same thing and can be understood at a glance:

> The server sends the phone number to the browser, and the page then decides whether to show it. The check happens after the data has already arrived.

Every identifier in the first version is real and correct — and none of it belongs in "What's happening". It goes in **Where**, at the bottom, where a reader who has already decided to act will look for it.

### The same finding rendered for Slack

Layers 1 and 2 in the message; nothing else. Note the list shows the area, not file paths.

```
❌ Needs changes — 2 blockers · 6 should-fix · 2 nits
careconvoy web #88 · core #96

🔴 Transcript page hides the phone number instead of withholding it — transcripts
🔴 Shipping the frontend first breaks Interactions for everyone — deploy
🟠 6 should-fix · ⚪ 2 nits

Detail in thread 🧵
```

Then one thread reply per blocker:

```
1/ 🔴 Transcript page hides the phone number instead of withholding it

The server sends the phone number to the browser, and the page then
decides whether to show it. The check happens after the data has
already arrived.

Why it matters — Anyone who can open a transcript, a wider group than
escalation access, can read the number in their network inspector.
Both gates are cosmetic here.

The fix — Blank both fields server-side for viewers who don't qualify.
This PR already does exactly that for the call-history modal.

Where — call-transcript-service.ts:210 · transcripts/actions.ts
```

Should-fixes and nits are batched into one further reply, not one each.

### The same finding rendered for GitHub

One summary comment carrying layers 1 and 2 as a table, with layer 3 in collapsible blocks:

```markdown
## ❌ Needs changes — 2 blockers · 6 should-fix · 2 nits

|   | Finding | Where |
|---|---------|-------|
| 🔴 | Transcript page hides the phone number instead of withholding it | transcripts |
| 🔴 | Shipping the frontend first breaks Interactions for everyone | deploy |
| 🟠 | The escalation flag is tied to the wrong half of the webhook | webhooks |

<details>
<summary>🔴 Transcript page hides the phone number instead of withholding it</summary>

The server sends the phone number to the browser, and the page then decides
whether to show it. The check happens after the data has already arrived.

**Why it matters** — Anyone who can open a transcript, a wider group than
escalation access, can read the number in their network inspector. Both
gates are cosmetic here.

**The fix** — Blank both fields server-side for viewers who don't qualify.
This PR already does exactly that for the call-history modal.

**Where** — `src/lib/services/call-transcript-service.ts:210` ·
`transcripts/actions.ts`
</details>
```

Plus one inline review comment anchored to the offending line — a single sentence, never the full finding:

```
🔴 Blocker: the phone number reaches the browser before the access check
runs. Full detail in the summary comment.
```

### The same finding rendered as HTML

Structure rather than markup — the page is generated, so what matters is what goes where:

```
verdict band           merge recommendation + counts, always visible
risk callout           full-bleed; only when a release constraint exists
filter row             severity + repo, combinable
grouped finding rows   accordion; collapsed shows severity, title, area
  └ expanded           statement, then why/fix side by side, then where
coverage block         collapsed, 5+ findings only
```

The expanded statement is set larger than the body text and carries no label — its size announces what it is. Everything in the panel shares one left edge; do not indent the detail away from its own heading.

## Part 6 — Closing checklist

- Where goes last, always.
- No code identifiers in "What's happening".
- Never report an unverified claim as fact; tag it SUSPECTED or leave it out.
- Compare against the base-branch baseline before attributing a failure to the PR.
- Separate pre-existing issues from introduced ones, and say which is which.
- Credit correct patterns the author already used elsewhere in the same PR when pointing at a fix.
- Don't pad with generic praise.
