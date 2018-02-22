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
        return f"<Price ('{self.namespace}:{self.symbol}'date:{self.datetime},value:{self.value},currency:{self.currency})>"
