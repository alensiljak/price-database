""" Mapping entities to domain model objects """
from datetime import datetime
from decimal import Decimal
from . import dal
from .model import PriceModel

class PriceMapper:
    """ Map price entity """
    def __init__(self):
        pass

    def map_entity(self, entity: dal.Price) -> PriceModel:
        """ Map the price entity """
        if not entity:
            return None

        result = PriceModel()
        result.currency = entity.currency

        # date/time
        dt_string = entity.date
        format_string = "%Y-%m-%d"
        if entity.time:
            dt_string += f"T{entity.time}"
            format_string += "T%H:%M:%S"
        result.datetime = datetime.strptime(dt_string, format_string)
        assert isinstance(result.datetime, datetime)

        result.namespace = entity.namespace
        result.symbol = entity.symbol
        # Value
        value = Decimal(entity.value) / Decimal(entity.denom)
        result.value = Decimal(value)

        return result
