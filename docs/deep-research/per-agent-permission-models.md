# Per-Agent Permission Models: Supporting Tool and MCP Restrictions in APM

The Agent Package Manager (APM) ecosystem operates at the intersection of multiple agent CLI platforms, each with its own approach to agent-level tool governance. This document examines the permission models of Claude Code and OpenCode, evaluates APM's current primitive architecture against them, and identifies minimally-invasive pathways for APM to support per-agent tool and MCP server restrictions.

---

## 1. Executive Summary

**Finding:** Neither Claude Code nor OpenCode's agent markdown frontmatter schemas are currently mapped into APM's primitive models. APM's `Chatmode` (agent) primitive has no fields for tools, permissions, or restrictions. However, both downstream ecosystems support native per-agent permission mechanisms that APM could surface through its existing pipeline with moderate effort.

**Key insight:** Because APM's `P1` principle ("No invented primitive frontmatter") forbids proprietary `apm-*` frontmatter keys, APM must operate within the canonical frontmatter schemas defined by upstream ecosystems. This is feasible — both Claude Code and OpenCode already define the relevant fields. APM's role is to parse, validate, and optionally inject them during deployment.

---

## 2. Claude Code Subagent Permission Model

Source: https://code.claude.com/docs/en/sub-agents

### Frontmatter Fields for Tool Governance

| Field | Type | Purpose |
|-------|------|---------|
| `tools` | `list[str]` | Allowlist: agent receives *only* these tools. Omitting a tool denies it. |
| `disallowedTools` | `list[str]` | Denylist: remove specific tools from the inherited set. Applied on top of `tools`. |
| `mcpServers` | `list[str \| dict]` | Scopes MCP servers to this subagent. Supports string references and inline definitions. |
| `permissionMode` | `str` | Behavioral mode: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. |

### Interaction Semantics

When both `tools` and `disallowedTools` are present:
1. `disallowedTools` is evaluated first — removes named tools from the pool.
2. `tools` is then resolved against the remaining pool — only named tools survive.
3. A tool listed in both is removed.

### Subagent Spawning Control

The `Agent(agent_type)` syntax in the `tools` allowlist controls which subagent types a coordinator can spawn:

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

- `Agent(worker, researcher)` — can only spawn `worker` and `researcher` subagents.
- Bare `Agent` (no parentheses) — spawn any subagent type.
- Omit `Agent` entirely — forbids spawning.

### Mechanisms Beyond Frontmatter

- **`settings.json`** `permissions.deny` — can deny specific subagents globally: `["Agent(Explore)", "Agent(my-custom-agent)"]`.
- **CLI flag** — `claude --disallowedTools "Agent(Explore)"`.
- **Tools always unavailable to subagents**: `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode` (unless `permissionMode: plan`), `ScheduleWakeup`, `WaitForMcpServers`.

### Plugin Subagent Restrictions

For security, plugin-hosted subagents do **not** support `hooks`, `mcpServers`, or `permissionMode` — these fields are silently ignored.

---

## 3. OpenCode Agent Permission Model

Source: https://opencode.ai/docs/permissions

### Frontmatter Permission Field

OpenCode uses a unified `permission` field with three states per tool category:

```yaml
---
description: Code review agent
mode: subagent
permission:
  edit: deny
  bash:
    "*": ask
    "git status *": allow
  webfetch: deny
  mymcp_*: deny
---
```

### All Permission Keys

| Key | Type | Tools Gated |
|-----|------|-------------|
| `read` | action \| object | `read` (matches file path globs) |
| `edit` | action \| object | `write`, `edit`, `apply_patch` |
| `glob` | action \| object | `glob` (matches glob pattern) |
| `grep` | action \| object | `grep` (matches regex pattern) |
| `list` | action \| object | `list` (directory listing) |
| `bash` | action \| object | `bash` (matches parsed commands) |
| `task` | action \| object | `task` (matches subagent type) |
| `external_directory` | action \| object | Tools accessing paths outside worktree |
| `lsp` | action \| object | `lsp` (LSP queries) |
| `skill` | action \| object | `skill` (matches skill name) |
| `todowrite` | action only | `todowrite`, `todoread` |
| `webfetch` | action only | `webfetch` (matches URL) |
| `websearch` | action only | `websearch` (matches query) |
| `question` | action only | `question` (asking user during execution) |
| `doom_loop` | action only | Recovery prompts when agent appears stuck |

### Action vs Object Syntax

**Action** (shorthand): `"allow"`, `"ask"`, `"deny"` — applies to all invocations of that tool.

