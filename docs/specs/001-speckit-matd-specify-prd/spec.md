---
type: spec
feature_id: "001-speckit-matd-specify-prd"
title: "speckit-matd-specify-prd — PM-facing PRD command for the MATD SpecKit extension"
status: draft
created: "2026-06-08"
owner: "Daniel Mingers"
branch: dev
---

# Spec: `speckit-matd-specify-prd`

A new command in the **MATD SpecKit extension** (`spec-kit-multi-agent-tdd`) for **Product
Managers**. It runs a scripted, schema-driven interview to produce a **Product Requirements
Document (PRD)** for a *change request*, then creates a linked **SDP initiative** in
"Ideation" status and persists the PRD to the agent workspace and Stash.

This spec consolidates the research and grilling session of 2026-06-08. Sources:
[architecture-designs-confluence.md](../../references/architecture-designs-confluence.md),
[agentic-pdlc-workspace-summary.md](../../references/agentic-pdlc-workspace-summary.md),
[AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md), the PLAYGROUND
`agentic-pdlc-workspace` and `spec-kit-agent-assign` repos (cloned under
`submodules/watching/`, gitignored).

---

## What & Why

StepStone's product org is introducing an explicit **"DESIGN" stage between Planning and
Develop**, composed of two artifacts with clear ownership:

| Artifact | Owner | Question | Content |
|---|---|---|---|
| **PRD** | Product | *What* we're building and why — testable | Problem framing · Goals & non-goals · Success metrics w/ measurement · User workflows & outcomes (not features) · Explicit scope in/out. **No screens, no service names, no schemas.** |
| **Solution Design** | Tech | *How* we deliver it — frozen baseline | FR + NFR · Architecture decisions (ADRs) · Service boundaries/interfaces/data model · Target architecture · Dependencies/risks/costs · C4 diagrams · LLD where critical |

PRD + Constitution (system invariants) → feed **Solution Design** → feed **specs** (vertical
slices / milestones that unlock value or downstream work). Focus is **backend development in
the cloud**.

Today this stage is unsupported in the MATD extension. The PLAYGROUND `agentic-pdlc-workspace`
proves the concept but is **token-heavy and LLM-driven**. This command delivers equivalent
value but **more scripted (lower token cost), more structure-oriented (yml-defined schema +
content tests), and with distinct-skillset agents assigned per step** — together raising
multi-agent reliability for development.

**PRD = change request, not product business case.** It overlaps the existing
[product-brief](../../../submodules/harness-tooling/.speckit-templates/specs/product-brief-template.md)
but orients on the *goal of the change*, not the product's own goal. A change may introduce
new success criteria, new features, or be purely technical.

## Business Value

