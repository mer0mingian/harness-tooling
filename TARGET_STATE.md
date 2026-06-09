---
type: target-state
created: "2026-06-09"
owner: "Daniel Mingers"
---

# harness-tooling — Target State

Target architecture for the MATD tooling shipped from this marketplace. Captures decisions surfaced
during the DESIGN-stage command design (2026-06-08). The driving specs live in the **harness core
repo** under `docs/specs/001..004-*` and `docs/AGENT_SKILL_MATRIX.md`.

> **OSS-safe invariant:** This repo is the OSS marketplace. StepStone-specific content (EA
> principles, AWS accounts, internal endpoints, Confluence mirrors) **must not** live here — it
> belongs in private/local skills (`.claude/skills/stepstone-*`). Only generic, content-free
> frameworks are upstreamed here.

## Status

DESIGN-stage command implementation status:

| Spec | Command | Status |
|---|---|---|
| 001 | `speckit-matd-specify-prd` | **In progress** |
| 002 | `speckit-matd-specify-product-brief` | Stub |
| 003 | `speckit-matd-specify-constitution` | Stub |
| 004 | `speckit-matd-specify-solution-design` | Stub |

---

## 1. MATD Agent Skill Re-scoping

**Current problem:** Agent files in `.agents/plugins/matd/agents/` over-share role-specific skills
beyond what is appropriate per role — `dev-tdd`, `review-check-correctness`, `stdd-openspec`, and
`general-system-design` appear across agents that should not carry them.

**Target state** per `docs/AGENT_SKILL_MATRIX.md` (core repo):

| Agent | Role-defining skills | Excluded |
|---|---|---|
| `matd-specifier` | `general-grill-me`, `general-grill-with-docs`, `arch-writing-plans`, `stdd-product-spec-formats` | `dev-tdd`, `review-*` |
| `matd-critical-thinker` | `review-check-correctness`, `general-grill-me`, `general-grill-with-docs`, `review-simplify-complexity`, `review-systematic-debugging`, `review-differential-review`, `general-improve-codebase-architecture`, `review-orchestrate-dual-review` | `dev-tdd`, `stdd-openspec` |
| `matd-architect` | `arch-c4-architecture`, `arch-architecture-patterns`, `arch-api-design-principles`, `arch-mermaid-diagrams`, `arch-design-system-patterns`, `arch-smart-docs`, `general-system-design`, `general-solid`, `general-improve-codebase-architecture`, `review-simplify-complexity`, `arch-writing-plans`, `dev-database-migration`, `docker-expert` | `dev-tdd`, `review-check-correctness` |
| `matd-dev` | `dev-tdd`, `dev-databases`, `dev-database-migration`, `dev-backend-to-frontend-handoff`, `dev-diagnose`, `dev-mobile-android-design`, `dev-alpine-js-patterns`, `python-*`, `general-solid`, `arch-api-design-principles`, `filesystem-context`, `file-ops-*`, `docker-expert` | `review-check-correctness`, `arch-c4-architecture` |
| `matd-qa` | `review-check-correctness`, `review-systematic-debugging`, `review-differential-review`, `review-e2e-testing-patterns`, `review-webapp-testing`, `review-orchestrate-dual-review`, `dev-tdd`, `dev-diagnose`, `python-*`, `python-testing-uv-playwright` | `arch-*`, `stdd-openspec` |
| `matd-orchestrator` (OpenCode-only) | `orchestrate-subagent-driven-development`, `orchestrate-dispatching-parallel-agents`, `orchestrate-executing-plans`, `orchestrate-multi-agent-patterns`, `manage-*`, `update-config`, `arch-writing-plans`, `context-degradation`, `context-compression` | — |

**Shared baseline skills** accepted as overlap across all roles (do not de-duplicate):
`general-rtk-usage`, `general-verification-before-completion`, `context-optimization`,
`context-fundamentals`, `general-git-advanced-workflows`, `general-git-guardrails-claude-code`,
`brainstorming` (universal pre-artefact skill — any role that authors a new artefact should
ideally explore intent before writing; kept in the baseline so it does not need to be listed
per-role and does not create false "cross-role overlap" findings).

**Two-tier plugin model:**

- **`harness-matd-core`** — minimal baseline shared by all MATD roles (~13 skills): verification,
  rtk, git guardrails, git advanced, context-optimization, arch-writing-plans, dev-tdd,
  review-check-correctness, orchestration (3 skills), grill-me, grill-with-docs.
