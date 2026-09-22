# Skills

A personal collection of agent skills, one directory each, each with a `SKILL.md` loaded on demand by Codex or Claude Code.

| Skill | What it does | Reach for it when |
|---|---|---|
| fudge:ship | Takes one idea, issue, or story to a verified feature. You approve the test case matrix before code; issue updates and the PR cycle are optional, and a release is not required. | "take this feature from idea to completion" |
| fudge:delegate | Enforces the orchestrator/worker split — the main agent plans, delegates, and verifies; workers implement. | "this task turned into implementation" |
| fudge:report-deck | Design system for standalone HTML report decks — the format to reach for instead of a markdown file. | "need a shareable report, not markdown" |
| fudge:gap-analysis | Reconstructs end-to-end flows from a pile of project docs, then reports the gaps and routes the open questions to whoever can answer them. | "what are we missing in these specs" |
| fudge:mindmap | Turns a document, transcript, or pile of notes into an interactive animated HTML mindmap. | "mindmap this document" |
| fudge:ui-mock | Lays out every state and flow of a feature as labeled frames on a Figma-like HTML canvas, before you build it. | "mock this up before building" |
| fudge:layered-review | Reviews a PR or diff, then layers the findings — verdict, one-line list, drill-down detail — for Slack, GitHub, or an HTML report. | "review this and don't bury me in text" |
| fudge:decision-room | Cross-functional personas pressure-test a decision independently, then synthesize into one recommendation. | "should we build this" |
| fudge:rust-arch | Idiomatic Rust architecture — project layout, workspaces, error handling, config, tracing, iced GUIs. | "structure my rust project" |
| fudge:design-system | Turns a moodboard, screenshots, or aesthetic brief into a full design system — tokens, component contracts, patterns, docs, demo screen. | "make our product look like this" |
| fudge:test-plan | Builds a risk-based test case matrix for review, then optionally executes the approved cases and records observed results in HTML. | "what should I test here" |
| fudge:conventions | Interviews you across structure, architecture, testing, tooling, workflow, docs and security, then emits a project-specific skill encoding the rules agents follow when writing code there. | "what patterns should we use in this project" |

## Install

Symlink or copy a skill directory into the skills directory for your agent (`~/.codex/skills/` or `~/.claude/skills/`):

```bash
ln -s "$PWD/fudge-test-plan" ~/.codex/skills/fudge-test-plan
```

The agent picks them up by the `name` and `description` in each `SKILL.md`'s frontmatter.

## Layout

```
fudge-test-plan/
├── SKILL.md                              # the skill itself: workflow Claude follows
├── assets/
│   ├── example.html                      # sample of the HTML report output
│   └── styles.css                        # styling for the report
└── references/
    └── test-design-heuristics.md         # supporting reference material
```
