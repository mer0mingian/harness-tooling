# agentic-pdlc-workspace — Reference Summary

- **Source:** https://stash.stepstone.com/projects/PLAYGROUND/repos/agentic-pdlc-workspace/browse
- **Clone URL used:** `ssh://git@stash.stepstone.com:7999/playground/agentic-pdlc-workspace.git` (HTTPS failed — no cached credentials)
- **Local (gitignored scratch clone, NOT a submodule):** `submodules/watching/agentic-pdlc-workspace/`
- **Captured:** 2026-06-08
- **Access:** SUCCESS

## What this repo is

A Claude Code marketplace plugin / pilot workspace that implements an **AI-Assisted Product Development Lifecycle (PDLC)** — the "AI-Native SDLC v3.7", an 11-phase pipeline (Ph00–Ph10) from Initiative PRD through System Design, RFCs, Feature PRDs, Epic Implementation Plan, Stories, Tasks, Execution, Deploy, and post-deploy verification. Each phase is driven by a Claude Code **skill** (`.claude/skills/`) and supported by specialist **sub-agents** (`.claude/agents/`), each with a strict evidence ceiling.

**Load-bearing invariant — the evidence hierarchy (cited on every claim):**
```
0 model inference < 1 PRD < 2 docs/wiki/ADRs < 3 Stonehenge catalogue < 4 source/tests/CI/IaC < 5 deployed runtime
```
PRD claims are L1 (hints, not truth). Higher levels override lower ones.

> **NOTE on "Constitution":** No "Constitution" artefact, principle set, or governance/charter document exists in this repo (searched `constitution|principle|governance|charter` across all `.md`/`.json` — zero hits). The closest analogues are the **CLAUDE.md "Hard rules in this workspace" (11 numbered rules)** and the **evidence hierarchy**. If "Constitution" refers to the SpecKit `/constitution` concept, it is not present here.

## Repo structure (key dirs/files)

```
agentic-pdlc-workspace/
├── CLAUDE.md                  # 11 "Hard rules", path scheme, agents+evidence ceilings, MCP usage
├── README.md                  # pilot context, EIP frontmatter spec, full phase-by-phase table
├── TEAM-QUICKSTART.md
├── .claude/
│   ├── agents/                # 14 specialist sub-agents (each with evidence ceiling)
│   ├── skills/                # 30+ skills — one per PDLC phase + gates
│   │   ├── prd/               # Ph00 Initiative PRD (17-section template)
│   │   ├── feature-prd/       # Ph01 Feature PRD (= Epic) — L7 thesis template
│   │   ├── feature-prd-eval/  # Ph01 gate — 16 criteria /32 + 6 hard-fails
│   │   ├── high-level-system-design/  # produces solution-design.md + arch diagram
│   │   ├── epic-implementation-plan-compiler/  # FLAGSHIP — templates/ + rubrics/ + sections/
│   │   ├── adversarial-check-1/2/3/   # Loops A / B / C
│   │   └── ... (rfc, system-design-planner, task-author, red-test-author, etc.)
│   ├── hooks/                 # PostToolUse validators (EIP, RFC, story-tasks)
│   └── settings.json
├── docs/
│   ├── pilot-operating-model.md
│   ├── epic-implementation-plan-lifecycle.md
│   ├── stepstone-conventions/ # ingress-topology, compliance-framework, tech-radar, new-app-conventions
│   └── ...
├── mcp-servers/               # stonehenge-mcp (SQL catalogue), atlassian (Jira+Confluence)
├── scripts/                   # validators, repo cloning, env setup
├── tests/                     # fixtures + runner for the structural validators
└── .maister/knowledge/pdlc-ecosystem-context.md  # ecosystem map (skill/agent inventory)
```

## PDLC workflow (stages, gates, ownership)

11 phases. Each row: owner invokes primary skill; gate fires at the end. (Source: `README.md`, `CLAUDE.md`.)

