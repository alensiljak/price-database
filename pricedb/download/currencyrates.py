"""
Fetches the current exchange rates.
Currently uses Fixer API.
"""
import glob
import os
import tempfile
from datetime import datetime
from decimal import Decimal
from logging import ERROR, log
from typing import List

from pricedb.model import PriceModel

try: import simplejson as json
except ImportError: import json



class CurrencyRatesRetriever:
    """Retrieves prices from data files or online provider(s)"""
    def __init__(self):
        self.cache_path = tempfile.gettempdir()
        self.logger = None

    def download(self, namespace: str, mnemonic: str, currency: str) -> PriceModel:
        """ Download latest rates. Caches into temp directory. """
        assert namespace == "CURRENCY"

        rates_dict = None
        if self.latest_rates_exist():
            self.logger.debug(f"Cached rates found.")
            rates_dict = self.__read_rates_from_file()
        else:
            rates_dict = self.__download_rates(currency, mnemonic)

        mapper = FixerioModelMapper(rates_dict)
        model = mapper.get_model_for_symbol(mnemonic)
        self.logger.debug(model)
        return model

    def __download_rates(self, base_currency: str, symbols: List[str]):
        """
        Downloads the latest rates. Requires base currency and a list of currencies to
        retrieve.
        Returns json response object from Fixer.io.
        """
        import requests

        assert isinstance(base_currency, str)

        # Downloads the latest rates using Fixerio. Returns dict.
        # https://pypi.python.org/pypi/fixerio
        # from fixerio import Fixerio
        # fxrio = Fixerio(base=base_currency) #, symbols=symbols)
        # latest_rates = fxrio.latest()
        
        result = None
        base_url = 'http://api.fixer.io/latest'
        symbols_csv = ",".join(symbols)
        query = base_url + f"?base={base_currency}&symbols={symbols_csv}"
        try:
            response = requests.get(query)
            # print("[%s] %s" % (response.status_code, response.url))
            if response.status_code != 200:
                result = 'N/A'
            else:
                result = response.json()
                # rate_in_currency = rates["rates"][rate_in]
        except requests.ConnectionError as error:
            self.logger.error(error)

        self.logger.debug(f"Latest prices downloaded.")

        # Since these are daily rates, cache them into a file.
        # Ignored for now since we are downloading individual currencies, not all together.
        self.__save_rates(result)

        return result

    def get_yesterdays_file_path(self):
        """ Full path to the today's rates file. """
        from gnucash_portfolio.lib import generic

        yesterday = generic.get_date_iso_string(generic.get_yesterday())
        return self.__get_rate_file_path(yesterday)

    def get_todays_file_path(self):
        """ path to today's cached file """
        from gnucash_portfolio.lib import generic

        #today = generic.get_date_iso_string(generic.get_today())
        today = generic.get_today()
        return self.__get_rate_file_path(today)

    def latest_rates_exist(self):
        """ Check if latest rates cached file exists. """
        file_path = self.get_todays_file_path()
        exists = os.path.isfile(file_path)

        if exists:
            self.logger.debug(f"Cached file found at {file_path}")

        return exists

    def __get_rate_file_path(self, filename):
        """
        Assemble full file path for the given name (date).
        """
        return os.path.abspath(f"{self.cache_path}/{filename}.json")

    def __read_rates_from_file(self):
        file_path = self.get_todays_file_path()

        with open(file_path, 'r') as file:
            content = file.read()
            return json.loads(content)

    def __save_rates(self, rates):
        """
        Saves the retrieved rates into a cache file
        """
        file_date = rates["date"]
        filename = self.__get_rate_file_path(file_date)

        content = json.dumps(rates)

        with open(filename, 'w') as file:
            file.write(content)
            self.logger.debug(f"rates saved in {filename}.")


class FixerioModelMapper:
    """ Maps the result from Fixer.io into an array of PriceModels """
    def __init__(self, json_response):
        self.__data = json_response

    def get_model_for_symbol(self, symbol: str) -> PriceModel:
        """ Read and map a single currency rate """
        from gnucash_portfolio.lib import datetimeutils

        date_str = self.__data["date"]
        rate_date = datetimeutils.parse_iso_date(date_str)
        assert isinstance(rate_date, datetime)

        base = self.__data["base"]
        rates_dict = self.__data["rates"]
        value_str = rates_dict[symbol]
        value = Decimal(value_str)
        # The rate is inverse value.
        rate = Decimal(1) / value
        # Round to 6 decimals max.
        rounded_str = "{0:.6f}".format(rate)
        rounded = Decimal(rounded_str)

        model = PriceModel()
        model.namespace = "CURRENCY"
        model.symbol = symbol
        model.value = rounded
        model.datetime = rate_date
        model.currency = base

        return model
