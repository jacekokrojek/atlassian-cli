#!/usr/bin/env python3
"""Minimal auth helper for standalone scripts.

Provides require_auth(username=None, password=None) which uses provided
values, then env variables, then prompts via click.
"""
import os
import click


def require_auth(username=None, password=None):
    username = username or os.environ.get('USERNAME')
    password = password or os.environ.get('PASSWORD')

    if not username:
        username = click.prompt('Username')
    if not password:
        password = click.prompt('Password', hide_input=True)

    return username, password
