---
source: https://gemini.google.com/share/5c42a53260f8
verified_against: /home/mer0/repositories/harness-tooling/watching/apm (v0.10.0)
date: 2026-06-15
---

# APM Implementation Plan: Engine-Level Permission Enforcement

## ⚠️ Prerequisite: Verify `disallowedTools` Syntax

There is **ambiguity in the actual syntax** for blocking skills in Claude Code and OpenCode. Two variants exist in the documentation, and they may differ between runtimes. **This plan must not be implemented until the following experiment confirms which syntax works.**

### The Ambiguity

| Source | Claims | Status |
|--------|--------|--------|
| Gemini conversation (source URL) | `disallowedTools` works for **both** Claude Code and OpenCode | Unconfirmed |
| Claude Code official docs | `disallowedTools: [Write, Edit]` in subagent frontmatter; `Skill(name)` syntax in settings.json only | Confirmed syntax |
| This codebase's agents | OpenCode uses `permission: { skill: { "pattern": deny } }`, NOT `disallowedTools` | Found in `.opencode/agents/tdd-code-reviewer.md` |
| Assumption | `disallowedTools: Skill("grill-*")` | Needs verification |

### Required Experiment

Deploy **three test subagents** and invoke each to enumerate available tools:

**1. Claude Code — plain name variant:**
```yaml
# .claude/agents/test-cc-plain.md
name: test-cc-plain
disallowedTools:
  - grill-me
---
List every tool available to you. Is `grill-me` present?
```

**2. Claude Code — wrapped `Skill()` variant:**
```yaml
# .claude/agents/test-cc-wrapped.md
name: test-cc-wrapped
disallowedTools:
  - Skill(grill-me)
---
List every tool available to you. Is `grill-me` present?
```

**3. OpenCode — `permission` prefix variant:**
```yaml
# .opencode/agents/test-oc-prefix.md
name: test-oc-prefix
permission:
  skill:
    "grill-": deny
---
List every tool available to you. Is `grill-me` present?
```

### Verification Criteria

| Variant | `grill-me` removed from tool list? | Correct syntax |
|---------|-----------------------------------|----------------|
| Claude Code `disallowedTools: [grill-me]` | ❓ | ❓ |
| Claude Code `disallowedTools: [Skill(grill-me)]` | ❓ | ❓ |
| OpenCode `permission: { skill: { "grill-": deny } }` | ❓ | ❓ |

The variant that actually removes the skill from the agent's available tool list (not just telling it not to use it) is the correct engine-level syntax. **Only proceed with implementation once this is confirmed.**

---

## Verified APM Behavior (from Source)

APM v0.10.0 handles agent files as follows, verified from the source code in `watching/apm/`:

| Target | Install Path | Format | What APM Does | Frontmatter? |
|--------|-------------|--------|---------------|-------------|
| **Claude Code** | `.claude/agents/*.md` | `claude_agent` | **Copies verbatim** | Preserved as-is |
| **OpenCode** | `.opencode/agents/*.md` | `opencode_agent` | **Copies verbatim** (validates + warns on incompatible fields) | Preserved as-is |

Key source: `AgentIntegrator.copy_agent()` reads the source file and writes it as-is. APM does **not** inject or transform frontmatter. The `apm compile` step generates `CLAUDE.md`/`AGENTS.md` from primitives — agent files are handled at `apm install` time.

## Core Finding

There is **no shared permission engine** between Claude Code and OpenCode. Each uses a different native mechanism. APM is the **distribution** layer — it copies files to the right directories, but does not enforce or transform permissions.

## Engine-Level Mechanisms per Runtime (Post-Verification)

