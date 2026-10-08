---
name: "fudge:write"
description: "Write, rewrite, or review software documentation, tickets, and PR prose for clear instructions and faithful technical meaning. Use for requested technical writing work, not code changes or automatic editing of every chat reply."
---

# Write

Make technical prose easy to understand and act on. Use Simplified Technical English (STE) principles where they help software readers, while preserving the user's meaning, tone, and format.

## Locate guidance

Resolve the package root before opening shared or bundled guidance: walk ancestors of this file to `.fudge-package.json`. Paths under `shared/` are relative to that package root, even when this guide is nested. In the source checkout, the root is the ancestor containing `scripts/skill-manifest.json`; shared paths are unchanged. Links to this guide's own references remain relative to this file.

Read package-root `shared/writing.md` for complementary voice and prose guidance. The fidelity rules below constrain its style suggestions: never remove meaningful uncertainty or replace a precise technical term just to sound plainer. Read [references/examples.md](references/examples.md) when examples would help resolve a wording choice.

## Scope and output

- **Write:** Produce the requested prose from supplied facts. Use the audience, purpose, and format in the request; infer ordinary defaults when they are clear.
- **Rewrite:** Return the revised prose in the requested format. Preserve useful structure and the author's requested voice.
- **Review:** Report material clarity or meaning problems, with a correction when the source supports one. Identify the affected wording and its consequence. If there are no material problems, say so; do not manufacture findings to meet a quota.

Keep the work within the requested text. Do not modify application code, enforce this skill on unrelated replies, or create reports or files unless requested. A rewrite does not authorize posting or publishing it. Avoid an editing-method preamble unless the user asks for one.

## Meaning comes first

Before editing, identify what the reader needs to know or do and which facts support it. After editing, compare the result with the source for these invariants:

- Facts, quantities, units, version limits, sequence, actors, and responsibilities stay the same.
- Conditions, exceptions, negation, and scope remain attached to the correct action or claim. Preserve distinctions such as all versus some, and before versus after.
- Requirement strength stays the same. `May`, `should`, and `must` are not interchangeable. Do not turn a possibility into a promise, advice into a requirement, or a requirement into a suggestion.
- Uncertainty and evidence status stay visible. Preserve distinctions among suspected, reproduced, verified, planned, and shipped. Remove redundant hedging only when the remaining wording has the same meaning.
- Keep identifiers, API names, configuration keys, paths, commands, code, and quoted text exact unless the user explicitly requests changes to them. Edit surrounding explanation instead.

Do not invent missing actors, causes, acceptance criteria, measurements, or verification results. If ambiguity could change behavior, preserve the uncertain wording or mark the narrow point that needs clarification. Continue editing the parts that are clear. Use a labeled placeholder in a draft when needed; do not silently fill it with a guess.

## Make the reader's task clear

- Lead with the action, behavior, or finding the reader needs. Remove introductions that do not help them act or understand.
- Prefer short sentences with one main idea. Review procedural sentences above 20 words and descriptive sentences above 25 words for possible splits. These are review targets, not proof of clarity or correctness; keep a longer sentence when splitting would obscure a condition or relationship.
- Give each procedural step one action. Keep prerequisites and warnings before the affected action. Place a condition before its action when this helps the reader decide whether to proceed.
- Name the actor and use active voice when the source establishes who acts. Passive voice is useful when the actor is unknown or irrelevant; do not invent one to avoid it.
- Use one stable term for one concept. Distinguish different concepts even when repeating words feels less elegant. Keep domain terms that carry precise meaning; explain unfamiliar terms when the audience needs it.
- Choose plain words when the meaning is equal: `use` instead of `utilize`, `if` instead of `in the event that`. Do not replace technical words, modals, or commands through indiscriminate synonym substitution.
- Make references explicit when `it`, `this`, or `they` could identify more than one thing. Preserve the original actor if it is known; ask or flag the ambiguity if it is not.
- Use lists for steps or parallel facts and headings for meaningful divisions. Do not impose a template, sentence limit, or layout over the user's requested format.

For software docs, distinguish what the system does from what the reader must do. For tickets, keep observed behavior, expected behavior, and proposed work distinct when relevant. For PRs, describe the concrete trigger and resulting behavior, and report only supplied or observed validation. Adapt these distinctions to the requested structure rather than adding mandatory sections.

## Final pass

Read the result as the intended reader. Check that they can identify the action or claim, its actor, applicable conditions, and exceptions without backtracking. Compare each changed claim with its source; correct any drift before returning the prose or review.

## Inspiration

Inspired by [0xpili/simplified-technical-english](https://github.com/0xpili/simplified-technical-english). This is original, STE-inspired guidance for software writing. It does not use an approved-word dictionary or certify ASD-STE100 compliance.
