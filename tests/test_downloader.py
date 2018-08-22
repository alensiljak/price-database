""" Test price download and parsing """
from finance_quote_python import Quote
from pricedb import PriceDbApplication


def test_ms_price_dl():
    """ test price download """
    uat = Quote()
    uat.set_source("morningstar")
    #actual = uat.download("ASX:VHY", "AUD", "morningstar")
    result = uat.fetch("ASX", ["VHY"])
    actual = result[0]

    assert actual is not None
    assert actual.currency == "AUD"


# def test_vg_price_dl():
#     """ test vg price download """
#     uat = PriceDownloader()
#     actual = uat.download("Vanguard:HY")

#     assert actual is not None

def test_fixerio():
    uat = Quote()
    #actual = uat.download("AUD", "EUR", "fixerio")
    uat.set_source("fixerio")
    result = uat.currency("AUD", "EUR")

    assert result

    actual = result[0]

    assert actual is not None
    assert actual


def test_download_using_symbols_in_db():
    """ Download the prices that are listed in db. 
    Used for debugging
    """
    app = PriceDbApplication()
    app.download_prices()
