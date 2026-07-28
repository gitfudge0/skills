---
name: gf-design-system
description: Build a complete, production-grade design system from a moodboard, screenshots, brand assets, or a written aesthetic brief. Use this whenever the user supplies visual references or describes a look and wants design tokens, a component library, UI patterns, documentation, or anything they call a "design system" — and also when they ask for a style guide, brand-to-UI translation, theming or dark-mode architecture, component library foundations, or say things like "make our product look like this" at more than one-screen scale. The skill interrogates the user to fill the semantic gaps a moodboard cannot answer, locks a written direction, then emits a three-tier token architecture, component contracts, an archetype-matched pattern library, a documentation site, and a working demo screen that provably consumes the same tokens.
---

# Design System Forge

## The problem this solves

A moodboard tells you **aesthetics**. A design system needs **semantics**.

Pinterest boards, brand decks, and "make it feel like Linear" briefs carry palette, typographic character, density temperament, and geometry. They carry almost nothing about what the product *means*: whether colour encodes state, what a disabled control communicates, which four states every surface needs, what density the user's actual job demands, whether dark mode is a preference or a requirement.

Generating a design system from aesthetics alone produces a beautiful token file that collapses the first time someone builds a real screen with it. The gap between the two is what this skill exists to close — first by extracting everything extractable, then by diagnosing precisely what is still unknown, then by asking about only the unknowns that matter.

**Never generate before the semantic layer is settled.** A gorgeous palette attached to no decisions is the failure mode, and it is seductive because it looks like progress.

---

## Workflow

Five phases. Do not skip phase 4.

### Phase 1 — Intake and extract

Inventory what you were given, then mine it. Read `references/reading-inputs.md` for the full extraction procedure.

| Input | Do this |
|---|---|
| Images (moodboard, screenshots, brand deck) | View every one. Extract palette, type character, density, geometry, materiality, vernacular. Write down what you observed, not what you assume. |
| A named reference ("like Stripe", "like Notion") | Name the two or three specific properties being pointed at. People rarely mean "clone it" — they mean one attribute. Confirm which. |
| A written brief | Extract the same axes. Mark every axis the brief left silent. |
| Existing product or repo | Audit first: count distinct colours, spacing values, button treatments, font sizes actually in use. The inventory is both scope document and funding argument. |
| Nothing but a sentence | Say so plainly, and go to Phase 3 with a wider question set. |

Produce an **extraction table**: each axis, what the input said, and your confidence. Low confidence is a signal for Phase 2, not something to paper over.

### Phase 2 — Gap diagnosis

Run the coverage checklist in `references/coverage.md` against the extraction. Sort every unresolved decision into three buckets:

- **Blocking** — generation is impossible or meaningless without it. *What is the product? Who uses it, in what conditions? What surfaces exist?* Rarely more than four.
- **Consequential** — a default is possible, but a wrong default is expensive to unwind. *Does colour carry state meaning? Is dark mode required or nice-to-have? What density does the work demand? What accessibility target? Multi-brand or single?*
- **Deferrable** — pick a sane default and state it. *Radius scale, motion durations, elevation depth, icon stroke weight.* These get recorded as assumptions, never as questions.

The bucketing is the skill's core judgement. Getting it wrong in either direction is a failure: ask about deferrables and you burn the user's patience on trivia; assume a consequential and you rebuild later.

### Phase 3 — Interrogation

Ask about blocking and consequential unknowns only. Question bank and phrasing in `references/interrogation.md`.

Rules that keep this from becoming an interview:

1. **Batch.** One round, everything at once. A second round only if answers opened a genuine fork. Never a third.
2. **Cap at seven.** If you have more than seven, you have mis-bucketed — demote the weakest to assumptions.
3. **Offer options, not open fields.** "Who uses this?" is work for the user. "Internal ops team all day / customers occasionally / developers integrating — which?" is a tap. Where the interface supports choice widgets, use them.
4. **Never ask what the input already answered.** Re-reading is cheaper than the user's goodwill, and asking twice reads as not having looked.
5. **Ask consequences, not preferences.** Not "do you want dark mode?" — everyone says yes. Ask "do people use this at night or on a factory floor, or is dark mode a nice-to-have?" The answer changes whether theming is architected in or bolted on.
6. **Let them punt.** Offer "you decide" on every question. If they take it, decide, and record it in DECISIONS.md as an assumption rather than a fact.

### Phase 4 — Direction lock

Before generating anything, write a one-page direction and get explicit agreement. This is the cheapest possible place to be wrong.

