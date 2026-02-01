#!/usr/bin/env python3
"""Top-level CLI group."""
import click
from .jira import jira as jira_group
from .confluence import confluence as confluence_group


@click.group()
@click.option('--username', envvar='USERNAME', help='Username for both Jira and Confluence')
@click.option('--password', envvar='PASSWORD', help='Password or token for both Jira and Confluence', prompt=False, hide_input=True)
@click.pass_context
def cli(ctx, username, password):
    """Atlassian CLI wrapper for Jira and Confluence"""
    ctx.ensure_object(dict)
    ctx.obj['username'] = username
    ctx.obj['password'] = password


# register sub-commands
cli.add_command(jira_group)
cli.add_command(confluence_group)
