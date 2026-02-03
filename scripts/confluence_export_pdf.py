#!/usr/bin/env python3
"""Export a Confluence page to PDF and save to disk.

Usage: python scripts/confluence_export_pdf.py PAGE_ID --url <CONFLUENCE_URL> [-o output.pdf]
"""
import os
import sys
import argparse
from atlassian import Confluence

def main():
    parser = argparse.ArgumentParser(description='Export a Confluence page to PDF and save to disk')
    parser.add_argument('page_id')
    parser.add_argument('--url', default=os.environ.get('CONFLUENCE_URL'), required=True,
                        help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
    parser.add_argument('-o', '--output', 'output_path', default=None,
                        help='Output path for PDF (defaults to confluence_page_<id>.pdf)')
    parser.add_argument('--username', default=os.environ.get('USERNAME'), help='Username')
    parser.add_argument('--password', default=os.environ.get('PASSWORD'), help='Password or token')
    parser.add_argument('--verify-ssl', dest='verify_ssl', action='store_true', help='Enable SSL verification (default: False)')

    args = parser.parse_args()

    try:
        confluence = Confluence(url=args.url, username=args.username, password=args.password, verify=args.verify_ssl)
        pdf_bytes = confluence.export_page(args.page_id)
    except Exception as e:
        print(f"Failed to export page {args.page_id}: {e}", file=sys.stderr)
        raise SystemExit(1) 

    if not pdf_bytes:
        print(f"No PDF content returned for page {args.page_id}", file=sys.stderr)
        raise SystemExit(1)

    out = args.output or f"confluence_page_{args.page_id}.pdf"
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
