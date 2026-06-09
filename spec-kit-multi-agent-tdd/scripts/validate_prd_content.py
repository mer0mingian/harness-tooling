"""
validate_prd_content.py — PRD content validator (V-model right-side check).
Validates a PRD markdown file against prd-schema.yml rules.
Exit 0: all CRITICAL rules pass (warnings may exist)
Exit 1: one or more CRITICAL rules failed
"""
# NOTE: validation rules are implemented inline in each pass function.
# The prd-schema.yml validation_rules field documents the rules for human readers
# but is not read by this script. A mismatch between schema and script is a
# maintenance risk — treat schema validation_rules as the source of truth.
import re
import sys
import json
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

Finding = dict  # {rule_id, severity, section, message, line}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_without_frontmatter). Empty dict if none."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


def parse_sections(body: str) -> dict[str, tuple[str, int]]:
    """Return {section_heading_lower: (content, start_line_number)}."""
    sections: dict[str, tuple[str, int]] = {}
    current_heading = None
    current_lines: list[str] = []
    current_start = 0
    body_lines = body.split("\n")
    for i, line in enumerate(body_lines):
        m = re.match(r"^(#{2,3})\s+(.+)", line)
        if m:
            if current_heading is not None:
                sections[current_heading] = ("\n".join(current_lines), current_start)
            current_heading = m.group(2).strip().lower()
            current_lines = []
            current_start = i + 1
        else:
            if current_heading is not None:
                current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = ("\n".join(current_lines), current_start)
    return sections


def section_key(name: str) -> str:
    """Normalise section name for lookup: lower, underscores→spaces, strip."""
    return name.lower().replace("_", " ").strip()


def find_section(sections: dict, schema_name: str) -> tuple[str, int] | None:
    key = section_key(schema_name)
    if key in sections:
        return sections[key]
    # fuzzy: check if key is substring
    for k, v in sections.items():
        if key in k or k in key:
            return v
    return None


def lines_after(text: str, marker_pos: int, n: int = 3) -> str:
    """Return the line containing marker_pos plus n following lines."""
    lines = text.split("\n")
    char_count = 0
    start_line = 0
    for i, ln in enumerate(lines):
        if char_count + len(ln) >= marker_pos:
            start_line = i
            break
        char_count += len(ln) + 1
    return "\n".join(lines[start_line: start_line + n + 1])


# ── Pass 1: Frontmatter ──────────────────────────────────────────────────────

REQUIRED_FM_FIELDS = ["change_id", "title", "owner", "status", "created"]


def pass1_frontmatter(fm: dict, has_fm: bool) -> list[Finding]:
    findings = []
    if not has_fm:
        findings.append({"rule_id": "HDR-V000", "severity": "CRITICAL",
                         "section": "header",
                         "message": "PRD must start with YAML frontmatter (--- ... ---)"})
        return findings
    for field in REQUIRED_FM_FIELDS:
        if not fm.get(field):
            findings.append({"rule_id": f"HDR-V001-{field}", "severity": "CRITICAL",
                             "section": "header",
                             "message": f"frontmatter missing required field: {field}"})
    return findings


# ── Pass 2: Required sections ────────────────────────────────────────────────

def pass2_required_sections(sections: dict, schema_sections: list) -> list[Finding]:
    findings = []
    for sec in schema_sections:
        if not sec.get("required"):
            continue
        # 'header' section is represented by YAML frontmatter, validated in Pass 1
        if sec["id"] == "header":
            continue
        result = find_section(sections, sec["name"])
        if result is None or not result[0].strip():
            findings.append({"rule_id": f"{sec['id'].upper()}-V001", "severity": "CRITICAL",
                             "section": sec["id"],
                             "message": f"required section '## {sec['name']}' is missing or empty"})
    return findings


# ── Pass 3: Placeholder residue ──────────────────────────────────────────────

PLACEHOLDER_RE = re.compile(r'\[PLACEHOLDER\]|\[TBD\]|TODO|<!--.*?-->', re.DOTALL)
OPEN_Q_KEYS = {"open questions", "open_questions"}


def pass3_placeholders(sections: dict, schema_sections: list) -> list[Finding]:
    findings = []
    required_ids = {s["id"] for s in schema_sections if s.get("required")}
    for sec_name, (content, start_line) in sections.items():
        if sec_name in OPEN_Q_KEYS:
            continue
        # find matching schema section
        schema_sec = next((s for s in schema_sections
                           if section_key(s["name"]) == sec_name), None)
        if schema_sec is None or schema_sec["id"] not in required_ids:
            continue
        for m in PLACEHOLDER_RE.finditer(content):
            line_no = start_line + content[:m.start()].count("\n") + 1
            findings.append({"rule_id": f"{schema_sec['id'].upper()}-V002", "severity": "CRITICAL",
                             "section": schema_sec["id"],
                             "message": f"placeholder residue '{m.group()[:40]}' at line {line_no}"})
    return findings


# ── Pass 4: Hypothesis structure ─────────────────────────────────────────────

