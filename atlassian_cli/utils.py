import click


def require_auth(ctx):
    """Return (username, password), prompting if not provided in context or env.

    Username and PASSWORD can be provided via env variables `USERNAME` and `PASSWORD`.
    """
    username = ctx.obj.get('username') or click.prompt('Username')
    password = ctx.obj.get('password') or click.prompt('Password', hide_input=True)
    return username, password
