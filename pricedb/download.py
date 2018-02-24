"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""
import logging
import urllib.parse
import urllib.request
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum, auto

from alpha_vantage.timeseries import TimeSeries
# from html.parser import HTMLParser
# from lxml import html
from bs4 import BeautifulSoup

from . import utils
from .config import Config, ConfigKeys
from .mappers import PriceMapper
from .model import PriceModel
from .repositories import PriceRepository

try: import simplejson as json
except ImportError: import json


class DownloadAgents(Enum):
    """ Available agents for price download """
    morningstar = auto(),
    vanguard_au = auto(),
    alphavantage = auto()


class PriceDownloader:
    """ Proxy class for downloading prices """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download(self, symbol: str, currency: str, agent: str):
        """ Download single latest price """
        # TODO check which downloader to use by loading the symbol record from the db.
        # Or check the namespace.

        namespace, mnemonic = utils.split_symbol(symbol)

        if agent == DownloadAgents.morningstar.name:
            actor = MorningstarDownloader()
        elif agent == DownloadAgents.vanguard_au.name:
            actor = VanguardAuDownloader()
        elif agent == DownloadAgents.alphavantage.name:
            actor = AlphaVantageDownloader()
        else:
            raise ValueError("No agent specified for price download.")

        actor.logger = self.logger
        price = actor.download(namespace, mnemonic, currency)

        return price


class MorningstarDownloader:
    """ Fetches prices from Morningstar site """
    def __init__(self):
        self.url = "http://quotes.morningstar.com/stockq/c-header"
        self.params = {'t': 'symbol'}
        self.namespaces = {
            "AMS": "XAMS",
            "ASX": "XASX",
            "XETRA": "XETR",
            "LSE": "XLON",
            "NASDAQ": "XNAS",
            "NYSE": "XNYS",
            "NYSEARCA": "ARCX"
        }
        self.logger = logging.getLogger(__name__)

    def download(self, namespace: str, symbol: str, currency: str) -> PriceModel:
        """ Download the given symbol """
        if not namespace:
            raise ValueError(f"Namespace not sent for {symbol}")

        # get the translated namespace
        local_namespace = self.namespaces[namespace]
        self.params["t"] = f"{local_namespace}:{symbol}"
        # assemble url
        params = urllib.parse.urlencode(self.params)
        url = self.url + '?' + params
        self.logger.debug(f"fetching price from {url}")

        with urllib.request.urlopen(url) as response:
            html = response.read()

        if not html:
            return None

        # parse HTML
        price = self.parse_price(html)
        if price:
            price.namespace = namespace
            price.symbol = symbol
        # compare currency
        if price.currency != currency:
            raise ValueError(f"Currency does not match for {symbol}! {currency}")

        return price

    def parse_price(self, page: str) -> PriceModel:
        """ parse html to get the price """
        result = PriceModel()
        soup = BeautifulSoup(page, 'html.parser')

        # Price value
        price_el = soup.find(id='last-price-value')
        if not price_el:
            logging.debug(f"Received from mstar: {page}")
            raise ValueError("No price info found in returned HTML.")

        value = price_el.get_text().strip()
        try:
            result.value = Decimal(value)
        except InvalidOperation:
            message = f"Could not parse {value}"
            print(message)
            self.logger.error(message)
            return None

        # The rest
        date_str = soup.find(id="asOfDate").get_text().strip()
        date_val = datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
        result.datetime = date_val

        # tz_str = soup.find(id="timezone").get_text().strip()

        currency = soup.find(id="curency").get_text().strip()
        result.currency = currency

        return result


class AlphaVantageDownloader:
    """ Uses AlphaVantage to get prices """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download(self, namespace: str, symbol: str, currency: str):
        """ Download price """
        cfg = Config()
        api_key = cfg.get(ConfigKeys.alphavantage_api_key)
        ts = TimeSeries(key=api_key)

        #pylint: disable=no-member
        # data, meta_data = ts.get_daily(symbol)
        data, meta_data = ts.get_intraday(symbol)
        # self.logger.debug(data)

        keys = list(data.keys())
        latest_key = keys[0]
        latest_price = data[latest_key]
        value = latest_price["4. close"].strip("0")

        # Parse
        result = PriceModel()
        result.namespace = namespace
        result.symbol = symbol
        result.datetime = datetime.strptime(latest_key, "%Y-%m-%d %H:%M:%S")
        result.value = Decimal(value)
        result.currency = currency

        self.logger.debug(f"{latest_key}, {result}")
        return result


class VanguardAuDownloader:
    """
    Downloads prices from Vanguard Australia
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download(self, namespace: str, symbol: str, currency: str):
        """ Download price """
        if namespace != "Vanguard":
            raise ValueError("Only Vanguard namespace is handled by this agent.")
