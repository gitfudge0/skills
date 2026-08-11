#!/usr/bin/env python3
"""
Emit the token layers of a design system stylesheet from tokens.json.

Writes the custom-property layers in the order references/generation.md
fixes: tier 1, tier 2, theme overrides, print overrides, tier 3, density
overrides. The rest of the stylesheet — reset, type roles, component
classes, utilities — is hand-authored in the parts file and concatenated
by build.py, so it is deliberately not emitted here.

    python emit.py <tokens.json> -o <name>.tokens.css

`--format` switches the substrate the same tokens are written out in, for
a consuming project that is not plain CSS. CSS custom properties remain
the source of truth in every format: the adapters reference them, they
never resolve them to literals, because a literal is frozen at emit time
and no theme can ever reach it again.

    css       (default) the custom-property layers
    ts        a dependency-free TypeScript module — tree plus name map
    tailwind  a Tailwind v4 @theme block and a v3 theme.extend fragment
    shadcn    shadcn/ui's fixed slot vocabulary aliased onto our semantics
"""

import argparse
import json
import pathlib
import re
import sys

TIERS = ("primitive", "semantic", "component")
ALIAS = re.compile(r"\{([^{}]+)\}")

HEADER = "/* Emitted by emit.py. Edit tokens.json, not this file. */"

# Tier 1 is the only layer allowed a literal colour, so the boundary is
# emitted: below it, a raw value is a leak rather than a primitive.
SENTINEL = "/* ---- end tier 1 · no raw values below this line ---- */"


def fail(message):
    sys.exit(f"emit: {message}")


# --------------------------------------------------------------------------
# token tree
# --------------------------------------------------------------------------
def prop(path):
    """Custom property name for a token path: drop the tier, join the rest.

    primitive.neutral.900   -> --neutral-900
    semantic.color.surface  -> --color-surface

    The group already says which tier a token is in, so carrying the tier
    too would only lengthen every name. This is the flattening the template's
    $themes keys assume and the one build.py's gates parse.
    """
    return "--" + "-".join(path.split(".")[1:])


def collect(node, path, tokens):
    """Walk a tier into an ordered {path: $value} map, skipping $-metadata."""
    for key, child in node.items():
        if key.startswith("$"):
            continue
        here = f"{path}.{key}"
        if not isinstance(child, dict):
            fail(f"{here}: expected a token or a group, found {child!r}")
        if "$value" in child:
            tokens[here] = child["$value"]
        else:
            collect(child, here, tokens)


def load(data):
    """The three tiers flattened into one ordered {path: $value} map."""
    tokens = {}
    for tier in TIERS:
        if isinstance(data.get(tier), dict):
            collect(data[tier], tier, tokens)
    if not tokens:
        fail("no primitive/semantic/component tier found — is this a tokens.json?")
    return tokens


def render(value, where, known):
    """Render one $value, resolving {a.b.c} aliases to var(--b-c).

    Aliases stay aliases: flattening one to the literal it points at today
    breaks the moment a theme remaps the tier underneath it.
    """
    text = str(value)
    # Catches the bare "REPLACE" and the "#REPLACE" the colour slots carry,
    # since the latter contains the former.
    if "REPLACE" in text:
        fail(f"{where}: $value is still the template placeholder — {text!r}")

    def swap(match):
        target = match.group(1).strip()
        if target not in known:
            fail(f"{where}: alias {{{target}}} resolves to no token in this system")
        return f"var({prop(target)})"

    return ALIAS.sub(swap, text)


def check_path(key, value, where, known):
    """Reject anything that is not a declared dotted token path."""
    if isinstance(value, dict):
        fail(f"{where}: {key!r} is a nested group, not a dotted path")
    if "." not in key or key.split(".")[0] not in TIERS:
        fail(f"{where}: {key!r} is not a dotted token path "
             f"(expected e.g. semantic.color.surface)")
    if key not in known:
        fail(f"{where}: {key!r} names no token in this system")


