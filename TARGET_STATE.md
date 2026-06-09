---
type: target-state
created: "2026-06-09"
owner: "Daniel Mingers"
---

# harness-tooling — Target State

Target architecture for the MATD tooling shipped from this marketplace. Captures decisions surfaced
during the DESIGN-stage command design (2026-06-08). The driving specs live in **this repo**
under `docs/specs/001..004-*` and `docs/AGENT_SKILL_MATRIX.md`.

> **OSS-safe invariant:** This repo is the OSS marketplace. StepStone-specific content (EA
> principles, AWS accounts, internal endpoints, Confluence mirrors) **must not** live here — it
> belongs in private/local skills (`.claude/skills/stepstone-*`). Only generic, content-free
> frameworks are upstreamed here.

## Status

**Last updated:** 2026-06-10

**Architectural phase:** Design complete — ready for implementation

**Key decisions finalized (2026-06-09 grilling session):**
- 7-agent architecture (matd-product-manager, matd-requirements-engineer, matd-architect, matd-critical-thinker, matd-qa, matd-dev, matd-orchestrator)
- Agent restrictions via disallowedTools + inline MCP scoping
- Four SpecKit extensions split by PDLC phase
- Enhanced workspace structure (specs-as-folders, matd-config.yml)
- Traceability chain (PRD → SD → Spec → Tests → Code)

See **Section 9 (Implementation Status)** for detailed command implementation progress.

---

## 1. MATD Agent Skill Re-scoping

**Current problem:** Agent files in `.agents/plugins/matd/agents/` over-share role-specific skills
beyond what is appropriate per role — `dev-tdd`, `review-check-correctness`, and
`general-system-design` appear across agents that should not carry them.

**Target state** per `docs/AGENT_SKILL_MATRIX.md` (this repo):

7-agent architecture supporting full PDLC workflow:

| Agent | Role-defining skills | Excluded |
|---|---|---|
| `matd-product-manager` | `general-grill-me`, `general-grill-with-docs`, `arch-writing-plans`, Jira MCP (inline scope) | `dev-tdd`, `review-*`, `arch-*` |
| `matd-requirements-engineer` | `general-grill-me`, `general-grill-with-docs`, `arch-writing-plans`, `brainstorming`, Confluence MCP (inline scope) | `dev-tdd`, `review-*`, `arch-*` |
| `matd-architect` | `arch-c4-architecture`, `arch-architecture-patterns`, `arch-api-design-principles`, `arch-mermaid-diagrams`, `arch-design-system-patterns`, `arch-smart-docs`, `general-system-design`, `general-solid`, `general-improve-codebase-architecture`, `review-simplify-complexity`, `arch-writing-plans`, `dev-database-migration`, `docker-expert` | `dev-tdd`, `review-check-correctness` |
| `matd-critical-thinker` | `review-check-correctness`, `general-grill-me`, `general-grill-with-docs`, `review-simplify-complexity`, `review-systematic-debugging`, `review-differential-review`, `general-improve-codebase-architecture`, `review-orchestrate-dual-review` | `dev-tdd` |
| `matd-qa` | `review-check-correctness`, `review-systematic-debugging`, `review-differential-review`, `review-e2e-testing-patterns`, `review-webapp-testing`, `review-orchestrate-dual-review`, `dev-tdd`, `dev-diagnose`, `python-*`, `python-testing-uv-playwright` | `arch-*` |
| `matd-dev` | `dev-tdd`, `dev-databases`, `dev-database-migration`, `dev-backend-to-frontend-handoff`, `dev-diagnose`, `dev-mobile-android-design`, `dev-alpine-js-patterns`, `python-*`, `general-solid`, `arch-api-design-principles`, `filesystem-context`, `file-ops-*`, `docker-expert` | `review-check-correctness`, `arch-c4-architecture` |
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
  - `product-pack`: Jira MCP configuration (inline agent scope)
  - `requirements-pack`: Confluence MCP configuration (inline agent scope)
  - `architect-pack`: `arch-*`, `general-system-design`, `general-solid`, `dev-database-migration`, `docker-expert`
  - `critic-pack`: `review-simplify-complexity`, `review-systematic-debugging`, `review-differential-review`, `review-orchestrate-dual-review`, `general-improve-codebase-architecture`
  - `qa-pack`: `review-e2e-testing-patterns`, `review-webapp-testing`, `python-testing-uv-playwright`
  - `dev-pack`: `python-*`, `dev-*`, `file-ops-*`, `filesystem-context`, `general-solid`, `arch-api-design-principles`
  - `orchestrator-pack`: `manage-*`, `update-config`, `context-degradation`, `context-compression`

