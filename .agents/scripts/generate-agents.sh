#!/bin/bash
# Generate CLI-specific agent.md files from canonical source + frontmatter specs
# Usage: bash scripts/generate-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$(dirname "$SCRIPT_DIR")"

echo "[generate-agents] Starting agent generation..."
echo "[generate-agents] Base directory: $AGENTS_DIR"

# Clean generated directory
rm -rf "$AGENTS_DIR/generated"
mkdir -p "$AGENTS_DIR/generated/claude" "$AGENTS_DIR/generated/opencode"

# Counters
CLAUDE_COUNT=0
OPENCODE_COUNT=0
WARNINGS=0

# Generate Claude Code agents
echo ""
echo "[generate-agents] Generating Claude Code agents..."
for frontmatter_file in "$AGENTS_DIR/frontmatter/claude"/*.yml; do
    if [ ! -f "$frontmatter_file" ]; then
        echo "[generate-agents] Warning: No frontmatter files found in frontmatter/claude/"
        break
    fi

    agent_name=$(basename "$frontmatter_file" .yml)
    canonical_file="$AGENTS_DIR/canonical/${agent_name}.md"

    if [ ! -f "$canonical_file" ]; then
        echo "[generate-agents] Warning: No canonical file for $agent_name (expected: $canonical_file)"
        WARNINGS=$((WARNINGS + 1))
        continue
    fi

    # Create output directory
    output_dir="$AGENTS_DIR/generated/claude/$agent_name"
    mkdir -p "$output_dir"

    # Combine frontmatter + canonical content
    {
        echo "---"
        cat "$frontmatter_file"
        echo "---"
        echo ""
        cat "$canonical_file"
    } > "$output_dir/agent.md"

    CLAUDE_COUNT=$((CLAUDE_COUNT + 1))
    echo "  ✓ Generated: claude/$agent_name/agent.md"
done

# Generate OpenCode agents
echo ""
echo "[generate-agents] Generating OpenCode agents..."
for frontmatter_file in "$AGENTS_DIR/frontmatter/opencode"/*.yml; do
    if [ ! -f "$frontmatter_file" ]; then
        echo "[generate-agents] Warning: No frontmatter files found in frontmatter/opencode/"
        break
    fi

    agent_name=$(basename "$frontmatter_file" .yml)
    canonical_file="$AGENTS_DIR/canonical/${agent_name}.md"

    if [ ! -f "$canonical_file" ]; then
        echo "[generate-agents] Warning: No canonical file for $agent_name (expected: $canonical_file)"
        WARNINGS=$((WARNINGS + 1))
        continue
    fi

    # Create output directory
    output_dir="$AGENTS_DIR/generated/opencode/$agent_name"
    mkdir -p "$output_dir"

    # Combine frontmatter + canonical content
    {
        echo "---"
        cat "$frontmatter_file"
        echo "---"
        echo ""
        cat "$canonical_file"
    } > "$output_dir/agent.md"

    OPENCODE_COUNT=$((OPENCODE_COUNT + 1))
    echo "  ✓ Generated: opencode/$agent_name/agent.md"
done

# Summary
echo ""
echo "[generate-agents] ═══════════════════════════════════════════"
echo "[generate-agents] Agent generation complete:"
echo "[generate-agents]   Claude Code: $CLAUDE_COUNT agents"
echo "[generate-agents]   OpenCode: $OPENCODE_COUNT agents"
if [ $WARNINGS -gt 0 ]; then
    echo "[generate-agents]   Warnings: $WARNINGS (check logs above)"
fi
echo "[generate-agents] ═══════════════════════════════════════════"

# Create .gitkeep placeholders
touch "$AGENTS_DIR/generated/.gitkeep"

# Exit with warning code if some agents failed
if [ $WARNINGS -gt 0 ]; then
    exit 1
fi

exit 0
