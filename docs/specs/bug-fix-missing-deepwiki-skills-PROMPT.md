# Subagent Investigation Prompt: Missing deepwiki/litho Skills Integration

**Task Type:** Architectural analysis + integration recommendation
**Expected Deliverable:** Skill analysis + architecture recommendation + size/performance data
**Estimated Effort:** 8 story points (5 investigation + 3 implementation)

---

## Your Mission

The harness-tooling plugin manifest is missing three critical skills from the deepwiki-rs repository. Before integrating them, we need to understand:

1. **What these skills do** - Purpose, inputs, outputs, execution model
2. **What they depend on** - Binaries, files, network services
3. **Where they should run** - Agent container, separate litho container, or hybrid
4. **Cost of integration** - Container size, build time, complexity

You will investigate these questions and make a **data-driven architectural recommendation**.

---

## Context

### The Problem

Current plugin manifest: `harness-tooling/.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json`

**Missing from manifest:**
1. `deepwiki-rs/assets/skill-litho/SKILL.md`
2. `deepwiki-rs/.skills/ai-context-generator/SKILL.md`
3. `deepwiki-rs/.ai-context/SKILL.md`

### Current Architecture

- **Agent container**: Runs Claude Code CLI, executes skills, has access to workspace
- **Litho container**: Separate service running deepwiki/litho (compose profile `--profile litho`)
- **Separate containers**: Skills might need to call from agent → litho

### Key Question

**Should we integrate these skills into the agent container (single container) or keep them calling the separate litho container (multi-container)?**

This decision affects:
- Container size (sandbox is a dev container - weight matters)
- Build time (slower builds = worse DX)
- Execution speed (docker exec adds latency)
- Maintenance complexity (RPC vs direct calls)

---

## Investigation Plan (Execute in Order)

### Phase 1: Understand the Skills (REQUIRED)

**Objective:** Document what each skill does and needs.

#### Step 1.1: Read skill definitions

```bash
cd ~/repositories/harness-workplace/deepwiki-rs

# Read each skill
rtk cat assets/skill-litho/SKILL.md
rtk cat .skills/ai-context-generator/SKILL.md
rtk cat .ai-context/SKILL.md
```

**For each skill, document:**

| Skill | Purpose | Inputs | Outputs | Calls binary? | Writes files? |
|-------|---------|--------|---------|---------------|---------------|
| skill-litho | [TBD] | [TBD] | [TBD] | litho? deepwiki? | Where? |
| ai-context-generator | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| ai-context | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

#### Step 1.2: Check for implementation files

```bash
cd ~/repositories/harness-workplace/deepwiki-rs

# Look for scripts/code near skills
rtk find assets/skill-litho -type f
rtk find .skills/ai-context-generator -type f
rtk find .ai-context -type f

# Search for invocation examples
rtk grep -r "skill-litho" . --include="*.md" --include="*.sh" | rtk head -20
rtk grep -r "ai-context-generator" . --include="*.md" --include="*.sh" | rtk head -20
```

**Document:**
- Are there Python/Bash/Rust files alongside the SKILL.md files?
- How are these skills invoked? (examples from docs/code)

#### Step 1.3: Identify binary dependencies

```bash
cd ~/repositories/harness-workplace/deepwiki-rs

# What binaries do skills reference?
rtk grep -E "\blitho\b|\bdeepwiki\b|\bcargo\b|\brustc\b" assets/skill-litho/SKILL.md
rtk grep -E "\blitho\b|\bdeepwiki\b|\bcargo\b|\brustc\b" .skills/ai-context-generator/SKILL.md
rtk grep -E "\blitho\b|\bdeepwiki\b|\bcargo\b|\brustc\b" .ai-context/SKILL.md
```

**Document:**
- Does skill-litho call `litho` binary? With what arguments?
- Does ai-context-generator call `deepwiki`?
- Any Rust/cargo requirements?

---

### Phase 2: Check Current Container State (REQUIRED)

**Objective:** Understand what's already available in each container.

