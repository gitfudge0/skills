# Code Quality, Security & CI Automation

The compiler enforces memory safety; **`cargo clippy`** is the arbiter of idiomatic
correctness and performance. Maintaining quality across a team requires aggressive,
automated static analysis in CI.

## Elevating Clippy strictness

Clippy catches hundreds of anti-patterns by default. Enterprise apps raise strictness
via lint groups in `Cargo.toml` under `[lints.clippy]`.

**Prohibit `unwrap()` and `expect()` in production paths.** These panic immediately on
`Err`/`None`, causing catastrophic crashes. Set:

```toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
```

CI then fails any PR that bypasses safe error handling. If an engineer can prove an
invariant guaranteeing a value is present, they must explicitly opt out with
`#[allow(clippy::unwrap_used)]` plus a mandatory explanatory comment — forcing
intent-driven review.

## `clippy.toml` for architectural compliance

The `clippy.toml` file can ban specific types and methods workspace-wide via the
`disallowed-methods` array — a powerful lever for enforcing consistency.

- **Better filesystem errors:** `std::fs::read_to_string` returns opaque errors ("No
  such file or directory") without naming the file. Disallow `std::fs` methods and
  mandate the `fs_err` crate so every filesystem error includes the exact path,
  cutting debugging time.
- **Prevent test race conditions:** Rust runs tests concurrently by default. A test
  calling `std::env::set_current_dir` changes the working directory for the whole
  process, creating subtle races. Disallow it globally to force isolated temp
  directories or a process-isolated runner like `cargo-nextest`.

## Security & input sanitization

Rust prevents buffer overflows, null-pointer dereferences, and use-after-free — but
**not logical flaws**. Safe Rust stops memory corruption, not SQL injection or XSS.

- Treat all external data as hostile.
- Use the type system to enforce validation boundaries: parse inputs into strongly
  typed wrappers (e.g. `struct UserId(u32)`) rather than passing raw strings around.
- Minimize and heavily audit `unsafe` — it strips the compiler's guarantees and
  reintroduces the possibility of undefined behavior.
