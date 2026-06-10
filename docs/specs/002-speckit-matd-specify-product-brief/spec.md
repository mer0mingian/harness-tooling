---
type: spec
feature_id: "002-speckit-matd-specify-product-brief"
title: "speckit-matd-specify-product-brief — Product Brief (business invariants) ENHANCEMENT (FUTURE STUB)"
status: stub
created: "2026-06-08"
updated: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
---

# Spec (STUB): `speckit-matd-specify-product-brief` (enhancement)

> **Status: STUB.** Companion to [001-speckit-matd-specify-prd](../001-speckit-matd-specify-prd/spec.md).
> The **business-invariants** pillar of the three-input DESIGN model (Product Brief + System
> Constitution + PRD → Solution Design).

## Decision (Spec-002 Q1, 2026-06-08)
**Enhance the existing `speckit-matd-specify-product-brief` command — do not create a second
business doc.** Canonical name = **Product Brief** (keep the existing command, template, and
`product/brief.md` file). The Product Brief is the content of the Confluence **Product Charter**
and displays **Product Invariants**: the **business case for a product is itself an invariant**
— if it changes fundamentally, it becomes a *new* product (new brief), which is why the brief is
**persistent** (never archived). Reuse the current template/structure if it fits the purpose;
otherwise align it to the Charter's stable subset.

## What & Why
A persistent, per-workspace **Product Brief** capturing **business invariants** (vision, scope,
value, stakeholders, governance, budget, success criteria) — the business case, expressed as
invariants. One of three inputs to Solution Design. Distinct from a PRD (a transient change request).

## Source of truth & authority (Spec-002 Q2 / OQ-B3, 2026-06-08)
**The Product Brief in the system's agent workspace repo (`product/brief.md`, on Stash) is the
source of truth — NOT Confluence.** Confluence renders it via a **markdown-view link/embed** so it
stays visible to stakeholders, but Confluence is **not the authority**; the agent workspace is.
Direction is workspace → Confluence (view), never Confluence → authoritative-write. This matches
the PRD pattern (workspace repo authoritative, linked outward into Jira/Confluence).

> **Note (no contradiction with the System Constitution):** the Product Brief is *product-team-owned*,
> so the workspace is authoritative. The **System Constitution** mirrors *enterprise* invariants that
> **EA owns in Confluence** (ARCH/DIG/TECHOPS) — there Confluence stays authoritative and the
> workspace holds a refreshed mirror. Different ownership ⇒ different authority direction, by design.

## Goals
- **Enhance** the existing `speckit-matd-specify-product-brief` command with two-tier schema:
  - **Tier A (Simple)**: Lightweight template for systems with ≤3 components (match workspace `product/brief.md`)
  - **Tier B (Full Charter)**: Full 9-section business-focused Charter for systems with ≥4 components
  - **Tier selection**: Query Stonehenge for component count at command start
  - **Inform structure from Charter**: Full template structure captured in [confluence-project-charter.md](../../references/confluence-project-charter.md)
  - Author/maintain the brief **in the workspace** (authoritative)
  - **Confluence publish (v1)**: Manual copy/paste by user when needed
  - **Confluence publish (future)**: Automated markdown macro embed for read-only view
  - Extend/refine via **grill-me** for gaps the Charter structure doesn't cover
  - Frame content as **Product Invariants** (stable; fundamental change ⇒ new product)
- Support **new and existing** products (existing → extract from Charter/repo; new → grill)
- Output to the **persistent** `product/brief.md` (never archived; evolves with the product)
- **Schema architecture**: Two separate schemas (not conditional)
  - `product-brief-simple-schema.yml` (Tier A, ≤3 components)
  - `product-brief-charter-schema.yml` (Tier B, ≥4 components)
  - Command selects schema based on Stonehenge component count
- **Validation**: Two-layer approach (consistent with PRD command)
  - Structural validator: Required sections present, field types correct
  - Content validator (LLM rubric): Semantic check - "Are these business invariants?" (not implementation detail, not temporary/dated)

## Content Structure

### Tier A (Simple - ≤3 components)
Based on workspace-template `product/brief.md`:
1. Vision (problem statement, strategic alignment)
2. Target Users (personas, goals, pain points)
3. Key Features (high-level capabilities with priorities)
4. Success Metrics (measurable KPIs)
5. Constraints (budget, timeline, resources, technical, compliance)
6. Dependencies (internal/external/data)
7. Risks (with mitigations)
8. Out of Scope (explicit exclusions)

### Tier B (Full Charter - ≥4 components)
**Business-focused subset** from Charter (excludes technical implementation sections):

**Included from Charter:**
- Section 0: Canvas Quick Reference
- Section 1: Vision & Why (Purpose, Business Value, Success Criteria)
- Section 2: Scope & Deliverables (In/Out, Key Deliverables, Dependencies)
- Section 4: Investment & Cost (Estimated Cost, Investment Breakdown, Timeline & Milestones)
- Section 5: Stakeholders & RACI (RACI Matrix, Core Team, Accountable/Consulted/Informed)
- Section 6: Risks & Issues (Risk Register, Issues Log)
- Section 7: Compliance & Governance (GDPR, AI/ML, Security Review, Architecture Review gates)
- Section 9: Success Metrics & Measurement (Key Metrics, Categories, Timeline, Evaluation)
- Section 10: Policies & Processes Affected (Documentation, Process Changes)
- Section 11: Relevant Links & Resources

