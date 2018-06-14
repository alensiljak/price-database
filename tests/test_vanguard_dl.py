""" Test Vanguard downloader """
from pricedb import PriceDbApplication
from pydatum import Datum

app = PriceDbApplication()

def test_date():
    """ Test the price date """
    price = app.download_price("VANGUARD:BOND", "AUD", "vanguard_au")

    assert price is not None
    assert price.datum.time.hour == 0
