#!/bin/bash
# Links the generic instructions as the user's CLAUDE.md and creates the private personal file.
# Safe to run again. Plugins are installed separately (see README).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
TARGET="$CLAUDE_DIR/CLAUDE.md"
PERSONAL="$HOME/.kings-ai/personal.md"

# The import in global.md points here; a missing file would leave the literal "@path" in the prompt.
create_personal_file() {
  [ -f "$PERSONAL" ] && return
  mkdir -p "$(dirname "$PERSONAL")"
  cp "$ROOT/install/personal.example.md" "$PERSONAL"
  printf 'Personal file created: %s (fill it in)\n' "$PERSONAL"
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

create_personal_file
link_global_instructions
