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

    def map_model(self, model: PriceModel) -> Price:
        """ Parse into the Price entity, ready for saving """
        entity = Price()

        # Format date as ISO string
        date_iso = f"{model.datetime.year}-{model.datetime.month:02d}-{model.datetime.day:02d}"
        entity.date = date_iso

        entity.time = f"{model.datetime.hour:02d}:{model.datetime.minute:02d}:{model.datetime.second:02d}"

        # Symbol
        # properly mapped symbols have a namespace, except for the US markets
        # TODO check this with .csv import
        # entity.namespace, entity.symbol = utils.split_symbol(model.symbol)
        if model.namespace:
            entity.namespace = model.namespace.upper()
        entity.symbol = model.symbol.upper()

        # Find number of decimal places
        dec_places = abs(model.value.as_tuple().exponent)
        entity.denom = 10 ** dec_places
        # Price value
        entity.value = int(model.value * entity.denom)

        # Currency
        entity.currency = model.currency.upper()

        # self.logger.debug(f"{entity}")
        return entity
