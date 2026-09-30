# Architectural lenses

Use these lenses as a discovery mechanism, not as a mandatory questionnaire. Apply the ones relevant to the system. A lens reveals a question or responsibility; it does not mandate a new service, store, queue, control, or work item. Report non-applicability only where it resolves a material ambiguity.

## 1. Outcome & scope
Look for:
- measurable user/business outcome;
- in-scope and out-of-scope behaviors;
- constraints and invariants;
- definition of success.

Prompts:
- What changes for the user when this exists?
- What must never happen?
- What is explicitly not being solved?

## 2. Actors & responsibilities
Look for:
- end users;
- admins/support;
- external organizations;
- automated actors/services;
- ownership and accountability.

Prompts:
- Who initiates this?
- Who approves, observes, supports, or revokes it?
- Who owns the result?

## 3. Journeys
Look for:
- entry points;
- prerequisites;
- main flow;
- alternate paths;
- termination and recovery.

Prompts:
- What happens immediately before and after?
- Where can the user leave and return?
- Is there a long-running or asynchronous path?

## 4. System boundaries
Look for:
- trust boundaries;
- service/API boundaries;
- organizational boundaries;
- cloud/account/tenant boundaries;
- local vs remote components.

Prompts:
- Where does responsibility change hands?
- Which side controls availability and change cadence?
- What cannot be assumed across the boundary?

## 5. Data & source of truth
Look for:
- core entities/events;
- authoritative system;
- read/write ownership;
- synchronization;
- freshness;
- retention and deletion;
- schema evolution.

Prompts:
- Where does this data originate?
- Who can change it?
- How stale can it be?
- What happens when two sources disagree?

## 6. Identity & correlation
Look for:
- user/resource identity;
- cross-system matching;
- duplicate identity;
- tenant/org context;
- external identifiers;
- merge/split behavior.

Prompts:
- How do we know X here is the same X there?
- What happens on no match or multiple matches?
- Are identifiers stable?

## 7. Permissions, consent & trust
Look for:
- authentication;
- authorization;
- delegation;
- consent;
- revocation;
- least privilege;
- auditability.

Prompts:
- Who may do what, to whose data?
- How is access granted and revoked?
- What happens to existing sessions/data after revocation?

## 8. Contracts & integration semantics
Look for:
- API/event/file contracts;
- protocol;
- versioning;
- rate limits;
- pagination;
- timeouts;
- compatibility;
- provider-specific behavior.

Prompts:
- What exactly crosses the boundary?
- Who owns the contract?
- What happens when one side changes?

## 9. State & lifecycle
Look for:
- states;
- transitions;
- terminal states;
- expiry;
- cancellation;
- retryable vs non-retryable states;
- reconciliation.

Prompts:
- What states can this thing be in?
- What can move it between states?
- What if a transition is interrupted?

## 10. Failure & partial failure
Look for:
- dependency outage;
- partial writes;
- timeout after success;
- duplicate delivery;
- retry storms;
- poison messages;
- inconsistent state;
- recovery path.

Prompts:
- What if this succeeds halfway?
- What if the caller retries after not seeing the response?
- Can the same command/event arrive twice?
- How is reconciliation performed?

## 11. Time, ordering & concurrency
Look for:
- event ordering;
- races;
- concurrent edits;
- clock/time-zone assumptions;
- delayed processing;
- scheduled behavior.

Prompts:
- Does order matter?
- What if two actors do this at the same time?
- Which timestamp is authoritative?

## 12. Scale & performance
Look for:
- expected and peak volume;
- latency expectations;
- payload size;
- fan-out;
- batching;
- backpressure;
- cost-sensitive hot paths.

Prompts:
- What grows with users/data/integrations?
- What happens at peak?
- Where is synchronous latency user-visible?

## 13. Security, privacy & compliance
Look for:
- sensitive data;
- encryption;
- secrets;
- access logs;
- data minimization;
- residency;
- regulatory controls;
- threat boundaries.

Prompts:
- What is the most sensitive thing crossing this system?
- Who should never be able to see it?
- What evidence must exist after an action?

## 14. Observability & supportability
Look for:
- metrics;
- logs;
- traces;
- correlation IDs;
- alerts;
- admin/support tooling;
- replay/retry capability;
- runbooks.

Prompts:
- How will we know this is broken before a user reports it?
- How will support diagnose one failed transaction?
- Can an operator safely recover it?

## 15. Rollout, migration & compatibility
Look for:
- existing data/users;
- backfill;
- feature flags;
- phased rollout;
- rollback;
- old clients/providers;
- dual-read/write;
- migration completion criteria.

Prompts:
- How do we get from today's world to the new world?
- Can old and new behavior coexist?
- What is rollback?

## 16. Testability & evidence
Look for:
- acceptance criteria;
- contract tests;
- integration environments;
- fixtures/sandboxes;
- failure injection;
- audit/evidence requirements.

Prompts:
- How do we prove this works end-to-end?
- Which failures must be reproducible?
- What dependencies need fakes/sandboxes?

## 17. Ownership & operations
Look for:
- service ownership;
- on-call/support ownership;
- SLAs/SLOs;
- dependency ownership;
- configuration;
- cost;
- decommissioning.

Prompts:
- Who owns this at 2 AM?
- Who can change configuration safely?
- What recurring operational work does this create?
