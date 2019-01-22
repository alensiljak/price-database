""" Domain model. Public """

class SecuritySymbol:
    """ Symbol security, using namespace and the mnemonic """
    def __init__(self, namespace: str, mnemonic: str):
        self.namespace = namespace
        self.mnemonic = mnemonic

    def __repr__(self):
        if self.namespace:
            return f"{self.namespace}:{self.mnemonic}"
        else:
            return self.mnemonic

    def parse(self, symbol: str) -> (str, str):
        """ Splits the symbol into namespace, symbol tuple """
        symbol_parts = symbol.split(":")
        namespace = None
        mnemonic = symbol

        if len(symbol_parts) > 1:
            namespace = symbol_parts[0]
            mnemonic = symbol_parts[1]

        self.namespace = namespace
        self.mnemonic = mnemonic

        return namespace, mnemonic


class PriceModel:
    """ The price element """
    def __init__(self):
        from decimal import Decimal
        from pydatum import Datum

        # self.datetime: datetime = None
        self.datum: Datum = Datum()
        self.symbol: SecuritySymbol = SecuritySymbol("", "")
        self.value: Decimal = Decimal(0)
        self.currency: str = None

    def __repr__(self):
        symbol = f"{str(self.symbol):<13}"

        value = f"{self.value:>6}"
        return f"<Price ('{symbol}', date:{self.datum}, value:{value}, currency:{self.currency})>"
