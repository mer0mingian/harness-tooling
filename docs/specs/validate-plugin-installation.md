# Validation Spec: Plugin Installation Testing

**Status:** Ready for validation
**Date:** 2026-05-15
**Scope:** Verify Claude Code plugin installation works after credential fix
**Story Points:** 1
**Parent Issue:** Bug fix validation - deepwiki skills integration

---

## 1. Context

The deepwiki skills integration (bug fix #2) included Step 6 validation: "Plugin Installation (Optional - Requires Claude Code)". This was skipped during implementation because the investigation agent determined Claude Code CLI was not available.

**However, the investigation was incomplete:**
- Claude Code IS installed in agent container: `/usr/local/bin/claude` v2.1.91
- Claude Code WAS unable to read config due to Bug #1 (credential access)
- Bug #1 has now been fixed (user namespace remapping)
- Plugin installation SHOULD now work

**This validation confirms:**
1. Claude Code can read credentials (Bug #1 fix successful)
2. Plugin discovery and installation work correctly
3. All 3 skills are discoverable via `claude skill list`

---

## 2. Problem Statement

### What Needs Validation

After fixing credential access (Bug #1), we must verify that:
- Claude Code CLI can authenticate with API key from config.json
- Plugin installation from local filesystem path works
- All 3 deepwiki skills are discoverable and loadable
- Skills have correct metadata (name, description)

### Why This Was Skipped

Original validation agent report stated:
> "Step 6 - Plugin Installation (Skipped): Requires Claude Code CLI not available in current environment"

This was based on:
- Investigation showing config.json was unreadable (permission denied)
- Assumption that without config access, plugin operations would fail
- Conservative approach: skip rather than fail

### Why We Can Test Now

Bug #1 fix enables:
- Container runs as UID 1000 (matches host user)
- Config files readable: `/home/sandbox/.claude/config.json` accessible
- Claude Code should authenticate successfully
- Plugin operations should work

---

## 3. Validation Plan

### Prerequisites

1. **Bug #1 fix applied:**
   - `docker-compose.yml` has `user: "${HOST_UID:-1000}:${HOST_GID:-1000}"`
   - Container rebuilt with new user mapping

2. **Bug #2 fix applied:**
   - Plugin manifest at `.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json`
   - 3 skill files exist: `skills/litho.md`, `skills/ai-context-generator.md`, `skills/ai-context.md`

3. **Containers running:**
   - Agent container: `harness-agent-sta2e-agent-workspace`
   - CGC profile active (default)

### Validation Steps

#### Step 1: Verify Claude Code CLI Available

```bash
rtk docker exec harness-agent-sta2e-agent-workspace which claude
# Expected: /usr/local/bin/claude

rtk docker exec harness-agent-sta2e-agent-workspace claude --version
# Expected: Claude Code v2.1.91 or similar
```

**Success Criteria:** Claude binary found and responds to --version

#### Step 2: Verify Config Access

```bash
rtk docker exec harness-agent-sta2e-agent-workspace bash -c 'cat ~/.claude/config.json | head -3'
# Expected: JSON with primaryApiKey visible (no permission denied)
```

**Success Criteria:** Config file readable, contains API key

#### Step 3: Test Plugin Installation

```bash
# Install from local path (bind-mounted workspace)
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  cd /workspace &&
  claude plugin install /workspace/../harness-tooling/.agents/plugins/harness-deepwiki-skill
'
# Expected: Installation success message or "already installed"
```

**Success Criteria:** No errors, plugin installs or reports already installed

**Common Issues:**
- Path resolution: Verify `/workspace/../harness-tooling` resolves correctly
- Alternative path: Use absolute path `/home/minged01/repositories/harness-workplace/harness-tooling/.agents/plugins/harness-deepwiki-skill` if bind mount structure differs

#### Step 4: List Installed Plugins

```bash
rtk docker exec harness-agent-sta2e-agent-workspace claude plugin list
# Expected: harness-deepwiki-skill listed
```

**Success Criteria:** Plugin appears in list

#### Step 5: List Skills from Plugin

```bash
rtk docker exec harness-agent-sta2e-agent-workspace claude skill list | rtk grep -E "litho|ai-context"
# Expected: 3 skills listed:
#   - litho
#   - ai-context-generator
#   - ai-context
```

**Success Criteria:** All 3 skills discoverable with correct names

#### Step 6: Verify Skill Metadata

```bash
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  claude skill list --json | jq ".[] | select(.name | test(\"litho|ai-context\"))"
'
# Expected: JSON objects with name and description fields for each skill
```

**Success Criteria:** Skills have valid metadata (name, description match skill frontmatter)

---

## 4. Expected Results

### Success Scenario

All validation steps pass:
- ✅ Claude Code CLI accessible
- ✅ Config file readable with API key
- ✅ Plugin installs without errors
- ✅ Plugin listed in `claude plugin list`
- ✅ All 3 skills listed in `claude skill list`
- ✅ Skill metadata matches frontmatter

**Outcome:** Step 6 validation (previously skipped) now PASSES ✅

### Failure Scenarios

**Scenario A: Config Still Unreadable**
- Symptom: Step 2 fails with permission denied
- Root cause: Bug #1 fix not applied or container not rebuilt
- Action: Verify docker-compose.yml has user directive, rebuild container

**Scenario B: Plugin Install Fails (Path Not Found)**
- Symptom: Step 3 fails with "path not found" or "invalid plugin"
- Root cause: Bind mount path incorrect
- Action: Check bind mount configuration, verify harness-tooling is accessible from container

**Scenario C: Skills Not Discovered**
- Symptom: Step 5 shows 0 or fewer than 3 skills
- Root cause: plugin.json syntax error or incorrect skill paths
- Action: Validate plugin.json with `jq`, check skill file paths

**Scenario D: Authentication Fails**
- Symptom: Claude Code commands fail with "not authenticated"
- Root cause: API key invalid or config malformed
- Action: Verify API key in config.json is valid, check for JSON syntax errors

---

## 5. Acceptance Criteria

- [ ] Claude Code CLI accessible in agent container (Step 1)
- [ ] Config file readable with API key visible (Step 2)
- [ ] Plugin installation succeeds (Step 3)
- [ ] Plugin appears in plugin list (Step 4)
- [ ] All 3 skills appear in skill list (Step 5)
- [ ] Skills have correct names: `litho`, `ai-context-generator`, `ai-context`
- [ ] Skill metadata includes descriptions (Step 6)
- [ ] No authentication errors during any operation

---

## 6. Implementation Prompt (For Subagent)

**Mission:** Validate that Claude Code plugin installation works after credential access fix.

**Context:**
- Bug #1 (credential access) has been fixed with user namespace remapping
- Bug #2 (deepwiki skills) has been integrated with 3 skills
- Step 6 validation was skipped because Claude Code appeared unavailable
- Claude Code IS installed (v2.1.91) and should now work with fixed credentials

**Your Task:**
1. Run validation steps 1-6 (see Validation Plan section above)
2. Document actual output for each step
3. Determine if validation PASSES or FAILS
4. If failures occur, diagnose root cause and report

**Working Directory:** `/home/minged01/repositories/harness-workplace/`

**Test Environment:**
- Container: `harness-agent-sta2e-agent-workspace`
- Plugin path: `/workspace/../harness-tooling/.agents/plugins/harness-deepwiki-skill`
- Alternative: `/home/minged01/repositories/harness-workplace/harness-tooling/.agents/plugins/harness-deepwiki-skill`

**Commands to Execute:**

```bash
# Step 1: Verify Claude Code
rtk docker exec harness-agent-sta2e-agent-workspace which claude
rtk docker exec harness-agent-sta2e-agent-workspace claude --version

# Step 2: Verify Config Access
rtk docker exec harness-agent-sta2e-agent-workspace bash -c 'cat ~/.claude/config.json | head -3'

# Step 3: Install Plugin
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  cd /workspace &&
  claude plugin install /workspace/../harness-tooling/.agents/plugins/harness-deepwiki-skill
'

# Step 4: List Plugins
rtk docker exec harness-agent-sta2e-agent-workspace claude plugin list

# Step 5: List Skills (with filter)
rtk docker exec harness-agent-sta2e-agent-workspace claude skill list | rtk grep -E "litho|ai-context"

# Step 6: Verify Skill Metadata (if JSON output supported)
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  claude skill list | grep -A2 -E "litho|ai-context"
'
```

**Success Criteria:**
- All steps produce expected outputs (see Validation Plan)
- No permission denied, authentication, or path errors
- 3 skills discoverable: litho, ai-context-generator, ai-context

**Deliverable:**
Report with:
1. Output from each validation step (1-6)
2. Pass/Fail status for each step
3. Overall validation result: PASS or FAIL
4. If FAIL: Root cause diagnosis and recommended fix

**Estimated Effort:** 1 story point (~30-60 minutes)

**Tools:**
- Use `rtk` prefix for all commands
- Use `verification-before-completion` skill before final report
- Document actual outputs, not assumptions

---

## 7. Post-Validation Actions

### If Validation Passes

1. **Update Bug #2 status:**
   - Mark Step 6 validation as PASSED ✅
   - Update implementation report in docs/specs/

2. **Update open-bugs.md:**
   - Change status from "⚠️ SKIP" to "✅ PASS"
   - Add validation date and notes

3. **Complete Bug #2:**
   - All 7 validation steps now complete (6 PASS, 1 remains - CA cert)
   - Bug #2 considered resolved except for infrastructure issue (CA cert)

### If Validation Fails

1. **Create bug report:**
   - Document failure symptoms
   - Identify root cause
   - Estimate complexity of fix

2. **Determine if blocker:**
   - Does failure block skill usage entirely?
   - Or just plugin auto-discovery (skills still usable manually)?

3. **Create fix spec (if needed):**
   - Follow same spec pattern
   - Include investigation findings
   - Propose solutions

---

## 8. Related Documentation

- Bug #1 Fix: [bug-fix-claude-config-in-sandbox.md](./bug-fix-claude-config-in-sandbox.md)
- Bug #2 Implementation: [bug-fix-missing-deepwiki-skills.md](./bug-fix-missing-deepwiki-skills.md)
- Plugin manifest: `harness-tooling/.agents/plugins/harness-deepwiki-skill/.claude-plugin/plugin.json`
- Claude Code CLI docs: Check Claude Code documentation for plugin commands

---

## 9. Notes

**Why This Matters:**
- Validates Bug #1 fix works for real-world use case (Claude Code authentication)
- Confirms Bug #2 integration is complete and functional
- Unblocks plugin-based skill discovery (vs manual skill file management)
- Demonstrates end-to-end workflow: fix credentials → install plugins → use skills

**Low Risk:**
- No code changes required (pure validation)
- Worst case: Validation fails, we document issue and create follow-up spec
- Skills are still usable via direct file references even if plugin system fails
