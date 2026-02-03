#!/usr/bin/env python3
"""Get a Confluence page by ID and print JSON (includes body.storage when available).

Usage: python scripts/confluence_get_page.py PAGE_ID --url <CONFLUENCE_URL>
"""
import json
import os
import sys
import argparse
from atlassian import Confluence
from common_args import add_auth_args, get_auth_kwargs, environ_or_required
from confluence_utils import extract_space_and_title, extract_page_id

def main():
    parser = argparse.ArgumentParser(description='Get a Confluence page by ID and print JSON')
    parser.add_argument('page_url', help="Confluence page url(e.g. https://your-domain.atlassian.net/wiki/z/asa)")
    parser.add_argument('--url', **environ_or_required('CONFLUENCE_URL'),
                        help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
    add_auth_args(parser)

    args = parser.parse_args()

    auth_kwargs = get_auth_kwargs(args)
    client = Confluence(url=args.url, **auth_kwargs)
    try:
        page_id = extract_page_id(args.page_url)
        if not page_id:
            (space, title) = extract_space_and_title(args.page_url)
            page_id = client.get_page_id(space, title)
        
        page = client.get_page_by_id(page_id, expand='body.view')
        print(json.dumps(page, indent=2))
    except Exception as e:
        print(f"Error fetching page {args.page_id}: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
