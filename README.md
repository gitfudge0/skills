# Skills

A personal collection of Claude Code skills, one directory each, each with a `SKILL.md` that Claude reads on demand.

| Skill | What it does | Reach for it when |
|---|---|---|
| bossie | Enforces the orchestrator/worker split — the main agent plans, delegates, and verifies; workers implement. | "this task turned into implementation" |
| deckie | Design system for standalone HTML report decks — the format to reach for instead of a markdown file. | "need a shareable report, not markdown" |
| gappie | Reconstructs end-to-end flows from a pile of project docs, then reports the gaps and routes the open questions to whoever can answer them. | "what are we missing in these specs" |
| mindie | Turns a document, transcript, or pile of notes into an interactive animated HTML mindmap. | "mindmap this document" |
| mockie | Lays out every state and flow of a feature as labeled frames on a Figma-like HTML canvas, before you build it. | "mock this up before building" |
| review-for-dummies | Reviews a PR or diff, then layers the findings — verdict, one-line list, drill-down detail — for Slack, GitHub, or an HTML report. | "review this and don't bury me in text" |
| roomie | Cross-functional personas pressure-test a decision independently, then synthesize into one recommendation. | "should we build this" |
| rustie | Idiomatic Rust architecture — project layout, workspaces, error handling, config, tracing, iced GUIs. | "structure my rust project" |
| testie | Right-sized, risk-prioritized test plan — then runs the cases and marks PASS/FAIL in an HTML report. | "what should I test here" |

## Install

These live in `~/.claude/skills/`; symlink or copy a skill directory there:

```bash
ln -s "$PWD/testie" ~/.claude/skills/testie
```

Claude picks them up by the `name`/`description` in each `SKILL.md`'s frontmatter.

## Layout

```
testie/
├── SKILL.md                              # the skill itself: workflow Claude follows
├── assets/
│   ├── example.html                      # sample of the HTML report output
│   └── styles.css                        # styling for the report
└── references/
    └── test-design-heuristics.md         # supporting reference material
```
