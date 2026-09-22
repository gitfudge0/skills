# Optional issue and PR workflows

Read this only when the run selected issue tracking, a PR endpoint, or release/deploy. These choices are independent of the test-case gate. They do not permit product or test code before matrix approval.

## Issue tracking

Issue mode is off by default. Select it explicitly and record the tracker, project, and existing issue or authorized new-issue destination. A supplied issue link is context, not permission to edit it. When selected, create or link the scoped work item and update it at meaningful milestones: approved behavior/test cases, implementation verified, PR opened, review or integration complete, and an actionable blocker. Keep updates factual and concise, with artifact or PR links where accessible. Do not post every internal iteration or close a larger release issue because one feature finished. If a tracker field, audience, or ownership is unclear, ask before changing it; log a failed update without pretending it succeeded.

## PR lifecycle

`verified locally` needs no branch, commit, push, or PR. `PR opened` authorizes the in-scope branch, commit, push, and PR creation needed for this work item; it ends with a live PR link and local verification evidence, while pending remote checks are reported as pending. `PR integrated` additionally authorizes following remote checks and review, addressing feedback, seeking required approval, and merging only when the host's rules and the selected destination allow it. Record the target branch and merge method if they matter; ask instead of guessing a consequential choice. Never self-approve, bypass branch protection, or merge with failing required checks. A reviewer's requested behavior change returns to the test-case gate before related code changes.

Use the repository's configured provider and available connector or CLI. Keep commits limited to run-owned files; inspect staged content before each commit so a dirty worktree cannot drag in user changes. Push only the run branch. Once open, track the PR through checks and review as far as the selected endpoint requires; respond to actionable feedback, delegate in-scope fixes, rerun local gates, push updates, and recheck remote status. If approval, credentials, CI, or policy blocks integration, leave the run open with the exact blocker and PR link. Do not convert a selected `PR opened` endpoint into an automatic merge.

Release/deploy is a separate explicit endpoint. Establish its target and prerequisites, then use the project's release/deployment instructions and checks. A feature may be integrated into a larger release and stop there; do not cut, tag, deploy, or announce a release merely because its feature run is complete. Stop before any irreversible or ambiguous production operation that the selected scope did not settle, and report what remains.
