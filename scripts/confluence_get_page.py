#!/usr/bin/env python3
"""Get a Confluence page by ID and print JSON (includes body.storage when available).

Usage: python scripts/confluence_get_page.py PAGE_ID --url <CONFLUENCE_URL>
"""
import json
import click
from atlassian import Confluence


@click.command()
@click.argument('page_id')
@click.option('--url', envvar='CONFLUENCE_URL', required=True, help='Confluence base URL (e.g. https://your-domain.atlassian.net/wiki)')
@click.option('--username', envvar='USERNAME', prompt=True, help='Username')
@click.option('--password', envvar='PASSWORD', prompt=True, hide_input=True, help='Password or token')
def main(page_id, url, username, password):
    # Username/password are provided via option, envvar, or prompted by Click if missing

    client = Confluence(url=url, username=username, password=password)
    try:
        page = client.get_page_by_id(page_id, expand='body.storage')
        click.echo(json.dumps(page, indent=2))
    except Exception as e:
        click.echo(f"Error fetching page {page_id}: {e}", err=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
