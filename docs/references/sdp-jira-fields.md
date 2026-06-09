# SDP Initiative — Jira Cloud field reference (authoritative)

- **Source:** live Jira Cloud createmeta — `GET /rest/api/3/issue/createmeta/SDP/issuetypes/11110`
- **Instance:** `stepstone.atlassian.net` (Atlassian Cloud, post-migration)
- **Issue type:** `Initiative` = id **11110** · Project **SDP**
- **Captured:** 2026-06-08 (read-only)

## Required fields to create an SDP Initiative
| Field | id | Type | Notes |
|---|---|---|---|
| Summary | `summary` | string | e.g. `[Q3 2026] <change title>` |
| Project | `project` | project | `{"key":"SDP"}` |
| Issue Type | `issuetype` | issuetype | `{"id":"11110"}` (Initiative) |
| **Stonehenge Domain** | `customfield_11259` | option (28) | **REQUIRED** select — see values below |
| **Initiative Category** | `customfield_11313` | option (3) | **REQUIRED** select |
| **Initiative Goal** | `customfield_11389` | option (3) | **REQUIRED** select |

### Stonehenge Domain (`customfield_11259`) — allowed values (id)
AI Internal Tools (12543) · Commercial and Marketplace Analytics Domain (12584) · Marketing Capital Allocation Domain (12585) · Marketing Channel Insights Domain (12586) · Marketing Data Engineering Domain (12587) · Marketplace Tech Domain (12588) · Marketing Data Science Domain (12589) · Apply (12546) · Business Model Transformation (BMT) / Commercial Products (12547) · Business Model Transformation / Customer Products (12548) · Commercial Data Solutions (12549) · Connect Apply & Quality (12551) · Connect Feeds (12552) · Customer Migrations (12556) · Data & AI Platform (12558) · Data Products (12561) · Data Science & Analytics Domain (12562) · Design & Platform Performance (12564) · Developer Platform (12565) · Job Discovery (12568) · Labor Markets (12570) · Markets Rollout (12572) · Native Apps (12573) · Offer Extension & Differentiation (12574) · Recruiter Platform (12576) · **Search & Match (12579)** · Talent Onboarding (12581) · User Dialogue (12583)

### Initiative Category (`customfield_11313`)
Strategic Capability (17550) · KTLO (17551) · Paying Down Debt (17552)

### Initiative Goal (`customfield_11389`)
Delivery (17653) · Enablement (17654) · Research (17655)

> Suggested defaults (PM confirms per change): Domain = team's domain (e.g. Search & Match 12579),
> Category = Strategic Capability (17550), Goal = Delivery (17653).

## Useful optional fields (live ids)
| Field | id | Type | Notes |
|---|---|---|---|
| Description | `description` | string | ADF on v3; put TL;DR + PRD link |
| Target start | `customfield_10022` | date | YYYY-MM-DD |
| Target end | `customfield_10023` | date | YYYY-MM-DD |
| Sprint | `customfield_10020` | array | SDP quarterly sprint id |
| Story Points | `customfield_10091` | number | |
| Priority | `priority` | priority (6) | P0–P5 mapping |
| Parent Link | `customfield_10018` | any | portfolio hierarchy |
| Epic Link | `customfield_10014` | any | |
| L0 Theme | `customfield_11223` | option (9) | annual OKR theme |
| Country | `customfield_11191` | array (13) | |
| Product area | `customfield_11233` | array (35) | |
| **Team** | `customfield_10001` | team (UUID) | Settable though **not on the createmeta create screen**; value is the team **UUID**. Verified on SDP-6701 = `{"id":"f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425","name":"Mamba"}`. Mamba UUID = `f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425`. Write format: try the UUID (string) or `{"id":"<uuid>"}` — verify at build. |
| Components | `components` | array (94) | |
| Fix versions | `fixVersions` | array (160) | L1 strategic initiatives |
| Labels | `labels` | array | |

## ⚠️ Corrections to outdated skill docs (post-Cloud-migration)
The local `stepstone-atlassian-skills/references/sdp-custom-fields.md` predates the Cloud migration
and is **wrong** on several ids. Live createmeta is authoritative:
- **Target start/end:** live `customfield_10022` / `customfield_10023` — NOT `16713`/`16714`.
- **Sprint:** live `customfield_10020` — NOT `10005`.
- **Story Points:** live `customfield_10091` (matches `jira-teams-config.yaml`).
- **Team:** **`customfield_10001`** (value = team **UUID**, e.g. Mamba `f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425`). It does **not** appear on the createmeta create screen but IS set on Initiatives (verified on SDP-6701) — set it during create or via a follow-up update. The old `customfield_13301`/numeric-id (`579`) is DC-era and deprecated.
- `jira-teams-config.yaml` is mostly correct (10022/10023, 10091); `sdp-custom-fields.md` needs the above fixes.

## Ready-to-use `jira_create_issue` (atlassian-write MCP) call
```jsonc
// tool: jira_create_issue
{
  "project_key": "SDP",
  "issue_type": "Initiative",
  "summary": "[Q3 2026] <change title>",
  "description": "<TL;DR>\n\nSource PRD: <stash-url>",
  "additional_fields": {
    "customfield_11259": {"id": "12579"},   // Stonehenge Domain (e.g. Search & Match)
    "customfield_11313": {"id": "17550"},   // Initiative Category = Strategic Capability
    "customfield_11389": {"id": "17653"},   // Initiative Goal = Delivery
    "customfield_10001": "f46fee6d-7a22-4189-9d0d-6767aec4ebb8-1425", // Team (UUID, e.g. Mamba) — verify write format
    "customfield_10022": "2026-07-01",       // Target start (optional)
    "customfield_10023": "2026-09-30",       // Target end (optional)
    "customfield_10020": <sprint_id>          // SDP quarterly sprint (optional)
  }
}
```
Then `jira_transition_issue` (id **101** → Idea Backlog **11256**), then `jira_create_remote_issue_link` → PRD on Stash.

**Build-time check:** re-run createmeta before shipping the SDP script — option ids and the
required-field set can change; resolve the team's Stonehenge Domain from the workspace jira-config (FR-055).