Both plugins ship the same 7 agent definitions; agent files declare their required skills.
See `docs/AGENT_SKILL_MATRIX.md` in this repo for the authoritative per-skill assignment.

---

## 2. Agent Capability Restrictions

**Design invariant:** Agents are scoped using `disallowedTools` (skill/MCP blocks) and inline MCP server configuration (role-based access).

**Skill restriction syntax:**
```yaml
disallowedTools:
  - "Skill(skill-name)"  # Must use exact Skill(name) format
```

**MCP restriction patterns:**

1. **Inline agent scoping** (preferred for role-based access):
   ```yaml
   # In agent.md frontmatter
   mcpServers:
     atlassian-write:
       command: "npx"
       args: ["-y", "@modelcontextprotocol/server-atlassian"]
   ```
   - Only that agent can see the MCP server
   - Other agents in workspace cannot access it
   - Use for Product Manager (Jira), Requirements Engineer (Confluence)

2. **Project-level scoping** (all-or-nothing):
   ```yaml
   # In workspace .claude/settings.json
   {
     "mcpServers": {
       "atlassian-write": {...}
     }
   }
   ```
   - All agents can access
   - Cannot restrict per-agent

**Priority levels:**
- Project agents: Priority 3 (higher precedence)
- Plugin agents: Priority 5
- Use `specify extension add <path> --priority 3` for project-level agents

Reference: `docs/context/agent-restrictions-learnings.md`

---

## 3. SpecKit Extension Split (4 Extensions)

**Design invariant:** SpecKit commands are split by PDLC phase, not bundled monolithically.

**Four extensions:**

1. **`matd-discovery`** — PRD capture, Product Brief, Constitution generation
   - Commands: `/matd.specify-prd`, `/matd.specify-product-brief`, `/matd.specify-constitution`
   - Agents: matd-product-manager, matd-requirements-engineer
   - Templates: `prd-schema.yml`, `product-brief.md.j2`, `constitution.md.j2`

2. **`matd-solution-design`** — Architecture design phase
   - Commands: `/matd.specify-solution-design`, `/matd.specify-adr`
   - Agents: matd-architect, matd-critical-thinker
   - Templates: `solution-design.md.j2`, `adr.md.j2`, `c4-diagram.puml.j2`

3. **`matd-refinement`** — Test design, implementation planning
   - Commands: `/matd.test`, `/matd.plan`
   - Agents: matd-qa, matd-architect
   - Templates: `test-scenario.md.j2`, `e2e-test.py.j2`, `implementation-plan.md.j2`

4. **`matd-implement-tdd`** — TDD workflow execution
   - Commands: `/matd.implement`, `/matd.review`, `/matd.commit`, `/matd.update-docs`
   - Agents: matd-dev, matd-critical-thinker, matd-architect, matd-qa
   - Templates: `unit-test.py.j2`, `review-checklist.md.j2`

**Shared resources:**
- All extensions share `templates/` subdirectory (common artifact formats)
- All extensions depend on `harness-matd-core` plugin (agents + baseline skills)
- Extension commands use `agent-assign` extension for CLI-agnostic agent routing

**SpecKit preset mechanism:**
```yaml
# In matd-discovery/presets/matd.yml
presets:
  matd:
    specify:
      default_template: "prd-schema.yml"
      default_command: "/matd.specify-prd"
```
- Overrides `/specify` behavior when `matd` preset is active
- Allows project-level `/specify` to route to MATD workflow

---

## 4. Enhanced Workspace Structure

**Design invariant:** Specifications are folders, not files. Each feature gets a structured directory with all artifacts co-located.

