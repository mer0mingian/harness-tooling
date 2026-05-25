# Spec: matd as Spec-Kit Extension

**Status:** Ready for implementation
**Date:** 2026-05-25
**Branch:** `feat/matd-as-speckit-extension`
**Story Points:** 8

---

## 1. Context & Problem Statement

The matd (Multi-Agent Test-Driven) workflow currently exists in two forms:

1. A mature Claude Code plugin at
   `/home/minged01/repositories/harness-workplace/harness-tooling/.agents/plugins/matd/`.
   Six agents, ~45 bundled skills, eight commands. Production-ready
   (v1.8.0), Claude-Code-only.
2. A spec-kit scaffold at
   `/home/minged01/repositories/harness-workplace/harness-tooling/spec-kit-multi-agent-tdd/`.
   Schema-1.0 manifest, eight Markdown commands, nine templates, validation
   scripts. Phase-4 Python-to-Markdown migration left an unresolved gap: the
   scaffold cannot dispatch named role agents because spec-kit has no native
   "agent" concept (see
   `/tmp/matd-speckit-research/extension-system.md` lines 279–292).

The result: matd is locked to Claude Code. OpenCode users and Gemini /
antigravity users have no path to the same workflow.

This spec converts the spec-kit scaffold into a working v2.0.0 extension
that runs on three host CLIs by exploiting each host's native subagent
dispatch primitive. The Claude Code plugin remains a primary delivery
channel; this is an additive change.

## 2. Goals

- **G1.** Ship a spec-kit extension at `spec-kit-multi-agent-tdd/` with
  `extension.id: "matd"`, `extension.version: "2.0.0"`,
  `schema_version: "1.0"` that installs cleanly via `specify extension add
  --dev <path>` on Claude Code, OpenCode (with subagent extension), and
  antigravity / Gemini.
- **G2.** Provide eight `speckit.matd.*` commands covering the full
  4-stage matd workflow plus review/commit/update-docs.
- **G3.** Each command body inline-instructs the host CLI to spawn a named
  role subagent loaded with a named skill set. The dispatch is delegated to
  the host's native subagent mechanism — the extension itself is dispatch-
  agnostic.
- **G4.** Bundle all ~45 skills currently shipped in
  `.agents/plugins/matd/skills/` inside the extension package so the install
  hook can expose them to whichever host CLI is in use.
- **G5.** Preserve the existing Claude Code plugin at
  `.agents/plugins/matd/` unchanged. No regression.
- **G6.** Provide a workflow `workflows/matd-tdd.yml` that sequences the
  four stages with explicit user-approval gates between each.

## 3. Non-Goals

- Adding agent-dispatch primitives to spec-kit itself.
- Publishing to a public spec-kit catalog. Local-dev install is sufficient
  for v2.0.0.
- Modifying `harness-sandbox/`. Spec-kit CLI is already present in the
  container.
- Supporting hosts other than Claude Code, OpenCode, and Gemini /
  antigravity.
- Genericising stdd-* skills for non-matd reuse.
- Removing the Claude Code plugin at `.agents/plugins/matd/`.

## 4. Functional Requirements

### FR1. Extension installs via `specify extension add --dev`

Running `specify extension add --dev <path-to-spec-kit-multi-agent-tdd>`
SHALL succeed without schema errors. The manifest SHALL conform to
schema_version 1.0 as documented in
`/tmp/matd-speckit-research/extension-system.md` lines 49–88.

### FR2. Extension uninstalls via `specify extension remove matd`

The uninstall path SHALL remove all files written by the install hook to
host-CLI-specific directories (`.claude/commands/`, `.claude/skills/`,
`.opencode/...`, `.gemini/...`). The Claude Code plugin at
`.agents/plugins/matd/` SHALL NOT be touched by the uninstaller.

### FR3. Command `speckit.matd.feat-workflow` — full 4-stage workflow

The command SHALL guide the user through specify → design → refine →
implement sequentially. Each stage requires explicit user approval before
proceeding. Maps from
`/home/minged01/repositories/harness-workplace/harness-tooling/.agents/commands/matd-feat-workflow.md`.

### FR4. Command `speckit.matd.specify` — feature specification

