# Future Work - Remaining Items

**Status:** Active grilling items only  
**Date:** 2026-06-10

For completed grilling sessions and implementation planning, see:
- [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) - Full 177 SP scope, estimates, sequencing (Section 11: Grilling Session Results)
- [TARGET_STATE.md](../../../TARGET_STATE.md) - Architectural decisions (7-agent architecture, plugin splits)
- [STATUS.md](../../../STATUS.md) - Current implementation status for specs 001-011

All completed grilling sessions (Sections 1-2, 4-7) are documented in:
- [context/matd-enhanced-structure.md](context/matd-enhanced-structure.md) - Enhanced workspace structure
- [context/speckit-preset-mechanism.md](context/speckit-preset-mechanism.md) - SpecKit preset system
- [context/agent-restrictions-learnings.md](context/agent-restrictions-learnings.md) - Agent capability restrictions
- [context/stdd-skills-analysis.md](context/stdd-skills-analysis.md) - STDD skills cleanup

---

## 1. New General Skills (Pending Grilling)

**Goal:** Add missing skill types for workflow metadata

### a) determine-change-level
- **Purpose:** Classify changes (patch/minor/major, or custom taxonomy)
- **Use by:** Agents need to assess impact before implementation
- **Triggers:** Before commit, during review, in planning

### b) estimate-complexity
- **Purpose:** Estimate story points, effort, or complexity
- **Use by:** Planning agents, orchestrators
- **Output:** Structured complexity assessment (points, confidence, factors)

### Questions for Grilling:
- What classification systems? (SemVer, impact levels, risk matrix?)
- Integration with existing review skills?
- Output format and structure?
- Should these be in matd-skills or general-* namespace?

---

## 2. Maintenance Commands (Tier 3 - Pending Grilling)

**Goal:** Add workflow automation commands for spec lifecycle management

### Missing Commands:

#### a) archive-spec
- **Purpose:** Move completed spec to specs_archive/ (preserves folder + ID)
- **Automation:** Part of matd workflow completion
- **Integration:** Maintains traceability chain after archival

#### b) update-traceability
- **Purpose:** Maintain product/prd/index.yml (PRD↔SD↔Spec chain)
- **Automation:** Update after spec creation, archival, or relationship changes
- **Format:** YAML index linking PRD IDs → SD IDs → Spec IDs

#### c) generate-dependency-map
- **Purpose:** Auto-generate specs/SPEC-XXXX/dependency-map.md from imports
- **Automation:** Parse code imports, build dependency graph
- **Output:** Mermaid diagram showing component dependencies

### Questions for Grilling:
- Trigger points: Manual commands or automatic hooks?
- Integration with existing matd-commit workflow?
- Error handling for broken traceability chains?
- Dependency detection scope (direct imports only, or transitive)?

---

## Next Steps

### Ready for Grilling:
1. **New General Skills** - determine-change-level, estimate-complexity
2. **Tier 3 Maintenance Commands** - archive-spec, update-traceability, generate-dependency-map

### Grilling Session Template:

```
I want to design [ITEM FROM ABOVE].

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

### Deferred Items (See IMPLEMENTATION_PLAN.md):
- **Tier 2:** generate-plan, generate-tasks improvements (native to SpecKit core)
- **Tier 4:** verify-spec-coverage, validate-traceability (quality commands)
- **Future:** C4 architecture commands (c4-architecture-from-code, c4-architecture-planning)

---

*Note: Do not implement these changes without completing specification and grilling phases.*