# --------------------------------------------------------------------------
# blocks
# --------------------------------------------------------------------------
def tier_block(tier, tokens, known, title):
    """One `:root` block for a whole tier, grouped as the source groups it."""
    paths = [p for p in tokens if p.startswith(f"{tier}.")]
    if not paths:
        return []
    lines = [f"/* ---- {title} ---- */", ":root {"]
    group = None
    for path in paths:
        if path.split(".")[1] != group:
            group = path.split(".")[1]
            lines.append(f"  /* {group} */")
        lines.append(f"  {prop(path)}: {render(tokens[path], path, known)};")
    return lines + ["}", ""]


def overrides(entries, where, known, indent="  "):
    """Declarations for one flat map of dotted token path -> value."""
    lines = []
    for key, value in entries.items():
        if key.startswith("$"):
            continue
        check_path(key, value, where, known)
        lines.append(f"{indent}{prop(key)}: "
                     f"{render(value, f'{where}.{key}', known)};")
    return lines


def scope_blocks(data, block, attribute, known):
    """Scoped override blocks for one of $themes or $densities."""
    lines = []
    for name, entries in (data.get(block) or {}).items():
        if name.startswith("$"):
            continue
        if not isinstance(entries, dict):
            fail(f"{block}.{name}: expected a map of overrides, found {entries!r}")
        lines += [f"/* ---- {attribute} · {name} ---- */",
                  f'[data-{attribute}="{name}"] {{']
        lines += overrides(entries, f"{block}.{name}", known) + ["}", ""]
    return lines


def print_block(block, known, props):
    """`@media print` — tier 2 remapped to ink, plus any page geometry."""
    flat = {k: v for k, v in block.items() if not isinstance(v, dict)}
    lines = ["/* ---- print overrides ---- */", "@media print {", "  :root {"]
    lines += overrides(flat, "$print", known, indent="    ")
    for name, entries in block.items():
        # `page` is CSS's own name for page geometry and gets the at-rule
        # below; any other nested group is a set of token overrides.
        if name.startswith("$") or name == "page" or not isinstance(entries, dict):
            continue
        for key, value in entries.items():
            if key.startswith("$"):
                continue
            # A print group either restates a declared token name outright
            # or namespaces it by the group. Accept both, invent neither.
            token = key if f"--{key}" in props else f"{name}-{key}"
            lines.append(f"    --{token}: "
                         f"{render(value, f'$print.{name}.{key}', known)};")
    lines.append("  }")
    page = block.get("page")
    if isinstance(page, dict):
        lines.append("  @page {")
        lines += [f"    {k}: {render(v, f'$print.page.{k}', known)};"
                  for k, v in page.items() if not k.startswith("$")]
        lines.append("  }")
    return lines + ["}", ""]


def emit_css(data):
    """The whole stylesheet's token layers, in generation.md's fixed order."""
    tokens = load(data)
    known, props = set(tokens), {prop(p) for p in tokens}

    out = [HEADER, ""]
    out += tier_block("primitive", tokens, known, "tier 1 · primitives")
    out += [SENTINEL, ""]
    out += tier_block("semantic", tokens, known, "tier 2 · semantic")
    out += scope_blocks(data, "$themes", "theme", known)
    if isinstance(data.get("$print"), dict):
        out += print_block(data["$print"], known, props)
    out += tier_block("component", tokens, known, "tier 3 · component")
    out += scope_blocks(data, "$densities", "density", known)
    return "\n".join(out)


def validate(data):
    """Put the whole file through the CSS emitter and drop the result.

    The adapters below read only some of these declarations, so without this
    a tokens.json the stylesheet loudly rejects would be quietly accepted by
    `--format ts`. Running the emitter rather than restating its gates is what
    keeps the two verdicts — and their error messages — from drifting apart.
    """
    emit_css(data)


# --------------------------------------------------------------------------
# typescript
# --------------------------------------------------------------------------
def nest(tokens):
    """The flat path map rebuilt as the nested tree, leaves -> var() strings."""
    tree = {}
    for path in tokens:
        parts = path.split(".")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                fail(f"{path}: a token already owns the name {part!r}")
        if isinstance(node.get(parts[-1]), dict):
            fail(f"{path}: a group already owns the name {parts[-1]!r}")
        node[parts[-1]] = f"var({prop(path)})"
    return tree


