# atlassian-cli 🔧

A minimal CLI wrapper around `atlassian-python-api` for **Jira** and **Confluence** built with `click`.

## Features ✅
- `jira get-issue ISSUE-KEY`
- `confluence get-page PAGE-ID`
- Read credentials from environment variables `USERNAME` and `PASSWORD` (shared between Jira and Confluence)
- Read base URLs from `JIRA_URL` / `CONFLUENCE_URL` environment variables or pass `--url`

## Quick start 💡

Install (editable):

```bash
python -m pip install -e .
```

Set credentials (shared):

```bash
set USERNAME=me@example.com
set PASSWORD=supersecret
set JIRA_URL=https://your-domain.atlassian.net
set CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
```

Usage examples:

```bash
# Jira
atlassian-cli jira get-issue ISSUE-1 --url https://your-domain.atlassian.net
# or if JIRA_URL is set in env:
atlassian-cli jira get-issue ISSUE-1

# Confluence
atlassian-cli confluence get-page 123456 --url https://your-domain.atlassian.net/wiki
```

Notes:
- If `USERNAME` / `PASSWORD` are not set, the CLI will prompt for them.
- Output is JSON printed to stdout.
