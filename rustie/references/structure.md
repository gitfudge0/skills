# Project Structure & Modularity

## The path to the Modular Monolith

Most projects start as a monolithic `main.rs` that accumulates hundreds of lines.
That single binary is often the *correct* starting point — it prioritizes a working
system over premature abstraction. The problem is unchecked growth: tight coupling,
merge conflicts, and unreadable code.

The recommended trajectory is to move to a **Modular Monolith** *before* ever
considering distributed microservices. Every boundary a distributed system adds —
HTTP hops, message brokers, serialization layers — makes the system harder to debug
and monitor. Process isolation buys crash containment, but that's unnecessary
overhead for most applications. Rust's module system plus Cargo workspaces give you
the encapsulation benefits of microservices while keeping the simplicity of a single
compilation unit and binary.

Refactoring order as complexity grows:
1. Extract distinct domains into separate files/directories via `mod` declarations.
2. As domains deepen, extract them into separate local crates under one Cargo workspace.

## Cargo workspaces

A workspace groups related crates in one repository, sharing a unified `Cargo.lock`
and `target/` directory. This guarantees unified dependency resolution — every
sub-crate uses the exact same version of heavy deps like `tokio` or `serde` —
preventing version conflicts and reducing binary bloat.

**Keep the workspace flat, not deeply nested.** Large projects like `rust-analyzer`
show flat structures are far more maintainable: better visibility, simpler dependency
management.

Dependency strategy: put shared core types, DB utilities, and infrastructure adapters
in dedicated crates (e.g. `shared_types`, `db_utils`). Application/API-gateway crates
import these internal packages via relative path dependencies. This isolation speeds
the inner loop — editing one service crate doesn't force recompiling the whole
workspace.

### Structure comparison

| Feature | Single Crate Monolith | Cargo Workspace (Modular Monolith) | Distributed Microservices |
|---|---|---|---|
| Compilation speed | Slows as codebase grows; recompiles all domain logic | Optimized — incremental compilation rebuilds only modified crates | Separate build pipelines/CI per service |
| Dependency management | Simple, one `Cargo.toml` | Centralized at workspace root, shared versions | Fragmented; strict cross-repo version sync |
| Testing isolation | Unit tests co-located; integration tests coupled | Excellent — test crates in isolation (`cargo test -p crate_name`) | Complex; staging envs, network mocking, API contracts |
| Deployment | Single executable | Single executable, optimizable via LTO | Multiple containers needing orchestration (e.g. Kubernetes) |

## Module visibility & API ergonomics

**Anti-pattern:** pervasive `pub`. Exposing all internals breaks module boundaries
and produces spaghetti where unrelated domains couple tightly.

**Default to private.** Explicitly choose exposure with `pub(crate)` or `pub(super)`
to restrict access to the workspace or module boundary.

**Flatten public APIs with `pub use`.** As internal modules nest deeply, imports get
cumbersome. Strategic `pub use` re-exports at a module's top level decouple the
internal file hierarchy from the external API contract — you can refactor file
layout without breaking downstream consumers.
