#!/usr/bin/env bash
# Convert packed report HTML with a local Chromium browser and native print CSS.
# Usage: html-to-pdf.sh input.html [output.pdf]
# CHROME_BIN selects a browser; RENDER_MS controls JS settle time (default 3000).
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "usage: $0 <input.html> [output.pdf]" >&2
  exit 2
fi
if [ ! -f "$1" ]; then
  echo "error: input file not found: $1" >&2
  exit 1
fi
REPORT_INPUT="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
REPORT_OUTPUT="${2:-${REPORT_INPUT%.*}.pdf}"
find_chrome() {
  if [ -n "${CHROME_BIN:-}" ] && [ -x "$CHROME_BIN" ]; then
    echo "$CHROME_BIN"; return 0
  fi
  local candidate
  for candidate in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/Applications/Chromium.app/Contents/MacOS/Chromium" "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" google-chrome google-chrome-stable chromium chromium-browser microsoft-edge; do
    if [ -x "$candidate" ]; then echo "$candidate"; return 0; fi
    if command -v "$candidate" >/dev/null 2>&1; then command -v "$candidate"; return 0; fi
  done
  return 1
}
REPORT_CHROME="$(find_chrome)" || {
  echo "error: set CHROME_BIN to a local Chromium-family browser" >&2
  exit 1
}
# A fresh browser profile avoids reusing persisted annotations/theme. Native print
# CSS supplies the white/gold palette and normal document pagination.
REPORT_PROFILE="$(mktemp -d "${TMPDIR:-/tmp}/fudge-report-pdf.XXXXXX")"
trap 'rm -rf "$REPORT_PROFILE"' EXIT
"$REPORT_CHROME" --headless=new --disable-gpu \
  --user-data-dir="$REPORT_PROFILE" --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget="${RENDER_MS:-3000}" \
  --print-to-pdf="$REPORT_OUTPUT" "file://$REPORT_INPUT"
if [ ! -s "$REPORT_OUTPUT" ]; then
  echo "error: PDF was not produced" >&2
  exit 1
fi
echo "Wrote $REPORT_OUTPUT (native print pagination; inspect pages before delivery)"
