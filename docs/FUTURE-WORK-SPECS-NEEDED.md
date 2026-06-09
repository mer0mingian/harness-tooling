# Future Work - Specs & Grilling Sessions Needed

**Status:** Planning stage - each item needs specification and grilling session before implementation  
**Date:** 2026-06-09

---

## 1. Split Claude Code matd Plugin

**Goal:** Reorganize matd plugin into separate, composable plugins

### Proposed Structure:

#### a) matd-agents-core
- **Contains:** 6 MATD agents + their required skills
- **Agents:** matd-architect, matd-dev, matd-qa, matd-specifier, matd-orchestrator, matd-critical-thinker
- **Skills:** Only skills referenced in agent frontmatter (see AGENT_SKILL_MATRIX.md)
- **Use case:** Users who want MATD agents without commands

#### b) matd-commands
- **Contains:** 8 MATD workflow commands (without SpecKit dependency)
- **Commands:** test, implement, review, commit, update-docs, specify-product-brief, specify-adr, specify-solution-design
- **Use case:** Users who want workflow commands but don't use SpecKit

#### c) matd-skills-extended
- **Contains:** Additional skills relevant for MATD workflows but not directly used by agents
- **Skills:** TBD - needs refinement session to identify
- **Use case:** Optional skill extensions for advanced workflows

### Questions for Grilling:
- How will commands work without SpecKit yml templates?
- What's the dependency chain? (Can commands work without agents?)
- Which skills go in "extended" vs bundled with agents?
- How do users combine these plugins?

---

## 2. Split SpecKit MATD Extension

**Goal:** Break monolithic MATD extension into focused, modular extensions

### Proposed Extensions:

#### a) matd-discovery
- **Commands:** specify-pdr, specify-system-constitution, specify-product-brief
- **Focus:** Product discovery and requirements
- **Standalone:** Yes

#### b) matd-solution-design
- **Commands:** design-solution-proposals, contract-data-producer, contract-data-consumer, contract-openapi, generate-c4-description, challenge-solution-design
- **Focus:** Architecture and design phase
- **Dependencies:** Needs discovery artifacts?

#### c) matd-refinement
- **Commands:** refine-test-cases, challenge-test-cases
- **Focus:** Test planning and review
- **Dependencies:** Needs design artifacts?

#### d) matd-implement-tdd
- **Commands:** test, implement, review, commit, update-docs (non-"specify" commands)
- **Focus:** TDD implementation workflow
- **Dependencies:** Needs refinement artifacts?

#### e) matd-implement-v
- **Commands:** TBD - to be refined later
- **Focus:** V-Model implementation
- **Status:** Future work

### Questions for Grilling:
- What are the artifact dependencies between extensions?
- Can these be used independently or must follow sequence?
- How do templates get shared across extensions?
- What's in each extension.yml manifest?
- Should these be separate repos or subdirectories?
- **Path configuration:** Extension template paths must match workspace-template structure (see harness-sandbox-stony/docs/WORKSPACE_TEMPLATE.md)

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

## 4. Open Questions to Resolve

### matd Commands Without SpecKit Templates
**Question:** How will matd-commands plugin work if users don't have SpecKit yml templates?

**Options:**
1. Bundle minimal templates in plugin
2. Commands dynamically generate artifacts
3. Commands fail gracefully with helpful messages
4. Split commands into "speckit-dependent" and "standalone" variants

**Needs:** Grilling session to evaluate tradeoffs

---

## Next Steps

For each work item above:

1. **Create specification document**
   - Clear scope and boundaries
   - Dependencies and constraints
   - Success criteria

2. **Run grilling session** (`/grill-me` or `/grill-with-docs`)
   - Challenge assumptions
   - Identify edge cases
   - Refine approach

3. **Get user approval**
   - Review spec and grilling results
   - Adjust based on feedback
   - Finalize before implementation

4. **Implementation**
   - Follow approved spec
   - Test each component
   - Update documentation

---

## Grilling Session Prompt Template

Use this template to start a grilling session for any of the above items:

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

---

*Note: Do not implement these changes without completing specification and grilling phases.*
