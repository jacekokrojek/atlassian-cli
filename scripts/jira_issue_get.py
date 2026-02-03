#!/usr/bin/env python3
"""Get a Jira issue and print JSON.

Usage: python scripts/jira_issue_get.py ISSUE-KEY
"""
import json
import os
import sys
import argparse
from atlassian import Jira
from common_args import add_auth_args, get_auth_kwargs ,environ_or_required

def main():
    parser = argparse.ArgumentParser(description='Get a Jira issue and print JSON')
    parser.add_argument('issue_key')
    parser.add_argument('--url', **environ_or_required('JIRA_URL'),
                        help='Jira base URL (e.g. https://your-domain.atlassian.net)')
    add_auth_args(parser)

    args = parser.parse_args()
    auth_kwargs = get_auth_kwargs(args)

    client = Jira(url=args.url, **auth_kwargs)
    try:
        issue = client.issue(args.issue_key)
        print(json.dumps(issue, indent=2))
    except Exception as e:
        print(f"Error fetching issue {args.issue_key}: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
