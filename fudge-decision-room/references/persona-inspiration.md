# Persona inspiration by domain

These are warm-up examples, not a checklist. Real casting should react to the specific company/topic found in Phase 1 — rename, merge, split, or invent roles as needed. A 5-person startup doesn't have a "VP of Platform"; a regulated fintech probably needs a compliance voice even for a small feature.

## Quick-commerce / consumer delivery
- PM — repeat-purchase behavior, conversion
- Design — flow friction, where the interaction lives
- Backend Eng — data model, scale, latency at read-heavy traffic
- Catalog/Ops — SKU volatility, per-store inventory reality (the "boring but real" constraint here — products go out of stock hourly)
- Growth — the retention loop this could unlock (notifications, personalization signal)
- Support lead — likely ticket volume from edge cases

## Fintech / regulated consumer
- PM — user trust, activation
- Compliance/Legal — regulatory exposure, audit trail requirements
- Backend Eng — data integrity, reconciliation
- Risk — fraud surface area a new feature opens up
- Design — clarity under regulatory copy constraints
- Support — dispute/chargeback volume implications

## B2B SaaS
- PM — expansion revenue, churn risk
- Sales/CS — what prospects and renewals are actually asking for
- Eng lead — technical debt tradeoff, maintenance burden
- Security — access control, tenant isolation implications
- Design — configurability vs. simplicity tension

## Dev tools / infra
- PM — adoption within existing workflows
- Eng (core maintainer) — backward compatibility, API surface growth
- DX/Docs — how the change will need to be explained
- SRE/Infra — operational burden, blast radius if it fails
- Skeptic — "does this belong in core, or should it be a plugin/extension"

## Social / consumer community apps
- PM — engagement loop, novelty vs. retention
- Trust & Safety — abuse surface a new feature opens
- Design — social dynamics (does this create comparison, pressure, gaming behavior)
- Growth — virality mechanics
- Eng — feed/notification infra load

## Always worth casting regardless of domain
- Someone whose job is to say "why are we building this at all" — a genuine skeptic, not a strawman
- Whoever eats the consequence after launch (ops, support, on-call) — usually the most undervalued voice in the room
