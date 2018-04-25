""" Tests for utilities """
from pricedb import utils


def test_split_symbol_with_namespace():
    """ Test splitting the symbol with namespace """
    symbol = "ASX:VHY"
    namespace, mnemonic = utils.split_symbol(symbol)

    assert namespace == "ASX"
    assert mnemonic == "VHY"


def test_split_symbol_without_namespace():
    """ Test splitting the symbol without namespace """
    symbol = "VHY.AX"
    namespace, mnemonic = utils.split_symbol(symbol)

    assert namespace is None
    assert mnemonic == symbol
