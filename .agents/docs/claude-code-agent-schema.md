# Claude Code Agent Schema Reference

Official schema documentation for Claude Code subagents. Extracted from https://code.claude.com/docs/en/sub-agents (2026-05-25).

## Overview

Agents are defined in Markdown files with YAML frontmatter. The frontmatter controls behavior, tool access, and capabilities. The markdown body becomes the agent's system prompt.

## File Structure

```markdown
---
name: agent-identifier
description: When Claude should delegate to this agent
tools: Read, Edit, Bash
model: sonnet
---

System prompt content in markdown. This becomes the agent's instructions.
```

## Complete Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | **Yes** | `string` | Unique identifier using lowercase letters and hyphens. Received by hooks as `agent_type`. Filename need not match. |
| `description` | **Yes** | `string` | When Claude should delegate to this agent. Used for automatic delegation decisions. |
| `tools` | No | `string` or `array` | Tools the agent can use. Inherits all tools if omitted. Examples: `"Read, Edit, Bash"` or `["Read", "Edit", "Bash"]` |
| `disallowedTools` | No | `string` or `array` | Tools to deny, removed from inherited or specified list. |
| `model` | No | `string` | Model to use: `sonnet`, `opus`, `haiku`, full model ID (e.g., `claude-opus-4-7`), or `inherit` (default). |
| `permissionMode` | No | `string` | Permission mode: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, or `plan`. Ignored for plugin agents. |
| `maxTurns` | No | `integer` | Maximum number of agentic turns before the agent stops. |
| `skills` | No | `array` | Skills to preload into agent context at startup. Full skill content is injected. |
| `mcpServers` | No | `array` | MCP servers available to this agent. Can be server names or inline definitions. Ignored for plugin agents. |
| `hooks` | No | `object` | Lifecycle hooks scoped to this agent. Ignored for plugin agents. |
| `memory` | No | `string` | Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning. |
| `background` | No | `boolean` | Set to `true` to always run as background task. Default: `false`. |
| `effort` | No | `string` | Effort level: `low`, `medium`, `high`, `xhigh`, `max`. Overrides session effort. Available levels depend on model. |
| `isolation` | No | `string` | Set to `worktree` to run in temporary git worktree with isolated repository copy. |
| `color` | No | `string` | Display color in task list and transcript: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`. |
| `initialPrompt` | No | `string` | Auto-submitted as first user turn when agent runs as main session (via `--agent` or `agent` setting). Commands and skills are processed. |

## Field Details

### name (required)

- **Type**: `string`
- **Pattern**: Lowercase letters and hyphens only
- **Purpose**: Unique identifier for the agent
- **Examples**: `code-reviewer`, `db-reader`, `test-runner`
- **Note**: Hooks receive this value as `agent_type`

### description (required)

- **Type**: `string`
- **Purpose**: Tells Claude when to delegate to this agent
- **Best Practice**: Include "use proactively" for automatic delegation
- **Examples**:
  - `"Expert code reviewer. Use proactively after code changes."`
  - `"Debugging specialist for errors and test failures."`
  - `"Execute read-only database queries."`

### tools (optional)

- **Type**: `string` (comma-separated) or `array`
- **Default**: Inherits all tools from main conversation
- **Available Tools**:
  - File Operations: `Read`, `Write`, `Edit`, `Grep`, `Glob`
  - Execution: `Bash`, `PowerShell`
  - Skills: `Skill`
  - Subagents: `Agent`, `Agent(specific-agent)`
  - MCP tools (inherited from main session)
- **Examples**:
  ```yaml
  tools: Read, Grep, Glob, Bash  # Read-only researcher
  tools: ["Read", "Edit", "Bash"]  # Can modify files
  tools: Agent(worker, researcher), Read  # Can spawn only specific agents
  ```
- **Note**: Use `skills` field to preload skills, not `Skill` in `tools`

### disallowedTools (optional)

- **Type**: `string` (comma-separated) or `array`
- **Purpose**: Denylist specific tools from inherited set
- **Example**:
  ```yaml
  disallowedTools: Write, Edit  # Inherits everything except file writes
  ```
- **Resolution**: Applied before `tools` list

### model (optional)

- **Type**: `string`
- **Default**: `inherit` (uses main conversation model)
- **Values**:
  - Aliases: `sonnet`, `opus`, `haiku`
  - Full IDs: `claude-opus-4-7`, `claude-sonnet-4-6`
  - `inherit`: Use parent session model
- **Resolution Order**:
  1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
  2. Per-invocation `model` parameter
  3. Agent definition's `model` field
  4. Main conversation model

### permissionMode (optional)

- **Type**: `string`
- **Default**: `default`
- **Values**:
  - `default`: Standard permission checking with prompts
  - `acceptEdits`: Auto-accept file edits in working directory
  - `auto`: Background classifier reviews commands
  - `dontAsk`: Auto-deny permission prompts
  - `bypassPermissions`: Skip all permission prompts (use with caution)
  - `plan`: Read-only exploration mode
- **Plugin Restriction**: Ignored for plugin agents
- **Parent Override**: `bypassPermissions` and `acceptEdits` in parent take precedence

### maxTurns (optional)

- **Type**: `integer`
- **Purpose**: Limit agent execution length
- **Example**: `maxTurns: 10`

### skills (optional)

- **Type**: `array` of skill names
- **Purpose**: Preload skill content into agent context at startup
- **Example**:
  ```yaml
  skills:
    - api-conventions
    - error-handling-patterns
  ```
- **Note**: Agent can still invoke other skills via Skill tool unless restricted

### mcpServers (optional)

- **Type**: `array` of server names or inline definitions
- **Purpose**: Grant agent access to MCP servers
- **Plugin Restriction**: Ignored for plugin agents
- **Example**:
  ```yaml
  mcpServers:
    # Inline definition
    - playwright:
        type: stdio
        command: npx
        args: ["-y", "@playwright/mcp@latest"]
    # Reference existing server
    - github
  ```
- **Inline Schema**: Same as `.mcp.json` entries (`stdio`, `http`, `sse`, `ws`)

### hooks (optional)

- **Type**: `object` mapping event names to hook arrays
- **Purpose**: Define lifecycle hooks scoped to this agent
- **Plugin Restriction**: Ignored for plugin agents
- **Supported Events**:
  - `PreToolUse`: Before agent uses a tool (matcher: tool name)
  - `PostToolUse`: After agent uses a tool (matcher: tool name)
  - `Stop`: When agent finishes (converted to `SubagentStop` at runtime)
- **Example**:
  ```yaml
  hooks:
    PreToolUse:
      - matcher: "Bash"
        hooks:
          - type: command
            command: "./scripts/validate-command.sh"
    PostToolUse:
      - matcher: "Edit|Write"
        hooks:
          - type: command
            command: "./scripts/run-linter.sh"
  ```

### memory (optional)

- **Type**: `string`
- **Values**: `user`, `project`, `local`
- **Purpose**: Enable persistent memory directory for cross-session learning
- **Locations**:
  - `user`: `~/.claude/agent-memory/<agent-name>/`
  - `project`: `.claude/agent-memory/<agent-name>/`
  - `local`: `.claude/agent-memory-local/<agent-name>/`
- **Behavior**:
  - System prompt includes memory directory instructions
  - First 200 lines or 25KB of `MEMORY.md` loaded
  - Read, Write, Edit tools auto-enabled for memory management

### background (optional)

- **Type**: `boolean`
- **Default**: `false`
- **Purpose**: Always run as background task
- **Behavior**:
  - Background agents run concurrently
  - Auto-deny permission prompts
  - Continue working without blocking main conversation
- **Override**: Disabled by `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`

### effort (optional)

- **Type**: `string`
- **Values**: `low`, `medium`, `high`, `xhigh`, `max`
- **Purpose**: Override session effort level when this agent is active
- **Note**: Available levels depend on model

### isolation (optional)

- **Type**: `string`
- **Values**: `worktree`
- **Purpose**: Run agent in temporary git worktree
- **Behavior**:
  - Isolated repository copy branched from default branch
  - File edits don't affect main checkout
  - Auto-cleanup if no changes made

### color (optional)

- **Type**: `string`
- **Values**: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`
- **Purpose**: Visual identification in task list and transcript

