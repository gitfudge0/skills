# Working defaults

Per-project preferences for how far work goes and what may be written outside the repository. They live in a `## Working defaults` section of the project's governing rules: the project conventions skill (`<project>-conventions`) when one exists, otherwise `AGENTS.md` or `CLAUDE.md`.

```markdown
## Working defaults

- endpoint: pr-opened
- commit-push: ask
- external-writes: draft-first
- runtime: docker-only
```

## Keys

All keys are optional. Unknown keys are ignored.

| Key | Values | Absent means |
|---|---|---|
| `endpoint` | `verified-locally` · `pr-opened` · `pr-ready` | ship's existing default (`pr-ready` when a forge is configured) |
| `commit-push` | `ask` · `allowed` | current behavior |
| `external-writes` | `draft-first` · `allowed` | `draft-first` for issue trackers and chat (for example Jira, Linear, Slack); existing behavior for PR delivery |
| `runtime` | `docker-only` · `local-ok` | follow the project's existing run docs |

## Precedence

1. An explicit instruction in the current conversation.
2. Working defaults.
3. Skill defaults.

A conversation instruction overrides a default for that work only; it does not rewrite the recorded defaults. An explicit request to create or post specified content to a specified destination authorizes that write; an explicit request to post without a draft overrides `draft-first` for that work. A generic request to draft, review or investigate does not authorize posting. Preserve an earlier approval of the exact content and destination rather than asking again. `external-writes: allowed` removes the draft gate; it does not authorize unrelated messages or destinations.

## Draft-first

Before posting to an external system (ticket text, tracker comment, chat message, review comments), show the exact content and its destination, then wait. A later "go ahead" authorizes that shown content only; changed or additional content needs its own approval. Drafting, reading, and local files are never blocked.

## Who reads and writes

- `fudge:setup` records and amends the section with the user's approval.
- `fudge:ship`, `fudge:ticket`, `fudge:review`, and `fudge:bug-fix` read it before choosing an endpoint, committing or pushing, starting services, or posting externally.
