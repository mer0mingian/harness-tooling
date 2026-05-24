# Bug Fix Spec: Litho Container CA Certificate Configuration

**Status:** Ready for implementation
**Date:** 2026-05-15
**Scope:** Enable litho container to make HTTPS requests through corporate proxy
**Story Points:** 1-5 (depends on solution chosen)
**Parent Issue:** Bug fix validation - deepwiki skills E2E testing

---

## 1. Bug Description

The litho container cannot make HTTPS requests to LLM APIs (Anthropic/OpenAI) due to CA certificate configuration issues in the Rust reqwest library.

### Symptoms

```
Error: reqwest::Error { 
  kind: Builder, 
  source: General("No CA certificates were loaded from the system") 
}
```

**Trigger:**
```bash
docker exec harness-litho-sta2e-agent-workspace litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs
```

**Expected behavior:** Litho generates documentation by calling LLM APIs via corporate proxy

**Actual behavior:** Litho fails immediately with CA certificate error, no API calls attempted

### Impact

- **Blocks:** End-to-end validation of litho skill integration (Step 7)
- **Workaround:** None - litho requires LLM API access to function
- **Severity:** High - litho skill is non-functional without this fix

---

## 2. Root Cause Analysis

### Investigation Findings

**Corporate CA Certificate Is Present:**
```bash
$ docker exec harness-litho-sta2e-agent-workspace ls -la /usr/local/share/ca-certificates/
-rw-r--r-- 1 root root 1968 Apr 20 08:50 corporate-ca.crt
```

**System CA Store Updated:**
```bash
$ docker exec harness-litho-sta2e-agent-workspace ls /etc/ssl/certs/ | wc -l
130  # Standard system CAs present
```

**Litho Uses Rust reqwest Library:**
- Rust's `reqwest` with `native-tls` feature uses system's OpenSSL
- OpenSSL searches specific paths for CA certificates
- Corporate CA is in `/usr/local/share/ca-certificates/` (non-standard location)
- OpenSSL default search paths don't include this directory

### Why Standard CA Installation Fails

**Standard Debian CA Update Process:**
```dockerfile
# This was done during image build (from litho Dockerfile)
COPY corporate-ca.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
```

**However:**
- `update-ca-certificates` creates symlinks in `/etc/ssl/certs/`
- Rust reqwest + native-tls on Debian looks for certs in:
  1. `SSL_CERT_FILE` environment variable (single file)
  2. `SSL_CERT_DIR` environment variable (directory)
  3. `/etc/ssl/certs/ca-certificates.crt` (bundle file)
  4. OpenSSL's compiled-in default paths

**The Problem:**
- Corporate CA certificate not being picked up by path 3 or 4
- No environment variables set (paths 1, 2)
- Litho binary doesn't know where to find the certificate

### Why This Affects Litho but Not Other Services

- **Agent container:** Python `requests` library uses `certifi` package (different CA search logic)
- **CGC container:** May not make external HTTPS calls, or uses different HTTP client
- **Litho container:** Rust + reqwest + native-tls = strict OpenSSL path requirements

---

## 3. Affected Components

### Files to Investigate

1. **`harness-sandbox/docker-compose.yml`** (litho service)
   - Environment variables for CA certificate paths
   - Volume mounts for certificate injection

2. **Litho container image** (harness-litho:stony)
   - Dockerfile for CA installation steps
   - Entrypoint script for runtime CA configuration
   - OpenSSL configuration

3. **`harness-sandbox/.env` / `.env.example`**
   - Corporate CA path configuration
   - SSL environment variables

### Runtime Dependencies

- OpenSSL library in litho container
- CA certificate bundle at `/etc/ssl/certs/ca-certificates.crt`
- Corporate CA certificate at `/usr/local/share/ca-certificates/corporate-ca.crt`

---

## 4. Proposed Solutions

### Solution A: Environment Variables (Recommended) ⭐

**Add SSL certificate paths to litho service environment.**

**File:** `harness-sandbox/docker-compose.yml` (litho service)

