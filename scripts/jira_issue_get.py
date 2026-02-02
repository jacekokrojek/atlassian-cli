#!/usr/bin/env python3
"""Get a Jira issue and print JSON.

Usage: python scripts/jira_issue_get.py ISSUE-KEY --url <JIRA_URL>
"""
import json
import os
import sys
import argparse
from atlassian import Jira

def main():
    parser = argparse.ArgumentParser(description='Get a Jira issue and print JSON')
    parser.add_argument('issue_key')
    parser.add_argument('--url', default=os.environ.get('JIRA_URL'), required=True,
                        help='Jira base URL (e.g. https://your-domain.atlassian.net)')
    parser.add_argument('--username', default=os.environ.get('USERNAME'), help='Username')
    parser.add_argument('--password', default=os.environ.get('PASSWORD'), help='Password or token')

    args = parser.parse_args()

    client = Jira(url=args.url, username=args.username, password=args.password)
    try:
        issue = client.issue(args.issue_key)
        print(json.dumps(issue, indent=2))
    except Exception as e:
        print(f"Error fetching issue {args.issue_key}: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
