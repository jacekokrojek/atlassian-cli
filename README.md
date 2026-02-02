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
# Install in editable/development mode:
python -m pip install -e .
# or (if you have pip on PATH):
pip install -e .
```

After installation a console script named `atlassian-cli` will be available; you can run it directly without prefixing with `python`.

Set credentials (shared):

```bash
set USERNAME=me@example.com
set PASSWORD=supersecret
set JIRA_URL=https://your-domain.atlassian.net
set CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
```

Usage examples:

```bash
# Jira (package entrypoint)
atlassian-cli jira get-issue ISSUE-1 --url https://your-domain.atlassian.net
# or if JIRA_URL is set in env:
atlassian-cli jira get-issue ISSUE-1

# Confluence (package entrypoint)
atlassian-cli confluence get-page 123456 --url https://your-domain.atlassian.net/wiki
```

Or, run individual standalone scripts (no package import needed):

```bash
# Jira: get an issue
python scripts/jira_issue_get.py ISSUE-1 --url https://your-domain.atlassian.net

# Jira: JQL search
python scripts/jira_issue_search.py "project = MYPROJ" --url https://your-domain.atlassian.net --all

# Confluence: get page
python scripts/confluence_get_page.py 123456 --url https://your-domain.atlassian.net/wiki

# Confluence: export to PDF
python scripts/confluence_export_pdf.py 123456 --url https://your-domain.atlassian.net/wiki -o page123.pdf
```

Notes:
- If `USERNAME` / `PASSWORD` are not set, the scripts will prompt for them.
- Output is JSON printed to stdout (unless the command writes a file, e.g. PDF export).
