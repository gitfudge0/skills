---
name: gf-ship
description: Use when the user wants to build a feature end to end rather than run one step — "build a feature", "take this from idea to implementation", "ship this", "run it through the skills", "full pipeline", "do the whole thing", or when they name several gf- skills in sequence for one piece of work. Also use on "resume" or "continue" when a previous run is open.
---

# gf-ship

Runs one feature from idea to reviewed implementation by sequencing the other gf- skills as stages, halting at three human gates.

## The core principle: gf-ship conducts, it does not produce

Nothing here writes a decision, a mock, a test plan, or code. Each stage hands off to the skill that owns that output, seeds it with everything learned so far, and holds the result. The value gf-ship adds is ordering, continuity between stages, and stopping.

Stopping is the load-bearing half. An unattended pipeline that runs decide → design → verify-plan → implement without a human in it produces a confident implementation of the wrong thing, four stages deep, with the artifacts that would have caught it already generated and unread. The gates exist to make a wrong route cost one stage instead of five.

## What this skill will not do

- **No parallelism between stages.** Each stage's output is the next stage's input. Running two at once means one is working from stale context.
- **No cost or time estimation before a run.** Route length is knowable; stage cost is not.
- **No partial re-run of a single completed stage.** A stage runs once per run. To redo one, start a new run.
- **No branch, commit, PR, or push** unless the user asks for it in so many words.
- **No scope expansion.** The request scoped at the start is the request at review. A stage that surfaces adjacent work reports it; it does not absorb it.

## The stages

Six skills are stages. Fixed order. Stages may be **dropped**, never **reordered**.

| Stage | Skill | Runs when |
|---|---|---|
| `understand` | gf-gap-analysis | A document corpus exists *and* the ask is vague |
| `decide` | gf-decision-room | The call is contested or not yet made |
| `design` | gf-ui-mock | A user-visible surface changes |
| `verify-plan` | gf-test-plan | Almost always |
| `implement` | gf-delegate | Code is being written |
| `review` | gf-layered-review | Code was written |

Three skills are **support** — invoked *inside* a stage, never as a stage of their own:

- **gf-report-deck** — styles the HTML a stage emits.
- **gf-mindmap** — offered when the input material is dense enough to be worth mapping.
- **gf-rust-arch** — loads during `implement` when the target is Rust.

**gf-delegate is not a producer.** It is a behavioral contract, not a tool that receives work. "Implement via gf-delegate" means the implement stage adopts the orchestrator/worker split — plan and verify here, delegate the editing to workers — not that the stage hands the feature to a separate system and waits.

## Routing

**If the user's prompt names stages, that is the route.** "Do a roomie, then mockie, then testie" means exactly those three, in that order. Obey literally: no inferred additions, no helpful extra review stage, no "they probably also want".

**Only when no stages are named** does gf-ship infer a route. Inference is judgement, not a rule table. Signals to weigh:

- Is there a document corpus to mine, and is the ask vague enough to need it?
- Is the call contested, or has the user already made it?
- Does a user-visible surface change?
- Is this reversible in one commit, or expensive to unwind?
- Is the target language Rust?

**State the route and the reasoning before running any stage.** Print the chosen stages, and say what was dropped and why. A wrong route corrected here costs nothing; corrected at review it costs the whole run.

If gf-decision-room's verdict is **don't build**, that is a full stop — not a gate. Report it and end the run. The user may override by saying so, and then the pipeline continues. gf-ship does not argue the point twice.

## Workspace

```
.gf-ship/<YYYY-MM-DD>-<slug>/
  run.json
  1-decision.html
  2-mock.html
  3-test-plan.html
  4-review.html
```

When `understand` runs, gf-gap-analysis keeps writing its own `.gap-analysis/`. Reference that path from `run.json`; do not move or copy it.

`run.json` is the source of truth. Exact keys:

