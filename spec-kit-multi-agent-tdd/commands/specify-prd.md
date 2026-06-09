---
description: "PM-facing PRD command: schema-driven interview → change-request PRD + SDP Initiative"
agent: matd-specifier
skills:
  - 'general-grill-me'
  - 'general-grill-with-docs'
  - 'stdd-product-spec-formats'
  - 'context-optimization'
tools:
  - 'filesystem/read'
  - 'filesystem/write'
  - 'filesystem/list'
templates:
  prd-schema: templates/prd-schema.yml
  sdp-initiative: templates/sdp-initiative-template.yml
  jira-config: .specify/jira-config.yml
exit_codes:
  0: "Success — PRD created, optionally SDP created and linked"
  1: "Validation failure — required inputs missing or CRITICAL content-test failures unacknowledged"
  2: "Script error — dependency script failed or workspace repo precondition not met"
---

# PRD Workflow (MATD — PM Change-Request Discovery)

This command runs a schema-driven grill interview to produce a **change-request PRD** and, optionally, a linked **SDP Initiative** in "Idea Backlog" status. It orchestrates a fixed 4-step linear flow: scripted scaffold → `matd-specifier` interview + authoring → `matd-critical-thinker` content tests → scripted SDP creation and commit. All mechanical plumbing is handled by scripts; LLM agents handle only authoring and review.

## Prerequisites

- `product/prd/` directory — created by this command if absent
- `product/context/` directory — created by this command if absent
- `product/prd/index.yml` — created by `allocate_prd_id.py` on first run if absent
- `atlassian-write` MCP installed and running (for SDP creation — env vars `JIRA_*` + cert bundle must be configured); if absent, the SDP step is skipped with guidance
- Workspace git repo exists (for the Stash commit — a Staff Engineer/EM provisions it for new systems); if absent, the commit step is skipped with guidance

## User Input

```
/speckit.matd.specify-prd [SLUG]
```

**Arguments:**
- `[SLUG]`: Optional URL-safe slug for the PRD (alphanumeric + hyphens, max 40 chars). If not provided, it is derived from the PRD title during the interview.

---

## Step 1: Scaffold

**Runner: command + scripts (no LLM)**

### 1.1 Load schema

- Check for workspace-local override at `<workspace>/.specify/prd-schema.yml`
- Fall back to shipped default at `<extension-root>/templates/prd-schema.yml`
- Load and parse the schema; surface the 13 section names for the interview

### 1.2 Allocate PRD ID

```bash
python3 <extension-root>/scripts/allocate_prd_id.py \
  --index <workspace>/product/prd/index.yml \
  --slug <slug>
```

Capture output as `PRD_ID` (e.g. `PRD-001`). If `index.yml` does not exist, the script creates it.

### 1.3 Create index entry

```bash
python3 <extension-root>/scripts/maintain_prd_index.py create \
  --index <workspace>/product/prd/index.yml \
  --id <PRD_ID> \
  --slug <slug>
```

### 1.4 Load context files (reference-only — do NOT regenerate)

- System constitution at `<workspace>/architecture/system-constitution.md` — load if present, note if absent (continue either way)
- Product brief at `<workspace>/product/brief.md` — load if present (informational context for the interview)

### 1.5 Create output directories if needed

```bash
mkdir -p <workspace>/product/prd
mkdir -p <workspace>/product/context
```

### Report to PM (step 1 summary)

```
✓ Schema loaded: <N> sections, <N> grill prompts
✓ Allocated: <PRD_ID>
✓ Index entry created
ℹ Constitution: <loaded | not found — continuing>
ℹ Product brief: <loaded | not found — continuing>
```

---

## Step 2: Interview + Author

**Runner: matd-specifier agent**

Use `general-grill-me` skill throughout. Use `general-grill-with-docs` to reference the constitution and brief when loaded. Use `context-optimization` to load only the current section's schema data (progressive disclosure — do not load future sections into context).

### 2.1 Interview (section-by-section)

- For each of the 13 schema sections, run the `grill_prompts` from the schema in order
- Present one section at a time — do not dump all questions at once
- For each section, allow the PM to defer items to Open Questions (`OQ-NNN`)
- Surface relevant constitution invariants (backend-cloud policies, tech-radar constraints) as they relate to the section in play (FR-011)

