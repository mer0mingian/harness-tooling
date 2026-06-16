#!/usr/bin/env bash
# install.sh: One-time setup for harness-tooling
#
# Run this from the harness-tooling directory to:
#   1. Check prerequisites (git, claude, uv)
#   2. Install specify CLI if missing
#   3. Add harness-setup to PATH
#   4. Set HARNESS_TOOLING_DIR environment variable
#
# Usage:
#   cd ~/.harness-tooling  # or wherever you cloned harness-tooling
#   ./install.sh

set -euo pipefail

log()  { printf '\033[36m[install]\033[0m %s\n' "$*"; }
warn() { printf '\033[33m[warn]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

log ""
log "=== Harness Tooling Installation ==="
log ""

# Determine installation directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log "Installation directory: $SCRIPT_DIR"
log ""

# [1/5] Check prerequisites
log "[1/5] Checking prerequisites..."

# Check git
if ! command -v git &>/dev/null; then
  die "git not found. Install git first."
fi
log "  ✓ git: $(git --version | head -1)"

# Check claude CLI
if ! command -v claude &>/dev/null; then
  die "Claude Code CLI not found. Install from claude.ai/code"
fi
log "  ✓ claude: $(claude --version 2>/dev/null || echo 'installed')"

# Check uv
if ! command -v uv &>/dev/null; then
  die "uv not found. Install from https://docs.astral.sh/uv/"
fi
log "  ✓ uv: $(uv --version)"

# [2/5] Install specify if missing
log ""
log "[2/5] Checking SpecKit CLI..."

if command -v specify &>/dev/null; then
  SPECIFY_VERSION=$(specify --version 2>/dev/null || echo "unknown")
  log "  ✓ specify: $SPECIFY_VERSION"

  # Auto-upgrade to v0.10.2
  log "  • Running specify self upgrade..."
  specify self upgrade 2>/dev/null || log "    • Upgrade skipped (may already be latest)"
else
  log "  • specify not found, installing..."
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.10.2 || die "Failed to install specify"
  log "  ✓ specify installed"

  # Verify installation
  specify self check || warn "specify self check reported issues"
fi

# [3/5] Detect shell
log ""
log "[3/5] Detecting shell..."

SHELL_TYPE=""
SHELL_RC=""

# Detect current shell
if [[ -n "${ZSH_VERSION:-}" ]] || [[ "$SHELL" == *"zsh"* ]]; then
  SHELL_TYPE="zsh"
  SHELL_RC="$HOME/.zshrc"
elif [[ -n "${BASH_VERSION:-}" ]] || [[ "$SHELL" == *"bash"* ]]; then
  SHELL_TYPE="bash"
  SHELL_RC="$HOME/.bashrc"
else
  die "Unsupported shell. Expected bash or zsh (WSL2/Ubuntu or macOS)."
fi

log "  ✓ Detected: $SHELL_TYPE"
log "  ✓ Config:   $SHELL_RC"

# [4/5] Update shell config
log ""
log "[4/5] Updating $SHELL_RC..."

# Create shell config if it doesn't exist
touch "$SHELL_RC"

# Check if harness-tooling block already exists
if grep -q "# harness-tooling setup" "$SHELL_RC"; then
  log "  • Configuration already exists, updating..."

  # Remove old block
  sed -i.bak '/# harness-tooling setup/,/# end harness-tooling/d' "$SHELL_RC"
fi

# Add new configuration block
cat >> "$SHELL_RC" << EOF

# harness-tooling setup
export HARNESS_TOOLING_DIR="$SCRIPT_DIR"
export PATH="\$HARNESS_TOOLING_DIR/bin:\$PATH"
# end harness-tooling
EOF

log "  ✓ Added HARNESS_TOOLING_DIR=$SCRIPT_DIR"
log "  ✓ Added $SCRIPT_DIR/bin to PATH"

# [5/5] Make CLI executable
log ""
log "[5/5] Setting up CLI..."

chmod +x "$SCRIPT_DIR/bin/harness-setup"
log "  ✓ harness-setup is executable"

# Export for current session
export HARNESS_TOOLING_DIR="$SCRIPT_DIR"
export PATH="$SCRIPT_DIR/bin:$PATH"

log ""
log "✓ Installation complete!"
log ""
log "Configuration:"
log "  HARNESS_TOOLING_DIR=$SCRIPT_DIR"
log "  PATH includes: $SCRIPT_DIR/bin"
log ""
log "Next steps:"
log "  1. Restart your shell (or run: source $SHELL_RC)"
log "  2. cd to your project directory"
log "  3. Run: harness-setup"
log "  4. Optional: harness-setup --init-agent-workspace"
log ""
log "Update later with:"
log "  harness-setup update"
log ""
