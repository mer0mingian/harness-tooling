# Implementation Prompt: Missing deepwiki/litho Skills Integration

**Task Type:** Plugin integration (Model B - RPC via docker exec)
**Story Points:** 3
**Investigation Reference:** [Investigation Report](./bug-fix-missing-deepwiki-skills-PROMPT.md)

---

## Your Mission

Integrate three missing skills from deepwiki-rs into the harness-tooling plugin using the approved RPC approach (docker exec to litho container). The architectural decision (Model B) has been made and approved.

**What you will do:**
1. Fix broken plugin manifest path
2. Create/copy 3 skill files with docker exec wrappers
3. Update plugin.json to reference correct paths
4. Validate skills are discoverable and executable
5. Use verification-before-completion skill before claiming success

---

## Architecture Summary (From Investigation)

**Approved Model:** Model B (RPC via separate litho container)

**Why:**
- Zero container bloat (+0 MB vs +1.24GB for Rust toolchain)
- Docker exec latency negligible (54ms vs 10s-10min real operations)
- Matches existing architecture (litho already separate service)

**Implementation Pattern:**
- skill-litho: Wrapper with `docker exec harness-litho-${PROJECT_NAME} litho ...`
- ai-context-generator: Prompt-based (no binary, just markdown)
- ai-context: Pure documentation (reference files)

---

## Implementation Steps

### Step 1: Create Skills Directory Structure

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Create directory for skills
mkdir -p .agents/plugins/harness-deepwiki-skill/skills
```

### Step 2: Copy/Create Skill 1 - litho (Wrapper)

**File:** `.agents/plugins/harness-deepwiki-skill/skills/litho.md`

**Content:**
```markdown
---
name: litho
description: Generate comprehensive C4 architecture documentation using litho (deepwiki-rs) engine
---

# Litho Documentation Generator

Use this skill to generate comprehensive documentation for a codebase, including C4 architecture diagrams (Context, Container, Component, Code levels).

## When to Use

- **Initial project documentation** - Generate complete docs for new or undocumented projects
- **Architecture visualization** - Create C4 diagrams showing system structure
- **Large codebase analysis** - Understand complex projects through generated documentation
- **Documentation updates** - Refresh docs after major architectural changes

## Prerequisites

**REQUIRED:** Litho container must be running. Start with:
```bash
harness up --profile litho
```

If you see "container not found" errors, the litho container is not running.

## Usage

### Basic Documentation Generation

Generate docs in default location (`./litho.docs/`):

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs
```

**Note:** `PROJECT_NAME` is set by harness based on your working directory.

### With Model Selection

Choose specific LLMs for different phases:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs \
  --model-efficient gpt-4o-mini \
  --model-powerful claude-sonnet-4
```

**Model Options:**
- Efficient (bulk processing): `gpt-4o-mini`, `gpt-3.5-turbo`
- Powerful (complex analysis): `claude-sonnet-4`, `gpt-4o`, `claude-opus-4`

### Skip Preprocessing (If Already Done)

Preprocessing analyzes file structure and dependencies. Skip if you've run litho before and structure hasn't changed:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  --skip-preprocessing
```

### Skip Research Phase (Quick Test)

Research phase calls LLM APIs (expensive/slow). Skip for testing:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.test \
  --skip-research
```

## Output Structure

Litho generates:
- `litho.docs/architecture/` - C4 diagrams (mermaid format)
- `litho.docs/components/` - Component documentation
- `litho.docs/context/` - System context and domain model
- `litho.docs/decisions/` - Architecture decision records

## Environment Variables

- `PROJECT_NAME` - Auto-set by harness (e.g., `sta2e-agent-workspace`)
- Container name: `harness-litho-${PROJECT_NAME}`

## Troubleshooting

**Error: "container not found"**
- **Cause:** Litho container not running
- **Fix:** Run `harness up --profile litho` from your project directory

**Error: "permission denied" or "no such file"**
- **Cause:** Path mismatch - litho can't access project files
- **Fix:** Check bind mount in `docker-compose.yml` (should mount workspace to `/workspace`)

**Error: SSL certificate verification failed**
- **Cause:** Corporate proxy issues (Cloudflare/Zscaler)
- **Fix:** Ensure using `litho:stony` image variant (has corporate CA certificates)

**Error: API key not found**
- **Cause:** Litho needs LLM API keys (Anthropic/OpenAI)
- **Fix:** Check environment variables in litho container: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`

## Performance Notes

- **Typical runtime:** 10 seconds to 10 minutes (depends on codebase size and LLM API speed)
- **Docker exec overhead:** ~54ms (negligible compared to LLM API calls)
- **Cost:** Varies by model and codebase size (~$0.10-$5.00 per full generation)

## Related

- Quick start guide: `/workspace/project/assets/skill-litho/quick-start.sh`
- CI integration: `/workspace/project/assets/skill-litho/ci-setup.sh`
```

### Step 3: Copy Skill 2 - ai-context-generator

