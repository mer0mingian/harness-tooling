---
type: spec
feature_id: "012-stdd-skills-cleanup"
title: "STDD skills cleanup - delete obsolete skills, rename product-spec-formats"
status: implementation-ready
created: "2026-06-10"
owner: "Daniel Mingers"
branch: dev
estimate: 2
---

# Spec: STDD Skills Cleanup

## Problem

After the STDD → MATD migration, several STDD-prefixed skills remain in the marketplace that are now obsolete or misnamed:

- **Obsolete skills (7)**: Functionality replaced by MATD workflows, agent presets, or SpecKit extension
- **Misnamed skill (1)**: `stdd-product-spec-formats` should be framework-agnostic

These skills create confusion, add maintenance burden, and violate the naming conventions established during the MATD migration.

## Solution

**Delete 7 obsolete skills:**
1. `stdd-ask-questions-if-underspecified` - Replaced by agent-specific clarification workflows
2. `stdd-make-constrained-implementation` - Replaced by matd-dev agent preset
3. `stdd-openspec` - Replaced by SpecKit extension specification commands
4. `stdd-pm-linear-integration` - Linear integration moved to separate tooling
5. `stdd-project-summary` - Replaced by context-* skills and project-level documentation
6. `stdd-test-author-constrained` - Replaced by matd-qa agent preset
7. `stdd-test-driven-development` - Replaced by matd-dev agent preset with TDD workflow

**Rename 1 skill:**
- `stdd-product-spec-formats` → `spec-product-requirement-formats`
  - Removes framework-specific prefix
  - Framework-agnostic naming (works in MATD, STDD, custom workflows)
  - Usable by matd-product-manager and other product-focused agents

**Update all references:**
- Plugin manifests (`.agents/plugins/*/plugin.json`)
- Agent instructions (`.agents/agents/*/AGENT.md`)
- Documentation files

## Scope

**In scope:**
- Delete 7 skill directories from `.agents/skills/`
- Rename 1 skill directory
- Update all plugin.json files that declare these skills
- Update all AGENT.md files that reference these skills
- Update documentation referencing these skills

**Out of scope:**
- Creating replacement skills (replacements already exist)
- Migrating skill content (skills are obsolete, not migrated)

## Rationale

See [stdd-skills-analysis.md](../../context/stdd-skills-analysis.md) for detailed reasoning.

**Key lessons:**
- Avoid framework prefixes in skill names (use domain-based: `spec-*`, `arch-*`, `dev-*`)
- Keep workflows in agents, not skills (workflows change, patterns don't)
- Skills provide knowledge/patterns; agents provide workflow orchestration

## Estimate

**2 Story Points** (simple cleanup, well-defined scope)

## References

- Analysis: [stdd-skills-analysis.md](../../context/stdd-skills-analysis.md)
- Agent Skill Matrix: [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md)
- Skills Directory: `.agents/skills/`
