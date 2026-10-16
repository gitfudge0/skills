# Shared decision-brief UI

Use package-root `shared/report-deck/guide.md` for the canonical plan runtime, packing and visual verification. Adapt `../assets/example.src.html`; its packed `../assets/example.html` is an offline preview. Source links resolve to `../../../plan/runtime/`; installed packages bundle `shared/report-deck/runtime/`. Pack with the applicable runtime's `pack.mjs`, which resolves canonical assets by filename in installed packages.

Use the runtime's header, metadata, `doc-plan`, stable-ID `doc-claim` tree, `doc-note`, `dl.kv` and explicitly labeled pills. Its theme toggle, comments, Copy response and print behavior provide the surrounding UI. Add no report skin, remote font, duplicate stylesheet or theme script.

The first substantive claim states the recommendation and rationale. Follow with risks, conditions/open questions and out-of-scope boundaries; then show each simulated perspective's role, priority, stance, take, flagged risk and grounding. Keep evidence and assumptions attached to arguments. Label generated perspectives as simulated, separate them from actual testimony, and never treat agreement as corroboration. Preserve uncertainty and missing evidence.

Report comments and copied responses are feedback, not build or execution approval. Do not introduce `doc-ask` controls or an approval gate merely because the output is HTML. Keep real unresolved choices in the conditions content and honor the caller's authorization contract. Plan-specific packing advice about prose or exhibit structure is advisory for reports; never invent evidence to satisfy it.
