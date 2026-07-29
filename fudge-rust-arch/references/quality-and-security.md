# Code Quality, Security & CI Tooling

The compiler enforces memory safety; **`cargo clippy`** is the arbiter of idiomatic
correctness and performance. Maintaining quality across a team requires aggressive,
automated static analysis in CI, plus a small, boring, well-chosen tool stack.

## Lint configuration lives in `Cargo.toml`

Since Rust 1.74, lints belong in the manifest — **not** in `#![deny(...)]` crate
attributes and **not** in `RUSTFLAGS` (which busts the build cache and breaks
`cargo` invocations that don't inherit the env). The consensus pattern:

```toml
# workspace root Cargo.toml
[workspace.lints.rust]
unsafe_code = "forbid"
missing_debug_implementations = "warn"

[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }   # priority -1 => later keys override
# curated allows — each needs a reason
module_name_repetitions = "allow" # domain types read better fully qualified
missing_errors_doc = "allow"      # thiserror variants are self-documenting
must_use_candidate = "allow"      # noise on internal APIs
# targeted denies on top of the group
unwrap_used = "deny"
expect_used = "deny"
```

```toml
# each member crate
[lints]
workspace = true
```

The `priority = -1` trick is load-bearing: group-level lints must be evaluated
before the individual overrides, otherwise the group re-enables what you allowed.

**Warn locally, deny in CI.** Keep levels at `warn` in the manifest so local
iteration isn't blocked, and run `cargo clippy --all-targets --all-features -- -D warnings`
in CI. Escaping a `deny` requires `#[allow(clippy::unwrap_used, reason = "...")]`
with an explanatory comment — forcing intent-driven review.

## Prohibit `unwrap()`/`expect()` in production paths

These panic immediately on `Err`/`None`, causing catastrophic crashes. Deny them
crate-wide and re-allow in tests:

```toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
```

Test modules get `#![cfg_attr(test, allow(clippy::unwrap_used))]` or a
`#[allow]` on the `mod tests` block.

## `clippy.toml` for architectural compliance

`clippy.toml` bans specific types and methods workspace-wide via
`disallowed-methods`/`disallowed-types` — a powerful lever for consistency.

- **Better filesystem errors:** `std::fs::read_to_string` returns opaque errors
  ("No such file or directory") without naming the file. Disallow `std::fs`
  methods and mandate `fs_err` so every error includes the exact path.
- **Prevent test race conditions:** disallow `std::env::set_current_dir` — it
  mutates process-global state and races with concurrent tests. Force isolated
  temp dirs or a process-isolated runner (`cargo-nextest`).

## Formatting

Use **stock rustfmt**. Team-specific style knobs are churn with no payoff; the
only setting worth pinning is the style edition:

```toml
# rustfmt.toml
style_edition = "2024"   # stable since Rust 1.85
```

- CI: `cargo fmt --all -- --check`.
- **Bare `rustfmt` assumes edition 2015** and chokes on modern syntax (async
  blocks, `dyn`). Always go through `cargo fmt`, or pass `--edition 2021`/`2024`
  explicitly when invoking `rustfmt` on individual files.

## Test running

**`cargo-nextest` is the default runner.** Process-per-test isolation (no shared
global state, a panic/abort kills one test not the run), much faster on large
suites, real retry support, and machine-readable output.

```toml
# .config/nextest.toml
[profile.ci]
fail-fast = false          # report every failure in one run
retries = 2
failure-output = "immediate-final"
[profile.ci.junit]
path = "junit.xml"

[[profile.ci.overrides]]
filter = "all()"
flaky-result = "fail"      # a test that only passes on retry still fails CI
```

**Nextest does not run doctests.** Always pair it:

```
cargo nextest run --profile ci --all-features
cargo test --doc --all-features
```

Adopt as needed, one line each:

- **insta** — snapshot testing; `cargo insta review` for interactive accept.
- **proptest** — property-based testing with shrinking (quickcheck is
  maintenance-mode; don't start new work there).
- **cargo-mutants** — mutation testing; run `cargo mutants --in-diff pr.diff` so
  PRs are scoped and fast rather than a multi-hour whole-repo sweep.
- **cargo-llvm-cov + nextest** (`cargo llvm-cov nextest`) — the coverage pairing;
  source-based instrumentation, accurate. tarpaulin is in decline.

## Dependency hygiene & supply chain

**`cargo-deny` is the superset tool** — it subsumes cargo-audit and cargo-license.

```toml
# deny.toml
[advisories]
# since 0.17 advisories are deny-by-default; `ignore` takes RUSTSEC ids
unmaintained = "workspace"     # only flag unmaintained crates you actually own a dep on
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unicode-3.0"]
[bans]
multiple-versions = "warn"     # noisy as deny; watch the trend
wildcards = "deny"
[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

- **cargo-machete** — fast unused-dependency scan, stable toolchain, good enough
  for CI. `cargo-udeps` is more exact but needs nightly and a full build.
- **typos-cli** — spelling in code, comments, and docs; near-zero false
  positives, runs in milliseconds. Config in `_typos.toml`.

## Git hooks

Use **lefthook**: a single static binary, parallel execution, YAML config, no
Python/venv bootstrap (unlike `pre-commit`) and no build-time hook injection
(unlike `cargo-husky`).

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    fmt:
      glob: "*.rs"
      run: cargo fmt --all -- --check
    typos:
      run: typos
```

**Hooks stay fast** — formatting and spelling only. Clippy, tests, and
cargo-deny belong in CI; a pre-commit hook that takes 40 seconds gets bypassed
with `--no-verify` and stops protecting anything.

## CI (GitHub Actions)

`actions-rs/*` is unmaintained and archived — do not use it. Current stack:

- **dtolnay/rust-toolchain@stable** (minimal, fast) or
  **actions-rust-lang/setup-rust-toolchain@v1** (reads `rust-toolchain.toml`,
  bundles caching).
- **Swatinem/rust-cache@v2** for build caching.
- **taiki-e/install-action@v2** for prebuilt tool binaries (nextest, llvm-cov,
  typos, cargo-deny) — seconds instead of a `cargo install` compile.
- **EmbarkStudios/cargo-deny-action@v2**.

**Pin the channel in `rust-toolchain.toml`** (`channel = "1.85"`, not `"stable"`)
so a new upstream release with new clippy lints can't turn CI red on an unrelated
PR; bump it deliberately.

```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rust-lang/setup-rust-toolchain@v1
        with: { components: rustfmt, clippy }
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-nextest,typos-cli,cargo-machete
      - run: cargo fmt --all -- --check
      - run: typos
      - run: cargo clippy --all-targets --all-features -- -D warnings
      - run: cargo nextest run --profile ci --all-features
      - run: cargo test --doc --all-features
      - run: cargo machete
  deny:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: EmbarkStudios/cargo-deny-action@v2
```

## Security & input sanitization

Rust prevents buffer overflows, null-pointer dereferences, and use-after-free — but
**not logical flaws**. Safe Rust stops memory corruption, not SQL injection or XSS.

- Treat all external data as hostile.
- Use the type system to enforce validation boundaries: parse inputs into strongly
  typed wrappers (e.g. `struct UserId(u32)`) rather than passing raw strings around.
- Minimize and heavily audit `unsafe` — it strips the compiler's guarantees and
  reintroduces the possibility of undefined behavior. `unsafe_code = "forbid"` in
  `[workspace.lints.rust]` where you can afford it.
</content>
</invoke>
