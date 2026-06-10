---
type: spec
feature_id: "003-speckit-matd-specify-constitution"
title: "speckit-matd-specify-constitution — technical-invariants command (FUTURE STUB)"
status: stub
created: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
---

# Spec (STUB): `speckit-matd-specify-constitution`

> **Status: STUB.** Captures intent + research so a full spec can be written later. Companion to
> [001-speckit-matd-specify-prd](../001-speckit-matd-specify-prd/spec.md). Part of the three-input
> DESIGN model (System Constitution = **technical invariants**).

## What & Why
A SpecKit MATD command that produces/maintains the **System Constitution** — the persistent
**technical-invariants** document: company tech policies, tech radar, architectural rules/
principles, team skill sets, AWS accounts, ingress/network topology, data/API standards,
security & AI-Act compliance. It is one of the three inputs to Solution Design (with the
project brief and a PRD). It captures **only technical** invariants — business ones live in the
project brief.

## Goals
- Generate a System Constitution for **both new and existing** projects/workspaces.
- Use **Confluence as reference** (see [confluence-constitution-sources.md](../../references/confluence-constitution-sources.md)):
  - **ARCH** (Enterprise Architecture): EA Standards (205816680), Standards Governance (205834046),
    ~20 EA Principles (205833694–205833772, incl. "NFRs are Non-Negotiable", "Cloud-Native First"),
    Policy registry (251527616), Tech Radar (205816740), AWS Account Structure/Standard/Strategy
    (205803578/205799436/205787448), routing/DNS (205840766/205879296/205901424),
    Data Architecture (205833488) + API/Data Contract Standards (205837384),
    Reference Architectures/Blueprints (205912972/205914241), **ADR: Standardisation of Agent
    Framework** (205899394 — directly relevant to this harness).
  - **DIG** (Digital Governance): AI Principles (126059588), EU AI Act Conformity (126060268),
    AI Logging & Retention (126058852).
  - **TECHOPS**: Naming & Level Conventions (218681516), Critical System Uptime/Availability (218664327), chapter skill-sets.
- Extend/refine via **grill-me**.
- Mirror the PDLC repo's `docs/stepstone-conventions/` pattern: per-invariant **digest** + **raw
  Confluence mirror** + **refresh procedure**.
- Output to the **persistent** location `architecture/system-constitution.md` (never archived).

## Pending input
- **EA-Maps application content** — Daniel to provide; wire in as a reference input. (Memory: `ea-maps-constitution-input`.)

## System-Constitution SKILL — design (DO NOT BUILD YET; specify only)

The command references a dedicated **system-constitution knowledge skill**. Implementing agents
return to this skill to check applicable invariants — not all apply to every change.

### Placement (OSS-safe)
StepStone-specific content (EA principles, AWS accounts, internal endpoints) **must not** enter
the OSS marketplace (`harness-tooling`) per the OSS-safe invariant. → The filled skill lives with
the other gitignored corporate skills: **`.claude/skills/stepstone-system-constitution/`**
(consistent with `stepstone-sdp-planning`, `stepstone-atlassian-skills`). A generic, content-free
*framework* (template shape + update mechanism) MAY later be upstreamed to `harness-tooling`.
*[Confirm — OQ-C6.]*

### Skill layout (to build later)
```
.claude/skills/stepstone-system-constitution/
├── SKILL.md                          # how to build/use/update the constitution; concise
├── templates/
│   └── system-constitution-template.md   # compliance CHECKLIST: bullets + references
├── prompts/
│   └── check-for-updates.md          # update prompt: re-check mirrored sources for drift
└── references/
    ├── pdlc/                          # COPIED from PDLC repo (skip ingress):
    │   ├── compliance-framework.md    #   docs/stepstone-conventions/compliance-framework.md
    │   ├── tech-radar.md              #   docs/stepstone-conventions/tech-radar.md
    │   └── new-application-conventions.md
    └── confluence/                    # MIRRORED via Haiku subagents (future build step)
        ├── ea-principles.md  ea-standards.md  policy-registry.md
        ├── tech-radar.md  aws-accounts.md  data-api-standards.md
        ├── reference-architectures.md  adr-agent-framework.md
        ├── ai-act-compliance.md  ai-logging-retention.md
        └── naming-conventions.md  availability-nfrs.md
```
**Explicitly skip `ingress-topology`.** Source pages enumerated in
[confluence-constitution-sources.md](../../references/confluence-constitution-sources.md).