HYP_RE = re.compile(r'HYP-\d+')
NUM_RE = re.compile(r'\d+(?:\.\d+)?(?:\s*%|\s*\w+)?')
BASELINE_RE = re.compile(r'\bbaseline\b|\bcurrent\b|\bB\s*:', re.IGNORECASE)
TARGET_RE = re.compile(r'\btarget\b|\bT\s*:', re.IGNORECASE)
TIMEFRAME_RE = re.compile(r'\d+\s+(?:week|month|quarter|day)s?|Q[1-4]\b|W\d+\b', re.IGNORECASE)


def pass4_hypothesis(sections: dict) -> list[Finding]:
    findings = []
    hyp = find_section(sections, "hypothesis")
    if not hyp:
        return findings
    content, start_line = hyp
    for m in HYP_RE.finditer(content):
        ctx = lines_after(content, m.start(), 3)
        item = m.group()
        if not (NUM_RE.search(ctx) and BASELINE_RE.search(ctx)):
            findings.append({"rule_id": "HYP-V003", "severity": "CRITICAL",
                             "section": "hypothesis",
                             "message": f"{item} — missing measurable baseline B"})
        if not (NUM_RE.search(ctx) and TARGET_RE.search(ctx)):
            findings.append({"rule_id": "HYP-V004", "severity": "CRITICAL",
                             "section": "hypothesis",
                             "message": f"{item} — missing measurable target T"})
        if not TIMEFRAME_RE.search(ctx):
            findings.append({"rule_id": "HYP-V005", "severity": "CRITICAL",
                             "section": "hypothesis",
                             "message": f"{item} — missing timeframe W"})
    return findings


# ── Pass 5: Success metrics structure ────────────────────────────────────────

SM_RE = re.compile(r'SM-\d+')
MEASURE_RE = re.compile(
    r'\bmethod\b|\bmeasurement\b|\bmeasure\b|\bmeasured\b|\btool\b|\bdashboard\b'
    r'|\bquery\b|\bplatform\b|\banalytics\b|\btracking\b', re.IGNORECASE)
BASELINE_SM_RE = re.compile(
    r'\bbaseline\b|\bcurrent rate\b|\bcurrent value\b|\bcurrent %\b|\bas of\b'
    r'|\bTBC\b|\bTBD\b|\bto be confirmed\b|\bto be determined\b|\bto be measured\b',
    re.IGNORECASE)


def pass5_success_metrics(sections: dict) -> list[Finding]:
    findings = []
    sm = find_section(sections, "success metrics")
    if not sm:
        sm = find_section(sections, "success_metrics")
    if not sm:
        return findings
    content, start_line = sm
    for m in SM_RE.finditer(content):
        ctx = lines_after(content, m.start(), 3)
        item = m.group()
        if not MEASURE_RE.search(ctx):
            findings.append({"rule_id": "SM-V003", "severity": "CRITICAL",
                             "section": "success_metrics",
                             "message": f"{item} — missing measurement method"})
        if not BASELINE_SM_RE.search(ctx):
            findings.append({"rule_id": "SM-V004", "severity": "CRITICAL",
                             "section": "success_metrics",
                             "message": f"{item} — missing baseline value or TBC plan"})
    return findings


# ── Pass 6: Scope section ────────────────────────────────────────────────────

def pass6_scope(sections: dict) -> list[Finding]:
    findings = []
    scope = find_section(sections, "scope")
    if not scope:
        return findings
    content, _ = scope
    if not re.search(r'\bIN-\d+', content):
        findings.append({"rule_id": "SCOPE-V003", "severity": "WARNING",
                         "section": "scope",
                         "message": "scope section has no IN-NNN scope-in items"})
    if not re.search(r'\bOUT-\d+', content):
        findings.append({"rule_id": "SCOPE-V004", "severity": "WARNING",
                         "section": "scope",
                         "message": "scope section has no OUT-NNN scope-out items"})
    return findings


# ── Pass 7: User workflows leakage ───────────────────────────────────────────

IMPL_TERMS = [
    (r'\bAPI\b', 'API'), (r'\bendpoint\b', 'endpoint'), (r'\bdatabase\b', 'database'),
    (r'\bschema\b', 'schema'), (r'\bmicroservice\b', 'microservice'), (r'\bREST\b', 'REST'),
    (r'\bGraphQL\b', 'GraphQL'), (r'\bSQL\b', 'SQL'), (r'\btable name\b', 'table name'),
    (r'\bDynamoDB\b', 'DynamoDB'), (r'\bS3\b', 'S3'),
]


def pass7_uw_leakage(sections: dict) -> list[Finding]:
    findings = []
    uw_key = "user workflows and outcomes"
    uw = find_section(sections, uw_key)
    if not uw:
        uw = find_section(sections, "user_workflows_and_outcomes")
    if not uw:
        return findings
    content, start_line = uw
    for pattern, term in IMPL_TERMS:
        flags = 0 if term in ('API', 'REST', 'GraphQL', 'SQL', 'DynamoDB', 'S3') else re.IGNORECASE
        for m in re.finditer(pattern, content, flags):
            line_no = start_line + content[:m.start()].count("\n") + 1
            findings.append({"rule_id": "UW-V003", "severity": "WARNING",
                             "section": "user_workflows_and_outcomes",
                             "message": f"implementation term found: '{term}' at line {line_no}"})
    return findings


