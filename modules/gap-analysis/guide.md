# Requirements discovery and gap analysis

Internal capability: enter through the owning public skill. Resolve cross-module and shared paths from the package root (nearest ancestor containing `.fudge-package.json`): `references/modules/<module>/guide.md`, `references/roots/<root>/guide.md`, and `shared/`. In source, use the repository identified by `scripts/skill-manifest.json`, with `modules/`, `fudge-<root>/SKILL.md`, and `shared/`. Local assets and references remain relative to this guide.

Use a bounded requirements check for a clear request, a focused gap list for incomplete scope, and this full corpus pipeline only for scattered or conflicting requirements. Analysis-only requests stop before implementation. Use evidence to resolve gaps and continue independent work; ask only about consequential unresolved choices. The full pipeline produces: reconstructed flows, a gap register, an assumption map, and — the actual deliverable — a routed list of questions humans must answer.

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

## Evidence and decision boundaries

Stay inside these lines. Exceeding them is how the output becomes untrustworthy.

- **Propose priorities transparently.** Use consequence, dependencies, and discovery cost to recommend ordering. Record the rationale and honor the accountable owner’s existing decisions; do not present a proposed ranking as stakeholder agreement.
- **Close only against evidence.** A gap with an objective closure action can be resolved when the action is verified. Preserve the evidence and history; a gap requiring a stakeholder decision remains open until that decision is recorded. Never override an existing human disposition silently.
- **It does not replace contact with reality.** Site visits, vendor calls and watching the real process cannot be simulated. When a gap can only close that way, say so in the closure action.
- **It does not invent domain facts to fill gaps.** If the corpus does not say how the robot receives a plan, the answer is a question, never a guess dressed as a finding.

## Modes

Pick based on what the user asked for. Default to the smallest analysis that can answer the request. Use a focused requirements check for ordinary build requests; use `map` when a large corpus needs inventory before choosing depth.

| Mode | Trigger | Does |
|---|---|---|
| `check` | Clear or partially specified build request | Read relevant code and sources, identify consequential missing behavior/dependencies/acceptance criteria, resolve supported answers, and report remaining choices in chat. No workshop artifacts by default. |
| `map` | "what have we got", first contact with a corpus | Stage 0 only. Document inventory and coverage grid. Minutes, not hours. |
| `run` | Explicit corpus analysis or scattered/conflicting requirements needing reconstruction | Full pipeline, stages 0–8. |
| `refresh` | Humans have filled in `answers.yaml`, or documents changed | Re-runs against updated inputs, **diffing** against the existing register. Never regenerates from scratch. |

## Workspace

All artifacts live beneath one output root. Resolve the default with package-root `shared/artifacts.md` using category `gap-analysis`. A caller may supply another output root; use it for the whole run and create it if absent. Resolve every artifact path below against that root, including `map` and thin-corpus outputs. Do not also write to the default directory when an override is present.

State persists per branch: `refresh` diffs `register.yaml` and reads `answers.yaml` from that same branch's directory. Nothing is shared across branches.

```
<output-root>/
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
  payload.json           stage 8 — JSON payload rendered into report.html
```

`register.yaml` is canonical. Everything else is either an input to it or a rendering of it. `report.html` is disposable and regenerated every run.

## Output location

Follow package-root `shared/artifacts.md` for path resolution, caller overrides, collision handling, and repository exclusions. The default artifact category is `gap-analysis`. Product files retain their established project locations; a chat-only answer creates no artifact.

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

Work **one seam at a time**. Sweeping everything at once is how you get the gap-analysis equivalent of test case vomit: forty generic findings nobody reads. Keep every distinct valid gap in the canonical register. Rank the summary to show the top five per seam; list additional entries as deferred or lower priority with their IDs and closure actions. Summary limits must never delete findings.

Every record needs a falsifiable closure action. If you cannot say what would resolve it, it is an anxiety, not a gap. Cut it.