**File:** `.agents/plugins/harness-deepwiki-skill/skills/ai-context-generator.md`

**Copy from source:**
```bash
cd ~/repositories/harness-workplace/harness-tooling

# Copy the original skill (prompt-based, no modifications needed)
cp ~/repositories/harness-workplace/deepwiki-rs/.skills/ai-context-generator/SKILL.md \
   .agents/plugins/harness-deepwiki-skill/skills/ai-context-generator.md
```

**Verify frontmatter:**
```bash
rtk head -10 .agents/plugins/harness-deepwiki-skill/skills/ai-context-generator.md
# Should contain: ---\nname: ...\ndescription: ...\n---
```

### Step 4: Copy Skill 3 - ai-context

**File:** `.agents/plugins/harness-deepwiki-skill/skills/ai-context.md`

**Copy from source:**
```bash
cd ~/repositories/harness-workplace/harness-tooling

# Copy the original skill (pure documentation reference)
cp ~/repositories/harness-workplace/deepwiki-rs/.ai-context/SKILL.md \
   .agents/plugins/harness-deepwiki-skill/skills/ai-context.md
```

**Verify frontmatter:**
```bash
rtk head -10 .agents/plugins/harness-deepwiki-skill/skills/ai-context.md
# Should contain: ---\nname: ...\ndescription: ...\n---
```

### Step 5: Update plugin.json

**File:** `.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json`

**Current content (BROKEN):**
```json
{
  "name": "harness-deepwiki-skill",
  "version": "1.0.0",
  "description": "Architecture documentation skills",
  "author": "Daniel Minges",
  "skills": "../../../skills/architecture-wiki/"
}
```

**New content (FIXED):**
```json
{
  "name": "harness-deepwiki-skill",
  "version": "1.1.0",
  "description": "Architecture documentation generation skills (litho/deepwiki-rs)",
  "author": "Daniel Minges",
  "skills": [
    "skills/litho.md",
    "skills/ai-context-generator.md",
    "skills/ai-context.md"
  ]
}
```

**Changes:**
- Version bumped to 1.1.0
- `skills` changed from string (broken path) to array of relative paths
- Description updated to mention litho

### Step 6: Verify File Structure

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Check directory structure
rtk find .agents/plugins/harness-deepwiki-skill -type f
# Expected output:
# .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
# .agents/plugins/harness-deepwiki-skill/skills/litho.md
# .agents/plugins/harness-deepwiki-skill/skills/ai-context-generator.md
# .agents/plugins/harness-deepwiki-skill/skills/ai-context.md

# Verify plugin.json is valid JSON
rtk cat .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json | jq .
# Expected: Pretty-printed JSON (no parse errors)
```

---

## Validation Plan (REQUIRED - Use verification-before-completion)

**You MUST run ALL validation steps and confirm success before claiming the fix works.**

### Validation Step 1: Plugin Manifest Valid

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Check plugin.json syntax
rtk jq empty .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
# Expected: No output (means valid JSON)

# Check skills array
rtk jq '.skills | length' .agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json
# Expected: 3
```

**Success criteria:** Valid JSON, 3 skills listed

### Validation Step 2: Skill Files Exist

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Check all skill files exist
for skill in skills/litho.md skills/ai-context-generator.md skills/ai-context.md; do
  if [ -f ".agents/plugins/harness-deepwiki-skill/$skill" ]; then
    echo "✓ $skill exists"
  else
    echo "✗ $skill MISSING"
    exit 1
  fi
done
# Expected: All 3 show "✓ ... exists"
```

**Success criteria:** All 3 skill files exist

### Validation Step 3: Skill Files Have Valid Frontmatter

```bash
cd ~/repositories/harness-workplace/harness-tooling

# Check each skill has frontmatter with name and description
for skill in skills/litho.md skills/ai-context-generator.md skills/ai-context.md; do
  echo "Checking $skill:"
  rtk head -10 ".agents/plugins/harness-deepwiki-skill/$skill" | rtk grep -E "^name:|^description:"
done
# Expected: Each skill shows "name: ..." and "description: ..." lines
```

**Success criteria:** All skills have valid frontmatter (name + description)

### Validation Step 4: Litho Container Available

```bash
cd ~/repositories/sta2e-agent-workspace

# Start litho container
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho

# Verify litho container is running
rtk docker ps --format '{{.Names}}' | rtk grep litho
# Expected: harness-litho-sta2e-agent-workspace

# Verify litho binary works
rtk docker exec harness-litho-sta2e-agent-workspace litho --version
# Expected: Version output (e.g., "litho 0.x.y")
```

**Success criteria:** Litho container runs, binary accessible

### Validation Step 5: Docker Exec Wrapper Works

```bash
cd ~/repositories/sta2e-agent-workspace

# Test the exact command from litho skill
PROJECT_NAME=$(basename $PWD)
rtk docker exec harness-litho-${PROJECT_NAME} litho --help
# Expected: Help text from litho binary (not "container not found")
```

**Success criteria:** Docker exec command succeeds

### Validation Step 6: Plugin Installation (Optional - Requires Claude Code)

**Manual test (if Claude Code is available in sandbox):**

```bash
cd ~/repositories/sta2e-agent-workspace

