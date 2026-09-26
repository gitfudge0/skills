#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/.fudge-build"
ROOTS=(design ux ship review)
AGENT_NAMES=(claude codex cursor opencode)
OPTIONAL=()
for skill_dir in "$SCRIPT_DIR"/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  skill_name="$(basename "$skill_dir")"
  case "$skill_name" in fudge-design|fudge-ux|fudge-ship|fudge-review) ;; *) OPTIONAL+=("${skill_name#fudge-}") ;; esac
done

usage() {
  cat <<HELP
Usage: $0 [install|list|remove] [options]

Install defaults to the design, ux, ship, and review root skills. Individual skills are optional.

Options:
  -a <agent>         target agent, repeatable: claude|codex|cursor|opencode
  --root <name>      root skill, repeatable: design|ux|ship|review
  --skill <name>     individual skill, repeatable (see below)
  --no-roots         install only explicitly selected individual skills
  --all              select all four roots and every individual skill
  --copy             copy instead of symlink (install only)
  -y                 skip confirmation; update installer-owned installs
  -h, --help         show this help

Subcommands:
  install            install selected skills (default)
  list               show agent skill directories
  remove             remove installer-owned skills (use --all -y for all)

Individual skills: ${OPTIONAL[*]}
HELP
}
fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }
note() { printf '%s\n' "$*"; }
contains() { local wanted="$1" item; shift; for item in "$@"; do [ "$item" = "$wanted" ] && return 0; done; return 1; }
append_unique() {
  local name="$1" value="$2" item
  eval "local existing=(\"\${${name}[@]}\")"
  contains "$value" "${existing[@]}" || eval "$name+=(\"\$value\")"
}

SUBCMD=install ALL=0 COPY=0 YES=0 NO_ROOTS=0 EXPLICIT_SELECTION=0
AGENTS=() SELECTED_ROOTS=() SELECTED_OPTIONAL=()
if [ "$#" -gt 0 ]; then
  case "$1" in install|list|remove) SUBCMD="$1"; shift ;; esac
fi
while [ "$#" -gt 0 ]; do
  case "$1" in
    -a)
      [ "$#" -ge 2 ] || fail '-a needs an agent'
      contains "$2" "${AGENT_NAMES[@]}" || fail "unknown agent: $2"
      append_unique AGENTS "$2"; shift 2 ;;
    --root)
      [ "$#" -ge 2 ] || fail '--root needs a name'
      contains "$2" "${ROOTS[@]}" || fail "unknown root skill: $2"
      append_unique SELECTED_ROOTS "$2"; EXPLICIT_SELECTION=1; shift 2 ;;
    --skill)
      [ "$#" -ge 2 ] || fail '--skill needs a name'
      requested="${2#fudge-}"
      contains "$requested" "${ROOTS[@]}" && fail "$2 is a root skill; use --root $requested"
      contains "$requested" "${OPTIONAL[@]}" || fail "unknown individual skill: $2"
      append_unique SELECTED_OPTIONAL "$requested"; EXPLICIT_SELECTION=1; shift 2 ;;
    --no-roots) NO_ROOTS=1; EXPLICIT_SELECTION=1; shift ;;
    --all) ALL=1; EXPLICIT_SELECTION=1; shift ;;
    --copy) COPY=1; shift ;;
    -y) YES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done
[ "$NO_ROOTS" -eq 0 ] || [ "${#SELECTED_ROOTS[@]}" -eq 0 ] || fail '--no-roots cannot be combined with --root'
if [ "$ALL" -eq 1 ] && { [ "$NO_ROOTS" -eq 1 ] || [ "${#SELECTED_ROOTS[@]}" -gt 0 ] || [ "${#SELECTED_OPTIONAL[@]}" -gt 0 ]; }; then
  fail '--all cannot be combined with skill selections'
fi

