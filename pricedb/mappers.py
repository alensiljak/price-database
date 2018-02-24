""" Mapping entities to domain model objects """
from datetime import datetime
from decimal import Decimal
from . import dal, utils
from .dal import Price
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

    def map_model(self, price: PriceModel) -> Price:
        """ Parse into the Price entity, ready for saving """
        new_price = Price()

        # Format date as ISO string
        date_iso = f"{price.datetime.year}-{price.datetime.month:02d}-{price.datetime.day:02d}"
        new_price.date = date_iso

        # Symbol
        price.symbol = price.symbol.upper()
        # properly mapped symbols have a namespace, except for the US markets
        new_price.namespace, new_price.symbol = utils.split_symbol(price.symbol)

        # Find number of decimal places
        dec_places = abs(price.value.as_tuple().exponent)
        new_price.denom = 10 ** dec_places
        # Price value
        new_price.value = int(price.value * new_price.denom)

        # Currency
        new_price.currency = price.currency.upper()

        # self.logger.debug(f"{new_price}")
        return new_price
