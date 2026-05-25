# Agent Architecture - Dual-CLI Template Generation

This directory implements template-based agent generation to support both Claude Code and OpenCode with a single source of truth.

## Problem

Claude Code and OpenCode have **incompatible agent frontmatter schemas**:

| Field | Claude Code | OpenCode | Compatible? |
|-------|-------------|----------|-------------|
| `name` | ✅ Required | ❌ Uses filename | ❌ |
| `description` | ✅ | ✅ | ✅ |
| `skills` | ✅ Array | ❌ | ❌ |
| `tools` | ✅ Array | ❌ | ❌ |
| `memory` | ✅ Boolean | ❌ | ❌ |
| `mode` | ❌ | ✅ (subagent/primary) | ❌ |
| `permission` | ❌ | ✅ Dict (read/write/bash) | ❌ |
| `temperature` | ❌ | ✅ Float | ❌ |

**Conclusion**: Cannot use a single agent.md file for both CLIs.

## Solution: Template Generation

Generate CLI-specific agent.md files from canonical source at **build time**.

### Directory Structure

```
.agents/
├── canonical/                    # Source of truth (human-maintained)
│   ├── matd-qa.md               # Pure markdown persona (no frontmatter)
│   ├── matd-dev.md
│   ├── matd-architect.md
│   ├── matd-critical-thinker.md
│   ├── matd-orchestrator.md
│   └── matd-specifier.md
│
├── frontmatter/                  # CLI-specific specifications
│   ├── claude/                   # Claude Code YAML specs
│   │   ├── matd-qa.yml
│   │   ├── matd-dev.yml
│   │   ├── matd-architect.yml
│   │   ├── matd-critical-thinker.yml
│   │   ├── matd-orchestrator.yml (complete, but Claude Code doesn't need orchestrator)
│   │   └── matd-specifier.yml
│   └── opencode/                 # OpenCode YAML specs
│       ├── matd-qa.yml
│       ├── matd-dev.yml
│       ├── matd-architect.yml
│       ├── matd-critical-thinker.yml
│       ├── matd-orchestrator.yml
│       └── matd-specifier.yml
│
├── generated/                    # Generated at build time (gitignored)
│   ├── .gitkeep
│   ├── claude/
│   │   ├── matd-qa/
│   │   │   └── agent.md         # canonical/matd-qa.md + frontmatter/claude/matd-qa.yml
│   │   ├── matd-dev/
│   │   │   └── agent.md
│   │   └── ...
│   └── opencode/
│       ├── matd-qa/
│       │   └── agent.md         # canonical/matd-qa.md + frontmatter/opencode/matd-qa.yml
│       ├── matd-dev/
│       │   └── agent.md
│       └── ...
│
├── agents/                       # DEPRECATED: Legacy combined agents
│   ├── matd-qa.md               # Symlink → generated/opencode/matd-qa/agent.md
│   ├── matd-dev.md              # Symlink → generated/opencode/matd-dev/agent.md
│   └── ...                       # (Backward compatibility for OpenCode)
│
├── scripts/
│   └── generate-agents.sh        # Build-time generator
│
└── docs/
    ├── claude-code-agent-schema.md
    └── ARCHITECTURE.md (this file)
```

## Generation Process

### Build-Time (Dockerfile)

```dockerfile
# In harness-sandbox-base Dockerfile
USER root
WORKDIR /workspace/submodules/harness-tooling/.agents
RUN bash scripts/generate-agents.sh
```

**Output**: `generated/claude/` and `generated/opencode/` directories populated with agent.md files

### Runtime (Entrypoint)

```bash
# In scripts/entrypoint.sh (step 6)

# Detect CLI and install agents
if command -v claude &> /dev/null; then
    mkdir -p ~/.claude/agents
    cp -r /workspace/submodules/harness-tooling/.agents/generated/claude/* ~/.claude/agents/
fi

if command -v opencode &> /dev/null; then
    mkdir -p ~/.opencode/agents
    # Symlink for backward compatibility
    ln -sf /workspace/submodules/harness-tooling/.agents/generated/opencode/* ~/.opencode/agents/
fi
```

## CLI-Specific Divergence

### Claude Code Agents

**Location**: `~/.claude/agents/{agent-name}/agent.md`

**Frontmatter** (from `frontmatter/claude/*.yml`):
```yaml
name: matd-qa
description: "QA engineer who reviews test coverage"
skills:
  - review-check-correctness
  - python-testing-uv-playwright
tools:
  - Read
  - Grep
  - Bash
  - Write
model: sonnet
memory: true
```

