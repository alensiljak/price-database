""" CSV parsing elements """
from decimal import Decimal
from datetime import datetime
from typing import List
import logging
from .dal import get_session, Price
from . import config


class CsvPrice:
    """ The price object parsed from a .csv file """
    def __init__(self):
        self.date: datetime = None
        self.symbol: str = None
        self.value: Decimal = None

    def __repr__(self):
        return f"<CsvPrice (date={self.date},symbol={self.symbol},value={self.value})>"

class CsvParser:
    """ Parse CSV file """
    def __init__(self):
        pass

    def parse_file(self, file_path) -> List[CsvPrice]:
        """ Load and parse a .csv file """
        # load file
                # read csv into memory?
        contents = self.load_file(file_path)
        prices = []

        # parse price elements
        for line in contents:
            price = self.parse_line(line)
            assert isinstance(price, CsvPrice)
            prices.append(price)
        
        return prices

    def load_file(self, file_path) -> str:
        """ Loads the content of the text file """
        content = []
        with open(file_path) as csv_file:
            content = csv_file.readlines()
        return content

    def parse_line(self, line: str) -> CsvPrice:
        """ Parse a CSV line into a price element """
        line = line.rstrip()
        parts = line.split(',')
        #logging.debug(parts)
        
        result = CsvPrice()

        # symbol
        result.symbol = self.translate_symbol(parts[0])


        # value
        result.value = Decimal(parts[1])
        # date
        date_str = parts[2]
        date_str = date_str.replace('"', '')
        date_parts = date_str.split('/')

        year_str = date_parts[2]
        month_str = date_parts[1]
        day_str = date_parts[0]

        logging.debug(f"parsing {date_parts} into date")
        result.date = datetime(int(year_str), int(month_str), int(day_str))

        return result

    def translate_symbol(self, in_symbol: str) -> str:
        """ translate the incoming symbol into locally-used """
        # TODO read all mappings from the db
        db_path = config.price_db_path()
        session = get_session(db_path)
        #session.query(Price
        # TODO translate the incoming symbol
        
        return in_symbol