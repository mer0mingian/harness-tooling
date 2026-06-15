---
source: https://gemini.google.com/share/5c42a53260f8
date: 2026-06-15
---

# Deep Research: Cross-Platform Agent Permission Management

## Origin

Conversation with Gemini about finding an open-source alternative to Microsoft's Agent Package Manager (APM) that supports **granular tool permissions** and **multi-client agent distribution** across Claude Code, OpenCode, and Codex CLI.

## Problem Statement

An organization has:
- Multiple coding agents in use across teams (Claude Code, OpenCode, Codex CLI)
- An internal skills marketplace distributed via `npx skills`
- A specialized **architect subagent** that must be restricted from using the popular `"grill-me"` skill (adversarial testing requirement)
- Need for **project-scoped** (not user-scoped) installation that is checked into Git
- Requirement for **engine-level enforcement** — the agent must literally be unable to invoke the tool/skill, not just be told not to

## Candidates Evaluated

### 1. Astro Rosie (`withastro/rosie`)
- **Role:** Pure package distribution layer (like npm/cargo for agents)
- **Limitation:** No runtime permission enforcement whatsoever
- **Verdict:** Insufficient — cannot block skills per agent

### 2. Qwen Code
- **Strengths:** Native `disallowedTools` frontmatter, explicit subagent control via `approvalMode`
- **Limitation:** IDE-specific, not designed for multi-CLI distribution
- **Verdict:** Interesting permission model but wrong integration layer

### 3. Goose (by Block/Signal0)
- **Strengths:** Environment-level subagent control via `GOOSE_SUBAGENT_MAX_TURNS=0`
- **Limitation:** Execution-mode based, not file-based skill filtering
- **Verdict:** Not applicable for skill-level restrictions

### 4. NVIDIA OpenShell
- **Strengths:** Kernel-level sandbox, OS-level process isolation
- **Limitation:** Overkill for skill-level restrictions; infrastructure-heavy
- **Verdict:** Enterprise sandboxing, not skill management

### 5. Charlie (`henriquemoody/charlie`)
- **Strengths:** Universal agent config generator targeting multiple CLIs
- **Limitations:** Small user base, experimental, "too shaky" for enterprise
- **Verdict:** Rejected by user

### 6. Skills.sh + `allowed-tools` Frontmatter
- **Strengths:** Official `agentskills.io` open standard, `allowed-tools` allowlist approach
- **Limitations:** User-scope default in CLI, no native project-scoped install without scripts
- **Verdict:** Usable but requires custom synclinking scripts for multi-client parity

### 7. Microsoft APM (Recommended Distribution Layer)
- **Strengths:** Native `apm compile` multi-target compilation, project-scoped (`apm.lock.yaml`), token-optimized output per client
- **Limitation:** Does not provide a unified permission engine — enforcement depends on each runtime's native mechanism
- **Verdict:** Best distribution tool, but not a permission system itself

## Critical Finding: No Cross-Platform Permission Engine Exists

Each runtime has its own **native** engine-level enforcement mechanism, and they are fundamentally different:

| Runtime | Engine-Level Mechanism | What It Does |
|---------|----------------------|-------------|
| Claude Code | `disallowedTools` frontmatter | Strips tool/skill definitions from agent's context window before invocation |
| Claude Code | `Agent(Name)::Tool(Pattern)` in settings.json | Intercepts tool calls at the client level before they reach the model |
| OpenCode | `disallowedTools` frontmatter | Same as Claude Code — tools removed from context at initialization |
| Codex CLI | Directory indexing (`.agents/skills/`) | Skills not in the indexed directory are not discovered at startup |
| Codex CLI | No native `disallowedTools` | Tool-level granularity is **not available** |

There is **no single open source tool** that provides engine-level tool/skill/MCP permission enforcement across all three runtimes. The enforcement always happens inside each proprietary runtime.

## Permission-Only vs Distribution-Only Tools

The landscape is bifurcated:

- **Distribution tools** (APM, Rosie): Install files into the correct directories. They do not enforce permissions.
- **Runtime engines** (Claude Code, OpenCode, Codex): Enforce permissions natively. Each has a different system.
- **Instruction-level tools** (`.apm/instructions/`, prompt injection): Tell the agent not to use something but do not prevent it. **Not engine enforcement.**

## Final Architecture

The recommended approach combines:
1. **APM** as the distribution layer (installs files, compiles per-client output)
2. **`disallowedTools` frontmatter** for Claude Code + OpenCode (engine-level skill/tool stripping)
3. **Directory indexing control** for Codex CLI (omit the skill from the indexed directory)
4. **`Agent(Name)::Tool(Pattern)`** in `.claude/settings.json` as an additional Claude Code guard

**Codex CLI limitation:** If tool-level granularity is needed for Codex CLI (e.g., blocking `Edit` or `Bash` on a specific subagent), this cannot be achieved at the engine level. Instruction-level prompting is the only fallback.

## MCP Server Restriction

No cross-platform runtime MCP permission layer exists. Each runtime handles MCP server configuration independently. APM's `apm-policy.yml` provides install-time MCP blocking (package-level) but cannot enforce per-agent MCP restrictions at runtime.
