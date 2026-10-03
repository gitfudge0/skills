# Deck shell and composition

Assets in example output use `assets/`; the guide resources below use `../assets/` relative to this reference. Copy assets to the output bundle or inline them for a single-file deliverable.

## Required shell

Every report needs: a `.deck` of `.slide` sections, the nav chrome, the theme toggle, and `deck.js`. Include the Mermaid `<script>` only if the deck has diagrams.

```html
<!DOCTYPE html>
<!-- data-style is the user's chosen visual style (see Visual styles); omit it for the default editorial look. -->
<html lang="en" data-style="[chosen-style]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Report title]</title>
  <link rel="stylesheet" href="assets/report.css">
  <!-- <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script> -->
</head>
<body>
<button class="theme-toggle" aria-label="Toggle dark mode"></button>
<div class="deck-progress"></div>

<div class="deck">

  <!-- REQUIRED: cover slide (slide 1) -->
  <section class="slide slide-cover">
    <div class="slide-inner">
      <div class="report-header-meta">
        <span class="badge badge-accent">[Report type]</span>
        <span class="badge badge-success">[Status]</span>
        <span class="report-header-date">[Date]</span>
      </div>
      <h1>[Title]</h1>
      <p class="lead">[One or two sentences on what this deck covers and why.]</p>
    </div>
  </section>

  <!-- CONTENT SLIDES — one per major idea. -->
  <section class="slide">
    <div class="slide-inner">
      <h2 class="slide-title">[Slide title]</h2>
      <!-- components, see below -->
    </div>
  </section>

  <!-- REQUIRED: closing slide carrying the footer -->
  <section class="slide">
    <div class="slide-inner">
      <h2 class="slide-title">[Closing / summary title]</h2>
      <footer class="report-footer">
        <span>[Report title — short form]</span>
        <span class="report-footer-brand">[Author or project]</span>
      </footer>
    </div>
  </section>

</div>

<!-- REQUIRED: deck navigation -->
<nav class="deck-nav" aria-label="Slide navigation">
  <button class="deck-prev" aria-label="Previous slide">‹</button>
  <button class="deck-next" aria-label="Next slide">›</button>
</nav>

<script src="assets/deck.js"></script>
</body>
</html>
```

`deck.js` wires it all: nav (arrows/swipe/buttons, clamps at the ends — no wrap), theme persistence (light/dark via the on-screen button), visual-style cycling (press **T** to step through the 7 styles, persisted), per-slide overflow auto-scroll, and Mermaid (re)init on load and theme switch. Don't reimplement it inline.

## Components

All classes are defined in `report.css` — read it for exact structure. Use these as building blocks **inside each slide's `.slide-inner`**; mix freely. Index:

| Class group | For | Note |
|---|---|---|
| `section` + `section-label` | a labelled sub-group under the slide title | |
| `metric-grid` > `metric-card` (`metric-label/value/sub`) | 2–6 key numbers | only when numbers are meaningful, not filler |
| `finding` (`finding-num/body/title-row` + badge) | numbered findings/issues | |
| `callout`, `callout-warning`, `callout-danger` | a note/warning | sparingly — 1–2 per deck |
| `kv-block` > `kv-row` (`kv-label/value`) | structured metadata/specs | |
| `data-table` inside `.data-table-wrap` | tabular data | wrap is required for horizontal scroll |
| `item-list` > `item-row` (icon + title/desc + badge) | risks, checklists, open questions | |
| `file-tree` (spans `.new/.mod/.del/.dir/.note`) | file structure with change annotations | |
| `mock-frame` (`mock-bar/dot/url/body`) + `mock-caption` | UI mockups | see mocks note below |
| `diagram-wrap` > `.mermaid` + `mock-caption` | flow/sequence/state/ER diagrams | needs the Mermaid `<script>` |
| `next-steps` (`section` + `<ol>`) | ordered actions/recommendations | see grid footgun below |
| `badge-*` | status/type chips | see colors below |

**Four real footguns (the reason this section exists):**
- **`next-steps` and `item-list` rows are CSS grids.** Wrap each `<li>`'s content in a single element (e.g. one `<span>`), or mixed inline content (`<strong>` + text + `<code>`) shatters into separate grid cells and wraps one word per line.
- **Exact class names matter — there is no fallback.** The CSS classes are precise; invented variants (`item-icon`, `item-body`, `item-title`, `item-desc`) match nothing, so the grid/flex layout never applies. Two telltale failures: a title and its description **run together with no break** (the styling that stacks them was never applied), and a numbered row shows a **large empty gap above it** (the flex wrapper that puts the number beside the body is missing). Copy these skeletons verbatim — don't paraphrase the class names:

  ```html
  <!-- finding: number BESIDE body requires the .finding-header flex wrapper -->
  <div class="finding">
    <div class="finding-header">
      <span class="finding-num">1</span>
      <div class="finding-body">
        <div class="finding-title-row"><span class="finding-title">Title</span><span class="badge badge-critical">Blocker</span></div>
        <p>Body text.</p>
      </div>
    </div>
  </div>

  <!-- item-row: middle column is ONE wrapper div holding the two classed lines (optional trailing badge) -->
  <div class="item-list">
    <div class="item-row">
      <span class="item-row-icon">1</span>
      <div>
        <div class="item-row-title">Title</div>
        <div class="item-row-desc">Description that sits under the title.</div>
      </div>
      <span class="badge badge-warning">Decide</span>
    </div>
  </div>
  ```

