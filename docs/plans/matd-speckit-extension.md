# Plan: matd as Spec-Kit Extension

**Status:** Ready for execution
**Date:** 2026-05-25
**Branch:** `feat/matd-as-speckit-extension`
**Story Points:** 8

---

## 1. Goal & Scope

Convert the existing matd Claude Code plugin at `.agents/plugins/matd/` into a
spec-kit extension under `spec-kit-multi-agent-tdd/`, while preserving the
plugin as a primary delivery channel. The extension MUST install cleanly on
three host CLIs (Claude Code, OpenCode with subagent extension, Gemini /
antigravity) and dispatch named role subagents loaded with named skill sets.

Cross-references:
- Spec: `docs/specs/matd-speckit-extension.md`
- Implementation contract: `docs/specs/matd-speckit-extension-IMPLEMENTATION.md`
- Implementation prompt: `docs/specs/matd-speckit-extension-PROMPT.md`

## 2. Out of Scope

- Modifications to `harness-sandbox/` (spec-kit CLI is already present in the
  container; no Dockerfile changes in this branch).
- Removal of the Claude Code plugin at `.agents/plugins/matd/`. It stays.
- Publishing to a public spec-kit catalog. Local-dev install (`specify
  extension add --dev`) and private-URL install are the only delivery modes
  in v2.0.0.
- Genericising stdd-* skills for non-matd reuse.
- A new orchestration mechanism inside spec-kit itself. The extension
  delegates dispatch to each host CLI's native subagent feature.

## 3. Branch & Locations

| Path                                                  | Action               |
| ----------------------------------------------------- | -------------------- |
| `spec-kit-multi-agent-tdd/`                           | Rework in place      |
| `spec-kit-multi-agent-tdd/extension.yml`              | Bump to `2.0.0`      |
| `spec-kit-multi-agent-tdd/commands/`                  | Replace all 8 files  |
| `spec-kit-multi-agent-tdd/skills/`                    | New, copied from plugin |
| `spec-kit-multi-agent-tdd/workflows/matd-tdd.yml`     | Replace with 4-stage workflow |
| `spec-kit-multi-agent-tdd/hooks/install.sh`           | Replace, add per-host branches |
| `.agents/plugins/matd/**`                             | Untouched             |
| `.agents/agents/stdd-solution-design-subagent.md`     | Delete (non-blocking) |
| `.agents/docs/stdd-workflow.md`                       | Delete (non-blocking) |
| `.agents/docs/research_stdd_workflows.md`             | Delete (non-blocking) |
| `harness-sandbox/**`                                  | Untouched             |

## 4. Target Hosts

Three hosts only. Each is verified during the install hook:

- **Claude Code** — uses `.claude/commands/`; native subagent mechanism is
  the Task tool.
- **OpenCode** — requires the subagent extension; uses `.opencode/commands/`
  (path TBC — see §9).
- **antigravity / Gemini** — uses `.gemini/commands/` with TOML conversion
  (path TBC — see §9).

## 5. Dispatch Model Summary

The extension does **not** ship agent definition files. Each spec-kit command
body inline-instructs the host CLI to spawn a named subagent loaded with a
named skill set. Two flows, one per host family:

- **Claude Code flow.** The main agent reads the command body and assumes
  the matd-orchestrator role itself. It then dispatches role subagents
  (matd-specifier, matd-architect, matd-qa, matd-dev, matd-critical-thinker)
  via the Task tool, supplying the per-role skill list and persona pointer.
- **OpenCode / Gemini flow.** The main agent first spawns a
  matd-orchestrator subagent (read-only, orchestration skills). That
  subagent then dispatches the role subagent.

Every command body in `commands/*.md` carries BOTH flows, clearly labeled.
The host CLI picks the relevant branch based on which integration is active.

## 6. Skill Bundling Strategy

Copy all ~45 skills from `.agents/plugins/matd/skills/*` into
`spec-kit-multi-agent-tdd/skills/*` (exact copy, no edits). The install hook
then exposes them to whichever host the project uses:

- Claude Code: symlink or copy into `.claude/skills/` (existing convention).
- OpenCode: TBC. Subagent extension docs to be consulted by implementation
  subagent.
- Gemini: TBC. Same.

Rationale: spec-kit has no native "skill" concept (see
`/tmp/matd-speckit-research/extension-system.md` lines 279–292). We bundle
the files inside the extension package and let the install hook expose them
to the host CLI that consumes them.

## 7. Subagent Sequencing (6 implementation tasks)

The implementation will be executed by subagents dispatched from the
orchestrator. Each task is small enough to fit a single agent context.

