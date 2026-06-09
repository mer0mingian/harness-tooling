# Plugin & Extension Comparison Table

## Overview: What Gets Installed

| Module | Type | Installation | What It Provides |
|--------|------|--------------|------------------|
| **harness-agents** | Claude Code Plugin | `claude plugin install harness-agents` | 5 specialist agents + 16 skills |
| **matd** | Claude Code Plugin | `claude plugin install matd` | 6 MATD agents + 8 workflow commands |
| **matd** | SpecKit Extension | `specify extension add matd` | 8 SpecKit commands + templates |

---

## Detailed Comparison

### 1. harness-agents Plugin

**Installation:**
```bash
claude plugin install harness-agents --scope project
```

**What It Provides:**

| Component | Count | Claude Code Exposure | Description |
|-----------|-------|---------------------|-------------|
| **Agents** | 5 | `@test-specialist`<br>`@dev-specialist`<br>`@arch-specialist`<br>`@review-specialist`<br>`@qa-specialist` | Available via Agent tool or @ mentions |
| **Skills** | 16 | Not directly invocable | Used by agents via `use_mcp_tool` |
| **Commands** | 0 | None | No slash commands |

**Agents Included:**
- `@test-specialist` - Writes failing tests, validates RED state
- `@dev-specialist` - Implements features, makes tests GREEN
- `@arch-specialist` - Architecture and design decisions
- `@review-specialist` - Code review and quality checks
- `@qa-specialist` - End-to-end testing and verification

**Skills Included:**
- `general-python-environment`
- `general-solid`
- `general-verification-before-completion`
- `orchestrate-executing-plans`
- `python-async-patterns`
- `python-design-patterns`
- `python-fastapi-templates`
- `python-testing-uv-playwright`
- `review-check-correctness`
- `review-differential-review`
- `review-e2e-testing-patterns`
- `review-simplify-complexity`
- `review-webapp-testing`

**Claude Code Usage:**
```
User: "I need to write tests for the login feature"

Agent spawn: @test-specialist
# Or via Agent tool in conversation

No slash commands available
```

**Purpose:** Provides **specialist agents** you can spawn for specific tasks in multi-agent workflows.

---

### 2. matd Plugin (Claude Code)

**Installation:**
```bash
claude plugin install matd --scope project
```

**What It Provides:**

| Component | Count | Claude Code Exposure | Description |
|-----------|-------|---------------------|-------------|
| **Agents** | 6 | `@matd-architect`<br>`@matd-dev`<br>`@matd-qa`<br>`@matd-specifier`<br>`@matd-orchestrator`<br>`@matd-critical-thinker` | Available via Agent tool or @ mentions |
| **Commands** | 8 | `/matd-test`<br>`/matd-implement`<br>`/matd-review`<br>`/matd-commit`<br>`/matd-update-docs`<br>`/matd-specify-product-brief`<br>`/matd-specify-adr`<br>`/matd-specify-solution-design` | Direct slash commands |
| **Skills** | 0 | Not included | Agents use skills from other plugins |

**Agents Included:**
- `@matd-orchestrator` - PM coordinator, delegates to other agents
- `@matd-specifier` - Requirements engineer (OpenSpec format)
- `@matd-critical-thinker` - Red team validator
- `@matd-architect` - Solution designer, C4 diagrams
- `@matd-qa` - Test architect, E2E tests
- `@matd-dev` - Implementation engineer (sandboxed TDD)

**Commands Included:**
1. `/matd-test` - Generate failing tests (RED state)
2. `/matd-implement` - Implement feature code (RED → GREEN)
3. `/matd-review` - Parallel architecture + code review
4. `/matd-commit` - Validate evidence and create git commit
5. `/matd-update-docs` - Update C4 diagrams and CGC index
6. `/matd-specify-product-brief` - Create product brief via grill-me
7. `/matd-specify-adr` - Create Architecture Decision Record
8. `/matd-specify-solution-design` - Generate solution design (ADR + C4)

**Claude Code Usage:**
```bash
# Direct slash commands (workflows)
/matd-test feat-123
/matd-implement feat-123
/matd-review feat-123
/matd-commit feat-123

# Or spawn agents directly
@matd-architect "Design the authentication system"
```

**Command vs Agent:**
- **Commands** = orchestrated workflows (invoke multiple agents)
- **Agents** = individual specialists (can be used standalone)

**Purpose:** Provides **complete MATD workflow** with orchestrated commands + specialist agents.

---

### 3. matd Extension (SpecKit)

**Installation:**
```bash
specify extension add matd --dev ./harness-tooling/speckit-extensions/matd
```

**What It Provides:**

| Component | Count | Claude Code Exposure | Description |
|-----------|-------|---------------------|-------------|
| **Commands** | 8 | `/speckit.matd.test`<br>`/speckit.matd.implement`<br>`/speckit.matd.review`<br>`/speckit.matd.commit`<br>`/speckit.matd.update-docs`<br>`/speckit.matd.specify-product-brief`<br>`/speckit.matd.specify-adr`<br>`/speckit.matd.specify-solution-design` | Via SpecKit integration |
| **Templates** | Multiple | N/A | SpecKit artifact templates |
| **Hooks** | Multiple | N/A | PreToolUse hooks for Claude Code |

**Commands Included:**
1. `/speckit.matd.test` - Generate failing tests (RED state)
2. `/speckit.matd.implement` - Implement feature code (RED → GREEN)
3. `/speckit.matd.review` - Parallel architecture + code review
4. `/speckit.matd.commit` - Validate evidence and create git commit
5. `/speckit.matd.update-docs` - Update C4 diagrams and CGC index
6. `/speckit.matd.specify-product-brief` - Create product brief
7. `/speckit.matd.specify-adr` - Create Architecture Decision Record
8. `/speckit.matd.specify-solution-design` - Generate solution design

