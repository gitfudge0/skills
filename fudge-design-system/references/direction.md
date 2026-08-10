# Direction

Phase 2. Three directions rendered as real screens, one gets picked, and the look is locked. It runs on the extraction alone, before interrogation, because every token in the system derives from the look — put a questionnaire in front of it and the dependency is inverted. Prose is no substitute: it asks the user to agree to a description of a room they have not stood in, nobody can do that honestly, and the real reaction arrives after generation, when it is expensive to act on.

## Contents

- [Deriving three directions](#deriving-three-directions)
- [Diverge on the silent axes](#diverge-on-the-silent-axes)
- [The divergence rule](#the-divergence-rule)
- [Worked example — console](#worked-example--console)
- [What a tile is](#what-a-tile-is)
- [The directions.html contract](#the-directionshtml-contract)
- [Presenting the choice](#presenting-the-choice)
- [Mixes](#mixes)
- [Rejection](#rejection)
- [What this phase does not decide](#what-this-phase-does-not-decide)
- [Recording and locking](#recording-and-locking)

---

## Deriving three directions

You have the extraction and whatever the user's own brief stated outright. That is less than you would like, and it is enough — the three tiles are how the rest arrives.

1. **Fix what is not up for a vote.** Everything the extraction pinned down and everything the brief said in words: the neutral ramp read off the moodboard, a named typeface, a stated platform, an existing product to stay consistent with. These are constraints on all three. A direction that quietly relaxes one is not a direction, it is a different brief, and it will win for the wrong reason.
2. **List the axes the input left silent.** Separation, density, type character, colour budget, plus the secondaries below — minus any the extraction already settled. The silent ones are the whole working area.
3. **Pick the surface to draw.** A tile needs a screen. Use the most plausible busiest surface the input implies, and say which you assumed, in the tile label. If the input genuinely never says what the product is, that one question — *what is this, in one line, and who uses it?* — rides along in the same message as the tiles rather than becoming a round of its own. One question is not a questionnaire.
4. **Commit each direction hard to one axis** and let the rest follow from it. The commitment is what makes a direction nameable; a direction you cannot name in one word has not committed.
5. **Screen all three against the anti-default guard** in `generation.md` before rendering anything. Three directions that all trip the same entry are one direction rendered three times. The guard exists because these outputs converge under pressure, so this failure is the likely case, not the exotic one.

Never build a timid one, a bold one, and a middle one. That is a slider, not a choice, and the middle always wins by default rather than on merit. All three must be ones you would defend. Three, not two: two reads as a binary and invites "can I have both". Three, not four: by the fourth you are padding, and the user can feel it.

---

## Diverge on the silent axes

**Diverge where the input said nothing. Never on what it already settled.** If the moodboard clearly landed a warm neutral ramp, all three tiles keep the warm neutral ramp and fight somewhere else. A tile that swaps in cool greys to widen the spread reads as not having looked at the moodboard, and it costs you the other two as well — the user now suspects none of the three came from their material. That loses you a divergence axis every time the input is rich, which is the correct trade: an axis the user has already decided is not a question, and re-opening it in pixels is the same rudeness as re-opening it in words. If the extraction settled so much that fewer than four axes are left silent, say so and push harder on the ones remaining rather than manufacturing a disagreement.

**Thin input makes this phase more valuable, not less.** A single sentence leaves nearly every axis silent, so the three spread as wide as they legitimately can — and three wide guesses rendered is the cheapest method anyone has for finding out what a person wants. The instinct that you need more information before showing options has it backwards: the options are how the information arrives.

---

## The divergence rule

**The three must take different positions on separation device, density, type character, and colour budget — every one of those the input left silent.** Three hues of one layout is one direction wearing three shirts. The user works this out in about four seconds, and the phase then costs credibility instead of buying it.

| Axis | Positions to choose between |
|---|---|
| Separation | Rules · elevation · fill · space. One per direction, doing all the work. A direction using all four has not decided anything. |
| Density | Row height, gutter, information per screen. Two directions landing at the same density have wasted the axis. |
| Type character | Grotesque · humanist · condensed · mono · serif — each chosen for a property the brief needs, never because it is current. |
| Colour budget | How much surface area may carry hue, and whether hue is data or decoration. Where the brief has not said, treat both readings as live and let the tiles argue it. |

Secondary axes — radius and stroke, motion temperament, where the signature element sits, chrome weight — should vary too, but variation *only* here is the failure the rule bans.

---

## Worked example — console

Extraction from a six-image moodboard of operations tooling, plus a one-line brief: *an alerting console for an infrastructure team.* The moodboard settled a cool charcoal ramp and a dark field, so all three keep those; it said nothing about separation, density, type character, or colour budget, so those are the working area. Same screen in all three tiles — the alert board, assumed as the busiest surface: twelve rows, three severities, one acknowledged row, one filtered-empty state.

**Strip Board** — *The row is the object. Severity tints the whole strip, so the board reads as a colour field from three metres away.*
Separation by **fill**; no rules, no shadow. Medium density, 36px strips with a 4px gap between them. **Condensed grotesque**, uppercase micro-labels, tight tracking. **High colour budget** — six severity tints own most of the surface; brand appears nowhere in the data area. 2px radius. Vernacular: air-traffic paper flight strips.

**Long Watch** — *Nothing is drawn that space could do. The board is still legible on hour nine because there is almost no ink in it.*
Separation by **space**; zero borders, zero fills, one alignment spine. Loosest density, 48px rows, wide gutters. **Humanist sans** at a large body size with a true italic for metadata. **Minimal colour budget** — one hue in the entire system; severity carried by weight, a repeated glyph, and rank order. No radius, because there is no box.

**Rack** — *Panels are housings. Maximum density, every value monospaced, the board behaves like a wall of gauges rather than a document.*
Separation by **elevation**; recessed field, panels lifted one level, rules only *inside* a panel. Tightest density, 26px rows and a compact mode below that. **Mono for every value**, narrow grotesque for chrome only. **Medium colour budget** — two hues; severity by saturation step on one ramp, paired with a numeric badge. 6px radius on panels, 0 inside them.

None trips the guard: no cream-and-serif with a terracotta accent, no near-black field with one acid accent (Rack runs a two-hue palette on a mid-charcoal), no gradient, no hairline-rule broadsheet (Long Watch has no rules at all), and three different radii rather than 8px everywhere. Each type choice names the property earning it.

---

## What a tile is

A tile is a small but genuine screen from the archetype's busiest surface, at real density with real content and at least one edge case. Every tile shows **the same content**, so design is the only variable.

Each tile carries three labels: a **name**, a **one-line thesis**, and a **differs-on** line naming the axes and the position taken. The third label is what lets the user say *the density* rather than *that one*, and an axis named is an axis you can mix. Where the surface itself was an assumption, the label says so, so a wrong guess gets corrected in the same breath as the pick.

A tile is never a swatch grid, a palette strip, a type specimen, a component gallery, a mood collage, or lorem ipsum. Those are the failure this phase was built to fix — a palette strip communicates the hexes, which is the one thing prose already conveyed perfectly well.

Keep each tile roughly ten minutes of work. A tile polished for an hour is a tile you will defend instead of drop, and your investment is not evidence about the user's taste.

---

## The directions.html contract

- **One self-contained file.** No network of any kind, no build step, no `build.py`. It opens by double-click and works offline.
- **Three tiles, equal width, side by side.** Below roughly 1000px they stack, in the original order. The order never changes — "the second one" must stay the second one for the whole conversation.
- **Tiles must not share styles.** Scope every rule per tile. These are competing systems, and one custom property leaking across is a rigged comparison.
- **One theme, the one the extraction implies.** Render both only if the input already established a dark product. Whether dark mode is *required* is an interrogation answer that has not been asked yet, and it applies to the locked look afterwards; comparing a light tile against a dark one compares nothing.
- **It does not ship.** It is a pre-generation artefact, not a token consumer, and it is exempt from every Phase 5 gate. Do not build it from the system; the system does not exist yet.

---

## Presenting the choice

Open the file, then ask one question: **which of these would you defend to someone who disagreed?** Not which they like — liking is polite and defending is real.

In the same message, state both other legal moves explicitly, or the user will assume the menu is the whole menu:

- **Mix.** "Tile 2's palette with tile 1's density" is a valid answer.
- **Reject all three.** Also valid, and cheap here.

Do not name your own favourite before they answer. It collapses the sample to your taste, which is the failure mode this phase exists to escape. Answer afterwards if asked.

---

## Mixes

A mix is often where the real answer is, because it names the axis the user actually cares about — information a clean pick does not carry. Check coherence before locking, though: two directions' best halves frequently contradict.

- Dense structural grid + spacious editorial type scale — two systems in one file, and the type will lose every layout argument.
- Fill separation + a high colour budget elsewhere — severity now competes with brand for the same surface, and severity must win.
- Elevation separation + zero radius and hairline strokes — the shadows read as printing errors.
- Mono data + a loose humanist scale — the alignment that justified mono is gone, so the mono is costing width for nothing.

If the halves fight, say which two and why, then resolve toward the axis the user's mix revealed they care about. Re-render only the mixed tile if the conflict is genuinely unclear — that is one tile of work, not three.

---

## Rejection

All three rejected is a cheap and successful outcome, not a failure. It cost one throwaway file and it happened before generation rather than after.

Ask what was wrong; it is almost always one axis. Then run **one** more round of three, moved decisively on that axis — not three fresh guesses.

Never a third round. Three plus three that land nothing means the brief is wrong, not the directions. Say that out loud, name which blocking answer you now doubt, and go back to it. Continuing to generate directions at that point is expensive theatre.

---

## What this phase does not decide

The look is locked. The density floor, colour semantics, and the accessibility target are not — those are interrogation answers, and they can land in conflict with the tile that won. When they do, **the look holds and the semantics bend it.** An AA target lifts the foreground on a low-contrast winner; it does not send you back to the tiles. All-day sessions tighten or loosen row height inside the winning direction; the separation device survives untouched.

The exception is a structural collision — colour is decorative in the winning tile and interrogation turns up six severity levels that need hue, or the winner separates by space and the answer is a virtualised table of thousands of rows. Then name the collision to the user in plain terms and re-render **only the affected tile**, on the one axis that broke. That is one tile of work. Do not restart the phase: the user's taste did not change, one of your assumptions did.

---

## Recording and locking

DECISIONS.md records the winner **and both losers** — name, thesis, and why each lost, in the user's words wherever they gave them. The losers are the most useful entries in the file. "Why doesn't this look like X?" gets asked by every new team, and "we built X, here it is, here is why it lost" ends that conversation in one message instead of a meeting.

This phase hands forward two things: the **locked look** — separation device, density position, type character, colour budget, radius and stroke, where the signature sits — and the **loser record**. The written one-pager is not filled here. It waits for Phase 4, because Product, Archetype, Principles and Assumptions all need answers only interrogation produces; the locked look supplies its Palette, Type and Geometry rows when it gets there. Both checks run on the page then — and by then they are a transcription check on something the user has stood in, rather than a bet on something they have only read.