#### Step 2.1: Start both containers

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc --profile litho
```

#### Step 2.2: Check agent container

```bash
# What's in the agent container?
rtk docker exec harness-agent-sta2e-agent-workspace which litho || echo "NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which deepwiki || echo "NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which cargo || echo "NOT FOUND"
rtk docker exec harness-agent-sta2e-agent-workspace which rustc || echo "NOT FOUND"

# What's installed?
rtk docker exec harness-agent-sta2e-agent-workspace dpkg -l | rtk grep -i rust || echo "No Rust packages"
```

**Document:**
- Agent container has: [list available binaries]
- Agent container missing: [list missing binaries that skills need]

#### Step 2.3: Check litho container

```bash
# What's in the litho container?
rtk docker exec harness-litho-sta2e-agent-workspace which litho
rtk docker exec harness-litho-sta2e-agent-workspace which deepwiki
rtk docker exec harness-litho-sta2e-agent-workspace litho --version
rtk docker exec harness-litho-sta2e-agent-workspace deepwiki --version

# Check if litho container has Rust
rtk docker exec harness-litho-sta2e-agent-workspace which cargo || echo "NOT FOUND"
```

**Document:**
- Litho container has: [list available binaries with versions]
- Can litho container execute the skills directly?

---

### Phase 3: Measure Container Size Impact (REQUIRED)

**Objective:** Get hard numbers for the architectural decision.

#### Step 3.1: Measure baseline

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Current agent image size
rtk docker images harness-agent | rtk awk 'NR==2 {print $1,$2,$7}'

# Document: harness-agent size = [XXX MB]
```

#### Step 3.2: Test with full Rust toolchain

Create `Dockerfile.test-rust-full`:

```dockerfile
# Copy FROM line from actual Dockerfile
FROM [check actual base image in Dockerfile]

# Install Rust toolchain (standard method)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Verify installation
RUN rustc --version && cargo --version

# Simulate installing deepwiki/litho
# (Skip actual install to save time, just measure toolchain overhead)
```

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Build test image
time rtk docker build -f Dockerfile.test-rust-full -t harness-rust-test-full . 2>&1 | rtk tee /tmp/rust-full-build.log

# Measure size
rtk docker images harness-rust-test-full | rtk awk 'NR==2 {print $1,$2,$7}'

# Document results
echo "Build time:" | rtk grep "real" /tmp/rust-full-build.log
# Size increase = [YYY MB]
# Build time = [X min Y sec]
```

#### Step 3.3: Test multi-stage build (binaries only)

**First, check how litho/deepwiki are installed:**

```bash
# Check litho Dockerfile to understand installation
cd ~/repositories/harness-workplace/harness-sandbox
rtk grep -B5 -A5 "litho" docker-compose.yml | rtk grep image
# This tells us the litho image - check its Dockerfile if available
```

Create `Dockerfile.test-rust-bins`:

```dockerfile
# Builder stage - has Rust toolchain
FROM rust:1.75-alpine AS builder
WORKDIR /build

# Install deepwiki/litho (adjust based on actual installation method)
# If they're from crates.io:
RUN cargo install deepwiki litho
# OR if they're from git:
# RUN git clone [repo] && cd [repo] && cargo build --release

# Runtime stage - copy binaries only
FROM [actual agent base image]

# Copy compiled binaries from builder
COPY --from=builder /usr/local/cargo/bin/deepwiki /usr/local/bin/
COPY --from=builder /usr/local/cargo/bin/litho /usr/local/bin/

# Verify they work
RUN deepwiki --version && litho --version
```

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Build multi-stage image
time rtk docker build -f Dockerfile.test-rust-bins -t harness-rust-test-bins . 2>&1 | rtk tee /tmp/rust-bins-build.log

# Measure size
rtk docker images harness-rust-test-bins | rtk awk 'NR==2 {print $1,$2,$7}'

# Document results
echo "Build time:" | rtk grep "real" /tmp/rust-bins-build.log
# Size increase = [ZZZ MB]
# Build time = [X min Y sec]
```

