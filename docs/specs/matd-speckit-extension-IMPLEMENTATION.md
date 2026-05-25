# Implementation Contract: matd as Spec-Kit Extension

**Status:** Authoritative for implementation subagents
**Date:** 2026-05-25
**Branch:** `feat/matd-as-speckit-extension`
**Spec:** `docs/specs/matd-speckit-extension.md`
**Plan:** `docs/plans/matd-speckit-extension.md`

This document locks every implementation choice. If something is ambiguous,
stop and ask — do NOT invent. Items explicitly marked **TBC** are the only
ones an implementation subagent is permitted to research and resolve;
everything else is locked.

---

## 1. Target Directory Tree (post-implementation)

```
spec-kit-multi-agent-tdd/
├── extension.yml                        # rewritten — schema 1.0, version 2.0.0
├── README.md                            # updated — describes v2.0.0
├── CHANGELOG.md                         # updated — adds 2.0.0 entry
├── LICENSE                              # unchanged
├── matd-config.yml.template             # unchanged
├── config-schema.json                   # unchanged
├── pyproject.toml                       # unchanged
├── requirements.txt                     # unchanged
├── uv.lock                              # unchanged
├── .extensionignore                     # unchanged
│
├── commands/                            # 8 files, all rewritten
│   ├── speckit.matd.feat-workflow.md
│   ├── speckit.matd.specify.md
│   ├── speckit.matd.design.md
│   ├── speckit.matd.refine.md
│   ├── speckit.matd.implement.md
│   ├── speckit.matd.review.md
│   ├── speckit.matd.commit.md
│   └── speckit.matd.update-docs.md
│
├── skills/                              # NEW — exact copy of plugin skills
│   ├── arch-api-design-principles/
│   ├── arch-architecture-patterns/
│   ├── arch-c4-architecture/
│   ├── arch-design-system-patterns/
│   ├── arch-mermaid-diagrams/
│   ├── arch-smart-docs/
│   ├── arch-writing-plans/
│   ├── dev-alpine-js-patterns/
│   ├── dev-backend-to-frontend-handoff/
│   ├── dev-database-migration/
│   ├── dev-databases/
│   ├── dev-diagnose/
│   ├── dev-tdd/
│   ├── general-finishing-a-development-branch/
│   ├── general-git-advanced-workflows/
│   ├── general-git-guardrails-claude-code/
│   ├── general-grill-me/
│   ├── general-grill-with-docs/
│   ├── general-improve-codebase-architecture/
│   ├── general-python-environment/
│   ├── general-rtk-usage/
│   ├── general-solid/
│   ├── general-system-design/
│   ├── general-using-git-worktrees/
│   ├── general-verification-before-completion/
│   ├── orchestrate-dispatching-parallel-agents/
│   ├── orchestrate-executing-plans/
│   ├── orchestrate-finishing-a-development-branch/
│   ├── orchestrate-multi-agent-patterns/
│   ├── orchestrate-subagent-driven-development/
│   ├── python-async-patterns/
│   ├── python-code-style/
│   ├── python-configuration/
│   ├── python-design-patterns/
│   ├── python-fastapi-templates/
│   ├── python-packaging/
│   ├── python-testing-uv-playwright/
│   ├── review-check-correctness/
│   ├── review-differential-review/
│   ├── review-e2e-testing-patterns/
│   ├── review-openai-playwright/
│   ├── review-simplify-complexity/
│   ├── review-systematic-debugging/
│   ├── review-webapp-testing/
│   ├── stdd-ask-questions-if-underspecified/
│   ├── stdd-make-constrained-implementation/
│   ├── stdd-openspec/
│   ├── stdd-pm-linear-integration/
│   ├── stdd-product-spec-formats/
│   ├── stdd-project-summary/
│   ├── stdd-test-author-constrained/
│   └── stdd-test-driven-development/
│
├── workflows/
│   └── matd-tdd.yml                     # rewritten — 4 stages + gates
│
├── hooks/
│   ├── install.sh                       # rewritten — per-host branches
│   └── config.yml                       # unchanged (Claude Code PreToolUse hooks)
│
├── templates/                           # unchanged — 9 artifact templates
├── lib/                                 # unchanged — 12 Python helpers
├── scripts/                             # unchanged — 10 validation scripts
├── config/                              # unchanged
├── docs/                                # unchanged
├── examples/                            # unchanged
├── tests/                               # unchanged
├── artifacts/                           # unchanged
└── .specify/                            # unchanged
```

---

## 2. `extension.yml` — Complete YAML

Field meanings cited from `/tmp/matd-speckit-research/extension-system.md` §A
lines 49–88 and §D lines 296–329.

