# Future Work - Specs & Grilling Sessions Needed

**Status:** Planning stage - each item needs specification and grilling session before implementation  
**Date:** 2026-06-10

---

## 1. Split Claude Code matd Plugin

**Status:** ✅ Specified - See Spec 007  
**Goal:** Reorganize matd plugin into separate, composable plugins

### Final Structure:

#### a) matd-agents-core
- **Contains:** 7 MATD agents + their required skills
- **Agents:** matd-product-manager, matd-requirements-engineer, matd-architect, matd-qa, matd-critical-thinker, matd-dev, matd-orchestrator
- **Skills:** Only skills referenced in agent frontmatter (see AGENT_SKILL_MATRIX.md)
- **Use case:** Users who want MATD agents without commands

#### b) matd-skills-extended
- **Contains:** Additional skills relevant for MATD workflows but not directly used by agents
- **Skills:** TBD - needs refinement session to identify
- **Use case:** Optional skill extensions for advanced workflows

### Grilling Decisions:
- NO matd-commands plugin - commands live only in SpecKit extensions
- Agent restrictions via disallowedTools, MCP scoping via inline mcpServers
- Skills split defined in AGENT_SKILL_MATRIX.md

---

## 2. Split SpecKit MATD Extension

**Status:** ✅ Specified - See Spec 008  
**Goal:** Break monolithic MATD extension into focused, modular extensions

### Final Structure:

#### a) matd-discovery
- **Commands:** specify-prd (✅ exists), specify-product-brief (✅ exists), specify-constitution (❌ needs implementation - Spec 003)
- **Focus:** Product discovery and requirements
- **Standalone:** Yes
- **Templates:** From shared monorepo templates/ directory

#### b) matd-solution-design
- **Commands:** specify-solution-design, specify-adr
- **Focus:** Architecture and design phase
- **Templates:** From shared monorepo templates/ directory

#### c) matd-refinement
- **Commands:** TBD - may not need separate commands, part of test workflow
- **Focus:** Test planning and review
- **Status:** Deferred pending test workflow design

#### d) matd-implement-tdd
- **Commands:** test, implement, review, commit, update-docs
- **Focus:** TDD implementation workflow
- **Templates:** From shared monorepo templates/ directory

### Grilling Decisions:
- Monorepo structure with shared templates/ directory
- ALL paths configurable via matd-config.yml
- Workspace-template-aligned defaults
- Removed non-existent commands (design-solution-proposals, contract-*, etc.)

---

## 3. Create New General Skills

**Goal:** Add missing skill types for workflow metadata

### Proposed Skills:

#### a) determine-change-level
- **Purpose:** Classify changes (patch/minor/major, or custom taxonomy)
- **Use by:** Agents need to assess impact before implementation
- **Triggers:** Before commit, during review, in planning

#### b) estimate-complexity
- **Purpose:** Estimate story points, effort, or complexity
- **Use by:** Planning agents, orchestrators
- **Output:** Structured complexity assessment (points, confidence, factors)

### Questions for Grilling:
- What classification systems? (SemVer, impact levels, risk matrix?)
- Integration with existing review skills?
- Output format and structure?
- Should these be in matd-skills or general-* namespace?

---

## 4. Enhanced Workspace Structure

**Status:** ✅ Specified - See grilling session context  
**Goal:** Specs as folders with embedded artifacts

### Final Structure:
- **Format:** specs/SPEC-0001/ containing spec.md, plan.md, tasks.md, dependency-map.md
- **Traceability:** PRD→SD→Spec numbering chain
- **Test linking:** @pytest.mark.spec("SPEC-XXXX")
- **Configuration:** matd-config.yml with all paths configurable
- **Reference:** /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/docs/context/matd-enhanced-structure.md

### Workspace Template Updates Needed:
- Add product/prd/ directory
- Add product/context/ directory
- Add .specify/ directory

---

## 5. SpecKit Preset for /specify Override

**Status:** ✅ Specified - See Spec 009  
**Goal:** Allow users to override default /specify command with matd-specify-prd

### Final Design:
- **Mechanism:** SpecKit preset system with priority-based resolution
- **Reference:** /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/docs/context/speckit-preset-mechanism.md
- **User Experience:** Install matd-discovery preset to get /specify → matd-specify-prd

---

## 6. Agent Capability Restrictions Experiment

**Status:** ✅ Specified - See Spec 006  
**Goal:** Validate disallowedTools, MCP scoping, skill restrictions work as documented

### What to Test:
- disallowedTools enforcement
- MCP server scoping via inline mcpServers
- Skill restriction patterns
- **Reference:** /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/docs/context/agent-restrictions-learnings.md

---

## 7. STDD Skills Cleanup

**Status:** ✅ Specified - See grilling session context  
**Goal:** Remove obsolete skills, rename survivor

### Actions:
- **Delete:** stdd-ask-questions-if-underspecified, stdd-make-constrained-implementation, stdd-openspec, stdd-pm-linear-integration, stdd-project-summary, stdd-test-author-constrained, stdd-test-driven-development
- **Rename:** stdd-product-spec-formats → spec-product-requirement-formats
- **Reference:** /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/docs/context/stdd-skills-analysis.md

---

## 8. Command Inventory & Gaps

### Current Commands (10 total)

**Discovery Phase (matd-discovery):**
- ✅ specify-product-brief - Create/update product brief (Spec 002)
- ✅ specify-prd - PM-facing PRD → PRD + SDP Initiative (Spec 001)
- ❌ specify-constitution - System Constitution (Spec 003) - **MISSING, NEEDS IMPLEMENTATION**

