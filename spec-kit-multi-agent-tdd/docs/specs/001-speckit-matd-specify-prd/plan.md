---
type: plan
feature_id: "001-speckit-matd-specify-prd"
title: "Implementation Plan — speckit-matd-specify-prd"
status: draft
created: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
spec: ./spec.md
---

# Implementation Plan: `speckit-matd-specify-prd`

> ## ⚠️ v1 scope amendment (2026-06-08) — supersedes conflicting detail below
> Per critical review + user decisions, v1 is **lean (~20–24 SP)**. Where this amendment and the
> detailed plan below disagree, **this wins**. See spec §"v1 scope (MVP) & risk register".
>
> **Cut from v1:** the `matd-ops` Haiku agent (→ command calls scripts directly), `agent-assignments.yml`
> + assign/validate/execute, the multi-agent build-wave/orchestration, the alternative Solution Design
> template (→ [spec 004](../004-speckit-matd-specify-solution-design/spec.md)), automated Stash push (→ human pushes).
>
> **Kept:** SDP-key write-back; full `index.yml` (`specs[]` + archival lifecycle); the archived-specs folder schema.
>
> **Changed:** SDP creation via the **`atlassian-write` MCP** (sooperset `mcp-atlassian`, tested
> 2026-06-08 against live Cloud `stepstone.atlassian.net`): `jira_create_issue` → `jira_transition_issue`
> (id 101 → Idea Backlog 11256) → `jira_create_remote_issue_link`; auth via env token (not code).
> REST+token is fallback. (Earlier "REST not MCP" note superseded — that was the *official* MCP.)
> structural validator is **advisory** in v1; ship a **Jira config scaffold** in the marketplace while
> the **live per-team config lives in the agent workspace only** (OSS-safe).
>
> **Build order (single builder, sequential — no parallel wave):** thin `prd-schema.yml` → command
> (grill + render + PRD-NNN/index) → advisory validator + eval rubric → SDP REST script
> (create+transition, gated on OQ-11a Cloud-URL confirmation) → local commit + remote-link + write-back
> (human push). Two smart agents only: `matd-specifier` (authoring, .md), `matd-critical-thinker` (review).

> Generated via the `/speckit-plan` workflow, adapted to this repo's `docs/specs/` layout.
> The standard SpecKit `setup-plan.sh` / `.specify/` scaffolding is **not present in this core
> repo** (it lives inside the consumed workspaces), so the plan is written directly against the
> SpecKit plan-template structure. **No new git branch created — stays on `dev`** per task scope.

## Summary

Deliver a new MATD SpecKit command, `speckit-matd-specify-prd`, that runs a **scripted,
schema-driven** interview to produce a **change-request PRD** and (optionally, on explicit
confirmation) creates a linked **SDP initiative** in the "Idea Backlog" status, persisting the
PRD + its context file to the system's agent-workspace repo on Stash.

Core technical approach (Design Principle 1 — scripted/LLM split):
- **Deterministic shell/python** does plumbing: PRD-NNN allocation, schema parse, scaffolding,
  content-test linting, SDP create + transition, Stash commit, remote-link, index maintenance,
  SDP-key write-back.
- **The LLM authors only** the interview answers → `prd.md` + `prd-context.md` (`.md`-only).
- Steps are mapped to **distinct-skillset MATD agents** via `agent-assignments.yml`, introducing a
  new Haiku **`matd-ops`** agent for mechanical work and confining the smart **`matd-specifier`**
  to `.md` authoring, with **`matd-critical-thinker`** running read-only content tests.

## Technical Context

