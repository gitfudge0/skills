
# Optional HTML report renderer

A design system for standalone report decks. You already know how to code — this file conveys **intent, conventions, and the gotchas you can't infer from the CSS**. For exact component structure, read `assets/report.css`; for the deck runtime, read `assets/deck.js`. Don't re-derive what those files already define.

## When to use it

Use HTML when requested, or when a standalone visual deliverable helps the caller’s task. Follow explicit Markdown, document, and chat format requests. Length alone does not require HTML. This renderer controls presentation, not report content or authorization.

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

**Fonts and style.** Use system fallbacks by default for portable offline output. If remote fonts are deliberately chosen, load only the selected style’s families and verify fallback rendering. Reuse an established style; otherwise choose `editorial`. Offer the style gallery only when the user wants to choose. Do not add an approval round for styling.

## Output model

Use a deck for sequential presentation. Use a scrolling report for dense reference material where searching and comparing sections matters; omit deck navigation/runtime and supply explicit normal-flow layout overrides. The shipped runtime remains for deck output. A `.deck` holds a sequence of `.slide` sections; on screen one shows at a time (arrow keys / on-screen ‹ ›), and in PDF each becomes one landscape page.

Deck composition rules:
- **Slide 1 is the cover** (`.slide.slide-cover` — carries meta badges, `<h1>`, lead). **The last slide carries the footer.**
- **One major idea per slide.** Don't cram unrelated ideas together; don't stretch one thin point across many.
- **Add an agenda slide** when the deck exceeds ~4 content slides.
- **Prefer splitting over scrolling.** A too-tall slide auto-scrolls within itself, but if you see that, split it.
- Each content slide: an `<h2 class="slide-title">` and a body wrapped in a single `.slide-inner`.

## Files and location

Follow package-root `shared/artifacts.md`; the default category is `report-deck`. The nearest ancestor `.fudge-package.json` identifies the installed package root. In source, `scripts/skill-manifest.json` identifies the repository. Honor caller destinations and collision rules. Local resources remain relative to this guide. Copy CSS/runtime into the output bundle with correct relative links, or inline them for a single-file deliverable.

## Shell and composition

Read [deck shell and component examples](references/composition.md) for exact markup. Reuse `assets/report.css` and `assets/deck.js`; do not reinvent the runtime. The reference retains grid structure, exact class names, content budgets, mock grounding, and composition archetypes.

## Design language

- **Sentence case everywhere** — headings, labels, badges. Never title case.
- **Two font weights only:** 400 body, 600/700 headings/labels.
- **Follow the selected style.** Use its native effects, including glass gradients and brutalist shadows. Avoid extra decoration that weakens readability.
- **Separate with whitespace, not lines.** Borders are for *structure* — the box around a card/table/mock, the callout's left rule, the header/footer/slide-title rules. They are **not** for separating repeated items: rows in `item-list`, `kv-block`, `next-steps`, and stacked `finding`s rely on spacing (`gap`/padding), not per-row hairlines. A deck where every list row carries a divider reads as noisy and over-ruled — if you find yourself adding `border-bottom` to a repeating element, use a gap instead. (The shipped CSS already does this; don't reintroduce row borders.)
- **Never hardcode hex.** Use the `--color-*` variables (dark mode is togglable). Inventing names like `--purple`, `--coral`, or `--success` **fails silently** — the property is ignored and the color falls back. The real names are `--color-accent`, `--color-teal`, `--color-amber`, `--color-red` (each with a `-light` variant), plus `--color-text/-secondary/-tertiary`, `--color-bg`, `--color-surface`, `--color-border/-light`.
- **Color = two tiers, one rule.** A color marks either *brand* or *status*, never both:
  - **Brand — accent (`badge-accent`, coral-orange):** wayfinding/identity only (progress bar, section labels, step numbers, links, cover report-type badge). **No** good/bad valence.
  - **Status — the color IS the meaning:** `badge-success`/teal = positive·added·done · `badge-warning`/amber = caution·modified·in-progress · `badge-critical`/red = error·breaking·deleted · `badge-info`/neutral = informational·minor. Status colors never decorate; the brand accent never implies status.

## PDF export

Only when asked — the HTML is the primary deliverable.

Reuse the HTML’s established style unless the user requests a different PDF style. Invoke the bundled script by its resolved absolute path, for example `bash <renderer-directory>/scripts/html-to-pdf.sh <report.html> <report.pdf>`. Set `STYLE` only for an intentional override. Do not ask for a style again solely because output is frozen.

One landscape page per slide, always rendered in **light mode** (PDFs are light regardless of the on-screen theme). It drives a **headless Chromium-family browser** to execute Mermaid JS and honor `@media print`; choose a renderer that supports both.
- `STYLE=<style>` pins one of the 7 visual styles for the render (validated; invalid values error out).
- Set `CHROME_BIN=/path/to/chrome` to pick a browser; bump `RENDER_MS=6000` if diagrams come out blank.
- **Verify the page count equals the number of `.slide` sections.** Don't trust `file foo.pdf` or a `/Count` grep — both misreport for Chrome PDFs. Use a PDF parser for the page count, for example:
  ```bash
  python3 -c "from pypdf import PdfReader; print(len(PdfReader('foo.pdf').pages))"
  ```

## Verify before handoff

Use an available browser automation tool when practical: drive a `file://` load at viewport 1280×720, set `data-theme` to `light` then `dark`, step every slide with `ArrowRight`, screenshot each, and log any slide where `scrollHeight > clientHeight`. This catches overflow and theme-specific breakage that the naked eye misses. Then read the screenshots. Use the installed tool’s documented import/API contract. If rendering tools are unavailable, report the unverified visual checks.

Open the deck and check — these fail *silently*:
- **Navigation:** arrow keys and ‹ › advance slides, progress bar updates, prev/next disable at the ends (clamp, no wrap).
- **No orphaned scrolling:** every slide body is in `.slide-inner`; slide 1 is `.slide-cover`. Check `scrollHeight > clientHeight` per slide in **both themes** (dark text/badges can reflow differently); if a slide overflows by more than a hair, split it.
- **Component class names:** spot-check that `finding`/`item-row` markup matches the skeletons exactly — mashed title+desc or a gap above a numbered row means a wrong/missing class (see footgun).
- **CSS var typos:** grep for any `var(--…)` not in the list above — typos fall back silently.
- **Grid components** (`next-steps`, `item-list`): correct `<li>`/row child structure (see footgun).
- **Mermaid on later slides:** navigate to each diagram slide — inactive slides stay laid out (not `display:none`) so diagrams size correctly; a regression shows as a blank/collapsed diagram.
- **PDF (if exported):** page count == `.slide` count (see above), diagrams rendered.
