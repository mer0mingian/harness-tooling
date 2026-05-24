# Bug Fix Spec: Claude Code Configuration in Sandbox

**Status:** Ready for investigation
**Date:** 2026-05-15
**Scope:** Container startup, config mounting, plugin initialization, Claude Code updates
**Story Points:** 5

---

## 1. Bug Description

Claude Code CLI within the sandbox container does not have access to the API key and configuration provided by the host at `~/.claude/config.json`. Additionally, plugins installed during the image build are not available when Claude Code starts for the first time in the container.

### Symptoms

1. **API key not found**: Claude Code cannot authenticate API requests because it doesn't see `~/.claude/config.json` from the host
2. **Missing plugins**: Plugins that should be available from marketplace installations are not loaded on first Claude Code invocation
3. **Stale Claude Code version**: The container may ship with an outdated version of Claude Code that doesn't get updated on startup

### Expected Behavior

- Claude Code in sandbox uses API key from host `~/.claude/config.json`
- All installed plugins (including custom marketplaces like `stst-ai-tools-marketplace`) are available immediately
- Claude Code updates to latest version on container startup

### Actual Behavior

- API key not accessible (config file not mounted or path mismatch)
- Plugins require manual installation after container starts
- Claude Code version frozen to whatever was in the Docker image at build time

---

## 2. Root Cause Analysis

**Investigation needed.** Likely causes:

### Hypothesis A: Config Directory Not Mounted

The host `.claude/` directory may not be bind-mounted into the container, or mounted to the wrong path. 

**Check:**
- Does `docker-compose.yml` mount `~/.claude` to `/home/agent/.claude`?
- Is the container user's `HOME` environment variable set correctly?
- Does Claude Code in the container look for config in a different location?

### Hypothesis B: File Permissions/Ownership Mismatch

If `.claude/` is mounted, the container user may lack read permissions.

**Check:**
- What UID/GID does the agent container run as?
- What are the permissions on host `~/.claude/config.json`?
- Does the container need a `user:` directive in compose?

### Hypothesis C: Plugin Path Resolution

Claude Code may be looking for plugins in a different directory than where they're installed during image build.

**Check:**
- Where does `pip install claude-code` place plugins during Dockerfile `RUN`?
- Where does Claude Code at runtime search for plugins?
- Are plugin manifests in the expected format/location?

### Hypothesis D: No Update Mechanism

The Dockerfile installs Claude Code once via `pip install claude-code`, but there's no entrypoint command to run `pip install --upgrade claude-code` on container startup.

**Check:**
- Is there a container entrypoint script?
- Should the update happen in entrypoint or via a startup command?

---

## 3. Affected Components

### Files to Investigate

1. **`harness-sandbox/Dockerfile`**
   - How Claude Code is installed
   - Which user/UID the installation runs as
   - Plugin installation commands

2. **`harness-sandbox/docker-compose.yml`** (agent service)
   - Volume mounts for `.claude/` directory
   - User/UID configuration
   - Environment variables affecting Claude Code paths

3. **`harness-sandbox/bin/harness`** (wrapper)
   - Any pre-flight checks or config preparation
   - Environment variable passing to containers

4. **Host `~/.claude/config.json`**
   - API key format verification
   - Custom marketplace definitions
   - File permissions

### Components to Create

1. **Container entrypoint script** (if not exists)
   - Update Claude Code on startup
   - Validate config access
   - Initialize plugins

---

## 4. Investigation Plan

### Phase 1: Understand Current State

**Step 1.1:** Document Claude Code installation in Dockerfile
```bash
cd ~/repositories/harness-workplace/harness-sandbox
rtk grep -n "claude-code" Dockerfile
rtk grep -n "pip install" Dockerfile
```

**Step 1.2:** Document current volume mounts
```bash
rtk grep -A10 "agent:" docker-compose.yml | rtk grep -E "volumes:|  -"
```