### Template = compliance checklist
Like the PRD: the **template carries the checklist + structure; the written markdown is concise**.
Each invariant is a **bullet with a reference** (Confluence URL / page id / radar entry) so the doc
doubles as an audit checklist agents can tick against a change. Categories (from research, skip ingress):
- Architecture **principles** (EA: "NFRs are Non-Negotiable", "Cloud-Native First", "Data is Shared", cohesion/coupling) + **standards** + governance
- **Tech radar** (sanctioned/hold technologies)
- **AWS** account structure / landing zones / cloud standards
- **Data & API** contract standards
- **Security & compliance** (DIG: AI principles, EU AI-Act conformity, AI logging/retention)
- **Naming conventions** + **availability/uptime NFRs** (TECHOPS)
- **Agent-framework** standardisation ADR (relevant to this harness)

### New section — Team-specific invariants (brainstorm)
A dedicated constitution section capturing invariants that derive from the **team**, not the enterprise:
- **Team skill sets / chapters** — languages, frameworks, tools the team is fluent in (constrains tech choices to what the team can run).
- **Familiar technologies** — preferred stacks; "unknown tech" flagged as risk requiring spike.
- **AWS setup in use** — the team's accounts/regions/landing-zone, deploy targets.
- **Internal endpoints** — services/APIs reachable only within the team domain / org structure (not public), so designs don't assume external availability.
*(EA-Maps content — pending from Daniel — feeds team skills + org-structure endpoints. Memory: `ea-maps-constitution-input`.)*

### Agent-workspace concept (constitution must explain)
The constitution documents the **agent-workspace doc structure** generated by the harness sandbox
(`product/` brief + PRDs, `architecture/` constitution + decisions + c4, `specs/`, `tests/`,
`research/`, `components/`, `specs_archive/`) so agents know where artefacts live and the
persistence/archival rules (brief + constitution persistent; PRDs/specs archived, numbering kept).

### Stonehenge as source of truth (constitution must explain)
Document how content is retrieved from **Stonehenge** (StepStone's Backstage catalogue) and that it
is the **source of truth** for systems/components/repos/ownership. From the PDLC repo:
- MCP `mcp__stonehenge-mcp__execute_query` — SQL-over-HTTP at `https://stonehenge-mcp.ds.daas.stepstone.com/mcp`; tables `stonehenge`, `entity_scans`, `check_results`, `activity`, `stash`.
- Canonical query patterns in the PDLC repo's `mcp-servers/stonehenge-mcp/sql-cheatsheet.md` (copy/adapt).
- Rule (from PDLC): catalogue is L3 discovery; validate against source (L4) before in-scope claims.

### Update prompt
`prompts/check-for-updates.md` — re-fetches the mirrored Confluence/radar/policy sources, diffs
against the local mirror, and reports drift (which invariants changed) so the constitution can be
refreshed. Mirrors the PDLC `refresh-conventions.sh` + per-file "Refresh procedure" pattern.

### Setup parity with PRD command
yml-schema-driven structure + content-test gate; deterministic fetch/mirror via scripts (Haiku
`matd-ops`-style); smart agent only for synthesis/grill. Concise written output.

## Open Questions
- OQ-C1: Constitution structure — sections per invariant category vs. SpecKit constitution-template shape vs. PDLC conventions-style files.
- OQ-C2: Which ARCH/DIG/TECHOPS pages are MUST-mirror vs. link-only; refresh cadence.
- OQ-C3: How team skill-sets + AWS accounts are represented (link, table, generated from EA-Maps?).
- OQ-C4: Relationship to existing `/speckit-constitution` command (extend vs. replace for the MATD/Stepstone context).
- OQ-C5: yml schema + content-test rubric for the constitution.
- OQ-C6: Skill placement — confirm `.claude/skills/stepstone-system-constitution/` (gitignored, corporate) with optional OSS-safe framework upstreamed to harness-tooling.

## Dependencies

### Upstream Dependencies
- **SPEC-013** (Enhanced Workspace Structure) - BLOCKS THIS SPEC
  - Requires: Config location pattern (`.specify/extensions/matd/matd-config.yml`)
  - Requires: `architecture/` path configuration in matd-config.yml
  - Status: Design-complete, 8 SP
- **EA-Maps application content** - User to provide (Memory: `ea-maps-constitution-input`)

### Related Specs
- **SPEC-002** (Product Brief) - Business invariants (complements this spec's technical invariants)
- **SPEC-004** (Solution Design) - Consumes both Product Brief + Constitution as inputs

## References
- [confluence-constitution-sources.md](../../references/confluence-constitution-sources.md)
- PDLC repo `docs/stepstone-conventions/` (digest+mirror+refresh pattern)
- [001 PRD spec — three-input DESIGN model](../001-speckit-matd-specify-prd/spec.md)
- workspace-template `architecture/system-constitution.md` (existing scaffold)
