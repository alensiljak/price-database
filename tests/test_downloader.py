""" Test price download and parsing """
from pricedb.download import PriceDownloader

def test_ms_price_dl():
    """ test price download """
    uat = PriceDownloader()
    actual = uat.download("ASX:VHY")

    assert actual is not None
