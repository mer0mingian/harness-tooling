# Target State - Sandbox Restructure
**Date**: 2026-06-05
**Status**: IN PROGRESS

> **IMPORTANT:** Compare [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for the implemented design.
---

## Overview

The original plan was to split the legacy `harness-sandbox` into two separate repos:
- **harness-sandbox-base** (GitHub, OSS-safe) — private development sandbox
- **harness-sandbox-stony** (Stash mirror, GitHub primary) — corporate overlay with Cloudflare CA, managed settings, AWS CLI, with `harness-sandbox-base` as a nested submodule

**What was actually built:** A single unified `harness-sandbox-stony` repository with profile-based image selection (`private` / `stony`). External dependencies (harness-tooling, cloudflare-cert-installer, claude-budget-setup, CodeGraphContext) are direct submodules. This eliminated the submodule nesting complexity and simplified builds.

Both profiles support:
- Multiple parallel sandboxes (one per project, isolated by `PROJECT_NAME`)
- VS Code dev-container configuration
- MATD extension for Claude Code (OpenCode deferred to v1.1)
- Harness binary as the primary host-side interface

---

## 1. Repository Structure

### 1.1 Planned Structure *(Not built — see implementation note above)*

The original plan placed `harness-sandbox-base` and `harness-sandbox-stony` as siblings inside a non-git parent workspace (`harness-workplace/`), with stony referencing base as a nested submodule. This was superseded by the single-repo approach.

### 1.2 Actual Structure

```
harness-sandbox-stony/              ← THIS REPO (canonical, single git repo)
├── docker/
│   ├── Dockerfile.private          # OSS base image (1.94 GB)
│   └── Dockerfile.stony            # Corporate image (1.6 GB)
├── docker-compose.yml              # Profile-aware service definitions
├── bin/harness                     # Host-side CLI (profile detection, init, up/down)
├── scripts/                        # Build scripts, entrypoints, CA cert installer
├── workspace-template/             # Scaffold copied by `harness init`
└── submodules/
    ├── harness-tooling/            # Skills, agents, commands (marketplace)
    ├── CodeGraphContext/           # CGC Docker service source
    ├── cloudflare-cert-installer/  # CA certificate + install script (stony only)
    └── claude-budget-setup/        # Cost-saving layer (stony only)
```

### 1.3 Git Remote Strategy

- **harness-sandbox-stony**: Stash primary (`ssh://git@stash.stepstone.com:7999/zd/harness-sandbox-stony.git`)
- **harness-tooling**: Stash (`ssh://git@stash.stepstone.com:7999/~minged01/harness-tooling.git`)
- **Corporate submodules** (`cloudflare-cert-installer`, `claude-budget-setup`): Stash only
- **CodeGraphContext**: GitHub (`ssh://git@github.com:mer0mingian/CodeGraphContext.git`)

### 1.4 Workspace Template

**Location**: `workspace-template/` (repo root)

**Purpose**: Template directory copied by `harness init` to create new project workspaces.

**Template contents**:
- `.env.example` → User copies to `.env` (secrets, git-ignored)
- `.harness.yml.example` → User copies to `.harness.yml` (project config)
- `.devcontainer/` → VS Code dev-container configuration
- `litho.toml` → C4 documentation config (per-project, each system has own architecture)
- `AGENT.md`, `CONTEXT.md`, `README.md` → Agent orientation files
- `architecture/`, `specs/`, `plans/`, `tests/`, `components/` → Project folder scaffold

**Why litho.toml lives in the workspace (not the sandbox repo)**: Each project has unique architecture; litho.toml configures which components/layers to document per system.

---

## 2. MATD Dual-CLI Architecture & Harness Binary Design

Full specification moved to [docs/MATD_CLI_ARCHITECTURE.md](./docs/MATD_CLI_ARCHITECTURE.md).

**Summary**: Claude Code and OpenCode use incompatible frontmatter schemas, so CLI-specific `agent.md` files must be generated from a canonical source at build time. The harness binary detects profile via CLI flag → env var → `.harness.yml` → default (`stony`), exports `SANDBOX_REPO`, `WORKSPACE_ROOT`, and related vars for docker compose, and manages `harness init`, `up`, `down`, `shell`, `exec`, `build`.

---

## 3. Docker Compose Configuration

**Note (2026-06-04):** A CLI-per-image naming scheme was decided (`claude`, `opencode`, `agy`, `codex`) to replace the single `stony` profile. See STATUS.md for the updated image architecture.

Three services defined in `docker-compose.yml`:

| Service | Profile | Purpose |
|---------|---------|---------|
| `agent` | (default) | Main sandbox container, bind-mounts project workspace |
| `cgc` | `cgc`, `full` | CodeGraphContext indexing service, built from `${SANDBOX_REPO}/submodules/CodeGraphContext` |
| `litho` | `litho`, `full` | Deepwiki documentation generator |

**Key volume mounts** (agent service):
- `${WORKSPACE_ROOT}:/workspace` — project code (read-write)
- `~/.claude`, `~/.config/opencode`, `~/.gemini` — CLI config persistence
- `${SSH_AUTH_SOCK}:/ssh-agent` — SSH agent forwarding

**Parallel sandbox isolation** via `${PROJECT_NAME}` (read from `.harness.yml`):
- Container: `harness-${PROJECT_NAME}-agent`
- Network: `harness-${PROJECT_NAME}`
- Volumes: `harness-cgc-${PROJECT_NAME}`, `harness-litho-${PROJECT_NAME}`

---

## 4. Configuration Files

### 4.1 .env (Secrets Only, git-ignored)

Key variables: `GIT_USER_NAME`, `GIT_USER_EMAIL`, `GH_TOKEN`, `CGC_PORT` (default 4740), `LITHO_PORT` (default 4741). Corporate adds: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, Bitbucket/Jira/Confluence tokens. See `.env.example` and `.env.private.example` in repo root.

### 4.2 .harness.yml (Non-Secret Config)

`workspace.name` is **required** — used for container naming, volume naming, and network isolation. Falls back to directory name if workspace.name is missing.

Key sections: `workspace` (name, profile, type), `compose.profiles`, `services` (cgc/litho enabled + ports), `marketplaces` (plugin sources), `extensions` (SpecKit extension paths).

See `workspace-template/.harness.yml.example` for full schema.

---

## 5. VS Code Dev-Container

A `.devcontainer/devcontainer.json` is provided in `workspace-template/` and copied to each project workspace by `harness init`. It references `docker-compose.yml` from `${SANDBOX_REPO}` and targets the `agent` service. Extensions pre-installed: Python, Claude Code, OpenCode (stony adds AWS Toolkit).

Corporate dev-container additionally mounts `~/.aws` and uses the stony compose overlay (`docker-compose.stony.yml`).

Dev-container qualification was **not tested** in v1 — see Section 7.

---

## 6. Testing Requirements

### 6.1 Build Tests
- ✅ Build private image (`1.94 GB`)
- ✅ Build stony image (`1.6 GB`, after cert fix)
- ✅ Submodule recursion verified (`git clone --recurse-submodules`)
- ✅ CA cert installation confirmed (stony Stage 1)

### 6.2 CLI Tests
- ✅ Claude Code available and working (`v2.1.162`)
- ✅ SpecKit CLI available (`specify-cli v0.8.15.dev0`)
- ✅ RTK installed and functional
- ✅ claude-budget-setup: 3 skills, 6 hooks, `ANTHROPIC_MODEL` via .env

### 6.3 MATD Tests
- ✅ Extension install verified (specify-cli v0.8.15.dev0, installed in Dockerfile.private Stage 4)
- ✅ Agent generation script runs at build time; generates 6 Claude Code + 6 OpenCode agents

### 6.4 Parallel Sandbox Tests
- ⚠️ Compose isolation architecture implemented; not tested with real simultaneous execution

### 6.5 SSH Tests
- ⚠️ Not tested — SSH agent forwarding wired in compose but not validated end-to-end

### 6.6 Dev-Container Tests
- ⚠️ Not tested — devcontainer.json provided in workspace-template but not qualified

---

## 7. Open Items for V0.3

**Multi-CLI Plugin Support:**
- OpenCode plugin auto-install in private image
- Codex CLI support planning for stony image
- Agent/skill compatibility matrix across CLIs
- Clear documentation for creating cross-CLI agents

**MCP Servers in .harness.yml:**
Restore a full `mcp_servers:` section to `.harness.yml.example` (removed in v0.2 cleanup but needed for configuring CGC, Litho, and company MCP servers). Reference the section from `archive/legacy-harness-sandbox/workspace-template/.harness.yml` (lines 113–296) covering: codegraphcontext, litho, datadog, terraform_registry, slack, kibana, stonehenge, atlassian, aws_api/aws_docs.

**Direction:**
The SpecKit extension will be split into two independent repositories to separate generic spec-driven development workflows from Stepstone-specific integrations. This enables:
- OSS-safe core extension that can be shared publicly
- Corporate-specific extension with Jira/Confluence/internal tooling integration
- Independent release cycles (core can evolve without breaking corporate workflows)
- Clear ownership boundaries (core = dev team, stepstone = ops/integration team)
Compare information in [open to-dos](./docs/backlog/todo-items.md).

---

## 8. Success Criteria

### Implementation Status (2026-05-27)

**Architecture Change**: Implemented as single merged repository (harness-sandbox-stony) with profile-based image selection, not two separate repos as originally specified. This document describes the target architecture; see CHANGE_PLAN.md for actual implementation status.

### 8.1 V1 Complete When:
- [x] ~~Both repos created~~ → **Merged into harness-sandbox-stony/**
  - ✅ Submodule structure preserved
  - ✅ harness-tooling as direct submodule
  - ✅ Corporate submodules (cloudflare-cert-installer, claude-budget-setup)
- [x] Both images build successfully
  - ✅ harness-sandbox:private (1.94GB)
  - ✅ harness-sandbox:stony (2.56GB)
- [ ] MATD works with Claude Code and OpenCode (DEFERRED to v1.1 or v2)
  - ⚠️ Agent generation not implemented end-to-end
  - ⚠️ Template architecture documented but not built
- [x] Parallel sandboxes support verified
  - ✅ docker-compose uses ${PROJECT_NAME} for isolation
  - ⚠️ Not tested with actual multiple running sandboxes
- [x] Corporate CA trust chain working
  - ✅ CA-first architecture implemented (Stage 1)
  - ✅ Real Cloudflare CA cert installed and SSL verified
- [x] Managed Claude Code settings applied
  - ✅ Copied in Dockerfile.stony Stage 4
  - ⚠️ Not runtime-tested
- [ ] Dev-container qualification verified (NOT TESTED)
- [x] Harness binary orchestrates all operations
  - ✅ Profile detection (CLI flag → env → config → default)
  - ✅ Commands: up, down, logs, exec, build, init, config
  - ✅ Pure bash (no yq dependency)
- [x] Documentation complete
  - ✅ README.md with profile examples
  - ✅ docs/ARCHITECTURE.md with ADRs
  - ✅ CLAUDE.md updated to core-repo framing

### 8.2 User Acceptance:
- [x] Developer can clone repo and run `harness up .` → working sandbox
  - ✅ E2E test verified init + both profiles work
- [x] Developer can work on multiple Stepstone systems simultaneously
  - ✅ Compose isolation architecture implemented
  - ⚠️ Not tested with real parallel execution
- [ ] Claude Code and OpenCode both invoke MATD agents (DEFERRED)
- [ ] SSH operations (git push/pull) work with both host and sandbox keys (NOT TESTED)
- [ ] VS Code dev-container opens and connects without errors (NOT TESTED)

### 8.3 V1 Status Summary

**Completed (Core Infrastructure)**:
- ✅ Repository merge and profile-based architecture
- ✅ Both Docker images built and tested
- ✅ Enhanced harness CLI with profile support
- ✅ Profile-aware docker-compose
- ✅ CA-first corporate image pattern
- ✅ Comprehensive documentation
- ✅ E2E testing verification

**Pending (Testing & Integration)**:
- ⚠️ SSH operations testing
- ⚠️ VS Code dev-container qualification
- ⚠️ Real parallel sandbox execution test

**Deferred (v1.1 or v2)**:
- Phase 2: MATD agent generation and dual-CLI support
- Advanced testing scenarios
- Production hardening

---
