# Design experiment

Internal capability: enter through the owning public skill and retain the caller's scope. Resolve package addresses through `shared/locate.md`.

Answer a bounded interaction, feasibility, or performance question with a runnable experiment. Name the decision, the observation that would change it, and the smallest experiment that can produce that observation. Use realistic inputs and record their provenance alongside any mocked behavior.

Start with the requested variants and the cases needed to distinguish them. Expand the experiment only when the caller asks or additional evidence could change the decision. Stop once the requested scope is covered and the evidence supports a conclusion at the stated level of confidence.

## Build and observe

1. Resolve an isolated artifact path with `shared/artifacts.md` (default category `prototype` for a technical experiment). Honor an explicit caller destination. Use an unused path for a new experiment and update an existing experiment in place when the caller requests a revision. Label the artifact exploratory and contain its state, dependencies, and simulated services. Keep production files and lockfiles untouched.
2. Use the experiment that fits the question:
   - **Interaction:** follow `references/modules/ui-prototype/guide.md` for path reservation, runnable transitions, state and reset, relevant recovery branches, and rendered inspection. Use `references/modules/ux-research/guide.md` when the decision depends on what people understand or do.
   - **API or algorithm:** build the smallest harness that exercises the disputed contract against representative inputs. Include a meaningful boundary or failure where it could change the decision. Capture actual results and errors. Identify which behaviors are implemented by fixtures or mocks and which were observed against the real dependency.
   - **Performance:** follow the performance link in `references/modules/engineering/guide.md` for workload, correctness, method, and variability. Use `references/modules/verification/guide.md` for performance evidence. Match comparisons to the feasibility question and keep the experiment separate from a production optimization run.
3. Run the artifact and inspect the decisive cases. Record inputs, outputs, and limits so the outcome can be reproduced. Give exact run, reset, and cleanup instructions. Track task-owned processes and stop them after verification unless the caller requests a running preview.

Return the artifact path, what the experiment answered, observed results, and the limits of the evidence. Keep the default delivery exploratory. Production promotion uses a separately scoped implementation through `fudge:ship`.
