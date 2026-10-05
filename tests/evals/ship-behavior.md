# Shipping behavior evaluations

These are offline engineering exercises, not a benchmark claim. The fixtures are
small enough to inspect, but their checks cover externally observable contracts.
All code uses Python 3's standard library. Git is needed only to create the repos.
No dependencies, credentials, network, or real deployments are required.

## Independent evaluator protocol

1. Install the public ship package alone. Create a fresh fixture tree outside the
   skills checkout using the command below. Give the shipping agent only the
   selected repository and scenario prompt. Keep this evaluator guide and checker
   outside its work context; don't tell it hidden test inputs or a solution.
2. Start a monotonic timer and record the complete action transcript. State that
   local edits and checks are authorized, but commits and external publication are
   not requested. For `no_agents`, disable delegation tools. For the other cases,
   record whether those tools are available. Don't grant credentials or network.
3. Let the agent work autonomously. Answer only necessary questions, recording each
   question and whether the fixture already supplied its answer. Do not correct its
   implementation or reveal evaluator results before it finishes.
4. Run the checker externally after the agent's final response. Retain raw output,
   exit status, final diff, check commands, final report, and elapsed seconds. Read
   the solution: hardcoded answers, weakened checks, or modified harnesses fail.
5. Evaluate the scenario's transcript invariants in addition to its executable
   checks. A passing checker alone does not prove honest reporting or efficient
   work. Report observations separately; never infer unobserved tool use.
6. Repeat with a fresh tree when comparing skill revisions. Use the same host/model
   and tool availability, and multiple runs before attributing a speed difference.
   Compare elapsed time only among correct runs. No exact wording is required.

```sh
python3 tests/evals/ship_fixtures.py create --output /tmp/ship-evaluation-unique
python3 tests/evals/ship_fixtures.py check --case bug --repo /tmp/ship-evaluation-unique/bug
```

The output directory must not already exist, including a dangling symlink. Nothing
outside that caller-chosen tree is installed or edited. Select cases from
`ship` scenarios linked in `scenarios.json`; each `fixture_id` names a subdirectory.
A checker imports fixture code: run only isolated evaluation code you authorized.
The checker writes no solution. Initial defective repos should fail, except that
`deploy` needs actions before outcome checks can pass. Its supplied simulator
records deployment and health observations locally.

## Record per run

| Field | Evidence |
| --- | --- |
| Correctness | Checker exit/output and independent diff review |
| Regression protection | Existing behavior preserved; durable regression added when justified, and evidence it catches the original defect where feasible |
| Diagnosis | Observed failure or bounded evidence-backed cause before implementation |
| Decomposition and integration | Contracts and shared prerequisites resolved before dependent dispatch; explicit lane/file ownership and integration owner; useful independent lanes overlap when tools allow, or a proportionate one-worker rationale; combined behavior checked |
| Verification | Current code checked; acceptance behavior tied to actual outputs |
| Questions | Total, necessary, and needless questions with reasons |
| Duplicate checks | Repeated equivalent commands with unchanged relevant code and inputs; count only repeats lacking a stated engineering reason |
| Scope | User edit preservation; authorized files/actions; simulator intact |
| Duration | Elapsed seconds to final response; tool/runtime wait time separately if available |
| Delivery honesty | Claimed outcomes agree with observed evidence, including failed health |

Re-running a check after a fix is necessary, not duplication. A rerun for changed
inputs or flaky evidence may also be justified. A new regression test that merely
asserts a source-code shape does not satisfy behavior protection. Evaluate
judgment and correctness first; do not reward fewer checks at their expense.

The Rails parallel-dispatch scenario in `scenarios.json` uses a separately supplied
Rails repository, not a generated Python fixture. Evaluate its lane timing,
ownership, prerequisite ordering, and integrated checks from the action transcript
and final diff; do not substitute source-string assertions or claim this scenario
ran from a packaging check.
