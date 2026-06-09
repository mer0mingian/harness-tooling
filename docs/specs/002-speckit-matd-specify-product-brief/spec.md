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
- **Enhance** the existing `speckit-matd-specify-product-brief` command (not a new command) to:
  - **Inform the template structure from the Confluence Product Charter** (its 11-section /
    stable-subset shape → the `product-brief-template.md` sections). Source captured in
    [confluence-project-charter.md](../../references/confluence-project-charter.md) — research found
    "Project Charter Template (5+ SP)" (ME, 170265460); confirm whether a distinct **Product
    Charter** exists vs. the same page (OQ-B5).
  - Author/maintain the brief **in the workspace** (authoritative); **publish a markdown view to Confluence** (read-only link/embed).
  - Extend/refine via **grill-me** for gaps the Charter structure doesn't cover.
  - Frame content as **Product Invariants** (stable; fundamental change ⇒ new product).
- Support **new and existing** products (existing → extract from Charter/repo; new → grill).
- Output to the **persistent** `product/brief.md` (never archived; evolves with the product).
- yml-schema-driven + content-test gated, consistent with the PRD command (concise written doc;
  checklist/structure in the template).

## Content (Product Charter stable subset → Product Invariants)
Vision & Why · Scope (in/out) · quantified Business Value + realization timeline · Success
criteria/metrics · Stakeholders/RACI · Governance & compliance gates · Budget/investment ·
Affected policies/processes. (Full 11-section Charter structure + 20 table schemas in the
reference doc.) Apply the Charter framework's "right-size to complexity" and "Specifications not
Requirements" rules. Reuse the existing `product-brief-template.md` / workspace `product/brief.md`
if valid; else align to this subset.

## Open Questions
- OQ-B1: ✅ **RESOLVED (2026-06-08)** — enhance existing product-brief command; name "Product Brief"; placement `product/brief.md`; reuse existing template if it fits.
- OQ-B2: ✅ **RESOLVED (2026-06-09):** **Schema-driven gap-filling, not source-specific extraction.** The command takes **whatever initial content the user provides** (Confluence Charter link, existing `product/brief.md`, draft doc, bullet points, or nothing), loads the Product Brief schema/template, and **grills to fill only the non-answered questions** (skips what's already covered). Flexible input; consistent output.
- OQ-B3: ✅ **RESOLVED (2026-06-08):** Agent workspace repo (`product/brief.md`) is the **source of truth**; Confluence is a **markdown-view link** (not authority). Template **structure informed by the Product Charter**. Publish direction workspace → Confluence.
- OQ-B4: ✅ **RESOLVED (2026-06-08):** Brief holds **stable, identity-defining business invariants** (vision, target market/users, value proposition, business/monetization model, non-negotiable governance/compliance, top-level product KPIs) — no dated/temporary/feature/implementation detail. A change to one of these is a new-product/major-version event. The brief **may slowly evolve**; a **PRD is a change/feature/new-product request**. The content-test asserts entries are invariant-level. (yml schema + exact rubric still to detail at build time.)
- OQ-B5: ✅ **RESOLVED (2026-06-09):** Use the **"Project Charter Template"** (ME/170265460) as the canonical structure source — it's the org's standard for product business cases. Frame the output as the **Product Brief** to distinguish persistent product-level invariants from transient project artifacts. The 11-section Charter structure + 20 table schemas (captured in [confluence-project-charter.md](../../references/confluence-project-charter.md)) are the stable subset.
- **OQ-B6 (NEW, design):** Derive a **generic `product-brief-schema.yml`** from the Charter template (applicable to any future product, not over-fit). Start with the template structure (sections/tables), validate against 1-2 real filled Charter examples to ground field types/cardinality. The schema drives the grill + rendering, analogous to `prd-schema.yml` in spec 001.

## References
- [confluence-project-charter.md](../../references/confluence-project-charter.md)
- [001 PRD spec — three-input DESIGN model](../001-speckit-matd-specify-prd/spec.md)
- Existing command `spec-kit-multi-agent-tdd/commands/specify-product-brief.md` + `product-brief-template.md`
- workspace-template `product/brief.md` (existing scaffold)
