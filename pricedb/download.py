"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""
import urllib.request
import urllib.parse

from . import utils
from .model import PriceModel


class PriceDownloader:
    """ Proxy class for downloading prices """
    def __init__(self):
        pass
    
    def download(self, symbol: str):
        """ Download single latest price """
        # TODO check which downloader to use by loading the symbol record from the db.
        namespace, mnemonic = utils.split_symbol(symbol)
        
        actor = MorningstarDownloader()
        price = actor.download(namespace, mnemonic)
        return price


class MorningstarDownloader:
    """ Fetches prices from Morningstar site """
    def __init__(self):
        self.url = "http://quotes.morningstar.com/stockq/c-header"
        self.params = {'t': 'symbol'}

    def download(self, namespace: str, symbol: str) -> PriceModel:
        """ Download the given symbol """
        self.params["t"] = symbol
        # assemble url
        params = urllib.parse.urlencode(self.params)
        url = self.url + '?' + params
        with urllib.request.urlopen(url) as response:
            html = response.read()
        print(url, html)