> **During all sections but especially `User Workflows & Outcomes`:** If the PM mentions specific service names, API endpoints, database tables, schemas, UI screens, or system components, gently redirect: "That's an implementation detail — let's describe it as a user outcome or workflow instead. How does the user experience change?" Record any mentioned service names in the context file for the downstream Solution Design but do NOT write them into the PRD body.

### 2.2 Author the PRD (`product/prd/<PRD_ID>-<slug>.md`)

After all sections are complete (or deferred), render the PRD markdown from collected answers. The PRD **must** follow this exact structure:

**YAML frontmatter:**
```yaml
---
change_id: <PRD_ID>
title: <title>
owner: <PM name + team>
status: draft
sdp_key: null
stash_url: null
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

**Body sections (exact headers):**
- `## TL;DR` — 3 sentences: problem → change → outcome
- `## Problem Framing` — `PF-NNN` items
- `## Goals & Non-Goals` — `G-NNN` goals and `NG-NNN` non-goals
- `## Hypothesis` — `HYP-NNN` items (each with baseline B, target T, timeframe W, and Because rationale)
- `## Success Metrics` — `SM-NNN` items (each with `measurement_method` + baseline value or TBC plan with owner/date)
- `## User Workflows & Outcomes` — `UW-NNN` items; **NO service names, schemas, or screen references**
- `## Scope` — `IN-NNN` scope-in items, `OUT-NNN` scope-out items (both required, at least one each)
- `## Outcome-Level Requirements` — OPTIONAL; `REQ-NNN` capability-level items if the PM provides them; omit the section entirely if not needed
- `## Risks & Assumptions` — `R-NNN` risks and `A-NNN` assumptions
- `## Dependencies` — `DEP-NNN` team-level dependencies
- `## Open Questions` — `OQ-NNN` deferred items
- `## Rollout & Kill Condition` — `RK-NNN` items

Write **`.md` file only** — no YAML, no JSON, no scripts.

### 2.3 Author the context file (`product/context/<PRD_ID>-<slug>.context.md`)

Capture all extended design context that arose during the interview but does not fit the PRD template slots: rationale, discarded options, domain detail, constraints. This file is for downstream Solution Design and spec authors — keep it useful and searchable.

**Structure:**
```yaml
---
prd_id: <PRD_ID>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```
```
# Context: <PRD_ID> — <PRD title>
```
One section per topic that arose. Write **`.md` file only**.

---

## Step 3: Content Tests

**Runner: matd-critical-thinker agent (read-only review)**

### 3.1 Run deterministic structural validator

```bash
python3 <extension-root>/scripts/validate_prd_content.py \
  --prd <workspace>/product/prd/<PRD_ID>-<slug>.md \
  --schema <schema-path> \
  --max-findings 20
```

Display the output to the PM. If any CRITICAL findings are present:
- Show findings clearly
- Ask: "The PRD has CRITICAL structural issues. Fix them before proceeding to SDP creation, or acknowledge to override (audit trail will be recorded)."
- If PM acknowledges override: record in the context file header — `"CRITICAL override acknowledged by PM on <date>"`
- If PM fixes: re-run validator

### 3.2 Run LLM eval rubric

Read `<extension-root>/prompts/prd-eval-rubric.md`. Evaluate the PRD against the rubric as matd-critical-thinker. Display HF results, scored criteria, and verdict to the PM.

- Verdict **REWORK**: recommend revision; PM decides whether to continue
- Verdict **REVISE** or **PASS**: proceed

### 3.3 Report to PM

```
Structural validator: <PASS | N CRITICAL, M WARNING>
LLM rubric: <score>/32, verdict: <EXEMPLARY | ACCEPTABLE | REVISE | REWORK>
```

---

## Step 4: SDP + Commit

**Runner: command + scripts**

#### 4.1 Offer SDP creation (do NOT auto-create)

```
The PRD is ready. Would you like to create an SDP Initiative in Jira now?
This requires the atlassian-write MCP to be running and jira-config.yml to be configured.
[Y/N]
```

---

#### 4.Y — SDP path: Assemble payload + create + transition + link + write-back + commit

_Follow this branch when PM answers Y._

**4.Y.1 Check jira-config**

Look for the workspace jira-config in order:
1. `<workspace>/.specify/jira-config.yml` (preferred)
2. `<workspace>/architecture/jira-config.yml`

If not found: prompt PM to copy from `<extension-root>/templates/jira-config-scaffold.yml` and fill in team-specific values. Do not proceed until the config file exists.

