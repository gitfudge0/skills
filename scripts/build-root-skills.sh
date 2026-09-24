#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  printf 'Usage: %s OUTPUT_DIR\n' "${0##*/}" >&2
  exit 2
fi

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="$1"
mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd)"

if [[ "$output_dir" == "$source_dir" ]]; then
  printf 'Output directory must differ from the source directory.\n' >&2
  exit 2
fi

stage_dir="$(mktemp -d "$output_dir/.fudge-stage.XXXXXX")"
trap 'rm -rf "$stage_dir"' EXIT

for root in fudge-design fudge-ship; do
  cp -R "$source_dir/$root" "$stage_dir/$root"
  mkdir -p "$stage_dir/$root/references/specialists"
  touch "$stage_dir/$root/.fudge-build-generated"
done

for specialist in "$source_dir"/fudge-*; do
  [[ -d "$specialist" ]] || continue
  name="${specialist##*/}"
  case "$name" in
    fudge-ship|fudge-mindmap|fudge-report-deck|fudge-unslop)
      continue
      ;;
    fudge-design)
      roots=(fudge-ship)
      ;;
    *)
      roots=(fudge-design fudge-ship)
      ;;
  esac

  for root in "${roots[@]}"; do
    guide_dir="$stage_dir/$root/references/specialists/$name"
    mkdir -p "$guide_dir"
    cp -R "$specialist"/. "$guide_dir/"
    mv "$guide_dir/SKILL.md" "$guide_dir/guide.md"
  done
done

for root in fudge-design fudge-ship; do
  if [[ -e "$output_dir/$root" && ! -f "$output_dir/$root/.fudge-build-generated" ]]; then
    printf 'Refusing to replace an unmarked directory: %s\n' "$output_dir/$root" >&2
    exit 1
  fi
done

for root in fudge-design fudge-ship; do
  rm -rf "$output_dir/$root"
  mv "$stage_dir/$root" "$output_dir/$root"
done
