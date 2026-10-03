#!/usr/bin/env bash
#
# html-to-pdf.sh — convert a slide-deck report HTML into a shareable PDF.
#
# Uses a headless Chromium-family browser's print-to-PDF. This is the
# only approach that (a) executes the Mermaid JS so diagrams render and
# (b) honours the @media print rules in report.css that lay the deck
# out as one slide per landscape page with the meaning-bearing tints
# preserved.
#
# The deck prints in LANDSCAPE, one slide per page. The orientation and
# one-slide-per-page paging come from report.css (@page { size: landscape }
# + per-slide break-after). This script just renders with margins off and
# gives Mermaid time to settle.
#
# Usage:
#   scripts/html-to-pdf.sh <input.html> [output.pdf]
#
# If output is omitted, writes alongside the input with a .pdf extension.
#
# Env overrides:
#   CHROME_BIN   path to a chrome/chromium/edge binary (skips auto-detect)
#   RENDER_MS    virtual-time budget in ms for JS/Mermaid (default 3000)
#   STYLE        visual style to render the PDF in — one of marginalia,
#                verdant, blueprint, editorial, terminal, brutalist, glass.
#                Omit to keep whatever data-style the HTML already carries.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <input.html> [output.pdf]" >&2
  exit 2
fi

IN="$1"
if [ ! -f "$IN" ]; then
  echo "error: input file not found: $IN" >&2
  exit 1
fi

# Resolve to an absolute path (Chrome's --print-to-pdf needs a file:// URL).
IN_ABS="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
OUT="${2:-${IN_ABS%.*}.pdf}"
RENDER_MS="${RENDER_MS:-3000}"

# PDFs are always light. Force light mode for the render: the @media print
# CSS handles HTML/CSS colours, but Mermaid renders its SVG at load using the
# active theme — a diagram drawn in dark mode can't be recoloured by print
# CSS. So we render a temp copy with data-theme="light" pinned on <html>,
# which makes the theme script (and Mermaid init) resolve to light. The temp
# file sits beside the original so its relative assets/ paths still resolve.
# Validate an optional visual-style override.
STYLE="${STYLE:-}"
if [ -n "$STYLE" ]; then
  case "$STYLE" in
    marginalia|verdant|blueprint|editorial|terminal|brutalist|glass) ;;
    *) echo "error: invalid STYLE '$STYLE' (expected one of marginalia, verdant, blueprint, editorial, terminal, brutalist, glass)" >&2; exit 2 ;;
  esac
fi

DIR="$(dirname "$IN_ABS")"
TMP="$DIR/.pdf-render-$$.html"
# Rewrite the opening <html> tag on a temp copy that sits beside the original
# (so relative assets/ paths still resolve). We always force data-theme="light"
# and optionally pin data-style. We use perl, NOT sed: the `0,/re/` first-match
# address is a GNU-sed extension that silently no-ops on macOS's BSD sed.
#   - data-theme: always stripped then re-added as "light". PDFs are always
#     light — the @media print CSS recolours HTML, but Mermaid bakes its SVG at
#     load using the live theme, so a dark diagram can't be recoloured later.
#   - data-style: stripped + re-added only when STYLE is set; otherwise the
#     HTML keeps whatever style it already declares.
STYLE="$STYLE" perl -0777 -pe '
  s{<html\b[^>]*>}{
    my $tag = $&;
    $tag =~ s/\s+data-theme="[^"]*"//g;            # always re-pin theme below
    $tag =~ s/\s+data-style="[^"]*"//g if length $ENV{STYLE};
    my $attrs = q{ data-theme="light"};
    $attrs .= qq{ data-style="$ENV{STYLE}"} if length $ENV{STYLE};
    $tag =~ s/>$/$attrs>/;
    $tag;
  }e
' "$IN_ABS" > "$TMP"
RENDER_ABS="$TMP"
cleanup() { rm -f "$TMP"; }
trap cleanup EXIT

# ── Locate a Chromium-family binary ───────────────────────────────────
find_chrome() {
  if [ -n "${CHROME_BIN:-}" ] && [ -x "${CHROME_BIN}" ]; then
    echo "$CHROME_BIN"; return 0
  fi
  local candidates=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    google-chrome google-chrome-stable chromium chromium-browser
    microsoft-edge brave-browser chrome
  )
  local c
  for c in "${candidates[@]}"; do
    if [ -x "$c" ]; then echo "$c"; return 0; fi
    if command -v "$c" >/dev/null 2>&1; then command -v "$c"; return 0; fi
  done
  return 1
}

CHROME="$(find_chrome)" || {
  echo "error: no Chrome/Chromium/Edge/Brave binary found." >&2
  echo "       install one, or set CHROME_BIN=/path/to/chrome" >&2
  exit 1
}

echo "→ browser : $CHROME"
echo "→ input   : $IN_ABS"
echo "→ output  : $OUT"
echo "→ render  : ${RENDER_MS}ms (Mermaid/JS settle time)"
echo "→ layout  : landscape, one slide per page · forced light mode${STYLE:+ · style=$STYLE}"

# --virtual-time-budget lets queued JS (Mermaid diagram rendering) run to
# completion before the PDF is captured. --headless=new honours print-color.
# --no-margins + the @page { size: landscape; margin: 0 } rule in report.css
# give one full-bleed landscape page per slide; --print-to-pdf-no-header
# suppresses Chrome's default date/URL furniture.
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --no-margins \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget="$RENDER_MS" \
  --print-to-pdf="$OUT" \
  "file://$RENDER_ABS" 2>/dev/null

if [ -f "$OUT" ]; then
  echo "✓ wrote $OUT"
else
  echo "error: PDF was not produced" >&2
  exit 1
fi
