#!/usr/bin/env bash
set -euo pipefail

# macOS ships bash 3.2, which lacks namerefs (`local -n`) and fractional
# `read -t` timeouts used by the arrow-key picker. Re-exec under a newer bash
# if one is available (e.g. Homebrew); otherwise fall back to the plain picker.
_need_newer_bash() {
  [ "${BASH_VERSINFO[0]}" -lt 4 ] || { [ "${BASH_VERSINFO[0]}" -eq 4 ] && [ "${BASH_VERSINFO[1]}" -lt 3 ]; }
}
if [ -z "${SKILLS_INSTALL_REEXEC:-}" ] && _need_newer_bash; then
  for _b in /opt/homebrew/bin/bash /usr/local/bin/bash; do
    [ -x "$_b" ] || continue
    if "$_b" -c '[ "${BASH_VERSINFO[0]}" -gt 4 ] || { [ "${BASH_VERSINFO[0]}" -eq 4 ] && [ "${BASH_VERSINFO[1]}" -ge 3 ]; }' 2>/dev/null; then
      export SKILLS_INSTALL_REEXEC=1
      exec "$_b" "$0" "$@"
    fi
  done
fi
FANCY_OK=1
_need_newer_bash && FANCY_OK=0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

COLOR=1
[ -n "${NO_COLOR:-}" ] && COLOR=0
[ -t 1 ] || COLOR=0
if [ "$COLOR" -eq 1 ]; then
  C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'; C_DIM=$'\033[2m'; C_RESET=$'\033[0m'
else
  C_GREEN=""; C_YELLOW=""; C_RED=""; C_DIM=""; C_RESET=""
fi
ok()   { echo "${C_GREEN}✓ $*${C_RESET}"; }
warn() { echo "${C_YELLOW}$*${C_RESET}"; }
err()  { echo "${C_RED}$*${C_RESET}" >&2; }

usage() {
  cat <<EOF
Usage: $0 [install|list|remove] [options]

Subcommands:
  install   Install skills into agent skill dirs (default)
  list      List installed skills per agent
  remove    Remove previously installed skills

Options:
  --all         select all skills, non-interactive
  --copy        copy instead of symlink (install only)
  -a <agent>    target agent, repeatable: claude|codex|cursor|opencode
  -y            skip confirmations / auto-overwrite
  -h, --help    show this help

Agent target dirs:
  claude   -> ~/.claude/skills
  codex    -> ~/.codex/skills
  cursor   -> ~/.cursor/skills
  opencode -> ~/.config/opencode/skills
EOF
}

SUBCMD="install"; ALL=0; COPY=0; YES=0; AGENTS=()
if [ $# -gt 0 ]; then
  case "$1" in install|list|remove) SUBCMD="$1"; shift ;; esac
fi
while [ $# -gt 0 ]; do
  case "$1" in
    --all) ALL=1 ;;
    --copy) COPY=1 ;;
    -a) shift; AGENTS+=("${1:-}") ;;
    -y) YES=1 ;;
    -h|--help) usage; exit 0 ;;
    *) err "unknown option: $1"; usage; exit 1 ;;
  esac
  shift
done
[ "${#AGENTS[@]}" -eq 0 ] && AGENTS=(claude codex cursor opencode)

agent_dir() {
  case "$1" in
    claude) echo "$HOME/.claude/skills" ;;
    codex) echo "$HOME/.codex/skills" ;;
    cursor) echo "$HOME/.cursor/skills" ;;
    opencode) echo "$HOME/.config/opencode/skills" ;;
    *) err "unknown agent: $1"; exit 1 ;;
  esac
}
CLAUDE_DIR="$HOME/.claude/skills"

skills=()
for d in "$SCRIPT_DIR"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  skills+=("$(basename "$d")")
done

is_repo_skill() {
  local n s
  n="$1"
  for s in "${skills[@]}"; do [ "$s" = "$n" ] && return 0; done
  return 1
}

desc_of() {
  local f="$SCRIPT_DIR/$1/SKILL.md" d
  d="$(grep -m1 '^description:' "$f" 2>/dev/null | sed 's/^description:[[:space:]]*//')"
  [ -z "$d" ] && d="(no description)"
  echo "${d:0:80}"
}

term_width() {
  local w
  w="$(tput cols 2>/dev/null || true)"
  [ -z "$w" ] && w="${COLUMNS:-80}"
  [ -z "$w" ] && w=80
  echo "$w"
}

