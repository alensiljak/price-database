""" main api point """
import logging
from datetime import datetime
#from logging import log, DEBUG
from .csv import CsvParser, CsvPrice
from . import dal, model, mappers
from .repositories import PriceRepository


class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = None
    
    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
        assert isinstance(file_path, str)
        assert isinstance(currency_symbol, str)

        self.logger.debug(f"Importing {file_path}")
        parser = CsvParser()
        prices = parser.parse_file(file_path)

        counter = 0
        session = self.__get_session()
        repo = PriceRepository(session)
        # Create insert statements
        for price in prices:
            new_price = self.__parse_price_into_entity(price, currency_symbol)
            # TODO check if the price already exists in db.
            existing = (
                repo.query
                    .filter(dal.Price.namespace == new_price.namespace)
                    .filter(dal.Price.symbol == new_price.symbol)
                    .filter(dal.Price.date == new_price.date)
                    .filter(dal.Price.time == new_price.time)
                    .first()
            )
            if existing:
                new_value = new_price.value / new_price.denom
                self.logger.info(f"Price already exists for {new_price.symbol} on {new_price.date}/{new_price.time}. Updating to {new_value}.")
                if new_price.currency != existing.currency:
                    raise ValueError(f"The currency is different for price {new_price}!")
                existing.value = new_price.value
                existing.denom = new_price.denom
            else:
                session.add(new_price)
            counter += 1
        # Save all to database
        session.commit()
        print(f"{counter} records inserted.")

    def __parse_price_into_entity(self, price: CsvPrice, currency: str) -> dal.Price:
        """ Parse into the Price entity, ready for saving """
        new_price = dal.Price()

        # Format date as ISO string
        date_iso = f"{price.date.year}-{price.date.month:02d}-{price.date.day:02d}"
        new_price.date = date_iso

        # Symbol
        # properly mapped symbols have a namespace, except for the US markets
        symbol_parts = price.symbol.split(":")
        new_price.symbol = price.symbol
        if len(symbol_parts) > 1:
            new_price.namespace = f"{symbol_parts[0]}"
            new_price.symbol = symbol_parts[1]

        # Find number of decimal places
        dec_places = abs(price.value.as_tuple().exponent)
        new_price.denom = 10 ** dec_places
        # Price value
        new_price.value = int(price.value * new_price.denom)

        # self.logger.debug(f"{new_price}")
        return new_price
    
    def get_latest_price(self, namespace: str, symbol: str) -> model.Price:
        """ Returns the latest price for the given symbol """
        # TODO should include the currency? Need a public model for exposing the result.
        from sqlalchemy import desc
        session = self.__get_session()
        repo = PriceRepository(session)
        query = (
            repo.query
                .filter(dal.Price.symbol == symbol)
                .order_by(desc(dal.Price.date), desc(dal.Price.time))
        )
        if namespace:
            query = query.filter(dal.Price.namespace == namespace)

        latest = query.first()

        # map
        mapper = mappers.PriceMapper()
        result = mapper.map_entity(latest)

        return result

    def __get_session(self):
        """ Returns the current db session """
        if not self.session:
            self.session = dal.get_default_session()
        return self.session
