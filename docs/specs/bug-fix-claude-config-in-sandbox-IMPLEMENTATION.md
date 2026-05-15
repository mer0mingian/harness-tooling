# Implementation Prompt: Claude Code Configuration in Sandbox

**Task Type:** Bug fix implementation
**Story Points:** 2
**Investigation Reference:** [Investigation Report](./bug-fix-claude-config-in-sandbox-PROMPT.md)

---

## Your Mission

Implement the approved fix for Claude Code configuration access in the sandbox container. The root cause (UID mismatch preventing config file access) has been identified and the solution (user namespace remapping) has been approved.

**What you will do:**
1. Add user namespace remapping to docker-compose.yml
2. Add HOST_UID/HOST_GID to .env.example
3. Validate the fix works with complete testing
4. Use verification-before-completion skill before claiming success

---

## Root Cause Summary (From Investigation)

**Problem:** Container runs as `sandbox` user (UID 998), but host credential files are owned by UID 1000 with mode 600. Container user cannot read them.

**Solution:** Map container user to host user UID/GID so mounted files become readable while preserving security (mode 600).

---

## Implementation Steps

### Step 1: Update docker-compose.yml

**File:** `harness-sandbox/docker-compose.yml`

**Location:** Agent service definition (around line 75-84)

**Current code:**
```yaml
  agent:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: harness-agent-${PROJECT_NAME:-default}
    hostname: harness-agent
```

**Add this line after `hostname:`:**
```yaml
    # Map container user to host user for credential file access
    # The sandbox user (UID 998 in image) needs to match host UID to read
    # bind-mounted credential files with mode 600
    user: "${HOST_UID:-1000}:${HOST_GID:-1000}"
```

**Result:**
```yaml
  agent:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: harness-agent-${PROJECT_NAME:-default}
    hostname: harness-agent
    
    # Map container user to host user for credential file access
    # The sandbox user (UID 998 in image) needs to match host UID to read
    # bind-mounted credential files with mode 600
    user: "${HOST_UID:-1000}:${HOST_GID:-1000}"
```

### Step 2: Update .env.example

**File:** `harness-sandbox/.env.example`

**Location:** Add after line 51 (after PROJECT_NAME section)

**Add this section:**
```bash

# Host User Mapping
# ==================
# The container's 'sandbox' user must match your host UID/GID to read
# bind-mounted credential files (~/.claude/config.json) with mode 600.
#
# Run `id` on your host to confirm these values.
# Typically 1000:1000 for the first non-root user.
#
# If you get "Permission denied" when Claude Code tries to read config.json,
# check that HOST_UID and HOST_GID match your host user's `id -u` and `id -g`.
HOST_UID=1000
HOST_GID=1000
```

### Step 3: Verify Changes Are Correct

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Check docker-compose.yml has user directive
rtk grep -A2 "hostname: harness-agent" docker-compose.yml | rtk grep "user:"
# Expected: user: "${HOST_UID:-1000}:${HOST_GID:-1000}"

# Check .env.example has HOST_UID/HOST_GID
rtk grep "HOST_UID" .env.example
rtk grep "HOST_GID" .env.example
# Expected: Both variables present with defaults
```

---

## Validation Plan (REQUIRED - Use verification-before-completion)

**You MUST run ALL validation steps and confirm success before claiming the fix works.**

### Pre-Validation: Clean Slate

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness down
~/repositories/harness-workplace/harness-sandbox/bin/harness build
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc
```

### Validation Step 1: Container User ID

```bash
rtk docker exec harness-agent-sta2e-agent-workspace id
# Expected: uid=1000(...) gid=1000(...)
# NOT: uid=998(sandbox)
```

**Success criteria:** UID is 1000 (matches host), not 998

### Validation Step 2: Config File Readability

```bash
rtk docker exec harness-agent-sta2e-agent-workspace cat /home/sandbox/.claude/config.json | rtk head -5
# Expected: JSON output starting with {"primaryApiKey": "sk-ant-...
# NOT: Permission denied
```

**Success criteria:** File content is readable, no permission errors

### Validation Step 3: File Ownership Check

```bash
rtk docker exec harness-agent-sta2e-agent-workspace ls -la /home/sandbox/.claude/ | rtk grep "config.json"
# Expected: -rw------- 1 <user-mapped-to-1000> <group-mapped-to-1000> ... config.json
# Check that ownership appears compatible (not ubuntu:ubuntu if user is remapped)
```

**Success criteria:** Container can see the file with accessible ownership

### Validation Step 4: Claude Code Authentication

