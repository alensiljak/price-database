""" Test price download and parsing """
from pricedb.download import PriceDownloader
from pricedb import PriceDbApplication


def test_ms_price_dl():
    """ test price download """
    uat = PriceDownloader()
    actual = uat.download("ASX:VHY", "AUD", "morningstar")

    assert actual is not None
    assert actual.currency == "AUD"


# def test_vg_price_dl():
#     """ test vg price download """
#     uat = PriceDownloader()
#     actual = uat.download("Vanguard:HY")

#     assert actual is not None

def test_fixerio():
    uat = PriceDownloader()
    actual = uat.download("AUD", "EUR", "fixerio")

    assert actual is not None

def test_download_using_symbols_in_db():
    """ Download the prices that are listed in db. 
    Used for debugging
    """
    app = PriceDbApplication()
    app.download_prices_in_db()
