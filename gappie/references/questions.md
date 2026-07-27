# Questions (stage 7)

The questions are the deliverable. Flows, register and assumption map are intermediates that justify them. If the questions are weak, the run was a waste however good the document looks.

## Route by answerer, not topic

Group questions by **who can answer**, then by topic within that. This is what makes the output usable: a person opens one section, answers what they know, and never reads the rest. Topic grouping forces everybody to read everything, which means nobody reads anything.

Derive answerers from the corpus — document owners, named teams, vendors, roles that appear in flows. Where nobody obvious exists, the answerer is `UNASSIGNED` and that is itself a finding: a question nobody can answer means an unowned area, so register it as an `ownership` gap.

Typical answerer groups:

- Named individuals or roles where the corpus identifies one
- Teams — "EHR integration team", "clinical ops"
- External parties — "robot vendor engineering"
- `UNASSIGNED` — surface these prominently

## The two gates

### Gate 1: consequence

Every question must state what changes depending on the answer. If nothing changes, cut it — it is curiosity, and curiosity dressed as diligence is what makes these documents unreadable.

Write the consequence into the record, and render it beside the question. It does double duty: it proves the question earns its place, and it tells the answerer why their thirty seconds matter, which is most of what determines whether they answer at all.

### Gate 2: caps

Hard cap per answerer. Twelve is the ceiling; eight is better. Nobody answers forty questions — they answer eight and ignore a list of forty, so a list of forty yields fewer answers than a list of eight.

When over the cap, do not cut arbitrarily. Rank by discovery cost of the linked gap, then by how many other items depend on the answer. A question unblocking six downstream unknowns beats one unblocking a single detail even if that detail is more interesting.

Overflow goes into a clearly-marked deferred section, not into the main list. It should be visible without competing for attention.

## Question craft

**Answerable in the answerer's own knowledge.** "Does your FHIR endpoint support write to Observation?" is answerable. "What is the right write-back strategy?" is a design discussion — that is a meeting, not a question.

**One fact per question.** Compound questions get half answers, and you cannot tell which half.

**Closed where possible, open where necessary.** "Is plan import available programmatically, or console-only?" beats "How does plan import work?" Closed questions get answered; open ones get postponed. Add "if other, what?" rather than opening it up.

**Include what you currently believe.** State the assumption and ask for confirmation or correction. Correcting a wrong statement is far easier than composing an answer from nothing, and it surfaces disagreement you would not otherwise see.

**Name the source of the confusion.** "Doc A says X, doc B says Y — which holds?" lets the answerer resolve it in seconds.

## Worked examples

**Bad:** "How is patient identity handled across the platform?"
Too broad, no consequence, invites an essay. Cut or split.

**Good:** "We believe the platform joins EHR and imaging records on the site MRN. Doc `platform-prd:§3.2` implies this; nothing states it. Is the MRN the join key, or is there an enterprise identifier we should use instead?"
*Consequence: determines whether we need a master patient index component, which is roughly three weeks of work and a new operational dependency.*

**Bad:** "What are the performance requirements?"
Nobody knows what you mean; you will get "fast".

**Good:** "For imaging retrieval, what is the largest study size we must support end to end, and what wait is acceptable to a clinician at the point of use?"
*Consequence: decides whether we can stream on demand or must pre-fetch, which changes the storage footprint at every site.*

**Bad:** "Have you considered what happens if the robot is offline?"
Rhetorical, adversarial, and unanswerable as posed.

**Good:** "If the platform is unavailable at the time of the procedure, does theatre proceed using the existing manual process, or is the case postponed? We found no document covering this."
*Consequence: determines whether the platform is on the clinical critical path, which changes availability targets and the regulatory conversation.*

## Record schema

```yaml
- id: Q-021
  answerer: "Robot vendor — engineering"
  question: "Is programmatic plan import available under NDA, or is console import the only supported path?"
  we_believe: "Console-only, based on robot-sdk-overview:p.13"
  consequence: "If console-only, plan transfer needs a human step in theatre and the automated flow in platform-prd:§4.3 cannot be built as described"
  links: [GAP-014]
  discovery_cost: late
  rank: 1
  status: open        # open | answered | deferred
```

## Answers come back here

`answers.yaml` mirrors the question IDs:

```yaml
- id: Q-021
  answer: "Programmatic import exists in SDK v4.2 under NDA. Requires a signed integration agreement."
  answered_by: "M. Kaur, vendor eng"
  date: 2026-08-04
  confidence: high    # high | medium | low
```

On `refresh`, treat answers as corpus facts with authority above any document — a human asserted this directly, in context, knowing the question. Re-tag dependent flow events and gap records from `assumed` toward `stated`, and cite the answer as the source.

An answered question does not automatically close its linked gap. It changes the basis. A human still decides whether the gap is closed, and the report should present the answer next to the gap so that decision is easy to make.
