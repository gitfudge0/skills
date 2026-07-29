# Taxonomy and seam sweep (stage 5)

Covers: why the taxonomy exists, seam enumeration, the ten gap types with probes, the sweep procedure, quality gates, and discovery-cost scoring.

## Why a taxonomy

You cannot find a gap you have no name for. Unstructured review reliably finds the same three or four gap types — usually missing features, unclear requirements and integration difficulty — and reliably misses lifecycle, temporal and ownership gaps entirely, because nobody thought to look for a category they had not named.

Sweeping mechanically fixes this. It is boring and high-yield. Do not replace it with judgement.

## Seam enumeration

A seam is any point where two systems, two teams, or two organisations exchange something. Enumerate before sweeping:

1. Collect every `seam` tagged on flow events.
2. Add every system pair the corpus implies exchanges data, even where no flow reaches it.
3. Add human-to-human handoffs where work changes hands with no system in between. These are seams and they are almost never documented.
4. Add self-seams for systems talking to their own future selves across a long gap — a plan stored in March and executed in June crosses a version boundary.

Then build the seam grid: systems × systems, cell = seam exists. **Cells you have not examined are more dangerous than cells full of gaps**, because an unexamined seam has an unknown gap count and an examined one has a known count. Track examined-versus-existing explicitly and report the ratio.

## The ten types

Each type has probes. Run every probe against every seam. Most return nothing; that is expected and is the cost of the ones that return something.

### 1. Semantic
Does the same word mean the same thing on both sides?
- Which terms cross this seam? Does the glossary show a conflict for any?
- Units, precision, timezone, encoding — stated or assumed?
- Enumerations: does each side accept the other's full value set?
- Does "complete", "final", "approved" or "active" mean the same on both sides?

### 2. Identity
Can a record be joined across this seam?
- What key joins them? Is it stable, unique, and present on both sides?
- Who mints it? What happens on collision?
- Merge, split, rename, re-key — does the other side learn?
- Are there several identifier namespaces in play, and is the assigning authority carried?

### 3. Contract
Does the interface support the operation needed, in the direction needed?
- Is the operation documented, or assumed to exist?
- Read only, or write too? Write-back is where this most often fails.
- Push or pull? Who initiates? Is there a subscription or only polling?
- Rate limits, payload limits, batch limits — stated?
- Is the interface versioned? What happens when the vendor ships a new one?

### 4. Trigger and state
What exactly fires this, and is the upstream thing really finished?
- What is the precise triggering event, as opposed to the approximate one?
- How is upstream completeness determined? First item arriving is not completion.
- Is there a state machine, or is state inferred from message arrival?
- What blocks the transition, and who can override?

### 5. Temporal
- Which time is carried — occurrence, documentation, transmission, receipt?
- Are clocks synchronised across these systems? Verified, or assumed?
- Is ordering guaranteed by transport, or by nothing?
- Is there a staleness rule? At what age does this data stop being usable?

### 6. Lifecycle
Cancel, amend, supersede, retract, withdraw — almost always unmodelled.
- Can the upstream record be cancelled after transfer? Then what?
- Corrections: overwrite, version, or both?
- Is there a retraction path for something already delivered downstream?
- Are superseded versions retained, and can you tell which was used?

### 7. Failure
- Retry policy? Bounded? Idempotent on the receiving side?
- Duplicate detection — on what key?
- What happens during downtime on either side? Queue, block, degrade, or drop?
- Can a message be lost without anyone noticing? What reconciles?
- Is there a defined fallback when this seam is unavailable, and does the business process survive it?

### 8. Policy
- Who is authorised, for what purpose, and how is that enforced at this seam?
- Consent: required, captured, revocable? Does revocation propagate?
- Where does the data physically go, and is that permitted?
- What is logged, and does the log itself carry sensitive content?
- Regulatory classification: does moving this data across this seam change the product's obligations?

### 9. Ownership
- Who owns this seam at 3am? Name a team, not a system.
- Who is called when it breaks, and do they know they own it?
- Who approves a change to the contract, and who must be told?
- When the vendor on one side upgrades, whose backlog absorbs it?

Unowned seams are gaps by definition. When neither side's documentation claims a seam, register it with high discovery cost regardless of technical difficulty.

### 10. Variance
Is this one integration or N?
- Does this seam behave identically at every site, tenant, region or customer?
- What varies — versions, permissions, network topology, configuration, local conventions?
- Is per-instance configuration separated from the core, or does each deployment fork the code?
- How is a new instance onboarded, and who confirms it conforms?

Variance is the most under-detected type in platform work, because every document describes the seam as though there were one of it.

## Sweep procedure

One seam at a time. Sweeping all seams at once produces the gap-analysis equivalent of test case vomit.

For each seam:

1. Gather everything the corpus says about it — extracts, flow events, unhappy-path findings.
2. Run all ten types' probes.
3. Draft candidate gaps.
4. Apply the quality gates below.
5. Rank, cap at five, cut the rest.
6. Write records.

### Quality gates

Every candidate passes all four or it is cut.

**Specific** — names the thing that breaks, not the category. "No agreed join key between site MRN and enterprise identifier" passes; "identity management concerns" does not.

**Falsifiable closure** — you can state what would resolve it. If you cannot, it is an anxiety. Cut it.

**Surprising** — would a competent engineer already on this team be surprised? "The API needs authentication" would not. Cut it.

**Grounded or honestly flagged** — either it traces to corpus evidence, or its `provenance` is `assumed` and `basis` explains the pattern you are reasoning from. Never present an inference as a finding.

### The cap is load-bearing

Capping at five per seam forces ranking, and ranking is where the thinking happens. A twelve-gap seam list is a list nobody reads; a five-gap list with seven cut is a judgement. Record cut candidates in a `cut` field if useful for review, but keep them out of the main register.

## Record schema

```yaml
- id: GAP-014
  seam: platform→robot-controller
  flow: FLOW-02
  at_step: 7
  type: contract
  claim: "Plan transfer path to the controller is undefined; vendor doc states import is console-only"
  provenance: implied
  sources: [robot-sdk-overview:p.13, platform-prd:§4.3]
  basis: "PRD requires automated plan delivery; vendor doc describes only manual console import"
  closure: "Confirm with vendor engineering whether a programmatic import exists under NDA, or whether manual import is the intended path"
  closure_kind: external-contact   # decision | spike | external-contact | site-visit | build
  discovery_cost: late
  owner: null
  status: open
  first_seen: run-2026-07-27
```

## Discovery cost

Score mechanically. This is the one ranking dimension the skill may compute, because it depends on structure rather than on whose risk matters.

| Value | Meaning |
|---|---|
| `now` | Surfaces in design or first integration attempt |
| `mid` | Surfaces in system test or first end-to-end run |
| `late` | Surfaces in a pilot, at a second deployment site, or in production |
| `never` | Fails silently — wrong data, wrong record, no alarm. Worst class. |

`never` outranks everything. A gap producing silent incorrectness beats a higher-impact gap that announces itself immediately, because the announcing one gets fixed for free during normal work.

Report discovery cost alongside gaps but **do not produce an overall priority ordering** — that decision belongs to humans who know whose risk matters here.
