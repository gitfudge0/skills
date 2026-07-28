# Schemas and rendering (stages 6 and 8)

Covers: the assumption map, the report payload schema, how to render, and the refresh diff.

## Assumption map

An assumption is a load-bearing belief: something the design rests on that could turn out false. Extract them from `assumed`-tagged flow sentences, from gap records whose provenance is `assumed`, and from claims stated once in a single document with no corroboration.

**Derive the evidence axis mechanically.** Count independent corpus sources supporting the belief. Independent means different documents from different authors — six revisions of one PRD is one source, and a document quoting another is not a second source. A model rating its own confidence is not evidence; a source count is a fact about the corpus that a reviewer can check.

Judge importance: if this is wrong, does the design change? Binary — `high` or `low`. Resist a middle band; it absorbs everything and the table stops discriminating.

```yaml
- id: ASM-007
  claim: "The robot controller can accept a plan from an external system"
  importance: high
  sources: []                 # empty = unevidenced
  origin: FLOW-02:step-5
  falsifier: "Vendor confirms console-only import"
  links: [GAP-014, Q-021]
```

`falsifier` is what makes this a testable belief rather than a worry. If you cannot state what would prove it false, it is not an assumption — it is a mood. Cut it.

The table sorts important-and-unevidenced to the top. That block is the output that matters; everything else is context.

## Report payload

Stage 8 builds one JSON object and substitutes it for the literal string `__GAP_ANALYSIS_DATA__` in `assets/report-template.html`, writing the result to `.gap-analysis/report.html`.

```json
{
  "meta": { "project": "…", "run_id": "run-2026-07-27", "date": "27 July 2026", "mode": "run" },
  "corpus": { "doc_count": 41 },
  "contradictions": [
    { "id": "CONTRA-003", "kind": "sequence",
      "claim_a": { "text": "…", "source": "doc-id:loc" },
      "claim_b": { "text": "…", "source": "doc-id:loc" },
      "note": "why it matters" }
  ],
  "flows": [
    { "flow_id": "FLOW-02", "name": "…", "scope": "…", "assumed_ratio": 0.33,
      "actors": [ { "name": "Theatre technician", "kind": "person" } ],
      "events": [
        { "seq": 5, "subject": "Theatre technician", "verb": "transfers",
          "work_object": "approved plan", "work_object_kind": "physical",
          "object": "Robot controller", "provenance": "assumed",
          "basis": "…", "annotation": "…", "sources": [], "gaps": ["GAP-014"] }
      ] }
  ],
  "register": [
    { "id": "GAP-014", "seam": "planning-software→robot-controller", "type": "contract",
      "claim": "…", "provenance": "implied", "sources": ["doc-id:loc"], "basis": "…",
      "closure": "…", "closure_kind": "external-contact",
      "discovery_cost": "late", "owner": null, "status": "open" }
  ],
  "assumptions": [
    { "id": "ASM-007", "claim": "…", "importance": "high", "sources": [],
      "origin": "FLOW-02:step-5", "falsifier": "…", "links": ["GAP-014"] }
  ],
  "questions": [
    { "id": "Q-021", "answerer": "Robot vendor — engineering", "question": "…",
      "we_believe": "…", "consequence": "…", "links": ["GAP-014"], "status": "open" }
  ],
  "changes": { "new": [], "basis_changed": [], "resolved": [] }
}
```

Omit `changes` entirely on a first run — the template hides the section when absent.

### Enumerations the template depends on

| Field | Values |
|---|---|
| `provenance` | `stated` · `implied` · `assumed` |
| `discovery_cost` | `now` · `mid` · `late` · `never` |
| `status` (gap) | `open` · `investigating` · `closed` · `accepted` · `basis-changed` |
| `status` (question) | `open` · `answered` · `deferred` |
| `importance` | `high` · `low` |
| actor `kind` | `person` · `people` · `system` |
| `work_object_kind` | `document` · `digital` · `physical` · `info` |
| `answerer` | any string, or `UNASSIGNED` |

Values outside these fall through to neutral styling — nothing breaks, but the visual encoding is lost, so stick to them.

### Gaps render twice, on purpose

A gap listed in a sentence's `gaps` array is drawn **inside the flow diagram**, on the row where it bites, with its closure action beneath it. Every gap also appears in the register table. That redundancy is deliberate: the diagram answers "where does this hurt", the table answers "what is outstanding and who owns it", and those are different questions asked by different readers.

Cross-cutting gaps with no sensible step — seam ownership, per-site variance, terminology — appear in the table only. Do not manufacture an attachment.

## Rendering

Do not hand-write HTML. The template exists so runs are consistent, comparable and diffable; a bespoke document each time destroys all three.

```bash
python - <<'PY'
import json, pathlib
tpl = pathlib.Path("<skill>/assets/report-template.html").read_text()
data = json.loads(pathlib.Path(".gap-analysis/payload.json").read_text())
out = tpl.replace("__GAP_ANALYSIS_DATA__", json.dumps(data, ensure_ascii=False))
pathlib.Path(".gap-analysis/report.html").write_text(out)
PY
```

Use `json.dumps`, never string concatenation — claims contain quotes, arrows and unbalanced brackets that will break the payload silently.

The template is fully self-contained: no network requests, no web fonts, works offline, prints sensibly. Keep it that way. A report needing a CDN is a report that stops working when it is emailed to the one person who most needed to read it.

The flow diagrams are generated as SVG by the template at render time from the sentence data — you supply structure, never coordinates. Layout is deterministic, so two runs of the same flow produce the same picture and a visual diff means something changed.

### Section order is deliberate

Contradictions, flows, gaps, assumptions, questions.

Contradictions lead because they need no inference at all — a reader can act on them without trusting anything downstream. That sets the correct posture for the reconstruction that follows.

Coverage findings from stage 0 do not get their own section. They enter the register as `evidence`-type gaps and appear in the gaps table alongside everything else, which keeps the finding and drops the ceremony.

## Refresh diff

On `refresh`, compute `changes` by comparing the fresh analysis against the previous `register.yaml`.

| Bucket | Contents |
|---|---|
| `new` | Records with no matching prior ID |
| `basis_changed` | Prior ID whose `basis`, `sources` or `provenance` changed |
| `resolved` | Prior ID whose linked question now has an answer in `answers.yaml` |

Rules that keep the register trustworthy over months:

- **Never reissue an ID.** `GAP-014` is that finding forever. Deleted IDs stay retired.
- **Never silently drop a human-touched record.** If a gap marked `investigating` or `accepted` no longer appears in the fresh analysis, keep it and set `status: basis-changed` with a note. A record disappearing because a document was reworded is a bug, not a resolution.
- **Never auto-close.** An answer changes the basis; a human decides whether the gap is closed. Render the answer beside the gap so that decision takes seconds.
- **Surface drift as its own section.** Silent divergence between register and reality is what turns this into write-only noise by week three, and by then nobody trusts any of it.

Preserve human-authored fields across refreshes without exception: `owner`, `status`, and any note a person added. Those are the only fields in the file that were not machine-generated, which makes them the most valuable content in it.
