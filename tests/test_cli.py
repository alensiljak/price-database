"""
Development tests
"""
from pricedb import PriceDbApplication


def test_latest_prices():
    """ Get the latest prices """
    app = PriceDbApplication()
    latest = app.get_latest_prices()

    assert latest is not None


def test_dl_prices_for_currency(session):
    """ See if only prices for USD get downloaded.
    Testing the securities filter.
    """
    # TODO add at least one symbol with USD currency to the in-memory database first

    app = PriceDbApplication(session=session)
    app.download_prices(currency="USD")


# def test_namespace_parameter(session):
#     """
#     Test that the namespace parameter filters out appropriate symbols.
#     Debugging test.
#     """
#     from pricedb.dal import Security

#     # Arrange
#     app = PriceDbApplication(session)
#     repo = app.get_security_repository()
#     sec = Security()
#     sec.symbol = "BOND"
#     sec.namespace = "VANGUARD"
#     sec.updater = "vanguard_au"
#     sec.currency = "AUD"
#     repo.session.add(sec)

#     # Act
#     app.download_prices(namespace="vanguard")

#     # Assert
#     prices = app.get_latest_prices()
#     assert prices

def test_price_dl():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'emcr'])

    assert result is not None
    assert result.exit_code == 0

def test_prune():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['prune'])

    assert result is not None
    assert result.exit_code == 0

def test_export():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['export'])

    assert result is not None
    assert result.exit_code == 0

def test_dl_wrong_symbol():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'vexx'])

    assert result is not None
    assert result.exit_code == 0

def test_list():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['list'])

    assert result is not None
    assert result.exit_code == 0

def test_last():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['last'])

    assert result is not None
    assert result.exit_code == 0

def test_last_with_symbol():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['last', '-s', 'prop'])

    assert result is not None
    assert result.exit_code == 0