agent_dir() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    codex) printf '%s\n' "$HOME/.codex/skills" ;;
    cursor) printf '%s\n' "$HOME/.cursor/skills" ;;
    opencode) printf '%s\n' "$HOME/.config/opencode/skills" ;;
  esac
}
source_for() {
  case "$1" in
    fudge-design|fudge-ux|fudge-ship|fudge-review) printf '%s/%s\n' "$BUILD_DIR" "$1" ;;
    *) printf '%s/%s\n' "$SCRIPT_DIR" "$1" ;;
  esac
}
is_known_name() {
  case "$1" in fudge-design|fudge-ux|fudge-ship|fudge-review) return 0 ;; esac
  local short="${1#fudge-}"
  [ "$1" = "fudge-$short" ] && contains "$short" "${OPTIONAL[@]}"
}
owned_copy() {
  [ -d "$1" ] && [ ! -L "$1" ] && [ -f "$1/.fudge-installer" ] &&
    [ "$(cat "$1/.fudge-installer")" = "$SCRIPT_DIR" ] && is_known_name "$(basename "$1")"
}
owned_link() {
  [ -L "$1" ] || return 1
  local name="$(basename "$1")" expected
  is_known_name "$name" || return 1
  expected="$(source_for "$name")"
  [ "$(readlink "$1")" = "$expected" ] && return 0
  # Earlier installer versions linked roots, and review as an optional skill, to source folders.
  case "$name" in
    fudge-design|fudge-ux|fudge-ship|fudge-review) [ "$(readlink "$1")" = "$SCRIPT_DIR/$name" ] ;;
    *) return 1 ;;
  esac
}
install_state() {
  local dest="$1" src="$2"
  if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then note new
  elif [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    if [ "$COPY" -eq 0 ]; then note current; else note update; fi
  elif owned_link "$dest" || owned_copy "$dest"; then note update
  else note foreign
  fi
}

# The full-screen picker is deliberately self-contained: the command-line and
# plain-terminal paths below keep working without terminal control sequences.
ui_terminal_ready() {
  [ -t 0 ] && [ -t 1 ] && [ "${TERM:-dumb}" != dumb ] || return 1
  case "${TERM:-}" in
    xterm*|screen*|tmux*|rxvt*|ansi*|linux*|alacritty*|wezterm*|kitty*|iterm*) ;;
    *) return 1 ;;
  esac
  local size
  size="$(stty size 2>/dev/null)" || return 1
  UI_ROWS="${size%% *}"; UI_COLS="${size##* }"
  [ "$UI_ROWS" -ge 23 ] && [ "$UI_COLS" -ge 40 ]
}

ui_cleanup() {
  [ "${UI_ACTIVE:-0}" -eq 1 ] || return 0
  stty "$UI_STTY" 2>/dev/null || true
  printf '\033[0m\033[?25h\033[?1049l'
  UI_ACTIVE=0
}

ui_line() {
  local label="$1" kind="${2:-normal}" style=''
  case "$kind" in
    title|section) style='1;35' ;;
    muted) style='2' ;;
    focus) style='1;7' ;;
    alert) style='1;33' ;;
    error) style='1;31' ;;
  esac
  if [ "$UI_COLOR" -eq 1 ] && [ -n "$style" ]; then
    printf '\033[%sm%-*.*s\033[0m\n' "$style" "$UI_COLS" "$UI_COLS" "$label"
  else
    printf '%-*.*s\n' "$UI_COLS" "$UI_COLS" "$label"
  fi
}

