# Streamlined Installation - Single Repo, Git Clone + Local Install

## Current State vs Proposed

### Current install.sh
- ✅ Clones repo to `~/.my-harness`
- ✅ Symlinks `.agents/{skills,agents,commands}` to CLI directories
- ❌ Doesn't use Claude Code plugin marketplace system
- ❌ No SpecKit extension installation

### Proposed Approach
- ✅ Git clone (works - no auth needed on company network)
- ✅ Install Claude plugins from local marketplace.json
- ✅ Install SpecKit extensions from local directories
- ✅ Everything self-contained in repo

---

## Proposed Repository Structure

```
harness-tooling/
├── claude-plugins/                    # Claude Code plugins
│   ├── marketplace.json               # Marketplace manifest
│   ├── matd/
│   │   └── .claude-plugin/
│   │       └── plugin.json
│   ├── harness-agents/
│   ├── harness-management-tools/
│   └── ...
│
├── speckit-extensions/                # SpecKit extensions
│   ├── matd/
│   │   ├── extension.yml
│   │   ├── commands/
│   │   └── ...
│   ├── agent-assign/                  # Imported from public
│   │   ├── extension.yml
│   │   └── ...
│   └── v-model/                       # Imported from public
│       ├── extension.yml
│       └── ...
│
├── .agents/                           # Shared source (backward compat)
│   ├── agents/
│   ├── skills/
│   └── commands/
│
├── install.sh                         # New unified installer
└── README.md
```

---

## New install.sh Script

```bash
#!/usr/bin/env bash
# Install harness-tooling: Claude Code plugins + SpecKit extensions
# Usage:
#   bash install.sh                    # interactive
#   bash install.sh --scope user       # user-scoped
#   bash install.sh --scope project    # project-scoped

set -euo pipefail

REPO_URL_SSH="ssh://git@stash.stepstone.com:7999/~minged01/harness-tooling.git"
REPO_URL_HTTPS="https://stash.stepstone.com/scm/~minged01/harness-tooling.git"
DEFAULT_SRC_DIR="${HOME}/.harness-tooling"

SCOPE=""
SRC_DIR="${DEFAULT_SRC_DIR}"
USE_SSH=1  # Default to SSH (works on company network)

log()  { printf '\033[36m[harness]\033[0m %s\n' "$*"; }
die()  { printf '\033[31m[harness] error:\033[0m %s\n' "$*" >&2; exit 1; }

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)    SCOPE="${2:-}"; shift 2 ;;
    --scope=*)  SCOPE="${1#*=}"; shift ;;
    --src-dir)  SRC_DIR="${2:-}"; shift 2 ;;
    --https)    USE_SSH=0; shift ;;
    -h|--help)  echo "Usage: $0 [--scope user|project] [--src-dir DIR]"; exit 0 ;;
    *)          die "unknown flag: $1" ;;
  esac
done

# Interactive scope selection
if [[ -z "$SCOPE" ]]; then
  printf 'Install scope? [u]ser or [p]roject: '
  read -r ans
  case "$ans" in
    u|U|user)    SCOPE="user" ;;
    p|P|project) SCOPE="project" ;;
    *)           die "invalid scope" ;;
  esac
fi

[[ "$SCOPE" == "user" || "$SCOPE" == "project" ]] || die "--scope must be 'user' or 'project'"

# Clone or update repo
SRC_DIR="${SRC_DIR/#\~/$HOME}"
if [[ "$USE_SSH" -eq 1 ]]; then
  REPO_URL="$REPO_URL_SSH"
else
  REPO_URL="$REPO_URL_HTTPS"
fi

if [[ -d "$SRC_DIR/.git" ]]; then
  log "Updating repo at $SRC_DIR"
  git -C "$SRC_DIR" pull --ff-only
else
  log "Cloning $REPO_URL into $SRC_DIR"
  git clone "$REPO_URL" "$SRC_DIR"
fi

# Validate structure
[[ -f "$SRC_DIR/claude-plugins/marketplace.json" ]] || die "marketplace.json not found"
[[ -d "$SRC_DIR/speckit-extensions" ]] || die "speckit-extensions/ not found"

log ""
log "=== Installing Claude Code Plugins ==="

# Add marketplace
log "Adding marketplace..."
claude plugin marketplace add "$SRC_DIR/claude-plugins/marketplace.json"

# Install MATD plugin
log "Installing MATD plugin (scope: $SCOPE)..."
claude plugin install matd --scope "$SCOPE"

log ""
log "=== Installing SpecKit Extensions ==="

# Check if SpecKit is available
if ! command -v specify &> /dev/null; then
  log "SpecKit not found - skipping extension installation"
  log "Install SpecKit first: npm install -g @github/specify-cli"
else
  # Install extensions from local directories
  log "Installing MATD extension..."
  specify extension add --dev "$SRC_DIR/speckit-extensions/matd"
  
  log "Installing agent-assign extension..."
  specify extension add --dev "$SRC_DIR/speckit-extensions/agent-assign"
  
  log "Installing v-model extension..."
  specify extension add --dev "$SRC_DIR/speckit-extensions/v-model"
fi

log ""
log "✓ Installation complete!"
log ""
log "Installed components:"
log "  • Claude marketplace: harness-tooling-marketplace"
log "  • Claude plugin: matd (scope: $SCOPE)"
log "  • SpecKit extensions: matd, agent-assign, v-model"
log ""
log "Update later with:"
log "  git -C $SRC_DIR pull"
log "  claude plugin marketplace update harness-tooling-marketplace"
```