The command SHALL spawn the matd-specifier role subagent (skills per §6.1)
to draft OpenSpec proposal and `specs/requirements.md`, then optionally
spawn matd-critical-thinker for red-team review. Maps from
`matd-01-specification.md` plus the existing `specify-product-brief.md`.

### FR5. Command `speckit.matd.design` — solution design

The command SHALL spawn the matd-architect role subagent (skills per §6.2)
to produce design.md, C4 diagrams (Context/Container/Component/Code as
warranted), and ADRs. Maps from `matd-02-design.md` plus
`specify-solution-design.md` plus `specify-adr.md`.

### FR6. Command `speckit.matd.refine` — technical refinement

The command SHALL spawn matd-architect (delivery plan), then
matd-critical-thinker (audit), then matd-qa (RED-state tests). Maps from
`matd-03-refine.md`.

### FR7. Command `speckit.matd.implement` — TDD implementation loop

The command SHALL spawn matd-qa to produce RED-state tests, then matd-dev
for a TDD loop (max 20 iterations, halt condition: all tests pass), then
matd-qa for final audit, then matd-architect to finalize the PR. Maps from
`matd-04-implement.md` plus `commands/implement.md` plus `commands/test.md`.

### FR8. Command `speckit.matd.review` — parallel review

The command SHALL spawn matd-architect and matd-qa in parallel and reconcile
verdicts. Maps from the existing `spec-kit-multi-agent-tdd/commands/review.md`.

### FR9. Command `speckit.matd.commit` — evidence-gated commit

The command SHALL validate evidence (test output, artifact completeness)
and create a git commit only on success. Orchestrator-only; no role subagent
is spawned.

### FR10. Command `speckit.matd.update-docs` — post-implementation docs

The command SHALL spawn matd-architect to update C4 diagrams and the Code
Graph Context index after a feature is merged.

### FR11. Per-host dispatch contract

Every command body SHALL contain TWO clearly labeled dispatch flows:

- **Claude Code flow.** The main agent assumes the matd-orchestrator role
  itself and dispatches the role subagent via the Task tool.
- **OpenCode / Gemini flow.** The main agent first spawns a
  matd-orchestrator subagent (read-only, orchestration skills only); that
  subagent then dispatches the role subagent.

The host CLI SHALL select the relevant flow based on which integration is
active. Selection logic lives inside the command body's narrative
instructions, not inside spec-kit machinery.

## 5. Non-Functional Requirements

### NFR1. Version pinning

`extension.version` SHALL be `"2.0.0"` (MAJOR bump from the previous
scaffold's `1.0.0` because the dispatch model and command set are
incompatible). `schema_version` SHALL remain `"1.0"` per spec-kit's
current schema.

### NFR2. Manifest validity

`extension.yml` SHALL pass spec-kit's manifest validation. All required
fields per
`/tmp/matd-speckit-research/extension-system.md` §D table (lines 296–329)
SHALL be present.

### NFR3. Skill exposure across hosts

After install, every bundled skill SHALL be discoverable by the host CLI
through the path that host scans. For Claude Code this is
`.claude/skills/`; for OpenCode and Gemini the path is TBC and MUST be
verified by the implementation subagent against each host's
documentation.

### NFR4. No regression of the Claude Code plugin

`git status -- .agents/plugins/matd/` SHALL report clean after the branch
is complete. No file inside the plugin SHALL be modified, moved, or
deleted.

### NFR5. No regression of harness-sandbox

`git status` in the `harness-sandbox/` repo SHALL report clean. No
Dockerfile, compose, or entrypoint changes.

### NFR6. Command-name format

All command names SHALL match the pattern `^speckit\.matd\.[a-z0-9-]+$`
per
`/tmp/matd-speckit-research/extension-system.md` lines 131–134.

### NFR7. Deterministic install hook

`hooks/install.sh` SHALL be idempotent. Running it twice in a row SHALL
produce the same end state and SHALL NOT prompt the user a second time.

## 6. User-Visible Behavior

When the user runs each command, the host CLI does the following:

### `speckit.matd.feat-workflow`
The host prints a brief workflow summary, then runs `speckit.matd.specify`
and pauses for approval. On approve, runs `speckit.matd.design`, pauses;
then `speckit.matd.refine`, pauses; then `speckit.matd.implement`. Each
pause shows a one-line summary of what was just produced.

