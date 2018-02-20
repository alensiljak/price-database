""" Domain model. Public """
from decimal import Decimal


class Price:
    """ The price element """
    def __init__(self):
        self.datetime = None
        self.namespace = None
        self.symbol = None
        self.value = Decimal(0)
        self.currency = None

    def __repr__(self):
        return f"<Price (date:{self.datetime},ns:{self.namespace},symbol:{self.symbol},value:{self.value},currency:{self.currency})>"
