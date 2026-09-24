# Component inventory

Use this route for a requested component, component set, or full system. Existing code, screens, and wireframes can all supply evidence. Inventory the surfaces relevant to the request; inspect every relevant frame for a full product inventory, but do not require a wireframe for a small component contract.

## Decide what belongs

A component represents a reusable control, content pattern, or surface with a stable job and anatomy. A one-screen arrangement usually belongs to the screen design. Group full-system components by the jobs they serve, such as actions, navigation, input, feedback, and domain-specific content. Do not aim for a predetermined component count.

Record source references where they exist: frame IDs, screen names, code paths, or design nodes. If the request introduces a new component, mark its structure and behavior as proposed rather than extracted.

## Contract and specimens

For each component in scope, state its purpose, anatomy, relevant variants and sizes, behavior across meaningful states, tokens or shared rules consumed, and source references. Include a target-framework mapping when the handoff is for a known stack. Do not enumerate hover for a touch-only surface or error for a passive decorative element; do specify focus, disabled, loading, validation, and data states when that component can reach them. Distinguish an empty collection from no search results where both can occur.

A written contract, a visual specimen, or both may be appropriate. Use realistic product copy in specimens so length and density can be judged. For a full library, provide enough examples to inspect each reusable pattern and the states most likely to change its layout or meaning; a matrix of every variant multiplied by every state is unnecessary unless the task calls for exhaustive coverage.

## Token consistency

Components use the declared authoritative token or rule source. If a shared value is missing, add it there before applying it in multiple components. A one-off value may stay local when it truly belongs only to that component; document why if the distinction matters to handoff. Do not duplicate a complete token block in every file unless a self-contained artifact needs it.

For a token-only HTML specimen, verify CSS declarations outside the declared token-definition area do not introduce raw colors. Check the actual style declarations and any inline styles; a plain grep across the entire HTML file will also find legitimate token definitions, swatch labels, and documentation examples and cannot establish a leak. Compare any copied token definitions with their authoritative source. Apply the same principle to sizes and durations where they are part of the shared token contract.
