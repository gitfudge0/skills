# Output guidance

Lead with the desired outcome, the known system shape, and the uncertainty most likely to change the work. Keep a thin brief compact; expand detail only where it resolves a real dependency, risk, or decision. Do not fill missing detail with a larger diagram or speculative backlog.

A capability/work table can carry most of a small result:

| Capability / candidate work | Basis and responsibility | Dependencies / unresolved decisions | Observable acceptance evidence |
|---|---|---|---|
| Investigation or capability | Known source, inference, or proposal and why it matters | Prerequisites and decisions; unknown when unavailable | What behavior or evidence would demonstrate success; proposed when not agreed |

Merge related responsibilities rather than mirroring every lens as a row. Keep hypotheses and proposed acceptance evidence visibly provisional. Avoid estimates, owners, protocols, or numerical targets absent from the source.

Use a flow diagram for relationships, a sequence diagram for cross-system interactions, or a state diagram when transitions are central. Diagrams are optional. Label node and edge provenance directly: `Known`, `Observed`, `Inferred`, `Assumption`, or `Proposal` for nodes and `known`, `observed`, `inferred`, `assumed`, or `proposed` for relationships. A known pair of systems does not make their connecting flow known. Dash proposed edges as an additional cue if useful, never as the only cue.

For a complex system, add only the detail needed to assess it: authoritative entities, boundary contracts, lifecycle transitions, and material failures. A compact failure description is `failure → detection → recovery/degradation`; unknown detection or recovery remains unknown. State proposals as proposals.

End with the decisions that block or materially reshape candidate work, explaining their consequences. Lower-impact detail can stay in a supporting section or be deferred explicitly. Preserve traceability and avoid repeating the same concern across the opening, diagram, table, and prose.
