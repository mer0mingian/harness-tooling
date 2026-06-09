# Jira MCP — SDP Initiative Creation Feasibility

**Date:** 2026-06-08
**Scope:** READ-ONLY investigation. No Jira issue created.
**Question:** Can a Jira (Atlassian) MCP server create an SDP Initiative and transition it to "Idea Backlog", with auth handled at MCP/SDP level (not in our code)? Does our SDP field-set map cleanly to the MCP create tool?

> **Legend:** ✅ verified this session · ⚠️ inferred / strong indication · ❌ not available

---

## TL;DR

| Question | Answer |
|----------|--------|
| (a) MCP create + transition viable for SDP? | **NO** (for the official Atlassian Remote MCP) |
| (b) Create + transition tool names | `createJiraIssue` + `transitionJiraIssue` (+ `getTransitionsForJiraIssue`) — Cloud only |
| (c) Custom-field support verdict | **PARTIAL / unreliable** — custom fields "may not be recognized without explicit setup" |
| (d) Recommended approach | **REST with Bearer token** against `vulcan.stepstone.com` (current proven path) |

**Root blocker:** StepStone runs Jira **Data Center** (`vulcan.stepstone.com`, Bearer-token auth). The official Atlassian Remote MCP server is **Atlassian Cloud only**. It physically cannot reach our on-prem Jira. This is independent of whether the MCP's tooling is otherwise capable.

---

## 1. Are `mcp__atlassian__*` tools available in THIS environment right now?

**❌ No.** None are configured or exposed in this session.

Verified:
- `~/.claude.json` top-level `mcpServers` = `["bitbucket"]` only. The single project-scoped MCP server is `sequential-thinking` (in `stst-talent-mcp`). The only "atlassian" hit in `.claude.json` is a `skillUsage` counter, not a server. ✅
- No `.mcp.json` in the repo; no `atlassian` key in `.claude/settings.json` / `settings.local.json` / `~/.claude/settings.json`. ✅

**Historical note (important nuance):** Earlier sessions referenced `mcp__atlassian__jira_*` tools — `jira_create_issue`, `jira_update_issue`, `jira_transition_issue`, `jira_get_transitions`, `jira_create_issue_link`, `jira_link_to_epic`, `confluence_get_page`, etc. (snake_case). These names belong to the **self-hosted `mcp-atlassian` server (sooperset/Docker)** pointed at our Data Center — **not** the official Atlassian Cloud Remote MCP. That self-hosted server is also **not configured in this environment now**. The "earlier sessions found only REST worked" observation is consistent: even when that self-hosted MCP was around, sprint deletion / page restrictions / some field ops fell back to REST (see `learnings/session-history.md`).

So there are **two different "Jira MCP" products** in play, and the question conflates them:
1. **Official Atlassian Remote MCP** (`mcp.atlassian.com`, camelCase `createJiraIssue`) — Cloud only.
2. **Self-hosted `mcp-atlassian`** (sooperset, snake_case `jira_create_issue`) — can target Data Center, but not installed here.

---

## 2. Official Atlassian Remote MCP server (mcp.atlassian.com) — create/transition tools

**✅ Verified** from `support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/`.

The server (a.k.a. **Atlassian Rovo MCP Server**) DOES expose issue creation and transition. Tools are grouped by permission scope:

**`read_jira`**
- `getJiraIssue`
- `getJiraIssueTypeMetaWithFields`
- `getJiraProjectIssueTypesMetadata`
- `getTransitionsForJiraIssue`  ← lists valid transitions for an issue
- `getVisibleJiraProjects`
- `getJiraIssueRemoteIssueLinks`, `getIssueLinkTypes`, `lookupJiraAccountId`

**`write_jira`**
- `createJiraIssue`  ← create
- `editJiraIssue`  ← update fields on existing issue
- `transitionJiraIssue`  ← move through workflow
- `addCommentToJiraIssue`, `addWorklogToJiraIssue`

**`search_jira`**
- `searchJiraIssuesUsingJql`