```
## Direction — [system name]

Product        [what it is, who uses it, under what conditions]
Archetype      [console | admin | editor | marketplace | comms | content]
Thesis         [one sentence: the organising idea]
Principles     [3–4 trade statements, each naming what it costs]
Palette        [4–6 named hexes with roles]
Type           [display / body / data faces, and why these]
Geometry       [radius, stroke, density, separation device]
Signature      [the one element this system is remembered by]
Assumptions    [every deferrable you defaulted, listed]
Rejected       [what you considered and dropped, and why]
```

Two checks before showing it:

**The generic test.** Work through a plausible different brief and see whether you arrive somewhere similar. If you would, the direction is a default rather than a choice — revise it and say what changed. See the anti-default list in `references/generation.md`.

**The principles test.** Each principle must name what it costs. "Clarity over cleverness" settles no argument. "Optimise for the daily user, not the first-time user — we give up onboarding hand-holding for density" settles many.

### Phase 5 — Generate and verify

Build the artefact set in `references/generation.md`, then run the verification gates. Do not present unverified output — an inconsistency the user finds first costs more trust than one you caught.

Non-negotiable gates:

- **Derivation.** Every token traces to an extracted signal or a listed assumption. No arbitrary values. If you cannot say where a number came from, it does not ship.
- **Tier discipline.** Product and demo code reference tier 2 and tier 3 only. Grep the output for raw hex outside the primitive block; the count must be zero.
- **Single source.** The demo screen consumes the same stylesheet as the docs — build it, do not hand-write parallel CSS. Verify programmatically that both contain identical token blocks.
- **Contrast.** Assert every semantic foreground/background pair against its target ratio, in every theme shipped. Report the numbers; do not claim compliance you did not compute.
- **State completeness.** Every interactive component ships default, hover, focus-visible, active, disabled, loading, and error where applicable. A component missing states gets forked downstream, and a fork is permanent.
- **Four states.** Every data surface ships loading, empty, partial, and error. Empty distinguishes *nothing yet* from *nothing matched*.

---

## Output

```
<system-name>/
├── tokens.json          Source of truth, DTCG-shaped. Nothing downstream is hand-edited.
├── <system-name>.css    Generated: three token tiers, reset, component classes.
├── docs.html            The documentation site.
├── demo-<surface>.html  A real product screen, built only from the system.
├── DECISIONS.md         Assumptions, rejected alternatives, open questions.
└── build.py             Injects the stylesheet into both HTML consumers.
```

Adjust format to the target — a React or Tailwind consumer needs adapters rather than a CSS file, and a Figma-first team needs variable naming parity. The *architecture* holds regardless: one source, semantic seam for theming, component seam for density.

The demo screen matters more than it looks. It is the proof. A system that has never rendered a real screen with real content is a hypothesis, and the screen is where you discover the token set is missing something.

---

## Scope control

Systems fail from over-investment before adoption far more often than from under-scoping. Unless the user asks for the full build, generate **phase one**: tokens, the ten to fifteen components the archetype actually needs, accessibility baseline, and one demo surface. Name what phase two and three would add, and stop.

Match pattern coverage to the archetype rather than emitting a universal list — a console needs tables, filtering, and severity routing; a content tool needs editor chrome, autosave, and revision states. `references/coverage.md` has the archetype map.

If the user asks for everything up front, build it, but say once that shipping a narrower system into one real surface beats a complete one that arrives late.

---

## Reference files

Read these when you reach the relevant phase; do not preload all four.

| File | When |
|---|---|
| `references/reading-inputs.md` | Phase 1. Extraction procedure per input type, and the explicit list of what images cannot tell you. |
| `references/interrogation.md` | Phase 3. Question bank by bucket, with phrasings that get usable answers. |
| `references/coverage.md` | Phase 2 and 5. Everything a complete system contains; per-component contract; pattern sets by product archetype. |
| `references/generation.md` | Phase 5. File contracts, token tiering rules, code conventions, anti-default guard, verification scripts. |

`scripts/build.py` inlines the stylesheet into the HTML consumers and reports whether their token blocks match. `assets/tokens.template.json` is the starting shape for the source of truth.

---

## Working with an existing system

If the user has one already, the job is extension rather than creation. Audit first and report the drift — count hardcoded colours, forked components, off-scale spacing values. Then propose the smallest change that fixes the class of problem, not just the instance. Renaming a semantic token is a breaking change and ships with a codemod and a deprecation window; say so rather than silently renaming.