ui_display_dir() {
  local path
  path="$(agent_dir "$1")"
  case "$path" in
    "$HOME"/*) printf '~%s\n' "${path#"$HOME"}" ;;
    *) printf '%s\n' "$path" ;;
  esac
}

ui_count_states() {
  UI_NEW=0 UI_UPDATE=0 UI_CURRENT=0 UI_FOREIGN=0 UI_FIRST_FOREIGN=''
  local target name dest src state i
  for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do
    [ "${UI_AGENT[$i]}" -eq 1 ] || continue
    target="${AGENT_NAMES[$i]}"
    for name in "${UI_NAMES[@]}"; do
      dest="$(agent_dir "$target")/$name"; src="$(source_for "$name")"
      state="$(install_state "$dest" "$src")"
      case "$state" in
        new) UI_NEW=$((UI_NEW+1)) ;;
        update) UI_UPDATE=$((UI_UPDATE+1)) ;;
        current) UI_CURRENT=$((UI_CURRENT+1)) ;;
        foreign) UI_FOREIGN=$((UI_FOREIGN+1)); [ -n "$UI_FIRST_FOREIGN" ] || UI_FIRST_FOREIGN="$dest" ;;
      esac
    done
  done
}

ui_collect() {
  UI_NAMES=() UI_AGENT_COUNT=0 UI_ROOT_COUNT=0 UI_OPT_COUNT=0 UI_TARGETS=''
  local i name
  for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do
    [ "${UI_AGENT[$i]}" -eq 1 ] || continue
    UI_AGENT_COUNT=$((UI_AGENT_COUNT+1))
    name="${AGENT_NAMES[$i]}"
    [ -z "$UI_TARGETS" ] || UI_TARGETS="$UI_TARGETS, "
    UI_TARGETS="$UI_TARGETS$name"
  done
  for ((i=0; i<${#ROOTS[@]}; i++)); do
    [ "${UI_ROOT[$i]}" -eq 1 ] || continue
    UI_NAMES+=("fudge-${ROOTS[$i]}"); UI_ROOT_COUNT=$((UI_ROOT_COUNT+1))
  done
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do
    [ "${UI_OPT[$i]}" -eq 1 ] || continue
    UI_NAMES+=("fudge-${OPTIONAL[$i]}"); UI_OPT_COUNT=$((UI_OPT_COUNT+1))
  done
  ui_count_states
}

ui_filter_optional() {
  UI_MATCHES=()
  local i lowered
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do
    lowered="$(printf '%s' "${OPTIONAL[$i]}" | tr '[:upper:]' '[:lower:]')"
    case "$lowered" in *"$UI_SEARCH"*) UI_MATCHES+=("$i") ;; esac
  done
  if [ "${#UI_MATCHES[@]}" -eq 0 ]; then UI_OPT_POS=-1
  elif [ "$UI_OPT_POS" -lt 0 ] || [ "$UI_OPT_POS" -ge "${#UI_MATCHES[@]}" ]; then UI_OPT_POS=0; fi
  UI_OPT_SCROLL=0
}

ui_render_choice() {
  local label="$1" selected="$2" focused="$3" marker=' ' check=' '
  [ "$selected" -eq 0 ] || check="$UI_CHECK"
  if [ "$focused" -eq 1 ]; then marker="$UI_ARROW"; ui_line "  $marker [$check] $label" focus
  else ui_line "  $marker [$check] $label"; fi
}

ui_render_optional() {
  local i index end visible selected=0
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do [ "${UI_OPT[$i]}" -eq 0 ] || selected=$((selected+1)); done
  ui_line "  $selected selected  ·  / search" muted
  if [ "$UI_SEARCH_MODE" -eq 1 ]; then
    ui_line "  Search: $UI_SEARCH$UI_CURSOR" focus
  elif [ -n "$UI_SEARCH" ]; then
    ui_line "  Filter: $UI_SEARCH  ·  / to edit" muted
  else
    ui_line ''
  fi
  visible=$((UI_ROWS-13)); [ "$visible" -le 12 ] || visible=12
  [ "$visible" -ge 1 ] || visible=1
  if [ "$UI_OPT_POS" -ge $((UI_OPT_SCROLL+visible)) ]; then UI_OPT_SCROLL=$((UI_OPT_POS-visible+1)); fi
  if [ "$UI_OPT_POS" -ge 0 ] && [ "$UI_OPT_POS" -lt "$UI_OPT_SCROLL" ]; then UI_OPT_SCROLL="$UI_OPT_POS"; fi
  end=$((UI_OPT_SCROLL+visible)); [ "$end" -le "${#UI_MATCHES[@]}" ] || end="${#UI_MATCHES[@]}"
  if [ "${#UI_MATCHES[@]}" -eq 0 ]; then ui_line '  No matching individual skills.' muted; fi
  for ((i=UI_OPT_SCROLL; i<end; i++)); do
    index="${UI_MATCHES[$i]}"
    if [ "$UI_OPT_POS" -eq "$i" ] && [ "$UI_SEARCH_MODE" -eq 0 ]; then
      ui_render_choice "fudge:${OPTIONAL[$index]}" "${UI_OPT[$index]}" 1
    else
      ui_render_choice "fudge:${OPTIONAL[$index]}" "${UI_OPT[$index]}" 0
    fi
  done
  if [ "${#UI_MATCHES[@]}" -gt "$visible" ]; then
    ui_line "  Showing $((UI_OPT_SCROLL+1))-$end of ${#UI_MATCHES[@]}  ·  Up/Down to browse" muted
  fi
}

ui_review_lines() {
  UI_REVIEW_LINES=('  TARGETS')
  local i
  for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do
    [ "${UI_AGENT[$i]}" -eq 0 ] || UI_REVIEW_LINES+=("    ${AGENT_NAMES[$i]}  $(agent_dir "${AGENT_NAMES[$i]}")")
  done
  UI_REVIEW_LINES+=('  ROOT SKILLS')
  if [ "$UI_ROOT_COUNT" -eq 0 ]; then UI_REVIEW_LINES+=('    (none)'); fi
  for ((i=0; i<${#ROOTS[@]}; i++)); do
    [ "${UI_ROOT[$i]}" -eq 0 ] || UI_REVIEW_LINES+=("    fudge:${ROOTS[$i]}")
  done
  UI_REVIEW_LINES+=('  OPTIONAL SKILLS')
  if [ "$UI_OPT_COUNT" -eq 0 ]; then UI_REVIEW_LINES+=('    (none)'); fi
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do
    [ "${UI_OPT[$i]}" -eq 0 ] || UI_REVIEW_LINES+=("    fudge:${OPTIONAL[$i]}")
  done
}

ui_render_counts() {
  local kind="$1"
  if [ "$UI_COLS" -ge 72 ]; then
    ui_line "  $UI_NEW new  ·  $UI_UPDATE update  ·  $UI_CURRENT current  ·  $UI_FOREIGN conflict" "$kind"
  else
    ui_line "  $UI_NEW new  $UI_UPDATE update" "$kind"
    ui_line "  $UI_CURRENT current  $UI_FOREIGN conflict" "$kind"
  fi
}

ui_render_review() {
  ui_collect
  ui_review_lines
  local i end visible path_width path_offset path_lines=0
  ui_line "  ${#UI_NAMES[@]} skill(s) for $UI_AGENT_COUNT agent(s)  ·  $([ "$COPY" -eq 1 ] && printf Copy || printf Symlink)" muted
  ui_line ''
  if [ "$UI_FOREIGN" -gt 0 ]; then
    path_width=$((UI_COLS-4))
    path_lines=$(((${#UI_FIRST_FOREIGN}+path_width-1)/path_width))
  fi
  visible=$((UI_ROWS-14))
  if [ "$UI_FOREIGN" -gt 0 ]; then
    visible=$((UI_ROWS-16-path_lines))
    [ "$UI_COLS" -ge 72 ] || visible=$((visible-1))
  fi
  [ "$visible" -ge 1 ] || visible=1
  UI_REVIEW_VISIBLE="$visible"
  end=$((UI_REVIEW_SCROLL+visible)); [ "$end" -le "${#UI_REVIEW_LINES[@]}" ] || end="${#UI_REVIEW_LINES[@]}"
  for ((i=UI_REVIEW_SCROLL; i<end; i++)); do
    case "${UI_REVIEW_LINES[$i]}" in
      '  TARGETS'|'  ROOT SKILLS'|'  OPTIONAL SKILLS') ui_line "${UI_REVIEW_LINES[$i]}" section ;;
      *) ui_line "${UI_REVIEW_LINES[$i]}" ;;
    esac
  done
  if [ "${#UI_REVIEW_LINES[@]}" -gt "$visible" ]; then
    ui_line "  Showing $((UI_REVIEW_SCROLL+1))-$end of ${#UI_REVIEW_LINES[@]}  ·  Up/Down to browse" muted
  else ui_line ''; fi
  ui_line ''
  if [ "$UI_FOREIGN" -gt 0 ]; then
    ui_render_counts error
    ui_line '  Conflict:' error
    for ((path_offset=0; path_offset<${#UI_FIRST_FOREIGN}; path_offset+=path_width)); do
      ui_line "    ${UI_FIRST_FOREIGN:path_offset:path_width}" error
    done
    ui_line '  Resolve or deselect conflicts before installing.' alert
  else
    ui_render_counts section
  fi
}

ui_render_step() {
  local i label selected
  printf '\033[H\033[2J'
  ui_line '  FUDGE  /  Install skills' title
  ui_line "  Step $UI_STEP of 5" muted
  ui_line ''
  case "$UI_STEP" in
    1)
      ui_line '  Where should Fudge work?' section
      ui_line '  Select one or more agents.' muted
      ui_line ''
      for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do
        ui_render_choice "${AGENT_NAMES[$i]}  $(ui_display_dir "${AGENT_NAMES[$i]}")" "${UI_AGENT[$i]}" "$([ "$UI_AGENT_POS" -eq "$i" ] && printf 1 || printf 0)"
      done ;;
    2)
      ui_line '  Which core skills?' section
      ui_line '  Selected by default. Choose any, or continue with none.' muted
      ui_line ''
      for ((i=0; i<${#ROOTS[@]}; i++)); do
        ui_render_choice "fudge:${ROOTS[$i]}" "${UI_ROOT[$i]}" "$([ "$UI_ROOT_POS" -eq "$i" ] && printf 1 || printf 0)"
      done ;;
    3)
      ui_line '  Add individual skills?' section
      ui_line '  Optional. Select any, or continue with none.' muted
      ui_line ''
      ui_render_optional ;;
    4)
      ui_line '  How should skills be installed?' section
      ui_line '  Choose a method for every selected agent.' muted
      ui_line ''
      for ((i=0; i<2; i++)); do
        if [ "$i" -eq 0 ]; then label=Symlink; selected=$((1-COPY)); else label=Copy; selected="$COPY"; fi
        ui_render_choice "$label" "$selected" "$([ "$UI_METHOD_POS" -eq "$i" ] && printf 1 || printf 0)"
      done ;;
    5)
      ui_line '  Review installation' section
      ui_render_review ;;
  esac
  ui_line ''
  if [ -n "$UI_ERROR" ]; then ui_line "  $UI_ERROR" error; fi
  if [ "$UI_STEP" -eq 5 ]; then
    ui_line '  Up/Down browse' muted
    ui_line '  Esc Back  Enter Install  q Cancel' muted
  elif [ "$UI_STEP" -eq 1 ]; then
    ui_line '  Up/Down move  Space select' muted
    ui_line '  Enter Continue  Esc/q Cancel' muted
  elif [ "$UI_STEP" -eq 3 ]; then
    ui_line '  Up/Down move  Space select  / Search' muted
    ui_line '  Esc Back  Enter Continue  q Cancel' muted
  else
    ui_line '  Up/Down move  Space select' muted
    ui_line '  Esc Back  Enter Continue  q Cancel' muted
  fi
}

ui_read_key() {
  local first rest
  IFS= read -rsn1 first || return 1
  UI_KEY="$first"
  if [ "$first" = $'\033' ]; then
    # Bash 3.2 rejects fractional read -t values. Bytes in an arrow or
    # Shift-Tab sequence are already buffered, so these reads return at once.
    if IFS= read -rsn1 -t 1 rest; then
      UI_KEY="$UI_KEY$rest"
      if [ "$rest" = '[' ] || [ "$rest" = 'O' ]; then
        IFS= read -rsn1 -t 1 rest || rest=''
        UI_KEY="$UI_KEY$rest"
      fi
    fi
  fi
}

ui_move() {
  local direction="$1" max=0
  case "$UI_STEP" in
    1) max=$((${#AGENT_NAMES[@]}-1)); UI_AGENT_POS=$((UI_AGENT_POS+direction)); [ "$UI_AGENT_POS" -ge 0 ] || UI_AGENT_POS="$max"; [ "$UI_AGENT_POS" -le "$max" ] || UI_AGENT_POS=0 ;;
    2) max=$((${#ROOTS[@]}-1)); UI_ROOT_POS=$((UI_ROOT_POS+direction)); [ "$UI_ROOT_POS" -ge 0 ] || UI_ROOT_POS="$max"; [ "$UI_ROOT_POS" -le "$max" ] || UI_ROOT_POS=0 ;;
    3)
      max=$((${#UI_MATCHES[@]}-1)); [ "$max" -ge 0 ] || return 0
      UI_OPT_POS=$((UI_OPT_POS+direction))
      [ "$UI_OPT_POS" -ge 0 ] || UI_OPT_POS="$max"
      [ "$UI_OPT_POS" -le "$max" ] || UI_OPT_POS=0 ;;
    4) UI_METHOD_POS=$((1-UI_METHOD_POS)) ;;
    5)
      max=$((${#UI_REVIEW_LINES[@]}-UI_REVIEW_VISIBLE))
      [ "$max" -ge 0 ] || max=0
      UI_REVIEW_SCROLL=$((UI_REVIEW_SCROLL+direction))
      [ "$UI_REVIEW_SCROLL" -ge 0 ] || UI_REVIEW_SCROLL=0
      [ "$UI_REVIEW_SCROLL" -le "$max" ] || UI_REVIEW_SCROLL="$max" ;;
  esac
}

ui_toggle() {
  local index
  case "$UI_STEP" in
    1) UI_AGENT[$UI_AGENT_POS]=$((1-${UI_AGENT[$UI_AGENT_POS]})) ;;
    2) UI_ROOT[$UI_ROOT_POS]=$((1-${UI_ROOT[$UI_ROOT_POS]})) ;;
    3)
      if [ "$UI_OPT_POS" -ge 0 ] && [ "$UI_OPT_POS" -lt "${#UI_MATCHES[@]}" ]; then
        index="${UI_MATCHES[$UI_OPT_POS]}"; UI_OPT[$index]=$((1-${UI_OPT[$index]}))
      fi ;;
    4) COPY="$UI_METHOD_POS" ;;
  esac
}

ui_install() {
  local i key char
  UI_AGENT=(); UI_ROOT=()
  for ((i=0; i<${#ROOTS[@]}; i++)); do UI_ROOT+=(1); done
  if [ "${#AGENTS[@]}" -eq 0 ]; then
    UI_AGENT=(0 1 0 0)
  else
    for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do
      if contains "${AGENT_NAMES[$i]}" "${AGENTS[@]}"; then UI_AGENT+=(1); else UI_AGENT+=(0); fi
    done
  fi
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do UI_OPT+=(0); done
  UI_STEP=1 UI_AGENT_POS=1 UI_ROOT_POS=0 UI_OPT_POS=0 UI_OPT_SCROLL=0 UI_REVIEW_SCROLL=0
  for ((i=0; i<${#UI_AGENT[@]}; i++)); do
    if [ "${UI_AGENT[$i]}" -eq 1 ]; then UI_AGENT_POS="$i"; break; fi
  done
  UI_METHOD_POS="$COPY" UI_SEARCH='' UI_SEARCH_MODE=0
  UI_ERROR='' UI_CANCELLED=0 UI_CONFIRMED=0 UI_ACTIVE=0
  UI_COLOR=1; [ -z "${NO_COLOR:-}" ] || UI_COLOR=0
  UI_MATCHES=(); ui_filter_optional
  UI_ARROW='›' UI_CHECK='×' UI_CURSOR='█'
  case "$(locale charmap 2>/dev/null)" in
    UTF-8|utf8|UTF8) ;;
    *) UI_ARROW='>' UI_CHECK='x' UI_CURSOR='_' ;;
  esac
  UI_STTY="$(stty -g)" || return 1
  stty -echo -icanon min 1 time 0
  printf '\033[?1049h\033[?25l'
  UI_ACTIVE=1
  trap 'ui_cleanup' EXIT
  trap 'ui_cleanup; exit 130' INT
  trap 'ui_cleanup; exit 143' TERM
  while true; do
    ui_render_step
    ui_read_key || { UI_CANCELLED=1; break; }
    key="$UI_KEY"; UI_ERROR=''
    if [ "$UI_SEARCH_MODE" -eq 1 ]; then
      case "$key" in
        $'\033') UI_SEARCH_MODE=0 ;;
        ''|$'\n'|$'\r') UI_SEARCH_MODE=0 ;;
        $'\177'|$'\b') UI_SEARCH="${UI_SEARCH%?}"; ui_filter_optional ;;
        *)
          if [ "${#key}" -eq 1 ] && [ "$key" != $'\t' ]; then
            char="$(printf '%s' "$key" | tr '[:upper:]' '[:lower:]')"
            UI_SEARCH="$UI_SEARCH$char"; ui_filter_optional
          fi ;;
      esac
      continue
    fi
    case "$key" in
      $'\033[A') ui_move -1 ;;
      $'\033[B') ui_move 1 ;;
      ' ') ui_toggle ;;
      '/') [ "$UI_STEP" -ne 3 ] || UI_SEARCH_MODE=1 ;;
      ''|$'\n'|$'\r')
        case "$UI_STEP" in
          1)
            ui_collect
            if [ "$UI_AGENT_COUNT" -eq 0 ]; then UI_ERROR='Select at least one agent.'
            else UI_STEP=2; fi ;;
          2) UI_STEP=3 ;;
          3)
            ui_collect
            if [ "${#UI_NAMES[@]}" -eq 0 ]; then UI_ERROR='Select at least one skill.'
            else UI_STEP=4; fi ;;
          4) UI_STEP=5; UI_REVIEW_SCROLL=0 ;;
          5)
            ui_collect
            if [ "$UI_FOREIGN" -gt 0 ]; then UI_ERROR='Resolve conflicts before installing.'
            else UI_CONFIRMED=1; break; fi ;;
        esac ;;
      $'\033')
        if [ "$UI_STEP" -eq 1 ]; then UI_CANCELLED=1; break
        else UI_STEP=$((UI_STEP-1)); fi ;;
      q|Q|$'\004') UI_CANCELLED=1; break ;;
    esac
  done
  ui_cleanup
  trap - EXIT INT TERM
  [ "$UI_CANCELLED" -eq 0 ] || return 0
  AGENTS=() SELECTED_ROOTS=() SELECTED_OPTIONAL=()
  for ((i=0; i<${#AGENT_NAMES[@]}; i++)); do [ "${UI_AGENT[$i]}" -eq 0 ] || AGENTS+=("${AGENT_NAMES[$i]}"); done
  for ((i=0; i<${#ROOTS[@]}; i++)); do [ "${UI_ROOT[$i]}" -eq 0 ] || SELECTED_ROOTS+=("${ROOTS[$i]}"); done
  for ((i=0; i<${#OPTIONAL[@]}; i++)); do [ "${UI_OPT[$i]}" -eq 0 ] || SELECTED_OPTIONAL+=("${OPTIONAL[$i]}"); done
}

# Numbered picker works with macOS Bash 3.2 and keeps defaults on Enter.
pick() {
  local title="$1" choices_name="$2" defaults_name="$3" result_name="$4"
  local -a pick_choices pick_defaults pick_result
  eval "pick_choices=(\"\${${choices_name}[@]}\")"
  eval "pick_defaults=(\"\${${defaults_name}[@]}\")"
  local i choice answer token
  note "$title"
  for ((i=0; i<${#pick_choices[@]}; i++)); do
    choice="${pick_choices[$i]}"
    if contains "$choice" "${pick_defaults[@]}"; then printf '  [x] %2d  %s\n' "$((i+1))" "$choice"
    else printf '  [ ] %2d  %s\n' "$((i+1))" "$choice"; fi
  done
  read -rp 'Enter to keep defaults, numbers to select, a for all, or n for none: ' answer || answer=""
  case "$answer" in
    '') pick_result=("${pick_defaults[@]}") ;;
    a|A) pick_result=("${pick_choices[@]}") ;;
    n|N) pick_result=() ;;
    *)
      answer="${answer//,/ }"; pick_result=()
      for token in $answer; do
        [[ "$token" =~ ^[0-9]+$ ]] || fail "invalid selection: $token"
        [ "$token" -ge 1 ] && [ "$token" -le "${#pick_choices[@]}" ] || fail "selection out of range: $token"
        append_unique pick_result "${pick_choices[$((token-1))]}"
      done ;;
  esac
  eval "$result_name=(\"\${pick_result[@]}\")"
}
interactive() { [ -t 0 ] && [ "$YES" -eq 0 ] && [ "$ALL" -eq 0 ]; }
select_install() {
  local -a defaults filtered
  local search_term normalized skill
  if [ "$EXPLICIT_SELECTION" -eq 0 ] &&
     [ "$YES" -eq 0 ] && [ "$ALL" -eq 0 ] &&
     ui_terminal_ready; then
    ui_install
    [ "$UI_CANCELLED" -eq 0 ] || return 0
    return 0
  fi
  if [ "${#AGENTS[@]}" -eq 0 ]; then
    if interactive; then
      defaults=(codex)
      pick 'Choose target agents:' AGENT_NAMES defaults AGENTS
    else
      fail 'specify at least one target agent with -a for a non-interactive install'
    fi
  fi
  [ "${#AGENTS[@]}" -gt 0 ] || fail 'no agents selected'
  if [ "$ALL" -eq 1 ]; then
    SELECTED_ROOTS=("${ROOTS[@]}"); SELECTED_OPTIONAL=("${OPTIONAL[@]}")
  elif [ "$EXPLICIT_SELECTION" -eq 0 ]; then
    if interactive; then
      defaults=("${ROOTS[@]}")
      pick 'Root skills (installed by default):' ROOTS defaults SELECTED_ROOTS
      read -rp 'Browse optional individual skills? [y/N] ' browse_answer || browse_answer=""
      if [ "$browse_answer" = y ] || [ "$browse_answer" = Y ]; then
        while true; do
          read -rp 'Search optional skills (blank for all): ' search_term || search_term=""
          normalized="$(printf '%s' "$search_term" | tr '[:upper:]' '[:lower:]')"
          filtered=()
          for skill in "${OPTIONAL[@]}"; do
            case "$skill" in *"$normalized"*) filtered+=("$skill") ;; esac
          done
          [ "${#filtered[@]}" -gt 0 ] && break
          note "No optional skills match: $search_term"
        done
        defaults=()
        pick 'Optional individual skills (none selected by default):' filtered defaults SELECTED_OPTIONAL
      fi
    else
      SELECTED_ROOTS=("${ROOTS[@]}")
    fi
  elif [ "$NO_ROOTS" -eq 0 ] && [ "${#SELECTED_ROOTS[@]}" -eq 0 ]; then
    SELECTED_ROOTS=("${ROOTS[@]}")
  fi
  [ "${#SELECTED_ROOTS[@]}" -gt 0 ] || [ "${#SELECTED_OPTIONAL[@]}" -gt 0 ] || fail 'no skills selected'
  if interactive && [ "$COPY" -eq 0 ]; then
    read -rp 'Install method: (s)ymlink [default] or (c)opy: ' method_answer || method_answer=""
    [ "$method_answer" != c ] && [ "$method_answer" != C ] || COPY=1
  fi
}

do_install() {
  select_install
  [ "${UI_CANCELLED:-0}" -eq 0 ] || { note 'Aborted.'; return 0; }
  local -a selected=() foreign=()
  local root skill target name src dest state method
  for root in "${SELECTED_ROOTS[@]}"; do selected+=("fudge-$root"); done
  for skill in "${SELECTED_OPTIONAL[@]}"; do selected+=("fudge-$skill"); done
  method=symlink; [ "$COPY" -eq 0 ] || method=copy
  note 'Ready to install:'
  note "  Method: $method"
  note '  Targets:'
  for target in "${AGENTS[@]}"; do note "    $target  $(agent_dir "$target")"; done
  note '  Root skills:'
  for root in "${SELECTED_ROOTS[@]}"; do note "    fudge:$root"; done
  [ "${#SELECTED_ROOTS[@]}" -gt 0 ] || note '    (none)'
  note '  Optional individual skills:'
  for skill in "${SELECTED_OPTIONAL[@]}"; do note "    fudge:$skill"; done
  [ "${#SELECTED_OPTIONAL[@]}" -gt 0 ] || note '    (none)'
  for target in "${AGENTS[@]}"; do
    for name in "${selected[@]}"; do
      src="$(source_for "$name")"; dest="$(agent_dir "$target")/$name"
      state="$(install_state "$dest" "$src")"
      [ "$state" != foreign ] || foreign+=("$dest")
    done
  done
  if [ "${#foreign[@]}" -gt 0 ]; then
    printf 'Existing installs not owned by this installer:\n' >&2
    printf '  %s\n' "${foreign[@]}" >&2
    fail 'move or remove these entries manually, then rerun the installer'
  fi
  if [ "$YES" -eq 0 ] && [ "${UI_CONFIRMED:-0}" -eq 0 ] && [ -t 0 ]; then
    local answer
    read -rp 'Install these skills? [y/N] ' answer || answer=""
    [ "$answer" = y ] || [ "$answer" = Y ] || { note 'Aborted.'; return 0; }
  fi
  if [ "${#SELECTED_ROOTS[@]}" -gt 0 ]; then
    [ -f "$SCRIPT_DIR/scripts/build-root-skills.sh" ] || fail 'root package builder is missing'
    bash "$SCRIPT_DIR/scripts/build-root-skills.sh" "$BUILD_DIR"
    for root in "${SELECTED_ROOTS[@]}"; do
      [ -f "$BUILD_DIR/fudge-$root/SKILL.md" ] || fail "root package fudge-$root was not built"
    done
  fi
  local installed=0 current=0
  for target in "${AGENTS[@]}"; do
    local target_dir="$(agent_dir "$target")"
    mkdir -p "$target_dir"
    for name in "${selected[@]}"; do
      src="$(source_for "$name")"; dest="$target_dir/$name"
      state="$(install_state "$dest" "$src")"
      if [ "$state" = current ]; then current=$((current+1)); continue; fi
      [ "$state" != foreign ] || fail "destination changed during install: $dest"
      if [ -L "$dest" ]; then rm "$dest"
      elif [ -e "$dest" ]; then rm -rf "$dest"; fi
      if [ "$COPY" -eq 1 ]; then
        cp -R "$src" "$dest"
        printf '%s\n' "$SCRIPT_DIR" > "$dest/.fudge-installer"
      else
        ln -s "$src" "$dest"
      fi
      note "Installed $name -> $dest"
      installed=$((installed+1))
    done
  done
  note "Installed $installed skill(s); $current already current."
}

do_list() {
  local target dir entry name kind
  [ "${#AGENTS[@]}" -gt 0 ] || AGENTS=("${AGENT_NAMES[@]}")
  for target in "${AGENTS[@]}"; do
    dir="$(agent_dir "$target")"
    [ -d "$dir" ] || continue
    note "$target ($dir):"
    for entry in "$dir"/*; do
      [ -e "$entry" ] || [ -L "$entry" ] || continue
      name="$(basename "$entry")"
      if owned_link "$entry"; then kind=linked
      elif owned_copy "$entry"; then kind=copy
      else kind=foreign; fi
      note "  $kind  $name"
    done
  done
}

do_remove() {
  local target dir entry answer i
  local -a candidates=() labels=() defaults=() selected=()
  [ "${#AGENTS[@]}" -gt 0 ] || AGENTS=("${AGENT_NAMES[@]}")
  for target in "${AGENTS[@]}"; do
    dir="$(agent_dir "$target")"
    [ -d "$dir" ] || continue
    for entry in "$dir"/*; do
      [ -e "$entry" ] || [ -L "$entry" ] || continue
      if owned_link "$entry" || owned_copy "$entry"; then
        candidates+=("$entry"); labels+=("$target/$(basename "$entry")")
      fi
    done
  done
  [ "${#candidates[@]}" -gt 0 ] || { note 'No installer-owned skills found.'; return 0; }
  if [ "$ALL" -eq 1 ]; then
    selected=("${labels[@]}")
  elif [ -t 0 ]; then
    pick 'Select installed skills to remove:' labels defaults selected
  else
    fail 'remove requires a terminal selection or --all'
  fi
  [ "${#selected[@]}" -gt 0 ] || { note 'Nothing selected.'; return 0; }
  note 'Ready to remove:'
  for ((i=0; i<${#labels[@]}; i++)); do contains "${labels[$i]}" "${selected[@]}" && note "  ${candidates[$i]}"; done
  if [ "$YES" -eq 0 ]; then
    [ -t 0 ] || fail 'confirmation requires a terminal; pass -y'
    read -rp 'Remove these installs? [y/N] ' answer || answer=""
    [ "$answer" = y ] || [ "$answer" = Y ] || { note 'Aborted.'; return 0; }
  fi
  for ((i=0; i<${#labels[@]}; i++)); do
    contains "${labels[$i]}" "${selected[@]}" || continue
    entry="${candidates[$i]}"
    if owned_link "$entry"; then rm "$entry"
    elif owned_copy "$entry"; then rm -rf "$entry"
    else fail "destination changed during remove: $entry"; fi
    note "Removed $entry"
  done
}

case "$SUBCMD" in
  install) do_install ;;
  list) do_list ;;
  remove) do_remove ;;
esac
