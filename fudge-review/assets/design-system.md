# Indigo editorial design system

Reference spec for the HTML renderer in the `fudge:review` skill. Authoritative — the bundled `example-review.html` is a working implementation of exactly this spec, safe to copy and edit directly.

## Colour tokens

All values below are CSS custom properties. Every one must be defined in three places: `:root` (light default), `@media (prefers-color-scheme: dark)` scoped to `:root:not([data-theme])`, and duplicated as explicit `html[data-theme="dark"]` / `html[data-theme="light"]` blocks for the manual toggle to override system preference.

| Token | Role | Light | Dark |
|---|---|---|---|
| `--indigo` | Primary brand/accent — headline, numbers, borders | `#2D2DD6` | `#6a6af0` |
| `--indigo-d` | Darker indigo, reserved for future use / deep accents | `#1C1C8F` | `#4a4ad0` |
| `--indigo-l` | Light indigo — pill borders, toggle border | `#8A8AEA` | `#9a9af8` |
| `--canvas` | Outer background reference (page body uses `--indigo` directly instead) | `#E9ECF4` | `#05060a` |
| `--panel` | The near-white page panel background | `#FBFCFE` | `#0f121b` |
| `--panel-2` | Recessed surface — code chips | `#F3F5FA` | `#161a26` |
| `--ink` | Primary text | `#232848` | `#e6e8f0` |
| `--ink-2` | Secondary text — finding body copy | `#5D6484` | `#9199a6` |
| `--ink-3` | Tertiary text — labels, meta, eyebrow | `#9AA0B8` | `#7b81a6` |
| `--ghost` | Muted borders — nit/area pills, dotted icon stroke | `#C3C8DA` | `#3a4258` |
| `--line` | Section dividers (`.erow` top border) | `#D8DCE9` | `#2a3040` |
| `--hair` | Hairline, lighter than `--line` | `#E5E8F1` | `#1c2130` |
| `--red` | Blocker | `#E0402A` | `#f0665a` |
| `--red-t` | Blocker tint background | `#FCF0EE` | `#2a1a1c` |
| `--amber` | Should-fix | `#8a6d1f` | `#e0ab4a` |
| `--amber-t` | Should-fix tint (used sparingly; pills don't tint amber by default) | `#FBF3DE` | `#2e2717` |
| `--teal` | Fixed / clean | `#1a7a5c` | `#3fbf94` |
| `--teal-t` | Fixed/clean tint background | `#EDF6F2` | `#12241d` |

## Type scale

| Element | Size / weight |
|---|---|
| Eyebrow | 11px, letter-spacing `.24em`, uppercase, weight 700 |
| Headline (the verdict sentence) | `clamp(26px, 4vw, 42px)`, weight 600, line-height 1.28 |
| Meta line (branch · commit · PR · date · CI) | 11.5px |
| Stat number | 30px, weight 600 |
| Stat label | 10px, letter-spacing `.12em`, uppercase, weight 600 |
| Section label (`.erow-label .lbl`) | 15.5px, weight 700 |
| Section meta/description | 11px |
| Item title (layer 2 one-liner) | 14.5px, weight 600 |
| `subk` (field key) | 9px, letter-spacing `.14em`, uppercase, weight 700 |
| `subv` (field value) | 12.5px |
| Pill | 10.5px, weight 600 |
| Divider pill | 12.5px, letter-spacing `.16em`, uppercase, weight 700 |

Body font stack: `"Helvetica Neue", Inter, ui-sans-serif, -apple-system, "Segoe UI", Arial, sans-serif`. Base body text 14px/1.6. Monospace (code chips, meta commit hashes): `ui-monospace, "SF Mono", Menlo, monospace`.

## Component inventory

**Header.** Centered column, max-width 780px for the headline. Eyebrow names the review (repo/PR shorthand) above the headline. The headline itself IS the verdict sentence — merge recommendation in prose, not a separate badge. Meta line below carries branch, commit(s) vs base, a linked PR reference, the date, and CI status, joined with ` · `. On a re-review the eyebrow adds the round.

**Stats row.** A centered flex row, `gap: 56px`, wrapping on narrow viewports. Each stat is an icon + number + label stack: a 34×34 SVG circle whose stroke style encodes the category (solid stroke = blockers, `stroke-dasharray="4.5 4.5"` = should-fix, `stroke-dasharray="2 4"` = nits, solid stroke + checkmark path = fixed since the last round), a 30px indigo count, and a 10px uppercase label underneath. The counts are open findings, so they match the verdict line. Drop the fixed stat on a first-round review.

**`.erow`.** The section primitive. `display:flex; gap:44px` with a 1px `--line` top border, splitting into a 27%-width label column (bold indigo section title + small muted description of what the section means) and a 73%-width content column holding the findings. Sections map to finding groups (e.g. "Fixed since round 1", "Open", "For the team", "Method"). The team section holds a `ul.clean` of one-line team decisions, not `.item` findings. On narrow viewports the split collapses to a stacked column.

**`.item`.** One finding, carrying `id="R<n>"`, `data-sev`, and `data-status` for the filter. A 26px outlined circle (indigo border) shows the finding ID (`R1`, `R2`, …) left of the body. The body starts with the bold title, the symptom written trigger → result, then the detail fields as `subk`/`subv` pairs in fixed order: cause → impact (only when present) → fix → rule (conventions findings only) → where. `where` is always last. Inline `code` gets a monospace chip: `background: var(--panel-2)`, small radius, tight padding. A `.pillrow` below the fields carries severity, status, and area pills. `suspected` and `pre-existing` appear as muted pills only when they apply.

**Pills.** Outlined, `border-radius: 999px`, 10.5px text, `padding: 3px 12px`. Default (untinted) border/text color is `--indigo-l`/`--indigo` for neutral pills. Severity variants: `.red` (blocker) borders/text `--red` AND fills `--red-t` — one of only two tinted states. `.amber` (should-fix) borders/text `--amber`, no tint. `.teal` (fixed/clean) borders/text `--teal` AND fills `--teal-t` — the other tinted state. `.muted` (nit, or an area/category pill) borders `--ghost`, text `--ink-3`, no tint. Only red and teal ever get a filled background — this is deliberate, it makes the two "resolved" states (bad-and-active vs good) visually load-bearing while everything else stays quiet.

**Filter row.** `.filters`, centered under the stats row. One `button.pill` per severity and per status, each with `data-key` (`sev` or `status`), `data-val`, and `aria-pressed`. Pressed buttons keep the default indigo pill; unpressed ones fall back to the muted look. A finding shows when both its severity and its status are pressed, and a section hides when none of its findings show. Hidden in print.

**`.divider-pill`.** A centered pill with a heavier 2px indigo outline (vs. the 1.3px used on ordinary pills), uppercase, letter-spaced text, no fill. Used once, between the findings and the Method block, to mark the switch from findings to how the review was done.

**Method block.** The last `.erow`, with no top border. Its content is a `details.method` whose `summary` is one line (CI status and file counts) and whose body is a `ul.clean` taken from `method.md`: CI, files read fully / skimmed / not read, prior-comment statuses, and what wasn't checked. Collapsed by default.

## Theming and print

Three-block CSS variable pattern, always:
1. `:root { ... }` — light values, the default with no JS at all.
2. `@media (prefers-color-scheme: dark) { :root:not([data-theme]) { ... } }` — dark values, but **only** when the page has not been manually overridden. The `:not([data-theme])` scoping is what prevents this block from fighting the explicit override blocks below.
3. `html[data-theme="dark"] { ... }` and `html[data-theme="light"] { ... }` — explicit values applied the instant JS sets `data-theme` on `<html>`, regardless of system preference.

A tiny inline `<script>` in `<head>` runs before paint: read a fixed localStorage key (pick one string and keep it stable, e.g. `"rfd-theme"`), and if it's `"light"` or `"dark"`, set `data-theme` on `<html>` immediately — this avoids a flash of the wrong theme on reload.

A fixed top-right pill button (`position: fixed; top:20px; right:20px`) toggles theme on click: read the current effective theme (the `data-theme` attribute if set, else fall back to `matchMedia("(prefers-color-scheme: dark)")`), flip it, write the new value to both the `data-theme` attribute and localStorage, and update the button's own label/icon to reflect the *next* click's destination (e.g. show "☀ light" while dark is active).

`@media print` forces every theme block (`html`, `html[data-theme="dark"]`, `html[data-theme="light"]`) back to the light palette, sets the body background to plain white, removes the indigo framing padding, hides the theme toggle, and adds `break-inside: avoid` on `.item` (and `break-inside: avoid-page` on `.erow`) so a finding or section never splits across a page boundary.

## Common mistakes

- Putting `where` anywhere but last. It is always the final field. Leading with a file path makes a review read as code-driven.
- Titles that name the cause or a code identifier. The title is the symptom, trigger → result; the cause goes in its own field.
- Printing an empty `impact` field. Leave the pair out when the finding has no impact line.
- Using emoji (🔴🟠⚪) in the HTML renderer. HTML can style text, so severity is a pill here, not an emoji — emoji are for Slack/GitHub only.
- Forgetting the `:not([data-theme])` scoping on the dark-mode media query. Without it, the system-preference block and the explicit `data-theme` override block have equal specificity and fight each other, so manual toggling stops working reliably.
- Adding real client, tenant, employee, or project identifiers to example/template content. Any HTML built from this system that is meant as a reusable example must use invented names throughout — title, branch, PR link, commit hashes, file paths, code identifiers.
- Forgetting `break-inside: avoid` (and `avoid-page` on the row) — without it, printing or PDF-exporting a long review can split a single finding across two pages.
- Skipping the localStorage-persisted toggle, or implementing it so it only flips a CSS class without also updating the stored preference — the theme should survive a reload.
- Tinting pills that aren't red or teal. Should-fix (amber) and nit/area (muted) pills are outlined only; tinting everything defeats the point of using fill to mark the two states ("actively bad" and "resolved/clean") that most deserve the eye's attention.
