""" main api point """
import logging
#from logging import log, DEBUG
from .csv import CsvParser, CsvPrice
from . import dal


class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
        assert isinstance(file_path, str)
        assert isinstance(currency_symbol, str)

        self.logger.debug(f"Importing {file_path}")
        parser = CsvParser()
        prices = parser.parse_file(file_path)

        session = dal.get_default_session()
        # Create insert statements
        for price in prices:
            command = self.__parse_price_into_insert_command(price, currency_symbol)
            self.logger.debug(command)
            session.execute(command)
        # Save all to database
        session.commit()

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
