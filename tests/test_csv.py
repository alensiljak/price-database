""" Test CSV parsing """
from datetime import datetime
from decimal import Decimal
from pricedb.csv import CsvPrice, CsvParser

def test_loading_file(csv_path):
    """ load csv file """
    parser = CsvParser()
    actual = parser.parse_file(csv_path)

    assert actual

def test_types(csv_path):
    """ Test correct parsing """
    parser = CsvParser()
    prices = parser.parse_file(csv_path)
    for price in prices:
        assert isinstance(price.date, datetime)
        assert isinstance(price.value, Decimal)
        assert isinstance(price.symbol, str)
