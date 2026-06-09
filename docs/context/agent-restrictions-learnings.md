# Agent Restrictions Learnings

## Source
Grilling session 2026-06-09
Subagent research into Claude Code agent configuration patterns

## Context
Understanding agent restriction mechanisms is critical for designing the SpecKit extension's agent presets. Different restriction types have different scopes and priority levels that affect multi-agent workflows.

## Details

### Priority Levels
- **Project agents:** Priority 3 (lower number = higher priority)
- **Plugin agents:** Priority 5
- Project agents override plugin agents when names conflict
- Use priority flag during installation: `specify extension add <path> --priority 3`

### Tool Restriction Syntax

**Skills (slash commands):**
```yaml
disallowedTools:
  - "Skill(name)"  # Must use exact Skill(name) format
```

Example:
```yaml
disallowedTools:
  - "Skill(general-git-advanced-workflows)"
  - "Skill(docker-expert)"
```

**MCP Tools:**
```yaml
disallowedTools:
  - "mcp__atlassian-write__jira_create_issue"  # Full MCP tool name
```

### MCP Server Scoping

**Inline scoping (agent-specific):**
```yaml
# In agent config
mcpServers:
  atlassian-write:
    command: "..."
```
- Only that specific agent can see the MCP server
- Other agents in the same workspace cannot access it
- Useful for role-based access (e.g., only matd-product-manager sees Jira)

**Project-level scoping:**
```yaml
# In workspace .claude/settings.json
{
  "mcpServers": {
    "atlassian-write": {...}
  }
}
```
- All agents in workspace can access
- Cannot restrict per-agent (all or nothing)

### Project Memory Loading

**Automatic loading:**
- All agents automatically load `~/.claude/projects/<hash>/memory/MEMORY.md`
- Applies to workspace-scoped agents
- Exceptions: Explore agents, Plan agents (stateless)

**Memory scope:**
- Project-level only (not agent-specific)
- Shared across all agents in workspace
- Use for domain glossary, architectural invariants

## References
- Claude Code Documentation: https://docs.claude.ai/code/agent-configuration
- SpecKit Extension Design: /home/minged01/repositories/test/harness-sandbox-stony/SPECKIT_EXTENSION_STRUCTURE.md
- Agent Skill Matrix: /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/AGENT_SKILL_MATRIX.md
