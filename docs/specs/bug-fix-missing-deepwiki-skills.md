# Bug Fix Spec: Missing deepwiki/litho Skills Integration

**Status:** Investigation required
**Date:** 2026-05-15
**Scope:** deepwiki/litho architecture analysis, skill integration strategy, container weight assessment
**Story Points:** 8 (investigation: 5, implementation: TBD after investigation)

---

## 1. Bug Description

The harness-tooling plugin manifest at [.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json](../../.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json) contains fewer skills than what exists in the deepwiki-rs repository. Several critical skills for operating deepwiki/litho are missing from the harness marketplace integration.

### Missing Skills

From `deepwiki-rs` repository at `/home/minged01/repositories/harness-workplace/deepwiki-rs/`:

1. **`assets/skill-litho/SKILL.md`** - Litho-specific skill
2. **`.skills/ai-context-generator/SKILL.md`** - AI context generation skill  
3. **`.ai-context/SKILL.md`** - AI context handling skill

### Current Integration Architecture

The harness currently runs deepwiki in a **separate container** attached to the sandbox (litho service in docker-compose.yml). This may or may not be the optimal architecture for skill integration.

### Expected Behavior

All skills required to operate deepwiki/litho should be:
- Discoverable via Claude Code plugin system
- Executable from agent container
- Properly integrated with the current architecture (single container vs multi-container)

### Actual Behavior

Critical deepwiki/litho skills are missing from the plugin manifest, limiting the agent's ability to use deepwiki's full capabilities.

---

## 2. Investigation Scope

This bug requires a **research-first approach** because:

1. **Architecture unclear**: We don't know if the separate-container model is optimal or if skills should run in the agent container
2. **Dependency tree unknown**: We don't know what runtime dependencies these skills have (Rust/cargo, litho binary, etc.)
3. **Container weight unknown**: The sandbox currently lacks Rust/cargo; we need to assess size impact before committing to an architectural direction

### Key Questions to Answer

#### Q1: What do these skills do?

For each missing skill, document:
- **Purpose**: What problem does it solve?
- **Inputs/outputs**: What does it consume/produce?
- **Execution model**: Does it call litho CLI, generate files, orchestrate deepwiki, etc.?

#### Q2: What are the runtime dependencies?

For each missing skill, identify:
- **Binary dependencies**: Does it require `litho`, `deepwiki`, `cargo`, Rust toolchain?
- **File dependencies**: Does it need access to specific directories (.litho cache, deepwiki output)?
- **Network dependencies**: Does it make HTTP calls to deepwiki/litho services?

#### Q3: Where should skills execute?

Evaluate three integration models:

**Model A: Skills in Agent Container**
- Skills packaged in harness-tooling plugin
- Executed directly by Claude Code in agent container
- Agent container gets necessary binaries (litho, deepwiki)

**Model B: Skills as RPC Wrappers**
- Skills in harness-tooling are thin wrappers
- Actual execution happens in litho container via docker exec or HTTP API
- Agent container stays lightweight

**Model C: Hybrid**
- Lightweight skills (pure prompt/text) in agent container
- Heavy skills (requiring Rust) proxy to litho container

#### Q4: What is the cost of Rust in agent container?

Measure container size impact:
- **Base agent image size**: Current size without Rust
- **With Rust toolchain**: Size after adding `rustc`, `cargo`, `rustup`
- **With compiled binaries only**: Size after multi-stage build (compile in builder, copy bins to runtime)
- **Build time impact**: How much longer does image build take?

#### Q5: Is the current separate-container architecture optimal?

Consider tradeoffs:

**Separate container (current):**
- ✅ Pro: Agent container stays small
- ✅ Pro: Litho/deepwiki can be updated independently
- ❌ Con: Skills need RPC/exec mechanism
- ❌ Con: Additional container overhead
- ❌ Con: Network latency for skill execution

