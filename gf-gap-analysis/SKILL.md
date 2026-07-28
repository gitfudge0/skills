---
name: gf-gap-analysis
description: Run a document-driven gap analysis workshop over a corpus of project material. Reads specs, PRDs, API docs, vendor material, meeting notes and diagrams; reconstructs end-to-end flows using EventStorming and domain storytelling; sweeps every system seam against a gap taxonomy; maps assumptions by evidence; and produces a reviewable HTML report plus a list of questions routed to the humans who can answer them. Use this skill whenever someone wants to find gaps, unknowns, blind spots, missing requirements or open questions across project documents — including phrasings like "what are we missing", "gap analysis", "are we ready to build", "review these specs", "what should we be asking", "kick off discovery for X", "we have docs from five teams, make sense of them", or any multi-team project where requirements are scattered across many sources. Also use it to re-run the analysis after humans have answered the previous round of questions.
---

# gf-gap-analysis

Turn a pile of project documents into a reviewable workshop output: reconstructed flows, a gap register, an assumption map, and — the actual deliverable — a routed list of questions humans must answer.

## The core principle: inference debt is the finding

This pipeline derives flows from documents, then analyses those flows. Every derivation step is an opportunity to invent something plausible and then analyse the invention with full confidence. That failure mode produces a polished document that makes a team *feel* gap analysis has happened while leaving the real gaps untouched.

The defence is to treat your own inference as data. Where you had to bridge a hole to make a flow connect, humans have not specified that thing — the bridge itself is the gap. So every derived element carries a provenance tag:

| Tag | Meaning |
|---|---|
| `stated` | A document says this. Cite the document and location. |
| `implied` | Logically necessary given two or more stated things. Cite both. |
| `assumed` | You bridged a hole. Nothing in the corpus supports this. |

Density of `assumed` is the heatmap. A flow that is 70% assumed is not a flow — it is a report that this process is undocumented, and it should read that way to the human.

Never smooth over an `assumed` step to make a narrative flow nicely. The awkwardness is the signal.

## What this skill will not do

Stay inside these lines. Exceeding them is how the output becomes untrustworthy.

- **It does not decide priority.** Ranking gaps encodes whose risk matters — a stakeholder-political act. Compute discovery cost mechanically; leave final ordering to humans.
- **It does not close gaps.** Only a human with evidence moves a record to `closed`.
- **It does not replace contact with reality.** Site visits, vendor calls and watching the real process cannot be simulated. When a gap can only close that way, say so in the closure action.
- **It does not invent domain facts to fill gaps.** If the corpus does not say how the robot receives a plan, the answer is a question, never a guess dressed as a finding.

## Modes

Pick based on what the user asked for. When unclear, run `map` first — it is cheap and its output usually determines whether a full run is worth it.

| Mode | Trigger | Does |
|---|---|---|
| `map` | "what have we got", first contact with a corpus | Stage 0 only. Document inventory and coverage grid. Minutes, not hours. |
| `run` | "do the gap analysis", "what are we missing" | Full pipeline, stages 0–8. |
| `refresh` | Humans have filled in `answers.yaml`, or documents changed | Re-runs against updated inputs, **diffing** against the existing register. Never regenerates from scratch. |

## Workspace

All artifacts live in `.gap-analysis/` at the project root. Create it if absent.

```
.gap-analysis/
  corpus-map.md          stage 0 — inventory + coverage
  extracts/<doc-id>.yaml stage 1 — per-document structured extraction
  glossary.yaml          stage 2 — terms, and where they conflict
  contradictions.yaml    stage 2 — documents that disagree outright
  flows/<flow-id>.yaml   stage 3-4 — reconstructed flows with provenance
  register.yaml          stage 5 — the gap register (source of truth)
  assumptions.yaml       stage 6 — assumption map
  questions.yaml         stage 7 — routed questions
  answers.yaml           ← humans write here; read on refresh
  report.html            stage 8 — rendered output
```

`register.yaml` is canonical. Everything else is either an input to it or a rendering of it. `report.html` is disposable and regenerated every run.

## Pipeline

Run stages in order. Each stage writes its artifact before the next begins — if the run is interrupted, the work so far survives and `refresh` can resume.

### Stage 0 — Corpus map

Inventory every document: id, filename, type, date if determinable, apparent owner or team, one-line summary.

Then build the coverage grid: systems and journey phases down one axis, documents across the other, cell = how many documents substantively address that intersection. Read `references/extraction.md` for how to identify systems before you have read everything.

**This grid is often the single most valuable output of the whole run.** "Thirty-eight documents concern the patient app, two mention the robot in passing, zero describe the planning software's export format" is actionable today, before any analysis. Zero-coverage cells go straight into the register as `evidence` gaps.

The grid does not get its own section in the report — the findings survive as register entries and the ceremony is dropped. It is still the whole output of `map` mode, and `corpus-map.md` remains on disk.

Write `corpus-map.md`. If mode is `map`, stop here and present it.

### Stage 1 — Extraction

Per document, extract structured intermediates: systems, actors, events, entities, terms, explicit claims, stated constraints — each with a source location so every downstream statement can be traced back.

Work document by document and write each `extracts/<doc-id>.yaml` as you go. Reasoning in later stages happens over these intermediates, not the raw documents, which is what lets the skill handle a corpus larger than one context window. See `references/extraction.md`.

### Stage 2 — Glossary and contradictions

Collate terms across extracts. Where the same term carries different meanings in different documents, that is a semantic gap requiring zero inference — the highest-confidence output this skill produces.

