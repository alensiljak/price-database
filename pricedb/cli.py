"""
CLI entry point
"""
import logging
from datetime import datetime
from decimal import Decimal

import click
import click_log

from .app import PriceDbApplication
from .map_cli import symbol_map
from .model import PriceModel, SecuritySymbol

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    """ entry point """
    pass


@click.command()
@click.option("--symbol", prompt="Security symbol with exchange (EXCH:SYMBOL)", type=str)
@click.option("--date", prompt="Date in ISO format (yyyy-mm-dd)")
@click.option("--value", prompt="Price")
@click.option("--currency", prompt=True, type=str)
def add(symbol: str, date, value, currency: str):
    """ Add individual price """
    symbol = symbol.upper()
    currency = currency.upper()

    app = PriceDbApplication()
    price = PriceModel()

    # security = SecuritySymbol("", "")
    price.symbol.parse(symbol)
    # price.symbol.mnemonic = price.symbol.mnemonic.upper()

    # date_str = f"{date}"
    # date_format = "%Y-%m-%d"
    # if time:
    #     date_str = f"{date_str}T{time}"
    #     date_format += "T%H:%M:%S"
    # datum.from_iso_date_string(date)
    # price.datetime = datetime.strptime(date_str, date_format)
    price.datum.from_iso_date_string(date)

    price.value = Decimal(value)
    price.currency = currency
    app.add_price(price)
    app.save()

    click.echo("Price added.")


@click.command("import")
@click.argument("file", "FILE - path to the .csv file to import")
@click.argument("currency", "currency - to use for imported prices")
@click_log.simple_verbosity_option(logger)
def import_csv(file, currency: str):
    """ Import prices from CSV file """
    logger.debug(f"currency = {currency}")
    # auto-convert to uppercase.
    currency = currency.upper()

    app = PriceDbApplication()
    app.logger = logger
    app.import_prices(file, currency)


@click.command()
@click.argument("symbol")
def last(symbol: str):
    """ displays last price for symbol """
    # convert to uppercase
    symbol = symbol.upper()
    # extract namespace
    sec_symbol = SecuritySymbol("", "")
    sec_symbol.parse(symbol)

    app = PriceDbApplication()
    latest = app.get_latest_price(sec_symbol)
    assert isinstance(latest, PriceModel)
    print(f"{latest}")


@click.command("list")
@click.option("--date", help="The date for which to show prices.")
@click.option("--currency", help="The currency for which to show prices.")
@click.option("--last", is_flag=True, help="Display only the latest prices per symbol")
@click_log.simple_verbosity_option(logger)
def list_prices(date, currency, last):
    """ Display all prices """
    app = PriceDbApplication()
    app.logger = logger

    if last:
        # fetch only the last prices
        prices = app.get_latest_prices()
    else:
        prices = app.get_prices(date, currency)
    for price in prices:
        print(price)

    print(f"{len(prices)} records found.")


@click.command("dl")
@click.option("--namespace", "-n", default=None, help="Namespace for the securities to update")
@click.option("--symbol", "-s", default=None, help="Symbol for the individual price to download")
@click.option("--file", "-f", default=None, help="The text file containing the symbols to download")
@click.option("--agent", "-a", default=None, help="Agent to use for download (vanguard_au, morningstar, alphavantage)")
@click.option("--currency", "-c", default=None, help="Currency symbol to use for the price(s)")
@click_log.simple_verbosity_option(logger)
def download(symbol: str, file: str, agent: str, currency: str):
    """ Download the latest prices """
    app = PriceDbApplication()
    app.logger = logger
    
    if currency:
        currency = currency.strip()
    
    # if symbol:
    #     # download individual price
    #     app.download_price(symbol, currency, agent)
    #     return

    if file:
        # Download prices from the file. One symbol per line.
        app.download_prices_from_file(file, currency, agent)
        return
    
    # Otherwise download the prices for securities listed in the database.
    if file is None:
        app.download_prices_in_db()

    #print("Please use --symbol or --file option. --help for more info. Symbol will have preference over file.")


@click.command("prune")
@click.option("--all", "-a", is_flag=True, help="Delete historical prices for all symbols")
@click.option("--symbol", "-s", help="Symbol for which to delete prices")
@click_log.simple_verbosity_option(logger)
def prune(symbol: str, all):
    """ Delete old prices, leaving just the last. """
    app = PriceDbApplication()
    app.logger = logger

    if symbol is not None:
        sec_symbol = SecuritySymbol("", "")
        sec_symbol.parse(symbol)

        app.prune(sec_symbol)
    else:
        app.prune_all()


######
cli.add_command(add)
cli.add_command(download)
cli.add_command(import_csv)
cli.add_command(symbol_map)
cli.add_command(last)
cli.add_command(list_prices)
cli.add_command(prune)

##################################################
# Debug run
# if __name__ == "__main__":
#     import_csv(["file", "data/AUD.csv"])
