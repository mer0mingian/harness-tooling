#!/usr/bin/env python3
"""Atomically allocate the next PRD ID from product/prd/index.yml."""
import argparse
import fcntl
import os
import re
import sys
from datetime import date

import yaml


SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9\-]{0,38}[a-z0-9]$|^[a-z0-9]$')
DEFAULT_INDEX = {
    'next_prd_seq': 1,
    'prds': {},
}


def _load(fh) -> dict:
    data = yaml.safe_load(fh)
    return data if data else DEFAULT_INDEX.copy()


def _save(fh, data: dict) -> None:
    fh.seek(0)
    fh.truncate()
    fh.write('# product/prd/index.yml — traceability index, machine-maintained\n')
    yaml.dump(data, fh, default_flow_style=False, allow_unicode=True)


def allocate(index_path: str, slug: str) -> str:
    if not SLUG_RE.match(slug):
        print(f"Error: invalid slug '{slug}'. Use lowercase alphanumeric + hyphens, max 40 chars.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(index_path)), exist_ok=True)

    with open(index_path, 'a+') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        content = fh.read()
        if content.strip():
            data = yaml.safe_load(content)
            if not data:
                data = DEFAULT_INDEX.copy()
        else:
            data = DEFAULT_INDEX.copy()

        seq = data.get('next_prd_seq', 1)
        if not isinstance(seq, int) or seq < 1:
            print(f"Error: next_prd_seq in index must be a positive integer, got: {seq!r}", file=sys.stderr)
            sys.exit(1)

        prd_id = f'PRD-{seq:03d}'
        data['next_prd_seq'] = seq + 1

        if 'prds' not in data or data['prds'] is None:
            data['prds'] = {}

        _save(fh, data)
        fcntl.flock(fh, fcntl.LOCK_UN)

    return prd_id


def main() -> None:
    parser = argparse.ArgumentParser(description='Allocate next PRD ID from index.yml.')
    parser.add_argument('--index', required=True, help='Path to product/prd/index.yml')
    parser.add_argument('--slug', required=True, help='URL-safe slug (lowercase, hyphens, max 40 chars)')
    args = parser.parse_args()

    prd_id = allocate(args.index, args.slug)
    print(prd_id)


if __name__ == '__main__':
    main()
