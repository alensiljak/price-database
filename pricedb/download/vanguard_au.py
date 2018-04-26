"""
The script downloads fund prices from Vanguard Australia site.
Retail Funds
Vanguard Diversified Bond Index Fund                  VAN0101AU   8123 = VANGUARD:BOND
Vanguard International Shares Index Fund (Hedged)     VAN0107AU   8146 = VANGUARD:HINT
Vanguard Australian Property Securities Index Fund    VAN0012AU   8147 = VANGUARD:PROP
Vanguard Australian Shares High Yield Fund            VAN0017AU   8148 = VANGUARD:HY
"""
import logging
from datetime import datetime
from decimal import Decimal

import requests

from pricedb.model import PriceModel, SecuritySymbol

try:
    import simplejson as json
except ImportError:
    import json


class FundInfo:
    """ Vg fund info. A DTO. """

    def __init__(self):
        self.name: str = None
        self.identifier = None
        self.date = None
        self.value: str = None
        self.mstar_id = None
        self.currency = None

    def __repr__(self):
        return f"<FundInfo (name='{self.name}',id='{self.identifier}',value={self.value})>"


class VanguardAuDownloader:
    """
    Downloads prices from Vanguard Australia
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # cached HTML
        self.__data = None
        self.fund_map = {
            "VANGUARD:BOND": "8123",
            "VANGUARD:HINT": "8146",
            "VANGUARD:PROP": "8147",
            "VANGUARD:HY": "8148"
        }

    def download(self, namespace: str, mnemonic: str, currency: str):
        """ Download price """
        if namespace != "Vanguard".upper():
            raise ValueError(f"Only Vanguard namespace is handled by this agent. Requested {namespace}:{mnemonic}!")

        fund_data = self.__load_fund_data()

        symbol = f"{namespace}:{mnemonic}"
        fund_id = self.fund_map[symbol]
        fund_info = self.__get_fund_price(fund_data, fund_id)
        # self.logger.debug(f"{price}")

        result = PriceModel()

        date_format = "%d %b %Y"
        result.datetime = datetime.strptime(fund_info.date, date_format)

        result.symbol = SecuritySymbol("VANGUARD", mnemonic)

        value = fund_info.value.strip("$")
        result.value = Decimal(value)

        result.currency = "AUD"
        return result

    def get_fund_info(self, fund_symbol: str):
        """ For compatibility. Returns the full fund info """
        self.__load_fund_data()
        fund_id = self.fund_map[fund_symbol]
        if not fund_id:
            raise ValueError(f"Fund not found in map {fund_symbol}")

        return self.__get_fund_price(self.__data, fund_id)

    def __load_fund_data(self):
        """
        Fetches retail fund prices.
        """
        if self.__data:
            return self.__data

        # url = "https://www.vanguardinvestments.com.au/retail/ret/investments/product.html"
        # url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPrice?portId=" + fund_id
        # pylint: disable=C0301
        # url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPriceList.jsonp"
        # url = "https://intlgra-globm-209.gra.international.vgdynamic.info/rs/gre/gra/datasets/auw-retail-listview-data.jsonp"
        url = "https://intlgra-graapp-72-prd.gra.international.vgdynamic.info/rs/gre/gra/datasets/auw-retail-listview-data.jsonp"
        response = requests.get(url)
        if response.status_code != 200:
            return "Error"

        content = response.content
        content = str(content, 'utf-8')

        # clean-up the response
        if content.startswith("callback("):
            length = len(content) - 1
            content = content[9:length]

        # cache the downloaded page? The prices are daily.

        content_json = json.loads(content)

        self.__data = content_json["fundData"]
        return self.__data

    def __get_fund_price(self, fund_data, fund_id: str):
        """
        Extracts the price value from json response.
        Returns the Price object with name, identifier, date, value, mstar_id.
        """
        info_json = fund_data[fund_id]
        fund_info = FundInfo()

        fund_info.name = info_json["name"]
        fund_info.identifier = info_json["identifier"]
        fund_info.date = info_json["asOfDate"]
        # Using NAV price for the value.
        fund_info.value = info_json["navPrice"]
        fund_info.mstar_id = info_json["mStarID"]
        # Currency?
        # fund_info.currency = info_json["currency"]["currencyCode"]

        return fund_info
