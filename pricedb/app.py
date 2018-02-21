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
        # Create insert statements
        for price in prices:
            command = self.__parse_price_into_insert_command(price, currency_symbol)
            self.logger.debug(command)
            session.execute(command)
            counter += 1
        # Save all to database
        session.commit()
        print(f"{counter} records inserted.")

    def __parse_price_into_insert_command(self, price: CsvPrice, currency: str) -> str:
        """ Parses a CSV line into an INSERT command """
        # Format date as ISO string
        date_iso = f"{price.date.year}-{price.date.month}-{price.date.day}" 
        
        # CSV prices are with 2 decimals right now
        store_value = price.value * 100
        store_denom = 100
        
        # properly mapped symbols have a namespace, except for the US markets
        symbol_parts = price.symbol.split(":")
        namespace = "NULL"
        symbol = price.symbol
        if len(symbol_parts) > 1:
            namespace = f"'{symbol_parts[0]}'"
            symbol = symbol_parts[1]

        # Assemble the insert statement.
        header = "namespace,symbol,date,value,denom,currency"
        command = f"insert into price ({header}) values ({namespace},'{symbol}','{date_iso}',{store_value},{store_denom},'{currency}');"
        
        return command

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