| Aspect | Decision |
|---|---|
| **Command location** | `submodules/harness-tooling/spec-kit-multi-agent-tdd/commands/specify-prd.md` (FR-001) |
| **Schema** | `prd-schema.yml` shipped in extension `templates/`; workspace `.specify/prd-schema.yml` overrides (FR-002/003) |
| **Languages** | Bash + Python 3 (Atlassian/Stash calls, YAML parse) — matches existing `scripts/*.py` in the extension |
| **PRD layout** | File-based, no per-PRD folder: `product/prd/PRD-NNN-<slug>.md` + `index.yml`; context in `product/context/PRD-NNN-<slug>.context.md` (OQ-3/9) |
| **SDP target status** | Create as Initiative (type id `11110`) → land in "To Do" (`11092`) → transition id `101` → "Idea Backlog" (`11256`). Re-resolve transitions at runtime via `GET /issue/{key}/transitions` (FR-051) |
| **Link mechanism** | Phase-A: Jira remote/web link to PRD on Stash (`POST .../remotelink`) + URL in description; abstracted for later swap to custom field (Phase-B) (OQ-4/FR-054) |
| **Agents** | `matd-ops` (NEW, Haiku), `matd-specifier` (smart, `.md`-only), `matd-critical-thinker` (read-only) (FR-041/041a) |
| **Reused-as-scripts** | SDP-creation logic extracted from `stepstone-sdp-planning` + `stepstone-atlassian-skills` into bundled scripts, NOT skill-invocation (FR-043) |
| **Config inputs** | `jira-teams-config.yaml`, `references/sdp-custom-fields.md` (FR-052) |
| **Constitution** | Reference-only at `architecture/system-constitution.md`; never regenerated (FR-010, OQ-5) |
| **NEEDS CLARIFICATION** | None in spec 001 — all OQ-1..10 resolved. Residual unknowns belong to downstream stubs 002/003 and external deps (see Complexity Tracking) |

## Constitution Check

Evaluated against this repo's architectural invariants (CLAUDE.md) — there is no `.specify/memory/constitution.md`
in the core repo; these are the binding gates.

| Gate | Status | Note |
|---|---|---|
| **OSS-safe marketplace** (NFR-003) | ✅ PASS | Command + schema + content-test + eval rubric + `matd-ops` agent are OSS-safe and live in `harness-tooling`. **StepStone-specific SDP scripts, `jira-teams-config.yaml`, `sdp-custom-fields.md` stay in private/gitignored skills** — bundled scripts must read corp config from the private side, not embed it. |
| **Code bind-mounted, not copied** | ✅ PASS | No image changes; command operates on bind-mounted workspace. |
| **Skills referenced, not duplicated** | ⚠️ JUSTIFIED | FR-043 deliberately **extracts SDP logic as scripts** (reuse-as-scripts) rather than invoking the skill — for token-cost + self-containment. Tracked in Complexity Tracking. Source-of-truth remains the skill; scripts are a vendored, OSS-safe-shaped copy of the *mechanism*. |
| **Local-first, docker-compose** (NFR-004) | ✅ PASS | No infra changes. |
| **Human gate preserved** | ✅ PASS | SDP creation offered-not-automatic (FR-050); content-test override is audit-trailed (FR-032). |
| **Backend-cloud / no UI** | ✅ PASS | PRD schema forbids screens/service-names/schemas. |

**Post-design re-evaluation:** unchanged — the reuse-as-scripts exception is the only deviation and is justified by FR-043/FR-060 (token cost). No new violations introduced by the design.

## Project Structure

### Artifacts produced by this plan
```
docs/specs/001-speckit-matd-specify-prd/
├── spec.md                  # (exists, frozen)
├── plan.md                  # THIS FILE
├── dependency-map.md        # task graph + parallelization plan
└── (tasks.md)               # produced later by /speckit-tasks
```

### Implementation footprint (where the work lands)
```
submodules/harness-tooling/spec-kit-multi-agent-tdd/
├── commands/
│   └── specify-prd.md                       # FR-001  the command (T-CMD)
├── templates/
│   ├── prd-schema.yml                       # FR-003  schema SSOT (T-SCHEMA)
│   ├── sdp-initiative-template.yml          # FR-007  payload field-map (T-SDPTMPL)
│   └── solution-design-alt-template.md      # alt 9-section SD template (T-SDTMPL)
├── scripts/
│   ├── validate_prd_content.py              # FR-030  deterministic content test (T-VALIDATOR)
│   ├── allocate_prd_id.py                    # FR-008  PRD-NNN allocation (T-INDEX)
│   ├── maintain_prd_index.py                 # FR-009  index.yml maintenance (T-INDEX)
│   └── sdp/                                  # FR-043  bundled SDP scripts (T-SDPSCRIPTS)
│       ├── create_sdp_initiative.py          #   create + transition→Idea Backlog
│       ├── link_prd_to_sdp.py                #   remotelink + writeback (T-STASH/T-LINK)
│       └── commit_prd_to_stash.sh            #   git commit/push to workspace repo
├── prompts/ (or commands inline)
│   └── prd-eval-rubric.md                   # FR-031  LLM eval rubric (T-RUBRIC)
└── .agents/plugins/matd/agents/
    └── matd-ops.md                          # FR-041a  NEW Haiku agent (T-OPSAGENT)

docs/specs/001-speckit-matd-specify-prd/
└── agent-assignments.yml                    # FR-040  step→agent map (T-ASSIGN)
```
*(Exact `prompts/` vs inline placement to be confirmed against extension conventions during T-CMD.)*

