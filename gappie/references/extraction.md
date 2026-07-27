# Extraction (stages 0–2)

Covers: identifying systems before you have read everything, the per-document extraction schema, citation format, corpora larger than context, glossary collation, and contradiction detection.

## Identifying systems early

Stage 0 needs a system list before stage 1 has read anything properly. Get it cheaply:

1. Skim filenames, titles and headings across the whole corpus.
2. Pull proper nouns that appear in a technical-participant position — things that send, receive, store, or are integrated with.
3. Include external parties and vendors even when no document describes them. **Especially** then: a system everybody references and nobody documents is the highest-value cell in the coverage grid.
4. Include the human actor groups too — they are participants in flows and they own seams.

Do not over-refine. The list gets corrected during stage 1; its stage-0 job is only to give the coverage grid its axis.

## Coverage grid

Rows: systems and journey phases. Columns: documents, or document clusters if there are many.

Cell value is substantive coverage, not mentions. A document that names a system in a bullet list does not cover it. Score each cell:

- `2` — describes behaviour, interface, or data in usable detail
- `1` — mentions with some context
- `0` — absent

Row totals give you the story. Any row summing to `0` or `1` becomes a register entry immediately, type `evidence`, provenance `stated` — you are not inferring that documentation is missing, you are observing it.

## Per-document extraction

Write one `extracts/<doc-id>.yaml` per document. Keep `<doc-id>` short, stable and derived from the filename so it survives re-runs.

```yaml
doc_id: robot-sdk-overview
source: vendor/robot-sdk-overview.pdf
type: vendor-doc          # spec | prd | api-doc | vendor-doc | notes | diagram | email | ticket | other
date: 2026-03-11          # null if undeterminable
owner: "Vendor — integrations team"   # null if unclear
summary: "Overview of the surgical robot SDK; connectivity and telemetry only."

systems:
  - name: Robot controller
    role: "Executes loaded plan; emits telemetry"
    loc: "p.4"

actors:
  - name: Theatre technician
    role: "Loads plan, confirms readiness"
    loc: "p.7"

events:
  - text: "Plan loaded onto controller"
    loc: "p.7"
  - text: "Case marked ready"
    loc: "p.8"

entities:
  - name: Case
    attributes: [case_id, plan_version, patient_ref]
    loc: "p.5"

terms:
  - term: "case"
    meaning: "One scheduled procedure on one controller"
    loc: "p.5"

claims:
  - text: "SDK exposes read-only telemetry endpoints"
    loc: "p.12"
    kind: constraint      # capability | constraint | intent | number | decision
  - text: "Plan import is performed via vendor console only"
    loc: "p.13"
    kind: constraint

silences:
  - "No mention of how a plan reaches the controller from an external system"
  - "No error or failure behaviour described anywhere"
```

### The `silences` field carries unusual weight

What a document conspicuously fails to say, given what it is, is evidence. An API document with no error semantics, a workflow spec with no cancellation path, a vendor overview that never mentions authentication — each is a finding with `provenance: stated`, because you are reporting an observable property of the document rather than inferring anything.

Populate it deliberately. Ask of each document: given its type and title, what would a reader reasonably expect to find here that is not here?

## Citation format

Every downstream statement traces back through `doc_id` plus `loc`. Use whatever locator the source supports — page, section number, heading text, slide number, line range, timestamp. Be specific enough that a reviewer can find it in under ten seconds; that is the whole test.

Cite as `doc-id:loc`, for example `robot-sdk-overview:p.12`.

## Corpora larger than context

Stage 1 is deliberately a map step so the rest of the pipeline reads extracts rather than sources.

- Process documents one at a time, writing each YAML before opening the next.
- Never hold more than a few raw documents in context simultaneously.
- If a single document exceeds context, extract it section by section, appending to the same YAML.
- For very large corpora, cluster near-duplicates at stage 0 (six revisions of the same PRD) and extract only the latest, noting the superseded ones in `corpus-map.md`. Version churn itself sometimes indicates an unstable requirement worth registering.

## Glossary collation

Collate `terms` across all extracts.

```yaml
- term: "case"
  senses:
    - meaning: "One scheduled procedure on one controller"
      sources: [robot-sdk-overview:p.5]
    - meaning: "A patient's full episode of care, referral through follow-up"
      sources: [platform-prd:§2.1, clinical-workflow-notes:p.2]
  conflict: true
  note: "Used in both senses in the same corpus. Any interface using 'case_id' is ambiguous."
```

`conflict: true` always produces a register entry. Semantic mismatches at seams are among the most expensive gaps in integration work and among the cheapest to find — they need no inference, only collation.

## Contradiction detection

Look for pairs of claims that cannot both be true.

```yaml
- id: CONTRA-003
  claim_a:
    text: "Plan approval occurs before imaging review"
    source: clinical-workflow-notes:p.2
  claim_b:
    text: "Imaging review gates plan generation"
    source: platform-prd:§4.3
  kind: sequence          # sequence | ownership | data-flow | number | capability | policy
  note: "Ordering differs. One of these documents describes a process that is not the one being built."
```

Prefer under-reporting to over-reporting. Two documents at different levels of abstraction, or written at different times, are not necessarily contradicting each other — say so in `note` rather than manufacturing conflict. A contradiction list that includes soft disagreements loses its authority, and its authority is the point.

Contradictions render first in the report, ahead of everything else. They are the findings a reviewer can act on without trusting any of your inference.
