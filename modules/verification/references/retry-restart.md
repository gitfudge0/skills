# Verify retry and restart behavior

Use when changes affect durable side effects such as jobs, installers, migrations, exports, or deliveries and rerun/recovery is a relevant risk. Adapted from [make operations idempotent](https://github.com/cursor/plugins/tree/main/pstack/skills/principle-make-operations-idempotent).

Identify operation identity, persisted progress, duplicate suppression, side effects, and the intended completion/recovery contract. Select meaningful interruption boundaries: for example after persisting progress but before recording completion, or after one item in a batch. Use the existing harness or isolated local fixtures to exercise partial failure, restart/rerun with the same identity, and duplicate completed execution where relevant.

Assert persisted outcomes, effect counts, and recovery state, including preserved unrelated data/resources and surfaced errors. An identical response alone does not prove one durable effect. Verify valid new operation identities still proceed. Avoid destructive live experiments and an exhaustive interruption matrix by habit; select boundaries that can independently violate the changed contract. If interruption cannot be exercised, report the unverified recovery boundary rather than calling restart behavior passed.
