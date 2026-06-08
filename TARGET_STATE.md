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

## 5. Atlassian / SDP skills → matd plugin, MCP-first

> **Deferred** to future spec `005-atlassian-sdp-skill-migration` (validate-first: StepStone's
> marketplace may already ship Jira/SDP MCP plugins — adopt before building). **Assumption going
> forward:** the `atlassian-write` MCP is **installed & running in each agent workspace** (a
> precondition, like Stash auth) — commands use it, they do not install/manage it.

The local corporate skills `stepstone-atlassian-skills` and `stepstone-sdp-planning` migrate into
the **matd Claude Code plugin**, restructured **MCP-first**:

- **Mechanism → the `atlassian-write` MCP** (sooperset `mcp-atlassian`, write-enabled, tested
  2026-06-08 against Cloud `stepstone.atlassian.net`): `jira_create_issue`, `jira_transition_issue`,
  `jira_update_issue`, `jira_create_remote_issue_link`, `jira_search`, `confluence_create_page`/
  `update_page`. **Drop** the old Python `.atlassian-venv`/`requests` patterns and DC/`vulcan` snippets.
- **Knowledge stays, but OSS-safe-split:** generic SDP/Atlassian *workflow logic* (the command/skill
  prose, status lifecycle, dual-linking, quarterly planning) can live in the OSS matd plugin;
  **StepStone-specific data** (custom-field ids, allowed-value ids, team UUIDs, Stonehenge domains,
  transition ids) **stays in the agent-workspace live config** (per the FR-055 scaffold pattern),
  **never** in the OSS marketplace.
- **Verified field facts to carry** (live createmeta 2026-06-08): Initiative type `11110`; required
  selects Stonehenge Domain `customfield_11259`, Initiative Category `customfield_11313`, Initiative
  Goal `customfield_11389`; Team `customfield_10001` (UUID, e.g. Mamba `f46fee6d-…-1425`); Target
  start/end `10022`/`10023`; Sprint `10020`; Story Points `10091`; create-default `To Do` (11092) →
  transition `101` → Idea Backlog (`11256`). Full reference: core repo `docs/references/sdp-jira-fields.md`.
- **Slim `stepstone-atlassian-skills`** (approved): drop Python-vs-MCP/venv/requests + generic CRUD;
  keep references (`custom_fields`, project structures, epic-linking, confluence markup) + best-practices.

## Open items
- Generic OSS-safe framework for the system-constitution skill (filled content stays private).
- `matd-ops` agent definition + permissions (bash/scripts/git allowed; no `.md`-prose authoring). *(Note: matd-ops dropped from PRD-command v1; may still be useful elsewhere.)*
- Migrate `stepstone-atlassian-skills` + `stepstone-sdp-planning` into the matd plugin (MCP-first, OSS-safe split — §5).
- Bundled SDP-creation flow via `atlassian-write` MCP (was: scripts extracted from `stepstone-sdp-planning`).
