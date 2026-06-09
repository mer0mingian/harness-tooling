# STATUS — DESIGN-stage MATD Commands

**Last Updated:** 2026-06-10  
**Branch:** `dev`  
**Session:** Grilling session + 7-agent architecture finalization (2026-06-09..10)

---

## Summary

Eleven **DESIGN-stage SpecKit MATD command specs** designed (specs 001-011), grounded in live Jira/Confluence verification and comprehensive grilling session (2026-06-09/10). **Spec 001 (PRD command) is implementation-ready** with a lean v1 scope (~20-24 SP). Atlassian/SDP MCP integration tested and proven. 7-agent architecture finalized. Enhanced workspace structure designed. All specs committed to core repo `dev` branch.

## Spec Status

| Spec | Command | Status | Key Decisions |
|------|---------|--------|---------------|
| **001** | `speckit-matd-specify-prd` | ✅ **Implementation-ready** (lean v1) | SDP via `atlassian-write` MCP, drop matd-ops/agent-assign, human-push, Team UUID field verified |
| **002** | `speckit-matd-specify-product-brief` (enhance) | 🔄 **Stub** (OQ-B1..5 resolved, B6 open) | Schema-driven gap-fill, Charter-informed template, workspace SoT |
| **003** | `speckit-matd-specify-constitution` | 🔄 **Stub** (full skill design captured) | EA/DigiGov/TechOps sources, team-specific section, compliance checklist |
| **004** | `speckit-matd-specify-solution-design` (alt template) | 🔄 **Stub** (9-section structure captured) | StepStone official EA template, moved from 001 |
| **005** | Atlassian/SDP skill migration | ⏸️ **Deferred** (validation gate) | Check StepStone marketplace first; MCP-first, OSS-safe split |
| **006** | Agent restrictions experiment | 🔄 **Stub** (concept validated via grilling) | Formal decision gates, cascading restrictions, agent-level enforcement |
| **007** | Split Claude Code plugin | 🔄 **Stub** (architecture defined) | Command marketplace (plugins) vs. SpecKit extension (preset/settings) |
| **008** | Split SpecKit extension | 🔄 **Stub** (7-section design) | v-model + workspace + skills + agent-restrictions + budget + MATD |
| **009** | SpecKit preset /specify override | 🔄 **Stub** (implementation path clear) | Multi-template support, preset field, template discovery |
| **010** | `speckit-determine-change-level` skill | 🔄 **Stub** (CLI API defined) | MATD/matd-ops only, single-file Confluence check, no git integration |
| **011** | `speckit-estimate-complexity` skill | 🔄 **Stub** (story-point focus) | Story points (Agile), no hourly estimates, calibrated examples |

## What's Implementation-Ready (Spec 001)

**Lean v1 scope (~20-24 SP):**
- ✅ Thin `prd-schema.yml` (sections + grill prompts)
- ✅ Command (schema-driven grill → render → PRD-NNN/index) — calls scripts directly, no matd-ops agent
- ✅ Advisory validator (structural only) + LLM eval rubric
- ✅ SDP create+transition via `atlassian-write` MCP (tested 2026-06-08 against live Cloud)
- ✅ Local commit + remote-link + SDP-key write-back (human pushes to Stash)
- ✅ Jira config scaffold in marketplace / live per-team config in workspace only (OSS-safe)

**Agents:** `matd-specifier` (smart, .md-only authoring) + `matd-critical-thinker` (smart, read-only review)

**Build order:** schema → command → validator+rubric → SDP MCP script → commit/link (sequential, single builder)

**Critical path:** ~20-24 SP, no external blockers (only a 5-min Team UUID write-format verification at build time)

## Key Achievements This Session

### 1. Grilling Session Completed (Specs 002-011) ✅

