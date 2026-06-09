#!/usr/bin/env python3
"""
create_sdp_initiative.py
Assembles Jira payloads for SDP Initiative creation and transition.
Does NOT call the MCP — writes JSON files for the command (T011) to consume.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_prd(prd_path: Path) -> dict:
    text = prd_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        print("ERROR: PRD has no YAML frontmatter (--- ... ---)", file=sys.stderr)
        sys.exit(1)
    frontmatter = yaml.safe_load(fm_match.group(1)) or {}

    # Extract TL;DR paragraph
    tldr = ""
    tldr_match = re.search(r"^##\s+TL;DR\s*\n+(.*?)(?=\n#|\Z)", text, re.MULTILINE | re.DOTALL)
    if tldr_match:
        para = tldr_match.group(1).strip().split("\n\n")[0].strip()
        tldr = para[:500]

    return {"frontmatter": frontmatter, "tldr": tldr}


def load_jira_config(config_path: Path) -> dict:
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


def validate_inputs(fm: dict, cfg: dict) -> list[str]:
    errors = []
    if not fm.get("title") and not fm.get("change_id"):
        errors.append("PRD frontmatter missing both 'title' and 'change_id' (need at least one)")
    sdp = cfg.get("sdp") or {}
    domain_id = sdp.get("stonehenge_domain", {}).get("option_id", "")
    if not domain_id or "<" in str(domain_id):
        errors.append("jira-config missing or placeholder: sdp.stonehenge_domain.option_id")
    category_id = sdp.get("initiative_category", {}).get("option_id", "")
    if not category_id or "<" in str(category_id):
        errors.append("jira-config missing or placeholder: sdp.initiative_category.option_id")
    goal_id = sdp.get("initiative_goal", {}).get("option_id", "")
    if not goal_id or "<" in str(goal_id):
        errors.append("jira-config missing or placeholder: sdp.initiative_goal.option_id")
    return errors


def get_quarter() -> str:
    """Derive current quarter label from today's date."""
    d = date.today()
    q = (d.month - 1) // 3 + 1
    return f"Q{q} {d.year}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render SDP Initiative JSON payloads for MCP consumption."
    )
    parser.add_argument("--prd", required=True, help="Path to PRD markdown file")
    parser.add_argument("--jira-config", required=True, help="Path to workspace jira-config.yml")
    parser.add_argument("--output-dir", required=True, help="Directory to write JSON output files")
    args = parser.parse_args()

    prd_path = Path(args.prd)
    config_path = Path(args.jira_config)
    output_dir = Path(args.output_dir)

    if not prd_path.exists():
        print(f"ERROR: PRD file not found: {prd_path}", file=sys.stderr)
        sys.exit(1)
    if not config_path.exists():
        print(f"ERROR: jira-config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    prd = parse_prd(prd_path)
    fm = prd["frontmatter"]
    tldr = prd["tldr"]
    cfg = load_jira_config(config_path)

    errors = validate_inputs(fm, cfg)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    sdp = cfg.get("sdp") or {}
    title = fm.get("title") or fm.get("change_id", "Untitled")
    quarter = sdp.get("sdp_quarter") or get_quarter()
    summary = f"[{quarter}] {title}"

    stash_url = fm.get("stash_url") or "PENDING"
    description = f"{tldr}\n\nSource PRD: {stash_url}" if tldr else f"Source PRD: {stash_url}"

    domain_id = str(sdp.get("stonehenge_domain", {}).get("option_id", ""))
    category_id = str(sdp.get("initiative_category", {}).get("option_id", ""))
    goal_id = str(sdp.get("initiative_goal", {}).get("option_id", ""))
    team_uuid = sdp.get("team", {}).get("uuid", "")
    sprint_id = sdp.get("sprint", {}).get("sprint_id")

    if not team_uuid or "<" in str(team_uuid):
        print("WARNING: sdp.team.uuid missing or placeholder — customfield_10001 will be omitted", file=sys.stderr)
        team_uuid = None

    additional_fields: dict = {
        "customfield_11259": {"id": domain_id},
        "customfield_11313": {"id": category_id},
        "customfield_11389": {"id": goal_id},
    }
    if team_uuid:
        additional_fields["customfield_10001"] = team_uuid
    if sprint_id is not None:
        additional_fields["customfield_10020"] = sprint_id

    create_payload = {
        "project_key": "SDP",
        "issue_type": "Initiative",
        "summary": summary,
        "description": description,
        "additional_fields": additional_fields,
    }

    transition_params = {
        "note": "IMPORTANT: Do NOT use last_known_transition_id_reference_only directly. Always resolve the transition id at runtime by calling jira_get_transitions(issue_key) and finding the transition whose name matches target_status_name. The last_known value is for human reference only.",
        "target_status_name": "Idea Backlog",
        "target_status_id": "11256",
        "last_known_transition_id_reference_only": "101",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    create_file = output_dir / "sdp-create-payload.json"
    transition_file = output_dir / "sdp-transition-params.json"

    create_file.write_text(json.dumps(create_payload, indent=2), encoding="utf-8")
    transition_file.write_text(json.dumps(transition_params, indent=2), encoding="utf-8")

    print(f"CREATE_PAYLOAD: {create_file}")
    print(f"TRANSITION_PARAMS: {transition_file}")


if __name__ == "__main__":
    main()
