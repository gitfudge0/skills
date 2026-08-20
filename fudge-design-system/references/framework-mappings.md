# Phase 2 — Target-framework mapping

Tokens that only exist as CSS custom properties get retyped by hand into the app, badly. Every token therefore ships its **exact code equivalent in the same row** of `DESIGN.md`, and beside the swatch in `DESIGN.html`.

## Detection

| Signal in the project | Target |
|---|---|
| `pubspec.yaml` | Flutter |
| `package.json` with `react` / `next` | React (+ Tailwind if `tailwindcss` present) |
| `package.json` with `svelte` / `vue` / `@angular/core` | That framework |
| Static HTML/CSS only, no manifest | None needed — CSS custom properties *are* the mapping |

Multiple manifests or none of the above: ask the user **once**, in one message, then proceed. Do not run a detection round-trip per token group.

## Where the mapping lives

In the token tables and specimens, never a separate document. Two consumers, two drift profiles:

- **`DESIGN.html`** generates code strings from the same JS data arrays that render the swatches. Value and code are the same source — they cannot drift.
- **`DESIGN.md`** tables are hand-copied. State this in the doc: *the Markdown tables are a copy; `DESIGN.html` is generated from one source and wins on conflict.*

---

## Flutter profile

The fully worked profile. Other frameworks get the equivalent treatment (see stubs below).

### Colors

`Color(0xFFRRGGBB)` — ARGB, alpha first, so `#C13B63` → `Color(0xFFC13B63)`.

Semantic tokens have **no single Flutter value** — they resolve per `Brightness`. Express the semantic tier as two const classes, `AppColorsDark` and `AppColorsLight`, with identical member names, selected via `Theme.of(context).brightness`. Private const constructor, `static const Color` members, camelCase names matching the token (`color-surface-raised` → `surfaceRaised`).

### Typography

`TextStyle(fontFamily: …, fontSize: …, height: …, fontWeight: FontWeight.w…)`.

- `fontSize` in logical px: **1rem = 16 logical px**.
- Flutter's `height` is a multiplier of `fontSize`, so a unitless CSS line-height carries over unchanged.
- Weights map directly: 400 → `FontWeight.w400`, etc.
- Loading faces: `google_fonts` (`GoogleFonts.poppins()`) or bundled TTFs declared under `flutter: fonts:` in `pubspec.yaml`. Name both options.

### Radius

`BorderRadius.circular(n)`; `BorderRadius.zero` for none. For pills use **`StadiumBorder()`**, not `circular(999)` — the stadium stays a true pill at any height where a fixed large radius only approximates one. Say so in the row.

### Spacing, gaps, icon sizes, opacity, border widths

Plain `double` constants in const classes (`AppSpacing.space4 = 16`). Border widths become `BorderSide(width: 1.0)`. Icon sizes are doubles for `Icon(size:)` / `IconThemeData(size:)`. Opacity values are doubles for `Opacity(opacity:)` or `color.withValues(alpha:)`.

Flutter has **no `gap` property** on `Row`/`Column`. Insert space explicitly: `SizedBox(height: AppSpacing.gapMd)`, `Gap(...)` from the `gap` package, or `spacing:` on `Wrap`/`Flex` (Flutter 3.27+). Note this in the Gaps section.

### Shadows

One `List<BoxShadow>` per variant, per theme: `AppShadowsLight` / `AppShadowsDark`. `BoxShadow(color: Color.fromRGBO(r, g, b, a), offset: Offset(x, y), blurRadius: b)`. CSS spread has no direct equivalent — if a token uses spread, say what you dropped.

### Motion

- `Duration(milliseconds: n)`.
- Easings as **exact `Cubic(x1, y1, x2, y2)`**, never the nearest `Curves.*` constant. `Curves.easeOut` and friends are genuinely different curves and will drift from the web build. State this.
- Reduced motion: the Flutter equivalent of `prefers-reduced-motion` is `MediaQuery.disableAnimationsOf(context)`. When true, use `Duration.zero` **and** skip transform-based transitions.

### Z-index

**There is no Flutter equivalent.** Paint order comes from `Stack` child order (later children paint on top) and `Overlay` entry insertion order. Keep the z tokens as **ordering semantics only** — sort stack children or overlay insertions by them, never assign them to a widget property. The table's Flutter column says exactly that rather than inventing a value.

### Blur

`ImageFilter.blur(sigmaX: s, sigmaY: s)` inside `BackdropFilter`. A CSS `blur()` radius is roughly **2× the Gaussian sigma**, so **sigma = CSS px / 2**. State the conversion in the row and in Assumptions.

---

## Stubs for other targets

Same principle, less prose. Give the equivalent for every token group and flag every group with no equivalent, as z-index is flagged for Flutter.

**React / plain web:** CSS custom properties are already the runtime form — `var(--color-brand)`. Add a typed TS module whose leaves are `var()` *references*, not resolved literals, so theming still works at runtime.

**Tailwind:** a v4 `@theme` block mapping semantic names to the custom properties (and a v3 `theme.extend` fragment if the project is on v3). Map the **semantic** tier only — binding a utility to `--neutral-700` binds to a value instead of a meaning, and the next theme breaks it.

**shadcn/ui:** its fixed slot vocabulary (`--background`, `--foreground`, `--primary`, …) on the `.dark` convention, aliased onto your semantic tokens. Aliases project outward; they never become a second source. A project that hand-edits the alias layer has forked the system invisibly — say so once.