```bash
# Try to use Claude Code with API (requires valid API key in config)
rtk docker exec harness-agent-sta2e-agent-workspace bash -c 'echo "test" | claude prompt "say hello" 2>&1 | head -10'
# Expected: Claude response (not authentication error)
# Acceptable: API error if key is invalid, but NOT "config not found" or "permission denied"
```

**Success criteria:** Claude Code can read config (even if API call fails due to network/key issues)

### Validation Step 5: Workspace File Ownership

```bash
rtk docker exec harness-agent-sta2e-agent-workspace touch /workspace/validation-test.txt
rtk docker exec harness-agent-sta2e-agent-workspace ls -l /workspace/validation-test.txt
# Expected: File owned by UID 1000 (should match host user)

# Verify on host side
ls -l ~/repositories/harness-workplace/sta2e-agent-workspace/validation-test.txt
# Expected: Owned by your host user (minged01 or UID 1000)

# Cleanup
rm ~/repositories/harness-workplace/sta2e-agent-workspace/validation-test.txt
```

**Success criteria:** Files created by container are owned by host user (not root, not sandbox)

### Validation Step 6: CGC Service (If Used)

```bash
# Verify CGC service still works with user remapping
rtk docker exec harness-agent-sta2e-agent-workspace cgc --version 2>&1
# Expected: Version output or help text (not permission errors)
```

**Success criteria:** CGC binary is still executable

---

## Success Criteria (All Must Pass)

Before claiming success, verify:

- [x] docker-compose.yml has `user:` directive with correct variables
- [x] .env.example has HOST_UID and HOST_GID with documentation
- [x] Validation Step 1 passes: Container runs as UID 1000
- [x] Validation Step 2 passes: Config file is readable
- [x] Validation Step 3 passes: File ownership is compatible
- [x] Validation Step 4 passes: Claude Code can access config
- [x] Validation Step 5 passes: Workspace files have correct ownership
- [x] Validation Step 6 passes: Other services (CGC) still work

---

## Error Handling

### If Validation Fails

**Do NOT proceed to next step if any validation fails. Instead:**

1. **Document the failure:**
   - Which validation step failed?
   - What was the actual output vs expected?
   - Any error messages?

2. **Investigate root cause:**
   - Check docker-compose.yml syntax
   - Verify environment variables are set
   - Check container logs: `rtk docker logs harness-agent-sta2e-agent-workspace`

3. **Report the issue:**
   - Provide failure details
   - Suggest potential fixes
   - Ask for guidance

### Common Issues and Fixes

**Issue 1: Container fails to start**
- Symptom: `docker compose up` fails with user-related error
- Check: Is `${HOST_UID}` set correctly? Run `echo $HOST_UID` on host
- Fix: Ensure .env has `HOST_UID=1000` or set in environment

**Issue 2: Files still show Permission Denied**
- Symptom: Step 2 fails, can't read config.json
- Check: What UID is container running as? (Step 1 output)
- Fix: Verify user directive is applied; check compose file syntax

**Issue 3: Workspace files owned by wrong user**
- Symptom: Step 5 shows root or wrong UID ownership
- Check: Is user directive on correct service (agent, not others)?
- Fix: Ensure `user:` is under `agent:` service, not global

---

## Tools & Constraints

**You MUST:**
- Use `rtk` prefix for all bash commands
- Use `verification-before-completion` skill before claiming success
- Run ALL validation steps and document results
- Report actual output vs expected for each validation

**Work from:**
- Repository: `/home/minged01/repositories/harness-workplace/harness-sandbox/`
- Test project: `~/repositories/sta2e-agent-workspace`

**Files to modify:**
- `harness-sandbox/docker-compose.yml` (agent service)
- `harness-sandbox/.env.example` (add HOST_UID/HOST_GID)

**Do NOT:**
- Modify Dockerfile (not needed for this fix)
- Change file permissions on host (defeats security purpose)
- Skip validation steps
- Claim success without running all validations

---

## Deliverable

Report back with:

1. **Changes made:**
   - Exact lines added to docker-compose.yml
   - Content added to .env.example

2. **Validation results:**
   - Output from each validation step (1-6)
   - Success/failure for each
   - Any unexpected behavior

3. **Final status:**
   - "All validations passed - fix complete"
   - OR "Validation X failed - issue found: [details]"

---

## Story Points Justification

**2 story points** = ~2-3 hours work:
- 20 minutes: Code changes (2 files, simple additions)
- 10 minutes: Build and restart containers
- 60 minutes: Run complete validation suite (6 steps)
- 30 minutes: Troubleshoot any issues
- 20 minutes: Documentation and reporting

This is a straightforward configuration change with well-defined validation steps.