**Specs-as-folders pattern:**
```
specs/
├── 001-user-authentication/
│   ├── spec.md              # Feature specification
│   ├── solution-design.md   # Architecture design
│   ├── test-design.md       # Test scenarios
│   ├── impl-notes.md        # Implementation notes
│   ├── arch-review.md       # Architecture review findings
│   ├── code-review.md       # Code review findings
│   └── workflow-summary.md  # Final workflow summary
├── 002-payment-processing/
│   └── ...
└── matd-config.yml          # Workspace MATD configuration
```

**matd-config.yml schema:**
```yaml
version: "1.0"
agents:
  product_manager: "matd-product-manager"
  requirements_engineer: "matd-requirements-engineer"
  architect: "matd-architect"
  critical_thinker: "matd-critical-thinker"
  qa: "matd-qa"
  dev: "matd-dev"

artifacts:
  root: "specs"                    # Configurable root directory
  types:
    spec: "spec"
    solution_design: "solution-design"
    test_design: "test-design"
    impl_notes: "impl-notes"
    arch_review: "arch-review"
    code_review: "code-review"
    workflow_summary: "workflow-summary"
  search_paths:                    # Fallback search order
    - "specs"
    - "docs/features"
    - ".specify/specs"

gates:
  default_mode: "auto"
  manual_gates: []
  max_review_cycles: 3
  convergence_detection: true

test_framework:
  type: "pytest"
  failure_codes:
    valid_red:
      - "AssertionError"
      - "NameError"
      - "AttributeError"
    invalid_escalate:
      - "SyntaxError"
      - "ImportError"
```

**Design principle:** Configurable paths via matd-config.yml, not hardcoded in commands. Commands read config to determine artifact locations.

---

## 5. Traceability Chain

**Design invariant:** Every implementation artifact traces back through Solution Design → Product Brief → PRD.

**Numbering scheme:**
- PRD: Transient (archived after conversion to Product Brief)
- Product Brief: Persistent, no number (single document per product)
- Solution Design: `SD-NNN` (per-change identifier)
- Spec: `{feature-id}` (e.g., `001-user-authentication`)

**Traceability metadata:**
```yaml
# In specs/001-user-authentication/spec.md frontmatter
feature_id: "001-user-authentication"
solution_design: "SD-042"           # Links to solution design
product_brief: "Product Brief v2.1" # Links to product brief context
prd: "PRD-2024-Q2-003"              # Original PRD (archived)
```

**Test markers for traceability:**
```python
@pytest.mark.feature("001-user-authentication")
@pytest.mark.solution_design("SD-042")
@pytest.mark.acceptance_criteria("AC-1.2")
def test_user_login_with_valid_credentials():
    ...
```

Enables:
- Forward trace: PRD → SD → Spec → Tests → Code
- Backward trace: Code → Tests → Spec → SD → Product Brief
- Impact analysis: "Which tests cover SD-042?"
- Coverage reports: "Which acceptance criteria lack tests?"

Reference: Solution Design template includes traceability section linking to Product Brief and PRD.

---

## 6. DESIGN-Stage Commands as SpecKit Commands + Templates

The PLAYGROUND `agentic-pdlc-workspace` capabilities are **not** ported as bespoke skills or agent
definitions. They are **re-expressed as SpecKit commands** (`.md` command files in extension
`commands/` subdirectories) **paired with shipped templates**.

**Commands across 4 extensions (in PDLC order):**

| Extension | Commands | Artefacts | Owner | Persistence |
|---|---|---|---|---|
| `matd-discovery` | `/matd.specify-prd`, `/matd.specify-product-brief`, `/matd.specify-constitution` | PRD, Product Brief, Constitution | Product/Requirements/EA | transient (PRD), persistent (Brief/Constitution) |
| `matd-solution-design` | `/matd.specify-solution-design`, `/matd.specify-adr` | Solution Design, ADRs | Architect | per-change (SD), persistent (ADRs) |
| `matd-refinement` | `/matd.test`, `/matd.plan` | Test Design, Implementation Plan | QA/Architect | per-feature |
| `matd-implement-tdd` | `/matd.implement`, `/matd.review`, `/matd.commit`, `/matd.update-docs` | Code, Reviews, Commits, Docs | Dev/Reviewer | per-commit |

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

