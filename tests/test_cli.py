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


def test_namespace_parameter(session):
    """
    Test that the namespace parameter filters out appropriate symbols.
    Debugging test.
    """
    from pricedb.dal import Security

    # Arrange
    app = PriceDbApplication(session)
    repo = app.get_security_repository()
    sec = Security()
    sec.symbol = "BOND"
    sec.namespace = "VANGUARD"
    sec.updater = "vanguard_au"
    sec.currency = "AUD"
    repo.session.add(sec)

    # Act
    app.download_prices(namespace="vanguard")

    # Assert
    prices = app.get_latest_prices()
    assert prices
    