### initialPrompt (optional)

- **Type**: `string`
- **Purpose**: Auto-submitted as first user turn when agent runs as main session
- **Usage**: Only applies when agent launched via `--agent` flag or `agent` setting
- **Processing**: Commands and skills are processed
- **Behavior**: Prepended to any user-provided prompt

## Agent Scope & Discovery

Agents are discovered from multiple locations with priority order:

| Location | Scope | Priority | Creation Method |
|----------|-------|----------|-----------------|
| Managed settings | Organization-wide | 1 (highest) | Deployed via managed settings |
| `--agents` CLI flag | Current session | 2 | Pass JSON when launching |
| `.claude/agents/` | Current project | 3 | Interactive or manual |
| `~/.claude/agents/` | All your projects | 4 | Interactive or manual |
| Plugin `agents/` | Where plugin enabled | 5 (lowest) | Installed with plugins |

**Discovery Rules**:
- `.claude/agents/` and `~/.claude/agents/` scanned recursively
- Subdirectories allowed for organization (e.g., `agents/review/security.md`)
- Identity comes from `name` field only, not filepath
- Higher-priority location wins when names conflict
- Plugin agents: subfolder becomes part of scoped ID (`plugin:subfolder:name`)

## CLI-Defined Agents

Pass JSON to `--agents` flag for session-only agents:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality, security, best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Available Fields**: Same as frontmatter except use `prompt` for system prompt (replaces markdown body).