# ── Pass 8: REQ-NNN format ───────────────────────────────────────────────────

REQ_ID_RE = re.compile(r'\bREQ-\d{3}\b')
ANY_REQ_RE = re.compile(r'\bREQ-\S+')


def pass8_req_format(sections: dict) -> list[Finding]:
    findings = []
    req = find_section(sections, "outcome-level requirements")
    if not req:
        req = find_section(sections, "outcome_level_requirements")
    if not req or not req[0].strip():
        return findings
    content, start_line = req
    for m in ANY_REQ_RE.finditer(content):
        token = m.group()
        if not REQ_ID_RE.match(token):
            line_no = start_line + content[:m.start()].count("\n") + 1
            findings.append({"rule_id": "REQ-V001", "severity": "WARNING",
                             "section": "outcome_level_requirements",
                             "message": f"requirement ID '{token}' does not match REQ-NNN format at line {line_no}"})
    return findings


# ── Main ──────────────────────────────────────────────────────────────────────

def run(prd_path: str, schema_path: str, output_fmt: str, max_findings: int) -> int:
    prd_text = Path(prd_path).read_text(encoding="utf-8")
    schema = yaml.safe_load(Path(schema_path).read_text(encoding="utf-8"))
    schema_sections = schema.get("sections", [])

    fm, body = parse_frontmatter(prd_text)
    has_fm = prd_text.startswith("---")
    sections = parse_sections(body)

    findings: list[Finding] = []
    findings += pass1_frontmatter(fm, has_fm)
    findings += pass2_required_sections(sections, schema_sections)
    findings += pass3_placeholders(sections, schema_sections)
    findings += pass4_hypothesis(sections)
    findings += pass5_success_metrics(sections)
    findings += pass6_scope(sections)
    findings += pass7_uw_leakage(sections)
    findings += pass8_req_format(sections)

    # Compute full lists before any truncation — exit-code uses these
    criticals = [f for f in findings if f["severity"] == "CRITICAL"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]
    total_count = len(findings)

    # Truncate ONLY for display
    display_findings = findings[:max_findings] if max_findings > 0 else []
    display_criticals = [f for f in display_findings if f["severity"] == "CRITICAL"]
    display_warnings = [f for f in display_findings if f["severity"] == "WARNING"]
    truncated = total_count > len(display_findings)
    hidden_count = total_count - len(display_findings)

    if output_fmt == "json":
        result_dict: dict = {
            "file": prd_path,
            "schema": schema_path,
            "findings": display_findings,
            "summary": {
                "critical": len(criticals),
                "warning": len(warnings),
                "displayed": len(display_findings),
                "total": total_count,
                "result": "FAIL" if criticals else "PASS",
            },
        }
        if truncated:
            result_dict["truncation_note"] = (
                f"{hidden_count} more finding(s) not shown — increase --max-findings"
            )
        print(json.dumps(result_dict, indent=2))
    else:
        print("=== PRD Content Validator ===")
        print(f"File:   {prd_path}")
        print(f"Schema: {schema_path}")
        print()
        if display_criticals:
            print(f"CRITICAL ({len(criticals)} finding{'s' if len(criticals) != 1 else ''}"
                  f"{', ' + str(len(display_criticals)) + ' shown' if truncated else ''}):")
            for f in display_criticals:
                print(f"  [{f['rule_id']}] {f['section']}: {f['message']}")
        if display_warnings:
            print(f"\nWARNING ({len(warnings)} finding{'s' if len(warnings) != 1 else ''}"
                  f"{', ' + str(len(display_warnings)) + ' shown' if truncated else ''}):")
            for f in display_warnings:
                print(f"  [{f['rule_id']}] {f['section']}: {f['message']}")
        if not display_findings:
            if criticals or warnings:
                print(f"(all {total_count} finding(s) hidden — increase --max-findings to see them)")
            else:
                print("No findings.")
        if truncated:
            print(f"\n({hidden_count} more finding(s) not shown — increase --max-findings)")
        result = "FAIL" if criticals else "PASS"
        suffix = f" ({len(criticals)} CRITICAL finding{'s' if len(criticals) != 1 else ''})" if criticals else ""
        print(f"\nResult: {result}{suffix}")

    # Exit code uses full (untruncated) lists
    return 1 if criticals else 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a PRD markdown file against prd-schema.yml rules.")
    parser.add_argument("--prd", required=True, help="Path to PRD markdown file")
    parser.add_argument("--schema", required=True, help="Path to prd-schema.yml")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--max-findings", type=int, default=50,
                        help="Maximum number of findings to report (default: 50)")
    args = parser.parse_args()
    sys.exit(run(args.prd, args.schema, args.output, args.max_findings))


if __name__ == "__main__":
    main()