### `speckit.matd.specify`
The user sees the host announce it is dispatching matd-specifier with the
documented skill loadout. After the subagent returns, the host announces
it is dispatching matd-critical-thinker for red-team review (skippable).
Final output: a path to the OpenSpec proposal and `specs/requirements.md`.

### `speckit.matd.design`
The host dispatches matd-architect and reports back with paths to design.md,
generated C4 diagrams, and ADRs. The user is prompted to review before
moving on.

### `speckit.matd.refine`
The host dispatches matd-architect → matd-critical-thinker → matd-qa in
sequence. Final output: a delivery plan, an audit log, and a set of
failing E2E tests (RED state).

### `speckit.matd.implement`
The host dispatches matd-qa for tests, then matd-dev for TDD iterations
(loop counter visible to the user, max 20). The user sees per-iteration
test output. On all-green, matd-qa runs a final audit, then matd-architect
opens a PR.

### `speckit.matd.review`
The host dispatches matd-architect and matd-qa in parallel. Final output:
a merged review verdict.

### `speckit.matd.commit`
The host runs validation scripts, prints the evidence summary, and either
commits or refuses with a clear reason.

### `speckit.matd.update-docs`
The host dispatches matd-architect to update C4 diagrams and re-index the
codebase.

## 7. Acceptance Criteria

- [ ] **FR1.** `specify extension add --dev
      /workspace/harness-tooling/spec-kit-multi-agent-tdd` returns exit 0
      inside the sandbox container.
- [ ] **FR2.** `specify extension remove matd` removes all host-CLI files
      and leaves `.agents/plugins/matd/` untouched.
- [ ] **FR3.** `speckit.matd.feat-workflow` sequences the four stages with
      visible user gates.
- [ ] **FR4.** `speckit.matd.specify` dispatches a subagent named
      `matd-specifier` with the exact 12 skills listed in §6.1.
- [ ] **FR5.** `speckit.matd.design` dispatches a subagent named
      `matd-architect` with the exact 22 skills listed in §6.2.
- [ ] **FR6.** `speckit.matd.refine` dispatches three subagents in order.
- [ ] **FR7.** `speckit.matd.implement` enforces the 20-iteration loop cap
      and short-circuits when all tests pass.
- [ ] **FR8.** `speckit.matd.review` shows both parallel review outputs.
- [ ] **FR9.** `speckit.matd.commit` refuses to commit when evidence is
      missing.
- [ ] **FR10.** `speckit.matd.update-docs` regenerates C4 diagrams.
- [ ] **FR11.** Every command body contains both dispatch flows, each
      under its own labeled heading.
- [ ] **NFR1.** `grep -F 'extension.version: "2.0.0"' extension.yml`
      returns a match.
- [ ] **NFR2.** Spec-kit's manifest validator reports zero errors.
- [ ] **NFR3.** Skills are discoverable in the host's expected directory
      after install. Per host: Claude Code verified; OpenCode and Gemini
      paths verified per implementation subagent's research (TBC at spec
      time).
- [ ] **NFR4.** `git diff --name-only .agents/plugins/matd/` is empty.
- [ ] **NFR5.** `harness-sandbox/` has no changes on this branch.
- [ ] **NFR6.** All eight command names match the regex.
- [ ] **NFR7.** Running `hooks/install.sh` twice produces an unchanged
      filesystem on the second run.

## 8. Glossary

- **matd.** Multi-Agent Test-Driven workflow. Six named roles, four
  workflow stages, evidence-gated commits.
- **spec-kit.** GitHub's command-extension framework for AI agents.
  Universal Markdown command format auto-converts to host-specific
  formats. Native concepts: extensions, workflows, templates, hooks.
- **host CLI.** The agent runtime that consumes spec-kit commands. Three
  in scope: Claude Code, OpenCode (with subagent extension), Gemini /
  antigravity.
- **role subagent.** A short-lived subagent dispatched by the orchestrator
  to perform a single workflow role (specifier, architect, qa, dev,
  critical-thinker). Persona and skill loadout are specified in the
  command body.
- **orchestrator.** The coordinator that sequences role subagents and
  enforces user gates. On Claude Code, the main agent IS the orchestrator.
  On OpenCode / Gemini, a matd-orchestrator subagent is spawned first.
- **skill loadout.** The exact, ordered list of skill names a role
  subagent must load before doing its work. Skill lists are defined
  per-role in §6 below.