**4.Y.2 Assemble SDP payload**

```bash
python3 <extension-root>/scripts/sdp/create_sdp_initiative.py \
  --prd <workspace>/product/prd/<PRD_ID>-<slug>.md \
  --jira-config <jira-config-path> \
  --output-dir <temp-dir>
```

**4.Y.3 Create SDP Initiative (via atlassian-write MCP)**

Read `<temp-dir>/sdp-create-payload.json` and call `jira_create_issue` with those fields. Capture the returned SDP key (e.g. `SDP-1234`).

**4.Y.4 Transition to Idea Backlog (via atlassian-write MCP)**

- Call `jira_get_transitions(issue_key=<SDP_KEY>)` to resolve the transition id for "Idea Backlog" at runtime — **do not hard-code transition ids**
- Call `jira_transition_issue(issue_key=<SDP_KEY>, transition_id=<resolved_id>)`
- Confirm the status is now "Idea Backlog"
- If transition fails: display the created SDP key and manual instructions; continue to 4.Y.5

**4.Y.5 Link PRD to SDP and write-back**

```bash
python3 <extension-root>/scripts/sdp/link_prd_to_sdp.py \
  --prd <workspace>/product/prd/<PRD_ID>-<slug>.md \
  --prd-id <PRD_ID> \
  --sdp-key <SDP_KEY> \
  --stash-url <stash-url-from-jira-config> \
  --jira-config <jira-config-path> \
  --index <workspace>/product/prd/index.yml \
  --workspace-root <workspace-root> \
  --scripts-dir <extension-root>/scripts/ \
  --output-dir <temp-dir>
```

The script writes `<temp-dir>/sdp-remotelink-payload.json`. Then call `jira_create_remote_issue_link` with that payload to link the PRD Stash URL to the SDP initiative.

The script also:
- Writes `sdp_key` and `initiative_link` back into the PRD frontmatter (FR-052b)
- Calls `maintain_prd_index.py bind-sdp` to update `index.yml`
- Commits the PRD and context file locally via `commit_prd_to_stash.sh`

**4.Y.6 Final report (SDP path)**

```
✓ PRD created: product/prd/<PRD_ID>-<slug>.md
✓ Context file: product/context/<PRD_ID>-<slug>.context.md
✓ SDP Initiative: <SDP_KEY> — "Idea Backlog" status
✓ Remote link: PRD linked to <SDP_KEY>
✓ Locally committed — push when ready:
   git -C <workspace-root> push

Next step: /speckit.matd.specify-solution-design
Inputs: PRD (<PRD_ID>), Product Brief, System Constitution
```

---

#### 4.N — PRD-only path: Commit + final report

_Follow this branch when PM answers N._

**4.N.1 Commit PRD (no SDP)**

```bash
python3 <extension-root>/scripts/sdp/commit_prd_to_stash.sh \
  --workspace-root <workspace-root> \
  --prd-id <PRD_ID> \
  --slug <slug>
```

**4.N.2 Final report (PRD-only path)**

```
✓ PRD created: product/prd/<PRD_ID>-<slug>.md
✓ Context file: product/context/<PRD_ID>-<slug>.context.md
ℹ SDP Initiative: skipped (PM decision)
✓ Locally committed — push when ready:
   git -C <workspace-root> push

To create the SDP later: re-run /speckit.matd.specify-prd with PRD-NNN already existing, or create manually in Jira project SDP.
Next step: /speckit.matd.specify-solution-design
```

---

## Token Efficiency

Progressive disclosure (FR-061):
- Schema loaded one section at a time during the interview — only the current section's schema data is in context
- Validator output capped at `--max-findings 20` (advisory; do not surface more than 20 findings at once)
- Context file is written separately so the PRD stays concise; depth lives in `product/context/`
- LLM agents (matd-specifier, matd-critical-thinker) handle authoring and review only; all plumbing is scripts invoked by the command

---

## Exit Codes

- **0**: Success — PRD created, optionally SDP created and linked
- **1**: Validation failure — required inputs missing or CRITICAL findings unacknowledged
- **2**: Script error — dependency script failed or workspace repo precondition not met

---

## Related Commands

- `/speckit.matd.specify-product-brief` — product business invariants (persistent)
- `/speckit.matd.specify-constitution` — technical invariants (persistent)
- `/speckit.matd.specify-solution-design` — builds on PRD + brief + constitution
