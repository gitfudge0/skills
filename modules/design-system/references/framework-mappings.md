# Target-framework mapping

Map values when the user wants implementation guidance or the design deliverable is meant to hand values to a known app stack. Use the project's existing theme mechanism where it exists. Map the tokens needed by the requested scope; do not generate a code equivalent for unrelated groups just to fill a table.

## Detection

| Signal in the project | Target |
|---|---|
| `pubspec.yaml` | Flutter |
| `package.json` with `react` / `next` | React (+ Tailwind if `tailwindcss` present) |
| `package.json` with `svelte` / `vue` / `@angular/core` | That framework |
| Static HTML/CSS only, no manifest | None needed — CSS custom properties *are* the mapping |

If the consuming stack is unclear and the user only asked for design direction, omit the mapping. If code-level handoff is required, inspect the project and ask once only when the target cannot be inferred.

## Where the mapping lives

Put mappings beside the corresponding values or reference the authoritative token file. Do not create a separate mapping document unless the requested handoff needs one. If multiple files show the values, name the authority and check any copied code examples against it. Generating swatches and code strings from the same data is a useful approach when building an HTML specimen, not a requirement for every deliverable.

---

## Flutter profile

Use the applicable parts of this profile for selected token groups.

### Colors

`Color(0xFFRRGGBB)` — ARGB, alpha first, so `#C13B63` → `Color(0xFFC13B63)`.

When both themes exist, semantic tokens resolve per `Brightness`. Keep identical semantic names in each theme and select through the app's theme mechanism, such as `Theme.of(context).brightness`. Do not introduce two classes for a single-theme scope.

### Typography

`TextStyle(fontFamily: …, fontSize: …, height: …, fontWeight: FontWeight.w…)`.

- Resolve CSS `rem` against the source root font size before mapping to Flutter logical pixels. Use 16 only when the source establishes that root size; record any cross-platform scaling assumption.
- Flutter's `height` is a multiplier of `fontSize`, so a unitless CSS line-height carries over unchanged.
- Weights map directly: 400 → `FontWeight.w400`, etc.
- Load the selected face through the project's existing font strategy. For a new Flutter app, `google_fonts` or bundled TTFs in `pubspec.yaml` are options.

### Radius

`BorderRadius.circular(n)`; `BorderRadius.zero` for none. For pills use **`StadiumBorder()`**, not `circular(999)` — the stadium stays a true pill at any height where a fixed large radius only approximates one. Say so in the row.

### Spacing, gaps, icon sizes, opacity, border widths

Plain `double` constants in const classes (`AppSpacing.space4 = 16`). Border widths become `BorderSide(width: 1.0)`. Icon sizes are doubles for `Icon(size:)` / `IconThemeData(size:)`. Opacity values are doubles for `Opacity(opacity:)` or `color.withValues(alpha:)`.

Flutter has **no `gap` property** on `Row`/`Column`. Insert space explicitly: `SizedBox(height: AppSpacing.gapMd)`, `Gap(...)` from the `gap` package, or `spacing:` on `Wrap`/`Flex` (Flutter 3.27+). Note this in the Gaps section.

### Shadows

Map each shadow variant and theme that exists, for example with `List<BoxShadow>`. `BoxShadow(color: Color.fromRGBO(r, g, b, a), offset: Offset(x, y), blurRadius: b)`. Map CSS spread to [`spreadRadius`](https://api.flutter.dev/flutter/painting/BoxShadow/BoxShadow.html). Inspect the rendered shadow because blur rendering can still differ across platforms.

### Motion

- `Duration(milliseconds: n)`.
- When matching a specified cubic-bezier curve, use `Cubic(x1, y1, x2, y2)` rather than an approximate named curve.
- Reduced motion: the Flutter equivalent of `prefers-reduced-motion` is `MediaQuery.disableAnimationsOf(context)`. When true, use `Duration.zero` **and** skip transform-based transitions.

### Z-index

**There is no Flutter z-index property.** Paint order comes from `Stack` child order (later children paint on top) and `Overlay` entry insertion order. Map layer semantics to that ordering rather than inventing a widget value.

### Blur

`ImageFilter.blur(sigmaX: s, sigmaY: s)` inside `BackdropFilter`. The [CSS `blur()` parameter](https://www.w3.org/TR/filter-effects-1/#funcdef-filter-blur) already specifies Gaussian standard deviation, so use the resolved CSS length as sigma under the stated CSS-pixel/logical-pixel mapping. Keep this separate from box-shadow blur-radius conversion, and inspect the rendered result.

---

## Stubs for other targets

Use the same principle for token groups in scope, and flag any group with no direct equivalent.

**React / plain web:** CSS custom properties are already the runtime form — `var(--color-brand)`. Add a typed TS module only if the app uses one; keep references to runtime variables if theming is dynamic.

**Tailwind:** map semantic names to the custom properties through the project's Tailwind version and conventions. Binding a utility directly to `--neutral-700` makes it harder to change theme meaning.

**shadcn/ui:** alias its slots (`--background`, `--foreground`, `--primary`, …) to the authoritative semantic tokens. Keep the alias layer from becoming a second token source.
