# HTML Report Skill

A design system for standalone report decks. You already know how to code — this file conveys **intent, conventions, and the gotchas you can't infer from the CSS**. For exact component structure, read `assets/report.css`; for the deck runtime, read `assets/deck.js`. Don't re-derive what those files already define.

## When to use it

Generate an HTML report instead of markdown whenever the output is a **standalone deliverable** the user will read, share, or revisit — findings, audits, code reviews, plans, architecture decisions, research handoffs, or anything a page or longer that benefits from visual hierarchy. When in doubt: if you'd reach for a markdown file, reach for HTML instead.

This skill defines the **visual language**, not what sections a report contains. A proposal, a test plan, a critique, and an ADR all differ — compose whatever structure fits. The only fixed part is the shell.

## Visual styles

The shipped `report.css` carries **7 selectable visual styles** layered over the same component library. The deck author opts in by setting `data-style` on `<html>` (e.g. `<html data-style="terminal" data-theme="light">`); with no `data-style` the default editorial look applies. Every style works in both light and dark — the toggle is unchanged.

| `data-style` | One-liner |
|---|---|
| `marginalia` | Ink on warm paper, one grotesk, a single marker accent as hand-drawn marks. |
| `verdant` | Friendly product deck — green accent, soft rounded cards on a tinted ground. |
| `blueprint` | Technical schematic — graph-paper grid, engineering blue, mono labels, dimension lines. |
| `editorial` | Magazine — large italic display serif, hot magenta accent, drop cap (default look). |
| `terminal` | Monospace console — window-chrome bar, `$`/`>` prompt, `[status]` badges, phosphor green. |
| `brutalist` | Thick black borders, hard zero-blur offset shadows, clashing blue + highlighter yellow. |
| `glass` | Aurora Glass — frosted translucent cards over a violet-to-cyan gradient mesh. |

**Fonts.** Add the Google-fonts `<link>` to `<head>` covering all faces these styles use — **Inter, Space Grotesk, Plus Jakarta Sans, Instrument Serif, Space Mono, Sora** (the system fallbacks in the CSS keep an unstyled load readable, but link them for fidelity):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Sora:wght@400;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

**Choosing a style — do this BEFORE writing the report file:**
1. Point the user at the demo gallery so they can see all 7 in both light and dark — suggest they run `open <abs path to skill>/assets/style-gallery.html` (or open the copy you place in `.reports/assets/`).
2. Use the **AskUserQuestion** tool to ask which of the 7 styles they want (options: marginalia, verdant, blueprint, editorial, terminal, brutalist, glass).
3. Generate the report with `data-style="<choice>"` on `<html>`.

If the user declines or doesn't care, **default to `editorial`** (the no-`data-style` look) and proceed — never block on the question.

## Output model: a slide deck

Reports render as a **slideshow, not a scrolling page**. A `.deck` holds a sequence of `.slide` sections; on screen one shows at a time (arrow keys / on-screen ‹ ›), and in PDF each becomes one landscape page.

Composition rules:
- **Slide 1 is the cover** (`.slide.slide-cover` — carries meta badges, `<h1>`, lead). **The last slide carries the footer.**
- **One major idea per slide.** Don't cram unrelated ideas together; don't stretch one thin point across many.
- **Add an agenda slide** when the deck exceeds ~4 content slides.
- **Prefer splitting over scrolling.** A too-tall slide auto-scrolls within itself, but if you see that, split it.
- Each content slide: an `<h2 class="slide-title">` and a body wrapped in a single `.slide-inner`.

## Files & location

Write to `.reports/<descriptive-kebab-name>.html` at the project root (create the dir; add `.reports/` to `.gitignore` if the project has one). Copy **both** `assets/report.css` and `assets/deck.js` into `.reports/assets/` and link them (the multi-style `report.css` carries all 7 styles — no extra files). Copying `assets/style-gallery.html` alongside them is handy for the style-picker step above:

```html
<link rel="stylesheet" href="assets/report.css">
<script src="assets/deck.js"></script>   <!-- at end of <body> -->
```

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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Sora:wght@400;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
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
        <span class="report-footer-brand">Generated by Claude Code</span>
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

**`assets/gallery.html` is the living catalogue** — every archetype below rendered as a real slide, with a style switcher and theme toggle. Open it (`open <abs path to skill>/assets/gallery.html`) to see them, and **read it for the exact markup of any archetype** rather than reconstructing from scratch. It pairs with `style-gallery.html` (which shows the 7 styles).

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

## Design language

