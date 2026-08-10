# Coverage

What a complete system contains. Use in Phase 3 to find gaps, and in Phase 5 to check nothing shipped half-built.

## Contents

- [The four layers](#the-four-layers)
- [The four crosscutting concerns](#the-four-crosscutting-concerns)
- [Foundations checklist](#foundations-checklist)
- [Per-component contract](#per-component-contract)
- [Pattern sets by archetype](#pattern-sets-by-archetype)
- [Universal patterns](#universal-patterns)

---

## The four layers

**Principles** — three to five trade statements that settle arguments. Each names what it costs. Without them, every review is a taste debate.

**Foundations** — tokens, tiered. Not just colour and type: spacing rules, layout, elevation, z-index, motion, iconography.

**Components** — the library. Depth per component matters far more than count.

**Patterns** — how components combine to solve recurring product problems. The layer most often skipped, and where most of the value sits for anything B2B.

## The four crosscutting concerns

These are properties of every layer, not sections at the end.

**Accessibility** — target, contrast, focus, keyboard, screen reader, motion, target sizes, and how conformance is verified rather than assumed.

**Content** — voice, microcopy formulas, terminology glossary with one word per concept, formatting rules for dates, numbers, durations and currency, internationalisation readiness.

**Delivery** — token pipeline, package versioning, testing, documentation, migration tooling.

**Governance** — ownership, contribution path, definition of done, deprecation policy, adoption metrics.

---

## Foundations checklist

Everything below needs a decision. Most are deferrable, but none are skippable.

**Colour** — neutral ramp; accent ramps; semantic mapping to roles; state colours if colour carries meaning; surface hierarchy; border colours; overlay scrim; theme variants.

**Typography** — families by role; type scale with a fixed number of steps; weights; line heights; letter spacing; tabular figures for data; measure — line length capped by the container token, not eyeballed per breakpoint; responsive behaviour; uppercase policy.

**Space** — base unit; scale; and rules for *which* value applies where. The rules matter more than the scale, and are almost always missing. Label-to-control, field-to-field, section-to-section should each have an answer.

**Layout** — breakpoints set where the content breaks, not at device widths, which drift within a year; container widths; grid; density modes if the archetype needs them.

**Depth** — elevation levels tied to meaning, not just blur radii; a named z-index scale so nobody writes `z-index: 9999`.

**Shape** — radius scale; border widths; the primary separation device.

**Motion** — durations; easing curves for entrance and exit; what animates and what never does; reduced-motion handling as a global rule.

**Icons** — grid size; stroke weight; optical alignment; naming; delivery format; filled versus outline policy.

**Opacity** — disabled state is the only legitimate use of opacity on text; anywhere else it makes contrast uncomputable, since the ratio depends on whatever sits behind it.

**Focus** — ring colour, width, offset, set once and globally rather than per component — a ring that changes shape between components trains users to stop trusting it.

**Print** — page size and margins; ink-safe colour remap of the semantic tier; backgrounds do not print by default; hairlines below ~0.5pt vanish on press; pt, not px, drives the type scale; link URLs need a visible destination since paper can't be clicked. Print is a target, not a stylesheet afterthought.

---

## Per-component contract

A component is not done until all of this exists. Half-built components get forked, and forks are permanent — which is why partial components are worse than absent ones.

1. **Anatomy** — named parts, what is required, what is optional.
2. **Variants** — and what each one *means*, not just how it looks. If two variants have no semantic difference, there is one variant.
3. **Sizes** — and where each is appropriate.
4. **States** — default, hover, focus-visible, active, disabled, loading, error, read-only, selected. Not every component has all nine; every component has a documented answer for each.
5. **Responsive behaviour** — down to the narrowest supported width.
6. **Accessibility contract** — role, keyboard map, ARIA, focus management, announcement behaviour.
7. **Content guidelines** — what the label says, casing, length limits, what happens when text overflows.
8. **Do and don't** — the misuse this component actually attracts, not generic advice.
9. **API** — props or classes, defaults, and which are required.

The states matrix is what gets underestimated. A button is not one thing; it is variant × size × state × icon position. Enumerate before building, or the last three states never arrive.

---

## Pattern sets by archetype

Match the pattern set to the archetype rather than emitting a universal list. Identify the archetype in Phase 1 and confirm it in the direction lock.

### Console / monitoring
*Dashboards, observability, incident response, trading, logistics.* Users are here all day, scanning for exceptions.

Dense data tables · severity and status encoding · filtering and saved views · real-time updates without layout shift · alerting and notification routing · time range selection · drill-down from summary to detail · acknowledgement and assignment · density modes · keyboard-first navigation.

Charts consume system tokens rather than inventing their own — the names are reserved in the template's optional `semantic.chart` group. Palette construction — categorical vs sequential vs diverging, and each one's accessibility constraints — belongs to the `dataviz` skill; don't re-derive it here.

### CRUD admin
*Internal tools, back office, configuration.* Users are trained, tasks are repetitive.

Resource list and detail · create and edit forms with validation · bulk operations and undo · search and filter · permission-aware controls · audit trails · relationship pickers · destructive action confirmation · import and export.

### Editor / canvas
*Documents, design tools, IDEs, form builders.* Long focused sessions, high stakes on data loss.

Toolbars and contextual controls · selection model · undo and redo · autosave and save state indication · version history · collaboration presence and conflicts · panels and inspectors · zoom and viewport · keyboard shortcut system · unsaved-changes guards.

### Marketplace / commerce
*Storefronts, booking, listings.* Mostly unfamiliar users, conversion matters.

Browse and search with facets · product and listing cards · comparison · cart and checkout flow · payment and address forms · order status · reviews and ratings · availability and pricing display · trust and error recovery at payment.

### Communication
*Chat, email, support desks, social.* Interruption-driven, notification-heavy.

Message composition and threading · read and unread state · notification and badge counts · presence · attachments · search across history · mentions · mute and snooze · draft persistence.

### Content / publishing
*CMS, blogs, docs, learning.* Split between authoring and reading.

Reading typography at length · article and media layout · navigation and table of contents · authoring versus preview · publishing workflow and states · taxonomy and tagging · scheduling · media handling · SEO and metadata surfaces.

---

## Universal patterns

Every archetype needs these. If the generated system omits one, it is incomplete regardless of how good the tokens are.

**The four states.** Loading, empty, partial, error — for every surface that fetches. Empty distinguishes *nothing yet* (offer the first action) from *nothing matched* (offer to clear the filter). Partial means showing what loaded and marking what did not, rather than failing a whole page because one widget timed out.

**Feedback routing.** Which surface carries which message — inline for one control, toast for a completed action, banner for a system condition, dialog for the irreversible. Without a routing table every team reaches for a modal.

**Destructive actions.** Friction tiered by blast radius: reversible and local gets immediate action plus undo; irreversible gets a dialog naming exact consequences and counts. Prefer undo over confirmation wherever the action can be made reversible — a dialog is an admission that it could not be.

**Permissions.** What a user without access sees. Three legitimate treatments — hidden, disabled with a reason naming who *can* do it, or visible with a path to enable. The illegitimate one is a control that looks available and fails on click, which is the default outcome when nobody designs this.

**Forms and validation.** When validation fires, where errors appear, the error copy formula (*what happened · why · how to fix*), focus behaviour on failed submit, and the difference between disabled and read-only.

**Navigation and wayfinding.** Shell structure, current location, breadcrumbs or equivalent, and what happens at the narrowest supported width.