```yaml
schema_version: "1.0"

extension:
  id: "matd"
  name: "MATD (Multi-Agent Test-Driven)"
  version: "2.0.0"
  description: "Multi-Agent Test-Driven workflow for spec-kit. Dispatches role subagents (specifier, architect, qa, dev, critical-thinker) via host CLI native subagent mechanism."
  author: "Daniel Minges <minged01@stepstone.com>"
  repository: "https://github.com/mer0mingian/harness-tooling"
  license: "MIT"
  homepage: "https://github.com/mer0mingian/harness-tooling/tree/main/spec-kit-multi-agent-tdd"

requires:
  speckit_version: ">=0.1.0"
  integrations:
    any:
      - "claude"
      - "opencode"
      - "gemini"
  tools: []
  commands: []
  scripts: []

provides:
  commands:
    - name: "speckit.matd.feat-workflow"
      file: "commands/speckit.matd.feat-workflow.md"
      description: "Run the full 4-stage matd workflow (specify -> design -> refine -> implement) with user gates between stages."
      aliases: []
    - name: "speckit.matd.specify"
      file: "commands/speckit.matd.specify.md"
      description: "Stage 1: draft OpenSpec proposal and requirements via matd-specifier; optional red-team via matd-critical-thinker."
      aliases: []
    - name: "speckit.matd.design"
      file: "commands/speckit.matd.design.md"
      description: "Stage 2: produce design.md, C4 diagrams, and ADRs via matd-architect."
      aliases: []
    - name: "speckit.matd.refine"
      file: "commands/speckit.matd.refine.md"
      description: "Stage 3: delivery plan (architect) -> audit (critical-thinker) -> RED-state tests (qa)."
      aliases: []
    - name: "speckit.matd.implement"
      file: "commands/speckit.matd.implement.md"
      description: "Stage 4: RED tests (qa) -> TDD loop max 20 iterations (dev) -> final audit (qa) -> PR (architect)."
      aliases: []
    - name: "speckit.matd.review"
      file: "commands/speckit.matd.review.md"
      description: "Parallel architecture + QA review of an implementation."
      aliases: []
    - name: "speckit.matd.commit"
      file: "commands/speckit.matd.commit.md"
      description: "Evidence-gated git commit. Refuses on missing or invalid evidence."
      aliases: []
    - name: "speckit.matd.update-docs"
      file: "commands/speckit.matd.update-docs.md"
      description: "Post-merge: matd-architect updates C4 diagrams and re-indexes the codebase."
      aliases: []
  config:
    - name: "matd-config.yml"
      template: "matd-config.yml.template"
      description: "matd workflow configuration (test frameworks, paths, quality gates)"
      required: false

templates:
  directory: "templates/"

tags:
  - "tdd"
  - "multi-agent"
  - "workflow"
  - "matd"
  - "subagent-dispatch"

defaults: {}
```

**Notes for the implementation subagent:**
- `requires.integrations.any` is documented in
  `/tmp/matd-speckit-research/extension-system.md` lines 173–178 for
  workflows. If spec-kit's extension-manifest validator rejects this field
  at the extension level, drop it and move the integration list to
  `tags` plus a `README.md` note. **TBC** — verify by running the dev-install
  command.
- All command names match `^speckit\.matd\.[a-z0-9-]+$` (see
  `/tmp/matd-speckit-research/extension-system.md` lines 131–134).

---

## 3. Canonical Command Body Template

Every command file in `commands/` SHALL follow this skeleton:

```markdown
---
description: "<one-line description, mirrors extension.yml entry>"
tools: []
scripts: {}
---

# <Command title>

## User Input
$ARGUMENTS

## Mission
<one paragraph: what does the user get out of this command>

## Output Artifacts
- `<path/to/artifact1.md>`
- `<path/to/artifact2.md>`

## Subagent Role
**Name:** `<matd-role>`
**Persona:** see block-quote below.
**Skills loadout (in load order):**
- `<skill-1>`
- `<skill-2>`
- ...

> Persona source (read at dispatch time):
> `harness-tooling/.agents/plugins/matd/agents/<matd-role>.md`

## Host Dispatch Flow — Claude Code

The main agent IS the orchestrator. Do NOT spawn a separate orchestrator
subagent.

1. Read the persona file referenced above.
2. Use the Task tool to dispatch a subagent named `<matd-role>` with:
   - System prompt: persona content + skill loadout.
   - User prompt: the user's `$ARGUMENTS` plus relevant project context.
3. Stream the subagent's progress back to the user.
4. On return, validate the output artifacts exist and announce completion.

## Host Dispatch Flow — OpenCode / Gemini

The main agent first spawns the orchestrator subagent, which then dispatches
the role subagent.

1. Spawn subagent `matd-orchestrator` (read-only, skills per §6.6).
2. Pass it: the user's `$ARGUMENTS`, the persona path
   `harness-tooling/.agents/plugins/matd/agents/<matd-role>.md`, the skill
   loadout list, the output-artifact paths.
3. The orchestrator subagent then spawns `<matd-role>` using its host's
   native subagent mechanism (TBC — implementation subagent verifies exact
   syntax against OpenCode subagent-extension docs and Gemini
   subagent docs).
4. The orchestrator collects the role subagent's output and returns it.

## Validation / Gating

<command-specific evidence checks; what scripts in lib/ and scripts/ must
return before the user gate>

## User Gate

After validation passes, prompt the user with a one-line summary and
require explicit approval before the next command in the workflow runs.
```

