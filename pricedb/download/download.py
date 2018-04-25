"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""
import logging
from enum import Enum, auto

from pricedb import utils

from .alphavantage import AlphaVantageDownloader
from .morningstar import MorningstarDownloader
from .vanguard_au import VanguardAuDownloader
from .fixerio import Fixerio


class DownloadAgents(Enum):
    """ Available agents for price download """
    alphavantage = auto(),
    fixerio = auto(),
    morningstar = auto(),
    vanguard_au = auto()


class PriceDownloader:
    """ Proxy class for downloading prices """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download(self, symbol: str, currency: str = None, agent: str = None):
        """ Download single latest price """
        assert agent is not None
        assert isinstance(agent, str)

        symbol = symbol.upper()
        currency = currency.upper()
        agent = agent.lower()
        actor = None

        namespace, mnemonic = utils.split_symbol(symbol)

        if agent == DownloadAgents.morningstar.name:
            actor = MorningstarDownloader()
        elif agent == DownloadAgents.vanguard_au.name:
            actor = VanguardAuDownloader()
        elif agent == DownloadAgents.alphavantage.name:
            actor = AlphaVantageDownloader()
        elif agent == DownloadAgents.fixerio.name:
            # import finance_quote
            # app = finance_quote.App()
            # price = app.fixerio(currency, symbol)
            actor = Fixerio()
        else:
            raise ValueError("No agent specified for price download.")

        if actor:
            actor.logger = self.logger
            price = actor.download(namespace, mnemonic, currency)

        return price
