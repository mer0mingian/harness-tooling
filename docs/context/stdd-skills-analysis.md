# STDD Skills Analysis

## Source
Grilling session 2026-06-09
Skills audit and cleanup from STDD to MATD migration

## Context
During the STDD → MATD migration, several skills were identified as redundant or misnamed. This document records the decisions for historical reference and future skill development.

## Details

### Skills Deleted (7 total)

1. **stdd-orchestrator-guide**
   - Reason: MATD orchestration embedded in extension commands
   - Replaced by: Native SpecKit command orchestration

2. **stdd-specification-workflow**
   - Reason: Workflow now in matd-product-manager agent preset
   - Replaced by: Agent-specific instructions in AGENT_SKILL_MATRIX.md

3. **stdd-solution-design-workflow**
   - Reason: Workflow now in matd-architect agent preset
   - Replaced by: Agent-specific instructions in AGENT_SKILL_MATRIX.md

4. **stdd-implementation-workflow**
   - Reason: Workflow now in matd-dev agent preset
   - Replaced by: Agent-specific instructions in AGENT_SKILL_MATRIX.md

5. **stdd-testing-workflow**
   - Reason: Workflow now in matd-qa agent preset
   - Replaced by: Agent-specific instructions in AGENT_SKILL_MATRIX.md

6. **stdd-critical-review-workflow**
   - Reason: Workflow now in matd-critical-thinker agent preset
   - Replaced by: Agent-specific instructions in AGENT_SKILL_MATRIX.md

7. **stdd-phase-templates**
   - Reason: Templates moved to SpecKit extension templates/
   - Replaced by: SpecKit template system in spec-kit-multi-agent-tdd/templates/

### Skills Renamed (1 total)

**Before:** `stdd-product-spec-formats`
**After:** `spec-product-requirement-formats`

**Reasoning:**
- Remove "stdd" prefix (not STDD-specific, general skill)
- Rename "spec" → "product-requirement" for clarity
- Usable by matd-product-manager and other product-focused agents
- Framework-agnostic naming (works in MATD, STDD, custom workflows)

### Skill Naming Conventions (Lessons Learned)

**Avoid framework prefixes:**
- ❌ `stdd-*`, `matd-*` - Ties skill to specific framework
- ✅ `spec-*`, `arch-*`, `dev-*` - Domain-based naming

**Use role-based grouping:**
- `spec-*` - Specification/requirements skills
- `arch-*` - Architecture/design skills
- `dev-*` - Development/implementation skills
- `review-*` - Review/validation skills

**Keep workflows in agents, not skills:**
- Skills provide knowledge/patterns
- Agents provide workflow orchestration
- Workflows change per project, patterns don't

## References
- Agent Skill Matrix: /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/AGENT_SKILL_MATRIX.md
- Skills Directory: /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/.agents/skills/
- Extension Structure: /home/minged01/repositories/test/harness-sandbox-stony/SPECKIT_EXTENSION_STRUCTURE.md
