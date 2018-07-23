""" Mapping entities to domain model objects """
from datetime import datetime
from decimal import Decimal
from pydatum import Datum
from . import dal
from .dal import Price
from .model import PriceModel, SecuritySymbol


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
        price_datetime = datetime.strptime(dt_string, format_string)
        result.datum = Datum()
        result.datum.from_datetime(price_datetime)
        assert isinstance(result.datum, Datum)

        #result.namespace = entity.namespace
        #result.symbol = entity.symbol
        result.symbol = SecuritySymbol(entity.namespace, entity.symbol)

        # Value
        value = Decimal(entity.value) / Decimal(entity.denom)
        result.value = Decimal(value)

        return result

    def map_model(self, model: PriceModel) -> Price:
        """ Parse into the Price entity, ready for saving """
        # assert isinstance(model, PriceModel)
        assert isinstance(model.symbol, SecuritySymbol)
        assert isinstance(model.datum, Datum)

        entity = Price()

        # Format date as ISO string
        date_iso = f"{model.datum.value.year}-{model.datum.value.month:02d}-{model.datum.value.day:02d}"
        entity.date = date_iso

        entity.time = f"{model.datum.value.hour:02d}:{model.datum.value.minute:02d}:{model.datum.value.second:02d}"

        # Symbol
        # properly mapped symbols have a namespace, except for the US markets
        # TODO check this with .csv import
        if model.symbol.namespace:
            entity.namespace = model.symbol.namespace.upper()
        entity.symbol = model.symbol.mnemonic.upper()

        assert isinstance(model.value, Decimal)
        # Find number of decimal places
        dec_places = abs(model.value.as_tuple().exponent)
        entity.denom = 10 ** dec_places
        # Price value
        entity.value = int(model.value * entity.denom)

        # Currency
        entity.currency = model.currency.upper()

        # self.logger.debug(f"{entity}")
        return entity
