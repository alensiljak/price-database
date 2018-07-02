""" Test retrieving the prices """

import logging
from decimal import Decimal
from pydatum import Datum
from pricedb import PriceDbApplication, PriceModel, SecuritySymbol


def test_latest(session):
    """
    Test fetching the latest price.
    The date is always today, even if the latest price is not from today!
    """
    # Preparation
    add_price(session)

    # Fetch the latest price for xy
    app = PriceDbApplication(session=session)
    symbol = SecuritySymbol("VANGUARD", "BOND")
    
    latest_price = app.get_latest_price(symbol)

    assert latest_price

    yesterday = Datum()
    yesterday.yesterday()
    yesterday.start_of_day()
    yesterday_str = yesterday.to_iso_date_string()
    assert latest_price.datum.to_iso_date_string() == yesterday

def add_price(session):
    """ Create a price entry for test(s) """
    value = Decimal("1.0548")

    app = PriceDbApplication(session=session)

    datum = Datum()
    datum.yesterday()

    symbol = SecuritySymbol("VANGUARD", "BOND")

    model = PriceModel()
    model.currency = "AUD"
    model.datum = datum
    model.symbol = symbol
    model.value = value

    app.add_price(model)

    # make sure that the price is there
    first = app.price_repo.query.first()
    assert first
    
    yesterday_str = datum.to_iso_date_string()
    assert first.date == yesterday_str

    assert first.currency == "AUD"
    assert first.value == 10548
    assert first.denom == 10000