---

## Migration Steps

### 1. Restructure Repository

```bash
cd harness-tooling

# Create new structure
mkdir -p claude-plugins speckit-extensions

# Move Claude Code plugins
mv .agents/plugins claude-plugins/
mv .claude-plugin/marketplace.json claude-plugins/

# Move SpecKit extension
mv spec-kit-multi-agent-tdd speckit-extensions/matd

# Keep .agents/ for backward compatibility (symlinks point here)
```

### 2. Import Public SpecKit Extensions

```bash
cd speckit-extensions

# Clone public extensions
git clone https://github.com/xymelon/spec-kit-agent-assign.git agent-assign-tmp
git clone https://github.com/leocamello/spec-kit-v-model.git v-model-tmp

# Extract to flat directories
cp -r agent-assign-tmp/* agent-assign/
cp -r v-model-tmp/* v-model/

# Cleanup
rm -rf agent-assign-tmp v-model-tmp

# Commit
git add .
git commit -m "feat: import public SpecKit extensions"
```

### 3. Update marketplace.json

```json
{
  "name": "harness-tooling-marketplace",
  "owner": {
    "name": "Stepstone"
  },
  "plugins": [
    {
      "name": "matd",
      "source": "./matd",
      "description": "Multi-Agent Test-Driven Development",
      "version": "1.8.0"
    },
    {
      "name": "harness-agents",
      "source": "./harness-agents",
      "description": "Multi-agent TDD specialist agents",
      "version": "1.0.0"
    }
  ]
}
```

### 4. Update README.md

```markdown
## Installation

```bash
# Clone repository (works without auth on company network)
git clone ssh://git@stash.stepstone.com:7999/~minged01/harness-tooling.git
cd harness-tooling

# Run installer
bash install.sh --scope user

# Or interactive
bash install.sh
```

## Repository Structure

- `claude-plugins/` - Claude Code plugin marketplace
- `speckit-extensions/` - SpecKit extensions (including imported public ones)
- `.agents/` - Shared agent/skill source (backward compat)
```

---

## Benefits

### ✅ Everything in One Repo
- Clone once, install everything
- No external hosting needed
- No ZIP build scripts needed

### ✅ Works on Company Network
- Git clone via SSH (no auth prompt)
- Local file installation (no HTTPS restrictions)
- Self-contained

### ✅ Import Public Extensions
- Fork/vendor public extensions into repo
- Control versions
- Customize if needed
- No external dependencies at install time

### ✅ Clean Structure
```
claude-plugins/          → Claude Code users
speckit-extensions/      → SpecKit users
.agents/                 → Shared source
install.sh               → One script for everything
```

### ✅ Easy Updates
```bash
git -C ~/.harness-tooling pull
claude plugin marketplace update harness-tooling-marketplace
```

---

## Comparison with Current Approach

| Aspect | Current install.sh | Proposed |
|--------|-------------------|----------|
| **Clones repo** | ✅ Yes | ✅ Yes |
| **Claude plugins** | ❌ Symlinks only | ✅ Via marketplace |
| **SpecKit extensions** | ❌ Not installed | ✅ Installed |
| **Public extensions** | ❌ Manual | ✅ Imported in repo |
| **Structure** | `.agents/` flat | `claude-plugins/` + `speckit-extensions/` |
| **Updates** | `git pull` | `git pull` + `plugin update` |

---

## Installation Test

```bash
# User creates project
mkdir my-project
cd my-project
git init

# Run installer
bash <(curl -fsSL https://stash.stepstone.com/.../install.sh) --scope project

# Or if repo already cloned
git clone ssh://git@stash.stepstone.com:7999/~minged01/harness-tooling.git
cd my-project
bash ../harness-tooling/install.sh --scope project
```

**Result:**
- ✅ Claude plugin installed from local marketplace
- ✅ SpecKit extensions installed from local directories
- ✅ All in `.claude/` and `.specify/` (project-scoped)
- ✅ No external downloads needed

---

## Answers to Your Questions

### "Most streamlined way?"
**Git clone + local install script** - everything in one repo, one command

### "Repo readable for everyone in company network?"
**Yes - SSH clone works without auth** (tested)

### "Install list of plugins and extensions?"
**Yes - install.sh does both** (marketplace.json + specify extension add)

### "Kept within the repo?"
**Yes - no external hosting needed** (local paths for everything)

### "Two main folders?"
**Yes - `claude-plugins/` and `speckit-extensions/`**

### "Import public extensions?"
**Yes - git clone → copy → commit** (vendored into repo)
