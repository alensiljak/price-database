""" Mapping entities to domain model objects """
from datetime import datetime
from . import dal
from . import model

class PriceMapper:
    """ Map price entity """
    def __init__(self):
        pass
    
    def map_entity(self, entity: dal.Price) -> model.Price:
        """ Map the price entity """
        result = model.Price()
        result.currency = entity.currency

        # date/time
        dt_string = entity.date
        format_string = "%Y-%m-%d"
        if entity.time:
            dt_string += f"T{entity.time}"
            format_string += f"T%H:%M:%S"
        result.datetime = datetime.strptime(dt_string, format_string)
        assert isinstance(result.datetime, datetime)

        result.namespace = entity.namespace
        result.symbol = entity.symbol
        result.value = entity.value / entity.denom

        return result
