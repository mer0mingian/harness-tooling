# Subagent Investigation Prompt: Claude Code Configuration in Sandbox

**Task Type:** Bug investigation and fix proposal
**Expected Deliverable:** Root cause analysis + implementation plan with validation steps
**Estimated Effort:** 5 story points

---

## Your Mission

The harness sandbox container does not provide Claude Code CLI with access to the API key and configuration from the host's `~/.claude/config.json` file. Your job is to:

1. **Investigate** the current state to identify root cause
2. **Propose** concrete fixes with implementation details
3. **Validate** your proposed solution with test commands
4. **Report back** with a complete implementation plan

## Context

### Current Symptoms

1. Claude Code CLI in the agent container cannot authenticate (missing API key)
2. Plugins installed during image build are not available on first Claude Code start
3. Claude Code version is frozen to whatever was in the Docker image at build time

### What We Know

- Host has config at: `~/.claude/config.json`
- Config format:
  ```json
  {
    "primaryApiKey": "sk-ant-api03-...",
    "customApiKeyResponses": {
      "approved": ["..."]
    },
    "extraKnownMarketplaces": {
      "stst-ai-tools-marketplace": {
        "source": {
          "source": "git",
          "url": "git@stash.stepstone.com:7999/atm/stst-ai-tools-marketplace.git"
        }
      }
    }
  }
  ```
- Plugins are not failing during build; they're just unavailable at runtime
- Claude Code should update to latest version on container startup (not during build)

### Repository Structure

- `harness-sandbox/` - Docker runtime repo
  - `Dockerfile` - Agent container build
  - `docker-compose.yml` - Multi-service stack
  - `bin/harness` - Host-side wrapper script
- `harness-tooling/` - Marketplace repo with skills/plugins
- Parent workspace: `/home/minged01/repositories/harness-workplace/`

### Current Working State

You can test with:
```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc
```

---

## Investigation Steps (Follow This Order)

### Step 1: Document Current Installation

**Objective:** Understand how Claude Code is currently installed and configured.

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Check Dockerfile for Claude Code installation
rtk grep -n "claude" Dockerfile
rtk grep -n "pip install" Dockerfile

# Check which user runs the container
rtk grep -E "USER |user:" Dockerfile docker-compose.yml
```

**Document:**
- How is Claude Code installed? (pip, apt, from source?)
- What user does the container run as?
- Are there any existing entrypoint scripts?

### Step 2: Check Current Volume Mounts

**Objective:** See if `.claude/` directory is already mounted.

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Check agent service volumes
rtk grep -A20 "agent:" docker-compose.yml | rtk grep -E "volumes:|  -"
```

**Document:**
- Is `~/.claude` or `${HOME}/.claude` mounted?
- If yes, what's the target path and mode (ro/rw)?
- What other directories are mounted?

### Step 3: Test Config Access in Running Container

**Objective:** Verify if config is accessible and identify the exact problem.

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

# Check container environment
rtk docker exec harness-agent-sta2e-agent-workspace bash -c 'echo "HOME=$HOME USER=$USER UID=$(id -u)"'

# Try to access config
rtk docker exec harness-agent-sta2e-agent-workspace ls -la ~/.claude/ 2>&1
rtk docker exec harness-agent-sta2e-agent-workspace cat ~/.claude/config.json 2>&1

# Check Claude Code installation
rtk docker exec harness-agent-sta2e-agent-workspace which claude
rtk docker exec harness-agent-sta2e-agent-workspace claude --version 2>&1

# Check plugin directories
rtk docker exec harness-agent-sta2e-agent-workspace find ~ -name "*plugin*" -o -name "*marketplace*" 2>/dev/null | rtk head -20
```

**Document:**
- What's the container's HOME directory?
- Does `~/.claude/` exist in the container?
- Can the container user read the config file?
- Is Claude Code installed and in PATH?
- Where are plugins stored?

### Step 4: Compare with Host

**Objective:** Identify path mismatches or permission issues.

```bash
# On host
ls -la ~/.claude/
cat ~/.claude/config.json | jq .primaryApiKey | rtk head -c 30

