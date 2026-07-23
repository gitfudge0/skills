# Curation — building a mindmap that includes ALL of the source

**The single most important rule of mindie: no idea from the source may be left
out of the map.** Skipping content is treated as a critical failure, not a
stylistic simplification — a reader relies on the map *instead of* the original,
so anything missing is lost to them entirely. When any other guideline in this
document (branch counts, tidiness, readability) conflicts with including a piece
of source content, **inclusion wins.** Always.

This does not mean a node per sentence. It means total coverage of *ideas*:
every claim, fact, example, rule, caveat, name, and number that carries meaning
must live somewhere in the tree — as a node label, a node summary, or a point in
a node's detail. Routine connective phrasing and pure filler can be compressed,
but if you are ever unsure whether something "counts," include it. The cost of
including a minor detail is a slightly fuller panel. The cost of dropping one is
permanent loss.

## The two failure modes

- **Lossy (the one that matters here):** you pick a few themes and let the rest
  fall away. The map looks clean but silently misrepresents the source. This is
  the failure mindie exists to prevent.
- **Flat dump:** you turn every sentence into its own node. Nothing is lost but
  the structure teaches nothing.

The resolution is never to drop content to avoid a dump — it is to *organize*:
group related ideas under intermediate nodes, and push fine detail into panels.
Coverage and readability are achieved by structure, not by subtraction.

## Method — build coverage in, then verify it

Curation is a build-then-prove loop. The verification step is mandatory, not
optional, because a mental "I think I got everything" pass is exactly how
omissions slip through.

**Step 1 — Segment the source into atomic units.** Before or while building the
tree, break the source into its smallest meaningful pieces — one idea, claim,
fact, or example per unit. Write them to a coverage file (see
`scripts/check_coverage.py` for the format), grouped by the source's sections.
This list is your ground truth for what must be covered. Do this even for
material that looks simple; the discipline is what catches the misses.

**Step 2 — Find the spine.** Identify the source's own structure — chapters,
argument steps, chronology, taxonomy, problem→solution. The root is the single
subject; the top branches are the source's major divisions. Starting from the
source's own sections makes full coverage far easier than inventing categories.

**Step 3 — Place every unit.** Build the tree so that each unit from Step 1
lands somewhere. Record where, by tagging each line in the coverage file with the
node id that carries it. When a branch starts accumulating too many children,
**add an intermediate grouping node — never cut.** The tree grows a layer rather
than losing content. A list the source presents as a list (e.g. "the nine
rules") belongs in a branch's `detail.points`, with the few most important items
promoted to their own leaf nodes.

**Step 4 — Run the coverage check and make it PASS.**

```bash
python3 scripts/check_coverage.py --coverage cov.txt --data map.json
```

Every unit must be either mapped to a real node id or explicitly marked
`[OMIT: reason]`. The script fails (non-zero) on any unaccounted unit or any
mapping to a nonexistent node. **Do not proceed to render until this passes.**

**Step 5 — Justify every omission.** The only content that may sit outside the
tree is content marked `[OMIT: reason]`, and OMIT is reserved for material that
is genuinely not part of the source's substance — navigation chrome, newsletter
widgets, an author's meta-remarks about writing the piece, boilerplate. If you
find yourself omitting an actual idea from the source, that is a coverage bug:
put it back. Review the omission list in the check output every time; each line
is content the reader will never see.

## Shape guidelines (all subordinate to completeness)

These keep maps readable. Apply them *only* in ways that preserve full coverage
— if a guideline would force you to drop content, break the guideline instead.

- **One clear center.** Root = the single subject; its `detail` states the
  thesis or scope.
- **Top branches: aim for 4–8, but never merge unrelated content or drop a
  section to hit that range.** A dense source may legitimately need 9 or 10
  branches. More branches is always better than lost content.
- **Depth: 3 levels is typical; go deeper whenever the material has more
  structure to hold.** Depth is a tool for coverage, not something to ration.
- **Branch children: when a node exceeds ~6–7 children, add a grouping layer or
  move detail into panels — do not trim.** Crowding is a restructuring signal,
  never a cutting signal.
- **Labels stay short**; substance lives in `detail`. A short label plus a rich
  panel lets one node carry a lot without clutter.
- **Every substantive node carries `detail`.** Use `summary` (1–3 sentences) for
  the idea and `points` for any sub-ideas that don't each need their own node.
  Panels are the main tool for holding detail without growing the visible tree —
  lean on them heavily to reconcile "include everything" with "stay readable."

## Fidelity rules (accuracy alongside completeness)

Completeness governs *what* is included; these govern *how* faithfully.

- **Represent, don't editorialize.** Summaries reflect what the source says. A
  source's argument is presented as its claim, not as fact. Don't add outside
  information unless the user asked you to be the source (a topic with no doc).
- **Preserve the source's framing and vocabulary** — named concepts, key terms,
  the author's own categories. The map should read as *this* source.
- **Keep proportions honest.** A theme the source dwells on gets a richer
  subtree than an aside — but "aside" still means "included," just more briefly.
- **Quotes:** paraphrase into your own words; a brief quoted phrase is fine when
  wording truly matters, but don't reproduce long passages.

## `tag` conventions

`tag` is the one- or two-word pill atop each reading panel, labeling the *kind*
of node (e.g. argument: "Claim"/"Evidence"/"Objection"; process:
"Step"/"Input"/"Risk"; book: "Theme"/"Rule"/"Example"). Consistent tags across
siblings make the map coherent.

## Worked example — Ikigai

See `examples/ikigai.json` (the map) and `examples/ikigai-coverage.txt` (its
coverage file). The coverage file lists 55 units from the source; 51 map to
nodes and 4 are explicitly omitted — and every omission is non-book chrome (the
Makkajai office intro, the blog-post framing, a Medium signup widget, the
author's closing remark), never an idea from the book itself. Running the
checker on it PASSes with zero unaccounted units. That is the standard every
mindie map must meet: run the check, drive unaccounted to zero, and be able to
defend each recorded omission out loud.
