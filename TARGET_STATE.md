# harness-tooling — Target State

**Status:** Draft · **Last Updated:** 2026-06-08 · **Owner:** Daniel Mingers

Target architecture for the MATD tooling shipped from this marketplace. Captures decisions made
during the DESIGN-stage command design (2026-06-08). The driving specs live in the **harness core
repo** under `docs/specs/001..003-*` and `docs/AGENT_SKILL_MATRIX.md`.

> **OSS-safe invariant:** This repo is the OSS marketplace. StepStone-specific content (EA
> principles, AWS accounts, internal endpoints, Confluence mirrors) **must not** live here — it
> belongs in private/local skills (`.claude/skills/stepstone-*`). Only generic, content-free
> frameworks are upstreamed here.

## 1. PDLC artefacts are SpecKit commands + shipped templates

The PLAYGROUND `agentic-pdlc-workspace` capabilities are **re-expressed as SpecKit commands
oriented around shipped templates**, not ported as bespoke skills/agents. Rationale: SpecKit
commands natively test structural compliance (`/checklist` "unit tests for English" + `/analyze`)
and resolve templates via the standard project→preset→extension→core layering. (Principle 7 of
spec 001.)

The MATD extension (`spec-kit-multi-agent-tdd`) grows **one command per DESIGN artefact**, each
with a template + a content-test compliance gate:

| Command | Artefact | Owner | Persistence | Template / schema |
|---|---|---|---|---|
| `speckit-matd-specify-product-brief` (enhance existing) | Product Brief (**business** invariants; business case as invariant) | Product | persistent | from Confluence **Product Charter** |
| `speckit-matd-specify-constitution` | System Constitution (**technical** invariants) | Tech/EA | persistent | compliance-checklist template |
| `speckit-matd-specify-prd` | PRD (**change request**) | Product | transient (archived) | `prd-schema.yml` |
| `speckit-matd-specify-solution-design` | Solution Design | Tech | per-change | alt. 9-section StepStone template |

**Three-input DESIGN model:** Solution Design = f(Product Brief, System Constitution, PRD).

## 2. MATD agent roster & skill re-scoping

Agents carry **role-specific** skills with minimal cross-role overlap, per
`docs/AGENT_SKILL_MATRIX.md` (core repo). **Shared general/baseline skills** (`general-rtk-usage`,
`general-verification-before-completion`, `context-optimization`, git skills) are **accepted
overlap**; only role-defining skills (`arch-*`, `dev-tdd`, `review-check-correctness`, …) are
de-duplicated.

| Agent | Role | Model | Notes |
|---|---|---|---|
| `matd-specifier` | Requirements/interview authoring | smart (Sonnet/Opus) | writes **`.md` only** |
| `matd-critical-thinker` | Red-team / content tests | smart | read-only |
| `matd-architect` | Solution design | smart | downstream |
| `matd-qa` | Test authoring/review | smart | downstream |
| `matd-dev` | Implementation | smart | downstream |
| **`matd-ops`** *(NEW)* | Mechanical: env, scripts, SDP/Stash/Jira | **Haiku** | blunt; no prose authoring |
| `matd-orchestrator` | Coordination | — | OpenCode-only |

**New `matd-ops` (Haiku):** owns deterministic plumbing (scaffolding, index maintenance, SDP
creation, Stash commit/push, Jira remote-links). Keeps token cost low and protects authored
content from mechanical agents. The smart interviewer never runs scripts; the blunt ops agent
never writes prose.

## 3. Two-tier plugin model

- **`harness-matd-core`** — always installed (~15 must-have skills: verification, rtk, git
  guardrails, context-optimization, writing-plans, dev-tdd, check-correctness, orchestration,
  grill).
- **`harness-matd-extensions`** — opt-in specialty skills (all `arch-*`, `python-*`, most
  `review-*`/`dev-*`, `file-ops-*`, `manage-*`).

Both ship the same agents; agent files declare required skills. (See `docs/AGENT_SKILL_MATRIX.md`.)

## 4. Token-efficiency & V-model

- Deterministic shell/python plumbing (SpecKit `setup-*.sh` pattern) vs. LLM only for
  authoring/grill; progressive disclosure; output caps.
- V-model: every left-side artefact has a right-side content test; self-documenting hierarchical
  traceability IDs (`PRD-NNN → SPEC-NNNN → STORY/TASK`), permanent (deprecate, never renumber).
- Per-step agent assignment via the `spec-kit-agent-assign` pattern (`agent-assignments.yml`,
  assign→validate→execute).

## Open items
- Generic OSS-safe framework for the system-constitution skill (filled content stays private).
- `matd-ops` agent definition + permissions (bash/scripts/git allowed; no `.md`-prose authoring).
- Bundled SDP-creation scripts (extracted from `stepstone-sdp-planning`).
