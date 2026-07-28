# Infrastructure: Config, Errors, Observability

## Hierarchical configuration

Scalable apps need layered config: baseline defaults, environment-specific
TOML/JSON files, then environment-variable overrides (for injecting secrets).

| Crate | Key capabilities |
|---|---|
| `figment` | Most advanced layered config. Integrates with `serde` for typed extraction. Tracks value *provenance* — trace which file or env var supplied a value. Provides a `Jail` utility for sandboxed config testing. |
| `config-rs` | Widely adopted, straightforward merging of files + env vars. Maps nested struct fields from env vars via double underscore (`__`). |
| `conf` | Integrates tightly with `clap` for CLI args. Returns *all* validation errors at once rather than failing on the first missing key — great for debugging large deployments. |

Define a strongly typed `Settings` struct with `serde::Deserialize`, then load and
merge sources at startup. **Fail fast:** if an env var is misconfigured or a required
field is missing, panic immediately during bootstrap. This prevents catastrophic
failures that would otherwise surface deep in execution when a missing config is
first read.

## Idiomatic error handling

Rust uses `Result<T, E>` instead of exceptions, forcing explicit handling of failure.
Manually implementing `std::error::Error` and `std::fmt::Display` for every failure is
heavy boilerplate; two crates dominate.

**Guideline: libraries and core domain logic use `thiserror`; application binaries and
presentation layers use `anyhow`.**

- `thiserror` — procedural macros to generate custom error *enums*. Explicit variants
  (`DatabaseTimeout`, `InvalidCredentials`) give callers a strict API contract they can
  `match` on to run targeted recovery. Use for typed, recoverable errors.
- `anyhow` — a dynamic, opaque error type optimized for ergonomics. For failures you
  don't intend to recover from but just need to report: use `?` to bubble errors up
  while attaching rich, hierarchical context strings.

Two more for specialized needs:
- `eyre` — drop-in replacement for `anyhow` enabling custom report handlers with
  colorful, heavily formatted backtraces.
- `snafu` — context-driven domain errors, merging thiserror's typed nature with
  anyhow's contextual ergonomics for complex enterprise systems.

## Observability: logging → tracing

For **synchronous** apps, traditional logging (`log` + `env_logger`) is fine. `log`
emits flat, event-based string records at severity levels (ERROR/WARN/INFO/DEBUG/TRACE).

But modern Rust backends are almost always **async** on runtimes like `tokio`, where a
single OS thread interleaves many unrelated tasks. Flat log lines from different
requests become indistinguishably mixed — traditional logging fails here.

The community standard is the **`tracing`** ecosystem (maintained by the Tokio team):

- Introduces **spans** — structured, hierarchical contexts with a defined start/end.
- Annotate a function with `#[instrument]` to enter a span. Events emitted during
  execution — *even across `.await` points* where the task yields — automatically
  inherit the span's fields (`request_id`, `user_id`, etc.).
- **Subscriber architecture:** `tracing-subscriber` formats logs for the terminal;
  `tracing-opentelemetry` exports spans to Jaeger, Zipkin, or Datadog for distributed
  tracing, letting you visualize latency breakdowns across network calls, DB queries,
  and internal processing.
- **Backward compatible with `log`:** events from legacy dependencies are captured and
  wrapped in the active span automatically.
