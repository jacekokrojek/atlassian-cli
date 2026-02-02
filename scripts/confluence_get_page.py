#!/usr/bin/env python3
"""Get a Confluence page by ID and print JSON (includes body.storage when available).

Usage: python scripts/confluence_get_page.py PAGE_ID --url <CONFLUENCE_URL>
"""
import json
import os
import sys
import argparse
from atlassian import Confluence

def main():
    parser = argparse.ArgumentParser(description='Get a Confluence page by ID and print JSON')
    parser.add_argument('page_id')
    parser.add_argument('--url', default=os.environ.get('CONFLUENCE_URL'), required=True,
                        help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
    parser.add_argument('--username', default=os.environ.get('USERNAME'), help='Username')
    parser.add_argument('--password', default=os.environ.get('PASSWORD'), help='Password or token')

    args = parser.parse_args()

    client = Confluence(url=args.url, username=args.username, password=args.password)
    try:
        page = client.get_page_by_id(args.page_id, expand='body.view')
        print(json.dumps(page, indent=2))
    except Exception as e:
        print(f"Error fetching page {args.page_id}: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
