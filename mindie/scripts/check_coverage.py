#!/usr/bin/env python3
"""
mindie coverage checker.

Completeness is the top priority for a mindie map: no idea from the source may
be silently dropped. A mental "did I cover everything?" pass is not reliable —
this script turns coverage into an explicit, auditable step.

It does NOT try to judge meaning (a script can't know if an idea is
"represented"). Instead it enforces an accounting discipline: you list the
atomic units of the source in a coverage file, and for each one record where it
landed in the tree (or an explicit, reviewed decision to omit it). The script
then fails loudly if anything is unaccounted for.

--------------------------------------------------------------------------
WORKFLOW
--------------------------------------------------------------------------
1. Segment the source into atomic units (one idea/claim/fact/example each).
   Write them to a coverage file, one per line, before or alongside building
   the tree. See coverage-file format below.

2. As you build the map, tag each unit with the node id that carries it, e.g.
       [r2]  Eat to 80% of your hunger (hara hachi bu)
   A unit may map to a node's label, its summary, or one of its points — any
   is fine; what matters is that the idea is present in that node's content.

3. Run:
       python3 scripts/check_coverage.py --coverage cov.txt --data map.json
   The check passes only when every unit is either mapped to an existing node
   id, or explicitly marked OMIT with a reason.

--------------------------------------------------------------------------
COVERAGE FILE FORMAT (plain text, one unit per line)
--------------------------------------------------------------------------
    [node_id]  unit text            -> mapped to that node
    [OMIT: reason]  unit text       -> deliberately excluded, reason recorded
    unit text                       -> UNACCOUNTED (will fail the check)

Blank lines and lines starting with '#' are ignored (comments/section labels).

Example:
    # Section: Rules of Ikigai
    [rules]  The book lists rules for ikigai
    [r1]     Stay active, don't retire
    [r2]     Eat to 80% fullness
    [rules]  Surround yourself with good friends
    [OMIT: newsletter signup box, not book content]  Get Deep Shah's stories

--------------------------------------------------------------------------
EXIT CODES
--------------------------------------------------------------------------
    0  every unit accounted for (mapped or explicitly omitted)
    1  one or more units unaccounted for, or mapped to a nonexistent node id
"""
import argparse, json, re, sys

def collect_ids(node, ids):
    ids.add(node.get("id"))
    for c in node.get("children", []) or []:
        collect_ids(c, ids)

def parse_line(line):
    """Return (kind, key, text). kind in {map, omit, bare, comment}."""
    s = line.rstrip("\n")
    if not s.strip() or s.lstrip().startswith("#"):
        return ("comment", None, s)
    m = re.match(r"\s*\[\s*OMIT\s*:\s*(.*?)\s*\]\s*(.*)", s, re.IGNORECASE)
    if m:
        return ("omit", m.group(1), m.group(2).strip())
    m = re.match(r"\s*\[\s*([^\]:]+?)\s*\]\s*(.*)", s)
    if m:
        return ("map", m.group(1).strip(), m.group(2).strip())
    return ("bare", None, s.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage", required=True, help="coverage file (units + mappings)")
    ap.add_argument("--data", required=True, help="mindmap JSON (root node)")
    ap.add_argument("--min-mapped-ratio", type=float, default=0.0,
                    help="optional: fail if fraction of OMITs exceeds (1 - ratio)")
    args = ap.parse_args()

    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)
    ids = set()
    collect_ids(data, ids)

    mapped, omitted, unaccounted, bad_ref = [], [], [], []
    total_units = 0

    with open(args.coverage, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            kind, key, text = parse_line(line)
            if kind == "comment":
                continue
            total_units += 1
            if kind == "map":
                if key in ids:
                    mapped.append((key, text))
                else:
                    bad_ref.append((i, key, text))
            elif kind == "omit":
                omitted.append((key, text))
            else:  # bare
                unaccounted.append((i, text))

    print(f"Coverage report for {args.data}")
    print(f"  source units listed : {total_units}")
    print(f"  mapped to a node     : {len(mapped)}")
    print(f"  explicitly omitted   : {len(omitted)}")
    print(f"  UNACCOUNTED          : {len(unaccounted)}")
    print(f"  bad node references  : {len(bad_ref)}")

    ok = True

    if unaccounted:
        ok = False
        print("\nUNACCOUNTED UNITS (every one must be mapped [node_id] or [OMIT: reason]):")
        for ln, text in unaccounted:
            print(f"  line {ln}: {text}")

    if bad_ref:
        ok = False
        print("\nMAPPED TO NONEXISTENT NODE IDs (fix the id or the tree):")
        for ln, key, text in bad_ref:
            print(f"  line {ln}: [{key}] {text}")

    if omitted:
        print("\nOMISSIONS (recorded, review these — each is content NOT in the map):")
        for reason, text in omitted:
            print(f"  - {text}   << {reason}")

    if total_units and args.min_mapped_ratio > 0:
        ratio = len(mapped) / total_units
        if ratio < args.min_mapped_ratio:
            ok = False
            print(f"\nMAPPED RATIO {ratio:.2f} below required {args.min_mapped_ratio:.2f}"
                  f" — too much is being omitted.")

    print("\nRESULT:", "PASS — all source units accounted for" if ok
          else "FAIL — unaccounted content above; nothing may be silently dropped")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