**Current state (around line 388-410):**
```yaml
  litho:
    image: ${LITHO_IMAGE:-harness-litho:stony}
    container_name: harness-litho-${PROJECT_NAME:-default}
    working_dir: /tmp
    
    environment:
      - CLOUDFLARE_API_TOKEN
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
```

**Proposed change:**
```yaml
  litho:
    image: ${LITHO_IMAGE:-harness-litho:stony}
    container_name: harness-litho-${PROJECT_NAME:-default}
    working_dir: /tmp
    
    environment:
      - CLOUDFLARE_API_TOKEN
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
      # SSL certificate configuration for corporate proxy
      - SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
      - SSL_CERT_DIR=/etc/ssl/certs
      - REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

**Rationale:**
- `SSL_CERT_FILE`: Points to system CA bundle (includes corporate CA after update-ca-certificates)
- `SSL_CERT_DIR`: Points to directory with individual CA certs
- `REQUESTS_CA_BUNDLE`: For Python-based tools that might run in container
- No image rebuild required (immediate effect)
- Environment-based configuration (12-factor app principle)

**Risk:** Low - only adds environment variables, doesn't modify files

**Story Points:** 1

---

### Solution B: Regenerate CA Bundle in Entrypoint

**Run `update-ca-certificates` at container startup to ensure bundle is current.**

**File:** `harness-sandbox/litho-entrypoint.sh` (create new) or modify existing entrypoint

**Current state:** Litho container may use default Dockerfile CMD with no entrypoint script

**Proposed change:**

Create `harness-sandbox/litho-entrypoint.sh`:
```bash
#!/bin/bash
set -e

# Regenerate CA certificate bundle to include corporate CA
# This ensures /etc/ssl/certs/ca-certificates.crt includes our custom CA
echo "Updating CA certificates..."
update-ca-certificates --fresh 2>/dev/null || update-ca-certificates

# Set SSL environment variables explicitly
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
export SSL_CERT_DIR=/etc/ssl/certs

echo "CA certificates configured:"
ls -la /etc/ssl/certs/ca-certificates.crt
grep -c "BEGIN CERTIFICATE" /etc/ssl/certs/ca-certificates.crt || echo "0 certificates"

# Execute the original command (litho)
exec "$@"
```

Update `docker-compose.yml` litho service:
```yaml
  litho:
    image: ${LITHO_IMAGE:-harness-litho:stony}
    container_name: harness-litho-${PROJECT_NAME:-default}
    
    volumes:
      - ./litho-entrypoint.sh:/usr/local/bin/litho-entrypoint.sh:ro
    
    entrypoint: ["/usr/local/bin/litho-entrypoint.sh"]
    command: ["litho"]  # Original command
```

**Rationale:**
- Ensures CA bundle is regenerated at runtime (not just build time)
- Explicitly sets environment variables in entrypoint
- Provides diagnostic output for debugging
- More robust than relying on build-time CA configuration

**Risk:** Medium - requires entrypoint script, might interfere with existing startup

**Story Points:** 2

---

### Solution C: Verify and Fix CA Bundle in Dockerfile

**Rebuild litho image with explicit CA bundle verification.**

**File:** Litho Dockerfile (location TBD - may be in deepwiki-rs or harness-sandbox)

**Investigation needed:**
```bash
# Find litho Dockerfile
find ~/repositories/harness-workplace -name "Dockerfile*" -exec grep -l "litho" {} \;

# Check if litho image is built locally or pulled
docker image inspect harness-litho:stony | jq '.[0].Config.Labels'
```

**Proposed change (if Dockerfile accessible):**

Add after `update-ca-certificates` step:
```dockerfile
# Install corporate CA certificate
COPY corporate-ca.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

# Verify corporate CA was added to bundle
RUN grep -q "BEGIN CERTIFICATE" /usr/local/share/ca-certificates/corporate-ca.crt || \
    (echo "ERROR: Corporate CA certificate is empty or malformed" && exit 1)

RUN grep -l "$(grep -A20 'BEGIN CERTIFICATE' /usr/local/share/ca-certificates/corporate-ca.crt | head -5)" \
    /etc/ssl/certs/ca-certificates.crt || \
    (echo "ERROR: Corporate CA not found in system bundle" && exit 1)