# From inside agent container or on host with Claude Code:
# Install plugin
claude plugin install ~/repositories/harness-workplace/harness-tooling/.agents/plugins/harness-deepwiki-skill

# List skills
claude skill list | rtk grep -E "litho|ai-context"
# Expected: All 3 skills listed
```

**If Claude Code not available, skip this step.** Document that manual testing is needed post-deployment.

**Success criteria (if testable):** Skills discoverable via Claude Code

### Validation Step 7: End-to-End Test (Litho Generation)

```bash
cd ~/repositories/sta2e-agent-workspace

# Run actual litho documentation generation (quick test with --skip-research)
PROJECT_NAME=$(basename $PWD)
rtk docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.test \
  --skip-research

# Check output was created
test -d litho.test && echo "✓ Documentation generated" || echo "✗ Generation failed"
rtk ls -la litho.test/
# Expected: Directory exists with some structure (architecture/, etc.)

# Cleanup
rm -rf litho.test
```

**Success criteria:** Litho generates output without errors

---

## Success Criteria (All Must Pass)

Before claiming success, verify:

- [x] plugin.json is valid JSON with 3 skills in array format
- [x] All 3 skill files exist in correct paths
- [x] All skill files have valid frontmatter (name + description)
- [x] Litho container starts and binary is accessible
- [x] Docker exec wrapper command works
- [x] (Optional) Skills discoverable via Claude Code
- [x] End-to-end litho generation succeeds

---

## Error Handling

### If Validation Fails

**Do NOT proceed if any validation fails. Instead:**

1. **Document the failure:**
   - Which step failed?
   - Actual output vs expected?
   - Error messages?

2. **Check common issues:**
   - plugin.json syntax error? Run `jq` to validate
   - Skill files missing? Check `find` output
   - Litho container not starting? Check `docker ps` and logs
   - Docker exec failing? Verify container name matches PROJECT_NAME

3. **Report the issue:**
   - Provide failure details
   - Suggest potential fixes
   - Ask for guidance

### Common Issues and Fixes

**Issue 1: plugin.json parse error**
- Symptom: `jq` fails to parse
- Check: Missing comma, trailing comma, or unquoted strings
- Fix: Validate JSON syntax carefully

**Issue 2: Skill files not found**
- Symptom: Step 2 shows "MISSING"
- Check: File paths relative to plugin root
- Fix: Verify `cp` commands succeeded, check file permissions

**Issue 3: Litho container not found**
- Symptom: Step 4 or 5 shows "no such container"
- Check: Is `--profile litho` specified in harness up?
- Fix: Restart with correct profile

**Issue 4: Docker exec permission denied**
- Symptom: Step 5 shows permission error
- Check: Container user vs file ownership
- Fix: Verify bind mounts in docker-compose.yml

---

## Tools & Constraints

**You MUST:**
- Use `rtk` prefix for all bash commands
- Use `verification-before-completion` skill before claiming success
- Run ALL validation steps and document results
- Create skill files with proper frontmatter

**Work from:**
- Plugin directory: `/home/minged01/repositories/harness-workplace/harness-tooling/.agents/plugins/harness-deepwiki-skill/`
- Test project: `~/repositories/sta2e-agent-workspace`
- Source skills: `/home/minged01/repositories/harness-workplace/deepwiki-rs/`

**Files to create/modify:**
- `plugin.json` (update from string to array)
- `skills/litho.md` (create wrapper)
- `skills/ai-context-generator.md` (copy from deepwiki-rs)
- `skills/ai-context.md` (copy from deepwiki-rs)

**Do NOT:**
- Modify Dockerfile (not needed - using RPC model)
- Add Rust toolchain (explicitly rejected in architecture decision)
- Change docker-compose.yml (litho service already configured)
- Skip validation steps

---

## Deliverable

Report back with:

1. **Files created/modified:**
   - List of files with line counts
   - Confirmation of plugin.json array format

2. **Validation results:**
   - Output from each validation step (1-7)
   - Success/failure for each
   - Any unexpected behavior

3. **Testing notes:**
   - Docker exec latency observed (compare to 54ms baseline)
   - Any issues with litho container startup
   - Manual Claude Code testing status (done/skipped)

4. **Final status:**
   - "All validations passed - skills integrated"
   - OR "Validation X failed - issue found: [details]"

---

## Story Points Justification

**3 story points** = ~3-4 hours work:
- 30 minutes: Create skill directory structure
- 45 minutes: Write litho wrapper skill with documentation
- 15 minutes: Copy ai-context-generator and ai-context skills
- 15 minutes: Update plugin.json
- 60 minutes: Run validation suite (7 steps including litho generation)
- 45 minutes: Troubleshoot any issues (docker exec, permissions, paths)
- 15 minutes: Documentation and reporting

This is moderate complexity due to docker exec integration and validation requirements.