**Solution Design Phase (matd-solution-design):**
- ✅ specify-solution-design - Solution Design with C2/C3 architecture (Spec 004)
- ✅ specify-adr - Create Architecture Decision Record

**Refinement Phase (matd-refinement):**
- ✅ test - Generate failing tests (RED state)
- ⏳ generate-plan - (Native to SpecKit /plan - improve later)
- ⏳ generate-tasks - (Native to SpecKit /tasks - improve later)

**Implementation Phase (matd-implement-tdd):**
- ✅ implement - Implement feature code (RED → GREEN)
- ✅ review - Parallel architecture + code review
- ✅ commit - Validate evidence and create git commit
- ✅ update-docs - Update C4 diagrams and Code Graph Context

### Missing Commands

**Tier 1: Must Have (Add Now)**
- ❌ specify-constitution (Spec 003) - Already specified, needs implementation in matd-discovery

**Tier 2: Native to SpecKit Core (Defer - Improve Later)**
- ⏳ generate-plan - Bridge solution design → tasks (use /plan for now)
- ⏳ generate-tasks - Tasks with dependencies + story points (use /tasks for now)

**Tier 3: Maintenance Commands (Add Soon)**
- ❌ archive-spec - Move completed spec to specs_archive/ (preserves folder + ID)
- ❌ update-traceability - Maintain product/prd/index.yml (PRD↔SD↔Spec chain)
- ❌ generate-dependency-map - Auto-generate specs/SPEC-XXXX/dependency-map.md from imports

**Tier 4: Future Quality Commands (Defer)**
- ⏳ verify-spec-coverage - Test coverage reports by spec (uses @pytest.mark.spec markers)
- ⏳ validate-traceability - Verify PRD→SD→Spec chain integrity

### Future: C4 Architecture Commands

For matd-solution-design extension enhancement:
- c4-architecture-from-code - Generate C4 from existing codebase (litho/deepwiki)
- c4-architecture-planning - Generate C4 from planning artifacts pre-implementation

Reference: arch-c4-architecture skill + GitHub c4-architecture references

---

## Next Steps

### Completed Items (Ready for Implementation)
1. Split Claude Code matd Plugin (Spec 007)
2. Split SpecKit MATD Extension (Spec 008)
3. Enhanced Workspace Structure (context doc)
4. SpecKit Preset Mechanism (Spec 009)
5. Agent Restrictions Experiment (Spec 006)
6. STDD Skills Cleanup (context doc)

### Pending Items (Need Grilling)
1. **Create New General Skills** (Section 3)
   - determine-change-level skill
   - estimate-complexity skill
   - Needs: Classification systems, output formats, namespace decisions

2. **Tier 3 Maintenance Commands** (Section 8)
   - archive-spec command
   - update-traceability command
   - generate-dependency-map command
   - Needs: Design for automation, integration with matd workflow

### Grilling Session Results

All major architectural decisions captured in context documents:
- [matd-enhanced-structure.md](context/matd-enhanced-structure.md) - Enhanced workspace structure
- [speckit-preset-mechanism.md](context/speckit-preset-mechanism.md) - SpecKit preset system
- [agent-restrictions-learnings.md](context/agent-restrictions-learnings.md) - Agent capability restrictions
- [stdd-skills-analysis.md](context/stdd-skills-analysis.md) - STDD skills cleanup

---

## Grilling Session Prompt Template

Use this template for remaining items:

```
I want to design [ITEM FROM SECTION 3].

Context:
- Current state: [describe current structure]
- Goal: [what we want to achieve]
- Constraints: [technical, architectural, user experience]

My initial proposal:
[paste relevant section from above]

Please grill me on:
1. Architecture and dependencies
2. User experience and workflows
3. Edge cases and failure modes
4. Integration with existing components
5. Migration path from current structure

Challenge my assumptions and help me refine this design.
```

---

## File Organization Recommendation

This file has grown to cover:
- Completed grilling sessions (Sections 1-2, 4-7)
- Active work items (Section 3, 8)
- Future enhancements (C4 commands, Tier 4 commands)

### Recommended Split:

**A. COMPLETED-GRILLING-SESSIONS.md** (Archive)
- Sections 1-2, 4-7 with ✅ status
- Historical record of architectural decisions
- Link to context docs
- Reference: "See this file for past grilling results"

**B. ACTIVE-WORK-ITEMS.md** (Current Work)
- Section 3: New General Skills (determine-change-level, estimate-complexity)
- Section 8: Tier 1 & Tier 3 commands (specify-constitution, archive-spec, update-traceability, generate-dependency-map)
- Items ready for specification/implementation
- Link to specs 010-011 when created

**C. FUTURE-ENHANCEMENTS.md** (Backlog)
- C4 architecture commands (from-code, planning)
- Tier 2 command improvements (generate-plan, generate-tasks)
- Tier 4 quality commands (verify-spec-coverage, validate-traceability)
- V-Model implementation extension (matd-implement-v)
- Ideas not yet grilled

### Benefits:
- Clear separation: done vs active vs future
- Easier to find current work items
- Historical decisions preserved but not in the way
- Backlog doesn't clutter active work

### Migration Path:
1. Create COMPLETED-GRILLING-SESSIONS.md from sections 1-2, 4-7
2. Create ACTIVE-WORK-ITEMS.md from sections 3, 8 (Tier 1 & 3)
3. Create FUTURE-ENHANCEMENTS.md from Tier 2, 4, C4 commands
4. Keep FUTURE-WORK-SPECS-NEEDED.md as index pointing to all three

---

*Note: Do not implement these changes without completing specification and grilling phases.*