- Closes the "DESIGN" gap so PM intent flows reliably into tech delivery.
- Lower token consumption per PRD vs. the PLAYGROUND pipeline (scripted plumbing + schema-driven prompts).
- Higher agent reliability via the V-model: every left-side artifact has a right-side content test.
- Traceability `PRD ↔ Solution Design ↔ epics ↔ stories` (the ProductOps scorecard).
- Reusable team template (the project's overarching goal).

## Measurability / Success Criteria

- **SC-001:** A PM completes a PRD end-to-end via the command without hand-editing yml.
- **SC-002:** PRD content passes the deterministic content-test validator (see FR-030) with zero CRITICAL findings before SDP creation is offered.
- **SC-003:** Token usage for a representative PRD run is materially lower than the PLAYGROUND `prd` skill for the same input — **target ≥40% reduction** (scripted plumbing; LLM authoring only). To validate empirically once implemented.
- **SC-004:** Created SDP initiative lands in **"Ideation"** status with the PRD's Stash URL linked.
- **SC-005:** The two smart agents (`matd-specifier` authoring, `matd-critical-thinker` review) carry role-appropriate skillsets per [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md); mechanical steps run as scripts invoked by the command. No agent-assignment engine in v1.

## Goals & No-goals

### Goals
- A `speckit-matd-specify-prd` command producing a markdown PRD from a **yml schema** (`prd-schema.yml`) that defines sections, required fields, numbered-item prefixes, grill prompts, and validation rules.
- A **Constitution** integration (referenced as system invariants; gates downstream).
- Scripted SDP-initiative creation via **Jira MCP** (auth at MCP/SDP level) into **Idea Backlog**, reusing `stepstone-sdp-planning` / `stepstone-atlassian-skills` logic as bundled scripts.
- PRD committed to the workspace folder structure and pushed to Stash (working auth assumed; human pusher); source PRD linked to its SDP initiative.
- **Content tests** ("unit tests for English") + **V-model** verification orientation.
- _(The **alternative Solution Design template** moved to a dedicated future spec — see [004 solution-design](../004-speckit-matd-specify-solution-design/spec.md). It is **not** part of this command.)_

### No-goals
- Authoring the Solution Design or specs themselves (this command stops at PRD + SDP initiative; it *prepares* inputs for them).
- Replacing the product-brief command.
- Frontend/UI design specifics (backend-cloud focus).
- Auto-freezing or auto-approving any artifact (human gate, per MATD/PLAYGROUND Hard Rule).

---

## Design Principles (derived from research)

1. **Scripted/LLM split (SpecKit model).** Deterministic shell/python does plumbing — path
   resolution, scaffolding, schema parsing, content-test linting, SDP creation, Stash commit.
   The LLM does *only* the interview and section authoring. (Mirrors SpecKit `setup-*.sh` +
   `check-prerequisites.sh` emitting JSON; content generation stays with the model.)
2. **Structure via yml.** `prd-schema.yml` is the single source of truth for PRD structure
   (interpretation **A**: schema drives the interview *and* validation; markdown is the
   rendered output). Workspace-local override (`.specify/prd-schema.yml`) wins over the
   shipped default.
3. **Content tests = "unit tests for English."** Adopt SpecKit `/checklist` + `/analyze`
   concepts and the PLAYGROUND `feature-prd-eval` model (7 hard-fail checks + 16-criterion
   /32 rubric). Deterministic validator + LLM eval rubric. This is the V-model's right side
   for the PRD.
4. **V-model.** Each left-side artifact maps to a right-side verification: PRD → content-test
   + falsifiable hypothesis (If/Then/Because, baseline B → target T, timeframe W) verifiable
   post-deploy; Solution Design → design-consistency check; specs → acceptance tests. Maintain
   `PRD ↔ SD ↔ epics ↔ stories` traceability IDs.
5. **Two smart agents + scripts (v1 — no orchestration engine).** `matd-specifier` authors
   (`.md` only), `matd-critical-thinker` reviews (read-only); mechanical steps are plain scripts
   the command invokes. No `agent-assignments.yml`, no assign/validate/execute machinery (deferred
   until a second command shares the wiring). Agents carry role-appropriate skills per
   [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md); shared general/baseline skills are accepted
   overlap. (The `spec-kit-agent-assign` pattern remains a documented future option in TARGET_STATE.)
6. **Progressive disclosure / token caps.** Load only the schema section in play; cap validator
   output rows; cite verbatim only contracts/names.
7. **PDLC artefacts as SpecKit commands, not ported skills/agents.** The PLAYGROUND
   `agentic-pdlc-workspace` capabilities (PRD, Solution Design, RFC, Epic Implementation Plan,
   etc.) are **re-expressed as SpecKit commands oriented around shipped templates**, not copied
   as bespoke skills/agent definitions. Rationale: SpecKit commands are better suited to
   **test compliance with document structure** (native `/checklist` "unit tests for English" +
   `/analyze` cross-artifact checks) and orient around **templates that ship as a standard
   SpecKit feature** (project-override → preset → extension → core resolution). This command
   (`speckit-matd-specify-prd`) is the first such artefact; the rest follow the same pattern.

---

## Components & Artifacts

### Key Entities
- **`prd-schema.yml`** — section/field definitions, `id_prefix` per numbered list, `required` flags, `grill_prompts[]`, `validation_rules[]`. Shipped in the extension; workspace-overridable.
- **PRD markdown** — rendered output (template-structured), committed to the workspace + Stash.
- **PRD additional-context file** (`product/context/PRD-NNN-<slug>.context.md`) — captures the
  **extended shared design context** the grill surfaces *beyond* the template slots (rationale,
  discarded options, domain detail, constraints). Lives in a **central `product/context/` folder**
  (one file per PRD) so context is searchable in one place and the PRD needs **no folder of its
  own**. The H1 title and frontmatter name the **PRD id + created/updated dates**. The structured
  `prd.md` stays **short and concise**; depth lives here. Committed to Stash alongside the PRD.
- **SDP template file** (`sdp-initiative-template.yml`) — a field template that maps directly
  to the **JSON payload** for creating the SDP Jira ticket. Used by the optional SDP side-task.
- **Traceability index** (`product/prd/index.yml`) — machine-maintained single source of truth
  for the artefact mappings. Schema: `next_prd_seq` + `prds.<PRD-NNN>` with `slug`, `sdp_key`
  (1:1), `status`, `path`, `stash_url`, and `specs[]` (1:many — each `{spec_id, epic_key, path}`,
  `epic_key` 1:1 with the spec). Updated by scripts, never hand-edited. Tasks/Stories (1:many)
  live under each spec, not in this index.

### Artefact cardinality & ID lifecycle
```
PRD ──1:1── SDP            (internal PRD-NNN  ↔  SDP-key)
 └─1:many─► Spec ──1:1── Epic   (internal SPEC-NNNN  ↔  Epic-key)
              └─1:many─► Task/Story
```
IDs are **permanent** (never renumbered; deprecate only — v-model rule). Lifecycle:
1. PRD creation → allocate stable **`PRD-NNN`** (SDP key not yet known).
2. SDP creation → bind `PRD-NNN ↔ SDP-key` (1:1) in index + PRD frontmatter.
3. Solution design → derive **`SPEC-NNNN`** ids (1:many under the PRD). *(downstream command)*
4. After solution design → each spec gets its **Epic-key** (1:1) on Jira Epic creation. *(downstream)*

This command owns steps 1–2 and initialises the index; it reserves (does not fill) `specs[]`.
IDs (`PRD-NNN`) are stable, assigned first, never renamed to the SDP key.

### Workspace layout (file-based — PRDs need no folder)
```
product/
├── brief.md                          # persistent business invariants
├── prd/
│   ├── PRD-001-<slug>.md             # concise PRD (one file)
│   ├── PRD-001-<slug>.sdp.json       # optional rendered SDP payload (FR-007)
│   ├── index.yml                     # traceability index
│   └── _archive/                     # archived PRD files (numbering retained)
└── context/
    └── PRD-001-<slug>.context.md     # central additional-context store (one per PRD)
```

### Persistence vs archival
- **Persistent (long-lived, evolve with the product):** `product/brief.md` (product brief) and the **system constitution** (`architecture/system-constitution.md`). Never archived.
- **Archived on completion:** PRDs and specs. On completion, move `product/prd/PRD-NNN-<slug>.md` (+ its `.sdp.json`) → `product/prd/_archive/` and `product/context/PRD-NNN-<slug>.context.md` → a context archive (specs → existing `specs_archive/`), set the index entry `status: archived`/`done` with updated `path`. **Numbering remains** — sequences are monotonic; archived IDs never reused (v-model permanence). The index keeps archived entries.
- **Constitution** — system invariants (SpecKit `constitution-template.md` shape); referenced, not regenerated; gates Solution Design.
- **Jira config scaffold** — a placeholder config shipped in the marketplace; the **live, per-team config lives in the agent workspace only** (never in the marketplace). See FR-055.
- **SDP initiative** — Jira `SDP` project Initiative, created then transitioned to **"Idea Backlog"**, linked to the PRD Stash URL.

### Proposed PRD schema sections (change-request oriented)
Synthesised from the screenshot's PRD definition + PLAYGROUND `prd`/`feature-prd`, minus
product-business-case repetition:

1. **Header** — change_id, title, owner (Product), status, `initiative_link` (SDP key once created), `parent_product_brief` (optional), teams_impacted, created/updated
2. **TL;DR** — problem → change → outcome (3 sentences)
3. **Problem Framing** — who's affected, current experience, evidence, why now
4. **Goals & Non-Goals**
5. **Hypothesis** — If/Then/Because with baseline B, target T, timeframe W (falsifiable)
6. **Success Metrics** — primary / secondary / guardrail, each with measurement method + baseline or TBC plan (who/when/instrumentation)
7. **User Workflows & Outcomes** — *not* features; no screens/service-names/schemas
8. **Scope In / Scope Out** — explicit
9. **Outcome-level Requirements (OPTIONAL)** — `REQ-NNN` at capability level. The PM *may* provide these if they choose; full FR/NFR are **not** PRD content (they are required in the Solution Design — see OQ-1 resolution). PRD stays at user-workflows/outcomes with no service names or schemas.
10. **Risks & Assumptions**
11. **Dependencies** — team-level
12. **Open Questions**
13. **Rollout & Kill Condition**

> _The alternative Solution Design template (StepStone 9-section structure + 13 NFR categories) is
> **out of scope for this command** and fully specified in [004 solution-design](../004-speckit-matd-specify-solution-design/spec.md)._

---

## Three-input DESIGN model & companion commands

Unlike the standard SpecKit flow (constitution + spec), StepStone's org complexity requires
**three persistent/transient inputs to generate a Solution Design**:

| Input | Captures | Persistence | Owning command | Confluence reference |
|---|---|---|---|---|
| **Product Brief** | **Business** invariants (vision, scope, value, governance, budget) | Persistent | `speckit-matd-specify-product-brief` *(enhance existing — [002 stub](../002-speckit-matd-specify-product-brief/spec.md))* | Confluence **Product Charter** (Charter template ME/170265460; verify — OQ-B5) |
| **System Constitution** | **Technical** invariants (policies, tech radar, arch rules, team skills, AWS accounts) | Persistent | `speckit-matd-specify-constitution` *(future — [003 stub](../003-speckit-matd-specify-constitution/spec.md))* | EA `ARCH` space + `DIG` + `TECHOPS` (+ EA-Maps, TBD) |
| **PRD** | The **change request** (this command) | Transient (archived on completion) | `speckit-matd-specify-prd` *(this spec)* | — |

Both companion commands support **existing and new** projects, use **Confluence as reference**,
and extend with **grill-me**. Solution Design = f(Product Brief, System Constitution, PRD).

## Functional Requirements

**Command & schema**
- **FR-001:** Provide command `speckit-matd-specify-prd` as `spec-kit-multi-agent-tdd/commands/specify-prd.md` (a Claude Code command == skill), matching the existing `specify-*` naming.
- **FR-002:** Read `prd-schema.yml`; workspace-local (`.specify/prd-schema.yml`) overrides shipped default.
- **FR-003:** Ship `prd-schema.yml` alongside other templates in `spec-kit-multi-agent-tdd/templates/`.
- **FR-004:** Run a grill interview (general-grill-me) section-by-section, prompts sourced from the schema, one section at a time; allow deferral to Open Questions.
- **FR-005:** Render a markdown PRD from collected answers; never require the PM to hand-edit yml. The template is filled **after** the interview completes.
- **FR-006:** During the grill, build **extended shared design context** beyond the template slots, and persist it to a separate **additional-context file** at `product/context/PRD-NNN-<slug>.context.md` (central context store; H1 title + frontmatter carry the PRD id and created/updated dates). Keep the structured `prd.md` short/concise; put depth here. Capture rationale, discarded options, domain detail, constraints for downstream Solution Design / specs.
- **FR-007 (optional side-task):** Ship an **SDP template file** (`sdp-initiative-template.yml`) that maps to the **Jira REST `fields` payload** for SDP-Initiative creation; render it from the PRD + the workspace jira-config (FR-055). Field ids/values resolved against the workspace config (and live `GET /field` to reconcile id drift). Optional within this command (gated behind FR-050+).
- **FR-008:** Allocate a stable internal **`PRD-NNN`** id at PRD creation (from `product/prd/index.yml` → `next_prd_seq`); write it to the PRD frontmatter; name the file `product/prd/PRD-NNN-<slug>.md` (no per-PRD folder; never renamed).
- **FR-009:** Maintain the **traceability index** (`product/prd/index.yml`) via script: create the `PRD-NNN` entry on PRD creation, bind `sdp_key` (1:1) on SDP creation, write `stash_url`, and reserve an empty `specs[]` (filled by the downstream solution-design command). IDs are permanent (deprecate, never renumber).

**Constitution**
- **FR-010:** Load the existing **system constitution** at `architecture/system-constitution.md` (per-workspace, persistent) for reference during authoring; **do not regenerate it** (that is owned by `/speckit-constitution`). If absent, note it and continue (constitution is referenced, not required to author a PRD).
- **FR-011:** Surface constitution invariants relevant to backend-cloud changes during the interview.

**Content tests (V-model right side)**
- **FR-030:** Provide a deterministic content-test validator (script) checking structural rules from the schema (required sections present, numbered IDs well-formed, no placeholder residue, metrics have baseline-or-TBC). Exit non-zero on CRITICAL.
- **FR-031:** Provide an LLM eval rubric (hard-fail checks + scored criteria, adapted from `feature-prd-eval`) run before SDP creation is offered.
- **FR-032:** Block SDP creation until content tests pass with zero CRITICAL (human may override with acknowledgement, audit-trailed).
- **FR-033:** Keep deterministic (regex/structural) gates **separate from AI-judgment** review (advisory only), per `spec-kit-v-model` — only deterministic gates block. Use self-documenting hierarchical traceability IDs (e.g. `REQ-NNN` → downstream `SD`/`epic`/`story` refs) so PRD↔SD↔epics↔stories lineage is readable without a lookup table; IDs are permanent (deprecate, never renumber).

**Agents & steps (v1 — simplified, 2026-06-08)**

> Simplified per critical review + user decision: **no `matd-ops` agent, no `agent-assignments.yml`,
> no multi-agent build/runtime orchestration.** The command itself calls deterministic scripts
> directly for mechanics; only two smart agents are involved.

- **FR-040:** The command orchestrates a fixed linear flow itself (no `agent-assignments.yml`, no assign/validate/execute machinery):

  | # | Step | Runner | Writes |
  |---|---|---|---|
  | 1 | Scaffold (PRD-NNN, schema load, constitution/brief load) | command + scripts | index.yml, dirs |
  | 2 | Interview + author `prd.md` + `prd-context.md` | **matd-specifier** (smart) | **`.md` only** |
  | 3 | Content tests / eval (advisory rubric + structural validator) | **matd-critical-thinker** (smart) | read-only |
  | 4 | SDP create + transition + commit + link + SDP-key write-back | command + scripts (Jira MCP / git) | scripts, json/yml, git |

- **FR-041:** `matd-specifier` (smart) authors and writes **`.md` files only**; `matd-critical-thinker` (smart) runs content tests read-only. Mechanical steps (1, 4) are **plain scripts the command invokes** — no dedicated mechanical agent. (Token-efficiency comes from the script/LLM split, not from a Haiku sub-agent.)
- **FR-043:** Extract the SDP-creation logic from `stepstone-sdp-planning` / `stepstone-atlassian-skills` into **bundled scripts** shipped with the command (reuse-as-scripts, not skill-invocation), so the command is self-contained and token-cheap.

### What the command encapsulates & how it's critically questioned
- **Encapsulates:** schema-driven interview, markdown rendering, `PRD-NNN` allocation + index, content-test gate, SDP creation (scripts), commit + linking, SDP-key write-back, constitution/brief load (read-only).
- **Critically questioned (matd-critical-thinker, step 3):** Is the change a *single* unit (1:1 SDP) or should it split (1:many)? Are hypothesis + success metrics falsifiable with baselines? Does it conflict with system-constitution invariants or an existing PRD? Is scope a change request (not a product re-brief)? No service-names/schemas leaked into the PRD?
- **Other useful skills:** `stdd-product-spec-formats` (specifier), `general-grill-with-docs` (grill against brief/constitution), `context-optimization` (token budget).

**SDP initiative + persistence**
- **FR-050:** After PRD passes content tests, **offer** (do **not** auto-create) SDP-initiative creation. On explicit confirmation, create via the **`atlassian-write` MCP** (sooperset `mcp-atlassian`, write-enabled, **tested 2026-06-08** against live Cloud): `jira_create_issue` (project SDP, issuetype Initiative, `additional_fields` for the required select custom fields) → `jira_transition_issue` (transition **id 101** → **Idea Backlog 11256**). **Auth is handled by the MCP via env-var token** (`JIRA_*`, cert bundle) — **not in command code** (matches the "auth at MCP/SDP level" requirement). REST-with-token remains a documented fallback. If declined, stop after the PRD is written/committed.
- **FR-051:** The SDP initiative MUST land in the **"Idea Backlog"** status (the ideation stage; status id `11256`). Live Jira creates Initiatives into **"To Do"** (id `11092`) by default, so the command **creates the Initiative, then applies transition id `101` ("Idea Backlog")**. Issue type `Initiative` = id `11110`. (Validated against live Jira 2026-06-08; transition ids should be re-resolved at runtime via `GET /issue/{key}/transitions` rather than hard-coded, as workflow ids can change.)
- **FR-052:** Populate the **6 required SDP Initiative fields** (verified live 2026-06-08, see [sdp-jira-fields.md](../../references/sdp-jira-fields.md)): `summary`, `project=SDP`, `issuetype=11110`, and the 3 required selects — **Stonehenge Domain** `customfield_11259` (28 options), **Initiative Category** `customfield_11313` (Strategic Capability/KTLO/Paying Down Debt), **Initiative Goal** `customfield_11389` (Delivery/Enablement/Research). Plus **Team** `customfield_10001` (value = team **UUID**, e.g. Mamba `f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425`; verified on SDP-6701 — not on the createmeta create screen but set on Initiatives, so include it). Optional: Target start/end `customfield_10022`/`10023`, Sprint `customfield_10020`, Story Points `customfield_10091`. (These ids supersede the outdated `sdp-custom-fields.md` pre-Cloud values.) Resolve the team's UUID/domain/sprint from the workspace jira-config (FR-055); re-verify option ids + Team write-format at build time.
- **FR-052b:** Once the SDP key is known, **write it back into the PRD** — both the frontmatter (`sdp_key:`) and the PRD Header `initiative_link` — and re-commit the PRD so the persisted source carries its SDP key (completing the bidirectional `PRD-NNN ↔ SDP-key` bond alongside the index entry).
- **FR-053:** Commit the PRD (`product/prd/PRD-NNN-<slug>.md`) and its context file (`product/context/PRD-NNN-<slug>.context.md`) and push to **the system's own agent workspace repo on Stash** (one workspace repo per system, holding the workspace-template structure). Central searchability comes from the in-repo `index.yml` + `product/context/` folder, not a separate PRD repo.
- **FR-051a (precondition):** The command assumes the **`atlassian-write` MCP is installed & running** in the workspace (env vars + cert configured). It uses the MCP; it does not install or manage it. If unavailable, the SDP step is skipped with guidance (PRD authoring still completes).
- **FR-053a (precondition):** The command assumes the system's agent workspace repo **already exists** and that **Stash auth works**. For a **new system**, the **Staff Engineer / Engineering Manager** provisions it (from the workspace-template); for an **existing system**, the PM uses it directly. If absent, the command stops with guidance to have the StaffEng/EM create it — it does **not** create the workspace repo itself.
- **FR-053b (v1 push policy):** The command **commits locally and stages the push**, but the actual `git push` is performed by a **human who knows how to push** (working Stash auth assumed). v1 does not script the push (removes auth/non-fast-forward fragility from the automated path); can be automated later once proven.
- **FR-055:** Ship a **Jira config scaffold** with the command in the marketplace (placeholder structure mirroring `jira-teams-config.yaml` / `sdp-custom-fields`: team ids, Stonehenge Domain, Initiative Goal/Category, sprint, custom-field ids, transition ids — all blank/templated). The **live, filled config is custom per team and MUST live in the agent workspace only** (e.g. `.specify/jira-config.yml` or `architecture/`), **never committed to the marketplace** (OSS-safe boundary). An agent **populates** the workspace config by reading the team's values (from the live Jira via MCP/REST and/or PM input); the command reads the workspace config at runtime and falls back to the scaffold's documented shape.
- **FR-054:** Link the source PRD to the SDP initiative via the MCP's **`jira_create_remote_issue_link`** (or REST `/remotelink`) pointing to the **PRD markdown file on Stash** (title "Source PRD — PRD-NNN"), and include the URL in the initiative description. Also store `stash_url` in the index and `sdp_key` in the PRD frontmatter. **Planned migration:** switch to a dedicated **custom field (option B)** once the Atlassian team provisions it — keep the link-writing step abstracted so the mechanism can swap without changing the workflow.

**Token efficiency**
- **FR-060:** Deterministic plumbing (scaffold, parse, validate, SDP create, Stash commit) runs in scripts; the LLM is invoked only for the interview and authoring.
- **FR-061:** Load only the schema section currently in play; cap validator/eval output.

---

## Non-Functional Requirements
- **NFR-001 (COST):** Measurably lower token use than PLAYGROUND `prd` for equivalent input (SC-003).
- **NFR-002 (OBS):** Every workflow step reports stage, what completed, what's next, and required human gates (PLAYGROUND "guide, not compiler" rule).
- **NFR-003 (SEC):** No corporate secrets in the OSS marketplace; Stepstone specifics stay in private submodules/skills.
- **NFR-004 (ARCH):** OSS-safe; backend-cloud oriented; local-first (docker-compose).

---

## v1 scope (MVP) & risk register

Following the critical review (2026-06-08) + user decisions. **v1 = lean, ~20–24 SP.**

**In v1:** thin `prd-schema.yml` (sections + grill prompts), the command (calls scripts directly),
`PRD-NNN` + `index.yml` (full schema incl. `specs[]`/archival — **kept**), structural validator
**advisory** + LLM eval rubric, SDP create+transition via **Jira MCP** (offered), SDP-key
write-back (**kept**), local commit + remote-link (human pushes), Jira config scaffold + workspace
live config.

**Dropped/deferred:** `matd-ops` agent (→ scripts), `agent-assignments.yml` + assign/validate/execute,
multi-agent build orchestration, alternative Solution Design template (→ spec 004), automated Stash push (→ human).

| Risk | Sev | Mitigation (v1) |
|---|---|---|
| ~~Jira MCP can't create/transition~~ (R2/OQ-11) | ✅ Mitigated | **Resolved:** `atlassian-write` MCP tested against live Cloud — create/transition/remote-link tools work; auth via env token. REST fallback documented. Remaining: confirm required custom-field ids at build (drift). |
| **Stash push fragility** (R3) | Med-High | v1 commits locally; **human pushes** (FR-053b); assume working auth |
| **OSS-safe leak of corp IDs** (R6) | High | Marketplace ships **scaffold only**; live jira-config in workspace, never marketplace (FR-055) |
| **Content-test false gates** (R4) | Med | Structural validator **advisory** (warn) in v1; only frontmatter/section presence is hard (FR-033) |
| **Jira transition-id drift** (R1) | Med | Re-resolve transition ids at runtime; on transition fail, surface created key + manual-fix guidance |
| **Schema over-coupling** (R7) | Med | Start with thin schema (sections+prompts); grow validation later |

## Cross-repo impact (flows into `harness-tooling/TARGET_STATE.md`)

Per the user, part of this work belongs in a **`TARGET_STATE.md` for the harness-tooling
submodule** (does not yet exist; core repo's own `TARGET_STATE.md` is separate). Candidate
content to migrate there:

- The **MATD agent skill re-scoping** to match [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md):
  current agent files in `.agents/plugins/matd/agents/` over-share **role-specific** skills
  (`dev-tdd`, `review-check-correctness`, `stdd-openspec`, `general-system-design`,
  `general-grill-me` beyond specifier/critical-thinker). Target = the matrix's de-overlapped
  assignment + `harness-matd-core` / `harness-matd-extensions` tiers. **Note:** shared
  general/baseline skills (rtk, verification, context-optimization, git) are accepted overlap —
  only role-defining skills are de-duplicated.
- The **DESIGN-stage workflow** (PRD → Constitution → Solution Design → specs) and where its
  commands/templates live in the extension.
- The **alternative Solution Design template** placement.
- The principle that **PDLC artefacts are realised as SpecKit commands + shipped templates**
  (Design Principle 7), superseding any plan to port PLAYGROUND skills/agents verbatim. The
  MATD extension grows a command per artefact (PRD, Solution Design, RFC, Epic Implementation
  Plan, …), each with a template + content-test (`checklist`/`analyze`) compliance gate.

> **Action required:** confirm whether to create `submodules/harness-tooling/TARGET_STATE.md`
> (or fold into existing `harness-tooling/docs/architecture/`), then migrate the above. See OQ-7.

---

## Open Questions (resolve via follow-up clarify pass)

- **OQ-1 — FR/NFR ownership.** ✅ **RESOLVED (2026-06-08):** Stick with the **official StepStone model**. FR + NFR are **required for the Solution Design** (Tech-owned), **not** PRD content. The PRD creator **may optionally** provide outcome-level requirements (`REQ-NNN`); the PRD stays at user-workflows/outcomes with no service names/schemas.
- **OQ-2 — SDP "Ideation" status.** ✅ **RESOLVED (2026-06-08, live Jira):** No literal "Ideation" status. Target = **"Idea Backlog"** (id `11256`). Create lands in **"To Do"** (id `11092`); apply transition **id 101** ("Idea Backlog"). `Initiative` issue type id `11110`. **Follow-up:** the local `stepstone-sdp-planning` workflow doc is outdated (implies Idea Backlog is a create-default; casing "In Planning" vs live "In planning"; omits Icebox from main list) — corrected reference block added to the skill (see below).
- **OQ-3 — PRD workspace folder.** ✅ **RESOLVED (2026-06-08, revised):** **File-based, no per-PRD folder.** `product/prd/PRD-NNN-<slug>.md` (concise) + `product/prd/index.yml` + optional `.sdp.json`; additional context centralised in `product/context/PRD-NNN-<slug>.context.md`. Cardinality PRD↔SDP 1:1, PRD→Specs 1:many, Spec↔Epic 1:1, Spec→Tasks/Stories 1:many. Stable `PRD-NNN` ids.
- **OQ-4 — PRD↔SDP link mechanism.** ✅ **RESOLVED (2026-06-08):** Start with **(A)** a Jira remote/web link to the PRD markdown file on Stash + URL in description. **Migrate to (B)** a dedicated custom field once the Atlassian team provisions it. Keep the link step abstracted to allow the swap.
- **OQ-5 — Constitution scope & path.** ✅ **RESOLVED (2026-06-08):** Per-workspace, persistent, at **`architecture/system-constitution.md`** (already in workspace-template, referenced by AGENT.md). It captures **TECHNICAL invariants only** (company policies, tech radar, architectural rules, team skill sets, AWS accounts) — **not** business invariants (those go in the project brief). Modelled on the PDLC repo's `docs/stepstone-conventions/` pattern (digest + Confluence mirror + refresh). specify-prd **references** it (reference-only); creation/update owned by the future `speckit-matd-specify-constitution` command (see [003 stub](../003-speckit-matd-specify-constitution/spec.md)).
- **OQ-6 — Step→agent map.** ✅ **RESOLVED (2026-06-08, simplified):** Two smart agents + scripts (FR-040/041): interview/authoring → **matd-specifier** (`.md`-only); content-tests → **matd-critical-thinker** (read-only); mechanical steps (scaffold, SDP, commit/link) → **plain scripts the command invokes**. **Dropped** per review+decision: the `matd-ops` Haiku agent, `agent-assignments.yml`, and multi-agent build/runtime orchestration.
- **OQ-7 — harness-tooling TARGET_STATE.md.** ✅ **RESOLVED (2026-06-08):** **Create** `submodules/harness-tooling/TARGET_STATE.md`. Migrates: MATD agent skill re-scoping (per AGENT_SKILL_MATRIX) + new `matd-ops` Haiku agent; DESIGN-stage commands as SpecKit commands+templates (PRD/brief/constitution/solution-design); two-tier `harness-matd-core`/`-extensions` model; Principle 7.
- **OQ-8 — Command output scope.** ✅ **RESOLVED (2026-06-08):** Stops at PRD + (offered, non-automatic) SDP initiative. Does **not** author Solution Design/specs. **SDP creation is only offered**, never automatic (FR-050).
- **OQ-9 — Additional-context file.** ✅ **RESOLVED (2026-06-08, revised):** Central `product/context/PRD-NNN-<slug>.context.md` (one per PRD; title + frontmatter carry PRD id + created/updated), no per-PRD folder; committed to Stash with the PRD. Goal: terse structured `prd.md`, depth in context files.
- **OQ-10 — Stash target repo.** ✅ **RESOLVED (2026-06-08):** The **system's own agent workspace repo** (one per system, holds the workspace-template structure). New system → Staff Engineer/EM provisions it; existing system → PM uses it. The command assumes it exists (FR-053a), never creates it. Central search via in-repo `index.yml` + `product/context/`.
- **OQ-11 — Jira create path.** ✅ **RESOLVED (2026-06-08, tested):** Use the **`atlassian-write` MCP** (sooperset `mcp-atlassian`, configured in `.mcp.json`). Live test confirmed: server starts, auths via env-var token + cert bundle against **Cloud `stepstone.atlassian.net`**, and `jira_get_issue SDP-7768` returned a real Initiative in "To Do" (`isError:false`). Exposes `jira_create_issue`, `jira_transition_issue`, `jira_update_issue`, `jira_create_remote_issue_link`, `jira_search`, plus `confluence_create_page`/`update_page`. The earlier "MCP not viable" finding referred to the *official* Atlassian MCP; this *write* server is viable. REST+token is the fallback. Custom fields go via `jira_create_issue` `additional_fields` (reconcile field-id drift via `jira_search`/`GET /field` at build time).
  - **OQ-11a — Cloud confirmed.** ✅ Jira is **Atlassian Cloud `stepstone.atlassian.net`** (recent migration; the Data-Center/`vulcan` note was outdated).
  - **OQ-11b — RESOLVED (assumption):** the `atlassian-write` MCP is a **workspace precondition** — assume it is **installed & running** in each agent workspace (env vars + cert volume configured), like Stash auth. The command **uses** it; it does not install/manage it. (Shipping a default `.mcp.json` in workspace-template is a convenience, not this command's responsibility.)

---

## People
- **Product Owner / primary user:** Product Managers (StepStone)
- **Author:** Daniel Mingers
- **Downstream consumers:** Tech leads (Solution Design), ProductOps (scorecard/traceability)

## Dependencies
- `stepstone-sdp-planning`, `stepstone-atlassian-skills`, Atlassian MCP (OAuth), `jira-teams-config.yaml`
- `spec-kit-multi-agent-tdd` extension (commands/templates/agents)
- `spec-kit-agent-assign` pattern
- Stash access (SSH) for PRD push + linking
- [AGENT_SKILL_MATRIX.md](../../AGENT_SKILL_MATRIX.md)

---

**Verification Checklist:**
- [ ] All required sections present
- [ ] YAML frontmatter valid (type: spec)
- [ ] Feature ID and timestamp filled
- [ ] Open Questions enumerated (OQ-1..8)
- [ ] No unresolved placeholder content beyond explicit [NEEDS CLARIFICATION] markers