# Set default SSL paths for Rust reqwest
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_DIR=/etc/ssl/certs
```

**Rationale:**
- Build-time verification ensures CA is properly installed
- Environment variables baked into image (no compose file dependency)
- Most robust solution (won't break if compose config forgotten)

**Risk:** High - requires image rebuild, must locate and modify Dockerfile

**Story Points:** 5 (investigation + Dockerfile changes + rebuild + test)

---

### Solution D: Use rustls Instead of native-tls

**Recompile litho with rustls feature instead of native-tls.**

**Background:**
- Rust reqwest supports two TLS backends:
  1. `native-tls` (uses system OpenSSL - current, having issues)
  2. `rustls` (pure Rust TLS, includes Mozilla CA bundle)

**File:** Litho source (deepwiki-rs repository)

**Proposed change in `Cargo.toml`:**
```toml
[dependencies]
# Change from:
reqwest = { version = "0.11", features = ["json", "native-tls"] }

# To:
reqwest = { version = "0.11", features = ["json", "rustls-tls"], default-features = false }
```

Then add corporate CA to rustls cert store programmatically in litho source code.

**Rationale:**
- Eliminates dependency on system OpenSSL configuration
- Includes Mozilla CA bundle by default
- Can programmatically add custom CAs via rustls API

**Risk:** Very High - requires source code changes, full rebuild, testing

**Story Points:** 8+ (source modification + testing TLS changes + validation)

**Recommendation:** Only if Solutions A/B/C all fail

---

## 5. Decision Matrix

| Criterion | Solution A (Env Vars) | Solution B (Entrypoint) | Solution C (Dockerfile) | Solution D (rustls) |
|-----------|----------------------|------------------------|------------------------|---------------------|
| **Implementation Time** | 10 min | 30-60 min | 2-4 hours | 1-2 days |
| **Requires Rebuild** | No | No | Yes (image) | Yes (source + image) |
| **Risk Level** | Low | Medium | High | Very High |
| **Robustness** | Medium | High | Very High | Very High |
| **Reversibility** | Immediate | Easy | Medium | Hard |
| **Story Points** | 1 | 2 | 5 | 8+ |
| **Debugging Ease** | Easy | Easy | Medium | Hard |
| **12-Factor Compliant** | Yes | Partial | No | N/A |

**Recommendation Order:**
1. Try Solution A first (quickest, lowest risk)
2. If A fails, try Solution B (more robust, still no rebuild)
3. If B fails, investigate Solution C (requires Dockerfile access)
4. Avoid Solution D unless all others fail (massive complexity)

---

## 6. Implementation Plan (Solution A - Recommended)

### Step 1: Add Environment Variables

**File:** `harness-sandbox/docker-compose.yml`

**Location:** Litho service environment section (around line 395-400)

**Add these lines:**
```yaml
      # SSL certificate configuration for corporate proxy
      - SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
      - SSL_CERT_DIR=/etc/ssl/certs
      - REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

### Step 2: Verify Configuration

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Check environment section exists
rtk grep -A10 "litho:" docker-compose.yml | rtk grep -A5 "environment:"

# Validate YAML syntax
rtk docker compose config --services | rtk grep litho
```

### Step 3: Restart Litho Container

```bash
cd ~/repositories/sta2e-agent-workspace

# Stop and remove existing container
~/repositories/harness-workplace/harness-sandbox/bin/harness down

# Start with litho profile
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho
```

### Step 4: Verify Environment Variables Set

```bash
rtk docker exec harness-litho-sta2e-agent-workspace env | rtk grep SSL
# Expected output:
# SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# SSL_CERT_DIR=/etc/ssl/certs
# REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

### Step 5: Test HTTPS Connection

```bash
# Test with curl (should work - uses same OpenSSL)
rtk docker exec harness-litho-sta2e-agent-workspace curl -v https://api.anthropic.com 2>&1 | rtk grep -E "SSL|certificate"

# Expected: Successful SSL handshake, no certificate errors
```

### Step 6: Test Litho E2E (Quick Test)

