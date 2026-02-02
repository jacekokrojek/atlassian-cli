#!/usr/bin/env python3
"""Get a Jira issue and print JSON.

Usage: python scripts/jira_issue_get.py ISSUE-KEY --url <JIRA_URL>
"""
import json
import click
from atlassian import Jira
try:
    from scripts.utils import require_auth
except Exception:
    # allow running script directly (e.g. python scripts/jira_issue_get.py)
    import importlib.util
    import pathlib

    utils_path = pathlib.Path(__file__).resolve().parent / 'utils.py'
    spec = importlib.util.spec_from_file_location("scripts.utils_local", str(utils_path))
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)
    require_auth = utils.require_auth


@click.command()
@click.argument('issue_key')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.option('--username', envvar='USERNAME', default=None, help='Username')
@click.option('--password', envvar='PASSWORD', default=None, help='Password or token')
def main(issue_key, url, username, password):
    username, password = require_auth(username, password)

    client = Jira(url=url, username=username, password=password)
    try:
        issue = client.issue(issue_key)
        click.echo(json.dumps(issue, indent=2))
    except Exception as e:
        click.echo(f"Error fetching issue {issue_key}: {e}", err=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
