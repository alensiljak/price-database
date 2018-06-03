"""
Tests for debugging
Place a breakpoint in the coded and debug the test which calls it.
"""
from pricedb import PriceDbApplication


def test_debug_fixerio():
    """ Debug fixerio download for currencies """

    # pricedb dl -a fixerio -f symbols-fixerio-eur.txt -c eur
    app = PriceDbApplication()
    result = app.download_price("AUD", "EUR", "fixerio")
    assert result is not None


def test_debug_aud_morningstar():
    """ Debug download for aud quote """
    app = PriceDbApplication()
    result = app.download_price("ASX:AEF", "AUD", "morningstar")
    assert result is not None