# In container (from Step 3)
# Compare paths, permissions, ownership
```

**Document:**
- Are paths identical?
- Are UIDs different?
- Is there a permission mismatch?

### Step 5: Identify Root Cause

Based on Steps 1-4, determine which hypothesis is correct:

- **Hypothesis A:** Config directory not mounted → Need to add volume mount
- **Hypothesis B:** Permission/UID mismatch → Need user directive or chown
- **Hypothesis C:** Path mismatch → Claude Code looks elsewhere
- **Hypothesis D:** No update mechanism → Need entrypoint script

---

## Implementation Plan Template

Once you've identified root cause, propose a solution using this template:

### Root Cause

[1-2 sentences describing exactly what's wrong]

### Proposed Fix

**Fix 1: [Title]**

File: `harness-sandbox/[filename]`

**Current state:**
```yaml/dockerfile/bash
[Show current code]
```

**Proposed change:**
```yaml/dockerfile/bash
[Show new code with inline comments]
```

**Rationale:** [Why this fixes the problem]

**Fix 2: [Title]** (if multiple fixes needed)

[Same format as Fix 1]

### Implementation Order

1. [First thing to change]
2. [Second thing to change]
3. [etc.]

### Validation Commands

Provide exact commands to verify the fix works:

```bash
# Step 1: Clean start
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness down
~/repositories/harness-workplace/harness-sandbox/bin/harness build
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

# Step 2: Verify config access
rtk docker exec harness-agent-sta2e-agent-workspace [command to check config]
# Expected output: [what success looks like]

# Step 3: Verify API key
rtk docker exec harness-agent-sta2e-agent-workspace [command to verify API key]
# Expected output: [what success looks like]

# Step 4: Verify plugin availability
rtk docker exec harness-agent-sta2e-agent-workspace [command to list plugins]
# Expected output: [what success looks like]

# Step 5: Verify Claude Code version
rtk docker exec harness-agent-sta2e-agent-workspace claude --version
# Expected output: [latest version or matches host]
```

### Risk Assessment

**Risks:**
- [What could go wrong]
- [Any breaking changes]

**Mitigation:**
- [How to reduce risks]

**Rollback procedure:**
```bash
# Commands to revert if fix fails
rtk git checkout HEAD [files]
```

---

## Deliverable Format

Submit your findings as a structured report with these sections:

### 1. Investigation Summary

- Current state (1-2 paragraphs)
- Root cause identified (1 paragraph)
- Evidence from investigation steps

### 2. Proposed Solution

- Detailed fix(es) with code changes
- Implementation order
- Rationale for each change

### 3. Validation Plan

- Step-by-step validation commands
- Expected outputs for each step
- Success criteria

### 4. Risk Assessment

- Potential risks
- Mitigation strategies
- Rollback procedure

---

## Tools & Constraints

**You MUST use:**
- `rtk` prefix for all bash commands (token optimization)
- `verification-before-completion` skill before claiming anything works

**Work from:**
- Repository root: `/home/minged01/repositories/harness-workplace/`
- Test project: `~/repositories/sta2e-agent-workspace` or `~/repositories/sta2e-vtt-lite-system`

**Reference spec:**
- Full specification: [harness-tooling/docs/specs/bug-fix-claude-config-in-sandbox.md](./bug-fix-claude-config-in-sandbox.md)

**Do NOT:**
- Make any changes to files (investigation only - report findings)
- Implement the fix (just provide the plan)
- Guess or assume - test everything
- Skip validation commands

---

## Success Criteria

Your investigation is complete when you can answer:

1. ✅ What exactly is preventing config access?
2. ✅ What specific changes are needed? (file names, line numbers, code snippets)
3. ✅ How will we verify the fix works? (exact commands + expected output)
4. ✅ What are the risks and rollback steps?

Report back with your findings and we'll proceed with implementation.
