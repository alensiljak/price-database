""" Test price download and parsing """
from pricedb.download import PriceDownloader

def test_ms_price_dl():
    """ test price download """
    uat = PriceDownloader()
    actual = uat.download("ASX:VHY")

    assert actual is not None
    assert actual.currency == "AUD"

# def test_vg_price_dl():
#     """ test vg price download """
#     uat = PriceDownloader()
#     actual = uat.download("Vanguard:HY")

#     assert actual is not None
