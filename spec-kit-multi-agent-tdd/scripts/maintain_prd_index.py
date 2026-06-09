#!/usr/bin/env python3
"""Create and update PRD entries in product/prd/index.yml."""
import argparse
import fcntl
import os
import re
import sys
from datetime import date

import yaml

SLUG_RE = re.compile(r'^[a-z0-9]([a-z0-9\-]{0,38}[a-z0-9])?$')

VALID_STATUSES = {'draft', 'review', 'approved', 'done', 'archived'}
DEFAULT_INDEX = {'next_prd_seq': 1, 'prds': {}}


def _today() -> str:
    return date.today().isoformat()


def _load(fh) -> dict:
    data = yaml.safe_load(fh)
    return data if data else DEFAULT_INDEX.copy()


def _save(fh, data: dict) -> None:
    fh.seek(0)
    fh.truncate()
    fh.write('# product/prd/index.yml — traceability index, machine-maintained\n')
    yaml.dump(data, fh, default_flow_style=False, allow_unicode=True)


def _open_locked(index_path: str, must_exist: bool = True):
    if must_exist and not os.path.exists(index_path):
        print(f"Error: index file not found: {index_path}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(os.path.abspath(index_path)), exist_ok=True)
    fh = open(index_path, 'a+')
    fcntl.flock(fh, fcntl.LOCK_EX)
    fh.seek(0)
    return fh


def cmd_create(args) -> None:
    if not SLUG_RE.match(args.slug):
        print(f"Error: invalid slug '{args.slug}' — use lowercase alphanumeric and hyphens, max 40 chars", file=sys.stderr)
        sys.exit(1)
    fh = _open_locked(args.index, must_exist=False)
    data = yaml.safe_load(fh.read()) or DEFAULT_INDEX.copy()
    if data.get('prds') is None:
        data['prds'] = {}

    if args.id in data['prds']:
        print(f"Error: entry {args.id} already exists.", file=sys.stderr)
        fh.close()
        sys.exit(1)

    today = _today()
    base = f"{args.id}-{args.slug}"
    data['prds'][args.id] = {
        'slug': args.slug,
        'sdp_key': None,
        'status': 'draft',
        'path': f"product/prd/{base}.md",
        'context_path': f"product/context/{base}.context.md",
        'stash_url': None,
        'specs': [],
        'created': today,
        'updated': today,
    }
    _save(fh, data)
    fcntl.flock(fh, fcntl.LOCK_UN)
    fh.close()
    print(f"OK: create applied to {args.id}")


def cmd_bind_sdp(args) -> None:
    fh = _open_locked(args.index)
    fh.seek(0)
    data = yaml.safe_load(fh.read()) or DEFAULT_INDEX.copy()
    if data.get('prds') is None or args.id not in data['prds']:
        print(f"Error: ID {args.id} not found in index.", file=sys.stderr)
        fh.close(); sys.exit(1)
    entry = data['prds'][args.id]
    if entry.get('sdp_key') is not None:
        print(f"Error: sdp_key already set to '{entry['sdp_key']}' for {args.id}.", file=sys.stderr)
        fh.close(); sys.exit(1)
    entry['sdp_key'] = args.sdp_key
    entry['updated'] = _today()
    _save(fh, data)
    fcntl.flock(fh, fcntl.LOCK_UN)
    fh.close()
    print(f"OK: bind-sdp applied to {args.id}")


def cmd_set_stash(args) -> None:
    fh = _open_locked(args.index)
    fh.seek(0)
    data = yaml.safe_load(fh.read()) or DEFAULT_INDEX.copy()
    if data.get('prds') is None or args.id not in data['prds']:
        print(f"Error: ID {args.id} not found in index.", file=sys.stderr)
        fh.close(); sys.exit(1)
    data['prds'][args.id]['stash_url'] = args.url
    data['prds'][args.id]['updated'] = _today()
    _save(fh, data)
    fcntl.flock(fh, fcntl.LOCK_UN)
    fh.close()
    print(f"OK: set-stash applied to {args.id}")


def cmd_set_status(args) -> None:
    if args.status not in VALID_STATUSES:
        print(f"Error: invalid status '{args.status}'. Choose from: {', '.join(sorted(VALID_STATUSES))}", file=sys.stderr)
        sys.exit(1)
    fh = _open_locked(args.index)
    fh.seek(0)
    data = yaml.safe_load(fh.read()) or DEFAULT_INDEX.copy()
    if data.get('prds') is None or args.id not in data['prds']:
        print(f"Error: ID {args.id} not found in index.", file=sys.stderr)
        fh.close(); sys.exit(1)
    data['prds'][args.id]['status'] = args.status
    data['prds'][args.id]['updated'] = _today()
    _save(fh, data)
    fcntl.flock(fh, fcntl.LOCK_UN)
    fh.close()
    print(f"OK: set-status applied to {args.id}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Manage PRD entries in index.yml.')
    sub = parser.add_subparsers(dest='subcommand', required=True)

    p_create = sub.add_parser('create', help='Add a new PRD entry')
    p_create.add_argument('--index', required=True)
    p_create.add_argument('--id', required=True, help='PRD ID e.g. PRD-001')
    p_create.add_argument('--slug', required=True, help='URL-safe slug')

    p_sdp = sub.add_parser('bind-sdp', help='Set sdp_key for a PRD')
    p_sdp.add_argument('--index', required=True)
    p_sdp.add_argument('--id', required=True)
    p_sdp.add_argument('--sdp-key', required=True, dest='sdp_key')

    p_stash = sub.add_parser('set-stash', help='Set stash_url for a PRD')
    p_stash.add_argument('--index', required=True)
    p_stash.add_argument('--id', required=True)
    p_stash.add_argument('--url', required=True)

    p_status = sub.add_parser('set-status', help='Update PRD status')
    p_status.add_argument('--index', required=True)
    p_status.add_argument('--id', required=True)
    p_status.add_argument('--status', required=True, choices=sorted(VALID_STATUSES))

    args = parser.parse_args()
    {'create': cmd_create, 'bind-sdp': cmd_bind_sdp,
     'set-stash': cmd_set_stash, 'set-status': cmd_set_status}[args.subcommand](args)


if __name__ == '__main__':
    main()