**Claude Code Usage (if SpecKit is initialized):**
```bash
# SpecKit commands (only if specify init was run)
/speckit.matd.test feat-123
/speckit.matd.implement feat-123

# NOT visible as /matd-* commands
```

**Purpose:** Provides **SpecKit-compatible MATD workflow** for projects using SpecKit CLI (`specify` command).

---

## Slash Command Naming Comparison

| Context | Command Prefix | Example | When Visible |
|---------|---------------|---------|--------------|
| **matd Plugin** | `/matd-*` | `/matd-test feat-123` | Always (if plugin installed) |
| **matd Extension** | `/speckit.matd.*` | `/speckit.matd.test feat-123` | Only if SpecKit initialized (`.specify/` exists) |
| **harness-agents** | None | N/A | No commands, only agents |

---

## When to Use What

### Use harness-agents Plugin When:
- ✅ You want **individual specialist agents** to spawn
- ✅ You're building **custom multi-agent workflows**
- ✅ You need **fine-grained control** over agent orchestration
- ❌ You don't need pre-built workflow commands

**Example:**
```
User: "Review this code for security issues"

Spawn @review-specialist with review-check-correctness skill
```

### Use matd Plugin When:
- ✅ You want **complete MATD workflow** out-of-the-box
- ✅ You prefer **orchestrated commands** over manual agent spawning
- ✅ You're NOT using SpecKit CLI
- ✅ You want `/matd-*` slash commands in Claude Code

**Example:**
```bash
/matd-test feat-auth          # Orchestrates @matd-qa
/matd-implement feat-auth     # Orchestrates @matd-dev
```

### Use matd Extension When:
- ✅ You're using **SpecKit for spec-driven development**
- ✅ You've run `specify init` in your project
- ✅ You want **SpecKit artifact templates** (specs, plans, etc.)
- ✅ You want `/speckit.matd.*` commands instead of `/matd-*`

**Example:**
```bash
specify init . --integration claude
/speckit.matd.test feat-auth  # SpecKit-aware workflow
```

---

## Can You Install All Three?

**YES** - They can coexist:

```bash
# Install all three
claude plugin install harness-agents --scope project
claude plugin install matd --scope project
specify extension add matd --dev ./speckit-extensions/matd
```

**Result:**
- `@test-specialist`, `@dev-specialist`, etc. (harness-agents)
- `@matd-architect`, `@matd-qa`, etc. (matd plugin)
- `/matd-test`, `/matd-implement`, etc. (matd plugin)
- `/speckit.matd.test`, `/speckit.matd.implement`, etc. (matd extension, if SpecKit initialized)

**No Conflicts:** Different namespaces for agents and commands.

---

## Installation Matrix

| What You Want | Install This | Provides |
|---------------|-------------|----------|
| **Specialist agents only** | `harness-agents` | 5 agents, 16 skills |
| **MATD workflow + agents** | `matd` plugin | 6 agents, 8 commands |
| **SpecKit MATD workflow** | `matd` extension | 8 SpecKit commands |
| **Everything** | All three | All agents + both command sets |

---

## Command Routing in Claude Code

### How Slash Commands Work

```
User types: /matd-test feat-123

Claude Code:
1. Checks loaded plugins for commands
2. Finds matd plugin → commands/test.md
3. Loads command definition
4. Executes command (may spawn agents internally)
```

### How Agents Work

```
User types: @test-specialist

Claude Code:
1. Checks loaded plugins for agents
2. Finds harness-agents plugin → agents/test-specialist.md
3. Spawns agent with that definition
4. Agent uses skills from loaded plugins
```

### How SpecKit Commands Work

```
User types: /speckit.matd.test feat-123

Claude Code:
1. Checks if .specify/ directory exists
2. Reads .specify/extensions/.registry
3. Finds matd extension → commands/test.md
4. Loads command (SpecKit-aware)
5. Executes with SpecKit artifact templates
```

---

## Summary Table

| Aspect | harness-agents | matd Plugin | matd Extension |
|--------|---------------|-------------|----------------|
| **Type** | Plugin | Plugin | Extension |
| **Agents** | 5 specialists | 6 MATD agents | 0 (uses plugin agents) |
| **Commands** | 0 | 8 (`/matd-*`) | 8 (`/speckit.matd.*`) |
| **Skills** | 16 | 0 | 0 |
| **Slash Commands** | None | `/matd-test`, `/matd-implement`, etc. | `/speckit.matd.test`, etc. |
| **Agent Mentions** | `@test-specialist`, `@dev-specialist`, etc. | `@matd-architect`, `@matd-qa`, etc. | N/A |
| **Use Case** | Individual specialists | Complete workflow | SpecKit integration |
| **Requires SpecKit** | No | No | Yes (`.specify/` dir) |
| **Can Coexist** | Yes | Yes | Yes |

---

## Key Takeaways

1. **harness-agents** = Building blocks (agents + skills, no commands)
2. **matd plugin** = Complete workflow (agents + commands, Claude Code native)
3. **matd extension** = SpecKit variant (commands only, requires SpecKit)

4. **Slash commands** are different:
   - `/matd-*` = Claude Code plugin commands
   - `/speckit.matd.*` = SpecKit extension commands

5. **All can be installed together** without conflicts (different namespaces)

6. **Most users want:** `matd` plugin for `/matd-*` commands + agents