**Create comparison table:**

| Approach | Size | Size Δ | Build Time | Build Time Δ |
|----------|------|--------|------------|--------------|
| Baseline (current) | XXX MB | - | Y min | - |
| Full Rust toolchain | YYY MB | +AAA MB | Z min | +BB min |
| Binaries only (multi-stage) | ZZZ MB | +CCC MB | W min | +DD min |

---

### Phase 4: Measure RPC Latency (REQUIRED)

**Objective:** Understand the cost of docker exec (if we keep separate containers).

#### Step 4.1: Test docker exec overhead

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho

# Single call
time rtk docker exec harness-litho-sta2e-agent-workspace echo "test"

# Average over 20 calls
for i in {1..20}; do
  /usr/bin/time -f "%e" docker exec harness-litho-sta2e-agent-workspace echo "test" 2>&1
done | rtk awk '{sum+=$1; count++} END {printf "Average: %.3f seconds\n", sum/count}'
```

**Document:**
- Single docker exec: [XX ms]
- Average docker exec: [YY ms]
- Is this acceptable latency for skill execution?

#### Step 4.2: Test actual litho command latency

```bash
# How long does a real litho command take?
time rtk docker exec harness-litho-sta2e-agent-workspace litho --help

# Try a heavier operation if available
time rtk docker exec harness-litho-sta2e-agent-workspace litho [some-operation] 2>&1 || echo "Command failed, adjust as needed"
```

**Document:**
- Litho help command: [XXX ms]
- Real operation: [YYY ms or N/A]
- Docker exec overhead as % of total: [Z%]

---

### Phase 5: Analyze Current Plugin Integration (REQUIRED)

**Objective:** Understand the existing plugin manifest structure.

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Check current manifest
rtk cat .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json

# How many skills already integrated?
rtk jq '.skills | length' .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json

# List existing skills
rtk jq '.skills[].path' .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
```

**Document:**
- Current plugin has [N] skills
- Existing skills: [list paths]
- Do existing skills use docker exec pattern? (check skill content)

```bash
# Check if existing skills reference docker
cd ~/repositories/harness-workplace
rtk find harness-tooling/.agents/plugins/harness-deepwiki-skill -name "*.md" -exec grep -l "docker exec\|docker run" {} \;
```

---

### Phase 6: Make Architectural Recommendation (REQUIRED)

Based on your findings, fill out this decision matrix:

#### Decision Matrix

| Criterion | Model A: Unified (agent) | Model B: RPC (litho) | Model C: Hybrid |
|-----------|-------------------------|---------------------|-----------------|
| **Container size** | +[XXX] MB | +0 MB | +[YY] MB |
| **Build time** | +[X] min | +0 min | +[Y] min |
| **Skill execution latency** | ~0 ms | ~[ZZ] ms | Mixed |
| **Maintenance complexity** | Low (direct calls) | High (wrappers) | Medium |
| **Dev container weight** | Heavy | Light | Medium |
| **Setup complexity** | Low (one container) | Med (two containers) | High (conditional) |
| **Rust toolchain needed** | Yes/No | No | Partial |
| **Can skills share code?** | Yes | Harder | Depends |

#### Scoring Criteria

**Model A (Unified) is better if:**
- Size increase < 300 MB
- Build time increase < 5 min
- Skills need frequent execution (latency matters)
- Skills share dependencies or data

**Model B (RPC) is better if:**
- Size increase > 500 MB
- Build time increase > 5 min
- Skills are infrequently used
- Container weight is critical (dev container constraint)

**Model C (Hybrid) is better if:**
- Some skills are lightweight (pure text/prompts)
- Some skills are heavy (need Rust)
- Mixed usage patterns

#### Your Recommendation

**Recommended Model:** [A/B/C]

**Justification:**
[2-3 paragraphs explaining why based on the data you collected]

**Key Data Points Supporting This:**
- [Data point 1 with numbers]
- [Data point 2 with numbers]
- [Data point 3 with numbers]

