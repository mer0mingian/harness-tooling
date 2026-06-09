---
type: spec
feature_id: "006-agent-skill-restriction-experiment"
title: "Agent Skill Restriction Experiment"
status: stub
created: "2026-06-09"
owner: "Daniel Mingers"
branch: dev
---

# Spec (STUB): Agent Skill Restriction Experiment

> **Status: STUB.** Created from FUTURE-WORK grilling session 2026-06-09.

## What & Why

Mini experiment to confirm that `disallowedTools`, MCP scoping, and skill restrictions work as expected for constraining agent capabilities and enforcing separation of concerns.

## Deliverables

1. **Validated restriction configs** — tested `disallowedTools` patterns and MCP scope rules per agent role.
2. **[AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md) update** — must be updated to reflect the validated configurations. The matrix is the authoritative source for agent-skill assignment; results of this experiment flow back into it. Any change to which skills or tools are allowed/disallowed per agent must land in the matrix before the spec is closed.

## References
- [FUTURE-WORK-SPECS-NEEDED.md](../../FUTURE-WORK-SPECS-NEEDED.md)
- [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md) — current state; target of the write-back deliverable