Two-day comprehensive grilling session (2026-06-09/10) covering all design-stage specs:
- **Spec 002-004:** Three-input DESIGN model (Product Brief, Constitution, Solution Design) architecture finalized
- **Spec 005:** Atlassian/SDP skill migration validation gate confirmed
- **Spec 006-011:** Six new stub specs created (agent restrictions, plugin/extension split, /specify override, change-level, complexity estimation)
- **Open questions resolved:** 50+ OQ items addressed, 6 remaining (Section 3 + 8 Tier 3 items)
- **Command inventory catalogued:** 72 commands analyzed, gaps identified
- **STDD cleanup plan:** 7 skills for deletion, 1 rename

### 2. 7-Agent Architecture Finalized ✅

**Core Agents (7):**
- `matd-specifier` (smart, .md-only authoring, workflow orchestration)
- `matd-critical-thinker` (smart, read-only review, compliance checks)
- `matd-reviewer` (smart, diff/spec review, traceability validation)
- `matd-test-reviewer` (smart, PR review, test coverage enforcement)
- `matd-ops` (caveman, deterministic plumbing, Jira/git/workspace maintenance)
- `matd-implementer` (smart, code authoring, TDD execution)
- `matd-debugger` (smart, verification-first debugging, error analysis)

**Agent-Skill Matrix:** All agents mapped to skills with restriction levels (required, suggested, forbidden)

**Key decisions:**
- matd-ops remains caveman for deterministic operations (v1 PRD command calls scripts directly)
- Formal decision gates enforce restrictions (not just prompt hints)
- Cascading restrictions: forbidden > suggested > required

### 3. Enhanced Workspace Structure Designed ✅

**Workspace layout refinements:**
- `docs/product/brief.md` (SoT, Product-team owned)
- `docs/architecture/system-constitution.md` (working mirror of EA/Confluence)
- `docs/PRD-NNN/` (numbered PRDs, archived on completion)
- `docs/solution-designs/` (frozen at gate, 1:1 with Epics)
- `docs/specs/SPEC-NNN/` (hierarchical permanent IDs)
- `docs/references/pdlc/` (Constitution source material)

**Key principles:**
- Workspace is SoT for Product Brief (Confluence is markdown view)
- Constitution mirrors EA/Confluence (EA owns tech invariants)
- V-model traceability: PRD-NNN ↔ SDP-key (1:1), PRD → Specs (1:many), Spec ↔ Epic (1:1)

### 4. SDP/Jira MCP Integration — Verified & Tested ✅

- **Path proven:** The `atlassian-write` MCP (sooperset `mcp-atlassian`, write-enabled) works end-to-end against `stepstone.atlassian.net` (Cloud).
- **Tools confirmed:** `jira_create_issue`, `jira_transition_issue`, `jira_update_issue`, `jira_create_remote_issue_link`, `jira_search`, `confluence_create_page`/`update_page`.
- **Auth:** via env token (`JIRA_*`) + cert bundle — handled at MCP layer, not in code.
- **Test:** live read of SDP-7768 (Initiative, status "To Do", `isError:false`) validated auth + field access.
- **Assumption going forward:** the `atlassian-write` MCP is **installed & running in each agent workspace** (a precondition, like Stash auth).

### 5. SDP Initiative Fields — Live-Verified (2026-06-08)

Authoritative createmeta from `stepstone.atlassian.net` captured in [core repo `docs/references/sdp-jira-fields.md`](../../docs/references/sdp-jira-fields.md):

**6 required to create:**
- `summary`, `project=SDP`, `issuetype=11110` (Initiative)
- **Stonehenge Domain** `customfield_11259` (28 options, e.g. Search & Match 12579)
- **Initiative Category** `customfield_11313` (Strategic Capability 17550 / KTLO / Paying Down Debt)
- **Initiative Goal** `customfield_11389` (Delivery 17653 / Enablement / Research)

**Plus Team** `customfield_10001` (value = team **UUID**, e.g. Mamba `f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425` — verified on SDP-6701; not on createmeta create screen but set on Initiatives).

**Optional:** Target start/end `10022`/`10023`, Sprint `10020`, Story Points `10091`.

**Create-default status:** **To Do (11092)** → transition **101** → **Idea Backlog (11256)**.

