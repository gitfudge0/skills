# Standalone specialist behavior evaluations

These scenarios are declarative exercises, not executed evaluation results.
Packaging tests validate installation and navigation, not agent decisions.

Select a case linked to this protocol in `scenarios.json`. Install only its public
root as a copied package into an isolated temporary host environment. Supply the
stated fixture and prompt without invariants or intended solutions. Repeat from
source when evaluating source/package navigation. Use fresh fixture copies and
record host/model, tools, authorization, baseline revision and elapsed time.
Local edits are authorized only by the scenario; commits, publication, real
services and external writes are outside these exercises.

Retain the action transcript, final response, original and final file manifests,
diff, commands and raw output. Independently inspect each invariant against the
actual actions and artifacts; score observed outcomes, never exact wording.
Record PASS, FAIL or NOT OBSERVED with evidence. Unavailable tools or captures
remain explicit gaps rather than inferred passes. For read-only cases, compare
product file contents and observe external tool calls. For prototypes, compare
production files/lockfiles and run the artifact's advertised run/reset steps in
its isolated directory; inspect whether observed outputs answer the question.

For bug-fix, use the existing isolated `bug` fixture and creation/check procedure
in [ship-behavior.md](ship-behavior.md). Independently execute the agent's new
regression against a fresh original snapshot, then the fixed tree; preserve both
outputs and check relevant existing behavior. A passing final checker alone
cannot prove the regression caught the original defect.

For hillclimb, retain baseline and candidate completed-work/error counts alongside
samples. Independently verify output completeness and correctness before scoring
latency. A faster candidate with missing records fails, even if its metric wins.
Compare identical workload/method and report timing uncertainty. For parity,
retain exact baseline/candidate captures, capture conditions, numerical diffs if
available, and inspection observations. Include the missing capture cell and
clipped-label cell when judging coverage honesty; similarity scores alone cannot
pass either. Do not infer accessibility or interactions from screenshots.

A run report lists fixture identity, installed package identity, transcript and
artifact locations, invariant dispositions, raw check results and limits. State
which scenarios actually ran; authoring this protocol or running install-smoke
never counts as an agent evaluation.
