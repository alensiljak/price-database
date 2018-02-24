""" Domain model. Public """
from decimal import Decimal
from datetime import datetime


class PriceModel:
    """ The price element """
    def __init__(self):
        self.datetime: datetime = None
        self.namespace: str = None
        self.symbol: str = None
        self.value: Decimal = Decimal(0)
        self.currency: str = None

    def __repr__(self):
        symbol = f"{self.namespace}:{self.symbol}" if self.namespace else self.symbol
        symbol = f"{symbol:<13}"
        return f"<Price ('{symbol}',date:{self.datetime},value:{self.value},currency:{self.currency})>"