## Phases

### Phase 0 — Research (resolved)
All research questions from the spec are **resolved (OQ-1..10)**. No `research.md` regeneration
needed. Key carried-forward decisions: official StepStone FR/NFR ownership (SD, not PRD);
Idea-Backlog via transition `101`; file-based PRD layout; remote-link → custom-field migration
path; per-workspace constitution reference-only; 4-step agent map with new `matd-ops`.

Residual research belongs to **downstream stubs** (not this plan):
- Spec 002 OQ-B1..B4 (project-brief schema) — does not block 001.
- Spec 003 OQ-C1..C6 + **EA-Maps pending input** — does not block 001.

### Phase 1 — Design & Contracts
Defines the contracts the command exposes:
- **Schema contract** (`prd-schema.yml`): sections, `id_prefix`, `required`, `grill_prompts[]`,
  `validation_rules[]`. Drives both interview and validator (interpretation A).
- **Index contract** (`index.yml`): `next_prd_seq` + `prds.<PRD-NNN>{slug,sdp_key,status,path,stash_url,specs[]}`.
- **SDP payload contract** (`sdp-initiative-template.yml` → JSON): fields per `sdp-custom-fields.md`.
- **CLI contract**: validator exit-non-zero on CRITICAL (FR-030); abstracted link step (FR-054).
- **Agent contract**: `agent-assignments.yml` (`assign`→`validate`→`execute`), distinct skillsets
  per AGENT_SKILL_MATRIX (shared baseline skills accepted overlap).

### Phase 2 — Task breakdown & parallelization
See [dependency-map.md](./dependency-map.md) for the discrete tasks, Mermaid dependency graph,
parallelization plan, and agent-role mapping. (This is the deliverable of this exercise; full
`tasks.md` with TDD ordering is generated later by `/speckit-tasks`.)

## Complexity Tracking

| Item | Why it adds complexity | Justification / mitigation |
|---|---|---|
| **Reuse-as-scripts (FR-043)** vs skill-invocation | Vendored copy of SDP-creation logic; risk of drift from `stepstone-sdp-planning` | Justified by FR-060 token cost + self-containment; keep scripts thin, cite skill as source-of-truth, OSS-safe shape (corp config stays external) |
| **New `matd-ops` Haiku agent** | New agent file + AGENT_SKILL_MATRIX wiring + plugin tiers | Justified by FR-041a cost separation (Haiku plumbing) + content protection (specifier `.md`-only) |
| **Two-document split** (`prd.md` + `prd-context.md`) | Two artifacts to keep in sync | Justified by FR-006/OQ-9 (terse PRD, depth in context); both committed together |
| **Link mechanism abstraction** (A→B) | Indirection now for a future swap | Justified by OQ-4; **blocked external dep**: custom field not yet provisioned by Atlassian team |
| **Runtime transition-id resolution** | Cannot hard-code `101` | Justified by FR-051 (workflow ids change) — script calls `GET .../transitions` |

### Blocked by open decisions / external deps (NOT in this plan's critical path)
- **Atlassian custom field** (link mechanism Phase-B) — external; Phase-A remote-link ships now.
- **EA-Maps content** (spec 003) — pending from Daniel; only affects constitution command, not PRD.
- **`submodules/harness-tooling/TARGET_STATE.md`** (OQ-7) — agreed to create; migration of MATD
  agent re-scoping is a parallel cross-repo doc task, not a code dependency for the command.
