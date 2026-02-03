"""Simple helpers to add common CLI auth and SSL args.

Keep this minimal: scripts can call add_auth_args(parser) and then
use get_auth_kwargs(args) to obtain keyword args for client constructors.
"""
import os
def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )

def add_auth_args(parser):
    """Add common auth-related CLI arguments to an argparse parser.

    Adds:
      --username (defaults to $USERNAME)
      --password (defaults to $PASSWORD)
      --verify-ssl (boolean flag, default False)
    """
    parser.add_argument('--username', **environ_or_required('USERNAME'), help='Username')
    parser.add_argument('--password', **environ_or_required('PASSWORD'), help='Password or token')
    parser.add_argument('--verify-ssl', dest='verify_ssl', action='store_true', help='Enable SSL verification (default: False)')

def get_auth_kwargs(args):
    """Return a dict of kwargs for client constructors based on parsed args."""
    return {
        'username': args.username,
        'password': args.password,
        'verify_ssl': args.verify_ssl,
    }

