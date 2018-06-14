""" Test Vanguard downloader """
from pricedb import PriceDbApplication

app = PriceDbApplication()

def test_date():
    """ Test the price date """
    price = app.download_price("VANGUARD:BOND", "AUD", "vanguard")

    assert price is not None
