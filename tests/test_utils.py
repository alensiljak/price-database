""" Tests for utilities """
from pricedb import SecuritySymbol


def test_split_symbol_with_namespace():
    """ Test splitting the symbol with namespace """
    symbol = "ASX:VHY"
    sec_symbol = SecuritySymbol(None, None)
    sec_symbol.parse(symbol)

    assert sec_symbol.namespace == "ASX"
    assert sec_symbol.mnemonic == "VHY"


def test_split_symbol_without_namespace():
    """ Test splitting the symbol without namespace """
    symbol = "VHY.AX"
    sec_symbol = SecuritySymbol("", "")
    sec_symbol.parse(symbol)

    assert sec_symbol.namespace is None
    assert sec_symbol.mnemonic == symbol