**Excluded from Charter (belong in Solution Design or System Constitution):**
- ❌ Section 3: Solution Approach (Technical Approach, ADRs, Technology Choices) → Solution Design
- ❌ Section 8: Quality & NFRs (Testing Strategy, Monitoring, NFRs) → System Constitution

**Rationale:** Product Brief captures business invariants only. Technical decisions (architecture, tech choices, NFRs) belong in Solution Design and System Constitution per three-input model.

## Open Questions

### Resolved
- OQ-B1: ✅ **RESOLVED (2026-06-08)** — enhance existing product-brief command; name "Product Brief"; placement `product/brief.md`; reuse existing template if it fits.
- OQ-B2: ✅ **RESOLVED (2026-06-09):** Schema-driven gap-filling, not source-specific extraction. Flexible input; consistent output.
- OQ-B3: ✅ **RESOLVED (2026-06-08):** Agent workspace repo (`product/brief.md`) is source of truth; Confluence is markdown-view link.
- OQ-B4: ✅ **RESOLVED (2026-06-08):** Brief holds stable, identity-defining business invariants only.
- OQ-B5: ✅ **RESOLVED (2026-06-09):** Use "Project Charter Template" (ME/170265460) as canonical structure source.
- OQ-B6: ✅ **RESOLVED (2026-06-10):** Two-tier schema based on Stonehenge component count (≤3 = Tier A, ≥4 = Tier B).
- OQ-B10: ✅ **RESOLVED (2026-06-10):** Tier B includes business-focused Charter subset only (9 sections), excludes Solution Approach & Quality/NFRs (belong in Solution Design/Constitution).
- OQ-B11: ✅ **RESOLVED (2026-06-10):** Confluence publish v1 = manual copy/paste. Automated markdown macro embed deferred to future enhancement.
- OQ-B12: ✅ **RESOLVED (2026-06-10):** Two separate schemas (product-brief-simple-schema.yml, product-brief-charter-schema.yml). Command selects based on component count. Two-layer validation: structural + semantic (LLM rubric checks "business invariants only").

### Needs Clarification (MCP Integration)
- **OQ-B7:** System name → Stonehenge entity mapping for component count query
  - How does user-provided system name map to Stonehenge catalog entity?
  - Field to filter on? (`metadata.name`, `metadata.title`, custom field?)
  - Exact SQL WHERE clause pattern?
  
- **OQ-B8:** EA Maps fallback mechanism
  - When to use EA Maps vs Stonehenge?
  - How to query EA Maps programmatically?
  - EA Maps MCP tool status?
  - Integration priority: Stonehenge primary, EA Maps fallback?
  
- **OQ-B9:** MCP tool deployment in MATD workspaces
  - Is `stonehenge-mcp` auto-installed in harness sandbox?
  - Manual installation steps if needed?
  - Network requirements (corporate VPN)?
  - Graceful degradation if MCP unavailable?

## Dependencies

### Upstream Dependencies
- **SPEC-013** (Enhanced Workspace Structure) - BLOCKS THIS SPEC
  - Requires: Config location pattern (`.specify/extensions/matd/matd-config.yml`)
  - Requires: `product/` path configuration in matd-config.yml
  - Status: Design-complete, 6 SP

### External Dependencies
- **Stonehenge MCP Server** - Component count query (CLARIFICATION NEEDED)
  - **MCP Tool:** `mcp__stonehenge-mcp__execute_query` (already exists, production-ready)
  - **Endpoint:** `https://stonehenge-mcp.ds.daas.stepstone.com/mcp`
  - **Query:** `SELECT COUNT(*) FROM stonehenge WHERE kind = 'Component' AND [system_filter]`
  - **Purpose:** Determine schema tier (Tier A ≤3 components, Tier B ≥4 components)
  - **Required at:** Product Brief creation/update time
  - **Authentication:** Network-based (corporate VPN), no API keys
  - **Reference:** [stonehenge-api-access.md](../../references/stonehenge-api-access.md)
  - **NEEDS CLARIFICATION:**
    - System name → Stonehenge entity mapping (how to filter by system?)
    - EA Maps fallback mechanism (when/how to use?)
    - MCP tool configuration in MATD workspaces (install process?)
  - **Fallback:** Manual user input if Stonehenge/MCP unavailable, default to Tier A

### References
- [confluence-project-charter.md](../../references/confluence-project-charter.md)
- [001 PRD spec — three-input DESIGN model](../001-speckit-matd-specify-prd/spec.md)
- Existing command `spec-kit-multi-agent-tdd/commands/specify-product-brief.md` + `product-brief-template.md`
- workspace-template `product/brief.md` (existing scaffold)
