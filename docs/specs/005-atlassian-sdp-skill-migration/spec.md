---
type: spec
feature_id: "005-atlassian-sdp-skill-migration"
title: "Atlassian/SDP skills → matd plugin migration (FUTURE STUB — validate-first)"
status: stub
created: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
---

# Spec (STUB): Atlassian / SDP skill migration

> **Status: STUB — deferred.** Do not act yet. Captures intent + a mandatory validation gate.

## What & Why
The local corporate skills `stepstone-atlassian-skills` and `stepstone-sdp-planning` currently
mix **mechanism** (now covered by the `atlassian-write` MCP) with **StepStone-specific knowledge**
(field ids, team UUIDs, statuses, conventions). Target (TARGET_STATE §5): migrate into the **matd
plugin, MCP-first**, keeping corporate data in the agent-workspace live config (OSS-safe).

## ⚠️ Validation gate (do FIRST, before any migration)
**Check whether StepStone's internal marketplace already ships Jira/SDP/Atlassian MCP plugins or
skills.** Such plugins may already exist — adopting them beats reinventing.
- Search the StepStone Claude Code / agent marketplace(s) and `stst-ai-tools-marketplace` (referenced
  by the PLAYGROUND Stonehenge config) for: Atlassian/Jira MCP, SDP planning, Stonehenge query, etc.
- If a maintained plugin exists → **adopt/depend on it**; reduce our local skills to a thin
  workspace-config layer (corporate ids only).
- If not → migrate per TARGET_STATE §5 (MCP-first, OSS-safe split).

## Scope (after validation)
- Decide adopt-vs-build per the gate.
- MCP-first restructure; drop Python `.atlassian-venv`/`requests` + DC/`vulcan` patterns.
- Keep StepStone-specific data in workspace live config (FR-055 pattern), not the OSS marketplace.
- Preserve the verified field facts (see [sdp-jira-fields.md](../../references/sdp-jira-fields.md)).

## Open Questions
- OQ-M1: Which StepStone marketplace(s)/registries to check; who owns existing Atlassian/SDP plugins?
- OQ-M2: If adopting, how do existing plugins handle write + custom fields vs. our `atlassian-write` MCP?
- OQ-M3: OSS-safe boundary for any retained generic workflow logic in the matd plugin.

## References
- [harness-tooling/TARGET_STATE.md §5](../../../submodules/harness-tooling/TARGET_STATE.md)
- [docs/references/sdp-jira-fields.md](../../references/sdp-jira-fields.md)
- [docs/references/jira-mcp-sdp-creation.md](../../references/jira-mcp-sdp-creation.md)
- Local skills: `.claude/skills/stepstone-atlassian-skills/`, `.claude/skills/stepstone-sdp-planning/` (gitignored)
