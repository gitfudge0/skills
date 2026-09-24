#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_HOME="$(mktemp -d)"
trap 'rm -rf "$TEST_HOME"' EXIT
export HOME="$TEST_HOME"
INSTALLER="$REPO_DIR/install.sh"

assert_link() { [ -L "$1" ] || { printf 'Expected symlink: %s\n' "$1" >&2; exit 1; }; }
assert_missing() { [ ! -e "$1" ] && [ ! -L "$1" ] || { printf 'Expected absent: %s\n' "$1" >&2; exit 1; }; }
assert_entry_count() {
  local count
  count="$(find "$1" -mindepth 1 -maxdepth 1 | wc -l | tr -d '[:space:]')"
  [ "$count" = "$2" ] || { printf 'Expected %s entries in %s, found %s\n' "$2" "$1" "$count" >&2; exit 1; }
}

# A nonterminal install must name its targets before creating anything.
if bash "$INSTALLER" install -y > "$TEST_HOME/no-agent.log" 2>&1; then
  printf 'Expected a missing-agent failure\n' >&2; exit 1
fi
assert_missing "$HOME/.codex"
assert_missing "$HOME/.claude"
assert_missing "$HOME/.cursor"
assert_missing "$HOME/.config/opencode"

# Nonterminal invocation with an explicit agent installs exactly the three roots.
bash "$INSTALLER" install -a codex > "$TEST_HOME/default.log"
grep -q 'fudge:design' "$TEST_HOME/default.log"
grep -q 'fudge:ship' "$TEST_HOME/default.log"
grep -q 'fudge:review' "$TEST_HOME/default.log"
assert_link "$HOME/.codex/skills/fudge-design"
assert_link "$HOME/.codex/skills/fudge-ship"
assert_link "$HOME/.codex/skills/fudge-review"
assert_entry_count "$HOME/.codex/skills" 3
assert_missing "$HOME/.codex/skills/fudge-test-plan"
assert_missing "$HOME/.claude/skills/fudge-design"
[ -f "$HOME/.codex/skills/fudge-design/SKILL.md" ]
[ -f "$HOME/.codex/skills/fudge-ship/SKILL.md" ]
[ -f "$HOME/.codex/skills/fudge-review/SKILL.md" ]

# Review is a root, so the individual-skill option rejects it.
if bash "$INSTALLER" install -a cursor --skill review > "$TEST_HOME/review-individual.log" 2>&1; then
  printf 'Expected --skill review to fail\n' >&2; exit 1
fi
grep -q 'use --root review' "$TEST_HOME/review-individual.log"
assert_missing "$HOME/.cursor/skills"

# A symlink made by the previous installer is migrated to the bundled root.
mkdir -p "$HOME/.claude/skills"
ln -s "$REPO_DIR/fudge-design" "$HOME/.claude/skills/fudge-design"
bash "$INSTALLER" install -a claude --root design > "$TEST_HOME/migrate.log"
[ "$(readlink "$HOME/.claude/skills/fudge-design")" = "$REPO_DIR/.fudge-build/fudge-design" ]
assert_missing "$HOME/.claude/skills/fudge-ship"

# A preexisting optional review link is recognized and upgraded to the root package.
ln -s "$REPO_DIR/fudge-review" "$HOME/.claude/skills/fudge-review"
bash "$INSTALLER" install -a claude --root review > "$TEST_HOME/review-migrate.log"
[ "$(readlink "$HOME/.claude/skills/fudge-review")" = "$REPO_DIR/.fudge-build/fudge-review" ]
assert_missing "$HOME/.claude/skills/fudge-ship"

# Individuals are separate installs and --no-roots does not add roots elsewhere.
bash "$INSTALLER" install -a cursor --no-roots --skill test-plan > "$TEST_HOME/individual.log"
grep -q 'fudge:test-plan' "$TEST_HOME/individual.log"
assert_link "$HOME/.cursor/skills/fudge-test-plan"
assert_missing "$HOME/.cursor/skills/fudge-design"
assert_missing "$HOME/.cursor/skills/fudge-ship"
assert_missing "$HOME/.cursor/skills/fudge-review"

# An individual selection alone augments the default roots.
bash "$INSTALLER" install -a codex --skill test-plan > "$TEST_HOME/augment.log"
assert_link "$HOME/.codex/skills/fudge-design"
assert_link "$HOME/.codex/skills/fudge-ship"
assert_link "$HOME/.codex/skills/fudge-review"
assert_link "$HOME/.codex/skills/fudge-test-plan"

# --all includes three roots and the 18 optional skills.
bash "$INSTALLER" install -a claude --all > "$TEST_HOME/all.log"
assert_entry_count "$HOME/.claude/skills" 21
assert_link "$HOME/.claude/skills/fudge-review"

# Selecting review as a root installs it alone in a fresh target.
bash "$INSTALLER" install -a opencode --root review > "$TEST_HOME/review-only.log"
assert_link "$HOME/.config/opencode/skills/fudge-review"
assert_entry_count "$HOME/.config/opencode/skills" 1

# Copies are marked as owned so a later install can update them.
bash "$INSTALLER" install -a opencode --root design --copy > "$TEST_HOME/copy.log"
[ -f "$HOME/.config/opencode/skills/fudge-design/.fudge-installer" ]
assert_missing "$HOME/.config/opencode/skills/fudge-ship"
bash "$INSTALLER" install -a opencode --root design --copy > "$TEST_HOME/copy-update.log"

# A same-name foreign entry is never overwritten or removed, even with -y.
mkdir -p "$HOME/.codex/skills/fudge-ui-mock"
printf 'keep\n' > "$HOME/.codex/skills/fudge-ui-mock/foreign.txt"
if bash "$INSTALLER" install -a codex --no-roots --skill ui-mock -y > "$TEST_HOME/conflict.log" 2>&1; then
  printf 'Expected a foreign-install conflict\n' >&2; exit 1
fi
[ "$(cat "$HOME/.codex/skills/fudge-ui-mock/foreign.txt")" = keep ]
bash "$INSTALLER" remove -a codex --all -y > "$TEST_HOME/remove.log"
assert_missing "$HOME/.codex/skills/fudge-design"
assert_missing "$HOME/.codex/skills/fudge-ship"
assert_missing "$HOME/.codex/skills/fudge-review"
[ "$(cat "$HOME/.codex/skills/fudge-ui-mock/foreign.txt")" = keep ]

printf 'Installer smoke test passed.\n'