## 7. Design Principles

### Principle 7 — PDLC Artefacts as SpecKit Commands

> PDLC artefacts (PRD, Solution Design, RFC, Epic Implementation Plan, etc.) are realised as
> **SpecKit commands + shipped templates**, not as copied skills or bespoke agent definitions.
> SpecKit commands are natively suited to testing document structure compliance via `/checklist`
> (unit tests for English) and `/analyze` (cross-artifact consistency). Templates ship as the
> standard SpecKit feature (project-override → preset → extension → core resolution order).
> Each MATD extension grows commands for its PDLC phase.

This principle governs all future DESIGN-stage additions. Any capability from the PLAYGROUND
`agentic-pdlc-workspace` is adopted as a SpecKit command, not as a skill or agent clone.

### Principle 8 — Configurable Paths via matd-config.yml

> Artifact locations, agent assignments, and workflow behavior are **configurable via
> matd-config.yml**, not hardcoded in command implementations. Commands read the config to determine
> where to write artifacts, which agents to invoke, and which quality gates to enforce.
> This enables workspace-level customization without forking extension code.

Supports multi-tenant scenarios (different teams, different artifact structures) and gradual
adoption (start with defaults, customize as needed).

---

## 8. Future: spec-kit-agent-assign Pattern (deferred)

The `agent-assignments.yml` + assign/validate/execute machinery (from the `spec-kit-agent-assign`
reference implementation) is documented as a **future option** once multiple DESIGN-stage commands
share the wiring. It is **not implemented in v1** of any command.

In v1, commands call deterministic scripts directly for mechanical steps; smart agents are invoked
via command frontmatter `agent:` field (routed by `agent-assign` extension). The orchestration
engine would remove per-command wiring duplication once ≥2 commands prove out the pattern.

Reference implementation: `docs/references/spec-kit-agent-assign-summary.md` in the core repo.

---

## 9. Implementation Status

**Current focus:** Split SpecKit extension into 4 phase-based extensions per Section 3.

**Completed architectural decisions:**
- ✅ 7-agent architecture (Section 1)
- ✅ Agent capability restrictions via disallowedTools + inline MCP (Section 2)
- ✅ Four SpecKit extensions by PDLC phase (Section 3)
- ✅ Enhanced workspace structure (specs-as-folders, matd-config.yml) (Section 4)
- ✅ Traceability chain (PRD → SD → Spec → Tests → Code) (Section 5)
- ✅ Design principles for configurable paths (Section 7)

**Command implementation status:**

| Extension | Commands | Status |
|---|---|---|
| `matd-discovery` | `/matd.specify-prd`, `/matd.specify-product-brief`, `/matd.specify-constitution` | **In progress** (PRD command) |
| `matd-solution-design` | `/matd.specify-solution-design`, `/matd.specify-adr` | Stub |
| `matd-refinement` | `/matd.test`, `/matd.plan` | Stub |
| `matd-implement-tdd` | `/matd.implement`, `/matd.review`, `/matd.commit`, `/matd.update-docs` | Stub |

**Next steps:**
1. Update AGENT_SKILL_MATRIX.md to reflect 7-agent architecture
2. Split monolithic `spec-kit-multi-agent-tdd` into 4 extensions
3. Implement agent restriction patterns in agent.md frontmatter
4. Create matd-config.yml.template with full schema
5. Implement traceability metadata in templates

---

## 10. Open Items

**Architectural questions:**
1. Should agent-assign extension be vendored or external dependency?
2. MCP inline scoping: Test with Claude Code agent frontmatter (not yet validated)
3. SpecKit preset mechanism: Verify override behavior with `/specify` default command

**Implementation details deferred to spec documents:**
- Product Brief → Confluence sync mechanism (matd-discovery extension)
- Constitution → EA-Maps compliance checklist integration (matd-discovery extension)
- Solution Design → StepStone 9-section template adaptation (matd-solution-design extension)
- Test failure code detection patterns (matd-refinement extension)
