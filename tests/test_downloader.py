""" Test price download and parsing """
from finance_quote_python import Quote
from pricedb import PriceDbApplication

def test_ms_price_dl():
    """ test price download """
    uat = Quote()
    uat.set_source("morningstar")
    #actual = uat.download("ASX:VHY", "AUD", "morningstar")
    result = uat.fetch("ASX", ["VHY"])
    actual = result[0]

    assert actual is not None
    assert actual.currency == "AUD"

def test_fixerio():
    uat = Quote()
    #actual = uat.download("AUD", "EUR", "fixerio")
    uat.set_source("fixerio")
    result = uat.currency("AUD", "EUR")

    assert result

    #actual = result[0]
    actual = result

    assert actual is not None
    assert actual
    assert actual.currency == "EUR"
    assert actual.symbol.namespace == "CURRENCY"
    assert actual.symbol.mnemonic == "AUD"

def test_download_using_symbols_in_db():
    """ Download the prices that are listed in db.
    Used for debugging
    """
    app = PriceDbApplication()
    app.download_prices()

# def test_dl_bnd():
#     """ download BND quote """
#     app = PriceDbApplication()
#     price = app.download_price("NYSEARCA:VTI", "USD", "morningstar")
#     assert price
#     price = app.download_price("NYSEARCA:BND", "USD", "morningstar")
#     assert price

# def test_dl_all():
#     app = PriceDbApplication()
#     result = app.download_prices(currency=None, agent=None, symbol=None, exchange=None)
#     assert result is not None

# def test_dl_currency():
#     app = PriceDbApplication()
#     actual = app.download_prices(symbol='AUD')
#     #assert actual is not None

def test_dl_currency_cli():
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'AUD'])

    assert result is not None
    assert result.exit_code == 0

def test_yahoo_dl():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['dl', '-s', 'kbwy'])

    assert result is not None
    assert result.exit_code == 0