---

## 4. Worked Example — `commands/speckit.matd.specify.md`

```markdown
---
description: "Stage 1: draft OpenSpec proposal and requirements via matd-specifier; optional red-team via matd-critical-thinker."
tools: []
scripts: {}
---

# speckit.matd.specify

## User Input
$ARGUMENTS

## Mission
Transform an idea into concrete OpenSpec artifacts (proposal, specs) and
testable user stories using modern requirements formats (Job Stories, EARS,
Gherkin). Optional red-team pass surfaces edge cases before stage 2.

## Output Artifacts
- `openspec/changes/<slug>/proposal.md`
- `openspec/changes/<slug>/specs/requirements.md`
- `docs/business/product_summary.md` (if not present)

## Subagent Role
**Name:** `matd-specifier`
**Persona:** see block-quote below.
**Skills loadout (in load order):**
- `stdd-product-spec-formats`
- `stdd-project-summary`
- `stdd-openspec`
- `stdd-ask-questions-if-underspecified`
- `general-grill-me`
- `general-grill-with-docs`
- `general-system-design`
- `general-verification-before-completion`
- `general-rtk-usage`
- `general-git-guardrails-claude-code`
- `general-finishing-a-development-branch`
- `general-using-git-worktrees`

> Persona source (read at dispatch time):
> `harness-tooling/.agents/plugins/matd/agents/matd-specifier.md`

## Optional second pass — matd-critical-thinker

After matd-specifier returns, ask the user whether to red-team the spec. If
yes:
- Subagent name: `matd-critical-thinker`
- Skills loadout: `stdd-ask-questions-if-underspecified`,
  `review-check-correctness`, `general-grill-me`, `general-grill-with-docs`,
  `general-verification-before-completion`, `general-rtk-usage`,
  `general-git-guardrails-claude-code`,
  `general-finishing-a-development-branch`,
  `general-using-git-worktrees`
- Persona source:
  `harness-tooling/.agents/plugins/matd/agents/matd-critical-thinker.md`

## Host Dispatch Flow — Claude Code

The main agent IS the orchestrator. Do NOT spawn a separate orchestrator
subagent.

1. Read the persona file at the path above.
2. Dispatch `matd-specifier` via the Task tool with the persona content +
   skill loadout as system prompt and the user's `$ARGUMENTS` as the user
   prompt.
3. After return, validate that `proposal.md` and `specs/requirements.md`
   exist (use `lib/validate_artifacts.py`).
4. Prompt the user: "Run matd-critical-thinker red-team pass? (y/n)".
5. If y, dispatch `matd-critical-thinker` with the same context plus the
   matd-specifier outputs.

## Host Dispatch Flow — OpenCode / Gemini

The main agent first spawns the orchestrator subagent, which then dispatches
the role subagent.

1. Spawn subagent `matd-orchestrator` with the skill loadout in §6.6 of
   `docs/specs/matd-speckit-extension-IMPLEMENTATION.md`.
2. Pass the orchestrator: `$ARGUMENTS`, persona path
   `harness-tooling/.agents/plugins/matd/agents/matd-specifier.md`, the
   skill loadout above, the artifact paths.
3. The orchestrator subagent spawns `matd-specifier` using its host's
   native subagent mechanism. **TBC** for exact syntax in OpenCode and
   Gemini.
4. After return, the orchestrator validates artifacts and prompts the user
   about the optional red-team pass.

## Validation / Gating

Before user gate, run:
- `python lib/validate_artifacts.py --change <slug> --kind proposal`
- `python lib/validate_artifacts.py --change <slug> --kind requirements`

Both must exit 0.

## User Gate

Show: "Stage 1 complete. Proposal: <path>. Requirements: <path>. Run stage
2 (design)? (y/n)". Wait for explicit y.
```

---

## 5. `commands/speckit.matd.design.md`