- **`harness-matd-extensions`** — role-specific packs loaded opt-in:
  - `specifier-pack`: `stdd-product-spec-formats` (`brainstorming` is in shared baseline)
  - `critic-pack`: `review-simplify-complexity`, `review-systematic-debugging`, `review-differential-review`, `review-orchestrate-dual-review`, `general-improve-codebase-architecture`
  - `architect-pack`: `arch-*`, `general-system-design`, `general-solid`, `dev-database-migration`, `docker-expert`
  - `dev-pack`: `python-*`, `dev-*`, `file-ops-*`, `filesystem-context`, `general-solid`, `arch-api-design-principles`
  - `qa-pack`: `review-e2e-testing-patterns`, `review-webapp-testing`, `python-testing-uv-playwright`
  - `orchestrator-pack`: `manage-*`, `update-config`, `context-degradation`, `context-compression`

Both plugins ship the same 6 agent definitions; agent files declare their required skills.
See `docs/AGENT_SKILL_MATRIX.md` in the core repo for the authoritative per-skill assignment.

---

## 2. DESIGN-Stage Commands as SpecKit Commands + Templates

The PLAYGROUND `agentic-pdlc-workspace` capabilities are **not** ported as bespoke skills or agent
definitions. They are **re-expressed as SpecKit commands** (`.md` command files in
`spec-kit-multi-agent-tdd/commands/`) **paired with shipped templates**.

**Commands to build (in order):**

| # | Command | Artefact | Owner | Persistence | Template/schema |
|---|---|---|---|---|---|
| 1 | `speckit-matd-specify-prd` | PRD (change request) | Product | transient (archived) | `prd-schema.yml` |
| 2 | `speckit-matd-specify-product-brief` | Product Brief (business invariants) | Product | persistent | Confluence Product Charter |
| 3 | `speckit-matd-specify-constitution` | System Constitution (technical invariants) | Tech/EA | persistent | compliance-checklist template |
| 4 | `speckit-matd-specify-solution-design` | Solution Design (StepStone 9-section) | Tech | per-change | alt. 9-section StepStone template |

**Three-input DESIGN model:** Solution Design = f(Product Brief, System Constitution, PRD).

**Each command follows the same pattern:**

- `templates/` — shipped default template (project-override wins via standard SpecKit resolution order)
- `prompts/` or inline — grill prompts per section
- `scripts/` — deterministic validator (content-test; structural checks only; exit non-zero on CRITICAL)
- `commands/` — command orchestration (calls scripts for mechanics; invokes smart agents for authoring/review)

**Content-test compliance gate:** each command ships a validator that is the "right side of the
V-model" for its artefact. Deterministic (structural/regex) gates block; LLM-judgment review
is advisory. SpecKit's native `/checklist` ("unit tests for English") and `/analyze`
(cross-artifact consistency) are the canonical test entry points.

---

## 3. Design Principle 7 — PDLC Artefacts as SpecKit Commands

> PDLC artefacts (PRD, Solution Design, RFC, Epic Implementation Plan, etc.) are realised as
> **SpecKit commands + shipped templates**, not as copied skills or bespoke agent definitions.
> SpecKit commands are natively suited to testing document structure compliance via `/checklist`
> (unit tests for English) and `/analyze` (cross-artifact consistency). Templates ship as the
> standard SpecKit feature (project-override → preset → extension → core resolution order).
> The MATD extension grows one command per artefact.

This principle governs all future DESIGN-stage additions. Any capability from the PLAYGROUND
`agentic-pdlc-workspace` is adopted as a SpecKit command, not as a skill or agent clone.

---

## 4. Future: spec-kit-agent-assign Pattern (deferred)

The `agent-assignments.yml` + assign/validate/execute machinery (from the `spec-kit-agent-assign`
reference implementation) is documented as a **future option** once multiple DESIGN-stage commands
share the wiring. It is **not implemented in v1** of any command.

In v1, commands call deterministic scripts directly for mechanical steps; only two smart agents
are involved per command (e.g. `matd-specifier` for authoring, `matd-critical-thinker` for review).
The orchestration engine would remove per-command wiring duplication once ≥2 commands prove out
the pattern.

Reference implementation: `docs/references/spec-kit-agent-assign-summary.md` in the core repo.

---

## Open Items

> Implementation status is tracked in the **Status table** at the top of this file.
> No duplicate list is maintained here to avoid divergence.