| # | Task                                                          | Skills loaded                                    | Story points |
| - | ------------------------------------------------------------- | ------------------------------------------------ | ------------ |
| 1 | Rewrite `extension.yml` to schema 1.0, extension.version 2.0.0, 8 commands | arch-writing-plans                              | 1 |
| 2 | Rewrite the 8 command bodies under `commands/`               | arch-writing-plans, stdd-openspec                | 2 |
| 3 | Copy ~45 skills from plugin into `skills/`                    | general-rtk-usage                                | 1 |
| 4 | Rewrite `workflows/matd-tdd.yml` (4 stages + gates)           | arch-writing-plans                               | 1 |
| 5 | Rewrite `hooks/install.sh` with per-host skill exposure       | general-rtk-usage, general-verification-before-completion | 1 |
| 6 | Delete 3 STDD files; run `specify extension add --dev` dry-run inside sandbox; report errors | general-verification-before-completion, general-using-git-worktrees | 2 |

Tasks 1–5 are sequential (each depends on the prior file's structure).
Task 6 is the final validation gate.

## 8. Risks & Open Follow-ups

1. **OpenCode / Gemini skill-discovery paths are TBC.** Implementation
   subagent must verify from each CLI's documentation what directory the
   host scans for skills, and update IMPLEMENTATION.md inline before
   finishing. This is the single largest open question.
2. **OpenCode subagent dispatch syntax is TBC.** Whether OpenCode accepts a
   Claude-Code-style Task tool call, a slash command, or a different
   dispatch primitive needs to be confirmed against the subagent
   extension's docs.
3. **Gemini TOML conversion.** Spec-kit auto-converts universal Markdown
   commands to TOML for Gemini (see
   `/tmp/matd-speckit-research/extension-system.md` lines 274–276). Verify
   that the dispatch instructions survive the conversion, especially
   block-quoted persona pointers.
4. **Skill-name collisions.** If a host CLI already exposes a skill with the
   same name as one we bundle, the install hook should detect and warn.
   Resolution TBC; for v2.0.0 we accept "first one wins" with a warning.
5. **STDD cleanup is non-blocking.** Deleting `stdd-solution-design-subagent.md`,
   `stdd-workflow.md`, and `research_stdd_workflows.md` is a separate
   concern; if it fails or is contested, the extension can still ship.

## 9. Acceptance Criteria

- [ ] `spec-kit-multi-agent-tdd/extension.yml` declares
      `extension.version: "2.0.0"`, `schema_version: "1.0"`,
      `requires.integrations.any: [claude, opencode, gemini]`, all 8
      commands.
- [ ] All 8 command files exist and each one contains both host dispatch
      flows (Claude Code main-agent flow + OpenCode/Gemini
      orchestrator-subagent flow) clearly labeled.
- [ ] `spec-kit-multi-agent-tdd/skills/` contains all ~45 skill
      directories from `.agents/plugins/matd/skills/`, byte-equal to the
      source.
- [ ] `spec-kit-multi-agent-tdd/workflows/matd-tdd.yml` defines the 4
      stages (specify, design, refine, implement) with explicit user
      gates between each.
- [ ] `hooks/install.sh` detects the host CLI and exposes commands +
      skills at the correct paths for each. Each branch logs which host
      was detected.
- [ ] `.agents/plugins/matd/` is untouched on disk (verified with `git
      status -- .agents/plugins/matd`).
- [ ] `harness-sandbox/` has no changes on this branch.
- [ ] The 3 STDD files outside the plugin are deleted.
- [ ] Running `specify extension add --dev
      /workspace/harness-tooling/spec-kit-multi-agent-tdd` inside the
      sandbox container reports no schema errors. Output captured.
- [ ] `specify extension list` inside the sandbox shows `matd@2.0.0`.

## 10. Docker Sandbox Test Commands

Copy-paste-runnable. Run after each task to catch regressions early. Replace
`<workspace>` with the project workspace path.

```bash
# Start the sandbox
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

# Sanity: spec-kit CLI is present
rtk docker exec harness-agent-sta2e-agent-workspace specify --version

# Dev-install the extension
rtk docker exec harness-agent-sta2e-agent-workspace specify extension add --dev \
  /workspace/../harness-tooling/spec-kit-multi-agent-tdd

# List installed extensions; expect matd@2.0.0
rtk docker exec harness-agent-sta2e-agent-workspace specify extension list

# Show registered commands; expect 8 speckit.matd.* entries
rtk docker exec harness-agent-sta2e-agent-workspace specify extension info matd

# Verify Claude Code sees the commands (file presence check)
rtk docker exec harness-agent-sta2e-agent-workspace ls /workspace/.claude/commands/ \
  | rtk grep speckit.matd

# Verify the skills landed where the host expects them (Claude Code path)
rtk docker exec harness-agent-sta2e-agent-workspace ls /workspace/.claude/skills/ \
  | rtk grep -E "stdd-|arch-|dev-|orchestrate-"

# Verify the workflow is registered
rtk docker exec harness-agent-sta2e-agent-workspace specify workflow list \
  | rtk grep matd-tdd

# Smoke-test one command end-to-end (Claude Code only here)
rtk docker exec harness-agent-sta2e-agent-workspace specify run speckit.matd.specify \
  --args "test feature"
```

If any step fails, halt and report the exact error output before continuing
to the next task.
