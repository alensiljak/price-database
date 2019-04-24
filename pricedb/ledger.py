"""
Ledger-related code.
Used for export of prices in ledger format.
"""
from typing import List
from pricedb.model import PriceModel


class LedgerFormatter:
    ''' Format a price for ledger price db '''

    def format_price(self, price: PriceModel):
        '''
        ledger price format, ISO format supported:
        P 2004-06-21 02:17:58 TWCUX $27.76
        '''
        date_time = price.datum.to_datetime_string()

        fmt = f"P {date_time} {price.symbol.mnemonic} {price.value} {price.currency}"
        return fmt

    def format_prices(self, prices: List[PriceModel]):
        ''' format a list of prices '''
        output = ""
        for price in prices:
            output += self.format_price(price) + "\n"
        return output