**Unified container:**
- ✅ Pro: Direct skill execution (no RPC)
- ✅ Pro: Simpler architecture (fewer moving parts)
- ✅ Pro: Better performance (no container boundary)
- ❌ Con: Larger agent image
- ❌ Con: Longer build times
- ❌ Con: Couples agent updates to deepwiki updates

**Context:** The sandbox is used as a dev container, so weight matters more than in a pure runtime environment.

---

## 3. Affected Components

### Files to Investigate

1. **`deepwiki-rs/assets/skill-litho/SKILL.md`**
   - Skill definition and capabilities
   - Runtime requirements
   - Execution model

2. **`deepwiki-rs/.skills/ai-context-generator/SKILL.md`**
   - Skill definition and capabilities
   - Dependencies on deepwiki/litho

3. **`deepwiki-rs/.ai-context/SKILL.md`**
   - Skill definition and capabilities
   - File/directory requirements

4. **`harness-tooling/.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json`**
   - Current plugin manifest
   - Existing skill paths
   - Metadata structure

5. **`harness-sandbox/docker-compose.yml` (litho service)**
   - Current container configuration
   - Volume mounts
   - Network setup
   - Service dependencies

6. **`harness-sandbox/Dockerfile`**
   - Current agent container build
   - Installed packages
   - Available binaries

### Files to Create (Post-Investigation)

Based on investigation findings, may need to create:

1. **Skill wrappers** (if Model B or C chosen)
   - `harness-tooling/.agents/plugins/harness-deepwiki-skill/wrappers/*.sh`

2. **RPC/API layer** (if Model B or C chosen)
   - Service in litho container to accept skill execution requests

3. **Multi-stage Dockerfile** (if Rust needed)
   - Builder stage with Rust toolchain
   - Runtime stage with only compiled binaries

---

## 4. Investigation Plan

### Phase 1: Understand the Skills

**Step 1.1:** Read and document each missing skill

```bash
cd ~/repositories/harness-workplace/deepwiki-rs

# Skill 1: litho
rtk cat assets/skill-litho/SKILL.md
# Document: Purpose, inputs, outputs, dependencies

# Skill 2: ai-context-generator
rtk cat .skills/ai-context-generator/SKILL.md
# Document: Purpose, inputs, outputs, dependencies

# Skill 3: ai-context
rtk cat .ai-context/SKILL.md
# Document: Purpose, inputs, outputs, dependencies
```

**Step 1.2:** Check for associated code/scripts

```bash
# Look for implementation files near skills
rtk find assets/skill-litho -type f ! -name "SKILL.md"
rtk find .skills/ai-context-generator -type f ! -name "SKILL.md"
rtk find .ai-context -type f ! -name "SKILL.md"
```

**Step 1.3:** Search for skill invocation examples

```bash
# How are these skills currently used?
rtk grep -r "skill-litho\|ai-context-generator" deepwiki-rs/ --include="*.md" --include="*.sh"
```

### Phase 2: Analyze Dependencies

**Step 2.1:** Identify binary dependencies

```bash
# What binaries do skills reference?
cd ~/repositories/harness-workplace/deepwiki-rs
rtk grep -E "litho|deepwiki|cargo|rustc" assets/skill-litho/SKILL.md .skills/ai-context-generator/SKILL.md .ai-context/SKILL.md
```

**Step 2.2:** Check current agent container capabilities

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

# What's already installed?
rtk docker exec harness-agent-sta2e-agent-workspace which litho || echo "litho: NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which deepwiki || echo "deepwiki: NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which cargo || echo "cargo: NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which rustc || echo "rustc: NOT FOUND"
```

**Step 2.3:** Check litho container capabilities

```bash
# If litho container runs separately
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho

