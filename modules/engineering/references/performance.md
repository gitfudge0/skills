# Measured optimization

Read for requested measurable performance improvement. Adapted from poteto-mode's [hillclimb playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md).

Define the metric, representative workload, correctness constraints, useful target, and task time/cost boundary. Validate the measurement harness before optimizing: establish its sensitivity to a known relevant change and confirm it counts completed work and errors. Faster failures, dropped work, or a benchmark dominated by unrelated overhead are not improvements. Freeze the validated workload and measurement method during comparisons; if the harness must change, establish a new comparable baseline.

Record revision/environment, warm-up and caching behavior, sample meaning, repetitions, execution order, variability, and confounds under verification's performance evidence rules. Test one explanatory hypothesis at a time. For each attempt record hypothesis → task-owned delta → observed correctness/metric → keep or revert decision. Retain improvements only when correctness holds and measurements support the claim. Revert only attributable attempt changes, preserving user and other workers' work; use isolation where rollback ownership is unclear.

Stop at the agreed target or when the remaining likely benefit is outweighed by the task's time/cost limit. No minimum attempt count or obligation to manufacture a win. Record rejected attempts to prevent repeated work, and report an inconclusive result honestly. Do not change product behavior or broaden the task to improve the score.