Where a gap bites at a specific step, add its id to that sentence's `gaps` list so it renders inside the flow diagram rather than only in a table. Cross-cutting gaps — seam ownership, per-site variance, terminology — stay in the table.

Write `register.yaml`.

### Stage 6 — Assumption map

Extract every load-bearing belief. Plot on importance × evidence.

Count supporting sources mechanically and group copied or common-origin documents as one source family. A count is coverage, not proof of independent corroboration or correctness. Record ownership, recency, directness, contradictions, and source families alongside the count; do not turn model confidence into evidence. Importance asks whether being wrong changes the design.

Write `assumptions.yaml`. See `references/report.md` for the schema.

### Stage 7 — Questions

Convert unknowns into questions, grouped by **who can answer**, not by topic. That routing is what makes the document usable: the EHR integration lead opens one section, answers eight questions in half an hour, and never reads the rest.

Two gates, both strict — see `references/questions.md`:
- Every question must name what you would do differently depending on the answer. If nothing changes, cut it.
- Hard cap per answerer. Nobody answers forty questions; they answer eight and ignore a list of forty.

Write `questions.yaml`.

### Stage 8 — Render

Populate `assets/report-template.html` and write `<output-root>/report.html`. The template is self-contained — no network dependencies, works offline, prints sensibly.

Substitute serialized JSON into the `__GAP_ANALYSIS_DATA__` placeholder, escaping `<` as `\u003c` so source text cannot terminate the script element. Do not hand-write HTML; the template exists so output is consistent across runs and diffable between them. See `references/report.md` for the payload schema.

Sections run: contradictions, flows, gaps, assumptions, questions. Contradictions lead because they need no inference — a reader can act on them without trusting anything downstream, which sets the right posture for the reconstruction that follows. Flows render as domain story diagrams with gaps drawn on the step where they bite; everything else is a table.

## Identity and refresh

IDs are permanent. `GAP-014` refers to the same finding forever, across every run. Never reissue, never renumber, never reuse an ID after deletion.

On `refresh`:

1. Read `answers.yaml`. Compare each answer with the documents using the answerer’s ownership and authority over the subject, supporting evidence, and date. Cite answers as attributed statements; a recent answer from the accountable owner may supersede an older document, while an unsupported or conflicting answer remains unresolved. Do not silently convert a disputed assumption into a fact.
2. Re-run stages 1–7 against the updated corpus.
3. **Diff, do not replace.** Produce four buckets: new, changed basis, unchanged, and resolved by an answer.
4. Preserve every existing ID and recorded human disposition. If a gap no longer appears in fresh analysis, keep its history and mark its basis changed or resolution proposed; never silently delete it or override a human disposition.
5. Surface "records whose basis changed since last run" as its own report section. Silent drift is what turns a register into write-only noise by week three.

## Handling a thin corpus

If the corpus is too sparse to support flow reconstruction — no supported account of the relevant end-to-end process — do not proceed to stage 3. Judge substance, not document count: one complete specification may suffice; many thin documents may not. Record missing evidence without inventing a domain.

Instead, stop after stage 2 and deliver the corpus map, the contradictions, and a scoping interview: which flows matter, who owns each system, what documents exist that you were not given. Say plainly that flow reconstruction needs more input, and what kind.

The same applies mid-run to an individual flow: if a flow would be more than about 60% `assumed`, do not analyse it. Report it as undocumented and move on.

## Reference files

- `references/extraction.md` — per-document extraction schema, system identification, handling corpora larger than context
- `references/flows.md` — EventStorming shape, domain story format, provenance tagging, reverse narrative and unhappy-path passes
- `references/taxonomy.md` — the ten gap types with probe questions, seam enumeration, the seam sweep procedure
- `references/questions.md` — question craft, routing, caps, worked examples of good and bad questions
- `references/report.md` — register, assumption and question schemas, and the report payload spec
