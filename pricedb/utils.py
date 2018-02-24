""" Various utilities """

def split_symbol(symbol: str) -> (str, str):
    """ Splits the symbol into namespace, symbol tuple """
    symbol_parts = symbol.split(":")
    namespace = None
    mnemonic = symbol

    if len(symbol_parts) > 1:
        namespace = symbol_parts[0]
        mnemonic = symbol_parts[1]

    return (namespace, mnemonic)