So all four named in the brief exist with those **exact camelCase names**: `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `getTransitionsForJiraIssue`. ✅

### Platform & auth
- **❌ Cloud only.** Prereq stated verbatim: "An Atlassian Cloud site with Jira, Compass, and/or Confluence." No Data Center / Server support. ✅
- **Auth handled at MCP level:** **OAuth 2.1** (default), optionally API token if an admin enables it. All actions respect the user's existing Jira permissions. ✅ → For the part of the question "auth at MCP level, not in our code" — yes, the Cloud MCP does this. But it's moot because it can't reach our Jira.

### Input schemas
- **⚠️ Not published.** The official server is closed-source; the GitHub `atlassian/atlassian-mcp-server` repo is docs/README only and does **not** publish parameter schemas for `createJiraIssue` / `editJiraIssue`. The supported-tools page lists names + one-line descriptions, not field-level schemas. So the exact JSON payload shape (project / issueType / summary / description / fields object) is **not verifiable from public docs** — it is driven by natural-language + the server's internal field resolution.
- (The DeepWiki `mani0070/...` page with snake_case `jira_create_issue` is a **third-party fork**, not the official server — ignore for the official-MCP question.)

---

## 3. Does the create tool accept custom fields? (vs our SDP field set)

**⚠️ PARTIAL / unreliable — this is a soft blocker even on Cloud.**

Atlassian's own documentation carries the limitation (verified via search of support docs): **"Custom Jira fields may not be recognized or returned without explicit setup."** Where supported, you must reference by ID (`customfield_XXXXX`) when names collide. There is **no documented guarantee** that you can pass an arbitrary `fields: { customfield_XXXXX: ... }` block to `createJiraIssue` the way the Jira REST API allows.

Our SDP Initiative **requires** several custom fields (from `references/sdp-custom-fields.md` + `jira-teams-config.yaml`), most marked `required: true`:

| SDP field | Field ID | Type | Required | Shape (REST) |
|-----------|----------|------|----------|--------------|
| Stonehenge Domain | `customfield_11259` | select | ✅ | `{ "value": "Search & Match" }` |
| Initiative Goal | `customfield_11389` | select | ✅ | `{ "value": "Delivery" }` |
| Initiative Category | `customfield_11313` | select | ✅ | `{ "value": "Strategic Capability" }` |
| Team | `customfield_10001` | string (team UUID) | — | `"f46fee6d-...-1425"` (string, NOT dict) |
| Sprint | `customfield_10005` / `_10020` | sprint | — | integer sprint id (e.g. `26422`) |
| Story Points | `customfield_10091` | number | ✅ | `5.0` |
| Target start / end | `customfield_16713/16714` (or `_10022/_10023`) | date | — | `"YYYY-MM-DD"` |

> Note: the two reference files disagree on some IDs (e.g. Team `10001` vs Product Team `13301`; Sprint `10005` vs `10020`; Target dates `16713/16714` vs `10022/10023`). This ID ambiguity itself argues for the REST path with live `getFields` discovery, regardless of MCP.

**Verdict:** Even setting aside Data Center, the SDP create payload depends on several **required select-type custom fields** with specific value shapes. The official MCP gives **no contractual support** for passing these reliably — it's natural-language/field-resolution-driven and explicitly warns custom fields may not be recognized. Required custom fields that the MCP can't set would make `createJiraIssue` **fail validation** at the SDP screen. ❌ for clean mapping.

---

## 4. Create-default "To Do" (11092) → transition to "Idea Backlog" (11256, transition 101)

- **Two-call flow is the model the official MCP supports** ⚠️: `createJiraIssue` (lands in workflow's create-default status), then `getTransitionsForJiraIssue` → `transitionJiraIssue` with the transition id. This mirrors the REST pattern (`POST /issue` then `POST /issue/{key}/transitions {"transition":{"id":"101"}}`).
- **No documented atomic create-in-status** ❌. Neither the official MCP nor Jira's create API lets you choose a non-default initial workflow status in one call; you always create-then-transition. (This part is achievable in principle on either MCP or REST — it is NOT the blocker.)

---

## 5. Conclusion & recommended mapping

### Is MCP-driven SDP creation viable?
**NO for the official Atlassian Remote MCP** — two reasons, in priority order:
1. **Hard blocker:** Cloud-only; cannot reach Data Center `vulcan.stepstone.com`. ✅ verified
2. **Soft blocker:** No reliable custom-field support; SDP requires several required select custom fields. ⚠️ verified-as-documented-limitation

**Conditionally yes only via the self-hosted `mcp-atlassian` (sooperset) server** targeting our Data Center — but that is **not installed here**, and history shows it still falls back to REST for several ops. Auth there is our Bearer token configured into the MCP container (so "auth at MCP level" holds), but it's an extra moving part vs. a direct REST call.

### Recommended approach for the command: **REST with Bearer token** ✅
This is the proven path in this codebase:
- `JIRA_URL=https://vulcan.stepstone.com`, `JIRA_PERSONAL_TOKEN` (Bearer), per `references/rest-api-operations.md`.
- `POST /rest/api/2/issue` with full `fields` block (project, issuetype=Initiative, summary, description, + all required customfields in their exact shapes).
- `GET /rest/api/2/issue/{key}/transitions` to confirm, then `POST .../transitions` with `{"transition":{"id":"101"}}` to reach Idea Backlog (11256).
- Discover/confirm field IDs live with `GET /rest/api/2/field` (resolves the ID ambiguity in §3).

