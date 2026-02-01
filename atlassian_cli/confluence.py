import json
import click
import os
import requests
from atlassian import Confluence
from .utils import require_auth


@click.group()
def confluence():
    """Confluence commands"""


@confluence.command('get-page')
@click.argument('page_id')
@click.option('--url', envvar='CONFLUENCE_URL', required=True, help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
@click.pass_context
def get_page(ctx, page_id, url):
    """Get a Confluence page by ID and print JSON (includes body.storage when available)."""
    username, password = require_auth(ctx)

    client = Confluence(url=url, username=username, password=password)
    try:
        page = client.get_page_by_id(page_id, expand='body.storage')
        click.echo(json.dumps(page, indent=2))
    except Exception as e:
        click.echo(f"Error fetching page {page_id}: {e}", err=True)
        raise click.Abort()


@confluence.group('export')
def export():
    """Export content commands"""


@export.command('pdf')
@click.argument('page_id')
@click.option('--url', envvar='CONFLUENCE_URL', required=True, help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
@click.option('-o', '--output', 'output_path', default=None, help='Output path for PDF (defaults to confluence_page_<id>.pdf)')
@click.pass_context
def export_pdf(ctx, page_id, url, output_path):
    """Export a Confluence page to PDF and save to disk.

    This tries a few known endpoints used by Confluence Server/Cloud and writes the first successful PDF response to --output or a default filename.
    """
    username, password = require_auth(ctx)

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
                raise click.Abort()

    # If we reach here, none of the endpoints returned a PDF
    if isinstance(last_resp, requests.Response):
        click.echo(f"Failed to export page {page_id}. Last endpoint returned {last_resp.status_code} {last_resp.reason}", err=True)
    else:
        click.echo(f"Failed to export page {page_id}: {last_resp}", err=True)
    raise click.Abort()

