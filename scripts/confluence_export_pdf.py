#!/usr/bin/env python3
"""Export a Confluence page to PDF and save to disk.

Usage: python scripts/confluence_export_pdf.py PAGE_ID --url <CONFLUENCE_URL> [-o output.pdf]
"""
import os
import click
import requests


@click.command()
@click.argument('page_id')
@click.option('--url', envvar='CONFLUENCE_URL', required=True, help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
@click.option('-o', '--output', 'output_path', default=None, help='Output path for PDF (defaults to confluence_page_<id>.pdf)')
@click.option('--username', envvar='USERNAME', prompt=True, help='Username')
@click.option('--password', envvar='PASSWORD', prompt=True, hide_input=True, help='Password or token')
def main(page_id, url, output_path, username, password):
    # Username/password are provided via option, envvar, or prompted by Click if missing

    session = requests.Session()
    session.auth = (username, password)

    base = url.rstrip('/')
    candidates = [
        f"{base}/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}",
        f"{base}/wiki/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}",
        f"{base}/export/pdf?pageId={page_id}",
        f"{base}/rest/api/content/{page_id}/export/pdf",
    ]

    last_resp = None
    for ep in candidates:
        try:
            resp = session.get(ep, stream=True, timeout=30)
        except Exception as e:
            last_resp = e
            continue

        last_resp = resp
        content_type = resp.headers.get('Content-Type', '')
        if resp.status_code == 200 and 'pdf' in content_type.lower():
            out = output_path or f"confluence_page_{page_id}.pdf"
            out = os.path.abspath(out)
            try:
                with open(out, 'wb') as fh:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            fh.write(chunk)
                click.echo(f"Saved PDF to {out}")
                return
            except Exception as e:
                click.echo(f"Failed to write PDF to {out}: {e}", err=True)
                raise SystemExit(1)

    if hasattr(last_resp, 'status_code'):
        click.echo(f"Failed to export page {page_id}. Last endpoint returned {last_resp.status_code} {last_resp.reason}", err=True)
    else:
        click.echo(f"Failed to export page {page_id}: {last_resp}", err=True)
    raise SystemExit(1)


if __name__ == '__main__':
    main()
