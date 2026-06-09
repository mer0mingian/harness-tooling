#!/usr/bin/env python3
# Link mechanism: Phase-A (remote/web link to PRD on Stash).
"""
link_prd_to_sdp.py — Write SDP key back into PRD and produce remote-link payload.

Called AFTER the command has received the SDP key from jira_create_issue.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Link PRD to SDP initiative: produce remote-link payload and write-back SDP key."
    )
    parser.add_argument("--prd", required=True, help="Path to PRD markdown file")
    parser.add_argument("--prd-id", required=True, help="PRD identifier, e.g. PRD-001")
    parser.add_argument("--sdp-key", required=True, help="SDP initiative key, e.g. SDP-1234")
    parser.add_argument("--stash-url", required=True, help="Stash URL of the PRD file")
    parser.add_argument("--jira-config", required=True, help="Path to jira-config.yml")
    parser.add_argument("--index", required=True, help="Path to product/prd/index.yml")
    parser.add_argument("--workspace-root", required=True, help="Path to agent workspace root")
    parser.add_argument("--scripts-dir", required=True, help="Path to spec-kit-multi-agent-tdd/scripts/")
    parser.add_argument("--output-dir", required=True, help="Directory for JSON output files")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Step 1: Produce remote-link payload JSON
# ---------------------------------------------------------------------------

def produce_remotelink_payload(output_dir: str, sdp_key: str, stash_url: str, prd_id: str) -> str:
    # Phase-A: remote/web link to PRD on Stash.
    # Future Phase-B: swap to a dedicated custom Jira field when provisioned by the Atlassian team.
    # Keep this step abstracted — the payload JSON shape is the only thing that changes on Phase-B.
    os.makedirs(output_dir, exist_ok=True)
    payload = {
        "issue_key": sdp_key,
        "url": stash_url,
        "title": f"Source PRD — {prd_id}",
        "summary": "Source PRD for this SDP initiative",
        "relationship": "source PRD",
    }
    output_path = os.path.join(output_dir, "sdp-remotelink-payload.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"REMOTELINK_PAYLOAD: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Step 2 & 3: Write SDP key into PRD frontmatter and Header section
# ---------------------------------------------------------------------------

def _upsert_frontmatter_key(text: str, key: str, value: str, after_key: str = "status") -> str:
    """Add or update a key: value line in YAML frontmatter block."""
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"{key}: {value}", text)
    # Insert after the after_key line
    anchor = re.compile(rf"^({re.escape(after_key)}:.*)$", re.MULTILINE)
    match = anchor.search(text)
    if match:
        return text[: match.end()] + f"\n{key}: {value}" + text[match.end():]
    # Fallback: insert before closing ---
    closing = text.rfind("\n---")
    if closing != -1:
        return text[:closing] + f"\n{key}: {value}" + text[closing:]
    return text


def update_prd_frontmatter(prd_path: str, sdp_key: str, stash_url: str) -> None:
    with open(prd_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = _upsert_frontmatter_key(text, "sdp_key", sdp_key, after_key="status")
    text = _upsert_frontmatter_key(text, "stash_url", stash_url, after_key="sdp_key")

    with open(prd_path, "w", encoding="utf-8") as f:
        f.write(text)


def update_prd_header_section(prd_path: str, sdp_key: str) -> None:
    with open(prd_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Locate ## Header or # Header section (case-insensitive)
    header_match = re.search(r"^#{1,2}\s+Header\s*$", text, re.MULTILINE | re.IGNORECASE)
    if not header_match:
        # Nothing to do
        return

    section_start = header_match.end()

    # Find next section start (another heading) to limit scope
    next_section = re.search(r"^#{1,2}\s+", text[section_start:], re.MULTILINE)
    section_end = section_start + next_section.start() if next_section else len(text)
    section_body = text[section_start:section_end]

    # Try key-based replacement (YAML block style)
    kv_pattern = re.compile(r"^(initiative_link\s*:.*)$", re.MULTILINE)
    if kv_pattern.search(section_body):
        new_section_body = kv_pattern.sub(f"initiative_link: {sdp_key}", section_body)
    else:
        # Check if it looks like a YAML block (has key: value lines)
        yaml_like = re.search(r"^\w[\w_]+\s*:.*$", section_body, re.MULTILINE)
        if yaml_like:
            # Append as YAML key before next section
            new_section_body = section_body.rstrip() + f"\ninitiative_link: {sdp_key}\n"
        else:
            # Freeform markdown — append bold line
            new_section_body = section_body.rstrip() + f"\n**Initiative Link:** {sdp_key}\n"

    text = text[:section_start] + new_section_body + text[section_end:]
    with open(prd_path, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# Step 4: Update index.yml
# ---------------------------------------------------------------------------

def update_index(scripts_dir: str, index_path: str, prd_id: str, sdp_key: str, stash_url: str) -> None:
    maintain = os.path.join(scripts_dir, "maintain_prd_index.py")
    if not os.path.exists(maintain):
        print(f"Error: maintain_prd_index.py not found at {maintain}", file=sys.stderr)
        sys.exit(1)
    subprocess.run(
        ["python3", maintain, "bind-sdp", "--index", index_path, "--id", prd_id, "--sdp-key", sdp_key],
        check=True,
    )
    subprocess.run(
        ["python3", maintain, "set-stash", "--index", index_path, "--id", prd_id, "--url", stash_url],
        check=True,
    )


# ---------------------------------------------------------------------------
# Step 5: Re-commit the updated PRD
# ---------------------------------------------------------------------------

def _extract_slug(prd_path: str, prd_id: str) -> str:
    """Extract slug from filename: PRD-NNN-<slug>.md → <slug>."""
    filename = Path(prd_path).stem  # strip .md
    prefix = f"{prd_id.upper()}-"
    filename_upper = filename.upper()
    if filename_upper.startswith(prefix.upper()):
        slug = filename[len(prefix):]
        return slug.rstrip('.md').rstrip('.MD')
    # Fallback: try matching PRD-\d+-<slug>
    m = re.match(r"PRD-\d+-(.+)", filename, re.IGNORECASE)
    if m:
        return m.group(1)
    return filename


def recommit_prd(scripts_dir: str, workspace_root: str, prd_id: str, slug: str) -> None:
    commit_script = os.path.join(scripts_dir, "sdp", "commit_prd_to_stash.sh")
    if not os.path.exists(commit_script):
        print(f"Error: commit_prd_to_stash.sh not found at {commit_script}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        ["bash", commit_script, "--workspace-root", workspace_root, "--prd-id", prd_id, "--slug", slug],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"Error: commit_prd_to_stash.sh failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    if "Nothing to commit" in result.stdout:
        print("⚠ PRD re-commit: nothing to commit (SDP key may already be present)")
    else:
        print("✓ PRD re-committed with SDP key write-back")
    print(result.stdout, end="")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    # Fix 1: validate all required path inputs before any file operations
    prd_path = args.prd
    index_path = args.index
    workspace_root = args.workspace_root
    scripts_dir = args.scripts_dir

    required_paths = {
        '--prd': prd_path,
        '--index': index_path,
        '--workspace-root': workspace_root,
        '--scripts-dir': scripts_dir,
    }
    errors = []
    for arg, path in required_paths.items():
        if not os.path.exists(path):
            errors.append(f"{arg}: path does not exist: {path}")
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Fix 2: validate --stash-url before writing to PRD
    if not args.stash_url or not args.stash_url.startswith('http'):
        print(f"Error: --stash-url must be a non-empty URL starting with 'http', got: {args.stash_url!r}", file=sys.stderr)
        sys.exit(1)

    # Step 1
    payload_path = produce_remotelink_payload(args.output_dir, args.sdp_key, args.stash_url, args.prd_id)

    # Steps 2 & 3
    update_prd_frontmatter(prd_path, args.sdp_key, args.stash_url)
    update_prd_header_section(prd_path, args.sdp_key)

    # Step 4
    update_index(scripts_dir, index_path, args.prd_id, args.sdp_key, args.stash_url)

    # Step 5
    slug = _extract_slug(prd_path, args.prd_id)
    recommit_prd(scripts_dir, workspace_root, args.prd_id, slug)

    # Step 6 summary
    print(f"✓ Remote-link payload: {payload_path}")
    print(f"✓ PRD frontmatter updated: sdp_key={args.sdp_key}, stash_url={args.stash_url}")
    print(f"✓ PRD Header section updated: initiative_link={args.sdp_key}")
    print("✓ index.yml: sdp_key bound, stash_url set")


if __name__ == "__main__":
    main()
