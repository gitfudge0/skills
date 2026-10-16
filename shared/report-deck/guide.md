# Optional HTML reports with the plan runtime

Use this renderer for requested HTML reports or when a standalone visual deliverable serves the caller's task. Honor explicit chat, Markdown and document requests. Report content, evidence and authorization remain owned by the calling workflow; choosing HTML adds no required artifact or approval round.

The directory name remains `report-deck` for existing routes. Its UI is the actual plan runtime: nested numbered claims, contents navigation, native comments and copied responses, persisted light/dark theme, and print layout. Reports use the same interface as plans; they do not run the planning workflow.

## Runtime and output

Resolve the package root through `shared/locate.md`. In source, the canonical runtime is `plan/runtime/`. Every built root contains byte-identical `htmlplan.css`, `htmlplan.js` and `pack.mjs` in package-root `shared/report-deck/runtime/`, including roots with no plan dependency. These are generated package assets; maintain only the canonical source.

Read [composition and example](references/composition.md) before authoring. Copy `assets/example-report.src.html` to the caller's artifact destination, replace its fictional content, then pack with the resolved runtime:

```sh
# Source checkout
node plan/runtime/pack.mjs /absolute/output/report.src.html -o /absolute/output/report.html
# Installed package, from its root
node shared/report-deck/runtime/pack.mjs /absolute/output/report.src.html -o /absolute/output/report.html
```

The packer resolves canonical runtime filenames beside itself when copied template links no longer resolve. For an unpacked preview, adjust those links to the resolved runtime. Deliver packed HTML for offline use. Follow `shared/artifacts.md`; keep the caller's category and destination, or use `report-deck` when none is specified. Source and packed files belong to the same run.

## Content and feedback

Lead with the result, then organize evidence under stable claim IDs. Use native header/meta/pills, `doc-plan`, `doc-claim`, and exhibits. Preserve uncertainty, source citations and the caller's required fields. Use `doc-ask` only for a real unresolved user decision; reports need no manufactured questions. Comments and copied responses are feedback data, not updates to recorded evidence or authorization.

Keep the native runtime UI and theme/print behavior. Product mocks and screenshots retain their appearance inside exhibits. Report-specific presentation does not replace navigation, comments, themes or status components.

## Verify and export

Run the packer; resolve errors and assess warnings against the report's content contract. Planning suggestions such as five-claim budgets or a missing scope claim need not change a faithful report. Inspect packed output in a browser at desktop and narrow widths, both themes: open claims, follow contents links, add/reload a comment, and copy a response. Confirm IDs/evidence survived packing and runtime CSS/JS are inline. State unavailable visual checks.

Export PDF only when requested, using `scripts/html-to-pdf.sh` by its resolved path. It uses a local Chromium-family browser and the runtime's normal print pagination. `CHROME_BIN` selects a browser; `RENDER_MS` increases rendering time. Inspect resulting pages for clipped evidence, blank diagrams and broken tables. Page count depends on content, not claim count; there is no one-slide-per-page contract.
