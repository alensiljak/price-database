"""
Test (ledger) export
"""
from pricedb import PriceDbApplication

def test_export_all():
    """ export all prices """
    app = PriceDbApplication()
    prices = app.get_prices()
    prices.sort(key=lambda price: price.datum.date)
    assert prices is not None

def test_export_format():
    app = PriceDbApplication()
    result = app.ledger_export()
    assert result is not None

def test_security_export():
    app = PriceDbApplication()
    sec = app.get_security_list()
    assert sec is not None

def test_export_into_preset_file():
    ''' The file is set in the config '''
    app = PriceDbApplication()
    actual = app.ledger_export()

def test_prices_query():
    ''' Test the query that gets the symbol from the Security table '''
    from click.testing import CliRunner
    from pricedb.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ['export'])

    assert result is not None
    assert result.exit_code == 0
    