rtk docker exec harness-litho-sta2e-agent-workspace which litho
rtk docker exec harness-litho-sta2e-agent-workspace which deepwiki
rtk docker exec harness-litho-sta2e-agent-workspace litho --version
```

### Phase 3: Measure Container Size Impact

**Step 3.1:** Baseline agent container size

```bash
cd ~/repositories/harness-workplace/harness-sandbox
rtk docker images | rtk grep harness-agent
# Document: Current size in MB
```

**Step 3.2:** Create test Dockerfile with Rust toolchain

Create `Dockerfile.rust-test`:

```dockerfile
FROM <current-base-image>

# Option A: Full Rust toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Build test
RUN rustc --version && cargo --version
```

**Step 3.3:** Build and measure full toolchain impact

```bash
cd ~/repositories/harness-workplace/harness-sandbox
rtk docker build -f Dockerfile.rust-test -t harness-rust-test-full .
rtk docker images | rtk grep harness-rust-test-full
# Document: Size increase in MB
```

**Step 3.4:** Test multi-stage build approach

Create `Dockerfile.rust-multi-stage`:

```dockerfile
# Builder stage
FROM rust:1.75 AS builder
WORKDIR /build
# Simulate building deepwiki/litho
RUN cargo install --version 0.x.x deepwiki litho

# Runtime stage
FROM <current-base-image>
COPY --from=builder /usr/local/cargo/bin/deepwiki /usr/local/bin/
COPY --from=builder /usr/local/cargo/bin/litho /usr/local/bin/
RUN deepwiki --version && litho --version
```

**Step 3.5:** Build and measure binaries-only impact

```bash
rtk docker build -f Dockerfile.rust-multi-stage -t harness-rust-test-bins .
rtk docker images | rtk grep harness-rust-test-bins
# Document: Size increase in MB
```

**Step 3.6:** Compare build times

```bash
# Measure current build time
time rtk docker build -t harness-agent-current .

# Measure with Rust toolchain
time rtk docker build -f Dockerfile.rust-test -t harness-rust-test-full .

# Measure multi-stage
time rtk docker build -f Dockerfile.rust-multi-stage -t harness-rust-test-bins .

# Document: Build time increase in seconds/minutes
```

### Phase 4: Evaluate Integration Models

**Step 4.1:** Test docker exec latency (for Model B/C)

```bash
# How fast is skill execution via docker exec?
time rtk docker exec harness-litho-sta2e-agent-workspace litho --help

# Run 10 times to get average
for i in {1..10}; do
  time rtk docker exec harness-litho-sta2e-agent-workspace echo "test" 2>&1
done | rtk grep real | rtk awk '{sum+=$2; count++} END {print "Average:", sum/count, "seconds"}'
```

**Step 4.2:** Analyze current plugin manifest structure

```bash
cd ~/repositories/harness-workplace/harness-tooling
rtk cat .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
# Document: How many skills already included? What's their structure?
```

**Step 4.3:** Check if skills reference litho container

```bash
cd ~/repositories/harness-workplace/deepwiki-rs
# Do existing skills already use docker exec pattern?
rtk grep -r "docker exec\|docker run" assets/ .skills/
```

### Phase 5: Make Architectural Recommendation

Based on findings from Phases 1-4, create a decision matrix:

| Criteria | Model A (Agent) | Model B (RPC) | Model C (Hybrid) |
|----------|----------------|---------------|------------------|
| Container size | +XXX MB | +0 MB | +YY MB |
| Build time | +X min | +0 min | +Y min |
| Skill latency | ~0ms | ~XXms | Mixed |
| Maintenance complexity | Low | High | Medium |
| Dev container weight | Heavy | Light | Medium |
| Architectural simplicity | High | Low | Medium |
| **Recommended?** | TBD | TBD | TBD |

**Recommendation criteria:**

- If size increase < 200 MB AND build time < +2 min → Consider Model A
- If size increase > 500 MB OR build time > +5 min → Model B likely better
- If skills have mixed weight (some light, some heavy) → Model C

---

## 5. Implementation Approach (Post-Investigation)

**Note:** Actual implementation depends on Phase 1-5 findings. Below are templates for each model.

### If Model A (Unified Container) is Chosen

**Step A1:** Add Rust to Dockerfile using multi-stage build

```dockerfile
# Builder stage
FROM rust:1.75-alpine AS rust-builder
RUN cargo install deepwiki litho

