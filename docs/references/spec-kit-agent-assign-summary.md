# spec-kit-agent-assign — Reference Summary

**Source:** https://github.com/xymelon/spec-kit-agent-assign
**Inspected:** 2026-06-08
**Version inspected:** `1.1.0` (per `extension.yml`, CHANGELOG `[1.1.0] - 2026-04-28`)
**License:** MIT · **Requires:** `speckit_version: ">=0.7.1"`

A [GitHub Spec Kit](https://github.com/github/spec-kit/) extension that routes each task in `tasks.md` to a specialized Claude Code agent, instead of running everything in one flat `/speckit.implement` context. Three phases: **assign → validate → execute**.

---

## How it hooks into Spec Kit

From `extension.yml`:

- **Extension id:** `agent-assign` (`extension.id`); manifest `schema_version: "1.0"`.
- **Command naming:** `speckit.agent-assign.<command>` (registered under `provides.commands`).
- **`requires.commands`:** `speckit.tasks`, `speckit.implement`.
- **`after_tasks` hook** (`hooks.after_tasks`): after `/speckit.tasks` generates `tasks.md`, the extension can auto-trigger assignment.
  - `command: "speckit.agent-assign.assign"`, `optional: true`, `prompt: "Assign agents to the generated tasks?"`.
  - Per CHANGELOG 1.1.0 note: extension commands are hook *providers*, not consumers — the inline "check for extension hooks" blocks were removed from the command files.

Pipeline position (README "Workflow Integration"):
```
/speckit.tasks                 → tasks.md
/speckit.agent-assign.assign   → agent-assignments.yml        ← NEW
/speckit.agent-assign.validate → validation report            ← NEW
/speckit.agent-assign.execute  → implemented project          ← REPLACES /speckit.implement
```

Each command's frontmatter declares `scripts.sh` / `scripts.ps` pointing at `check-prerequisites.sh --json --require-tasks` (execute adds `--include-tasks`), invoked via the `{SCRIPT}` placeholder. Setup step parses `FEATURE_DIR` and `AVAILABLE_DOCS`. `assign` and `validate` also declare `handoffs` chaining to the next command.

---

## The three commands

### `speckit.agent-assign.assign` (`commands/assign.md`)
Scans agents, auto-matches each task, writes the YAML mapping.
- **Inputs:** `tasks.md` (required, else suggests `/speckit.tasks`); discovered agent files; optional `$ARGUMENTS`.
- **Steps:** Setup → Scan agents (build **Agent Registry** table) → Load tasks → Auto-match → **Present assignments table for confirmation** (Accept all / Modify e.g. `T003 → api-specialist` / Abort) → Write file → Report.
- **Outputs:** `FEATURE_DIR/agent-assignments.yml`; report with path, total assigned, per-agent breakdown, count of `default`.
- If no agent files found at any level: **STOP** and recommend plain `/speckit.implement`.

### `speckit.agent-assign.validate` (`commands/validate.md`)
**Read-only** consistency check; modifies nothing.
- **Inputs (required):** `agent-assignments.yml`, `tasks.md`; rescans current agent registry.
- If `agent-assignments.yml` missing: **STOP**, tell user to run `assign` first.
- **Outputs:** structured **Validation Report** (summary metrics table, per-task status, issues list, recommended actions) and a **PASS / FAIL** verdict. PASS → suggest `execute`; FAIL → suggest re-`assign`.

### `speckit.agent-assign.execute` (`commands/execute.md`)
Agent-aware replacement for `/speckit.implement`.
- **Inputs (required):** `tasks.md`, `agent-assignments.yml`, `plan.md`; optional `spec.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`.
- **Steps:** Setup → check assignment file → load context → project ignore-file verification (git/.dockerignore/.eslintignore/.prettierignore/.npmignore/.terraformignore/.helmignore — same as `implement`) → parse phases → **execute phase-by-phase**.
- **Execution modes per task:**
  - **Mode A — `default`:** run inline in current context (standard implement behavior).
  - **Mode B — named agent:** spawn the assigned agent as a dedicated subagent, given task id+description, plan/data-model/contract context, target file paths, and prior-task context; then verify its output.
- **Ordering:** complete each phase before next; sequential tasks in order; `[P]` tasks on *different* agents may run in parallel; tasks touching the same files stay sequential regardless of `[P]`.
- **Fallback:** if an agent file is missing at execution time, fall back to `default` with a warning.
- **Outputs:** marks tasks `[X]` in `tasks.md`; per-task ✓/✗ progress, per-phase summaries, final **Execution Summary** table + "agents used" counts.

---

## Agent scanning hierarchy

Follows Claude Code's official priority (high overrides low), per `CLAUDE.md` and `assign.md` step 2:

1. **Project-level (high):** `.claude/agents/*.md` in repo root
2. **User-level (low):** `~/.claude/agents/*.md` in home dir

For each file: parse YAML frontmatter for `name` (defaults to filename minus `.md` if absent) and `description`; record source level (`project`/`user`). **Dedup/override:** if the same agent name appears at multiple levels, keep only the highest-priority definition. `validate` re-runs the same scan to build a "Current Agent Registry" for drift comparison.

---

## `agent-assignments.yml` schema

Written to `FEATURE_DIR/` alongside `tasks.md`. Shape (from `assign.md` / README):

```yaml
# Agent Assignments
# Feature: <feature-name from plan.md or branch name>
# Generated: <timestamp>
# Command: /speckit.agent-assign.assign

agents_scanned:
  - name: "backend-dev"
    source: "project"          # project | user
    description: "Backend development specialist"
  - name: "frontend-dev"
    source: "project"
    description: "Frontend React/TypeScript specialist"

assignments:
  T001:
    agent: "default"           # "default" = run inline, no specialized agent
    reason: "General setup task, no specialized agent needed"
  T002:
    agent: "backend-dev"
    reason: "Task involves data model creation, matches backend-dev capabilities"
```

Top-level keys: **`agents_scanned`** (list of `name`/`source`/`description`) and **`assignments`** (map of task id → `{agent, reason}`).

---

## Assignment matching logic

`assign.md` step 4 — for each task, analyze description + file paths against each agent's description/capabilities, considering:
- **File-path patterns:** e.g. `src/api/` → API agent, `src/models/` → backend, `tests/` → test agent.
- **Task action keywords:** "Create model" → backend, "Write test" → test-writer, "Implement UI" → frontend.
- **Story context & phase:** Setup tasks may warrant a different agent than Polish tasks.

Every task gets a proposed assignment; if no agent fits, assign `default`. Task lines parsed as `- [ ] [TaskID] [P?] [Story?] Description with file path`.

---

## Validation checks (`validate.md` step 5)

1. **Coverage** — every task id in `tasks.md` has an `assignments` entry (`OK` / `UNASSIGNED`).
2. **Agent existence** — every referenced agent (except `default`) exists in current registry (`OK` / `MISSING`).
3. **Conflicts** — no agent name at multiple hierarchy levels with differing definitions (`OK` / `CONFLICT`).
4. **Drift** — compare `agents_scanned` against current registry; report agents removed since, or new agents added since, assignment.
5. **Frontmatter validity** — each referenced agent file has valid YAML frontmatter with at least a `description` (`OK` / `INVALID`).

---

## Reuse for per-step MATD agent assignment

Goal: assign distinct MATD agents to steps of a `speckit-matd-specify-prd` workflow.

- **Adopt the YAML mapping pattern.** A `agent-assignments.yml`-style file (keys `agents_scanned` + `assignments` with `{agent, reason}`) is a clean, validatable way to pin each PRD/MATD *step* (rather than task id) to a named agent — the same provider could key on step ids instead of `T0xx`.
- **Reuse the scan + dedup hierarchy.** Discovery of `.claude/agents/*.md` (project) over `~/.claude/agents/*.md` (user) with highest-priority-wins dedup already matches how MATD agents are installed; the registry/frontmatter parsing is directly portable.
- **Reuse validate-before-execute gating.** The five checks (coverage, existence, conflicts, drift, frontmatter) give a read-only gate that fits MATD's verification-before-completion discipline — run a "validate" pass before spawning per-step agents.
- **Reuse Mode B subagent spawning + `default` fallback.** The execute pattern (named agent → spawn dedicated subagent with scoped context + verify output; missing agent → fall back to `default` with warning; respect phase ordering and `[P]` parallelism) maps onto running each MATD workflow step under its assigned specialist with a safe generalist fallback.

> Note: matching here is keyword/path-based heuristic in the assign command's *prompt* (not a coded algorithm), and the extension keys on Spec Kit task ids in `tasks.md`. For MATD steps you'd adapt the matching prompt and key on step/command names; the storage schema, hierarchy scan, validation checks, and spawn/fallback execution model carry over as-is.
