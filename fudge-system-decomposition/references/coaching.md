# Coaching protocol

Load only for explicit coaching or practice. Help the user learn the decomposition heuristics through their own attempt, using the current problem rather than a generic lecture.

Frame the goal and source-supported actors/systems, then choose a relevant architectural lens and invite the user to identify concerns. Withhold the complete answer during that attempt, while respecting any request to reveal it.

When stuck, scaffold with prompts: What must be true? Who owns this? What crosses a boundary? What happens before and after? What if this happens twice or succeeds halfway? How do we know it worked? If needed, offer concrete examples and let the user continue.

After the attempt, compare what they found, what you would add, why it matters, and the lens or heuristic that exposes it. Explore valid alternatives and their tradeoffs; do not force your design or score the user unless asked.

Keep a compact gap log of meaningful missed concerns, lenses, and reusable heuristics. Use [the optional gap-log template](../assets/gap-log-template.md) when a saved learning log is requested; otherwise keep the log in chat. Do not write a file merely because coaching is active.

Integrate practiced lenses into a usable decomposition with the same provenance and candidate-work standards as ordinary analysis. `skip` reveals the current lens and moves on. `mode: fast` or a request to save time switches immediately to doing the analysis; `mode: training` resumes coaching.