**Step 1.3:** Check container user configuration
```bash
rtk grep -E "user:|USER " docker-compose.yml Dockerfile
```

**Step 1.4:** Test config access in running container
```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc
rtk docker exec harness-agent-sta2e-agent-workspace ls -la /home/agent/.claude/
rtk docker exec harness-agent-sta2e-agent-workspace cat /home/agent/.claude/config.json
```

### Phase 2: Root Cause Identification

**Step 2.1:** Compare host and container paths
```bash
# Host side
ls -la ~/.claude/
cat ~/.claude/config.json | jq .primaryApiKey

# Container side
rtk docker exec harness-agent-sta2e-agent-workspace bash -c 'echo $HOME'
rtk docker exec harness-agent-sta2e-agent-workspace ls -la $HOME/.claude/ || echo "NOT MOUNTED"
```

**Step 2.2:** Check Claude Code plugin directories
```bash
rtk docker exec harness-agent-sta2e-agent-workspace claude --version
rtk docker exec harness-agent-sta2e-agent-workspace pip show claude-code | rtk grep Location
rtk docker exec harness-agent-sta2e-agent-workspace find /home/agent -name "*plugin*" -o -name "*marketplace*" 2>/dev/null
```

**Step 2.3:** Verify API key accessibility
```bash
rtk docker exec harness-agent-sta2e-agent-workspace claude config show 2>&1
# OR if no such command:
rtk docker exec harness-agent-sta2e-agent-workspace python3 -c "import json; print(json.load(open('/home/agent/.claude/config.json'))['primaryApiKey'][:20])"
```

### Phase 3: Design Solution

Based on investigation, design fixes for:

1. **Config access**: Mount strategy (bind mount vs copy, path mapping)
2. **Plugin availability**: Installation timing (build vs startup, marketplace sync)
3. **Update mechanism**: Entrypoint script, update command, version pinning strategy

---

## 5. Proposed Fix (Preliminary)

**Note:** These are hypothetical solutions. Actual implementation depends on Phase 1-2 findings.

### Fix A: Mount Host .claude Directory

Add to `harness-sandbox/docker-compose.yml` agent service:

```yaml
volumes:
  - ${HOME}/.claude:/home/agent/.claude:ro
```

**Rationale:** Direct bind mount allows container to use host API key and config. Read-only prevents container from corrupting host config.

**Risk:** If container user UID differs from host, permissions may block access.

### Fix B: Create Container Entrypoint Script

Create `harness-sandbox/entrypoint.sh`:

```bash
#!/bin/bash
set -e

# Update Claude Code to latest version
echo "Updating Claude Code..."
pip install --upgrade --quiet claude-code

# Verify config access
if [[ ! -f ~/.claude/config.json ]]; then
    echo "WARNING: ~/.claude/config.json not found" >&2
fi

# Re-sync marketplace plugins
if command -v claude &>/dev/null; then
    claude marketplace sync 2>&1 | grep -v "already installed" || true
fi

# Execute CMD
exec "$@"
```

Add to `harness-sandbox/Dockerfile`:

```dockerfile
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
```

Update `docker-compose.yml` agent service:

```yaml
command: bash  # or original CMD from Dockerfile
```

**Rationale:** Ensures Claude Code is current and plugins are initialized before agent work begins.

### Fix C: Handle UID Mismatch

If investigation reveals UID mismatch, add to `docker-compose.yml` agent service:

```yaml
user: "${UID:-1000}:${GID:-1000}"
```

And update `harness-sandbox/bin/harness` wrapper to export UID/GID:

```bash
export UID=$(id -u)
export GID=$(id -g)
```

---

## 6. Validation Steps

Run these checks after implementing fixes. Use rtk for all commands.

### Step 1: Verify ConfigMount

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

