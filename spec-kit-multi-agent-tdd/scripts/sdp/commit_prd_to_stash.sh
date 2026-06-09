#!/usr/bin/env bash
# commit_prd_to_stash.sh
# Stages and commits a PRD markdown file and its context file to the agent
# workspace git repository. The human pushes — no auto-push (FR-053b).
#
# Usage:
#   ./commit_prd_to_stash.sh \
#     --workspace-root <absolute-path-to-agent-workspace-repo> \
#     --prd-id PRD-001 \
#     --slug <url-safe-slug>

set -euo pipefail

# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
usage() {
  cat <<EOF
Usage: $(basename "$0") --workspace-root <path> --prd-id <id> --slug <slug>

Options:
  --workspace-root <path>   Absolute path to the agent workspace git repository
  --prd-id <id>             PRD identifier, e.g. PRD-001
  --slug <slug>             URL-safe slug matching the PRD filename, e.g. user-auth
  -h, --help                Show this help message and exit

Example:
  $(basename "$0") --workspace-root /home/user/my-workspace --prd-id PRD-001 --slug user-auth

What this script does:
  1. Verifies that --workspace-root is a git repository.
  2. Locates product/prd/<prd-id>-<slug>.md and
     product/context/<prd-id>-<slug>.context.md inside the workspace.
  3. Stages both files (warns if either is missing).
  4. Commits with message: feat(prd): add <prd-id>-<slug>
  5. Prints the commit hash and a reminder to push manually.

No git push is performed — the human pushes (FR-053b).
EOF
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
WORKSPACE_ROOT=""
PRD_ID=""
SLUG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --workspace-root)
      WORKSPACE_ROOT="${2:-}"
      shift 2
      ;;
    --prd-id)
      PRD_ID="${2:-}"
      shift 2
      ;;
    --slug)
      SLUG="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Validate required args
# ---------------------------------------------------------------------------
if [ -z "$WORKSPACE_ROOT" ] || [ -z "$PRD_ID" ] || [ -z "$SLUG" ]; then
  echo "ERROR: --workspace-root, --prd-id, and --slug are all required." >&2
  usage >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Precondition: workspace-root must be a git repository
# ---------------------------------------------------------------------------
if ! git -C "$WORKSPACE_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
  cat >&2 <<EOF
ERROR: The agent workspace repo does not exist or is not a git repository.
       Path: ${WORKSPACE_ROOT}

A Staff Engineer or Engineering Manager must provision it from the
workspace-template before running this command. See FR-053a.
EOF
  exit 1
fi

# ---------------------------------------------------------------------------
# Derive file paths (relative to workspace root)
# ---------------------------------------------------------------------------
STEM="${PRD_ID}-${SLUG}"
PRD_FILE="product/prd/${STEM}.md"
CONTEXT_FILE="product/context/${STEM}.context.md"

# ---------------------------------------------------------------------------
# Warn if files are missing, but continue
# ---------------------------------------------------------------------------
missing=0
if [ ! -f "${WORKSPACE_ROOT}/${PRD_FILE}" ]; then
  echo "WARNING: PRD file not found: ${PRD_FILE}" >&2
  missing=$((missing + 1))
fi
if [ ! -f "${WORKSPACE_ROOT}/${CONTEXT_FILE}" ]; then
  echo "WARNING: Context file not found: ${CONTEXT_FILE} (may not exist yet)" >&2
  missing=$((missing + 1))
fi

if [ "$missing" -eq 2 ]; then
  echo "ERROR: Neither PRD file nor context file exists — nothing to commit." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Stage files
# ---------------------------------------------------------------------------
git -C "$WORKSPACE_ROOT" add "$PRD_FILE" "$CONTEXT_FILE" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Check whether anything is actually staged
# ---------------------------------------------------------------------------
if git -C "$WORKSPACE_ROOT" diff --cached --quiet; then
  echo "Nothing to commit — files are up to date."
  exit 0
fi

# ---------------------------------------------------------------------------
# Commit
# ---------------------------------------------------------------------------
COMMIT_MSG="feat(prd): add ${STEM}"
if ! git -C "$WORKSPACE_ROOT" commit -m "$COMMIT_MSG"; then
  echo "ERROR: git commit failed." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
COMMIT_HASH=$(git -C "$WORKSPACE_ROOT" rev-parse --short HEAD)

cat <<EOF
✓ Committed: ${STEM}
✓ Commit hash: ${COMMIT_HASH}
⚠  PUSH REQUIRED: Run the following to push to Stash:
   git -C ${WORKSPACE_ROOT} push
EOF

exit 0