- **Sentence case everywhere** — headings, labels, badges. Never title case.
- **Two font weights only:** 400 body, 600/700 headings/labels.
- **No gradients, shadows, or decorative effects.** Flat surfaces, whitespace, thin borders.
- **Separate with whitespace, not lines.** Borders are for *structure* — the box around a card/table/mock, the callout's left rule, the header/footer/slide-title rules. They are **not** for separating repeated items: rows in `item-list`, `kv-block`, `next-steps`, and stacked `finding`s rely on spacing (`gap`/padding), not per-row hairlines. A deck where every list row carries a divider reads as noisy and over-ruled — if you find yourself adding `border-bottom` to a repeating element, use a gap instead. (The shipped CSS already does this; don't reintroduce row borders.)
- **Never hardcode hex.** Use the `--color-*` variables (dark mode is togglable). Inventing names like `--purple`, `--coral`, or `--success` **fails silently** — the property is ignored and the color falls back. The real names are `--color-accent`, `--color-teal`, `--color-amber`, `--color-red` (each with a `-light` variant), plus `--color-text/-secondary/-tertiary`, `--color-bg`, `--color-surface`, `--color-border/-light`.
- **Color = two tiers, one rule.** A color marks either *brand* or *status*, never both:
  - **Brand — accent (`badge-accent`, coral-orange):** wayfinding/identity only (progress bar, section labels, step numbers, links, cover report-type badge). **No** good/bad valence.
  - **Status — the color IS the meaning:** `badge-success`/teal = positive·added·done · `badge-warning`/amber = caution·modified·in-progress · `badge-critical`/red = error·breaking·deleted · `badge-info`/neutral = informational·minor. Status colors never decorate; the brand accent never implies status.

## PDF export

Only when asked — the HTML is the primary deliverable.

**Before exporting, ask which style to render the PDF in.** The reader can flip styles live with **T**, but a PDF is frozen — use the **AskUserQuestion** tool to ask which of the 7 styles to bake in (options: marginalia, verdant, blueprint, editorial, terminal, brutalist, glass). Pass the answer via the `STYLE` env var. If the user has no preference, omit `STYLE` and the PDF keeps whatever `data-style` the HTML already carries.

```bash
STYLE=blueprint scripts/html-to-pdf.sh .reports/your-report.html   # → .reports/your-report.pdf
scripts/html-to-pdf.sh .reports/your-report.html                   # keep the HTML's own style
```

One landscape page per slide, always rendered in **light mode** (PDFs are light regardless of the on-screen theme). It drives a **headless Chromium-family browser** — the only reliable way to execute Mermaid JS and honour `@media print`; a plain HTML→PDF library drops both.
- `STYLE=<style>` pins one of the 7 visual styles for the render (validated; invalid values error out).
- Set `CHROME_BIN=/path/to/chrome` to pick a browser; bump `RENDER_MS=6000` if diagrams come out blank.
- **Verify the page count equals the number of `.slide` sections.** Don't trust `file foo.pdf` or a `/Count` grep — both misreport for Chrome PDFs. Count real page objects:
  ```bash
  python3 -c "import re;d=open('foo.pdf','rb').read();print(len(re.findall(rb'/Type\s*/Page[^s]',d)))"
  ```

## Verify before handoff

Strongly prefer an automated pass with Playwright (the Chromium browser ships under `~/Library/Caches/ms-playwright` or `~/.cache/ms-playwright`) over eyeballing: drive a `file://` load at viewport 1280×720, set `data-theme` to `light` then `dark`, step every slide with `ArrowRight`, screenshot each, and log any slide where `scrollHeight > clientHeight`. This catches overflow and theme-specific breakage that the naked eye misses. Then read the screenshots. Note: `playwright` is a CommonJS module — `import pkg from '.../playwright/index.js'; const { chromium } = pkg;`, not a named import.

Open the deck and check — these fail *silently*:
- **Navigation:** arrow keys and ‹ › advance slides, progress bar updates, prev/next disable at the ends (clamp, no wrap).
- **No orphaned scrolling:** every slide body is in `.slide-inner`; slide 1 is `.slide-cover`. Check `scrollHeight > clientHeight` per slide in **both themes** (dark text/badges can reflow differently); if a slide overflows by more than a hair, split it.
- **Component class names:** spot-check that `finding`/`item-row` markup matches the skeletons exactly — mashed title+desc or a gap above a numbered row means a wrong/missing class (see footgun).
- **CSS var typos:** grep for any `var(--…)` not in the list above — typos fall back silently.
- **Grid components** (`next-steps`, `item-list`): correct `<li>`/row child structure (see footgun).
- **Mermaid on later slides:** navigate to each diagram slide — inactive slides stay laid out (not `display:none`) so diagrams size correctly; a regression shows as a blank/collapsed diagram.
- **PDF (if exported):** page count == `.slide` count (see above), diagrams rendered.