**Corrections applied:** outdated pre-Cloud-migration ids (16713/16714, 10005, 13301/15001, `vulcan.stepstone.com`) were wrong; corrected in local skills (gitignored) and core repo references.

### 6. Lean v1 Scope — Risk Mitigation Applied

Per critical review + user decisions:
- **Dropped:** `matd-ops` agent (→ command calls scripts directly), `agent-assignments.yml` + assign/validate/execute, multi-agent build orchestration, automated Stash push (→ human), alternative Solution Design template (→ spec 004).
- **Kept:** SDP-key write-back, full `index.yml` (`specs[]` + archival), archived-specs folder schema.
- **Changed:** SDP via MCP (not REST-with-token), structural validator **advisory** in v1, Jira config scaffold (marketplace) / live config (workspace only, OSS-safe).

**Top risks mitigated:**
- R2 (MCP can't create/transition) → ✅ proven viable
- R3 (Stash push fragility) → human pushes in v1
- R6 (OSS-safe leak) → corp IDs in workspace config only, never marketplace

### 7. Three-Input DESIGN Model Defined

**Solution Design = f(Product Brief [business invariants], System Constitution [technical invariants], PRD [the change])**

- **Product Brief** (spec 002): persistent, business case as invariant (Vision, Scope, Value, RACI, Governance, Budget, Metrics) — from Confluence "Project Charter Template" (ME/170265460), workspace `product/brief.md` is SoT.
- **System Constitution** (spec 003): persistent, technical invariants (EA principles, Tech Radar, AWS, data/API standards, team skills, Stonehenge) — mirrors EA/DigiGov/TechOps Confluence, workspace `architecture/system-constitution.md` is working doc.
- **PRD** (spec 001): transient, the change request (Problem, Goals, Hypothesis, Metrics, User Workflows) — numbered `PRD-NNN`, archived on completion.
- **Solution Design** (spec 004): transient, Tech-owned "how" (FRs+NFRs, C4, cost, capacity) — 9-section EA structure, frozen at gate, links `PRD-NNN ↔ SPEC/EPIC`.

### 8. V-Model & Content Tests

- **V-model traceability:** `PRD-NNN ↔ SDP-key (1:1), PRD → Specs (1:many), Spec ↔ Epic (1:1)`. Hierarchical permanent IDs (never renumbered, only deprecated).
- **Content tests:** "unit tests for English" — deterministic validators (structural) + LLM eval rubrics (advisory). Gate PRD → SDP in spec 001.
- **Three enforcement layers:** in-prompt gates, deterministic validators, AI peer-review (matd-critical-thinker).

### 9. Documentation Created

**Core repo (`docs/`):**
- [specs/001-speckit-matd-specify-prd/spec.md](../../docs/specs/001-speckit-matd-specify-prd/spec.md) — PRD command (OQ-1..11 resolved), plus [plan.md](../../docs/specs/001-speckit-matd-specify-prd/plan.md) + [dependency-map.md](../../docs/specs/001-speckit-matd-specify-prd/dependency-map.md)
- [specs/002-speckit-matd-specify-product-brief/spec.md](../../docs/specs/002-speckit-matd-specify-product-brief/spec.md) — Product Brief (stub, OQ-B1..5 resolved)
- [specs/003-speckit-matd-specify-constitution/spec.md](../../docs/specs/003-speckit-matd-specify-constitution/spec.md) — System Constitution (stub, full skill design)
- [specs/004-speckit-matd-specify-solution-design/spec.md](../../docs/specs/004-speckit-matd-specify-solution-design/spec.md) — Solution Design alt template (stub, 9-section structure)
- [specs/005-atlassian-sdp-skill-migration/spec.md](../../docs/specs/005-atlassian-sdp-skill-migration/spec.md) — Migration plan (deferred, validation gate)
- [specs/006-agent-restrictions-experiment/spec.md](../../docs/specs/006-agent-restrictions-experiment/spec.md) — Agent restrictions (stub, formal decision gates)
- [specs/007-split-claude-code-plugin/spec.md](../../docs/specs/007-split-claude-code-plugin/spec.md) — Plugin split (stub, command marketplace vs. extension)
- [specs/008-split-speckit-extension/spec.md](../../docs/specs/008-split-speckit-extension/spec.md) — Extension split (stub, 7-section design)
- [specs/009-speckit-preset-specify-override/spec.md](../../docs/specs/009-speckit-preset-specify-override/spec.md) — /specify override (stub, multi-template support)
- [specs/010-speckit-determine-change-level/spec.md](../../docs/specs/010-speckit-determine-change-level/spec.md) — Change-level skill (stub, MATD/matd-ops CLI API)
- [specs/011-speckit-estimate-complexity/spec.md](../../docs/specs/011-speckit-estimate-complexity/spec.md) — Complexity estimation skill (stub, story-point focus)
- [references/sdp-jira-fields.md](../../docs/references/sdp-jira-fields.md) ✅ — Authoritative SDP Initiative field reference
- [references/jira-mcp-sdp-creation.md](../../docs/references/jira-mcp-sdp-creation.md) — MCP path analysis + correction
- [references/architecture-designs-confluence.md](../../docs/references/architecture-designs-confluence.md), [agentic-pdlc-workspace-summary.md](../../docs/references/agentic-pdlc-workspace-summary.md), [spec-kit-v-model-summary.md](../../docs/references/spec-kit-v-model-summary.md), [spec-kit-agent-assign-summary.md](../../docs/references/spec-kit-agent-assign-summary.md), [confluence-project-charter.md](../../docs/references/confluence-project-charter.md), [confluence-constitution-sources.md](../../docs/references/confluence-constitution-sources.md)

**Harness-tooling:**
- [TARGET_STATE.md](./TARGET_STATE.md) §5 — Atlassian/SDP skill migration deferred; MCP-first + OSS-safe split; running-MCP assumption
- [AGENT_SKILL_MATRIX.md](./AGENT_SKILL_MATRIX.md) — 7-agent architecture, agent-skill mappings, restriction levels
- [COMMAND_INVENTORY.md](./COMMAND_INVENTORY.md) — 72 commands catalogued, gaps identified
- [STDD_CLEANUP.md](./STDD_CLEANUP.md) — 7 skills for deletion, 1 rename

**Memory (core repo `.claude/projects/.../memory/`):**
- `sdp-jira-field-truth.md` — notes that gitignored local skills can vanish; durable truth in committed `docs/references/`
- `ea-maps-constitution-input.md` — reminder for Daniel to provide EA-Maps content

## Next Steps (Priority Order)

### 1. Build Spec 001 (PRD Command) — Implementation-Ready

**Lean v1 deliverables:**
- `prd-schema.yml` (thin: sections + grill prompts)
- Command file (`commands/speckit-matd-specify-prd.md`)
- Advisory validator script (structural only)
- LLM eval rubric
- SDP create+transition script (MCP `jira_create_issue` → `jira_transition_issue` 101 → Idea Backlog)
- Local commit + remote-link script (`jira_create_remote_issue_link`)
- SDP-key write-back script
- `index.yml` maintenance scripts (`allocate_prd_id.py`)
- Jira config scaffold (marketplace, blank template)

**Build estimate:** ~20-24 SP, single builder, sequential

**Blockers:** none (only a 5-min Team UUID write-format check at build time)

**Dependencies:** assume `atlassian-write` MCP installed & running in workspace

### 2. Execute STDD Cleanup

**Ready to execute:**
- Delete 7 skills: `stepstone-tech-design-doc-{author,critical-review,reviewer,test-reviewer}`, `stepstone-backend-dev`, `stepstone-debugger`, `stepstone-implementer`
- Rename 1 skill: `stepstone-agent-restrictions` → `stepstone-matd-agent-restrictions`
- Rationale captured in [STDD_CLEANUP.md](./STDD_CLEANUP.md)

### 3. Detail Specs 006-011

**Specs ready for detailing:**
- **006:** Agent restrictions experiment (formal decision gates, cascading restrictions)
- **007:** Split Claude Code plugin (command marketplace vs. extension)
- **008:** Split SpecKit extension (7-section design: v-model + workspace + skills + agent-restrictions + budget + MATD)
- **009:** SpecKit preset /specify override (multi-template support, preset field, template discovery)
- **010:** determine-change-level skill (MATD/matd-ops CLI API, single-file Confluence check)
- **011:** estimate-complexity skill (story points, calibrated examples)

### 4. Detail Specs 002/003/004 (Product Brief, Constitution, Solution Design)

**Spec 002 (product-brief):**
- **Remaining:** derive `product-brief-schema.yml` from the Project Charter Template (ME/170265460) + validate against 1-2 real Charter examples (OQ-B6)
- **Build after:** schema derivation + template alignment

**Spec 003 (constitution):**
- **Remaining:** none; full skill design captured (placement `.claude/skills/stepstone-system-constitution/`, template checklist, references/pdlc/, team-specific section)
- **Build after:** spec 001 ships (not blocking)

**Spec 004 (solution-design alt template):**
- **Remaining:** enhance existing vs. add template variant (OQ-S1), 9-section EA structure reconciliation (OQ-S2), ADR handling (OQ-S3), freeze-gate mechanics (OQ-S4), yml schema + content-test rubric (OQ-S5)
- **Build after:** spec 001 ships and PRD→SDP flow is proven

### 5. Execute Spec 005 Validation Gate

**Before** migrating `stepstone-atlassian-skills` + `stepstone-sdp-planning` into the matd plugin:
- **Search** StepStone's internal Claude Code / agent marketplace(s) and `stst-ai-tools-marketplace` for existing Jira/SDP/Atlassian MCP plugins
- **If maintained plugin exists** → adopt/depend on it; reduce local skills to thin workspace-config layer
- **If not** → migrate per TARGET_STATE §5 (MCP-first, OSS-safe split)

### 6. Complete Remaining Grilling Items

**Section 3 (Tier 1-2):** Still open from original grilling scope
**Section 8 (Tier 3):** 8 items remaining (lower priority, nice-to-have)

## Key Decisions & Rationale

| Decision | Rationale | Impact |
|----------|-----------|--------|
| **SDP via `atlassian-write` MCP** | Tested & proven; auth at MCP layer; write tools available | R2 risk mitigated; cleaner than REST-with-token |
| **Drop matd-ops agent** | Command calls scripts directly → simpler, no LLM indirection for deterministic plumbing | -5 SP, token savings |
| **Drop agent-assignments.yml** | Fixed 3-step flow doesn't need yml-driven assignment engine | -3 SP, defer until 2nd command |
| **Human pushes to Stash (v1)** | Removes auth/non-fast-forward fragility from automated path | R3 risk mitigated |
| **Team = customfield_10001 (UUID)** | Verified on live SDP-6701; not on createmeta but set on Initiatives | Corrects outdated DC-era ids |
| **Jira config: scaffold (marketplace) / live (workspace only)** | OSS-safe: corp IDs never in marketplace, always in workspace | R6 risk mitigated |
| **Product Brief = workspace SoT** | Product-team-owned; Confluence becomes a markdown view (linked outward) | Matches PRD pattern (workspace repo authoritative) |
| **Constitution mirrors EA/Confluence** | EA owns tech invariants in Confluence; workspace holds refreshed mirror | Different ownership ⇒ different authority direction |
| **Defer skill migration to spec 005** | StepStone marketplace may already have Jira/SDP plugins — validate before building | Avoids reinventing; cleaner OSS-safe split |
| **7-agent architecture** | Fixed core agents (matd-specifier, matd-critical-thinker, matd-reviewer, matd-test-reviewer, matd-ops, matd-implementer, matd-debugger) | Clean separation of concerns; matd-ops caveman for deterministic ops |
| **Formal decision gates for restrictions** | Agent-level enforcement (not just prompt hints), cascading priority (forbidden > suggested > required) | Prevents accidental violations; supports spec 006 experiment |
| **Command marketplace split** | Commands/plugins vs. SpecKit extension (preset/settings) | OSS-safe, reusable command marketplace; SpecKit-specific config separate |

## Assumptions & Preconditions

1. **`atlassian-write` MCP installed & running** in each agent workspace (env vars + cert configured) — workspace precondition, like Stash auth.
2. **Stash auth works** — commands assume working SSH/token; humans push in v1.
3. **Agent workspace repo exists** (one per system, workspace-template structure) — Staff Engineer/EM provisions for new systems; PMs use existing.
4. **Jira is Atlassian Cloud** `stepstone.atlassian.net` — post-migration; DC-era ids (`vulcan.stepstone.com`, 16713/16714, 10005, 13301/15001) are deprecated.
5. **7-agent architecture is fixed** — no dynamic agent creation/assignment in v1; fixed roles per AGENT_SKILL_MATRIX.md.
6. **Story points, not hours** — complexity estimation uses Agile story points (calibrated examples), never hourly time estimates.
7. **Lean v1 focus** — specs 001 implementation-ready; specs 002-011 stub/design stage; no parallel builds until 001 ships.

## References

- **Core repo:** `harness-sandbox-stony/docs/specs/` (specs 001-011), `docs/references/`, `DOCUMENT_INDEX.md`
- **Harness-tooling:** `TARGET_STATE.md`, `AGENT_SKILL_MATRIX.md`, `COMMAND_INVENTORY.md`, `STDD_CLEANUP.md`
- **Committed state:** core `dev` branch, harness-tooling `dev` branch (post-grilling 2026-06-10)
- **Confluence sources:**
  - Project Charter Template (ME/170265460)
  - Solution Design (ARCH/205793182, 205853106)
  - EA Standards, Principles, Tech Radar, AWS Structure (ARCH 205816680+)
  - AI Principles, EU AI-Act (DIG 126059588+)
- **External repos:** `spec-kit-v-model`, `spec-kit-agent-assign` (GitHub, cloned to `submodules/watching/`)

## Risks & Mitigations

See [core repo `docs/specs/001-.../spec.md` §v1 scope & risk register](../../docs/specs/001-speckit-matd-specify-prd/spec.md) for the full table. Key points:

| Risk | Severity | Status |
|------|----------|--------|
| **Jira MCP can't create/transition** | High | ✅ **Mitigated** — tested OK 2026-06-08 |
| **Stash push fragility** | Med-High | ✅ **Mitigated** — human pushes in v1 |
| **OSS-safe leak of corp IDs** | High | ✅ **Mitigated** — scaffold (marketplace) / live config (workspace only) |
| **Content-test false gates** | Med | ✅ **Mitigated** — advisory (warn) in v1; only frontmatter/sections are hard |
| **Jira transition-id drift** | Med | **Managed** — runtime lookup via `GET /transitions` |

## Session Artifacts

**Conversations:**
- 2026-06-08..09: Spec design + MCP validation + SDP field verification + critical review
- 2026-06-09..10: Grilling session (specs 002-011), 7-agent architecture, command inventory, STDD cleanup

**Commits (pending):**
- Core repo `dev`: specs 006-011 stub files, updated references
- Harness-tooling `dev`: AGENT_SKILL_MATRIX.md, COMMAND_INVENTORY.md, STDD_CLEANUP.md, STATUS.md update

**Gitignored local skills** (corrected, not committed): `stepstone-atlassian-skills/references/sdp-custom-fields.md`, `stepstone-sdp-planning/references/02-workflow.md`, `jira-teams-config.yaml` (Sprint 10005→10020)

---

**Bottom line:** Spec 001 is ready to build (~20-24 SP). Specs 002-011 are stub/design stage with architecture and key decisions captured. 7-agent architecture finalized. Enhanced workspace structure designed. STDD cleanup ready to execute. Grilling session completed with 6 open questions remaining (Section 3 + 8 Tier 3 items). SDP/Jira MCP integration proven. Lean v1 focus maintained.
