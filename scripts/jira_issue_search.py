#!/usr/bin/env python3
"""Search Jira issues via JQL and print JSON.

Usage: python scripts/jira_issue_search.py 'project = XYZ' --url <JIRA_URL> [--start] [--limit] [--all]
"""
import json
import click
from atlassian import Jira


@click.command()
@click.argument('jql')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.option('--start', default=0, type=int, help='Start index for pagination')
@click.option('--limit', default=50, type=int, help='Max results per page')
@click.option('--all', 'all_pages', is_flag=True, help='Fetch all pages of results')
@click.option('--username', envvar='USERNAME', prompt=True, help='Username')
@click.option('--password', envvar='PASSWORD', prompt=True, hide_input=True, help='Password or token')
def main(jql, url, start, limit, all_pages, username, password):
    # Username/password are provided via option, envvar, or prompted by Click if missing

    client = Jira(url=url, username=username, password=password)
    try:
        def fetch(start_at):
            return client.jql(jql, start=start_at, limit=limit)

        if all_pages:
            all_issues = []
            start_at = start
            while True:
                res = fetch(start_at)
                if isinstance(res, dict):
                    issues = res.get('issues', [])
                    total = res.get('total')
                else:
                    issues = res or []
                    total = None

                if not issues:
                    break

                all_issues.extend(issues)

                if total is not None:
                    start_at += len(issues)
                    if start_at >= total:
                        break
                else:
                    if len(issues) < limit:
                        break
                    start_at += limit

            click.echo(json.dumps({'total': len(all_issues), 'issues': all_issues}, indent=2))
        else:
            res = fetch(start)
            click.echo(json.dumps(res, indent=2))

    except Exception as e:
        click.echo(f"Error performing JQL search: {e}", err=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
