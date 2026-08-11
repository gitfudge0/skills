# Writing rules

Two jobs. **Part A** governs how a question is put to the user during the interview. **Part B** governs whether a rule is allowed to ship at all. Both are hard requirements, not style advice — a question that fails Part A wastes the user's attention, and a rule that fails Part B is the reason conventions docs get ignored.

---

## Part A — Question style

**Never ask an open-ended question when a draft can be shown instead.** Every question describes the actual situation and what's at stake in plain language before offering choices.

**No jargon. No counts-as-shorthand.** "You catch-and-log at 14 sites and propagate at 3" is exactly the phrasing to avoid — it assumes vocabulary the user may not share and states a statistic instead of a situation. Describe what's actually happening in the code, not a tally of it.

### The worked example

This is the model of the required voice — reproduced verbatim, not paraphrased, because the phrasing itself is the spec:

> **When something fails partway through — a database call times out, a file isn't there — the code has to decide who deals with it.**
> Right now this repo does both things. In most places, the failure is written to a log and the function quietly returns nothing, so whatever called it can't tell the difference between "no results" and "it broke." In a few places, the failure is handed back to the caller to decide.
>
> Doing both is how a bug hides for a week. Pick one:
>
> **A — Hand failures back to the caller.** Only the outer layer (the request handler, the CLI entry point) decides what the user sees. Nothing gets swallowed. More plumbing to write.
> **B — Deal with it where it happens.** Log it and carry on with a fallback. Less plumbing, but a failure can pass unnoticed.
>
> Most of this repo does B today. A is the safer default and what I'd suggest, but B is defensible if these failures are genuinely routine.

Read what that example is actually doing, because every question copies the moves:

1. The situation first, in the user's words, with a concrete instance of it.
2. What the code does *today* — observed, not assumed.
3. The cost of leaving it unresolved, in one sentence.
4. Two named options with their real prices, not their marketing.
5. A stance. The skill says what it would pick and why, and leaves the other option defensible.

### More transformations

Same discipline, other dimensions from `references/dimension-bank.md`. The left column is what not to send.

| Open-ended — don't ask this | Situation first — ask this |
|---|---|
| "What's your abstraction threshold? Do you want interfaces up front or added later?" | **There are three places here where an interface has exactly one thing implementing it.** Someone building a fourth has to read both files to work out that the indirection buys nothing yet. Pick one: **A — an interface appears when the second real implementation does**, and until then callers use the concrete type; simpler to read, one refactor when the second arrives. **B — an interface at every seam up front**, so swapping is free later; more files, and most of them never get a second implementation. A is what I'd suggest — the swap you're planning for usually never happens. |
| "What should the test floor be? What's your coverage policy?" | **"Done" needs to mean the same thing every time or it means whatever seemed reasonable that afternoon.** Right now some new modules arrive with tests and some arrive without, and nothing distinguishes them. Pick one: **A — anything with a branch in it ships with a test**, so a bug fix comes with the test that would have caught it; slower per change. **B — tests are expected on the core paths only**, and glue code goes untested; faster, and the untested glue is where the next outage lives. A is what I'd suggest for anything that will outlive the quarter. |

Two things those rows have in common and yours must too: the situation is described in terms a non-specialist can picture, and neither option is a strawman. If option B reads as obviously stupid, it is not a choice — it is a leading question with extra steps, and the user will notice.

### The rules inherit the voice

**Rules in the emitted artifact get the same treatment.** State the rule, then one sentence on what goes wrong without it — the same situation-first, plain-language discipline that governs the interview questions applies to the document they produce.

So this:

> Errors cross a seam as a returned value, never as a swallowed log line. Without it, a caller can't tell "no results" from "it broke," and the difference surfaces a week later as a data bug.

Not this:

> Follow proper error-handling practices at module boundaries.

---

## Part B — The admissibility bar

This is the load-bearing quality bar. It is what separates the output from a generic best-practices dump, and it is non-negotiable per rule — a rule that fails any test below does not ship.

