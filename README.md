# Skills

A personal collection of agent skills, one directory each, each with a `SKILL.md` loaded on demand by Codex or Claude Code.

| Skill | What it does | Reach for it when |
|---|---|---|
| fudge:ship | Takes one idea, issue, or story to a verified feature. UI guidance or a mock is used when needed; you approve the test case matrix before code. Issue updates and the PR cycle are optional. | "take this feature from idea to completion" |
| fudge:design | Routes UI work to concise guidance, a reviewable draft, reusable project rules, or a requested component build. Output and effort follow the decision and its risk. | "design this flow", "guide this UI build", or "build these components" |
| fudge:ux-research | Discovers user needs or tests UI tasks with participants, then traces findings to design decisions. | "learn what users need" or "test whether people can complete this task" |
| fudge:content-architecture | Organizes routes, navigation, labels, and interface copy around a person's task, with evidence and assumptions recorded. | "make this information findable" or "fix these labels and instructions" |
| fudge:interaction-design | Specifies actions, states, permissions, feedback, and recovery across a UI task. | "define how this flow behaves" or "what happens when save or submit fails" |
| fudge:accessible-ui | Designs or audits accessible UI with criterion-level evidence, remediation, and retest. | "audit this for WCAG" or "make this component work with keyboard and screen reader" |
| fudge:design-qa | Compares a built UI with its selected design across task paths, states, viewports, themes, content, and input. | "check this implementation against the mock" or "retest the UI design fixes" |
| fudge:experience-measurement | Defines task success and checks whether a launched UI improves it with trustworthy events and a credible comparison. | "did the redesign help people finish" or "measure this onboarding flow" |
| fudge:delegate | Enforces the orchestrator/worker split — the main agent plans, delegates, and verifies; workers implement. | "this task turned into implementation" |
| fudge:report-deck | Design system for standalone HTML report decks — the format to reach for instead of a markdown file. | "need a shareable report, not markdown" |
| fudge:gap-analysis | Reconstructs end-to-end flows from a pile of project docs, then reports the gaps and routes the open questions to whoever can answer them. | "what are we missing in these specs" |
| fudge:mindmap | Turns a document, transcript, or pile of notes into an interactive animated HTML mindmap. | "mindmap this document" |
| fudge:ui-mock | Shows the requested UI decision and consequential states in a self-contained HTML mock with task-relevant frames. | "mock this up before building" |
| fudge:ui-prototype | Builds a bounded runnable UI draft to test branching, navigation, persistence, or recovery before production. | "let me try this flow" or "prototype how save and resume should work" |
| fudge:layered-review | Reviews a PR or diff, then layers the findings — verdict, one-line list, drill-down detail — for Slack, GitHub, or an HTML report. | "review this and don't bury me in text" |
| fudge:decision-room | Cross-functional personas pressure-test a decision independently, then synthesize into one recommendation. | "should we build this" |
| fudge:design-system | Derives the requested tokens, style rules, component contracts, or visual specimens from a moodboard, screenshots, wireframe, or brief. Reuses the project's design source. | "define these tokens" or "make our product look like this" |
| fudge-design-for-recognition | Shapes UI information and interaction so people can find, understand, decide, and act, then checks the rendered result. | "make this interface easier to use" |
| fudge:test-plan | Builds a risk-based test case matrix for review, then optionally executes the approved cases and records observed results in HTML. | "what should I test here" |
| fudge:conventions | Sets up project-specific coding rules, audits a change for convention drift or gaps, and amends approved rules without repeating the full interview. | "check this change against our conventions" |
| fudge-unslop | Edits prose to cut generic AI phrasing and make it more direct and specific. | any writing task |

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
