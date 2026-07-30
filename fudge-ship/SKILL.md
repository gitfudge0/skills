---
name: fudge:ship
description: Use when the user wants to build a feature end to end rather than run one step — "build a feature", "take this from idea to implementation", "ship this", "run it through the skills", "full pipeline", "do the whole thing", or when they name several fudge skills in sequence for one piece of work. Also use on "resume" or "continue" when a previous run is open.
---

# fudge:ship

Runs one feature from idea to reviewed implementation by sequencing the other fudge skills as stages, halting at three human gates.

## The core principle: fudge:ship conducts, it does not produce

Nothing here writes a decision, a mock, a test plan, or code. Each stage hands off to the skill that owns that output and holds the result.

Stopping is the load-bearing half — the gates make a wrong route cost one stage instead of five.

## What this skill will not do

- **No parallelism between stages.** Each stage's output is the next stage's input. Running two at once means one is working from stale context.
- **No branch, commit, PR, or push** unless the user asks for it in so many words.
- **No scope expansion.** The request scoped at the start is the request at review. A stage that surfaces adjacent work reports it; it does not absorb it.
- **No substituting for a missing skill.** If a stage's skill is not installed, halt, name it, and say how to install it. Never hand-roll an ad-hoc equivalent. A missing fudge:layered-review is a full stop, not a drop — record `status: blocked`.

## The stages

Six skills are stages. Fixed order. Stages may be **dropped**, never **reordered**.

| Stage | Skill | Runs when |
|---|---|---|
| `understand` | fudge:gap-analysis | A document corpus exists *and* the ask is vague |
| `decide` | fudge:decision-room | The call is contested or not yet made |
| `design` | fudge:ui-mock | A user-visible surface changes |
| `verify-plan` | fudge:test-plan | Almost always |
| `implement` | fudge:delegate | Code is being written |
| `review` | fudge:layered-review | **Always, if `implement` ran** — see below |

Users name a stage by either column — the stage (`design`) or the skill (`fudge:ui-mock`). Both map to the same row. If a name matches neither, ask rather than guess.

**`review` is not droppable.** If code was written, fudge:layered-review runs. Omission does not drop it. Only an explicit exclusion ("skip the review", "no review") drops it, and then say so in `route_reason`. Do not ask permission to run it; run it and report.

Three skills are **support** — invoked *inside* a stage, never as a stage of their own:

- **fudge:report-deck** — styles the HTML a stage emits.
- **fudge:mindmap** — offered during `understand` only, when the corpus is large enough to be worth mapping. A decline is not a gate answer.
- **fudge:rust-arch** — see `implement`.

**fudge:delegate is a behavioral contract, not a producer, and it governs every stage, not just `implement`.** Producing an artifact is implementation under CLAUDE.md's own definition, so fudge:ship never runs a stage's skill inline. `understand`, `decide`, `design`, `verify-plan`, and `review` are each dispatched to a single worker subagent (`Agent` tool, model and effort tiered to the task per fudge:delegate) that invokes the stage's skill and hands back its artifact — fudge:ship reads that artifact back to verify and report, it does not author one. `implement` is the exception: there is no single document to dispatch for. fudge:ship itself applies fudge:delegate directly — splitting the work, dispatching its own fleet of workers, and verifying their output — rather than handing the whole stage to one intermediary worker.

## Routing

**If the user's prompt names stages, that is the route.** "Run fudge:decision-room, then fudge:ui-mock, then fudge:test-plan" means exactly those three, in that order. Obey literally: no inferred additions, no "they probably also want".

**Only when no stages are named** does fudge:ship infer a route, from the *Runs when* column. It is judgement, not a rule table — weigh how expensive the work is to unwind.

**State the route and the reasoning before running any stage.** Print the chosen stages, and say what was dropped and why.

If fudge:decision-room's verdict is **don't build**, that is a full stop — not a gate. Report it and end the run. The user may override by saying so, and then the pipeline continues. On override, recompute the route from the current understanding and re-state it before continuing. fudge:ship does not argue the point twice.

## Workspace

```
.fudge-ship/<YYYY-MM-DD>-<slug>/
  run.json
  1-decision.html
  2-mock.html
  3-test-plan.html
  4-review.html
```

When `understand` runs, fudge:gap-analysis keeps writing its own `.gap-analysis/`. Reference that path from `run.json`; do not move or copy it.

**Ignore the workspace at run creation.** Before writing `run.json`: if this is a git repo, append `.fudge-ship/` to the `.gitignore` at the repo root (`git rev-parse --show-toplevel`), creating it if absent and skipping if already ignored. If it is not a git repo, create the workspace and skip this step. Do it at run start, not the end, and mention it in the same message as the route — a silent write to a tracked file is a surprise in someone else's commit.

`run.json` is the source of truth. Exact keys:

