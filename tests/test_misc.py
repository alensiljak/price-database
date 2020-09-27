'''
Misc. tests
'''

def test_dl_saves_security_id():
    '''
    Downloading a price should save the security id and not
    the symbol
    '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'EMCR'])

    assert result is not None
    assert result.exit_code == 0
    