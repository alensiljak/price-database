'''
Fixer.io
'''

def test_dl():
    ''' download from Fixer.io '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'GBP'])

    assert result is not None
    assert result.exit_code == 0