```json
{
  "slug": "terminal-session-switching",
  "created": "2026-07-28",
  "request": "<the user's original ask, verbatim>",
  "route": ["decide", "design", "verify-plan", "implement", "review"],
  "route_reason": "<why these stages, why not the others>",
  "implement_baseline": {"head": "<git rev-parse HEAD>", "dirty": "<git status --porcelain>"},
  "stages": {
    "understand":  {"status": "skipped", "artifact": null,              "summary": null},
    "decide":      {"status": "done",    "artifact": "1-decision.html", "summary": "<one line>"},
    "design":      {"status": "gated",   "artifact": "2-mock.html",     "summary": "<one line>"},
    "verify-plan": {"status": "pending", "artifact": null,              "summary": null},
    "implement":   {"status": "pending", "artifact": null,              "summary": null},
    "review":      {"status": "pending", "artifact": null,              "summary": null}
  },
  "gates": {
    "1-decide":      {"answered": true,  "response": "<what the user actually said>", "at": "2026-07-28"},
    "2-design":      {"answered": false, "response": null, "at": null},
    "3-verify-plan": {"answered": false, "response": null, "at": null}
  }
}
```

`status` is one of `pending | running | gated | done | skipped | blocked`.

`stages` carries an entry for all six stages. Ones not in `route` are `skipped` at run creation, so a resumed run can tell *dropped* from *not yet reached*.

**`gates.*.response` is not optional and not a boolean in disguise.** Record what the user actually said — "yes but drop the sidebar variant", not "approved". Disk recovers *which* stage; only this recovers *what was approved*.

Write `run.json` after **every** stage transition and **every** gate answer. Not at the end.

## Running a route

### Stage 0 — Recon (always, before `decide`)

Read-only exploration of the codebase before the first real stage. Use parallel read-only Explore agents: what exists today in this area, what the design system actually looks like, where the seams are, what the test setup is.

Ungrounded personas give generic advice, and an ungrounded mock renders a UI that does not match the product. Recon is held as context and passed into stages — it is not written to a file and not shown as a deliverable.

### Seeding

Every stage receives the previous stage's output, not just the original request — `design` gets the decision's recommendation, risks, and out-of-scope list.

### Stage notes

Every stage below runs through the dispatch pattern above; `implement` is the one exception, where fudge:ship itself is the fudge:delegate orchestrator rather than a stage dispatched to a single worker.

- **`decide`** — frame fudge:decision-room around the *real* decision, not the feature title. "Should we add session switching" is a title; "do we switch sessions in-place or spawn a second pane, given the existing single-buffer renderer" is the decision.
- **`design`** — at GATE 2, loop on revisions as many times as the user wants. Each revision re-runs fudge:ui-mock and rewrites `2-mock.html`; the gate stays open until the user advances it.
- **`implement`** — orchestrate via fudge:delegate. Load fudge:rust-arch first if the target is Rust. Record `git rev-parse HEAD` and `git status --porcelain` into `run.json` as `implement_baseline` before any worker runs. `review` diffs against that baseline and names any pre-existing modifications separately rather than reporting them as this run's work. When workers report done, **re-run the build, tests, and lint yourself and read the raw output**. A worker's claim of success is zero evidence.
- **`review`** — fudge:layered-review over the diff this run produced, written to `4-review.html`.

## The gates

Three hard stops. At each one: halt, report the verdict or outcome in chat, give the artifact path, and **wait for the user**. Nothing downstream runs. Set the stage to `gated`, write `run.json`, and stop producing output.

- **GATE 1** — after `decide`
- **GATE 2** — after `design`
- **GATE 3** — after `verify-plan`, before `implement`

**The boundary is mechanical, not a matter of intent.** Until `gates.3-verify-plan.answered` is `true` in `run.json`: no Edit or Write to any file outside `.fudge-ship/`, no Bash command that mutates the working tree, and no Agent invocation whose prompt contains implementation instructions. Recon agents are read-only. These are forbidden regardless of what the agent believes it is doing — "I was only planning" is not an exemption.

**A gate advances only on an unambiguous instruction to proceed.** Anything conditional, partial, or a question is not an advance: answer it, keep `status: gated`, and re-present. If the response would change the artifact, re-run the stage rather than carrying the change as an unwritten amendment.

**One answer advances one gate.** A response that pre-approves later gates ("yes, and go ahead through the mock and plan too") advances only the current one. Never write a `response` into a gate that was not individually answered.

A stage runs once per run **after its gate is answered**. While a stage is `gated`, it may be re-run on feedback any number of times — that is a revision, not a re-run, and it applies at every gate.

A user who wrote "…and then proceed to implementation" in their opening prompt has authorized the *stage*, not the skipping of the *gate*. Pre-authorizing a sequence up front is not gate consent. Consent is a response to the artifact, given after seeing it — which is the entire point, since the plan the user is consenting to did not exist when they wrote the prompt.

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
- spawning a worker "just to plan the implementation" before GATE 3 is answered

## Resume and identity

`resume` or `continue` reads `run.json`, reports the route, the completed stages with their summaries, and the recorded gate responses, then picks up at the gated stage. If more than one open run exists under `.fudge-ship/`, list them with slug and date and ask which one — never guess.

Derive the slug as 2-5 kebab-case words from the user's ask, and propose it in the route message so it can be corrected early. After that it is permanent — never rename it mid-run.
