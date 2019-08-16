""" CSV parsing elements """
from decimal import Decimal
from datetime import datetime
from typing import List
import logging
from . import dal
from . import config
from .model import PriceModel
from .utils import read_lines_from_file

# class CsvPrice:
#     """ The price object parsed from a .csv file """
#     def __init__(self):
#         self.date: datetime = None
#         self.symbol: str = None
#         self.value: Decimal = None

#     def __repr__(self):
#         return f"<CsvPrice (date={self.date},symbol={self.symbol},value={self.value})>"

class CsvParser:
    """ Parse CSV file """
    def __init__(self):
        self.session = None
        self.symbol_maps = None

    def parse_file(self, file_path, currency) -> List[PriceModel]:
        """ Load and parse a .csv file """
        # load file
                # read csv into memory?
        contents = self.load_file(file_path)
        prices = []

        # parse price elements
        for line in contents:
            price = self.parse_line(line)
            assert isinstance(price, PriceModel)
            price.currency = currency
            prices.append(price)

        return prices

    def load_file(self, file_path) -> List[str]:
        """ Loads the content of the text file """
        content = []
        content = read_lines_from_file(file_path)
        return content

    def parse_line(self, line: str) -> PriceModel:
        """ Parse a CSV line into a price element """
        line = line.rstrip()
        parts = line.split(',')

        result = PriceModel()

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
        result.datetime = datetime(int(year_str), int(month_str), int(day_str))

        return result

    def __get_session(self):
        """ Reuses the same db session """
        if not self.session:
            self.session = dal.get_default_session()
        return self.session
