---
name: war-room
description: Generates cross-functional personas from the actual project/domain (PM, design, engineering, ops, etc.), gets each one's independent take on a feature, bug, or technical decision, then synthesizes their input into a clear product decision — a recommendation, risks to watch, and open conditions. Produces a decision-first HTML artifact plus a chat summary. Use this whenever the user wants multiple perspectives, a pressure-test, or help deciding on a feature, bug, architecture call, or product change — including indirect phrasing like "is this a good idea," "what would the team think," "what are the tradeoffs here," "should we build this," or "help me decide." Also trigger on explicit phrases like "war room this," "get different perspectives on this," "pressure-test this," or "run this by the team."
---

# War Room

Casts a small set of role-specific personas grounded in the actual project, gets each one's independent read on a feature/bug/decision, then synthesizes that input into an actual product decision — not a transcript of a meeting. The value is in reaching a clear recommendation while keeping real disagreement on record, not smoothing it into false consensus.

This skill has five phases: **gather context → cast the room → collect independent input → synthesize a decision → produce output.** Always deliver output as both a written summary in the chat and an HTML artifact — never one without the other.

## Phase 1: Gather context

You need two things before casting anyone: what kind of company/product this is, and what's actually being decided.

**Determine environment first:**
- If working in a real repository (files on disk, not just chat), scan it before asking the user anything. Useful signals: `package.json`/`pyproject.toml`/`Cargo.toml` (stack + dependencies), README (stated purpose), folder structure (monolith vs. services, mobile vs. web), CI config (release cadence, team maturity), and — if provided — a specific diff, issue, or PR as the topic itself. Prefer inferring over asking; you can usually tell "quick-commerce inventory system" from "internal analytics dashboard" just from the dependency list and folder names.
- If there's no repo, or you're working purely in chat, use whatever the user and prior conversation already tell you about the product/domain. If it's genuinely unclear, ask **one** short question covering both the domain and the company stage (e.g., "What does the product do, and roughly what stage — early startup, scaling, established?") rather than a checklist.

**The topic itself** (the feature, bug, or decision) usually arrives with the request. If it's too thin to debate meaningfully (e.g., "pin favorites" with zero detail on what pinning would even do), make one or two reasonable assumptions about scope, state them plainly, and proceed — don't stall the whole exercise on missing detail.

## Phase 2: Cast the room

Generate 5–7 personas *specific to this domain and this topic* — never reach for a fixed roster. A quick-commerce inventory feature and a fintech compliance change should produce visibly different rooms. See `references/persona-inspiration.md` for domain-flavored examples, but treat it as a warm-up, not a lookup table — invent and rename as the context demands.

For each persona, define:
- **Role** — their function (can be a real title or a plausible one for this company's size, e.g. a 5-person startup won't have a dedicated "Data Platform Lead")
- **Priority** — the one thing they're optimizing for or protecting (velocity, reliability, user trust, unit economics, compliance, support load, etc.)
- **Grounding detail** — one concrete fact tying them to *this* project if you found one in Phase 1 (e.g., "wary of this because the current DB has no read replicas" beats a generic "worried about scale")
- **Name** — if the user has asked for personas named after a fictional universe (a fantasy series, a show, etc.), pick the character whose known personality actually matches that persona's stance and priority — the paranoid/cautious character becomes the skeptic, the rule-bound stickler becomes whoever owns rigor and process, the ambitious risk-taker becomes whoever's pushing for more scope. Don't assign names arbitrarily; the fit should make each persona instantly readable. Once a universe has been established in the conversation, keep using it for later runs unless told otherwise.

Two casting rules that keep the room honest:
1. **Include a genuine skeptic** — someone whose default reaction is "why are we building this" or "this breaks something else." Rooms that only contain advocates produce useless output.
2. **Include whoever owns the boring-but-real constraint** — ops, support, legal, infra, whoever eats the consequences after launch. This is usually the most undervalued voice and the one most worth including.

## Phase 3: Collect each persona's input

No dialogue, no back-and-forth, no meeting transcript — each persona gives their own direct, independent read on the task, filtered through their priority. For every persona in the room, produce:

- **Stance** — for / skeptical / conditional
- **Take** — their 1–3 sentence case, grounded in their specific priority and (where you found one in Phase 1) a concrete project detail
- **Flagged risk or dependency** — the one thing they'd raise if nobody else did

Write each persona's input as if it's the only thing they were asked — not a reaction to anyone else's point. The value here is seeing where independent lenses land in the same place versus where they genuinely diverge, without staging that convergence as a conversation.

## Phase 4: Synthesize into a decision

This is the actual payoff, and it should read like a real product decision, not a recap of what everyone said:

- **Recommendation** — what to actually do (ship it, ship a smaller version, hold, kill it), stated plainly, not hedged
- **Why** — which personas' input supports this, and how you weighed conflicting priorities to land here
- **Risks to watch** — pulled from whichever persona(s) were skeptical or conditional; keep these on record rather than smoothing them into consensus
- **Conditions / open questions** — anything that needs resolving before or during build
- **Out of scope** — what's explicitly not part of this decision

One pattern worth calling out explicitly when it happens: if two or more personas raise the *same* concern independently, without having seen each other's input, that convergence is a stronger signal than any single persona's opinion — flag it as such in the synthesis.

## Phase 5: Produce output

Always produce both:

**1. Chat summary** (concise, in the response itself) — lead with the Recommendation, then Risks to Watch, then Conditions and Out of Scope. This is what the user is actually here for; don't bury it under a restatement of every persona's input.

**2. HTML artifact.** This is the visual version of the same thing — not a meeting recreation, a decision brief:
- Use the default visual identity in `references/design-system.md` (cream background, navy tree/org-chart structure, elbow connectors, node chains, annotation panels, pill badges) — this is a locked-in design system, not a fresh brief each time. Read it before building. Only depart from it if the user explicitly asks for a different look for that run; don't re-run frontend-design brainstorming by default the way a one-off page normally would.
- The decision (recommendation, risks, conditions, out of scope) should be the first substantive thing on the page and the easiest thing to find — not something the reader scrolls past persona detail to reach.
- Show each persona's input as its own row/node in the tree structure (role, priority, stance, take, flagged risk) — not chat bubbles, not a transcript, no implication they're responding to each other.
- Single HTML file, CSS variables for theming, no external dependencies beyond what's normally available in artifacts (Google Fonts links are fine).

## Notes by environment

- **Claude Code**: lean on real repo signals over asking questions. If a PR diff or issue is available, use it directly as the debate topic rather than asking the user to restate it.
- **Claude.ai / chat-only**: work from whatever context the conversation already provides; state assumptions inline rather than interrogating the user for details a real meeting wouldn't wait for either.
