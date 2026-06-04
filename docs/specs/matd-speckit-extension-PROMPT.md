# Implementation Prompt: matd as Spec-Kit Extension

**Task Type:** Convert existing spec-kit scaffold into a v2.0.0 extension.
**Story Points:** 8 (across 6 subagent tasks; see plan §7).
**Branch (already checked out):** `feat/matd-as-speckit-extension`
**Working directory:** `/home/minged01/repositories/harness-workplace/harness-tooling/`

---

## Source of Truth

The authoritative implementation contract is
[`docs/specs/matd-speckit-extension-IMPLEMENTATION.md`](./matd-speckit-extension-IMPLEMENTATION.md).
Read it first, in full. Every YAML field, every command-body section,
every skill name, every script path is locked there. The spec at
[`docs/specs/matd-speckit-extension.md`](./matd-speckit-extension.md) and
the plan at
[`docs/plans/matd-speckit-extension.md`](../plans/matd-speckit-extension.md)
provide context; IMPLEMENTATION.md overrides if there is any conflict.

Background research:
- `/tmp/matd-speckit-research/extension-system.md` (schema, install
  mechanics, naming rules)
- `/tmp/matd-speckit-research/matd-inventory.md` (per-role skill lists,
  legacy file paths)

---

## Allowed Write Paths

You MAY create, edit, or delete files at these paths only:

- `harness-tooling/spec-kit-multi-agent-tdd/**` — full read/write/delete.
- `harness-tooling/.agents/agents/stdd-solution-design-subagent.md` —
  delete only.
- `harness-tooling/.agents/docs/stdd-workflow.md` — delete only.
- `harness-tooling/.agents/docs/research_stdd_workflows.md` — delete only.

## Forbidden Paths

You MUST NOT touch:

- `harness-tooling/.agents/plugins/matd/**` — the Claude Code plugin
  stays exactly as it is. It is the source of the skill copy; reading is
  fine, writing/moving/deleting is not.
- `harness-tooling/.agents/agents/matd-*.md` — agent files outside the
  plugin are read-only for this task.
- `harness-tooling/.agents/commands/matd-*.md` — same.
- `harness-tooling/.agents/skills/**` — same.
- `harness-tooling/.claude-plugin/**` — same.
- `harness-tooling/docs/**` (except the four spec/plan files this branch
  already created) — do not edit other docs.
- `harness-sandbox/**` — out of scope on this branch. Spec-kit CLI is
  already in the container.
- Any file outside `harness-tooling/`.

---

## Order of Operations

Strict sequence. Each step has a single point of failure; do not move on
until the previous step's evidence is captured.

1. **Rewrite `spec-kit-multi-agent-tdd/extension.yml`.** Copy the YAML
   verbatim from IMPLEMENTATION.md §2. Save. Run
   `python -c "import yaml; yaml.safe_load(open('spec-kit-multi-agent-tdd/extension.yml'))"`
   to confirm valid YAML.
2. **Rewrite the 8 command files under `commands/`.** One per IMPLEMENTATION.md
   §4–§11. Delete any of the old `commands/*.md` files that are not in
   the new set (test.md, implement.md, review.md, commit.md,
   update-docs.md, specify-product-brief.md, specify-adr.md,
   specify-solution-design.md). Preserve `commands/MIGRATION.md` and
   append a v2.0.0 note.
3. **Copy ~51 skills from the Claude Code plugin into the extension.**
   Run the `cp -r` block in IMPLEMENTATION.md §13 exactly. Then verify
   with `diff -r`.
4. **Rewrite `workflows/matd-tdd.yml`.** Copy the YAML verbatim from
   IMPLEMENTATION.md §15.
5. **Rewrite `hooks/install.sh`.** Implement the pseudocode in
   IMPLEMENTATION.md §14. While rewriting, research the OpenCode and
   Gemini skill-discovery paths and update IMPLEMENTATION.md §14 inline
   (replace each `TBC` with the verified path or, if no canonical path
   exists, document that and propose a path).
6. **Delete the 3 STDD files** listed in IMPLEMENTATION.md §17. Stage
   the deletions in git.
7. **Final validation pass.** Run the QA checklist in IMPLEMENTATION.md
   §18. Capture all evidence blocks.

---

## Verification Step (mandatory)

Inside the harness-sandbox container, run:

```bash
cd ~/repositories/sta2e-agent-workspace
~/repositories/harness-workplace/harness-sandbox/bin/harness up --profile cgc

rtk docker exec harness-agent-sta2e-agent-workspace specify extension add --dev \
  /workspace/../harness-tooling/spec-kit-multi-agent-tdd 2>&1 | tee /tmp/matd-install.log
```

If the install reports any schema errors, do NOT attempt to fix them
silently. Stop and report the exact error message in your final report,
along with which manifest field it points at. The user will decide whether
to amend IMPLEMENTATION.md or to deviate.

Follow up with:

```bash
rtk docker exec harness-agent-sta2e-agent-workspace specify extension list
rtk docker exec harness-agent-sta2e-agent-workspace specify extension info matd
rtk docker exec harness-agent-sta2e-agent-workspace specify workflow list
```

Each must show `matd@2.0.0` / `matd-tdd` respectively.

---

## Idempotency Check

Run `hooks/install.sh` twice in the sandbox. Capture `ls -laR
.specify/ .claude/commands/ .claude/skills/` before, between, and after.
Diff the second and third snapshots; they MUST be byte-equal.

---

## Output Format

When done (or blocked), report back with exactly:

1. **Files written.** A flat list of absolute paths.
2. **Files deleted.** A flat list.
3. **Verification evidence.** The captured output of each step in
   IMPLEMENTATION.md §18.
4. **TBC items resolved.** For each `TBC` in IMPLEMENTATION.md, the
   resolved value plus the citation (URL or doc path) that backs it.
5. **TBC items still open.** Any `TBC` that could not be resolved, with
   a one-paragraph note on why.
6. **Blockers.** Any failures during install, validation, or idempotency
   checks, with the exact error output.

Do NOT mark the task complete until all 10 checks in IMPLEMENTATION.md
§18 are green AND the verification step above returns exit 0.

---

## Constraints

- Use `rtk` for all read-only shell commands (per
  `/home/minged01/.claude/RTK.md`).
- Do not amend existing commits. If a commit is needed, ask the user.
- Do not skip git hooks. If a hook fails, stop and report.
- Do not invent skill names. If a skill referenced in IMPLEMENTATION.md
  §12 is not present in `.agents/plugins/matd/skills/`, stop and report.
- Do not invent manifest fields. Only fields in
  `/tmp/matd-speckit-research/extension-system.md` §D are permitted.
- Estimate task complexity in story points if you need to break a step
  further. Do not use hours.