- **Violable today.** If no code in this repo could break it, cut it.
- **Checkable.** A reviewer can point at a line and say violated / not violated.
- **Carries a because.** The rationale is what lets an agent generalize to the case the rule didn't anticipate.
- **Counter-example from this codebase**, where one exists.
- **Not lintable.** If a formatter or linter can enforce it mechanically, it is a config line, not a prose rule. Prose rules duplicating tooling are how a conventions doc rots. Standing rule: tooling produces configuration, not prose.
- **Dependencies named.** A rule that only holds because another rule established its precondition says which rule, and `rationale.md` carries the link.

**Banned strings** — a rule containing any of the following is not admissible, full stop: "write clean code", "keep it simple", "follow SOLID", "use meaningful names".

The banned strings are not a stylistic preference. Each one is a rule that cannot be violated, cannot be checked, and carries no because — it fails three tests at once, which is why it is quicker to reject on the string.

### The bar, applied

The bar is only real if rules die at it. These are the shapes that show up most and what happens to them. The right-hand column is the instructive one: a rejected rule usually has a checkable version hiding inside it, and finding that version is the work.

| Proposed rule | Fails | What ships instead |
|---|---|---|
| "Keep it simple — don't over-engineer." | Banned string. Also unviolable and uncheckable: no reviewer can point at a line. | The threshold the user actually meant: "An interface ships when a second real implementation exists, not before. An interface with one implementation costs two files of indirection and buys nothing until the second arrives." |
| "Use meaningful names for variables and functions." | Banned string. No reviewer can adjudicate it. | Nothing at the naming level. If the user cares about a specific naming shape, it is either a linter rule (config) or a checkable one: "Exported names carry the domain noun, not the pattern — `OrderStore`, not `OrderManager`." |
| "Indent with two spaces; no unused imports; sort imports." | Not lintable — the formatter and linter enforce all three mechanically. | A line in `tooling.md`: the formatter and lint rules that enforce it, plus their inclusion in the one check command. Tooling produces configuration, not prose. |
| "Modules should be cohesive and loosely coupled." | Not checkable, and carries no because. | The import direction the user was describing: "Nothing under `domain/` imports from `http/` or `db/`. Because the domain is the part we test without a network or a database, and one import backwards takes that away." |
| "Never interpolate user input into a SQL string." | Not violable today — this project has no database and issues no queries. | Nothing. Cut it. A rule about a seam the code does not have is filler that trains the reader to skim. |
| "Errors propagate to the entry point." | Carries no because — an agent hitting a case the rule didn't anticipate has nothing to reason from. | Same rule with the reason attached: "…because a swallowed failure is indistinguishable from an empty result at the call site, and the outer layer is the only place that knows what the user should see." |
| "Background jobs authorize their own input." | Dependencies not named — it holds only because a rule elsewhere redefined "entry point" to include jobs, rake tasks, and console scripts. | The same rule, with the upstream rule named inline and the link recorded in `rationale.md`, so reversing the entry-point definition surfaces this rule instead of quietly invalidating it. |

Two patterns to take from that table. First, "not lintable" almost never means *delete* — it means the rule moves from prose to `tooling.md` as configuration. Second, a rule that fails "violable today" is the only category that reliably ends in deletion, and start-clean runs generate these in bulk because every round proposes a full default set regardless of what the code contains.

### What travels with the rules

Two things ship alongside the rules in the emitted artifact:

- A **rejected-alternatives register** (`rationale.md`), so a future agent does not reopen a settled call. Every row of the table above that was argued with the user belongs in it — the proposal, the test it failed, and what replaced it.
- An **escalation clause**: when a situation isn't covered, name the ambiguity and ask. Don't improvise a rule, and don't treat silence as permission.

The escalation clause is what makes a short rule set safe. Without it, an agent facing an uncovered case invents a rule and then treats its own invention as precedent — which is how a 40-rule contract becomes a 90-rule folk tradition nobody agreed to.
