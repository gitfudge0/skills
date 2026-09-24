# Skills

A personal collection of agent skills. The default install exposes three root skills: `fudge:design`, `fudge:ship`, and `fudge:review`. Each root includes the specialist guidance it needs as internal references. The other skills below are available as optional, separately invokable installs.

| Skill | What it does | Reach for it when |
|---|---|---|
| fudge:ship | Takes one idea, issue, or story to a verified feature. UI guidance or a mock is used when needed; you approve the test case matrix before code. Issue updates and the PR cycle are optional. | "take this feature from idea to completion" |
| fudge:design | Routes UI work to concise guidance, a reviewable draft, reusable project rules, or a requested component build. Output and effort follow the decision and its risk. | "design this flow", "guide this UI build", or "build these components" |
| fudge:review | Reviews a PR or diff and reports findings as symptom, cause, and fix — verdict, one-line list, detail — in chat, Slack, GitHub, or HTML. Re-reviews after new commits. | "review this and don't bury me in text" |
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
| fudge:decision-room | Cross-functional personas pressure-test a decision independently, then synthesize into one recommendation. | "should we build this" |
| fudge:design-system | Derives the requested tokens, style rules, component contracts, or visual specimens from a moodboard, screenshots, wireframe, or brief. Reuses the project's design source. | "define these tokens" or "make our product look like this" |
| fudge-design-for-recognition | Shapes UI information and interaction so people can find, understand, decide, and act, then checks the rendered result. | "make this interface easier to use" |
| fudge:test-plan | Builds a risk-based test case matrix for review, then optionally executes the approved cases and records observed results in HTML. | "what should I test here" |
| fudge:conventions | Sets up project-specific coding rules, audits a change for convention drift or gaps, and amends approved rules without repeating the full interview. | "check this change against our conventions" |
| fudge-unslop | Edits prose to cut generic AI phrasing and make it more direct and specific. | any writing task |

## Output location

Skills write their run artifacts — reports, registers, run state, and other generated files — to `.fudge/<branch>/<skill>/` at the root of the current working tree, one directory per skill per branch. That directory is hidden from Git via `.git/info/exclude`, not `.gitignore`. Product changes (source code, tests, project docs, project skills) still go where the project keeps them.

## Install

Run `./install.sh` in a terminal. The installer asks one question at a time, then shows a review before writing anything. **Codex** and the three core skills (**design**, **ship**, **review**) start selected; the 18 individual skills start unselected. Symlink is the default method.

```text
Step 1 of 5  Where should Fudge work?       Agents
Step 2 of 5  Which core skills?            Design, Ship, Review
Step 3 of 5  Add individual skills?        Optional skill search
Step 4 of 5  How should skills be installed?  Symlink or Copy
Step 5 of 5  Review installation           Destinations and changes
```

Use Up/Down to move through answers and Space to select. Enter continues to the next question; on Review, Enter installs. Esc goes back one question, or cancels from the first question. Press `q` to cancel from a question. On Optional skills, `/` starts a search, Backspace edits it, and Enter leaves search so you can select a result. Back preserves earlier answers. Review shows the selected agents, skills, method, and new, update, current, and conflict counts. A conflict must be resolved or deselected before installation. A narrow terminal keeps the same question-by-question flow; unsupported terminals use plain prompts.

For scripts, select at least one agent with `-a`. A nonterminal install without `-a` fails before it builds or installs anything. With `-a` in a nonterminal, it prints the summary and proceeds without a prompt. In a supported terminal, flags such as `-a claude --copy` preselect the wizard's answers. The command flags retain their existing nonterminal behavior.

```bash
./install.sh install -a codex
./install.sh install -a codex --root design
./install.sh install -a codex --root review
./install.sh install -a codex --root design --root ship --root review \
  --skill accessible-ui --skill ui-mock
./install.sh install -a codex --no-roots --skill test-plan
./install.sh install -a codex --all
./install.sh install -a codex --copy
./install.sh list -a codex
./install.sh remove -a codex --all -y
```

`--root` and `--skill` are repeatable. `--skill` on its own adds individual skills to the three default roots; `--no-roots` selects individuals only. `--all` explicitly installs all three roots and every individual skill. `-y` skips terminal confirmation. Root packages are generated from the current source during installation and installed as `fudge-design`, `fudge-ship`, and `fudge-review`. Selecting a root never creates separate installs of its specialists. Use `--root review` to install review alone; `--skill review` is rejected because review is a root.

The installer updates symlinks and copies it previously created. Copies carry a `.fudge-installer` marker. An entry at the destination that the installer cannot identify as its own is reported as a conflict and left untouched. `remove` likewise removes only installer-owned entries; older unmarked manual copies must be removed manually.

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