**Invocation**: Automatic via `Agent` tool
```python
Agent({
  description: "Review test coverage for feature",
  prompt: "Analyze test coverage and validate acceptance criteria"
})
# Claude Code selects matd-qa based on description match
```

### OpenCode Agents

**Location**: `~/.opencode/agents/{agent-name}/agent.md`

**Frontmatter** (from `frontmatter/opencode/*.yml`):
```yaml
description: QA engineer who reviews test coverage
mode: subagent
permission:
  read:
    '*': allow
  write:
    tests/**: allow
  bash:
    pytest: allow
temperature: 0.3
model: sonnet
max_iterations: 10
agent: matd-orchestrator  # Parent coordinator
```

**Invocation**: Explicit via `Task` tool + @mention
```python
Task({
  title: "Review test coverage",
  description: "Analyze test coverage for user authentication",
  assignee: "@matd-qa"
})
```

### Key Differences

| Aspect | Claude Code | OpenCode |
|--------|-------------|----------|
| **Agent Identity** | `name` field | Filename |
| **Discovery** | Description matching | @mention assignment |
| **Tools** | Allowlist (tools field) | Permission dict (read/write/bash) |
| **Skills** | skills array | skills array (same) |
| **Orchestration** | No orchestrator needed | matd-orchestrator coordinates |
| **Invocation** | Automatic selection | Explicit @mention |

## Backward Compatibility

### Symlink Strategy (Q4 Answer: Option C)

Legacy `.agents/agents/*.md` files are **symlinks** to generated OpenCode agents:

```bash
# After generation
cd .agents/agents
ln -sf ../generated/opencode/matd-qa/agent.md matd-qa.md
ln -sf ../generated/opencode/matd-dev/agent.md matd-dev.md
# ... (6 symlinks total)
```

**Why symlinks**:
- Existing SpecKit commands reference `agents/matd-qa.md`
- No file duplication
- Generated content automatically visible at legacy paths
- Clear indication that these are derived (ls -l shows → target)

**Divergence documented here** (not hidden in implementation).

## Maintenance Workflow

### Adding a New Agent

1. **Create canonical persona**: `canonical/new-agent.md` (markdown only)
2. **Create Claude Code spec**: `frontmatter/claude/new-agent.yml`
3. **Create OpenCode spec**: `frontmatter/opencode/new-agent.yml`
4. **Regenerate**: `bash scripts/generate-agents.sh`
5. **Update symlinks** (if needed): `ln -sf ../generated/opencode/new-agent/agent.md agents/new-agent.md`

### Updating an Agent

**Persona changes** (role, responsibilities):
- Edit `canonical/{agent-name}.md`
- Run `scripts/generate-agents.sh`

**CLI-specific changes** (tools, permissions):
- Edit `frontmatter/claude/{agent-name}.yml` OR `frontmatter/opencode/{agent-name}.yml`
- Run `scripts/generate-agents.sh`

### Build Pipeline

1. **Phase 0**: Submodule update (`git submodule update --remote --recursive`)
2. **Phase 1**: Generate agents (`bash .agents/scripts/generate-agents.sh`)
3. **Phase 2**: Build Docker image (includes generated/)
4. **Phase 3**: Entrypoint copies to CLI directories at runtime

## Benefits

✅ **Single source of truth**: Canonical personas maintained once
✅ **No markdown duplication**: Persona content in one place
✅ **Clear separation**: Specification (frontmatter) vs persona (canonical)
✅ **Build-time validation**: Generator fails if canonical file missing
✅ **CLI-agnostic**: Easy to add Gemini CLI or future CLIs

## Testing

```bash
# Generate agents
cd /workspace/submodules/harness-tooling/.agents
bash scripts/generate-agents.sh

# Verify Claude Code agents
ls -la generated/claude/matd-qa/agent.md
head -20 generated/claude/matd-qa/agent.md  # Should show Claude frontmatter

# Verify OpenCode agents
ls -la generated/opencode/matd-qa/agent.md
head -20 generated/opencode/matd-qa/agent.md  # Should show OpenCode frontmatter

# Verify symlinks
ls -la agents/matd-qa.md  # Should show → ../generated/opencode/matd-qa/agent.md
```

## Schema References

- **Claude Code**: `.agents/docs/claude-code-agent-schema.md`
- **OpenCode**: Documented in existing frontmatter files (no separate schema doc)

---

**Architecture Status**: Implemented in Phase 2 (Sandbox Restructure)
**Last Updated**: 2026-05-25