# Runtime stage  
FROM <current-agent-base>
COPY --from=rust-builder /usr/local/cargo/bin/deepwiki /usr/local/bin/
COPY --from=rust-builder /usr/local/cargo/bin/litho /usr/local/bin/
```

**Step A2:** Add skills to plugin manifest

```bash
cd ~/repositories/harness-workplace/harness-tooling
# Edit .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
# Add paths to three missing skills
```

**Step A3:** Remove or deprecate separate litho container

```bash
# Comment out or remove litho service from docker-compose.yml
# Update documentation to reflect unified architecture
```

### If Model B (RPC Wrapper) is Chosen

**Step B1:** Create skill wrapper scripts in harness-tooling

```bash
# harness-tooling/.agents/plugins/harness-deepwiki-skill/wrappers/litho-skill.sh
#!/bin/bash
docker exec harness-litho-${PROJECT_NAME} litho "$@"
```

**Step B2:** Create skill manifests that call wrappers

```markdown
<!-- harness-tooling/.agents/plugins/harness-deepwiki-skill/skills/litho-wrapper.md -->
---
name: litho
description: Executes litho in the litho container
---

[Skill content calling wrapper script]
```

**Step B3:** Update plugin manifest

```json
{
  "skills": [
    {"path": "skills/litho-wrapper.md"},
    {"path": "skills/ai-context-generator-wrapper.md"},
    {"path": "skills/ai-context-wrapper.md"}
  ]
}
```

### If Model C (Hybrid) is Chosen

Combine elements of A and B based on per-skill analysis.

---

## 6. Validation Steps

Run after implementing chosen model. Use rtk for all commands.

### Step 1: Verify Skill Discovery

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

# Check if skills are visible
rtk docker exec harness-agent-sta2e-agent-workspace claude plugin list | rtk grep -E "litho|ai-context"
# Expected: All three missing skills now listed
```

### Step 2: Verify Skill Execution

```bash
# Test each skill (exact commands depend on skill purpose)
rtk docker exec harness-agent-sta2e-agent-workspace claude skill run litho --help
rtk docker exec harness-agent-sta2e-agent-workspace claude skill run ai-context-generator --help
rtk docker exec harness-agent-sta2e-agent-workspace claude skill run ai-context --help

# Expected: Each skill executes without "command not found" or "dependency missing" errors
```

### Step 3: Measure Container Size (if Model A or C)

```bash
rtk docker images | rtk grep harness-agent
# Expected: Size increase documented and within acceptable limits (<500 MB growth)
```

### Step 4: Measure Build Time

```bash
cd ~/repositories/harness-workplace/harness-sandbox
time rtk docker build -t harness-agent-test .
# Expected: Build completes in reasonable time (<10 min total)
```

### Step 5: Verify Litho Container Still Works (if Model B)

```bash
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho
rtk docker ps | rtk grep litho
# Expected: Litho container running and accessible
```

### Step 6: Functional Test

```bash
# Run a skill that exercises the integration
# Example: Generate AI context for a project
cd ~/repositories/sta2e-agent-workspace
rtk docker exec harness-agent-sta2e-agent-workspace claude skill run ai-context-generator --project-path /workspace/sta2e-agent-workspace

# Expected: Skill completes successfully
# Expected: Output artifacts created in expected locations
```

---

## 7. Acceptance Criteria

### Investigation Phase

- [ ] All three missing skills documented (purpose, dependencies, execution model)
- [ ] Runtime dependencies identified for each skill
- [ ] Container size impact measured for all integration models
- [ ] Build time impact measured for models requiring Rust
- [ ] RPC latency measured for model B/C evaluation
- [ ] Decision matrix completed with data-driven recommendation
- [ ] Architectural recommendation approved by user