**Object** (fine-grained): maps patterns to actions, evaluated in order, last match wins:

```yaml
permission:
  edit:
    "*": deny
    "packages/web/src/content/docs/*.mdx": allow
  bash:
    "*": ask
    "git status *": allow
    "git log*": allow
```

### Wildcard MCP Tool Restriction

Permission keys use wildcard matching against tool names. Since MCP server tools follow the pattern `<mcp-name>_<tool-name>`, server-wide restrictions are straightforward:

```yaml
permission:
  playwright_*: deny
  playwright_navigate: ask
```

### Subagent Invocation Control via `permission.task`

Controls which subagents an agent can invoke via the Task tool:

```yaml
permission:
  task:
    "*": deny
    "orchestrator-*": allow
    "code-reviewer": ask
```

When set to `"deny"`, the subagent is removed from the Task tool description entirely.

### Deprecated `tools` Field

Predecessor to `permission`, still supported for backwards compatibility:

```yaml
---
tools:
  write: false
  bash: false
---
```

- `true` = `{"*": "allow"}`
- `false` = `{"*": "deny"}`

### Agent Mode Restrictions

| Mode | Can delegate? | Hardcoded restrictions |
|------|---------------|------------------------|
| `primary` | Yes (via Task) | None |
| `subagent` | No | `todowrite: deny`, `todoread: deny`, `task: deny` (hardcoded) |
| `all` | Yes (when acting as primary) | None |

---

## 4. APM Primitive Architecture Analysis

### Current State

APM defines four primitive types in `primitives/models.py`:

| Primitive | Fields | Permission Support |
|-----------|--------|--------------------|
| `Chatmode` (agent) | `name`, `file_path`, `description`, `apply_to`, `content`, `author`, `version`, `source`, `handoffs` | **None** |
| `Instruction` | `name`, `file_path`, `description`, `apply_to`, `content`, `author`, `version`, `source` | **None** |
| `Context` | `name`, `file_path`, `description`, `content`, `author`, `version`, `source` | **None** |
| `Skill` | `name`, `file_path`, `description`, `content`, `source` | **None** |

The frontmatter parser (`primitives/parser.py`) cherry-picks known metadata fields via `.get()` and silently ignores all others. Agent files pass through the compilation pipeline (`compilation/agents_compiler.py`) as opaque content — no frontmatter transformation or injection occurs.

### Gap Analysis

| Component | Existing Pattern | Gap | Fill Effort |
|-----------|-----------------|-----|-------------|
| `primitives/models.py` | `Chatmode` has `handoffs: list[str \| dict] \| None` | No `allowed_tools`, `denied_tools`, `mcp_servers`, `permission` fields | **Low** — add optional fields following `handoffs` pattern |
| `primitives/parser.py` | Uses `metadata.get("handoffs")` pattern | No extraction of permission-related frontmatter keys | **Low** — add `.get()` calls for new fields |
| `policy/matcher.py` | `_check_allow_deny()` with glob matching | No agent-tool-specific wrapper | **Low** — existing infrastructure directly reusable |
| `policy/schema.py` | Sub-policies for deps, MCP, compilation | No `AgentToolPolicy` or `AgentPolicy` | **Medium** — new dataclass + YAML parsing |
| `policy/policy_checks.py` | 18+ checks following uniform pattern | No agent-tool allow/deny checks | **Medium** — add `agent-tool-*` checks |
| `integration/agent_integrator.py` | `copy_agent()` verbatim copy | No frontmatter injection or validation during deploy | **Low–Medium** — add optional permission field injection |
| `compilation/agents_compiler.py` | Opaque content pass-through | Transparent — no changes needed | **None** |

### The `allowExecutables` Precedent

The only permission-like concept in APM is `allowExecutables` — a per-package approval gate for hooks, MCP servers, and bin/ executables stored in `apm.yml`. It operates at the **package level**, not the agent level, but establishes key architectural patterns:

- **User consent model**: users explicitly approve (`apm approve`) or deny (`apm deny`) executable side-effects.
- **Stored in manifest**: `apm.yml` tracks approved packages.
- **Enforced at install time**: the `exec_gate.py` phase checks approvals before deployment.

This pattern could be adapted for agent permissions: `apm.yml` could track approved/rejected tool access per agent, gated by policy at install/compile time.

---

## 5. Implementation Pathways

Three strategies for supporting per-agent permissions in APM, ordered by complexity.

### Pathway A: Frontmatter Pass-Through (Lowest Effort)

