---
type: spec
feature_id: "004-speckit-matd-specify-solution-design"
title: "speckit-matd-specify-solution-design — alternative Solution Design template (FUTURE STUB)"
status: stub
created: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
---

# Spec (STUB): `speckit-matd-specify-solution-design` (alternative template)

> **Status: STUB.** Captures **all Solution Design information gathered in the 2026-06-08 design
> conversation** for later build. Companion to [001 PRD](../001-speckit-matd-specify-prd/spec.md),
> [002 product-brief](../002-speckit-matd-specify-product-brief/spec.md),
> [003 constitution](../003-speckit-matd-specify-constitution/spec.md). The **"how" half** of the
> DESIGN stage. Moved here out of spec 001 (it is a No-goal of the PRD command).

## What & Why
The **Solution Design** is the Tech-owned **"how we deliver it — the frozen baseline"** artefact of
the DESIGN stage (PRD is the Product-owned "what"). It is **derived from the PRD** and **stays
living through execution until frozen at a gate**. This spec defines an **alternative Solution
Design template** modelled on StepStone's official Enterprise-Architecture structure — **distinct
from** the existing C4-centric `solution-design-template.md` and the existing
`speckit-matd-specify-solution-design` command (which this would enhance / offer as an alternative).

**Three-input model:** Solution Design = f(**Product Brief** [business invariants], **System
Constitution** [technical invariants], **PRD** [the change]).

## DESIGN-stage context (from screenshots)
- **PRD (Product):** problem framing, goals/non-goals, success metrics w/ measurement, user
  workflows & outcomes — *no screens/service-names/schemas*.
- **Solution Design (Tech) — the frozen baseline:** Functional + Non-functional requirements;
  Architecture decisions & constraints (ADRs for contested ones); Service boundaries, interfaces,
  data model; Target architecture (As-is / Target / transition); Dependencies, risks, costs, fit
  with policies & data architecture; C4 diagrams; low-level design where critical.
- **Workflow timing:** 6-week window — "WHAT" (PRD ~2wks) → **"HOW" (Solution Design ~2wks)** →
  "WHEN" (P&T SDP Planning ~2wks). ProductOps scorecards each initiative on **SD presence**, **SD
  quality** (FR complete · NFR coverage · decisions · boundaries · diagrams · costs) and
  **traceability** (PRD ↔ SD ↔ epics ↔ stories).

## Alternative template — StepStone official 9-section structure
(Source: [architecture-designs-confluence.md](../../references/architecture-designs-confluence.md),
Confluence ARCH/205793182; template page 205853106.)

1. **Solution Context** — Functional + Non-Functional Requirements
2. **Business Capability Mapping**
3. **High-Level Design (HLD)** — C4 **System + Container** diagrams (Staff Engineer authors)
4. **Data Architecture**
5. **Interfaces**
6. **Technology, Patterns & Core Concepts**
7. **Infrastructure Cost Estimate & Trade-offs** (monthly + annual; cost vs perf, build vs buy)
8. **Capacity & Resource Plan**
9. **Risk & Dependency Log**

**NFR categories (13 prefixes):** PERF, AVAIL, SCALE, SEC, DATA, GDPR, OBS, REC, USA, DOC, ARCH,
RES, COST. Tracked as a table: Category | Requirement | Target | status (CONFIRMED vs ASSUMPTION)
— e.g. LCP < 2.5s, INP < 200ms, uptime 99.9%.

## Solution Design structure (from screenshots — Architecture Plan + LLD/Refinement)
- **Architecture Plan:**
  - **Functional Requirements**
  - **Non-functional Requirements** → *Product-Specific NFRs* · *Enterprise NFRs* · *Relevant
    Platform NFRs (e.g. AI-Agent)*
  - **High-Level Design** → *Components & Resources* · *System View* · *BC & Data Impact*
  - **Infrastructure cost estimate**
- **LLD / Refinement:** Interfaces · Data Model · Low-level Design · Data Processing · Deep Dives

