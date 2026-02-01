from click.testing import CliRunner
from atlassian_cli.cli import cli


def test_jira_issue_get_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['jira', 'issue', 'get', '--help'])
    assert result.exit_code == 0
    assert 'ISSUE_KEY' in result.output or 'issue_key' in result.output


def test_jira_issue_search_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['jira', 'issue', 'search', '--help'])
    assert result.exit_code == 0
    assert '--all' in result.output
    assert '--start' in result.output
    assert '--limit' in result.output
