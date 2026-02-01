from click.testing import CliRunner
from atlassian_cli.cli import cli


def test_confluence_export_pdf_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['confluence', 'export', 'pdf', '--help'])
    assert result.exit_code == 0
    assert '--output' in result.output or '-o' in result.output