```bash
rtk docker exec harness-litho-sta2e-agent-workspace litho \
  -p /workspace/project \
  -o /workspace/project/litho.test \
  --skip-research
  
# Expected: No CA certificate errors
# Acceptable: API key errors (if keys not configured), but NOT SSL errors
```

### Step 7: Full E2E Test (If API Keys Available)

```bash
# Full documentation generation
rtk docker exec harness-litho-sta2e-agent-workspace litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs

# Expected: Documentation generated successfully
# Check output
test -d ~/repositories/sta2e-agent-workspace/litho.docs && \
  echo "✅ SUCCESS: Documentation generated" || \
  echo "❌ FAILED: No output directory"
```

---

## 7. Validation Steps

All checks must pass post-implementation. Use rtk for all commands.

### Validation 1: Environment Variables Present

```bash
rtk docker exec harness-litho-sta2e-agent-workspace bash -c 'echo $SSL_CERT_FILE'
# Expected: /etc/ssl/certs/ca-certificates.crt
```

**Success Criteria:** SSL_CERT_FILE environment variable set

### Validation 2: CA Bundle Exists and Readable

```bash
rtk docker exec harness-litho-sta2e-agent-workspace test -f /etc/ssl/certs/ca-certificates.crt && echo "EXISTS" || echo "MISSING"
# Expected: EXISTS

rtk docker exec harness-litho-sta2e-agent-workspace wc -l /etc/ssl/certs/ca-certificates.crt
# Expected: Several thousand lines (multiple certificates)
```

**Success Criteria:** CA bundle file exists and contains certificates

### Validation 3: Corporate CA in Bundle

```bash
rtk docker exec harness-litho-sta2e-agent-workspace grep -c "BEGIN CERTIFICATE" /etc/ssl/certs/ca-certificates.crt
# Expected: 100+ (system CAs) including corporate CA
```

**Success Criteria:** Multiple certificates in bundle

### Validation 4: Litho No Longer Errors on CA Certificates

```bash
rtk docker exec harness-litho-sta2e-agent-workspace litho --help 2>&1 | rtk grep -i "certificate"
# Expected: No output (no certificate errors)
```

**Success Criteria:** No CA certificate errors in litho output

### Validation 5: HTTPS Connectivity (curl test)

```bash
rtk docker exec harness-litho-sta2e-agent-workspace curl -I https://api.anthropic.com 2>&1 | rtk head -5
# Expected: HTTP response (401 unauthorized OK), not SSL error
```

**Success Criteria:** HTTPS connection succeeds (even if auth fails)

### Validation 6: Litho API Call (if keys available)

```bash
# Only if ANTHROPIC_API_KEY is set
rtk docker exec harness-litho-sta2e-agent-workspace bash -c '
  if [ -n "$ANTHROPIC_API_KEY" ]; then
    litho -p /workspace/project -o /workspace/project/litho.test --skip-research
  else
    echo "SKIP: No API key configured"
  fi
'
# Expected: Either documentation output or "SKIP" message
# NOT EXPECTED: CA certificate error
```

**Success Criteria:** No CA certificate errors (API errors acceptable if no keys)

---

## 8. Acceptance Criteria

- [ ] SSL_CERT_FILE environment variable set in litho container
- [ ] SSL_CERT_DIR environment variable set in litho container
- [ ] CA bundle file exists: `/etc/ssl/certs/ca-certificates.crt`
- [ ] Corporate CA present in bundle (100+ certificates)
- [ ] Litho --help runs without certificate errors
- [ ] HTTPS curl succeeds (HTTP-level errors OK, SSL errors NOT OK)
- [ ] Litho E2E test completes without CA errors
- [ ] (Optional) Full documentation generation succeeds with valid API keys

---

## 9. Rollback Plan

If Solution A causes issues:

```bash
cd ~/repositories/harness-workplace/harness-sandbox

# Revert docker-compose.yml
rtk git diff docker-compose.yml
rtk git checkout docker-compose.yml

# Restart without changes
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness down
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile litho
```

**Rollback time:** < 2 minutes

---

## 10. Implementation Prompt (For Subagent)

**Mission:** Fix CA certificate configuration in litho container to enable HTTPS API calls.

