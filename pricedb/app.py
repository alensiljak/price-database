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
            command = self.__parse_price_into_insert_command(price)
            session.execute(command)
        #session.commit()

    def __parse_price_into_insert_command(self, price: CsvPrice) -> str:
        """ Parses a CSV line into an INSERT command """
        date_iso = f"{price.date.year}-{price.date.month}-{price.date.day}" 
        # CSV prices are with 2 decimals right now
        store_value = price.value * 100
        store_denom = 100

        header = "symbol,date,value,denom"

        command = f"insert into price ({header}) values ('{price.symbol}','{date_iso}',{store_value},{store_denom});"
        self.logger.debug(command)
