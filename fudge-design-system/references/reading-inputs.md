# Reading inputs

Extract before you interpret. The output of this phase is a table of observations with confidence levels — not a design direction. The direction comes later, after the gaps are closed.

## Contents

- [The nine extraction axes](#the-nine-extraction-axes)
- [What images cannot tell you](#what-images-cannot-tell-you)
- [Reading a named reference](#reading-a-named-reference)
- [Reading a written brief](#reading-a-written-brief)
- [Auditing an existing product](#auditing-an-existing-product)
- [The extraction table](#the-extraction-table)

---

## The nine extraction axes

Work through all nine for every visual input. Record what you actually observe; mark the ones the input is silent on.

### 1. Palette

Pull real values, not impressions. For each image, identify:

- **The neutral ramp.** Is it warm, cool, or true grey? Does it start at pure white or an off-white? This decides more of the final feel than the accent does, and people almost never mention it.
- **Accent candidates** and roughly how much area they occupy. An accent covering 30% of a moodboard is a background colour, not an accent.
- **Saturation temperament.** Muted and desaturated, or vivid? Consistent across hues, or one hot colour among muted ones?
- **Contrast temperament.** High contrast with hard edges, or low contrast and tonal?
- **Where hue appears.** On large surfaces, on small marks, or only in imagery? A board that puts colour only on tiny marks is telling you something about the system's colour budget.

Note that moodboards routinely contain colours from photography that were never intended as brand colours. Separate deliberate palette from incidental photographic content, and say which is which.

### 2. Typography

- Serif, sans, or mixed. Grotesque, humanist, geometric, transitional?
- Stroke contrast, x-height, width. Condensed or extended?
- Weight range in use, and where heavy weights appear.
- Is there a monospace or technical face? Its presence usually indicates the subject involves data, code, or precision.
- Case usage. Any uppercase, and if so at what size and tracking?
- How many families. Two is typical; three needs a reason; one superfamily in several roles is often the strongest and most overlooked answer.

Identify faces by name where you can, but characterise them regardless — the character is what transfers, and the exact face may not be licensable.

### 3. Density and rhythm

- Generous or tight? Does content breathe or pack?
- Is spacing consistent (systematic) or varied (editorial)?
- Alignment discipline: strict grid, or deliberately loose?

Density is the axis moodboards mislead on most. Boards are curated at leisure and skew spacious; the product may be an eight-hour-a-day tool that needs to be dense. Flag any mismatch between board density and stated use, and raise it in interrogation.

### 4. Geometry

- Corner radius: sharp, subtle (2–4px), soft (8–12px), or pill.
- Stroke weight: hairline, medium, heavy.
- Shape vocabulary: rectilinear, rounded, circular, angular, organic.

### 5. Materiality and separation

How are surfaces distinguished from each other? This is a single decision with wide consequences:

- **Rules** — lines between things. Reads precise, technical, dense-friendly.
- **Elevation** — shadows. Reads soft, layered, spacious.
- **Fill** — tonal surface shifts. Reads calm, flat, modern.
- **Space alone** — nothing but gap. Reads editorial, confident, needs discipline.

Pick one as primary. Systems that use all four feel muddy.

### 6. Imagery, texture, ornament

Photography, illustration, iconography, texture, or none. Note icon style: outline or filled, stroke weight, corner treatment, grid size. Note whether there is any ornament at all — many strong systems have none, and that absence is itself a decision worth naming.

### 7. Motion

Rarely present in a static board, but if there are videos or prototypes: is motion snappy or eased, subtle or expressive? Absent input, this is a deferrable.

### 8. Vernacular

The world the subject comes from — its instruments, materials, artefacts, and language. This is where non-generic decisions come from, and it is the axis most often skipped.

A logistics tool's world contains manifests, seals, weights, and routes. A medical tool's contains charts, cuffs, and shift handovers. A music tool's contains meters, faders, and takes. Mine the vernacular for structural devices, naming, and the signature element. A system whose vocabulary comes from its subject will not look like anything else, and one whose vocabulary comes from other design systems will look like all of them.

### 9. Archetype

What kind of product this is: console, CRUD admin, editor, marketplace, communication, or content. The pattern sets in `coverage.md` are indexed by it.

Visual input names it by what it shows rather than by label. Rows, timestamps and status chips read as a console; chrome wrapped around a large empty canvas reads as an editor; faceted cards carrying prices read as a marketplace. A written brief or a named reference usually settles it in one sentence about who uses it and what they are doing.

Extract it here rather than later. The archetype fixes the pattern set and roughly half the component list, and it picks the busiest surface Phase 2 draws its three tiles on — derive it in Phase 3 and the tiles were already drawn on a surface guessed without it. Where the product is genuinely two things, name a primary and a secondary. Where the input will not support even a guess, record it blank and carry it into Phase 3 as blocking, not deferrable.

---

## What images cannot tell you

State this explicitly to the user when the input is visual-only. It reframes the interrogation as necessary rather than pedantic.

A moodboard is silent on every one of these, and each one changes the system materially:

- **Semantics.** Whether colour encodes state, and which states exist.
- **Density need.** Whether the user is here for eight hours or eight seconds.
- **Conditions of use.** Lighting, urgency, interruption, device, one hand or two.
- **Theming.** Whether dark mode is required, and whether customers ever re-theme it.
- **The four states.** What loading, empty, partial, and error should feel like.
- **Permissions.** What a user without access sees.
- **Data shape.** Whether there are tables, and how wide they get.
- **Accessibility target.** And whether procurement will demand evidence.
- **Internationalisation.** String expansion, RTL, locale formatting.
- **Platform surface.** Web only, or native and email and embeds too.
- **Voice.** How the product talks, especially when something has gone wrong.
- **Scale and governance.** How many teams consume this, and who owns it.

## Reading a named reference

When someone says "like Linear" or "like Stripe", they almost never mean clone it. They mean one or two specific properties. Name your best guess at which, and confirm:

> Linear could mean the speed and keyboard-first density, the restrained monochrome with one accent, or the crisp small-type hierarchy. Which of those are you pointing at?

This single question routinely prevents a whole wrong direction. If several references were given, look for the common property across them — that intersection is usually the real brief, and it is often something the user could not have articulated.

## Reading a written brief

Run the same nine axes and mark the silent ones. Adjectives need translating into decisions, and the translation should be shown rather than assumed, because most aesthetic adjectives are ambiguous in a way that matters:

| Brief says | Could mean | Resolve by |
|---|---|---|
| Clean | Low ornament, or low density, or high contrast | Asking which, or showing two directions |
| Modern | Geometric sans and flat, or something current in their field | Asking for one product they think looks modern |
| Professional | Conservative, or precise, or expensive | Asking who has to be impressed |
| Playful | Colour, or motion, or copy voice, or shape | Asking where the play should live |
| Minimal | Few elements, or few colours, or few type sizes | Asking what they would cut first |
| Bold | Type scale, or colour, or layout asymmetry | Asking for an example they admire |

## Auditing an existing product

If a product already exists, audit before designing. Ask for screenshots or repo access, then count:

- Distinct colour values actually in use, and how many are near-duplicates
- Distinct spacing values, and how many fall off any plausible scale
- Distinct font sizes and weights
- Button treatments, input treatments, and card treatments
- Border radii and shadow definitions

Report the counts plainly. "Forty-one greys, nine of which differ by less than 2%" does more to establish scope and urgency than any argument, and it tells you which parts of the system are genuinely contested versus merely accidental.

## The extraction table

Output of this phase. Keep it short enough to read at a glance.

```
Axis            Observed                                    Confidence
Neutral ramp    Warm, off-white base, no pure white         High
Accent          Single deep green, small marks only         High
Saturation      Muted throughout                            High
Type character  Transitional serif display, grotesque body  Medium
Mono present    Yes, in captions                            High
Density         Spacious — but board may not reflect product Low
Radius          Sharp to 2px                                High
Separation      Rules, hairline                             High
Icons           Not shown                                   —
Motion          Not shown                                   —
Vernacular      Field notebooks, survey markers, ledgers    Medium
Archetype       Admin primary, console secondary            Low
```

Low confidence and blank rows feed both Phase 2 and Phase 3 — a silent axis is where the three directions diverge, and a genuine blank is where gap diagnosis starts. Do not silently upgrade a guess to an observation — an assumption recorded as a fact is the thing that gets discovered three weeks later.