- **Budget content per slide — overflow is silent.** Rough ceiling at 1280×720: ~3–4 `finding` blocks, ~5–6 `item-row`s, or one `next-steps` of ~5 steps *plus* a `section` header. A slide carrying two `section`s each with their own `next-steps` (e.g. multiple phases) almost always overflows — split it. Don't trust the eye; screenshot at 1280×720 and check `scrollHeight > clientHeight` per slide (see Verify).
- **Ground mocks in existing UI.** Read the real components/pages first; include the surrounding chrome (nav, sidebars, real labels) so the feature appears in context, not floating. Build mocks with bare HTML + inline styles, and keep them inert. Only omit existing chrome for a brand-new standalone page.

## Composition archetypes

The components above are also assembled into **higher-level slide layouts** — the recurring shapes a deck needs (a chapter break, a single hero number, a comparison, a roadmap). Their classes live in the `COMPOSITION ARCHETYPES` block of `report.css` and, like every component, read only `--color-*`/`--font-*` tokens — so each one inherits all 7 visual styles and light/dark for free.

**`../assets/gallery.html` is the living catalogue** — every archetype below rendered as a real slide, with a style switcher and theme toggle. Open it (an available browser tool) to see them, and **read it for the exact markup of any archetype** rather than reconstructing from scratch. It pairs with `style-gallery.html` (which shows the 7 styles).

| Archetype | Class(es) | For |
|---|---|---|
| Section divider | `slide-divider` + `divider-num` | a chapter break in a long deck |
| KPI hero | `kpi-hero` + `kpi-figure` + `kpi-cap` | one giant number when a single figure is the story |
| Big takeaway / quote | `quote` + `quote-attr` | one chrome-less statement to leave the reader with |
| Stat band | `stat-band` > `stat` / `stat-divider` (`stat-figure`/`stat-label`) | a row of oversized figures split by hairlines |
| Two-column / split hero | `split` (+ `split-wide`), `panel` for the visual side | comparisons, before/after, claim + figure |
| Process steps | `process` > `process-step` (`process-disc`) + `process-arrow` | a left-to-right numbered pipeline |
| 2×2 quadrant | `quadrant` > `quadrant-cell`(`.is-priority`) + `axis-x`/`axis-y` | a priority / positioning matrix |
| Bar chart | `bar-chart` > `bar-row` (`bar-name`/`bar-track`/`bar-fill`/`bar-value`) | pure-CSS horizontal bars, no library |
| Comparison matrix | `data-table` with centered ✓/✗ cells | capability grid across options |
| Persona card | `persona` (`persona-avatar`/`persona-name`/`persona-role`) | research personas, stakeholder intros |
| Annotated mock | `pin` + `pin-over` (over a `mock-frame`) + `pin-list` | numbered callouts keyed to a legend |
| Q&A / FAQ | `qa` > `qa-q`/`qa-a` + `qa-marker` | questions, objections, open issues |
| Kanban board | `kanban` > `kanban-col-head`/`kanban-col-body`/`kanban-card` | to-do / doing / done snapshot |
| Code block | `code-block` (+ `code-comment`/`code-string`) | fenced multi-line code (prefer over inline) |
| Timeline / roadmap | `timeline` > `timeline-item` (`timeline-dot`, `.is-pending`) | phased work on a vertical rail |

Same rules as the base components apply: **copy the markup verbatim from `gallery.html`** (invented class names match nothing and fall back silently), keep one major idea per slide, and **budget content — overflow is still silent.** A few skeletons for the less obvious ones:

```html
<!-- KPI hero: one number, centered -->
<div class="kpi-hero">
  <div class="kpi-figure">−38%</div>
  <div class="kpi-cap">p95 latency after the cutover</div>
</div>

<!-- Bar chart: set each fill width inline; the outlier gets a status colour -->
<div class="bar-chart">
  <div class="bar-row"><div class="bar-name">Export API</div><div class="bar-track"><div class="bar-fill is-critical" style="width:82%"></div></div><div class="bar-value">1.40%</div></div>
  <div class="bar-row"><div class="bar-name">Webhooks</div><div class="bar-track"><div class="bar-fill" style="width:6%"></div></div><div class="bar-value">0.02%</div></div>
</div>

<!-- Timeline: one dot per item; mark not-yet-done dots .is-pending -->
<div class="timeline">
  <div class="timeline-item"><span class="timeline-dot"></span>
    <div class="timeline-title">Week 1 · Shadow write</div>
    <div class="timeline-desc">Behind a flag; compare against the legacy path.</div></div>
  <div class="timeline-item"><span class="timeline-dot is-pending"></span>
    <div class="timeline-title">Week 3 · Cut over</div>
    <div class="timeline-desc">Retire the old path once parity holds.</div></div>
</div>
```
