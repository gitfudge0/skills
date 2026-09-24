# High-fidelity conversion

Use this route when the user wants an existing wireframe, sketch, or low-fidelity screen translated into high-fidelity UI. Identify which frames or flow are in scope. A request for one screen does not authorize converting its entire board or building a full component library.

## Preserve the source

For a faithful conversion, keep the selected source's information hierarchy, labels, actions, state intent, and navigation connections. Preserve frame IDs and order where they are part of the deliverable. Compare all frames only when the user requested the whole board. If the source is missing a decision needed to render the result, make a visible assumption or ask when the choice would materially change the flow.

A source wireframe is needed to promise wireframe parity. If none exists, an original high-fidelity concept may still be useful when that is within the user's request; label it as a proposal, not a conversion. Do not force the user through a separate full low-fidelity board solely to make a high-fidelity draft.

## Render the selected scope

Use the project's existing tokens and component patterns where available. Define only missing values or patterns needed for the selected screens. Unless the request is itself a product deliverable with an established project location, write the rendered screens or board under this skill's Output location (`.fudge/<branch>/design-system/`) — it is a review artifact, not a new source of truth. Include states or responsive layouts that the user requested or that are needed to make the selected flow understandable. Content and visual stand-ins should represent the product credibly; mark invented copy, imagery, or data when they could be mistaken for approved material. Use approved assets when available instead of imposing a blanket ban on external imagery.

If the output is a self-contained HTML artifact, it may embed a copy of token definitions. Identify the authoritative source and compare the copy against it. Verify that styles meant to consume tokens do not introduce untracked shared colors. There is no universal raw-hex grep over the HTML: token definitions, swatch labels, and explanatory text can legitimately contain color literals.

## Check the conversion

Compare the selected source and output for the elements the task promises to preserve: frame IDs, labels, action text, order, and connections. Use structure-aware inspection or a manual comparison; counting occurrences of `frame-id` can miscount attributes, code, and references. Review the rendered result for overflow, illegible contrast, and invented stand-ins. Report the compared scope and unresolved assumptions.
