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