> The two structures reconcile: the 9-section Confluence template is the canonical doc shape; the
> screenshot's Architecture-Plan/LLD split is the working breakdown. The alternative template should
> present the 9 sections with the Architecture-Plan vs LLD/Refinement grouping, NFRs sub-split into
> Product / Enterprise / Platform.

## When a Solution Design is required (mandatory triggers)
New OKR-aligned objective (SDP ticket) · impact spans multiple teams · substantial investment
(> 2–3 sprints) · introducing a new service / component / dependency.

## Ownership & review
Staff Engineer owns delivery; PM owns FRs; EM / Principal Engineer / Enterprise Architect review &
approve. 4-phase workflow (Prep → Design → Analysis → Review), ~2–3 wks (small/medium) or 4–6 wks
(large). Lives through execution; **frozen at a gate** (human action).

## Acceptance-criteria categories (from Confluence)
Design Quality · Feasibility Confirmation · Cost & Resource Clarity · Risk Management · Team
Collaboration · Stakeholder Alignment. (Use as the content-test/checklist basis — the SD's
"unit tests for English", analogous to the PRD content test.)

## Design notes for the command (consistent with 001)
- **Alternative** to the existing C4-centric `solution-design-template.md`; offer both (the EA
  9-section template here is the StepStone-official alternative).
- Consume the three inputs (Product Brief, System Constitution, PRD) + reference the system
  constitution's tech invariants (NFRs, tech radar, AWS, data/API standards) and Stonehenge.
- Realised as a **SpecKit command + shipped template** (Principle 7) with a content-test gate
  (checklist/analyze). Scripted plumbing; smart agent (`matd-architect`) authors; advisory review.
- Traceability IDs link PRD `REQ-NNN`/`PRD-NNN` → SD → Spec/Epic (the `index.yml` `specs[]` slots
  reserved by 001 are filled here).

## Dependencies

### Upstream Dependencies
- **SPEC-013** (Enhanced Workspace Structure) - BLOCKS THIS SPEC
  - Requires: Config location pattern (`.specify/extensions/matd/matd-config.yml`)
  - Requires: `solution-designs/` path configuration in matd-config.yml
  - Requires: Traceability frontmatter schema (sd_id, prd, requirements, adrs)
  - Status: Design-complete, 8 SP
- **SPEC-002** (Product Brief) - Required input (business invariants)
- **SPEC-003** (System Constitution) - Required input (technical invariants)
- **SPEC-001** (PRD Command) - Related (PRD is the third input to Solution Design)

### Three-Input Model
Solution Design = f(**Product Brief**, **System Constitution**, **PRD**)
- Product Brief provides business invariants (vision, scope, value, stakeholders)
- System Constitution provides technical invariants (EA principles, tech radar, NFRs, standards)
- PRD provides the change request (what needs to be delivered)

## Open Questions
- OQ-S1: Enhance the existing `speckit-matd-specify-solution-design` command vs. add a template variant?
- OQ-S2: Reconcile the existing C4-centric template with this EA 9-section template — both selectable?
- OQ-S3: ADR handling — inline vs. separate ADR command (there is an existing `specify-adr`).
- OQ-S4: Freeze-gate mechanics + how SD updates flow back to the index/traceability.
- OQ-S5: yml schema + content-test rubric (map the 6 acceptance-criteria categories to checks).

## References
- [architecture-designs-confluence.md](../../references/architecture-designs-confluence.md) (StepStone official SD definition)
- Existing `spec-kit-multi-agent-tdd/templates/solution-design-template.md` (C4-centric — the one this offers an alternative to)
- Existing command `spec-kit-multi-agent-tdd/commands/specify-solution-design.md`
- [001 PRD spec — three-input DESIGN model](../001-speckit-matd-specify-prd/spec.md)
- Screenshots (DESIGN stage: PRD vs Solution Design; 6-week window; scorecard; SD structure) — provided 2026-06-08
