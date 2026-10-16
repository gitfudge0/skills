# Report composition

`../assets/example-report.src.html` is the editable native-runtime example; `../assets/example-report.html` is its generated offline counterpart. Copy the source rather than editing packed runtime bytes.

## Shell

Use `html lang`, UTF-8, viewport, a short document title, canonical `htmlplan.css` and deferred `htmlplan.js`. The source example links checkout assets at `../../../plan/runtime/`; installed runtime resolution is in the parent guide.

Place the title and result in `header`, followed by `p.meta` source/date/coverage information. Put one `doc-plan open="0"` in `main`. Each `doc-claim id="stable-id"` starts with a short claim in `p`. Nest supporting claims beneath it, preserving stable IDs across refreshes. Use auxiliary claims (`aux="method"`, for example) for methodology that is separate from conclusions.

## Evidence and decisions

Choose exhibits that prove the claim: `doc-code` for recorded text/code, `doc-flow` for flows, `doc-schema` for structure, `doc-quote` for attributed source text, and `doc-shot`/`doc-mock` for visual evidence. Plain tables can sit inside a claim when row/column comparison is the evidence. `doc-note` holds explanation beside that exhibit. Use the runtime's own components rather than adding report-specific cards, filters or slide navigation.

`span.pill` gives status with explicit text: neutral for information, `green` for completed/passed, `amber` for caution/pending and `red` for failed/blocking. The word carries meaning as well as color. Keep uncertainty labels visible while claims are closed.

Preserve recorded text as inert content. Escape prose/attributes. For `doc-code`, use `script type="text/plain"`; when text contains a closing script tag, use HTML-escaped `textarea class="src"` instead. Never execute report evidence as JavaScript. Avoid external resource dependencies in offline output.

When a genuine decision is requested, place `doc-ask id="stable-id"` at the claim it changes, with named native controls and a recommendation where supported by evidence. Leave settled decisions as recorded prose. Native comments and the copied response collect feedback without modifying the report's source of truth.

## Generation and fidelity

Regenerate the example from the source checkout:

```sh
node plan/runtime/pack.mjs shared/report-deck/assets/example-report.src.html -o shared/report-deck/assets/example-report.html
```

Keep the shared runtime's spacing, fonts, parent rows, contents rail, theme control, comments and response sheet. Additional styling belongs only inside a product mock exhibit. Verify the source and packed report preserve IDs, citations, statuses and evidence; packer warnings are suggestions unless they expose a real rendering or content error.