```markdown
---
description: "Stage 2: produce design.md, C4 diagrams, and ADRs via matd-architect."
tools: []
scripts: {}
---

# speckit.matd.design

## User Input
$ARGUMENTS

## Mission
Produce a technical blueprint: design.md, C4 diagrams
(Context/Container/Component/Code as warranted), data schema, ADRs, and
optional Deepwiki sync.

## Output Artifacts
- `docs/architecture/design.md`
- `docs/architecture/c4/*.md` (Context, Container, Component, Code as warranted)
- `docs/adr/<NNNN>-<slug>.md` (one or more)

## Subagent Role
**Name:** `matd-architect`
**Persona:** see block-quote below.
**Skills loadout (in load order):**
- `arch-c4-architecture`
- `arch-mermaid-diagrams`
- `arch-api-design-principles`
- `arch-architecture-patterns`
- `arch-design-system-patterns`
- `arch-smart-docs`
- `arch-writing-plans`
- `general-system-design`
- `general-improve-codebase-architecture`
- `general-grill-me`
- `stdd-openspec`
- `stdd-ask-questions-if-underspecified`
- `dev-backend-to-frontend-handoff`
- `orchestrate-dispatching-parallel-agents`
- `orchestrate-executing-plans`
- `orchestrate-multi-agent-patterns`
- `orchestrate-subagent-driven-development`
- `general-verification-before-completion`
- `general-rtk-usage`
- `general-git-guardrails-claude-code`
- `general-finishing-a-development-branch`
- `general-using-git-worktrees`

> Persona source (read at dispatch time):
> `harness-tooling/.agents/plugins/matd/agents/matd-architect.md`

## Host Dispatch Flow — Claude Code
Identical structure to `speckit.matd.specify` Claude Code flow; dispatch a
single `matd-architect` subagent with the loadout above.

## Host Dispatch Flow — OpenCode / Gemini
Identical structure to `speckit.matd.specify` OpenCode/Gemini flow;
orchestrator subagent dispatches `matd-architect`.

## Validation / Gating
- `python lib/validate_artifacts.py --change <slug> --kind design`
- Verify at least one C4 diagram exists (Context is mandatory).

## User Gate
"Stage 2 complete. Design: <path>. ADRs: <list>. Run stage 3 (refine)? (y/n)".
```

---

## 6. `commands/speckit.matd.refine.md`

```markdown
---
description: "Stage 3: delivery plan (architect) -> audit (critical-thinker) -> RED-state tests (qa)."
tools: []
scripts: {}
---

# speckit.matd.refine

## User Input
$ARGUMENTS

## Mission
Refine design into an executable delivery plan with 2–15-minute tasks,
audit the plan for clarity and risk, then produce failing E2E tests (RED
state).

## Output Artifacts
- `docs/delivery_plan.md`
- `docs/tasks/<task-id>.md` (one per task)
- `docs/audit/<slug>-audit.md`
- `tests/<feature-id>/test_*.py` (RED state — must fail)

## Subagent Sequence
1. **matd-architect** — produces delivery plan and task breakdown.
   Skills loadout: same 22 skills as §5.
2. **matd-critical-thinker** — audits plan for clarity, edge cases, risk.
   Skills loadout: 9 skills per §6.5.
3. **matd-qa** — authors failing E2E tests.
   Skills loadout: 16 skills per §6.3.

## Host Dispatch Flow — Claude Code
Three sequential Task-tool dispatches. After each subagent returns, the
main agent validates the artifact and decides whether to proceed.

## Host Dispatch Flow — OpenCode / Gemini
The orchestrator subagent runs the three dispatches in sequence using its
host's native subagent mechanism. **TBC** for exact syntax.

## Validation / Gating
- `python scripts/extract_acceptance_criteria.py` succeeds.
- `python scripts/validate_red_state.py` exits 0 (tests fail for the right
  reasons, not TEST_BROKEN or ENV_BROKEN).
- `python scripts/escalate_broken_tests.py` returns no escalations.

## User Gate
"Stage 3 complete. Delivery plan: <path>. RED tests: <count>. Run stage 4
(implement)? (y/n)".
```

---

## 7. `commands/speckit.matd.implement.md`

```markdown
---
description: "Stage 4: RED tests (qa) -> TDD loop max 20 iterations (dev) -> final audit (qa) -> PR (architect)."
tools: []
scripts: {}
---

# speckit.matd.implement

## User Input
$ARGUMENTS

## Mission
Execute the TDD loop: dev iterates against RED tests until GREEN, with a
hard 20-iteration cap. After GREEN, qa audits; architect finalizes the PR.

## Output Artifacts
- Source code passing all tests
- `docs/implementation/<slug>-notes.md`
- `docs/reviews/<slug>-final-audit.md`
- A GitHub pull request

## Subagent Sequence
1. **matd-qa** — re-confirms RED state. Skills per §6.3.
2. **matd-dev** — TDD loop. Skills per §6.4. Loop cap: `max: 20, until:
   "all tests pass"`. On cap-hit, halt and escalate.
3. **matd-qa** — final audit. Skills per §6.3.
4. **matd-architect** — opens PR with comprehensive summary. Skills per §6.2.

## Host Dispatch Flow — Claude Code
Four sequential Task-tool dispatches. Main agent enforces the loop counter
on step 2 and writes the iteration count to
`docs/implementation/<slug>-notes.md`.

## Host Dispatch Flow — OpenCode / Gemini
The orchestrator subagent runs the four dispatches. The loop counter is
maintained by the orchestrator, not by matd-dev. **TBC** for exact syntax.

## Validation / Gating
- `python scripts/validate_green_state.py` exits 0 after step 2.
- `python lib/evidence_validator.py --feature <slug>` exits 0 before step 4
  opens the PR.

## User Gate
"Implementation complete. Tests: <pass-count> / <total>. PR: <url>. Done."
```

---

## 8. `commands/speckit.matd.feat-workflow.md`

```markdown
---
description: "Run the full 4-stage matd workflow (specify -> design -> refine -> implement) with user gates between stages."
tools: []
scripts: {}
---

# speckit.matd.feat-workflow

## User Input
$ARGUMENTS

## Mission
Guide the user through the full matd workflow end-to-end, pausing for
explicit approval between stages.

## Output Artifacts
Union of stage 1–4 artifacts.

## Sequencing
This command is orchestrator-only. It does NOT spawn a role subagent. It
invokes the four stage commands in order, pausing at each user gate.

1. Invoke `speckit.matd.specify`. Wait for user gate.
2. Invoke `speckit.matd.design`. Wait for user gate.
3. Invoke `speckit.matd.refine`. Wait for user gate.
4. Invoke `speckit.matd.implement`.

## Host Dispatch Flow — Claude Code
Main agent runs the four commands sequentially via the host's internal
command-invocation mechanism (e.g. `/speckit.matd.specify`).

## Host Dispatch Flow — OpenCode / Gemini
Main agent spawns `matd-orchestrator` once at the start. Orchestrator runs
the four stage commands in sequence. Orchestrator persists across all four
stages.

## Validation / Gating
Each stage runs its own validation. This command adds no extra checks.

## User Gate
Implicit — the four stage commands each have their own gate.
```

---

## 9. `commands/speckit.matd.review.md`

```markdown
---
description: "Parallel architecture + QA review of an implementation."
tools: []
scripts: {}
---

# speckit.matd.review

## User Input
$ARGUMENTS

## Mission
Run matd-architect and matd-qa in parallel against the current branch's
changes. Reconcile verdicts.

## Output Artifacts
- `docs/reviews/<slug>-arch-review.md`
- `docs/reviews/<slug>-code-review.md`
- `docs/reviews/<slug>-verdict.md`

## Subagents
- **matd-architect** — architecture review. Skills per §6.2.
- **matd-qa** — code/test review. Skills per §6.3.

## Host Dispatch Flow — Claude Code
Main agent dispatches both via the Task tool in parallel (one tool-call
block with two invocations).

## Host Dispatch Flow — OpenCode / Gemini
Orchestrator subagent dispatches both in parallel using its host's
fan-out / parallel-subagent primitive. **TBC** for exact syntax in each
host.

## Validation / Gating
- `python scripts/detect_review_convergence.py` exits 0 (verdicts agree or
  the divergence is explicit and human-readable).

## User Gate
"Review complete. Arch verdict: <verdict>. Code verdict: <verdict>. Merge?
(y/n)".
```

---

## 10. `commands/speckit.matd.commit.md`

```markdown
---
description: "Evidence-gated git commit. Refuses on missing or invalid evidence."
tools: []
scripts: {}
---

# speckit.matd.commit

## User Input
$ARGUMENTS

## Mission
Validate evidence and create a git commit. No role subagent is spawned —
this is orchestrator-only.

## Output Artifacts
- One new git commit.
- `docs/workflow/<slug>-summary.md`

## Host Dispatch Flow — Claude Code
Main agent runs the validation scripts and creates the commit via Bash.

## Host Dispatch Flow — OpenCode / Gemini
Orchestrator subagent runs the same validation and commit sequence.

## Validation / Gating
- `python lib/evidence_validator.py --strict` exits 0.
- `python scripts/run_integration_checks.py` exits 0 (ruff, mypy, format).
- Working tree has staged changes.

## User Gate
"Evidence: ok. Files staged: <count>. Commit? (y/n)".
```

---

## 11. `commands/speckit.matd.update-docs.md`

```markdown
---
description: "Post-merge: matd-architect updates C4 diagrams and re-indexes the codebase."
tools: []
scripts: {}
---

# speckit.matd.update-docs

## User Input
$ARGUMENTS

## Mission
After a feature is merged, regenerate C4 diagrams (Context/Container/
Component/Code) and re-index the codebase (Code Graph Context / Deepwiki).

## Output Artifacts
- `docs/architecture/c4/*.md` (regenerated)
- Deepwiki index (regenerated)

## Subagent Role
**Name:** `matd-architect`
**Persona:** see block-quote below.
**Skills loadout:** same 22 skills as §5.

> Persona source: `harness-tooling/.agents/plugins/matd/agents/matd-architect.md`

## Host Dispatch Flow — Claude Code
Single Task-tool dispatch to `matd-architect`.

## Host Dispatch Flow — OpenCode / Gemini
Orchestrator subagent dispatches `matd-architect`.

## Validation / Gating
- Verify C4 Context diagram exists and is non-empty.
- Verify Deepwiki index regeneration command exited 0.

## User Gate
"Docs updated. <n> C4 diagrams regenerated. Done."
```

---

## 12. Per-Role Skill Loadouts (authoritative)

These lists are copied verbatim from
`/tmp/matd-speckit-research/matd-inventory.md` §B and from the matd plugin
agent files. **Do not modify**. If a command needs a different set,
escalate.

### 12.1 matd-specifier (model: default)
12 skills:
`stdd-product-spec-formats`, `stdd-project-summary`, `stdd-openspec`,
`stdd-ask-questions-if-underspecified`, `general-grill-me`,
`general-grill-with-docs`, `general-system-design`,
`general-verification-before-completion`, `general-rtk-usage`,
`general-git-guardrails-claude-code`,
`general-finishing-a-development-branch`, `general-using-git-worktrees`.

### 12.2 matd-architect (model: temperature 0.1)
22 skills:
`arch-c4-architecture`, `arch-mermaid-diagrams`,
`arch-api-design-principles`, `arch-architecture-patterns`,
`arch-design-system-patterns`, `arch-smart-docs`, `arch-writing-plans`,
`general-system-design`, `general-improve-codebase-architecture`,
`general-grill-me`, `stdd-openspec`,
`stdd-ask-questions-if-underspecified`,
`dev-backend-to-frontend-handoff`,
`orchestrate-dispatching-parallel-agents`,
`orchestrate-executing-plans`, `orchestrate-multi-agent-patterns`,
`orchestrate-subagent-driven-development`,
`general-verification-before-completion`, `general-rtk-usage`,
`general-git-guardrails-claude-code`,
`general-finishing-a-development-branch`, `general-using-git-worktrees`.

### 12.3 matd-qa (model: default)
16 skills:
`review-check-correctness`, `review-differential-review`,
`review-e2e-testing-patterns`, `review-openai-playwright`,
`review-systematic-debugging`, `review-webapp-testing`,
`review-simplify-complexity`, `python-testing-uv-playwright`,
`stdd-test-author-constrained`, `dev-tdd`,
`stdd-ask-questions-if-underspecified`,
`general-verification-before-completion`, `general-rtk-usage`,
`general-git-guardrails-claude-code`,
`general-finishing-a-development-branch`, `general-using-git-worktrees`,
`general-grill-me`.

### 12.4 matd-dev (model: temperature 0.2)
24 skills:
`dev-tdd`, `stdd-test-driven-development`,
`stdd-make-constrained-implementation`, `dev-alpine-js-patterns`,
`dev-backend-to-frontend-handoff`, `dev-database-migration`,
`dev-databases`, `python-async-patterns`, `python-code-style`,
`python-configuration`, `python-design-patterns`,
`python-fastapi-templates`, `python-packaging`,
`python-testing-uv-playwright`, `dev-diagnose`,
`stdd-ask-questions-if-underspecified`, `general-python-environment`,
`general-solid`, `general-verification-before-completion`,
`general-rtk-usage`, `general-git-guardrails-claude-code`,
`general-finishing-a-development-branch`, `general-using-git-worktrees`.

### 12.5 matd-critical-thinker (model: default)
9 skills:
`stdd-ask-questions-if-underspecified`, `review-check-correctness`,
`general-grill-me`, `general-grill-with-docs`,
`general-verification-before-completion`, `general-rtk-usage`,
`general-git-guardrails-claude-code`,
`general-finishing-a-development-branch`, `general-using-git-worktrees`.

### 12.6 matd-orchestrator (OpenCode / Gemini only — model: default, read-only)
16 skills:
`orchestrate-dispatching-parallel-agents`, `orchestrate-executing-plans`,
`orchestrate-finishing-a-development-branch`,
`orchestrate-multi-agent-patterns`,
`orchestrate-subagent-driven-development`,
`stdd-ask-questions-if-underspecified`, `stdd-openspec`,
`stdd-pm-linear-integration`,
`general-finishing-a-development-branch`,
`general-git-advanced-workflows`, `general-git-guardrails-claude-code`,
`general-python-environment`, `general-rtk-usage`, `general-solid`,
`general-system-design`, `general-using-git-worktrees`,
`general-verification-before-completion`.

---

## 13. Skill Bundling — Copy Commands

Inside the harness-tooling repo root, exactly:

```bash
mkdir -p spec-kit-multi-agent-tdd/skills
cp -r .agents/plugins/matd/skills/* spec-kit-multi-agent-tdd/skills/

# Verify byte-equal
diff -r .agents/plugins/matd/skills spec-kit-multi-agent-tdd/skills
# Expected: no output
```

Approximate count: 51 directories (see `ls .agents/plugins/matd/skills/ |
wc -l` at the time of writing). The plan / spec round this to "~45" for
readability.

---

## 14. `hooks/install.sh` — Pseudocode

The install hook MUST detect the host CLI and expose commands + skills at
the correct paths. Path mapping for OpenCode and Gemini is **TBC** —
implementation subagent verifies against each host's docs and updates this
section inline before declaring done.

```bash
#!/usr/bin/env bash
set -euo pipefail

EXTENSION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_ROOT="$(pwd)"
SPECIFY_DIR="${WORKSPACE_ROOT}/.specify"

echo "Installing matd extension v2.0.0..."

# --- Common: config + artifact dirs (unchanged from v1) ---
mkdir -p "${SPECIFY_DIR}/templates"
[[ -f "${SPECIFY_DIR}/matd-config.yml" ]] || \
  cp "${EXTENSION_DIR}/matd-config.yml.template" "${SPECIFY_DIR}/matd-config.yml"

for tpl in test-design implementation-notes arch-review code-review workflow-summary; do
  src="${EXTENSION_DIR}/templates/${tpl}-template.md"
  dst="${SPECIFY_DIR}/templates/${tpl}-template.md"
  [[ ! -f "$dst" && -f "$src" ]] && cp "$src" "$dst"
done

mkdir -p "${WORKSPACE_ROOT}/docs/tests/test-design" \
         "${WORKSPACE_ROOT}/docs/implementation" \
         "${WORKSPACE_ROOT}/docs/reviews/arch-review" \
         "${WORKSPACE_ROOT}/docs/reviews/code-review" \
         "${WORKSPACE_ROOT}/docs/workflow"

# --- Per-host skill exposure ---
expose_skills_claude() {
  echo "Detected Claude Code. Exposing skills to .claude/skills/."
  mkdir -p "${WORKSPACE_ROOT}/.claude/skills"
  cp -r "${EXTENSION_DIR}/skills/"* "${WORKSPACE_ROOT}/.claude/skills/"
}

expose_skills_opencode() {
  echo "Detected OpenCode. Exposing skills."
  # TBC: confirm path. Likely .opencode/skills/ — verify with subagent extension docs.
  mkdir -p "${WORKSPACE_ROOT}/.opencode/skills"
  cp -r "${EXTENSION_DIR}/skills/"* "${WORKSPACE_ROOT}/.opencode/skills/"
}

expose_skills_gemini() {
  echo "Detected Gemini / antigravity. Exposing skills."
  # TBC: confirm path. Likely .gemini/skills/ — verify with Gemini CLI docs.
  mkdir -p "${WORKSPACE_ROOT}/.gemini/skills"
  cp -r "${EXTENSION_DIR}/skills/"* "${WORKSPACE_ROOT}/.gemini/skills/"
}

# Detection: check for host marker files / env vars.
# Order: most specific first.
if [[ -d "${WORKSPACE_ROOT}/.claude" ]] || command -v claude >/dev/null 2>&1; then
  expose_skills_claude
fi
if [[ -d "${WORKSPACE_ROOT}/.opencode" ]] || command -v opencode >/dev/null 2>&1; then
  expose_skills_opencode
fi
if [[ -d "${WORKSPACE_ROOT}/.gemini" ]] || command -v gemini >/dev/null 2>&1; then
  expose_skills_gemini
fi

echo "matd extension v2.0.0 install complete."
```

Idempotency: every step is `mkdir -p` + conditional `cp`. Re-running is
safe.

---

## 15. `workflows/matd-tdd.yml` — Full Content

```yaml
---
schema_version: "1.0"
workflow:
  id: "matd-tdd"
  name: "MATD 4-stage TDD workflow"
  version: "2.0.0"
  author: "Daniel Minges"
  description: "Specify -> Design -> Refine -> Implement with user gates between stages."

requires:
  speckit_version: ">=0.1.0"
  integrations:
    any:
      - "claude"
      - "opencode"
      - "gemini"

inputs:
  feature_id:
    type: string
    required: true
    prompt: "Feature identifier (e.g. 'feat-123' or a short slug)"
  mode:
    type: string
    required: false
    default: "interactive"
    enum: ["interactive", "auto"]
    prompt: "Execution mode (interactive pauses at each gate; auto runs through)"

steps:
  - id: specify
    command: "speckit.matd.specify"
    input:
      args: "{{ inputs.feature_id }}"

  - id: gate-after-specify
    type: gate
    condition: "{{ inputs.mode == 'interactive' }}"
    message: "Stage 1 complete. Continue to design?"
    options: [approve, reject]
    on_reject: abort

  - id: design
    command: "speckit.matd.design"
    input:
      args: "{{ inputs.feature_id }}"

  - id: gate-after-design
    type: gate
    condition: "{{ inputs.mode == 'interactive' }}"
    message: "Stage 2 complete. Continue to refine?"
    options: [approve, reject]
    on_reject: abort

  - id: refine
    command: "speckit.matd.refine"
    input:
      args: "{{ inputs.feature_id }}"

  - id: gate-after-refine
    type: gate
    condition: "{{ inputs.mode == 'interactive' }}"
    message: "Stage 3 complete. Continue to implement?"
    options: [approve, reject]
    on_reject: abort

  - id: implement
    command: "speckit.matd.implement"
    input:
      args: "{{ inputs.feature_id }}"
```

Step types and field names cited from
`/tmp/matd-speckit-research/extension-system.md` lines 187–208.

---

## 16. Templates, lib, scripts — keep vs replace

| Path                                        | Action     | Reason |
| ------------------------------------------- | ---------- | ------ |
| `templates/`                                | Keep       | Artifact templates referenced by commands. |
| `lib/artifact_paths.py`                     | Keep       | Used by validators. |
| `lib/evidence_validator.py`                 | Keep       | Used by commit + implement. |
| `lib/validate_artifacts.py`                 | Keep       | Used by specify + design. |
| `lib/validate_manifests.py`                 | Keep       | Used by dev. |
| `lib/parse_test_evidence.py`                | Keep       | Used by implement. |
| `lib/test_runner.py`                        | Keep       | Used by implement. |
| `lib/generate_artifact.py`                  | Keep       | Template renderer. |
| `lib/human_feedback.py`                     | Keep       | Used by gates. |
| `lib/jira_local.py`                         | Keep       | Optional integration. |
| `lib/schemas/`                              | Keep       | JSON schemas. |
| `scripts/validate_red_state.py`             | Keep       | Used by refine. |
| `scripts/validate_green_state.py`           | Keep       | Used by implement. |
| `scripts/extract_acceptance_criteria.py`    | Keep       | Used by refine. |
| `scripts/escalate_broken_tests.py`          | Keep       | Used by refine. |
| `scripts/detect_review_convergence.py`      | Keep       | Used by review. |
| `scripts/parse_pytest_output.py`            | Keep       | Used by implement. |
| `scripts/run_integration_checks.py`         | Keep       | Used by commit. |
| `scripts/validate_artifact_structure.py`    | Keep       | Used by specify/design. |
| `scripts/validate_feature_artifacts.py`     | Keep       | Used by review. |
| `commands/*.md` (existing 8)                | Replace    | New names, new structure (see §3–11). |
| `extension.yml`                             | Replace    | Bump to 2.0.0, new command set, integrations clause. |
| `extension.json`                            | Replace or delete | Spec-kit reads `extension.yml`. `extension.json` is legacy — confirm not required by current CLI, then delete. **TBC**. |
| `workflows/matd-tdd.yml`                    | Replace    | 4 stages + gates (see §15). |
| `hooks/install.sh`                          | Replace    | Per-host branches (see §14). |
| `hooks/config.yml`                          | Keep       | Claude Code PreToolUse hooks. |
| `commands/MIGRATION.md`                     | Update     | Append note about v1->v2 transition. |
| `README.md`, `USER-GUIDE.md`, `CHANGELOG.md`| Update     | Reflect v2.0.0 changes. |

---

## 17. STDD Cleanup (non-blocking)

Out of scope for the core conversion but completed in the same branch.
Three files MUST be deleted, all OUTSIDE `.agents/plugins/matd/`:

1. `harness-tooling/.agents/agents/stdd-solution-design-subagent.md`
2. `harness-tooling/.agents/docs/stdd-workflow.md`
3. `harness-tooling/.agents/docs/research_stdd_workflows.md`

Preserve all `stdd-*` skill directories under
`.agents/plugins/matd/skills/`. The matd agents reference them.

After deletion, if there is a marketplace plan that references any of
these three files, annotate it with a brief note that they were removed
(do not invent or rewrite the marketplace plan content).

This cleanup is non-blocking: if it fails or is contested, the extension
can still ship.

---

## 18. Validation Contract

Before declaring the implementation done, the QA subagent MUST verify:

1. **Manifest validity.** `specify extension add --dev
   /workspace/harness-tooling/spec-kit-multi-agent-tdd` inside the
   sandbox container returns exit 0. Capture the full output.
2. **Command registration.** `specify extension info matd` lists all 8
   `speckit.matd.*` commands.
3. **Skill copy correctness.** `diff -r .agents/plugins/matd/skills
   spec-kit-multi-agent-tdd/skills` produces no output.
4. **Plugin untouched.** `git status --short .agents/plugins/matd/` is
   empty.
5. **Sandbox untouched.** No staged or unstaged changes in
   `harness-sandbox/`.
6. **STDD cleanup.** Three files are deleted from disk and git index.
7. **Workflow registration.** `specify workflow list` shows `matd-tdd`.
8. **Idempotent install.** Run `hooks/install.sh` twice; the second run
   produces no new files (capture before/after `ls -la` and confirm).
9. **Host-skill exposure.** On Claude Code: `ls .claude/skills/` lists
   all ~51 skills. On OpenCode/Gemini: verify per the path discovered
   during research (TBC).
10. **Command-body completeness.** Each of the 8 command files contains
    both labeled dispatch flows ("Host Dispatch Flow — Claude Code" and
    "Host Dispatch Flow — OpenCode / Gemini"). Use `grep -l` to confirm.

The QA subagent SHALL output each check's evidence as a single block in
the final report. No claim of done without evidence.
