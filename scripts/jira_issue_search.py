#!/usr/bin/env python3
"""Search Jira issues via JQL and print JSON.

Usage: python scripts/jira_issue_search.py 'project = XYZ' --url <JIRA_URL> [--start] [--limit] [--all]
"""
import json
import os
import sys
import argparse
from atlassian import Jira
from scripts.common_args import add_auth_args, get_auth_kwargs,environ_or_required


def main():
    parser = argparse.ArgumentParser(description='Search Jira issues via JQL and print JSON')
    parser.add_argument('jql')
    parser.add_argument('--url', **environ_or_required('JIRA_URL'),
                        help='Jira base URL (e.g. https://your-domain.atlassian.net)')
    parser.add_argument('--start', type=int, default=0, help='Start index for pagination')
    parser.add_argument('--limit', type=int, default=50, help='Max results per page')
    parser.add_argument('--all', dest='all_pages', action='store_true', help='Fetch all pages of results')
    add_auth_args(parser)

    args = parser.parse_args()
    auth_kwargs = get_auth_kwargs(args)

    client = Jira(url=args.url, **auth_kwargs)
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
