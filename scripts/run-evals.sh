#!/usr/bin/env bash
# Run tests/evals/scenarios.json through `claude plugin eval`.
#
#   bash scripts/run-evals.sh [--root NAME]... [--case GLOB] [--runs N]
#                             [--generate-only | --validate] [--out DIR]
#                             [-- <extra claude plugin eval flags>]
#
# Generates one plugin wrapper per selected root under .fudge-evals/ (gitignored),
# each wrapping a copy of the built package .fudge-build/<package>. Build first:
#   bash scripts/build-root-skills.sh .fudge-build
#
# Running cases spends model credit. --generate-only writes suites only.
# --validate also schema-checks every case.yaml and runs `claude plugin validate`
# on each wrapper; neither starts an agent (`claude plugin eval` has no dry run).
# Extra flags after `--` go to `claude plugin eval` (for example
# `--allow-tools Bash Edit Write`, `--scaffold`, `-j 4`, `--max-cost-usd 5`).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
out="$repo/.fudge-evals"
mode=run
case_glob='*'
gen_args=()
eval_args=()

while [ $# -gt 0 ]; do
  case "$1" in
    --root) gen_args+=(--root "$2"); shift 2 ;;
    --case) case_glob="$2"; shift 2 ;;
    --runs) gen_args+=(--runs "$2"); shift 2 ;;
    --out) out="$2"; shift 2 ;;
    --generate-only) mode=generate; shift ;;
    --validate) mode=validate; shift ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --) shift; eval_args=("$@"); break ;;
    *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

wrappers=()
while IFS=$'\t' read -r wrapper count; do
  echo "Generated $count case(s) in $wrapper"
  wrappers+=("$wrapper")
done < <(python3 "$repo/scripts/eval_cases.py" --out "$out" --case "$case_glob" ${gen_args[@]+"${gen_args[@]}"})
[ ${#wrappers[@]} -gt 0 ] || exit 1

if [ "$mode" = generate ]; then
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found; suites are generated under $out" >&2
  exit 1
fi

status=0
for wrapper in "${wrappers[@]}"; do
  if [ "$mode" = validate ]; then
    echo "== validate $wrapper"
    python3 "$repo/scripts/eval_cases.py" --check "$wrapper" || status=1
    claude plugin validate "$wrapper" || status=1
  else
    echo "== eval $wrapper"
    claude plugin eval "$wrapper" --eval-dir evals --case "$case_glob" \
      ${eval_args[@]+"${eval_args[@]}"} || status=1
  fi
done
exit $status