### Implementation Phase (criteria depend on chosen model)

**For all models:**
- [ ] All three skills discoverable via Claude Code plugin system
- [ ] All three skills executable without errors
- [ ] Plugin manifest updated with correct paths
- [ ] Documentation updated to reflect new architecture

**If Model A (unified):**
- [ ] Container size increase < 500 MB (or approved by user)
- [ ] Build time increase < 10 min
- [ ] All deepwiki/litho binaries available in agent container
- [ ] Separate litho container deprecated or removed

**If Model B (RPC):**
- [ ] Skill wrapper scripts functional
- [ ] Litho container accessible from agent container
- [ ] RPC latency acceptable (< 500ms per call)
- [ ] Agent container size unchanged

**If Model C (hybrid):**
- [ ] Light skills run directly in agent container
- [ ] Heavy skills proxy to litho container correctly
- [ ] Clear documentation on which skills use which model

---

## 8. Rollback Plan

If the chosen integration model causes issues:

1. **Revert plugin manifest:**
   ```bash
   cd ~/repositories/harness-workplace/harness-tooling
   rtk git checkout HEAD .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
   ```

2. **Revert Dockerfile (if modified):**
   ```bash
   cd ~/repositories/harness-workplace/harness-sandbox
   rtk git checkout HEAD Dockerfile
   ```

3. **Revert docker-compose.yml (if litho service removed):**
   ```bash
   rtk git checkout HEAD docker-compose.yml
   ```

4. **Remove skill wrappers (if created):**
   ```bash
   cd ~/repositories/harness-workplace/harness-tooling
   rtk rm -rf .agents/plugins/harness-deepwiki-skill/wrappers/
   ```

5. **Rebuild and restart:**
   ```bash
   cd ~/repositories/sta2e-agent-workspace
   ~/repositories/harness-workplace/harness-sandbox/bin/harness down
   ~/repositories/harness-workplace/harness-sandbox/bin/harness build
   ~/repositories/harness-workplace/harness-sandbox/bin/harness up
   ```

---

## 9. Related Documentation

- Deepwiki repository: /home/minged01/repositories/harness-workplace/deepwiki-rs/
- Current plugin manifest: harness-tooling/.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
- Litho service config: harness-sandbox/docker-compose.yml (litho service)
- Claude Code plugin specification: Check Claude Code CLI documentation
- Multi-stage Docker builds: https://docs.docker.com/build/building/multi-stage/
- Rust in Docker: https://hub.docker.com/_/rust

---

## 10. Decision Log (To Be Updated During Investigation)

This section will be populated as investigation progresses:

### Investigation Findings

**Skill Analysis:**
- skill-litho: [Purpose, dependencies - TBD]
- ai-context-generator: [Purpose, dependencies - TBD]
- ai-context: [Purpose, dependencies - TBD]

**Container Size Impact:**
- Baseline agent image: [XXX MB - TBD]
- With full Rust toolchain: [YYY MB - TBD]
- With binaries only: [ZZZ MB - TBD]

**Build Time Impact:**
- Baseline build: [X min - TBD]
- With Rust toolchain: [Y min - TBD]
- With multi-stage: [Z min - TBD]

**RPC Latency:**
- docker exec overhead: [XX ms - TBD]

### Architectural Decision

**Chosen Model:** [A/B/C - TBD]

**Justification:** [Data-driven reasoning based on measurements above]

**Tradeoffs Accepted:**
- [List tradeoffs of chosen approach]

**Tradeoffs Rejected:**
- [List tradeoffs of rejected approaches]

---

## 11. Future Improvements (Out of Scope)

- Investigate litho HTTP API if docker exec latency becomes problematic
- Consider packaging deepwiki/litho as standalone binaries (no Rust toolchain needed)
- Evaluate rust-musl for smaller static binaries
- Create automated tests for skill integration
- Document skill development guide for future deepwiki skills
- Consider plugin versioning strategy for deepwiki skills
