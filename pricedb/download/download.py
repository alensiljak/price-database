"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""
import logging
from enum import Enum, auto

# from html.parser import HTMLParser
# from lxml import html
from bs4 import BeautifulSoup

from pricedb import utils
from pricedb.mappers import PriceMapper
from pricedb.model import PriceModel
from pricedb.repositories import PriceRepository

from .alphavantage import AlphaVantageDownloader
from .morningstar import MorningstarDownloader
from .vanguard_au import VanguardAuDownloader

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

        symbol = symbol.upper()
        currency = currency.upper()
        agent = agent.lower()

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
