"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""
from decimal import Decimal, InvalidOperation
import urllib.request
import urllib.parse
from datetime import datetime
# from html.parser import HTMLParser
# from lxml import html
from bs4 import BeautifulSoup
import logging

from . import utils
from .model import PriceModel
from .repositories import PriceRepository
from .mappers import PriceMapper


class PriceDownloader:
    """ Proxy class for downloading prices """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def download(self, symbol: str):
        """ Download single latest price """
        # TODO check which downloader to use by loading the symbol record from the db.
        # Or check the namespace.

        namespace, mnemonic = utils.split_symbol(symbol)

        actor = MorningstarDownloader()
        actor.logger = self.logger
        
        price = actor.download(namespace, mnemonic)

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

    def download(self, namespace: str, symbol: str) -> PriceModel:
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
