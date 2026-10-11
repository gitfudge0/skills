# Check the test oracle

Use when reviewing or changing tests. Adapted from [test behavior, not implementation](https://github.com/cursor/plugins/tree/main/pstack/skills/principle-test-behavior-not-implementation).

Name a realistic incorrect implementation that could still pass the test: returning a canned success, skipping persistence, dropping part of a batch, rejecting valid input, or asserting only the mock's configured return. Check that the assertion establishes the claimed observable behavior at an appropriate boundary, including important negative cases. Distinguish what a mock exercises from what requires a real integration or product observation.

When practical and safe, demonstrate a meaningful regression test fails against the original defect or an isolated representative broken variant and passes for the valid implementation. Preserve user work; do not mutate a shared production target or demand mutation infrastructure for every test. Static reasoning can expose a weak oracle but must not be called an executed mutation pass. Strengthen only material gaps for the changed contract, avoiding assertions tied to incidental structure and unnecessary mirror tests.
