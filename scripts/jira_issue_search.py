#!/usr/bin/env python3
"""Search Jira issues via JQL and print JSON.

Usage: python scripts/jira_issue_search.py 'project = XYZ' --url <JIRA_URL> [--start] [--limit] [--all]
"""
import json
import os
import sys
import argparse
from atlassian import Jira
from atlassian_cli.utils import require_auth


def main():
    parser = argparse.ArgumentParser(description='Search Jira issues via JQL and print JSON')
    parser.add_argument('jql')
    parser.add_argument('--url', default=os.environ.get('JIRA_URL'), required=True,
                        help='Jira base URL (e.g. https://your-domain.atlassian.net)')
    parser.add_argument('--start', type=int, default=0, help='Start index for pagination')
    parser.add_argument('--limit', type=int, default=50, help='Max results per page')
    parser.add_argument('--all', dest='all_pages', action='store_true', help='Fetch all pages of results')
    parser.add_argument('--username', default=os.environ.get('USERNAME'), help='Username')
    parser.add_argument('--password', default=os.environ.get('PASSWORD'), help='Password or token')

    args = parser.parse_args()

    client = Jira(url=args.url, username=args.username, password=args.password)
    try:
        def fetch(start_at):
            return client.jql(args.jql, start=start_at, limit=args.limit)

        if args.all_pages:
            all_issues = []
            start_at = args.start
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
                    if len(issues) < args.limit:
                        break
                    start_at += args.limit

            print(json.dumps({'total': len(all_issues), 'issues': all_issues}, indent=2))
        else:
            res = fetch(args.start)
            print(json.dumps(res, indent=2))

    except Exception as e:
        print(f"Error performing JQL search: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
