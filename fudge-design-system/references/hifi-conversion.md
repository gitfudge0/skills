# Phase 4 — Hi-fi conversion

Input: the low-fi wireframe board + `DESIGN.html` tokens + `COMPONENTS.html` patterns. Output: `screens.html` at the project root.

A low-fi design is a **precondition**, not an option. Search the project for one (wireframe HTML board, sketches, screenshots) before doing anything. No low-fi found → stop and ask the user for one, or offer to create a low-fi board as its own step and get it approved first. Never generate hi-fi screens straight from tokens — there would be nothing to verify parity against.

The job is a **conversion, not a redesign**. The wireframe already settled flow, structure and naming; this phase settles only how it looks. Every improvement you are tempted to make to the flow is a separate conversation with the user.

## Parity rules

Reproduce the board 1:1:

| Wireframe element | In `screens.html` |
|---|---|
| Section headings and their letters (A, B, C…) | Same letters, same names, same sub-captions |
| Row labels ("Row A-main — the happy path") | Same labels, same wording |
| Frames | Same count, same IDs, same names, same descriptions, same order |
| Connectors | Same arrows, **same action labels** ("tap Next", "grant access in system picker") |
| Reference frames (a frame drawn elsewhere, pointed at) | Stay reference cards — do not redraw them as full frames; that breaks the count |
| Sticky notes | Same notes, same content |
| Pan/zoom chrome, HUD, legend | Present and functional |

Frame count parity is checkable and therefore checked:

```bash
grep -c 'frame-id' mock.html screens.html   # must match
```

Unequal counts means a frame was dropped, merged, or a reference card was promoted. Fix the file, not the count.

## Rendering each screen

Each frame's interior is built from Phase 3 component patterns styled with Phase 1 tokens — the same class names as `COMPONENTS.html` where they apply. A frame is a device-shaped viewport containing real component markup, not a screenshot and not a redrawn box.

Board chrome (frame captions, IDs, connectors, sticky notes, HUD) is *also* styled with the tokens — `--size-caption`, `--color-text-secondary`, `--z-sticky` and friends. The board is part of the artefact, not a wrapper around it.

## Stand-ins for placeholders

The wireframe's hatched rectangles and "image here" boxes become **token-built stand-ins**:

- Book covers, avatars, hero art → gradients built from the brand/accent ramps.
- Charts, sparklines → token-coloured SVG or CSS shapes.
- Icons → inline SVG using `currentColor`.

Never a raw hex, never an external image, never a remote font beyond the Google Fonts link. If a stand-in needs a colour that isn't a token, the token set is short — add it in `DESIGN.md`/`DESIGN.html` first.

Stand-ins are **invented content**. Collect them as you go and flag the list to the user for a visual pass: they are the places where you guessed at something the wireframe never specified, and they are the most likely thing to be wrong.

## Gates — run by the orchestrator

A worker's claim that these pass is not evidence. Run them and report numbers.

```bash
# 1. frame parity
grep -c 'frame-id' mock.html screens.html

# 2. zero raw hex outside the token block
awk '/^:root \{/{inblock=1} inblock&&/^\}/{inblock=0;next} !inblock' screens.html \
  | grep -nE '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\('

# 3. token block identical to DESIGN.html
diff <(sed -n '/^:root {/,/^}/p' DESIGN.html) <(sed -n '/^:root {/,/^}/p' screens.html)
```

Gate 2 has one legitimate exception class: nothing. Alpha variants belong in the token block as their own tokens, not inline.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Improving" the flow while converting | Convert only. Raise flow changes separately. |
| Reference cards redrawn as full frames | Keep them as cards; parity depends on it. |
| Connector labels paraphrased | Copy the wireframe's exact wording. |
| Board chrome hard-coded greys | Chrome uses tokens too. |
| Stand-ins shipped silently | List every one for the user's visual pass. |
