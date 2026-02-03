#!/usr/bin/env python3
"""Export a Confluence page to PDF and save to disk.

Usage: python scripts/confluence_export_pdf.py PAGE_ID --url <CONFLUENCE_URL> [-o output.pdf]
"""
import os
import sys
import argparse
from atlassian import Confluence
from common_args import add_auth_args, get_auth_kwargs, environ_or_required
from confluence_utils import extract_space_and_title, extract_page_id

def main():
    parser = argparse.ArgumentParser(description='Export a Confluence page to PDF and save to disk')
    parser.add_argument('page_url', help="Confluence page url(e.g. https://your-domain.atlassian.net/wiki/z/asa)")
    parser.add_argument('--url', **environ_or_required('CONFLUENCE_URL'),
                        help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output path for PDF (defaults to confluence_page_<id>.pdf)')
    add_auth_args(parser)

    args = parser.parse_args()
    auth_kwargs = get_auth_kwargs(args)

    try:
        confluence = Confluence(url=args.url, **auth_kwargs)
        page_id = extract_page_id(args.page_url)
        if not page_id:
            (space, title) = extract_space_and_title(args.page_url)
            page_id = confluence.get_page_id(space, title)
        
        pdf_bytes = confluence.export_page(page_id)
    except Exception as e:
        print(f"Failed to export page {args.page_url}: {e}", file=sys.stderr)
        raise SystemExit(1) 

    if not pdf_bytes:
        print(f"No PDF content returned for page {args.page_url}", file=sys.stderr)
        raise SystemExit(1)

    out = args.output or f"confluence_page_{page_id}.pdf"
    out = os.path.abspath(out)
    try:
        with open(out, 'wb') as fh:
            fh.write(pdf_bytes)
        print(f"Saved PDF to {out}")
        return
    except Exception as e:
        print(f"Failed to write PDF to {out}: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