rtk docker exec harness-agent-sta2e-agent-workspace cat /home/agent/.claude/config.json
# Expected: JSON with primaryApiKey matching host config
# Expected: customApiKeyResponses present
# Expected: extraKnownMarketplaces includes stst-ai-tools-marketplace
```

### Step 2: Verify Claude Code Version

```bash
# Host version
claude --version

# Container version (should match or be newer)
rtk docker exec harness-agent-sta2e-agent-workspace claude --version
# Expected: Version matches host or is latest from PyPI
```

### Step 3: Verify API Key Access

```bash
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  if grep -q "primaryApiKey" ~/.claude/config.json 2>/dev/null; then
    echo "API key accessible"
  else
    echo "FAIL: API key not found" >&2
    exit 1
  fi
'
# Expected: "API key accessible"
```

### Step 4: Verify Plugin Availability

```bash
rtk docker exec harness-agent-sta2e-agent-workspace claude plugin list 2>&1
# Expected: List includes all plugins from harness-tooling
# Expected: No "not found" or "not installed" errors
# Expected: stst-ai-tools-marketplace plugins visible (if installed)
```

### Step 5: Test Marketplace Access

```bash
rtk docker exec harness-agent-sta2e-agent-workspace bash -c '
  if grep -q "stst-ai-tools-marketplace" ~/.claude/config.json 2>/dev/null; then
    echo "Custom marketplace configured"
  else
    echo "FAIL: Custom marketplace not accessible" >&2
    exit 1
  fi
'
# Expected: "Custom marketplace configured"
```

### Step 6: Verify Update on Restart

```bash
# Check logs for update message
rtk docker logs harness-agent-sta2e-agent-workspace 2>&1 | rtk grep -i "claude-code"
# Expected: "Updating Claude Code..." or similar startup message
# Expected: "Successfully installed" or "already satisfied"
```

---

## 7. Acceptance Criteria

- [ ] Host `~/.claude/config.json` is accessible inside agent container
- [ ] API key from host config is readable by Claude Code in container
- [ ] Container user has correct permissions to read `.claude/` directory
- [ ] Custom marketplace `stst-ai-tools-marketplace` is accessible
- [ ] Claude Code updates to latest version on container startup
- [ ] Update process completes within 30 seconds
- [ ] All marketplace plugins are available immediately after container starts
- [ ] No manual plugin installation required after `harness up`
- [ ] Claude Code version in container matches or exceeds host version
- [ ] All validation steps 1-6 pass
- [ ] Config mount is read-only (prevents container from corrupting host config)
- [ ] Solution works for both cgc and default profiles

---

## 8. Rollback Plan

If the fix causes issues:

1. **Revert Dockerfile changes:**
   ```bash
   cd ~/repositories/harness-workplace/harness-sandbox
   rtk git checkout HEAD Dockerfile
   ```

2. **Revert docker-compose.yml changes:**
   ```bash
   rtk git checkout HEAD docker-compose.yml
   ```

3. **Remove entrypoint script (if created):**
   ```bash
   rtk rm entrypoint.sh
   rtk git checkout HEAD bin/harness
   ```

4. **Rebuild and restart:**
   ```bash
   cd ~/repositories/sta2e-agent-workspace
   ~/repositories/harness-workplace/harness-sandbox/bin/harness down
   ~/repositories/harness-workplace/harness-sandbox/bin/harness build
   ~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc
   ```

---

## 9. Related Documentation

- Claude Code config format: Check Claude Code CLI documentation
- Docker bind mount permissions: https://docs.docker.com/storage/bind-mounts/
- Container user/UID handling: https://docs.docker.com/compose/compose-file/compose-file-v3/#user
- Marketplace specification: harness-tooling plugin manifests

---

## 10. Future Improvements (Out of Scope)

- Version pinning strategy for Claude Code (pin vs always-latest)
- Cache pip packages to speed up startup updates
- Health check to validate config before starting agent services
- Automated test to verify API key access in CI/CD
- Support for multiple API keys / key rotation
- Encrypted config mounting for sensitive marketplaces