**Tradeoffs Accepted:**
- [What we're giving up with this choice]

**Tradeoffs Avoided:**
- [What we're NOT giving up vs other choices]

---

## Deliverable Format

Submit a structured report with these sections:

### 1. Executive Summary

- **Problem:** Missing 3 skills from plugin manifest
- **Recommendation:** Use Model [A/B/C] because [1 sentence]
- **Cost:** [size/time/complexity summary]

### 2. Skill Analysis

For each of the 3 missing skills:

**Skill: [name]**
- Purpose: [what it does]
- Inputs: [what it needs]
- Outputs: [what it produces]
- Dependencies: [binaries/files/services needed]
- Execution model: [calls litho? generates files? prompts only?]

### 3. Container Impact Analysis

**Current State:**
- Agent container: [size, has X, missing Y]
- Litho container: [size, has A, missing B]

**Size Impact Measurements:**
- Full Rust toolchain: +[XXX] MB, +[Y] min build
- Binaries only: +[ZZZ] MB, +[W] min build

**Latency Measurements:**
- Docker exec overhead: [XX] ms average
- Litho command execution: [YYY] ms
- Overhead as % of total: [Z]%

### 4. Architectural Recommendation

**Recommended Model:** [A/B/C]

**Decision Matrix:** [Include completed table from Phase 6]

**Justification:** [2-3 paragraphs with data references]

**Implementation Approach:**

If Model A:
```markdown
1. Modify Dockerfile to add Rust (multi-stage)
2. Add skills to plugin manifest at paths:
   - harness-tooling/.agents/plugins/harness-deepwiki-skill/skills/litho.md
   - harness-tooling/.agents/plugins/harness-deepwiki-skill/skills/ai-context-generator.md
   - harness-tooling/.agents/plugins/harness-deepwiki-skill/skills/ai-context.md
3. Update plugin.json to reference new skill paths
4. Consider deprecating separate litho container (if no longer needed)
```

If Model B:
```markdown
1. Create wrapper scripts in harness-tooling/wrappers/
2. Create skill manifests that call wrappers via docker exec
3. Update plugin.json to reference wrapper skills
4. Document RPC pattern for future skill developers
```

If Model C:
```markdown
1. Light skills: [list] → Model A approach
2. Heavy skills: [list] → Model B approach
3. [Detailed breakdown per skill]
```

### 5. Validation Plan

Provide exact commands to verify the chosen approach:

```bash
# Step 1: [validation command]
# Expected: [what success looks like]

# Step 2: [validation command]
# Expected: [what success looks like]

# etc.
```

### 6. Risk Assessment

**Risks:**
- [What could go wrong]
- [Performance concerns]
- [Maintenance burden]

**Mitigation:**
- [How to address each risk]

**Rollback:**
- [How to revert if it doesn't work]

---

## Tools & Constraints

**You MUST use:**
- `rtk` prefix for all bash commands
- `verification-before-completion` skill before claiming anything works
- Actual measurements (no guessing)

**Work from:**
- Repository root: `/home/minged01/repositories/harness-workplace/`
- Test project: `~/repositories/sta2e-agent-workspace`

**Reference:**
- Full spec: [harness-tooling/docs/specs/bug-fix-missing-deepwiki-skills.md](./bug-fix-missing-deepwiki-skills.md)
- Deepwiki repo: `/home/minged01/repositories/harness-workplace/deepwiki-rs/`

**Do NOT:**
- Make any changes to files (investigation only)
- Skip measurements (we need data to decide)
- Implement anything (just provide the plan)
- Guess container sizes (build and measure)

---

## Success Criteria

Your investigation is complete when you have:

1. ✅ Documented purpose/dependencies of all 3 skills
2. ✅ Measured container size impact for both Rust approaches
3. ✅ Measured docker exec latency with numbers
4. ✅ Completed decision matrix with data
5. ✅ Made clear recommendation (A/B/C) with justification
6. ✅ Provided step-by-step implementation approach
7. ✅ Listed validation commands for chosen approach

Report back with your complete analysis and recommendation.