| # | Phase | Owner | Primary skill | Gate / companion | Output |
|---|---|---|---|---|---|
| Ph00 | Initiative PRD (≡ SDP ticket) | PM | `prd` | "PRD Compliance Check" self-check | Initiative PRD (Confluence) |
| Ph01 | Feature PRD per capability (≡ Jira Epic) | PM + Tech Lead | `feature-prd` | `feature-prd-eval` | `feature-prd.md` |
| Ph02 | UI/UX → Figma Spec | Designer | `figma-design-spec` | `claude-design-agent` | `figma-spec.md` |
| Ph03 | Epic Implementation Plan | Tech Lead + PM | `epic-implementation-plan-compiler` | Loop A `adversarial-check-1`, pre-freeze `adversarial-check-2`, `baseline-freeze-prep` | `epic-implementation-plan.md` (draft→frozen) |
| Ph04 | Backlog Refinement → Stories | PM + Tech Lead | `user-story-author` | — | `stories/STORY-NNN-*.md` |
| Ph05 | Sprint Planning → Tasks | Tech Lead + PM | `task-author` → review → `adversarial-check-3` (Loop C) | `task-griller` | §3 Tasks in Story files |
| Ph06 | Test Authoring → Red Suite | QA + Eng | `red-test-author` | — | red test suite |
| Ph07 | Development → Feature PR (Green) | Engineer | `task-executor` | `tdd-loop` | Open PR on Stash |
| Ph08 | Review & Validation | Senior Eng | `independent-code-review` | `qa-exploratory` | Merged PR + triage |
| Ph09 | Deployment | Engineer | `release-orchestrator` (Bamboo) | `canary-watch` | Bamboo runbook |
| Ph10 | Verify & Operate → Loop D | SRE + Eng (PM+Analytics co-sign) | `verification-loop-d` | — | Loop D annotation on PRD |

