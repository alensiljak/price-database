"""
Development tests
"""
from pricedb import PriceDbApplication


def test_latest_prices():
    """ Get the latest prices """
    app = PriceDbApplication()
    latest = app.get_latest_prices()

    assert latest is not None


def test_dl_prices_for_currency():
    """ See if only prices for USD get downloaded.
    Testing the securities filter.
    """
    app = PriceDbApplication()
    app.download_prices_in_db(currency="USD")
