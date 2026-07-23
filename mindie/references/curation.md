# Curation — turning source material into a faithful mindmap

The goal of a mindie map is comprehension of the **whole** source. A reader who
explores the finished map should come away understanding what the material
covers, how its parts relate, and what each part says — without having to open
the original. Curation is therefore an act of *faithful compression*, not
highlight-picking. Dropping a section because it didn't fit a tidy branch count
is a failure, not a simplification.

## The core tension

Two failure modes sit on either side of good curation:

- **Lossy:** you pick a few themes and quietly discard the rest. The map looks
  clean but misrepresents the source by omission.
- **Flat dump:** you turn every sentence into a node. Nothing is lost, but the
  structure teaches nothing and the map is unreadable.

Good curation covers everything that carries meaning while *organizing* it so
the hierarchy itself explains the material. Aim for total coverage of ideas,
not total coverage of words.

## Method

Work top-down, in passes.

**Pass 1 — Find the spine.** Read (or skim, if long) for the source's own
structure. Most material already has one: chapters, argument steps, a
chronology, a taxonomy, problem→solution, cause→effect. The root is the single
subject. The top branches are the major divisions of the source. If the source
has explicit sections, start from those.

**Pass 2 — Account for every meaningful unit.** Go back through and make sure
each substantive idea in the source lands *somewhere* in the tree. When a
branch is accumulating too many children (see below), that's the signal to
introduce an intermediate node that groups them — not to cut them. The tree
grows a layer rather than losing content.

**Pass 3 — Push detail into panels, not extra nodes.** A node's `detail`
(summary + points) can hold several related facts without spawning child nodes.
Use this to keep the visible tree legible while still capturing specifics. A
branch's own `detail.points` is the right home for a list the source presents as
a list (e.g. "the nine rules"), rather than nine sibling nodes — unless an item
is important enough to deserve its own expandable node with its own detail.

**Pass 4 — Check coverage against the source.** Before rendering, mentally walk
the source section by section and confirm each is represented. If you can point
to a paragraph or idea that has no home in the tree, the tree isn't done.

## Shape guidelines (defaults, not hard rules)

These keep maps readable. Bend them when faithful coverage requires it — a
dense source legitimately needs more nodes than a light one.

- **One clear center.** Root = the single subject. Its `detail` states the
  thesis or scope in a sentence or two.
- **Top branches: usually 4–8.** These are the source's major divisions. If the
  material genuinely has more top-level parts, it's better to have 9 clear
  branches than to force unrelated things together. If it has fewer, don't pad.
- **Depth: typically 3 levels, deeper when the material is deep.** Root →
  branch → leaf handles most sources. Go to 4 levels when a branch has real
  internal structure worth showing. Don't nest for its own sake.
- **Branch children: a handful each.** When a node exceeds ~6–7 children,
  introduce a grouping layer or move some detail into panels. Crowding is a
  restructuring signal.
- **Labels are short** — a few words, ideally one line. Substance lives in
  `detail`, never in a long label.
- **Most non-trivial nodes carry `detail`.** A `summary` of 1–3 sentences, plus
  `points` when the node has several sub-ideas that don't each merit a node.
  Pure structural/grouping nodes can carry a short summary or none.

## Fidelity rules

- **Represent, don't editorialize.** Summaries reflect what the source says. If
  the source argues a position, the map presents it as the source's claim, not
  as fact. Don't inject outside information unless the user asked you to be the
  source (a topic with no document).
- **Preserve the source's own framing and vocabulary** where it's meaningful
  (named concepts, key terms, the author's categories). A reader should
  recognize the map as *this* source, not a generic take on the topic.
- **Keep proportions honest.** A theme the source spends half its length on
  shouldn't get the same weight as an aside. More important themes get richer
  subtrees and fuller detail.
- **Quotes:** paraphrase into your own words. If a specific short phrase from the
  source is genuinely important, a brief quoted phrase is fine, but the map is a
  summary artifact — it should not reproduce long passages.

## `tag` conventions

`tag` is the one- or two-word pill shown atop each reading panel. It labels the
*kind* of node so the reader orients quickly. Pick tags that reflect the
source's structure — e.g. for an argument: "Claim", "Evidence", "Objection";
for a process: "Step", "Input", "Risk"; for a book: "Theme", "Rule", "Example".
Consistent tags across siblings make the map feel coherent.

## Worked intuition

For the *Ikigai* book summary (see `examples/ikigai.json`): the root is the
concept itself with the four-circle thesis in its detail. The top branches mirror
the summary's own sections — what ikigai is, the rules, avoiding stress, flow,
slow living, and the centenarians' closing advice. The long lists the book gives
(the nine rules, the elders' sayings) live as `points` inside their branch's
detail, while the few ideas worth isolating (e.g. "eat to 80%", "one thing at a
time") become their own leaf nodes with their own panels. Every section of the
summary is represented; nothing is dropped; the tree's shape retraces the book's
argument.