Separately, find documents that assert incompatible things: different sequences, different owners, different data flows, different numbers.

Write `glossary.yaml` and `contradictions.yaml`. Every contradiction becomes a register entry with `provenance: stated`.

### Stage 3 — Flow reconstruction

Build candidate end-to-end flows as event timelines. EventStorming shape: domain events in chronological order, with actors and systems attached.

This is a thinking tool rather than an artifact — it is fast, it exposes ordering problems, and it stops you committing to actors before you know who they are. See `references/flows.md`.

Aim for two to five flows covering the primary value paths — not one flow per feature.

### Stage 4 — Domain stories and unhappy paths

Convert each flow into domain story sentences following the notation at <https://domainstorytelling.org/quick-start-guide> — **actor — verb — work object — actor**, numbered in sequence, in the domain's own language. This is the form the report renders as a diagram, so it is the canonical flow artifact.

Tag every sentence with provenance. Where you bridged a hole, tag `assumed` and record what you assumed and why; the renderer draws those as dashed red arrows and shades the row.

Then run two passes that find more real gaps than the happy path ever does:

- **Reverse narrative** — walk the flow backwards, asking what must have been true for each step. Steps that cannot be justified backwards have a hole before them.
- **Unhappy paths** — for each step: cancelled, amended, duplicated, arriving out of order, upstream system down, identity changed underneath. Most integration gaps live here.

See `references/flows.md`.

### Stage 5 — Seam sweep

Enumerate seams — every point where two systems, teams or organisations exchange something. Then sweep each seam against the ten-type taxonomy in `references/taxonomy.md`.

Work **one seam at a time**. Sweeping everything at once is how you get the gap-analysis equivalent of test case vomit: forty generic findings nobody reads. Cap at five gaps per seam and force a ranking — if a sixth wants in, something must come out.

Every record needs a falsifiable closure action. If you cannot say what would resolve it, it is an anxiety, not a gap. Cut it.

Where a gap bites at a specific step, add its id to that sentence's `gaps` list so it renders inside the flow diagram rather than only in a table. Cross-cutting gaps — seam ownership, per-site variance, terminology — stay in the table.

Write `register.yaml`.

### Stage 6 — Assumption map

Extract every load-bearing belief. Plot on importance × evidence.

Derive the evidence axis **mechanically** — count independent corpus sources supporting the belief. A model grading its own confidence is not evidence; a source count is. Importance is judged: if this is wrong, does the design change?

Write `assumptions.yaml`. See `references/report.md` for the schema.

### Stage 7 — Questions

Convert unknowns into questions, grouped by **who can answer**, not by topic. That routing is what makes the document usable: the EHR integration lead opens one section, answers eight questions in half an hour, and never reads the rest.

Two gates, both strict — see `references/questions.md`:
- Every question must name what you would do differently depending on the answer. If nothing changes, cut it.
- Hard cap per answerer. Nobody answers forty questions; they answer eight and ignore a list of forty.

Write `questions.yaml`.

### Stage 8 — Render

Populate `assets/report-template.html` and write `.gap-analysis/report.html`. The template is self-contained — no network dependencies, works offline, prints sensibly.

Substitute the JSON payload into the `__GAP_ANALYSIS_DATA__` placeholder. Do not hand-write HTML; the template exists so output is consistent across runs and diffable between them. See `references/report.md` for the payload schema.

Sections run: contradictions, flows, gaps, assumptions, questions. Contradictions lead because they need no inference — a reader can act on them without trusting anything downstream, which sets the right posture for the reconstruction that follows. Flows render as domain story diagrams with gaps drawn on the step where they bite; everything else is a table.

## Identity and refresh

IDs are permanent. `GAP-014` refers to the same finding forever, across every run. Never reissue, never renumber, never reuse an ID after deletion.

On `refresh`:

1. Read `answers.yaml`. Answered questions become corpus facts with high authority — higher than any document, since a human asserted them directly. Re-tag dependent items from `assumed` toward `stated`.
2. Re-run stages 1–7 against the updated corpus.
3. **Diff, do not replace.** Produce four buckets: new, changed basis, unchanged, and resolved by an answer.
4. Never silently drop a record a human has touched. If a gap marked `investigating` no longer appears in the fresh analysis, keep it and mark it `basis-changed` for human review.
5. Surface "records whose basis changed since last run" as its own report section. Silent drift is what turns a register into write-only noise by week three.

## Handling a thin corpus

If the corpus is too sparse to support flow reconstruction — under roughly five substantive documents, or no document describing an end-to-end process — do not proceed to stage 3. Producing thirty gaps from a one-page brief is hallucinating a domain.

Instead, stop after stage 2 and deliver the corpus map, the contradictions, and a scoping interview: which flows matter, who owns each system, what documents exist that you were not given. Say plainly that flow reconstruction needs more input, and what kind.

The same applies mid-run to an individual flow: if a flow would be more than about 60% `assumed`, do not analyse it. Report it as undocumented and move on.

## Reference files

- `references/extraction.md` — per-document extraction schema, system identification, handling corpora larger than context
- `references/flows.md` — EventStorming shape, domain story format, provenance tagging, reverse narrative and unhappy-path passes
- `references/taxonomy.md` — the ten gap types with probe questions, seam enumeration, the seam sweep procedure
- `references/questions.md` — question craft, routing, caps, worked examples of good and bad questions
- `references/report.md` — register, assumption and question schemas, and the report payload spec
