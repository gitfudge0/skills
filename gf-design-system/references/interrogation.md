# Interrogation

The goal is the smallest number of questions that make the system correct. Every question spends the user's patience, and patience spent on trivia is not available for the question that actually mattered.

## Contents

- [Rules](#rules)
- [Blocking questions](#blocking-questions)
- [Consequential questions](#consequential-questions)
- [Deferrables — never ask these](#deferrables--never-ask-these)
- [Phrasings that work](#phrasings-that-work)
- [Reading non-answers](#reading-non-answers)
- [Second rounds](#second-rounds)

---

## Rules

1. **One batch.** All questions at once, not a conversation.
2. **Seven maximum.** More than seven means the bucketing is wrong. Demote the weakest.
3. **Choices, not blanks.** Every question ships with 2–4 options plus an escape hatch. Where the interface has a choice widget, use it rather than prose bullets.
4. **Never re-ask.** If the input answered it, do not ask. Re-reading costs you nothing and asking twice reads as inattention.
5. **Consequences, not preferences.** People answer preference questions aspirationally and consequence questions accurately.
6. **Always allow a punt.** "You decide" is a valid answer. Take it, decide, and log it in DECISIONS.md as an assumption rather than a fact.

---

## Blocking questions

Generation is meaningless without these. There are rarely more than four, and the input often answers two.

**What is this, in one line, and who uses it?**
The single highest-value question. Everything else follows from it. Push past the category: "a CRM" tells you little; "a CRM for field service companies whose users are dispatchers watching a live board" tells you nearly everything about density, colour semantics, and pattern set.

**How long is a session, and under what conditions?**
Eight hours at a desk, or ninety seconds on a phone in a warehouse. Determines density, type size, target sizes, and contrast. Options: *all-day tool / several times a day / occasional / one-off*.

**What are the two or three main surfaces?**
Names the component and pattern set, and gives you the demo screen. If they cannot name them, the product is not defined enough to systematise yet — say so, and offer to work from one screen instead.

**Is this greenfield, or does something exist to stay consistent with?**
Changes the job entirely. Existing means audit-and-extend with migration cost; greenfield means free choice.

---

## Consequential questions

Defaultable, but a wrong default is expensive. Pick the three or four that actually bite for this product; do not ask all of them.

**Does colour need to carry meaning?**
Whether hue is decoration or data. If states, severities, tiers, or categories exist, colour is spoken for and the brand accent has to work around it. Options: *yes, several states / one or two states only / no, colour is decorative*. Ask whenever the product has status of any kind — which is most B2B products.

**Is dark mode required, or nice-to-have?**
Required means the semantic tier is architected as a real seam from day one and every pair is contrast-tested twice. Nice-to-have means it can be retrofitted at a known cost. Phrase it by condition: *do people use this at night, in dark rooms, or next to other dark tooling?*

**What accessibility target, and does anyone audit it?**
WCAG 2.2 AA is the sane default. Ask because the real question underneath is whether procurement will demand a conformance report — that changes documentation, testing, and timeline, not just contrast values. Options: *AA and we may need to prove it / AA as good practice / not a current concern*.

**How much data is on screen at once?**
Tables of thousands of rows demand density modes, sticky headers, virtualisation, and a different type scale than a form-based tool. Options: *heavy tables / moderate lists / mostly forms and detail views*.

**One brand, or many?**
White-labelling or customer theming forces stricter token discipline and bans hardcoded values anywhere. Retrofitting multi-brand is one of the most expensive changes there is, so this must be asked whenever the product has enterprise customers.

**What platforms consume this?**
Web-only stays CSS. Native, email, or embeds mean the source of truth must emit multiple formats and the component layer cannot assume the DOM.

**Who builds with this, and how many teams?**
One team needs a component library. Five teams need a contribution model, versioning policy, and adoption metrics — that is a different deliverable and a different amount of work.

**How should this sound when something breaks?**
Voice is a system decision and the error state is where it is most visible and most often wrong. Options: *plain and factual / warm and reassuring / terse and technical*.

---

## Deferrables — never ask these

Decide, state the assumption, move on. Every one of these has a defensible default derivable from the extraction, and asking about them signals that you cannot make a decision.

Radius scale · spacing base unit · elevation depth · motion durations and easing · icon stroke weight · z-index layers · border widths · focus ring style · skeleton versus spinner · exact type scale ratio · component naming convention · file organisation.

If the user volunteers an opinion on one, take it. Do not solicit it.

---

## Phrasings that work

| Weak | Strong | Why |
|---|---|---|
| Do you want dark mode? | Do people use this at night or in dark rooms, or is dark mode a nice-to-have? | Everyone says yes to the first; the second gets the truth |
| What's your brand colour? | Where should colour appear — on large surfaces, or only on small marks and states? | Gets the colour budget, which matters more than the hex |
| How accessible should it be? | Will anyone need to see a conformance report — procurement, a public sector customer? | Surfaces the real constraint behind the polite answer |
| What components do you need? | Walk me through your two busiest screens | Produces a real inventory instead of a wish list |
| Do you like this direction? | Which of these three would you defend to someone who disagreed? | Forces a real preference rather than politeness |
| How dense should it be? | Is someone in this all day, or dropping in occasionally? | Density is a consequence of use, not a taste |

## Reading non-answers

- **"All of them" / "everyone"** — the product is under-defined. Ask who uses it *most*, by hours.
- **"Make it pop"** — usually contrast, occasionally saturation, sometimes hierarchy. Show two options rather than asking again.
- **"Clean and modern"** — carries no information. Ask what they would cut first from a screen they already have.
- **"Like [competitor]"** — ask which specific property. See the named-reference procedure in `reading-inputs.md`.
- **Silence on a blocking question** — do not proceed on a guess. Say which decision is stuck and what you would assume, and let them correct it. A stated assumption is recoverable; a hidden one is not.

## Second rounds

One more round only when an answer opened a genuine fork — for example, "we white-label for enterprise customers", which changes token architecture, or "it's mostly used on a phone in a truck", which changes the whole density and target-size direction.

Never a third round. If you still have unknowns after two, they are deferrables in disguise. Default them, list them under Assumptions, and move to the direction lock — the user will correct what matters when they read it, and a written assumption is easier to argue with than a question is to answer.
