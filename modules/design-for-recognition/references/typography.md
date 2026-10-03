# Typography decisions

Read this when the task needs a type direction, a correction to text hierarchy, or responsive type guidance. Start with the actual copy and the role of each text element: what should be seen first, what people scan to choose, what they must read closely, and what supports the task. Make those roles distinguishable without weakening small or essential text. Type hierarchy can come from size, weight, color, placement, and whitespace; a large heading may need little extra weight, while a scan target can benefit from stronger weight than nearby body text.

## Choose faces by role

Serif and sans serif faces can both serve interface text when the particular face reads well in context. Display and handwritten faces usually work best in short, larger treatments where their details remain legible. One family with suitable weights and styles can cover a whole product. When pairing families, give each a clear role and check that they work together in real headings, labels, paragraphs, and numbers. Brand voice and script coverage matter more than a fixed font count or a generic claim that one category is more readable.

Compare more than nominal font size. The baseline, x-height, and cap height explain why two faces at the same CSS size can sit or look different. Use them when aligning text with icons, mixing fonts, or comparing apparent size; then inspect the optical result. Weight and color both change perceived emphasis. Avoid making the smallest text simultaneously the thinnest and faintest. Judge contrast on the actual background and theme rather than choosing an opacity percentage in isolation.

## Size, spacing, and screens

A small set of reusable type roles makes related screens coherent. A modular scale can supply candidate sizes: for example, a ratio around 1.27 gives larger jumps for display work, while a smaller ratio can suit dense dashboards or narrow screens. The golden ratio has no special authority here. Adjust candidates to the font, content, layout, and project system instead of deriving every heading mechanically.

Set line height and letter spacing for the face, size, and line measure. Long lines and small paragraph text often need more leading; large headings usually need less. Tight tracking can help some large headings, but can harm smaller text or fonts with different proportions. Test paragraphs, short labels, multi-line headings, numbers, and translated or long strings rather than tuning only a sample headline.

Choose mobile and wide-screen sizes from the layouts the product actually serves. Bounded fluid sizing can interpolate between them; breakpoints remain useful where hierarchy, available space, or layout changes. Inspect the rendered text at narrow, intermediate, and wide widths, including relevant themes and realistic content. The type decision is ready when the reading order and readability hold in those conditions.