# Interactive arrow-key checkbox picker. Args: title, items-array-name, checked-array-name (0/1, in/out).
checkbox_picker() {
  local title="$1"
  local -n items_ref="$2"
  local -n checked_ref="$3"
  local n="${#items_ref[@]}" cursor=0 width first_draw=1
  width="$(term_width)"

  trap 'tput cnorm 2>/dev/null || true' EXIT INT TERM
  tput civis 2>/dev/null || true

  draw() {
    [ "$first_draw" -eq 0 ] && tput cuu "$((n + 2))" 2>/dev/null || true
    first_draw=0
    echo "$title"
    local i box ptr label maxlen
    for ((i = 0; i < n; i++)); do
      tput el 2>/dev/null || true
      box="◯"; [ "${checked_ref[$i]}" -eq 1 ] && box="◉"
      ptr="  "; [ "$i" -eq "$cursor" ] && ptr="${C_GREEN}❯${C_RESET} "
      label="${items_ref[$i]}"
      maxlen=$((width - 6)); [ "$maxlen" -lt 10 ] && maxlen=10
      printf "%s%s %s\n" "$ptr" "$box" "${label:0:$maxlen}"
    done
    tput el 2>/dev/null || true
    echo "(Up/Down move, Space toggle, a=all, Enter confirm)"
  }

  draw
  while true; do
    IFS= read -rsn1 key
    if [ "$key" = $'\x1b' ]; then
      read -rsn2 -t 0.01 rest || true
      key+="$rest"
    fi
    case "$key" in
      $'\x1b[A') cursor=$(((cursor - 1 + n) % n)) ;;
      $'\x1b[B') cursor=$(((cursor + 1) % n)) ;;
      ' ') [ "${checked_ref[$cursor]}" -eq 1 ] && checked_ref[$cursor]=0 || checked_ref[$cursor]=1 ;;
      a|A)
        local i allon=1
        for ((i = 0; i < n; i++)); do [ "${checked_ref[$i]}" -eq 0 ] && allon=0 && break; done
        for ((i = 0; i < n; i++)); do checked_ref[$i]=$((1 - allon)); done
        ;;
      "") break ;;
    esac
    draw
  done
  tput cnorm 2>/dev/null || true
  trap - EXIT INT TERM
}

# Non-interactive / old-bash fallback: numbered list, read a=all or numbers.
# Uses eval-based indirection instead of namerefs so it runs on bash 3.2.
plain_picker() {
  local title="$1" items_name="$2" checked_name="$3"
  local n i sel label
  eval "n=\${#$items_name[@]}"
  echo "$title"
  for ((i = 0; i < n; i++)); do
    eval "label=\${$items_name[\$i]}"
    printf "  %d) %s\n" "$((i + 1))" "$label"
  done
  read -rp "Select (a=all, or numbers space/comma separated): " sel || sel=""
  sel="${sel//,/ }"
  for ((i = 0; i < n; i++)); do eval "$checked_name[\$i]=0"; done
  if [ "$sel" = "a" ] || [ "$sel" = "A" ]; then
    for ((i = 0; i < n; i++)); do eval "$checked_name[\$i]=1"; done
  else
    local tok idx
    for tok in $sel; do
      [[ "$tok" =~ ^[0-9]+$ ]] || continue
      idx=$((tok - 1))
      [ "$idx" -ge 0 ] && [ "$idx" -lt "$n" ] && eval "$checked_name[\$idx]=1"
    done
  fi
}

is_tty_interactive() { [ -t 0 ] && [ "$ALL" -eq 0 ]; }

# Dispatch to the fancy widget on a capable tty, plain numbered list otherwise.
pick() {
  if is_tty_interactive && [ "$FANCY_OK" -eq 1 ]; then checkbox_picker "$@"; else plain_picker "$@"; fi
}

