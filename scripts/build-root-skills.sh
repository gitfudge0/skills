#!/usr/bin/env bash
set -euo pipefail
[ "$#" -eq 1 ] || { printf 'Usage: %s OUTPUT_DIR\n' "$0" >&2; exit 2; }
exec python3 "$(dirname "$0")/build_root_skills.py" "$1"