| Runtime | Mechanism | Native Syntax | What It Does |
|---------|-----------|--------------|-------------|
| **Claude Code** | `disallowedTools` in agent frontmatter | TBD by experiment | Strips tool/skill defs from agent context before invocation |
| **Claude Code** | `.claude/settings.json` rules | `Agent(Name)::Tool(Pattern)` | Client-level interception before tool execution |
| **OpenCode** | `permission` block in agent frontmatter | `permission: { skill: { "prefix": deny } }` | Pattern-based tool/skill access control |

## How It Works

```
  # Package repo (.apm/agents/enterprise-architect.md)
  ---
  name: enterprise-architect
  disallowedTools:      ← or permission: depending on experiment result
    - grill-me
  ---
  [body...]

  apm install
       │
       ▼
  AgentIntegrator.copy_agent()  ← copies verbatim
       │
       ├── .claude/agents/enterprise-architect.md   ← verbatim copy
       └── .opencode/agents/enterprise-architect.md ← verbatim copy
```

## Implementation Steps

### Step 0: Confirm Syntax via Experiment

Run the experiment above (test-cc-plain, test-cc-wrapped, test-oc-prefix). Verify which syntax actually removes `grill-me` from the agent's tool list. Update all frontmatter in subsequent steps to use the confirmed syntax.

### Step 1: Package the Agent Source

Place the agent file in the package's `.apm/agents/` directory. APM will copy it verbatim to both targets.

```markdown
---
name: enterprise-architect
description: "Evaluates system architecture and domain boundaries."
# !! Use the syntax CONFIRMED by the experiment in Step 0 !!
# Claude Code variant:
disallowedTools:
  - grill-me
# ... OR OpenCode variant:
# permission:
#   skill:
#     "grill-": deny
metadata:
  version: "1.0.0"
  adversarial_mode: true
---

You are an isolated architectural evaluation subagent.
Analyze the codebase structure, mapping domain boundaries
and infrastructure bottlenecks.
```

### Step 2: Create the Project Manifest

```yaml
# apm.yml
name: enterprise-core-workspace
version: 1.0.0
description: "Project-scoped agent configuration mapping"
dependencies:
  apm:
    - internal-github.com/architecture-team/enterprise-architect#v1.0.0
includes: auto
```

### Step 3: Install

```bash
apm install
```

Runs `AgentIntegrator.integrate_agents_for_target()` for each active target. `copy_agent()` copies the file verbatim — whatever frontmatter the source has lands in both `.claude/agents/` and `.opencode/agents/`.

### Step 4: Additional Claude Code Guard via Hooks

Include a hooks file that APM's `HookIntegrator` merges into `.claude/settings.json`:

```json
// .apm/hooks/enterprise-architect-guard.json
{
  "permissions": {
    "rules": [
      {
        "comment": "Engine-level deny: architect cannot invoke grill-me",
        "tool": "Agent(enterprise-architect)::Skill(grill-me)",
        "action": "deny"
      }
    ]
  }
}
```

This provides a **second layer** of engine-level enforcement at the client level, independent of the frontmatter approach.

### Step 5: Commit to Version Control

```bash
git add apm.yml apm.lock.yaml .claude/agents/ .opencode/agents/
git commit -m "Add enterprise-architect with engine-level permission enforcement"
```

## Key Properties

| Property | Implementation | Level | Status |
|----------|---------------|-------|--------|
| **Claude Code restriction** | `disallowedTools` in frontmatter (verbatim copy) | Engine | ⏳ Depends on experiment |
| **OpenCode restriction** | `permission: { skill: { "grill-": deny } }` | Engine | ✅ Confirmed from codebase |
| **Claude Code additional guard** | `Agent(arch)::Skill(grill-me)` in settings.json | Engine (client-level) | ✅ Confirmed from docs |
| **Distribution** | APM copies agent files verbatim | Transport | ✅ Confirmed from source |

## What APM Does NOT Do

- APM does **not** inject or transform frontmatter — it only copies what's in the source file
- APM does **not** provide a unified permission engine
- APM's `apm-policy.yml` operates at the **install/packaging level**, not per-agent runtime
