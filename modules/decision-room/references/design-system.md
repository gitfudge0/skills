# Default visual identity

Established from a user-provided reference (a Korean research infographic: cream background, navy tree/org-chart structure, right-side annotation panels). Use this by default for every war-room HTML artifact. Only deviate if the user explicitly asks for a different look for that run — don't regenerate a fresh identity from scratch each time the way a one-off design brief normally would.

## Tokens

```css
--cream: #F3EEE1;   /* page background */
--card:  #FBF8EF;   /* card/panel background, slightly lighter than page */
--navy:  #2E2A6E;   /* primary accent — fills, borders, headers */
--navy-dark: #211D4E;
--text:  #26234F;
--text-dim: #78749C;
--line:  #D8D2E8;   /* hairlines, dashed dividers */
--for: #2E2A6E;          /* stance color: advocate */
--conditional: #A9791B;  /* stance color: conditional */
--skeptical: #A3402F;    /* stance color: skeptic */
```

Fonts: 'Space Grotesk' (700) for headers/labels/nodes, 'Inter' for body text. Both via Google Fonts.

## Structural pattern

1. **Header row** — navy filled title box (topic name) on the left; a plain metadata list (Scope / Domain / Perspectives) on the right, bold navy labels over plain values.
2. **Process band** — a small elbow-connector tree: a "THE PROCESS" root node with a stem down to a horizontal bar, fanning out to 3 phase boxes (first outlined, rest filled navy). A short descriptive paragraph sits beside it, not below it.
3. **Recommendation panel** — a heavier-bordered standalone card, always positioned before the persona detail so it's the first substantive thing read. Four-column sub-grid: Why / Risks to Watch / Conditions / Out of Scope.
4. **Persona rows** — one per persona, each a horizontal "chain": navy name+role node → connecting line → outlined priority node → connecting line → a pill badge (for/conditional/skeptical, color per token above). Beside the chain, an annotation block with "Take" and "Flags" as small caps headers over plain sentences. Rows are separated by a dashed hairline, not boxed individually.
5. **Legend panel** — a small cream card with a circled-"i" icon explaining the stance pill meanings, placed once, roughly mid-list rather than at the very top or bottom.
6. **Footer** — small caps, split between a line identifying the exercise and a line listing the cast by name.

## Notes

- Connectors are CSS (border/pseudo-element based elbow lines), not SVG — keep it that way for simplicity unless a run has a persona count or structure that breaks the layout, in which case adjust proportions rather than the visual language itself.
- Stance pill colors are the only place hue varies by content; everything else stays cream/navy regardless of topic.
- Mobile: chains and the process band stack vertically below ~700px; the recommendation grid drops to 2 columns.