do_install() {
  if [ "${#skills[@]}" -eq 0 ]; then
    err "no skills found in $SCRIPT_DIR"; exit 1
  fi

  local sel_skills=() i
  if [ "$ALL" -eq 1 ]; then
    sel_skills=("${skills[@]}")
  else
    local labels=() checked=() s installed
    for s in "${skills[@]}"; do
      installed=""
      { [ -e "$CLAUDE_DIR/$s" ] || [ -L "$CLAUDE_DIR/$s" ]; } && installed=" ${C_DIM}(installed)${C_RESET}"
      labels+=("$(printf "%-24s ${C_DIM}%s${C_RESET}%s" "$s" "$(desc_of "$s")" "$installed")")
    done
    for ((i = 0; i < ${#skills[@]}; i++)); do checked[$i]=0; done
    pick "Select skills to install:" labels checked
    for ((i = 0; i < ${#skills[@]}; i++)); do
      [ "${checked[$i]}" -eq 1 ] && sel_skills+=("${skills[$i]}")
    done
  fi
  [ "${#sel_skills[@]}" -eq 0 ] && { err "no skills selected"; exit 1; }

  local sel_agents=("${AGENTS[@]}") method="symlink"
  [ "$COPY" -eq 1 ] && method="copy"

  if [ "$ALL" -eq 0 ] && is_tty_interactive; then
    local all_agents=(claude codex cursor opencode) achecked=() method_choice
    for ((i = 0; i < ${#all_agents[@]}; i++)); do
      achecked[$i]=0; [ "${all_agents[$i]}" = "claude" ] && achecked[$i]=1
    done
    pick "Select target agents:" all_agents achecked
    sel_agents=()
    for ((i = 0; i < ${#all_agents[@]}; i++)); do
      [ "${achecked[$i]}" -eq 1 ] && sel_agents+=("${all_agents[$i]}")
    done
    echo
    read -rp "Install method: (s)ymlink [default] or (c)opy: " method_choice || method_choice=""
    [ "$method_choice" = "c" ] || [ "$method_choice" = "C" ] && method="copy"
  fi
  [ "${#sel_agents[@]}" -eq 0 ] && { err "no agents selected"; exit 1; }

  # An existing symlink already pointing at our source is not a conflict.
  up_to_date() { [ "$method" = "symlink" ] && [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]; }

  local total_installed=0 target
  for target in "${sel_agents[@]}"; do
    local dest_dir dest src s conflicts=0 overwrite=0 ans
    dest_dir="$(agent_dir "$target")"
    mkdir -p "$dest_dir"

    for s in "${sel_skills[@]}"; do
      dest="$dest_dir/$s"; src="$SCRIPT_DIR/$s"
      { [ -e "$dest" ] || [ -L "$dest" ]; } && ! up_to_date "$dest" "$src" && conflicts=$((conflicts + 1))
    done

    if [ "$YES" -eq 1 ] || [ "$ALL" -eq 1 ]; then
      overwrite=1
    elif [ "$conflicts" -gt 0 ]; then
      read -rp "Overwrite $conflicts existing in $dest_dir? [y/N] " ans || ans=""
      [ "$ans" = "y" ] || [ "$ans" = "Y" ] && overwrite=1
    fi

    for s in "${sel_skills[@]}"; do
      dest="$dest_dir/$s"; src="$SCRIPT_DIR/$s"
      up_to_date "$dest" "$src" && continue
      if { [ -e "$dest" ] || [ -L "$dest" ]; } && [ "$overwrite" -eq 0 ]; then
        warn "skipping $s ($dest_dir)"; continue
      fi
      if [ "$method" = "symlink" ]; then
        ln -sfn "$src" "$dest"
      else
        rm -rf "$dest"; cp -R "$src" "$dest"
      fi
      ok "$s -> $dest"
      total_installed=$((total_installed + 1))
    done
  done

  echo
  ok "Installed $total_installed skills to ${#sel_agents[@]} agents"
}

do_list() {
  local target dest_dir entry name resolved
  for target in "${AGENTS[@]}"; do
    dest_dir="$(agent_dir "$target")"
    [ -d "$dest_dir" ] || continue
    echo "$target ($dest_dir):"
    for entry in "$dest_dir"/*; do
      { [ -e "$entry" ] || [ -L "$entry" ]; } || continue
      name="$(basename "$entry")"
      if [ -L "$entry" ]; then
        resolved="$(readlink -f "$entry" 2>/dev/null || readlink "$entry")"
        case "$resolved" in
          "$SCRIPT_DIR"/*) echo "  ✓ linked  $name" ;;
          *) echo "  foreign   $name" ;;
        esac
      else
        echo "  copy      $name"
      fi
    done
  done
}

do_remove() {
  local candidates=() labels=() target dest_dir entry name resolved
  for target in "${AGENTS[@]}"; do
    dest_dir="$(agent_dir "$target")"
    [ -d "$dest_dir" ] || continue
    for entry in "$dest_dir"/*; do
      { [ -e "$entry" ] || [ -L "$entry" ]; } || continue
      name="$(basename "$entry")"
      if [ -L "$entry" ]; then
        resolved="$(readlink -f "$entry" 2>/dev/null || readlink "$entry")"
        case "$resolved" in "$SCRIPT_DIR"/*) ;; *) continue ;; esac
      else
        is_repo_skill "$name" || continue
      fi
      candidates+=("$target:$entry")
      labels+=("$target/$name")
    done
  done
  if [ "${#candidates[@]}" -eq 0 ]; then
    warn "no repo-installed skills found to remove"; return
  fi

  local checked=() i
  for ((i = 0; i < ${#candidates[@]}; i++)); do checked[$i]=0; done
  if [ "$ALL" -eq 1 ]; then
    for ((i = 0; i < ${#candidates[@]}; i++)); do checked[$i]=1; done
  else
    pick "Select installed skills to remove:" labels checked
  fi

  local to_remove=()
  for ((i = 0; i < ${#candidates[@]}; i++)); do
    [ "${checked[$i]}" -eq 1 ] && to_remove+=("${candidates[$i]}")
  done
  [ "${#to_remove[@]}" -eq 0 ] && { warn "nothing selected"; return; }

  if [ "$YES" -eq 0 ] && [ "$ALL" -eq 0 ]; then
    local ans
    read -rp "Remove ${#to_remove[@]} skill installs? [y/N] " ans || ans=""
    if [ "$ans" != "y" ] && [ "$ans" != "Y" ]; then warn "aborted"; return; fi
  fi

  local c entry_path
  for c in "${to_remove[@]}"; do
    entry_path="${c#*:}"
    name="$(basename "$entry_path")"
    if [ -L "$entry_path" ]; then
      rm "$entry_path"; ok "removed $entry_path"
    elif [ -d "$entry_path" ] && is_repo_skill "$name"; then
      rm -rf "$entry_path"; ok "removed $entry_path"
    else
      err "refusing to remove $entry_path (no matching repo skill)"
    fi
  done
}

case "$SUBCMD" in
  install) do_install ;;
  list) do_list ;;
  remove) do_remove ;;
esac
