from click.testing import CliRunner
from atlassian_cli.cli import cli


def test_help_shows():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Jira' in result.output or 'Confluence' in result.output