## Agent Context & Startup

Non-fork agents start with fresh context containing:
- **System prompt**: Agent's own prompt + environment details (NOT full Claude Code prompt)
- **Task message**: Delegation prompt from Claude
- **CLAUDE.md**: All memory hierarchy levels (except Explore and Plan)
- **Git status**: Snapshot from parent session start (except Explore and Plan)
- **Preloaded skills**: Full content of skills listed in `skills` field

**Built-in Agents**:
- **Explore** and **Plan**: Skip CLAUDE.md and git status for speed
- **General-purpose**: Inherits all context and tools

## Invocation Methods

### Automatic Delegation
Claude decides based on task and agent descriptions.

### @-mention
Type `@agent-<name>` or use typeahead to guarantee agent runs.
```text
@"code-reviewer (agent)" look at the auth changes
```

### Session-wide
```bash
claude --agent code-reviewer  # Entire session uses this agent
```

Or in `.claude/settings.json`:
```json
{"agent": "code-reviewer"}
```

### Plugin Agents
Use scoped name: `@agent-plugin-name:agent-name`

For subfolders: `@agent-plugin-name:subfolder:agent-name`

## Tool Restrictions

### Restrict Tool Access
```yaml
tools: Read, Grep, Glob, Bash  # Allowlist
disallowedTools: Write, Edit   # Denylist
```

### Restrict Subagent Spawning
```yaml
tools: Agent(worker, researcher)  # Can only spawn these agents
tools: Agent  # Can spawn any agent
# Omit Agent entirely: Cannot spawn any agents
```

### Disable via Permissions
In `.claude/settings.json`:
```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

## Common Patterns

### Read-Only Researcher
```yaml
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
```

### Code Modifier
```yaml
name: code-fixer
description: Fix bugs and modify code
tools: Read, Edit, Bash, Grep
```

### Background Task
```yaml
name: async-worker
description: Long-running background tasks
background: true
tools: Bash, Read, Write
```

### Project-Specific with Memory
```yaml
name: project-assistant
description: Project-specific helper with learning
memory: project
tools: Read, Edit, Bash
```

## Plugin Agent Restrictions

Plugin agents do NOT support:
- `hooks`
- `mcpServers`
- `permissionMode`

These fields are silently ignored when loading from plugin directories.

To use these features, copy the agent file to `.claude/agents/` or `~/.claude/agents/`.

## Validation Rules

### name
- ✅ `code-reviewer`, `db-reader`, `test-runner`
- ❌ `Code Reviewer`, `code_reviewer`, `codeReviewer`

### description
- ✅ Clear, specific, includes "use proactively" for automatic delegation
- ❌ Vague or generic descriptions

### tools
- ✅ Specific tool list or empty for inheritance
- ❌ Invalid tool names, typos

### model
- ✅ `sonnet`, `opus`, `haiku`, `inherit`, `claude-opus-4-7`
- ❌ Invalid model names or IDs

## Comparison with Other Agent Schemas

### Claude Code vs OpenCode

**Similarities**:
- Both use YAML frontmatter + markdown body
- Both support `name`, `description`, `tools`, `model`
- Both discovered from user/project directories

**Claude Code Specific**:
- `permissionMode`, `mcpServers`, `hooks` (not in OpenCode)
- `memory` with user/project/local scopes
- `background`, `effort`, `isolation` fields
- Built-in agents: Explore, Plan, general-purpose
- Fork mode support (experimental)
- Plugin agent support with scoped identifiers

**OpenCode Specific**:
- Different tool naming conventions
- Different discovery paths
- Different hook system

## Environment Variables

- `CLAUDE_CODE_SUBAGENT_MODEL`: Override agent model selection
- `CLAUDE_CODE_FORK_SUBAGENT=1`: Enable fork mode (experimental)
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`: Disable background agents
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`: Trigger compaction earlier (default: 95%)

## Examples

### Minimal Agent
```markdown
---
name: simple-reader
description: Read and analyze files
---
You are a file analysis agent. Read files and provide insights.
```

### Full-Featured Agent
```markdown
---
name: full-featured
description: Complex agent with all features
tools: Read, Edit, Bash, Grep, Glob
disallowedTools: Write
model: sonnet
permissionMode: acceptEdits
maxTurns: 20
skills:
  - coding-conventions
  - testing-patterns
memory: project
background: false
effort: high
color: blue
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
Complex agent with full configuration.
```

## References

- Official docs: https://code.claude.com/docs/en/sub-agents
- Hook system: https://code.claude.com/docs/en/hooks
- Skills: https://code.claude.com/docs/en/skills
- MCP: https://code.claude.com/docs/en/mcp
- Plugins: https://code.claude.com/docs/en/plugins
