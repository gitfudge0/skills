# Architectural Patterns in Rust

## Choosing a domain-driven pattern

The goal is isolating core business logic from external I/O. Each pattern maps
differently onto Rust's traits and ownership.

| Pattern | Core mechanism | Suitability for Rust |
|---|---|---|
| Hexagonal (Ports & Adapters) | Abstract "Ports" at the boundary; pluggable "Adapters" implement them | Excellent. Traits are natural ports; structs implementing them are swappable adapters |
| Onion | Concentric dependency rings; domain at center, infrastructure outside | Good. Enforceable via strict module hierarchy and workspace crate visibility |
| Clean | Strict layers (Domain, Use Cases, Controllers, Presenters) under the Dependency Rule | Often excessive boilerplate if ported directly from OOP; needs heavy adaptation |

## Adapting Hexagonal / Clean to idiomatic Rust

**Hexagonal is highly synergistic with Rust.** The inner domain layer holds pure
business logic and stays agnostic of HTTP frameworks, DB drivers, and brokers. It
declares its needs as traits (Ports) — e.g. `OrderNotifier`, `UserRepository`. Outer
Adapters implement those traits, so you can swap a PostgreSQL store for an in-memory
test store without touching core logic.

**Avoid DTO over-indirection.** Clean Architecture as practiced in C#/Java leans on
Data Transfer Objects, producing near-identical structs (`CreateUserDTO`,
`CreateUserDomain`, `CreateUserDbEntity`) plus exhaustive `From`/`Into` mappings. In
idiomatic Rust this is usually an anti-pattern — the type system, ownership, and
zero-cost abstractions already give the guarantees that indirection was chasing.
Prefer a single struct carried across boundaries using derive macros like
`#[derive(Serialize, Deserialize, FromRow)]`. This minimizes allocations and
boilerplate and leans on the type system for correctness.

**Dependency injection:** eschew heavy reflective DI frameworks. Prefer standard
constructor injection with generics and trait bounds. When runtime flexibility is
needed — or when generic bounds get complex enough to "infect" the whole codebase —
use dynamic dispatch via trait objects (`Box<dyn Trait>`), trading a microscopic
perf cost for real architectural flexibility.

## The Typestate pattern

Typestate encodes an object's runtime state into its compile-time type, moving state
transition validation from runtime to the compiler. This makes illegal states
unrepresentable and surfaces mistakes in the IDE — autocomplete only offers methods
valid for the current state.

Conventional OOP tracks state in a runtime field (e.g. an `enum { Open, Closed }`)
and every method re-checks it, panicking or erroring on misuse. Typestate instead:

1. Models states as distinct zero-sized marker structs: `struct Open;`, `struct Closed;`
2. Makes the object generic over state: `Connection<State>`
3. Implements methods only for specific states — a `write` method exists only on
   `impl Connection<Open>`, so calling `write` on a `Connection<Closed>` won't compile.
4. Makes transitions consume `self` and return a new-typed instance:

```rust
impl Connection<Open> {
    pub fn close(self) -> Connection<Closed> {
        // The original `Connection<Open>` is consumed and dropped;
        // a new `Connection<Closed>` is returned.
        Connection { state: Closed, ..self }
    }
}
```

Because Rust's affine type system forbids using a value after it's moved, the old
`Connection<Open>` is destroyed — no accidental reuse of stale state.

**Boilerplate note:** manual Typestate needs `PhantomData` or single-item tuples to
satisfy the unused-type-parameter rule. Procedural-macro crates like
`typestate-builder` automate this, generating state-enforced builder patterns that
require fields be initialized in a specific sequence before instantiation.
