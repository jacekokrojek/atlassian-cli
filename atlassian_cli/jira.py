import json
import click
from atlassian import Jira
from .utils import require_auth


@click.group()
def jira():
    """Jira commands"""


@jira.group('issue')
def issue():
    """Issue related commands"""


@issue.command('get')
@click.argument('issue_key')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.pass_context
def issue_get(ctx, issue_key, url):
    """Get a Jira issue by key and print JSON."""
    username, password = require_auth(ctx)

    client = Jira(url=url, username=username, password=password)
    try:
        issue = client.issue(issue_key)
        click.echo(json.dumps(issue, indent=2))
    except Exception as e:
        click.echo(f"Error fetching issue {issue_key}: {e}", err=True)
        raise click.Abort()


@issue.command('search')
@click.argument('jql')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.option('--start', default=0, type=int, help='Start index for pagination')
@click.option('--limit', default=50, type=int, help='Max results per page')
@click.option('--all', 'all_pages', is_flag=True, help='Fetch all pages of results')
@click.pass_context
def issue_search(ctx, jql, url, start, limit, all_pages):
    """Search issues with JQL and support pagination. Use --all to fetch all pages."""
    username, password = require_auth(ctx)

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

                # If server provided total, use it to stop
                if total is not None:
                    start_at += len(issues)
                    if start_at >= total:
                        break
                else:
                    # otherwise stop when fewer issues than limit returned
                    if len(issues) < limit:
                        break
                    start_at += limit

            click.echo(json.dumps({'total': len(all_issues), 'issues': all_issues}, indent=2))
        else:
            res = fetch(start)
            click.echo(json.dumps(res, indent=2))

    except Exception as e:
        click.echo(f"Error performing JQL search: {e}", err=True)
        raise click.Abort()


# backward compatible command
@jira.command('get-issue')
@click.argument('issue_key')
@click.option('--url', envvar='JIRA_URL', required=True, help='Jira base URL (e.g. https://your-domain.atlassian.net)')
@click.pass_context
def get_issue(ctx, issue_key, url):
    """Backward compatible alias for `jira issue get`"""
    # delegate to new command implementation
    ctx.invoke(issue_get, issue_key=issue_key, url=url)
