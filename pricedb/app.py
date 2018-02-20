""" main api point """
import logging
#from logging import log, DEBUG
from .csv import CsvParser, CsvPrice


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

        # Create insert statements
        for price in prices:
            command = self.__parse_price_into_insert_command(price)
        # Execute.
        #app.session.execute(command)
        # session.commit()?

    def __parse_price_into_insert_command(self, price: CsvPrice) -> str:
        """ Parses a CSV line into an INSERT command """
        date_iso = f"{price.date.year}-{price.date.month}-{price.date.day}" 
        header = "symbol,date,value,denom"
        command = f"insert into price ({header}) values ('{price.symbol}','{date_iso}',100);"
        self.logger.debug(command)
