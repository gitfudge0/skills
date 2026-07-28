# Flows (stages 3–4)

Covers: flow selection, the event timeline, conversion to domain story sentences, provenance tagging, attaching gaps to steps, and the reverse-narrative and unhappy-path passes.

Notation follows the Domain Storytelling quick-start guide: <https://domainstorytelling.org/quick-start-guide>

## Choosing flows

Aim for two to five flows, each an end-to-end path delivering something to somebody outside the system. Not one flow per feature — feature-shaped flows never cross a seam, and seams are where the gaps live.

Good boundaries start at an external trigger and end at an external outcome:
- "Referral received → procedure performed → result visible to patient"
- "Clinician requests a plan revision → revised plan executed"

Bad ones are internal slices: "user logs in", "data syncs".

Prefer flows crossing the most organisational boundaries. Where two candidates cover similar ground, keep the one touching more owners.

Follow the guide's scenario-based principle: model the concrete 80% case, not every branch. Variations become annotations, or their own flow if they are genuinely different stories. Resist modelling conditionals — premature abstraction hides the holes you are looking for.

## Stage 3 — event timeline first

Before writing sentences, lay the flow out as a chronological list of domain events — things that happened, past tense, in the domain's language. This is a thinking tool, not an artifact: it is fast, it exposes ordering problems, and it stops you committing to actors before you know who they are.

Do not model commands, aggregates or read models. That is design-level work; this pipeline is exploratory.

## Stage 4 — convert to domain story sentences

Each event becomes a sentence in the pictographic language. The basic syntax is **subject – predicate – object**:

> **actor** — *verb* — **work object** — **actor**

