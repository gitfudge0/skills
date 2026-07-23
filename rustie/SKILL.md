---
name: rustie
description: Architect, structure, and harden production-grade Rust applications following idiomatic best practices. Use this skill whenever the user is designing, refactoring, or reviewing a Rust codebase's structure — including questions about project layout, Cargo workspaces, the modular monolith vs microservices decision, domain-driven patterns (Hexagonal/Ports-and-Adapters, Onion, Clean Architecture), the Typestate pattern, dependency injection, configuration management (figment, config-rs, conf), error handling (thiserror vs anyhow, eyre, snafu), observability/tracing, Clippy linting and CI enforcement, or building GUIs with iced (Elm/MVU architecture, layouts, component scaling, async subscriptions). Trigger it even when the user just says things like "how should I structure my Rust project", "should I split this into crates", "how do I handle errors/config/logging in Rust", or "help me build a Rust desktop app" — anytime idiomatic Rust architecture guidance helps, even without a named pattern.
---

# Production-Grade Rust Architecture

This skill provides opinionated, idiomatic guidance for taking Rust code from a
single `main.rs` to a maintainable, observable, production-ready application. Use
it when making structural or infrastructure decisions, not for basic syntax or
borrow-checker questions.

## Core philosophy

Lean on the compiler. The strength of production Rust is shifting validation from
runtime to compile time: encode invariants in the type system, default to private
visibility, and let strict tooling (Clippy) enforce architectural rules in CI.
Prefer working, simple systems over premature abstraction — start monolithic and
extract structure only when growth demands it.

## How to use this skill

Identify which area(s) the user's question touches and read the matching reference
file(s) before answering. The references contain the detailed rules, code patterns,
and trade-off tables. Don't dump a whole reference at the user — pull the specific
guidance that answers their question and explain the reasoning.

| User's topic                                                                                                                         | Read                                  |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| Project layout, modules, Cargo workspaces, monolith vs microservices, `pub` visibility, re-exports                                   | `references/structure.md`             |
| Hexagonal / Onion / Clean Architecture, DTOs, dependency injection, the Typestate pattern                                            | `references/architecture-patterns.md` |
| Config management (figment/config-rs/conf), error handling (thiserror/anyhow/eyre/snafu), observability & tracing                    | `references/infrastructure.md`        |
| Clippy config, banning `unwrap`/`expect`, `clippy.toml` disallowed methods, input validation, `unsafe` discipline                    | `references/quality-and-security.md`  |
| GUI frameworks overview, iced, the Elm/MVU architecture, layouts, component scaling with `Element::map`, async `Task`/`Subscription` | `references/gui-iced.md`              |

Several references often apply to one question (e.g. "how do I structure a new
Rust backend" touches structure, architecture-patterns, and infrastructure). Read
all that are relevant.

## Quick-reference guardrails

Apply these defaults unless the user's situation argues otherwise:

- **Start with a modular monolith**, not microservices. Reach for a Cargo
  workspace (flat, not deeply nested) before distributing across processes.
- **Default to private visibility.** Use `pub(crate)`/`pub(super)` deliberately;
  flatten public APIs with `pub use` re-exports.
- **Libraries use `thiserror`; application binaries use `anyhow`** (or `eyre`).
- **Use `tracing`, not `log`**, for anything async.
- **Ban `unwrap()`/`expect()` in production paths** via Clippy lints in CI.
- **Model states as types** (Typestate) when illegal state transitions are a risk.
- **For native pure-Rust GUIs, reach for `iced`** and follow the Elm/MVU pattern.