### `sdp-initiative-template.yml` → call mapping (REST path)
> No `sdp-initiative-template.yml` exists in the repo yet (searched). Proposed mapping:

```
template.project.key            -> fields.project.key            = "SDP"
template.issue_type             -> fields.issuetype.name         = "Initiative"
template.summary                -> fields.summary
template.description            -> fields.description
template.stonehenge_domain      -> fields.customfield_11259      = {"value": <domain>}
template.initiative_goal        -> fields.customfield_11389      = {"value": <goal>}
template.initiative_category    -> fields.customfield_11313      = {"value": <category>}
template.team                   -> fields.customfield_10001      = "<team-uuid>"   (string)
template.story_points           -> fields.customfield_10091      = <float>
template.sprint                 -> fields.customfield_10005       = <sprint-id int>
template.target_start / _end    -> fields.customfield_16713/16714 = "YYYY-MM-DD"
# then, post-create:
template.target_status="Idea Backlog" -> POST transitions {"transition":{"id":"101"}}  (To Do 11092 -> Idea Backlog 11256)
```
(Verify each customfield ID against live `GET /field` before relying on the table — the two skill references disagree on a few IDs.)

---

## Verified vs inferred

| Claim | Status |
|-------|--------|
| No atlassian MCP configured in this session | ✅ verified (`.claude.json`, settings files) |
| Official Rovo MCP tool names (create/edit/transition/getTransitions) | ✅ verified (support.atlassian.com supported-tools) |
| Official MCP is Cloud-only, OAuth 2.1 | ✅ verified (support + GitHub README) |
| Custom fields "may not be recognized without explicit setup" | ✅ verified (Atlassian support doc, via search) |
| Exact createJiraIssue JSON payload shape | ⚠️ not published / unverifiable (closed-source) |
| Two-call create-then-transition; no atomic create-in-status | ⚠️ inferred from Jira workflow model + MCP tool list |
| SDP custom field IDs / required flags | ✅ from repo skill references (note internal ID disagreements) |
| StepStone Jira = Data Center @ vulcan.stepstone.com, Bearer | ✅ from `references/rest-api-operations.md` |

---

## ⚠️ CORRECTION — verified update (2026-06-08, later same day)

The "MCP not viable" conclusion above referred to the **official Atlassian Cloud/Rovo MCP**. A
**different, write-enabled server — `ghcr.io/sooperset/mcp-atlassian` (`atlassian-write` in
`.mcp.json`) — was live-tested and IS viable:**

- Jira is **Atlassian Cloud `stepstone.atlassian.net`** (recent migration; the Data-Center/`vulcan`
  claim above is OUTDATED — disregard it).
- The server starts over stdio, authenticates with the existing env vars (`JIRA_URL`,
  `JIRA_USERNAME`, `JIRA_API_TOKEN`) + the Cloudflare cert bundle (`REQUESTS_CA_BUNDLE`), and a
  read call `jira_get_issue SDP-7768` returned a real **Initiative** in status **"To Do"**
  (`isError:false`).
- Relevant write tools confirmed present: `jira_create_issue`, `jira_transition_issue`,
  `jira_update_issue`, `jira_create_remote_issue_link`, `jira_search`; plus
  `confluence_create_page` / `confluence_update_page`.
- **Path for the command:** `jira_create_issue` (SDP / Initiative / `additional_fields` for required
  select custom fields) → `jira_transition_issue` (id 101 → Idea Backlog 11256) →
  `jira_create_remote_issue_link` (→ PRD on Stash). Auth at the MCP layer, not in code.
- Remaining caveat: reconcile required custom-field ids (Stonehenge Domain, Initiative Goal/Category,
  Story Points) against live `jira_search`/field metadata at build time.
