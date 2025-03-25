"""
Fixer.io currency rates
Currently only implements the free public API access with yesterday's rates.
"""
import os
import tempfile
import logging
from decimal import Decimal
from pydatum import Datum

try:
    import simplejson as json
except ImportError:
    import json
from pricedb import SecuritySymbol
from pricedb.config import Config, ConfigKeys


class Quote:
    """Class to represent a quote (price, ...)"""

    def __init__(self):
        self.datum: Datum = Datum()
        #self.namespace: str = None
        self.symbol: SecuritySymbol = None
        self.value: Decimal = Decimal(0)
        self.currency: str = None

    def __repr__(self):
        # symbol = ("{namespace}:{symbol}".format(namespace=self.namespace, symbol=self.symbol)
        #           if self.namespace else self.symbol)
        symbol = repr(self.symbol)
        symbol = "{symbol:<13}".format(symbol=symbol)

        value = "{value:>6}".format(value=self.value)
        return f"<Quote ('{symbol}',date:{self.datum},value:{value},currency:{self.currency})>"


class FixerioQuote(Quote):
    """ Fixer.io-specific quote """
    pass


class Fixerio:
    """Retrieves prices from data files or online provider(s)"""

    def __init__(self):
        self.cache_path = tempfile.gettempdir()
        self.logger = logging.getLogger(__name__)

        # read fixer.io api key
        cfg = Config()
        self.api_key = cfg.get(ConfigKeys.fixerio_api_key)

    def download(self, symbol: SecuritySymbol, currency: str) -> FixerioQuote:
        """ Download latest rates. Caches into temp directory. """
        if symbol.namespace:
            symbol.namespace = symbol.namespace.upper()
            # assert namespace == "CURRENCY"
        # namespace is ignored, anyways.
        currency = currency.upper()
        symbol.mnemonic = symbol.mnemonic.upper()
        # make sure the symbol does not contain namespace
        if ":" in symbol.mnemonic:
            raise ValueError("Currency symbol should not contain namespace.")

        rates_dict = None
        if self.latest_rates_exist():
            self.logger.debug("Cached rates found.")
            rates_dict = self.__read_rates_from_file()
        else:
            rates_dict = self.__download_rates(currency)

        mapper = FixerioModelMapper(rates_dict)
        model = mapper.get_model_for_symbol(symbol.mnemonic)
        self.logger.debug(f"current model: {model}")
        return model

    def __download_rates(self, base_currency: str):
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
        base_url = 'http://data.fixer.io/api/latest'
        query = f"{base_url}?base={base_currency}&access_key={self.api_key}"

        # if symbols:
        #     symbols_csv = ",".join(symbols)
        # if symbols_csv:
        #     query += f"&symbols={symbols_csv}"

        try:
            self.logger.debug(f"retrieving rates from {query}")
            response = requests.get(query)
            # print("[%s] %s" % (response.status_code, response.url))
            if response.status_code != 200:
                result = 'N/A'
            else:
                result = response.json()
                # rate_in_currency = rates["rates"][rate_in]
        except requests.ConnectionError as error:
            self.logger.error(error)

        self.logger.debug("Latest prices downloaded.")

        # Since these are daily rates, cache them into a file.
        # Ignored for now since we are downloading individual currencies, not all together.
        self.__save_rates(result)

        return result

    def get_yesterdays_file_path(self):
        """ Full path to the today's rates file. """
        datum = Datum()
        datum.yesterday()
        yesterday = datum.get_iso_date_string()

        return self.__get_rate_file_path(yesterday)

    def get_todays_file_path(self):
        """ path to today's cached file """
        datum = Datum()
        datum.today()
        today = datum.get_iso_date_string()

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
        return os.path.abspath("{cache_path}/fixerio_{filename}.json".format(
            cache_path=self.cache_path, filename=filename))

    def __read_rates_from_file(self):
        file_path = self.get_todays_file_path()

        with open(file_path, 'r') as file:
            content = file.read()

        # self.logger.debug(f"cached rates: {content}")
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
    """ Maps the result from Fixer.io into an array of FixerioQuote """

    def __init__(self, json_response):
        self.__data = json_response

    def get_model_for_symbol(self, symbol: str) -> FixerioQuote:
        """ Read and map a single currency rate """
        date_str = self.__data["date"]
        # rate_date = datetime.strptime(date_str, "%Y-%m-%d")
        # assert isinstance(rate_date, datetime)

        base = self.__data["base"]
        rates_dict = self.__data["rates"]
        value_str = rates_dict[symbol]
        value = Decimal(value_str)
        # The rate is inverse value.
        rate = Decimal(1) / value
        # Round to 6 decimals max.
        rounded_str = "{0:.6f}".format(rate)
        rounded = Decimal(rounded_str)

        model = Quote()
        model.symbol = SecuritySymbol("CURRENCY", symbol)
        model.value = rounded
        model.datum.from_iso_date_string(date_str)
        model.currency = base

        return model
