# Rust GUI Development & the iced Framework

## Ecosystem overview

Choice of framework depends on deployment target, architecture, and performance.

| Framework | Paradigm | Primary use | Key characteristics |
|---|---|---|---|
| Tauri | Webview backend (HTML/CSS/JS frontend, Rust backend) | Lightweight desktop apps | Tiny binaries vs Electron; reuses web frontend skills with Rust for system perf |
| egui | Immediate Mode GUI | Tooling, game engines, debug UIs | Highly performant; UI redrawn every frame, no retained state; great embedded in `wgpu`/Bevy pipelines |
| Slint | Declarative UI language | Embedded, microcontrollers, desktop | Proprietary markup compiled to Rust; commercial backing; strong in resource-constrained IoT |
| iced | Retained mode / Elm Architecture | Cross-platform native desktop | Type-safe functional reactivity; built-in rendering via `wgpu`/`tiny-skia`; aggressive state/view decoupling |
| GTK-rs | Bindings to C-based GTK | Linux-first desktop | Mature, deep GNOME integration; relies on FFI and OOP paradigms |

For native, pure-Rust GUI development, **`iced`** is the premier choice. Its stability
and performance are validated by System76, who use it as the rendering engine for the
entire COSMIC Desktop Environment on Pop!_OS.

## The Elm Architecture (MVU)

`iced` rejects callback-driven OOP GUI models (Qt/GTK) for **The Elm Architecture
(TEA)**, a.k.a. Model-View-Update. Its strict unidirectional data flow harmonizes with
Rust's ownership and borrow-checking. Four decoupled concepts:

- **State (Model):** the single source of truth — a struct holding the app's data
  (counters, text buffers, loaded network data).
- **Messages:** an `enum` enumerating every possible user interaction or system event
  (`Message::IncrementPressed`, `Message::NetworkResponse(Data)`).
- **Update logic:** `fn update(&mut self, message: Message)` — the *sole* mutator of
  state. Processes a message, mutates state, optionally returns async commands.
- **View logic:** `fn view(&self) -> Element<Message>` — a *pure* function turning
  immutable state into widgets. Widgets emit `Message` variants on interaction,
  feeding back into update.

Because `view` holds only `&self`, UI components can't mutate data behind the scenes —
eliminating the whole class of state-desync bugs where a visual toggle disagrees with
the underlying boolean.

## Layouts & sizing

No global CSS. `iced` uses a compositional, flexbox-inspired model: build UIs with
`row!`, `column!`, and `container`. Widgets size via the `Length` type:

- `Length::Shrink` — collapse to intrinsic minimum size.
- `Length::Fill` — expand to consume all available space along the axis.
- Fixed numerical lengths are also allowed.

Nest `row!`/`column!` and apply `spacing`/`padding` via the builder pattern for
responsive native layouts. Theming is explicit: pass styling functions directly to
widgets; they evaluate against the active `Theme` (e.g. `Theme::Light`/`Theme::Dark`)
to derive palettes dynamically.

## Scaling: nested component mapping

Pitfall: letting the global `State` struct and `Message` enum grow into monoliths —
hundreds of variants in one `update` match destroys readability.

The fix is `Element::map`. Encapsulate complex UI into isolated child components, each
with its own local `State`, `Message`, `update`, and `view`. The parent's root enum
wraps child messages:

```rust
pub enum AppMessage {
    Settings(settings_panel::Message),
    Editor(editor::Message),
}
```

The child's `view` returns `Element<settings_panel::Message>`, but the parent must
return `Element<AppMessage>`, so the parent maps:

```rust
// Inside the parent view function
let settings_view = self.settings_panel
    .view()
    .map(AppMessage::Settings); // wraps child message into parent enum
```

In `update`, the parent matches `AppMessage::Settings(msg)` and delegates via
`self.settings_panel.update(msg)`. This fractal composition scales `iced` apps
indefinitely into localized, testable silos.

## Async concurrency & background subscriptions

The GUI main thread must stay responsive — heavy computation or blocking I/O on it
freezes the app. `iced` handles concurrency without manual thread handles or wrapping
UI state in `Mutex`.

- **One-shot async work** (e.g. an HTTP request): `update` returns a `Task` (`Command`
  in older versions). The runtime offloads the future to a background pool; on
  completion it resolves into a new `Message` placed back into the event loop for
  `update`.
- **Continuous streams** (serial port, WebSocket, timer tick): use the `Subscription`
  API. Subscriptions are re-evaluated after every state change, so the GUI can open/
  close background processes based on current context.

**Bidirectional background worker** via `Subscription::run`:
1. The subscription creates an async stream that initializes an `mpsc::channel`
   (multi-producer, single-consumer).
2. The worker immediately yields the `Sender` half back to the GUI via a setup message.
3. The GUI stores the `Sender` in its state and can push commands down the channel to
   the worker.
4. Concurrently the worker listens to events and yields output messages back up.

This isolates I/O from the rendering pipeline while keeping a thread-safe,
message-passing model aligned with Rust's safety guarantees.

## Production case study: COSMIC

System76 migrated off C-based GTK, building a customized widget library
(`libcosmic`) atop `iced` for a memory-safe, performant compositor and app suite.
For a scalable blueprint, study `cosmic-app-template` — it demonstrates production
layouts with localization (i18n), navigation bars, and cross-platform dual-install
support. COSMIC Terminal and COSMIC Files show Rust + Elm handling complex text
shaping, GPU rendering, and fast filesystem indexing without sacrificing
responsiveness.
