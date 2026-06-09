#!/usr/bin/env bash
# Install harness-tooling: Claude Code plugins + SpecKit extensions
#
# Everything installed from local repo (no external downloads):
#   - Claude Code plugins via marketplace.json
#   - SpecKit extensions from local directories
#
# Usage:
#   bash install.sh                    # interactive
#   bash install.sh --scope user       # user-scoped
#   bash install.sh --scope project    # project-scoped
#   bash install.sh --src-dir ~/code/harness-tooling

set -euo pipefail

REPO_URL_SSH="ssh://git@stash.stepstone.com:7999/~minged01/harness-tooling.git"
DEFAULT_SRC_DIR="${HOME}/.harness-tooling"

SCOPE=""
SRC_DIR="${DEFAULT_SRC_DIR}"

log()  { printf '\033[36m[harness]\033[0m %s\n' "$*"; }
warn() { printf '\033[33m[harness] warn:\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[31m[harness] error:\033[0m %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Install harness-tooling (Claude Code plugins + SpecKit extensions)

OPTIONS:
  --scope user|project    Installation scope (required if non-interactive)
  --src-dir DIR          Clone/update location (default: ~/.harness-tooling)
  -h, --help             Show this help

EXAMPLES:
  $0                              # Interactive
  $0 --scope user                 # User-scoped (~/.claude)
  $0 --scope project              # Project-scoped (./.claude)
  $0 --scope user --src-dir ~/dev/harness
EOF
  exit "${1:-0}"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)    SCOPE="${2:-}"; shift 2 ;;
    --scope=*)  SCOPE="${1#*=}"; shift ;;
    --src-dir)  SRC_DIR="${2:-}"; shift 2 ;;
    --src-dir=*) SRC_DIR="${1#*=}"; shift ;;
    -h|--help)  usage 0 ;;
    *)          die "unknown flag: $1 (try --help)" ;;
  esac
done

# Interactive scope selection if not provided
if [[ -z "$SCOPE" ]]; then
  printf 'Install scope? [u]ser (~/.claude) or [p]roject (./.claude): '
  read -r ans
  case "$ans" in
    u|U|user)    SCOPE="user" ;;
    p|P|project) SCOPE="project" ;;
    *)           die "invalid scope" ;;
  esac
fi

[[ "$SCOPE" == "user" || "$SCOPE" == "project" ]] || die "--scope must be 'user' or 'project'"

# Expand tilde in path
SRC_DIR="${SRC_DIR/#\~/$HOME}"

log ""
log "=== Harness Tooling Installation ==="
log "Scope:  $SCOPE"
log "Source: $SRC_DIR"
log ""

# Clone or update repository
if [[ -d "$SRC_DIR/.git" ]]; then
  log "[1/3] Updating repository..."
  git -C "$SRC_DIR" pull --ff-only
elif [[ -e "$SRC_DIR" ]]; then
  die "$SRC_DIR exists but is not a git repo; move it aside or pass --src-dir"
else
  log "[1/3] Cloning repository..."
  git clone "$REPO_URL_SSH" "$SRC_DIR"
fi

# Validate repository structure
[[ -f "$SRC_DIR/claude-plugins/marketplace.json" ]] || die "claude-plugins/marketplace.json not found"
[[ -d "$SRC_DIR/speckit-extensions" ]] || die "speckit-extensions/ not found"

log ""
log "[2/3] Installing Claude Code plugins..."

# Add marketplace
log "  • Adding marketplace..."
if claude plugin marketplace add "$SRC_DIR/claude-plugins/marketplace.json"; then
  log "    ✓ Marketplace added: harness-tooling-marketplace"
else
  warn "  Marketplace add failed (may already exist)"
fi

# Install MATD plugin
log "  • Installing MATD plugin..."
if claude plugin install matd --scope "$SCOPE"; then
  log "    ✓ MATD plugin installed (scope: $SCOPE)"
else
  warn "  MATD plugin install failed (may already exist)"
fi

log ""
log "[3/3] Installing SpecKit extensions..."

# Check if SpecKit CLI is available
if ! command -v specify &> /dev/null; then
  warn "SpecKit CLI not found - skipping extension installation"
  warn "Install SpecKit: npm install -g @github/specify-cli"
else
  # Initialize SpecKit if not already done
  if [[ ! -d ".specify" ]]; then
    log "  • Initializing SpecKit..."
    specify init . --integration claude --force || warn "SpecKit init failed (may already exist)"
  fi

  # Install MATD extension
  log "  • Installing MATD extension..."
  if specify extension add --dev "$SRC_DIR/speckit-extensions/matd"; then
    log "    ✓ MATD extension installed"
  else
    warn "  MATD extension install failed (may already exist)"
  fi

  # Install agent-assign extension
  log "  • Installing agent-assign extension..."
  if specify extension add --dev "$SRC_DIR/speckit-extensions/agent-assign"; then
    log "    ✓ agent-assign extension installed"
  else
    warn "  agent-assign extension install failed (may already exist)"
  fi

  # Install v-model extension
  log "  • Installing v-model extension..."
  if specify extension add --dev "$SRC_DIR/speckit-extensions/v-model"; then
    log "    ✓ v-model extension installed"
  else
    warn "  v-model extension install failed (may already exist)"
  fi
fi

log ""
log "✓ Installation complete!"
log ""
log "Installed components:"
log "  • Claude marketplace:    harness-tooling-marketplace"
log "  • Claude plugin:         matd (scope: $SCOPE)"
if command -v specify &> /dev/null; then
  log "  • SpecKit extensions:    matd, agent-assign, v-model"
fi
log ""
log "Source directory: $SRC_DIR"
log ""
log "Update later with:"
log "  git -C $SRC_DIR pull"
log "  claude plugin marketplace update harness-tooling-marketplace"
log ""
log "Verify installation:"
log "  cat .claude/settings.json              # Should show matd plugin"
log "  specify extension list                 # Should list extensions"
