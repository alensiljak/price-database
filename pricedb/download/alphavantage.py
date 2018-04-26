"""
Alphavantage downloader
"""
import logging
from datetime import datetime
from decimal import Decimal

from pricedb.config import Config, ConfigKeys
from pricedb.model import PriceModel, SecuritySymbol


class AlphaVantageDownloader:
    """ Uses AlphaVantage to get prices """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Provide the api key value.
        self.api_key = None

    def download(self, symbol: SecuritySymbol, currency: str):
        """ Download price """
        from alpha_vantage.timeseries import TimeSeries

        cfg = Config()
        self.api_key = cfg.get(ConfigKeys.alphavantage_api_key)
        ts = TimeSeries(key=self.api_key)

        # pylint: disable=E0632
        # data, meta_data = ts.get_daily(symbol)
        data, meta_data = ts.get_intraday(symbol.mnemonic)
        # pylint: enable=E0632

        # pylint: disable=no-member
        keys = list(data.keys())
        # pylint: enable=no-member
        latest_key = keys[0]
        latest_price = data[latest_key]
        value = latest_price["4. close"].strip("0")

        # Parse
        result = PriceModel()
        result.symbol = symbol
        result.datetime = datetime.strptime(latest_key, "%Y-%m-%d %H:%M:%S")
        result.value = Decimal(value)
        result.currency = currency

        self.logger.debug(f"{latest_key}, {result}")
        return result