**Context:**
- Litho fails with "No CA certificates were loaded from the system"
- Corporate CA cert exists: `/usr/local/share/ca-certificates/corporate-ca.crt`
- Rust reqwest library cannot find system CA certificates
- Blocks E2E validation of litho skill integration

**Your Task:**
1. Implement Solution A (environment variables) in docker-compose.yml
2. Restart litho container with new configuration
3. Run validation steps 1-6 (see Validation Steps section above)
4. Test litho execution (with and without API keys)
5. Use verification-before-completion skill before claiming success

**Solution A Implementation:**

Add to `harness-sandbox/docker-compose.yml` litho service environment section:
```yaml
      # SSL certificate configuration for corporate proxy
      - SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
      - SSL_CERT_DIR=/etc/ssl/certs
      - REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

**Working Directory:** `/home/minged01/repositories/harness-workplace/`

**Files to Modify:**
- `harness-sandbox/docker-compose.yml` (litho service environment)

**Validation Commands:**

```bash
# Verify env vars
rtk docker exec harness-litho-sta2e-agent-workspace bash -c 'echo $SSL_CERT_FILE'

# Verify CA bundle
rtk docker exec harness-litho-sta2e-agent-workspace test -f /etc/ssl/certs/ca-certificates.crt && echo "EXISTS"

# Test HTTPS
rtk docker exec harness-litho-sta2e-agent-workspace curl -I https://api.anthropic.com 2>&1 | rtk head -5

# Test litho
rtk docker exec harness-litho-sta2e-agent-workspace litho --help 2>&1 | rtk grep -i "certificate"
```

**Success Criteria:**
- All 6 validation steps pass
- No CA certificate errors in litho output
- HTTPS connectivity works (even if API auth fails)

**If Solution A Fails:**
- Document failure symptoms
- Try Solution B (entrypoint script) from spec
- Report which solution worked

**Deliverable:**
Report with:
1. Changes made (docker-compose.yml diff)
2. Validation results (all 6 steps with outputs)
3. Final status: PASS (CA cert fixed) or FAIL (still broken)
4. If FAIL: Symptoms and recommendation for next solution to try

**Estimated Effort:** 1 story point (~30-60 minutes including validation)

**Tools:**
- Use `rtk` prefix for all commands
- Use `verification-before-completion` skill before final report
- Document actual outputs, not assumptions

---

## 11. Fallback Solutions

### If Solution A Fails

**Try Solution B (Entrypoint Script):**
1. Create `harness-sandbox/litho-entrypoint.sh` (see Solution B section)
2. Add volume mount and entrypoint to docker-compose.yml
3. Restart container
4. Re-run validation

**Story Points:** +1 (total 2)

### If Solution B Fails

**Investigate Solution C (Dockerfile):**
1. Locate litho Dockerfile source
2. Verify corporate CA installation steps
3. Add explicit CA bundle verification
4. Rebuild image
5. Test with new image

**Story Points:** +3 (total 5)

---

## 12. Related Documentation

- Bug #2 Implementation: [bug-fix-missing-deepwiki-skills.md](./bug-fix-missing-deepwiki-skills.md)
- Litho container service: `harness-sandbox/docker-compose.yml` (line 388+)
- Corporate CA cert: `/usr/local/share/ca-certificates/corporate-ca.crt`
- OpenSSL CA paths: https://www.openssl.org/docs/man1.1.1/man1/openssl-env.html
- Rust reqwest native-tls: https://docs.rs/reqwest/latest/reqwest/#tls

---

## 13. Notes

**Why Environment Variables:**
- Standard approach for SSL configuration (SSL_CERT_FILE, SSL_CERT_DIR)
- Used by OpenSSL, curl, Python requests, and many other tools
- 12-factor app compliant (config via environment)
- No image rebuild required (fast iteration)
- Easy to debug (inspect env vars, test in isolation)

**Why This Matters:**
- Litho is non-functional without HTTPS access to LLM APIs
- Skills integration (Bug #2) cannot be fully validated
- Corporate proxy setup is common in enterprise environments
- Fix applies to any service needing HTTPS through corporate proxy