- **Actors** are nouns that act: a `person`, a group of `people`, or a `system`. Every actor appears exactly once in the story, which is why the renderer draws each as a single lane.
- **Work objects** are nouns that get exchanged: a `document`, a `digital` object, a `physical` thing, or `info` about something (the guide's speech-bubble case, for spoken or messaged information). A separate work object is drawn for *every* activity, even when it is nominally the same object — because its status or representation usually changes as the story moves.
- **Activities** are verbs, in the domain's own language. "Approves", "transfers", "returns" — not "processes" or "handles".
- **Sequence numbers** order the sentences and are what a reviewer points at when they say "that step is wrong".
- **Annotations** carry variations, error cases and assumptions. In this pipeline they do heavy lifting: every bridge you made becomes an annotation.

Use the domain's vocabulary, not the architecture's. If clinicians say "case", write case even where the internal model says `ProcedureRequest`. Vocabulary drift between the story and the documents is itself a finding — route it to the glossary.

## Provenance tagging

Every sentence carries one of three tags. The value of the whole report rests on this discipline.

- **`stated`** — a document describes this. Cite it. Renders as a solid arrow.
- **`implied`** — two or more stated things make it necessary. Cite both, explain in `basis`. Renders dashed amber.
- **`assumed`** — you bridged a hole. Nothing supports it. Record what you assumed and why. Renders dashed red, and the whole row is shaded.

The temptation is to upgrade `assumed` to `implied` because the assumption feels obvious. Resist it. The "obvious" assumptions in integration work — identifiers are stable, a system can write as well as read, events arrive in order — are exactly the ones that cost six months.

Calculate `assumed_ratio` per flow. Above roughly 0.6, do not analyse the flow: report it as undocumented, name the documentation that would fix it, and move on. Analysing a flow you mostly invented produces confident findings about a process that does not exist.

## Attaching gaps to sentences

Any gap that bites at a specific step carries that step's number, and the step carries the gap id. The renderer draws the gap inline on that row of the diagram, with its closure action underneath — so a reader meets the gap where it happens rather than in a list somewhere else.

Attach a gap to a step when the step is where the gap manifests. Leave `gaps` empty for cross-cutting gaps — ownership of a whole seam, per-site variance, a missing glossary term. Those live in the register table only. Do not force attachments to make the diagram look busy; a diagram where every row is shaded conveys nothing.

## Flow YAML

```yaml
flow_id: FLOW-02
name: "Referral to procedure to patient-visible result"
scope: "As-is + to-be, digitalized. Referral in the EHR through result visible in the patient app."
assumed_ratio: 0.33

actors:
  - { name: "Referring clinician", kind: person }
  - { name: "EHR",                 kind: system }
  - { name: "Platform",            kind: system }
  - { name: "Theatre technician",  kind: person }
  - { name: "Robot controller",    kind: system }

events:
  - seq: 1
    subject: "Referring clinician"
    verb: "records"
    work_object: "referral"
    work_object_kind: document
    object: "EHR"
    provenance: stated
    sources: [platform-prd:§2.1]

  - seq: 5
    subject: "Theatre technician"
    verb: "transfers"
    work_object: "approved plan"
    work_object_kind: physical
    object: "Robot controller"
    provenance: assumed
    basis: "Plan exists at step 4 and is executing at step 6. Nothing describes the transfer. Vendor doc states import is console-only."
    annotation: "Possibly a USB handoff; unconfirmed."
    seam: "planning-software→robot-controller"
    gaps: [GAP-014]
```

Declare `actors` explicitly — it fixes lane order in the diagram, and reading order matters. If omitted, the renderer derives them in order of first appearance, which is usually acceptable but rarely optimal.

Keep to six actors or fewer per flow. Beyond that the lanes get narrow, and the story is probably two stories.

`object` may be omitted where a sentence has no recipient. Where `subject` and `object` are the same actor the renderer draws a self-loop, which is correct for "the system checks its own record".

`seam` is what links stages 4 and 5 — the seam sweep inherits these, so a sentence crossing a boundary should always name it.

## Reverse narrative pass

Walk the story backwards. At each sentence ask: what must already be true for this to happen?

Then check whether anything earlier makes it true. Where nothing does, you have found a hole the forward pass concealed — forward narration builds momentum that carries a reader over missing preconditions, and reading backwards removes it.

Typical yield: unestablished identity, missing authorisation, absent state, data appearing without a source.

```yaml
- flow: FLOW-02
  at_step: 6
  precondition: "Controller holds the currently approved plan version"
  established_by: null
  finding: "Nothing establishes which version the controller holds, or that it matches the approved one"
```

Every unestablished precondition becomes a register entry, attached to that step.

## Unhappy-path pass

For each sentence, apply this list. Most integration gaps live here, not on the happy path.

| Perturbation | Probe |
|---|---|
| Cancelled | Upstream cancels after this step. What happens to work already done downstream? |
| Amended | Input is corrected after use. Does anything recompute? Is the earlier output retracted? |
| Duplicated | The trigger fires twice. Does this step produce two effects? |
| Out of order | This step's input arrives after the next step's. Is ordering enforced, or assumed? |
| Upstream down | Source unavailable. Does the flow block, queue, degrade, or fail silently? |
| Downstream down | Destination unavailable. Is the result buffered, retried, or lost? |
| Identity changed | Subject merged, renamed or re-keyed after this step. Do in-flight items relink? |
| Late arrival | Input arrives long after expected. Still valid? Is there a staleness rule? |
| Partial | Only some expected data arrives. How is completeness determined at all? |
| Timeout | The step takes far longer than expected. Who notices? |

You will not run all ten against every sentence — that is forty probes on a ten-step flow, and most yield nothing. Prioritise:

- Sentences crossing a seam (all ten)
- Sentences where a human takes an irreversible action (cancelled, amended, identity changed)
- Sentences consuming data produced much earlier (late arrival, amended, identity changed)

Record findings with the perturbation named, so a reviewer can see the coverage pattern and spot what was not probed:

```yaml
- flow: FLOW-02
  at_step: 4
  perturbation: amended
  finding: "Imaging is corrected and re-issued after the plan is approved. No document describes whether the plan is invalidated."
  seam: pacs→platform
```

Findings manifesting at a specific step belong in that step's `gaps` list, so they render on the diagram rather than only in the table.