**Concept**: APM parses and preserves permission-related frontmatter from source `.agent.md` files without modification. When deployed to a target CLI, the canonical fields (Claude Code `tools`/`disallowedTools`, OpenCode `permission`) pass through verbatim.

**Changes required:**
1. **`primitives/models.py`** — Add `allowed_tools`, `denied_tools`, `mcp_servers`, `permission_mode` fields to `Chatmode` (all optional, all `None` by default).
2. **`primitives/parser.py`** — Extract these fields from YAML frontmatter using the existing `.get()` pattern.
3. **`integration/agent_integrator.py`** — Ensure verbatim copy preserves frontmatter (already does — no changes needed).

**Result**: Agents declare their own permissions in their source `.agent.md`. APM passes them through to the target environment. No policy-level enforcement.

**Limitation**: No organizational governance. An agent author can grant themselves any tool access.

### Pathway B: Policy Injection (Medium Effort)

**Concept**: APM-policy.yml gains an `agent` section that can override or restrict permissions declared in agent frontmatter. On deploy, APM merges the agent's declared permissions with the policy's constraints.

**Changes required:**
1. All changes from Pathway A.
2. **`policy/schema.py`** — Add `AgentToolPolicy` dataclass:
   ```python
   @dataclass(frozen=True)
   class AgentToolPolicy:
       allowed_tools: tuple[str, ...] | None = None
       denied_tools: tuple[str, ...] | None = None
       enforce_from_frontmatter: bool = True  # Trust agent's own declarations?
   ```
3. **`policy/policy_checks.py`** — Add `agent-tool-allowlist` and `agent-tool-denylist` checks.
4. **`integration/agent_integrator.py`** — After reading source frontmatter, apply policy overrides:
   - If `enforce_from_frontmatter` is false, strip permission fields from deployed agent.
   - If `denied_tools` is set, inject `disallowedTools` (Claude Code) or `permission.<tool>: deny` (OpenCode).
   - If `allowed_tools` is set, inject `tools` (Claude Code) or set all unlisted to `deny` (OpenCode).

**Result**: Organizations can enforce least-privilege tool access across all agents, regardless of what individual agent files declare.

### Pathway C: Cross-CLI Permission Abstraction (Highest Effort)

**Concept**: APM defines a CLI-agnostic permission DSL in agent frontmatter that it compiles to ecosystem-specific output during deployment. This is analogous to how APM's compilation pipeline generates `AGENTS.md` in different formats per target.

**Changes required:**
1. Define a unified permission schema in APM (hypothetical `apm-permission` convention that P1 might block).
2. **`compilation/agents_compiler.py`** — Add a permission compilation phase that translates unified DSL → target-specific frontmatter.
3. Per-target formatters in `adapters/client/` that understand the permission DSL.

**Risk**: Violates P1 ("No invented primitive frontmatter"). Only viable if the unified schema is standardized upstream (e.g., `agentskills.io` extension).

---

## 6. Recommended Path

**Pathway B (Policy Injection)** offers the best balance of capability and effort for v1. Rationale:

1. It respects P1 by operating on canonical fields from upstream ecosystems.
2. It provides organizational governance without requiring agent authors to change their files.
3. It reuses existing infrastructure: `_check_allow_deny()` in `matcher.py`, the policy YAML loader, and the install pipeline's policy gate.
4. It follows the same architectural pattern as `McpPolicy` and `DependencyPolicy` — APM users already understand allow/deny lists.

### Estimated Implementation Sequence

1. Extend `Chatmode` model and parser (Low — a few hours)
2. Add `AgentToolPolicy` to `policy/schema.py` with YAML parsing (Medium — half day)
3. Implement `agent-tool-*` policy checks (Medium — half day)
4. Modify `copy_agent()` for policy-enforced permission injection (Medium — half day)
5. Test across Claude Code and OpenCode target ecosystems (Medium — half day)

**Total estimated effort: ~2-3 engineering days.**

---

## 7. References

- Claude Code Sub-agents: https://code.claude.com/docs/en/sub-agents
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Permission Modes: https://code.claude.com/docs/en/permission-modes
- OpenCode Agent Docs: https://opencode.ai/docs/agents
- OpenCode Permission Docs: https://opencode.ai/docs/permissions
- OpenCode Config Schema: https://opencode.ai/config.json
- APM Source: `/home/mer0/repositories/harness-tooling/watching/apm/src/apm_cli/`

---

**Last Updated:** 2026-06-15
**Author:** harness-tooling research