**Design layer runs at the INITIATIVE tier, once per initiative, BEFORE any Epic** (Hard Rule #7): `system-design-planner` (ISD, L1–L2) → `rfc-author` (one RFC per ISD §3 component) → human accepts RFCs → `high-level-system-design` (architecture diagram + **solution-design.md**). The Epic compiler is **standalone** — it reads only the Feature PRD + its own L3–L5 discovery, NOT the ISD/RFCs.

**Four-loop adversarial model:** Loop A (Strategy↔Design, end of Ph03) · AC2 (Build Brief consistency, pre-freeze) · Loop C (Task completeness, Ph05 DoR gate) · Loop D (Hypothesis verification, Ph10). Findings are **soft gates** — never hard-block; user can re-draft or approve-with-acknowledgement (audit-trailed).

**Freeze gates (human-only):** Drafts are never auto-frozen. Human replies `freeze EIP` / `approve RFC-NNN` in chat; skill performs the mechanical file update. `implementation-prompt-writer` and `user-story-author` agents **refuse** unless `status: frozen`.

**Path scheme:** every artefact keyed `sandbox/<SDP-key>/<EPIC-key>/` (e.g. `sandbox/SDP-100/INTG-123/`). Initiative-tier artefacts (`isd/`, `rfcs/`, `hld/`) live under `sandbox/<SDP-key>/`.

---

## PRD template / schema (Ph00 — `prd/SKILL.md`)

17-section structure. Section headings verbatim:

1. **Header** — Status | Owner | Phase | Scope | Teams impacted
2. **TL;DR** (3 sentences: problem → solution → outcome)
3. **Problem Statement** (who affected · current experience · root cause · evidence · why now · implication)
4. **User & Intent** (target segment · JTBD · current failure · why they don't self-solve)
5. **Hypothesis** — "If we [X], then [metric Y] will change from [baseline]→[target], because [mechanism]." (one per PRD)
6. **Mechanism & Alternatives** (min 2 alternatives rejected with rationale)
7. **Success Metrics** (Primary / Secondary / Guardrails + measurement dependency)
8. **Non-Goals**
9. **Key Scenarios** (Happy path / Failure state / Edge case)
10. **Phase 1 Capabilities** (P0/P1/P2; organised by user capability not feature)
11. **Functional Requirements** (`FR-001:` numbered — behaviour, trigger, expected outcome, edge cases, dependencies, acceptance signal)
12. **Non-Functional Requirements** (`NFR-001:` numbered — requirement, target/threshold, why, validation method)
13. **Under Investigation**
*(numbering then repeats in source:)* **Key Decisions** (table) · **Dependencies** · **Risks & Mitigations** · **Open Questions** · **Execution & Rollout** (incl. kill condition) · **Measurement Plan** (incl. A/B spec)

Mandatory gates: STEP 0 (Strategy Doc gate, Scope Confirmation, Workflow-vs-Feature gate), STEP 1 (5 structural checks), **L7 Thinking Check**, and an appended **PRD Compliance Check** checklist.

## Feature PRD template / schema (Ph01 — `feature-prd/SKILL.md`)

**Feature PRD = Epic** (same layer). Two entry modes (mandatory choice): **A. Feature PRD Mode** (requires Initiative PRD + HLD) or **B. Discovery Mode** (10 discovery questions). Max 2 pages / 800–1000 prose words.

Section headings verbatim:
- **0. Thesis** (mandatory opening paragraph; L7 mechanism-first pattern)
- **1. Problem Definition** (3–4 bullets, one number each, cohort+timeframe+reconciliation required)
- **2. Goal & Success Metrics** (Primary/Secondary/Guardrail; mechanism-first selection; 5-component metric definition: definition, unit, calculation logic, dedup logic, time window)
- **2a. Decision Rules** (mandatory table: Metric | Read | Proceed | Iterate | Halt/Escalate)
- ...then Scope (in/out), Dependencies (team-level only), Key flows, Risks & assumptions, Measurement plan, Design reference, Tracking requirements (events verified via Stonehenge/Stash/Confluence — invented event names forbidden).

## Solution Design template / schema

There is **no standalone "Solution Design" template file**. "Solution Design" is the written output of the **`high-level-system-design` skill** → `hld/solution-design.md`, produced from accepted RFCs + ADRs. Document sections (from `high-level-system-design/SKILL.md` stage 5):
> **System Overview, Component Table, Data Flow, Key Decisions (from ADRs — decision made + rationale), Outstanding Decisions (RFC §11 items not yet closed — owner + gate condition), Risks and Dependencies.**

Hard rules: only `status: accepted` RFCs admitted; every diagram box cites an RFC; verified contracts (L4 `<repo:file:line>`) drawn solid, Proposed/unverified drawn dashed; output is always `status: draft` pending `approve HLD`.

### Upstream design artefacts (related schemas)

**Initiative System Design (ISD)** template (`initiative-system-design-template.md`) — YAML frontmatter fields: `initiative_id`, `derived_from` (`initiative_prd`, `solution_design`, `adrs`), `target_brands`, `generated_at`, `generated_by`, `project_mode` (`brownfield|greenfield|hybrid`). Sections: 1. Scope boundary · 2. NFRs (2a product / 2b enterprise / 2c platform-AI) · 3a. Imported PRD constraints · 3. Components requiring design (with `component_mode: existing|new`, decision-kind taxonomy: data model / API contract / UI / IaC / cross-cutting / ingress / scheduling) · 4. Open questions for RFC · 5. Known unknowns · 6. Adjacent out-of-scope · 7. Hints · 8. Cross-checks vs Stepstone conventions · 9. Stale L1 claims.

**RFC** template (`rfc-template.md`) — YAML frontmatter fields: `rfc_id`, `feature_id`, `component`, `status` (`draft|accepted|amended|superseded`), `tier` (1|2|3), `created`, `dependencies`, `creates_new_decisions`, `refines_existing`, `derived_from` (`isd`, `evidence_pack`, `isd_open_questions`), `isd_component_ref`, `component_mode`, `authored_by`, `accepted_at`, `accepted_by`. Sections: 1. Context/Problem · 2. Goals · 3. Non-Goals · 4. High-Level Architecture (mermaid required) · 5. Component Responsibilities · 6. Interface Contracts (6.1 inbound / 6.2 outbound / 6.3 persistence / 6.4 events / **6.5 Greenfield Design Decisions** — new components only) · 7. Recomputation/Triggers · 8. Observability · 9. Edge Cases · 10. Alternatives Considered (min 2) · 11. Open Questions Remaining · 12. Required ADRs · 13. Amendments.

## Epic Implementation Plan (Ph03) — YAML frontmatter + sections

Frontmatter keys (validated by `scripts/validate-epic-implementation-plan.sh`):
```yaml
status: draft           # draft | review | frozen
version: 1
derived_from: { prd, parent_prd, solution_design: [refs], adrs: [ids] }
generating_team:
release_owner:
target_brands: [DE, AT]
related_prd:
related_prd_url:
evidence_pack_id:
project_mode:           # brownfield | greenfield | hybrid
prompt_pack_path:       # set on freeze
story_pack_path:        # set on freeze
frozen_at:              # ISO-8601; required iff status: frozen
```
Required keys enforced: `status`, `version`, `derived_from`, `generating_team`, `release_owner`, `target_brands`, `related_prd`, `evidence_pack_id`; `status` enum; `frozen_at` when frozen.

14 modular section includes (`templates/sections/`): 01-decisions, 02-affected-repos, 03-frozen-contracts, 04-naming, 05-system-views, 06-implementation-breakdown, 07-implementation-guidance, 08-observability, 09-rollout-kill-plan, 10-release-ownership, 11-reviewers, 12-open-questions, 13-pr-self-test, 14-evidence-references.

## Tooling / schema files of note

- `templates/evidence-pack-schema.json` — Evidence Pack JSON shape (Stonehenge findings, repo-relevance, contract findings).
- `scripts/validate-{epic-implementation-plan,rfc,story-tasks,evidence-pack,diagrams}.sh` — structural linters; two wired as PostToolUse hooks in `.claude/settings.json`.
- `.claude-plugin/marketplace.json` — ships as a Claude Code marketplace plugin.
- MCP: `stonehenge-mcp` (SQL over the service catalogue, L3) + `atlassian` (Jira/Confluence, OAuth).
