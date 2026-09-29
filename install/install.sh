#!/bin/bash
# Links the generic instructions as the user's CLAUDE.md and creates the private files it imports
# (personal context and paths map). Safe to run again. Plugins are installed separately (see README).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
TARGET="$CLAUDE_DIR/CLAUDE.md"
PRIVATE_DIR="$HOME/.kings-ai"

# global.md imports these; a missing file would leave the literal "@path" in the prompt.
create_private_file() {
  local target="$PRIVATE_DIR/$1"
  [ -f "$target" ] && return
  mkdir -p "$PRIVATE_DIR"
  cp "$ROOT/install/$2" "$target"
  printf 'Created %s (fill it in)\n' "$target"
}

# The defaults ship with the repo; a fixed link lets global.md import them without relying on how
# a relative import resolves through the CLAUDE.md symlink.
link_path_defaults() {
  mkdir -p "$PRIVATE_DIR"
  ln -sfn "$ROOT/claude-md/paths.md" "$PRIVATE_DIR/paths.default.md"
}

# An existing CLAUDE.md is kept as a dated backup, so its content can be moved to personal.md.
link_global_instructions() {
  mkdir -p "$CLAUDE_DIR"
  if [ -L "$TARGET" ] && [ "$(readlink "$TARGET")" = "$ROOT/claude-md/global.md" ]; then
    printf 'CLAUDE.md already linked\n'
    return
  fi
  if [ -e "$TARGET" ]; then
    mv "$TARGET" "$TARGET.$(date +%Y-%m-%d_%H-%M-%S).bak"
    printf 'Previous CLAUDE.md kept as a .bak next to it\n'
  fi
  ln -s "$ROOT/claude-md/global.md" "$TARGET"
  printf 'CLAUDE.md -> %s\n' "$ROOT/claude-md/global.md"
}

create_private_file personal.md personal.example.md
create_private_file paths.md paths.example.md
link_path_defaults
link_global_instructions