```json
{
  "slug": "terminal-session-switching",
  "created": "2026-07-28",
  "request": "<the user's original ask, verbatim>",
  "route": ["decide", "design", "verify-plan", "implement", "review"],
  "route_reason": "<why these stages, why not the others>",
  "stages": {
    "decide":      {"status": "done",    "artifact": "1-decision.html", "summary": "<one line>"},
    "design":      {"status": "gated",   "artifact": "2-mock.html",     "summary": "<one line>"},
    "verify-plan": {"status": "pending", "artifact": null,              "summary": null}
  },
  "gates": {
    "1-decide":      {"answered": true,  "response": "<what the user actually said>", "at": "2026-07-28"},
    "2-design":      {"answered": false, "response": null, "at": null},
    "3-verify-plan": {"answered": false, "response": null, "at": null}
  }
}
```

`status` is one of `pending | running | gated | done | skipped`.

**`gates.*.response` is not optional and not a boolean in disguise.** Record what the user actually said — "yes but drop the sidebar variant", not "approved". A resumed run can always recover *which* stage it was on from the files on disk; what it cannot reconstruct is *what was approved*, and losing that forces a re-ask that spends the user's attention on a question they already answered.

Write `run.json` after **every** stage transition and **every** gate answer. Not at the end.

## Running a route

### Stage 0 — Recon (always, before `decide`)

Read-only exploration of the codebase before the first real stage. Use parallel read-only Explore agents: what exists today in this area, what the design system actually looks like, where the seams are, what the test setup is.

This is not optional politeness. Ungrounded personas give generic advice, and an ungrounded mock renders a UI that does not match the product. Recon is held as context and passed into stages — it is not written to a file and not shown as a deliverable.

### Seeding

Every stage receives the previous stage's output, not just the original request. The design stage gets the decision's recommendation, risks, and out-of-scope list. The verify-plan stage gets the mock's states. The implement stage gets the plan. A stage that only sees the original prompt is running blind and will contradict the stage before it.

### Stage notes

- **`decide`** — frame gf-decision-room around the *real* decision, not the feature title. "Should we add session switching" is a title; "do we switch sessions in-place or spawn a second pane, given the existing single-buffer renderer" is the decision.
- **`design`** — at GATE 2, loop on revisions as many times as the user wants. Each revision re-runs gf-ui-mock and rewrites `2-mock.html`; the gate stays open until the user advances it.
- **`implement`** — orchestrate via gf-delegate. Load gf-rust-arch first if the target is Rust. When workers report done, **re-run the build, tests, and lint yourself and read the raw output**. A worker's claim of success is zero evidence.
- **`review`** — gf-layered-review over the diff this run produced, written to `4-review.html`.

## The gates

Three hard stops. At each one: halt, report the verdict or outcome in chat, give the artifact path, and **wait for the user**. Nothing downstream runs. Set the stage to `gated`, write `run.json`, and stop producing output.

- **GATE 1** — after `decide`
- **GATE 2** — after `design`
- **GATE 3** — after `verify-plan`, before `implement`

**GATE 3 is the one that gets rationalized away.** A user who wrote "…and then proceed to implementation" in their opening prompt has authorized the *stage*, not the skipping of the *gate*. Pre-authorizing a sequence up front is not gate consent. Consent is a response to the artifact, given after seeing it — which is the entire point, since the plan the user is consenting to did not exist when they wrote the prompt.

| Rationalization | Counter |
|---|---|
| "They already said proceed to implementation." | That authorized the stage, not the gate. They approved a plan they hadn't read. |
| "It's just a short pause — I'll present the plan and start." | Presenting while starting is not a gate. A gate has no output after the report. |
| "Objecting is cheap; I'll begin and they can stop me." | By then the workers have written code. The gate is cheap *because* it precedes that. |
| "The plan is uncontroversial." | You wrote the plan. You are the last party qualified to judge it uncontroversial. |
| "Stopping here is annoying for a pipeline skill." | Three stops in a five-stage run is the design, not friction to optimize away. |

Red flags — if you catch yourself writing any of these, you are mid-violation. Stop and gate:

- "unless the user objects"
- "not a hard gate" / "soft gate" / "brief pause"
- "since they already said…"
- "I'll start on the first task while they look"
- reading a file with intent to edit it, with no gate answer recorded in `run.json`

## Resume and identity

`resume` or `continue` reads `run.json`, reports the route, the completed stages with their summaries, and the recorded gate responses, then picks up at the gated stage. If more than one open run exists under `.gf-ship/`, list them with slug and date and ask which one — never guess.

The slug is permanent. It names the directory, and it is how the user refers to the run later. Never rename it mid-run.
