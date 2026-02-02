#!/usr/bin/env python3
"""Get a Jira issue and print JSON.

Usage: python scripts/jira_issue_get.py ISSUE-KEY --url <JIRA_URL>
"""
import json
import click
from atlassian import Jira


@click.command()
@click.argument('issue_key')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.option('--username', envvar='USERNAME', prompt=True, help='Username')
@click.option('--password', envvar='PASSWORD', prompt=True, hide_input=True, help='Password or token')
def main(issue_key, url, username, password):
    # Username/password are provided via option, envvar, or prompted by Click if missing

    client = Jira(url=url, username=username, password=password)
    try:
        issue = client.issue(issue_key)
        click.echo(json.dumps(issue, indent=2))
    except Exception as e:
        click.echo(f"Error fetching issue {issue_key}: {e}", err=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