def ts_object(node, depth):
    """One object literal, a key per line. Every key is quoted, because token
    segments are freely digits and dashes and neither is a bare identifier."""
    pad, close = "  " * (depth + 1), "  " * depth
    body = []
    for key, child in node.items():
        value = (ts_object(child, depth + 1) if isinstance(child, dict)
                 else json.dumps(child))
        body.append(f"{pad}{json.dumps(key)}: {value},")
    return "{\n" + "\n".join(body) + f"\n{close}}}"


def emit_ts(data):
    """A dependency-free TypeScript module — no framework import, so it reads
    the same from React, Angular or Svelte.

    Leaves are `var(--name)` references, never resolved literals: the browser
    re-resolves the reference under whatever theme is active at read time,
    which is the entire point of putting the tokens in custom properties.
    """
    tokens = load(data)
    validate(data)

    out = [HEADER, "",
           "/* ---- the token tree · leaves are CSS var() references ---- */",
           f"export const tokens = {ts_object(nest(tokens), 0)} as const;", "",
           "export type Tokens = typeof tokens;", "",
           "/* ---- token path -> custom property name, for imperative use ---- */",
           "export const cssVar = {"]
    out += [f"  {json.dumps(p)}: {json.dumps(prop(p))}," for p in tokens]
    out += ["} as const;", "",
            "export type TokenPath = keyof typeof cssVar;",
            "export type CustomProperty = (typeof cssVar)[TokenPath];", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------
# tailwind
# --------------------------------------------------------------------------
# Tailwind v4 is CSS-first: a variable declared in @theme under one of its
# namespaces is what generates the matching utilities. These are the group
# names the template fixes, against the namespace each one belongs in.
TAILWIND_V4 = {"color": "color", "space": "spacing", "radius": "radius",
               "text": "text", "font": "font", "easing": "ease",
               "elevation": "shadow", "breakpoint": "breakpoint"}

# The v3 `theme.extend` key each of those namespaces lives under.
TAILWIND_V3 = {"color": "colors", "spacing": "spacing", "radius": "borderRadius",
               "text": "fontSize", "font": "fontFamily", "shadow": "boxShadow",
               "ease": "transitionTimingFunction", "breakpoint": "screens"}

COLOUR = re.compile(r"^(#[0-9A-Fa-f]{3,8}$|(rgba?|hsla?|okl(ch|ab)|la[bc]|lch"
                    r"|color)\()")


def namespace(tier, group, tokens):
    """(Tailwind namespace, keep the group name?) for one source group.

    A group named after a Tailwind concept maps by name and sheds the name,
    since the namespace already carries it. A primitive ramp is recognised by
    its values instead — every leaf a literal colour is the only signal a ramp
    gives that it belongs in --color-* — and keeps its name, so a `neutral`
    ramp lands as --color-neutral-*. Anything else has no namespace.
    """
    if group in TAILWIND_V4:
        return TAILWIND_V4[group], False
    values = [str(v) for p, v in tokens.items() if p.startswith(f"{tier}.{group}.")]
    if values and all(COLOUR.match(v.strip()) for v in values):
        return "color", True
    return None, False


def tw_name(path, ns, keep_group):
    """The namespaced name a token takes inside @theme, or ours when it has none."""
    if ns is None:
        return prop(path)
    parts = path.split(".")
    return f"--{ns}-" + "-".join(parts[1:] if keep_group else parts[2:])


def emit_tailwind(data):
    """A v4 @theme block and a v3 theme.extend fragment, from the one tree.

    v3 is still widely deployed, so both are emitted; the file is valid CSS
    and the v3 object sits in a comment, since no one file can be both.
    """
    tokens = load(data)
    known = set(tokens)
    validate(data)

    theme, extend, plain = [], {}, []
    group = None
    for path in tokens:
        tier, here = path.split(".")[0], path.split(".")[1]
        if here != group:
            group = here
            ns, keep = namespace(tier, group, tokens)
            note = (f"generates {ns} utilities" if ns else
                    "no Tailwind namespace — a plain variable, no utilities")
            theme.append(f"  /* {tier} · {group} — {note} */")
            if ns is None:
                plain.append(f"{tier}.{group}")
        name = tw_name(path, ns, keep)
        # A namespace that lands on our own name cannot reference itself, so
        # the token carries its value; otherwise the namespaced name points at
        # ours and one source still drives both.
        value = (render(tokens[path], path, known) if name == prop(path)
                 else f"var({prop(path)})")
        theme.append(f"  {name}: {value};")
        key = TAILWIND_V3.get(ns)
        if key:
            extend.setdefault(key, {})[name[len(ns) + 3:]] = f"var({prop(path)})"

    out = [HEADER, "",
           "/* ================================================================ */",
           "/* Tailwind v4 · @theme — v4 is CSS-first, so these variables are   */",
           "/* the config: Tailwind reads the namespaces and generates the      */",
           "/* utilities. Import this after the emitted tokens stylesheet.      */",
           "/* ================================================================ */", "",
           "@theme {"] + theme + ["}", ""]

    out += ["/* ================================================================ */",
            "/* Tailwind v3 · theme.extend — copy the object below into          */",
            "/* tailwind.config.js. Values reference the emitted custom          */",
            "/* properties, so themes keep working and the source stays one.     */",
            "/* ================================================================ */", "", "/*"]
    out.append("{")
    for key, entries in extend.items():
        out.append(f"  {key}: {{")
        out += [f"    {json.dumps(k)}: {json.dumps(v)},"
                for k, v in entries.items()]
        out.append("  },")
    out.append("}")
    if plain:
        out += ["", "v3 has no theme.extend key for these groups; use the custom",
                "properties directly: " + ", ".join(plain) + "."]
    return "\n".join(out + ["*/", ""])


# --------------------------------------------------------------------------
# shadcn/ui
# --------------------------------------------------------------------------
# shadcn components are written against a fixed set of variable names — a
# consumer writes `bg-background`, never our token names — so the vocabulary
# below is shadcn's, not ours, and is the one place a hardcoded list belongs.
# Sources are given as custom property names, which makes them tier-agnostic.
SHADCN = (
    ("background", ("--color-canvas",)),
    ("foreground", ("--color-text-primary",)),
    ("card", ("--color-surface",)),
    ("card-foreground", ("--color-text-primary",)),
    ("popover", ("--color-elevated", "--color-surface")),
    ("popover-foreground", ("--color-text-primary",)),
    ("primary", ("--color-action-solid",)),
    ("primary-foreground", ("--color-text-inverse",)),
    ("secondary", ("--color-surface-sunken",)),
    ("secondary-foreground", ("--color-text-primary",)),
    ("muted", ("--color-surface-sunken",)),
    ("muted-foreground", ("--color-text-secondary",)),
    ("accent", ("--color-surface-hover",)),
    ("accent-foreground", ("--color-text-primary",)),
    ("destructive", ("--state-error-fg", "--state-error-solid")),
    ("destructive-foreground", ("--color-text-inverse",)),
    ("border", ("--color-rule",)),
    ("input", ("--color-rule",)),
    ("ring", ("--color-focus-ring", "--color-focus")),
    ("radius", ("--radius-md",)),
)

# shadcn pairs a surface with the text that sits on it, and names the pair by
# suffix, so which slots pair is read off the vocabulary rather than listed
# again. Plain `foreground` has no prefix and so pairs with nothing.
FOREGROUND = "-foreground"


def resolve(declared):
    """Settle shadcn's vocabulary against the tokens this system declares.

    A slot takes the first source in its chain that exists, so a system with a
    distinct elevated surface gets it and one without falls back to the
    ordinary surface a floating panel actually sits on. A chain counts as
    unmapped only once every link is absent.

    A foreground whose background never mapped goes with it. A text colour for
    a surface that fell back to some shadcn default the system has never seen
    is not half a pair, it is an incoherent one.
    """
    mapped, missing = [], []
    for slot, sources in SHADCN:
        hit = next((s for s in sources if s in declared), None)
        (mapped if hit else missing).append((slot, hit or sources))
    absent = {slot for slot, _ in missing}
    orphans = [slot for slot, _ in mapped
               if slot.endswith(FOREGROUND) and slot[:-len(FOREGROUND)] in absent]
    return ([row for row in mapped if row[0] not in orphans], missing, orphans)


def emit_shadcn(data):
    """shadcn's slots aliased onto our semantics, light at `:root` and each
    theme in its own block under shadcn's class convention.

    A slot no chain could reach is left out rather than filled in. A fabricated
    `--popover` is worse than an absent one: the component falls back to its own
    default and the consumer can see that it did, where a wrong value just looks
    deliberate.
    """
    tokens = load(data)
    known = set(tokens)
    validate(data)

    mapped, missing, orphans = resolve({prop(p) for p in tokens})
    if not mapped:
        fail("shadcn: not one slot maps — this system declares none of the "
             "semantic colour tokens shadcn's vocabulary is built on")

    out = [HEADER, ""]
    if missing or orphans:
        out += ["/* ---- left out · deliberately not invented ---- */"]
        out += [f"/*   --{slot}: no source token — tried {' or '.join(sources)} */"
                for slot, sources in missing]
        out += [f"/*   --{slot}: dropped with its unmapped "
                f"--{slot[:-len(FOREGROUND)]} */" for slot in orphans] + [""]
    out += ["/* ---- shadcn/ui slots · light ---- */", ":root {"]
    out += [f"  --{slot}: var({source});" for slot, source in mapped] + ["}", ""]

    for name, entries in (data.get("$themes") or {}).items():
        if name.startswith("$"):
            continue
        if not isinstance(entries, dict):
            fail(f"$themes.{name}: expected a map of overrides, found {entries!r}")
        shifted = {}
        for key, value in entries.items():
            if key.startswith("$"):
                continue
            check_path(key, value, f"$themes.{name}", known)
            shifted[prop(key)] = render(value, f"$themes.{name}.{key}", known)
        rows = [(slot, shifted[src]) for slot, src in mapped if src in shifted]
        if not rows:
            continue
        # shadcn scopes its dark values by class, so the theme name is the
        # class: the conventional `.dark` falls out of a theme named dark.
        out += [f"/* ---- shadcn/ui slots · {name} ---- */", f".{name} {{"]
        out += [f"  --{slot}: {value};" for slot, value in rows] + ["}", ""]

    if missing:
        print(f"emit: shadcn — {len(missing)} of {len(SHADCN)} slots unmapped; "
              f"this system declares no source token for them", file=sys.stderr)
        for slot, sources in missing:
            print(f"         --{slot:<22} tried {' or '.join(sources)}",
                  file=sys.stderr)
    if orphans:
        print(f"emit: shadcn — {len(orphans)} more dropped as orphaned "
              f"foregrounds, their background having not mapped", file=sys.stderr)
        for slot in orphans:
            print(f"         --{slot:<22} dropped with "
                  f"--{slot[:-len(FOREGROUND)]}", file=sys.stderr)
    if missing or orphans:
        print("       Nothing was invented for any of them. A shadcn component "
              "that uses\n       those slots falls back to its own default "
              "until the system declares one.", file=sys.stderr)
    return "\n".join(out)


# --------------------------------------------------------------------------
# entry
# --------------------------------------------------------------------------
FORMATS = {"css": emit_css, "ts": emit_ts,
           "tailwind": emit_tailwind, "shadcn": emit_shadcn}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tokens")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--format", choices=sorted(FORMATS), default="css",
                    help="substrate to write the tokens out in (default: css)")
    args = ap.parse_args()

    source = pathlib.Path(args.tokens)
    try:
        data = json.loads(source.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{source}: not valid JSON — {exc}")

    css = FORMATS[args.format](data)
    target = pathlib.Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(css)
    if args.format == "ts":
        count, unit = len(css.splitlines()), "lines"
    else:
        count = sum(1 for line in css.splitlines() if line.lstrip().startswith("--"))
        unit = "declarations"
    print(f"  emitted  {target.name:<32} {len(css):>8,} bytes"
          f"   {count} {unit}")


if __name__ == "__main__":
    main()
