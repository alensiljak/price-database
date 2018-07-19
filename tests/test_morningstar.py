""" Test Morningstar downloader """
from pricedb import PriceDbApplication
from pydatum import Datum
from decimal import Decimal

app = PriceDbApplication()

def test_date():
    """ Test the price date """
    price = app.download_price("ASX:VTS", "AUD", "morningstar")

    assert price is not None
    assert price.value > Decimal(0)
    #assert price.datum.time.hour == 0
    #assert price.datum.time.minute == 0
    #assert price.datum.time.second == 0
