"""
CLI entry point
"""
import logging
from decimal import Decimal

import click
import click_log

from pricedb import PriceDbApplication
# from pricedb.map_cli import symbol_map
from pricedb.model import PriceModel, SecuritySymbol

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    """ entry point """
    pass

@click.command()
@click_log.simple_verbosity_option(logger)
def config():
    ''' Display the configuration values '''
    app = PriceDbApplication()
    #app.

@click.command()
@click.option("--symbol", prompt="Security symbol with exchange (EXCH:SYMBOL)", type=str)
@click.option("--date", prompt="Date in ISO format (yyyy-mm-dd)")
@click.option("--value", prompt="Price")
@click.option("--currency", prompt=True, type=str)
@click_log.simple_verbosity_option(logger)
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


@click.command()
#@click.option("--format", help="The export format. The default is ledger.", default="ledger")
@click_log.simple_verbosity_option(logger)
def export():
    """ Export prices in ledger format """
    app = PriceDbApplication()
    result = app.ledger_export()
    print(result)


@click.command("import")
@click.argument("filepath") # "FILE - path to the .csv file to import"
@click.argument("currency") # "currency - to use for imported prices"
@click_log.simple_verbosity_option(logger)
def import_csv(filepath: str, currency: str):
    """ Import prices from CSV file """
    logger.debug(f"currency = {currency}")
    # auto-convert to uppercase.
    currency = currency.upper()

    app = PriceDbApplication()
    app.logger = logger
    app.import_prices(filepath, currency)


@click.command()
@click.option("symbol", "-s")
@click_log.simple_verbosity_option(logger)
def last(symbol: str):
    """ displays last price, for symbol if provided """
    app = PriceDbApplication()

    # convert to uppercase
    if symbol:
        symbol = symbol.upper()
        # extract namespace
        sec_symbol = SecuritySymbol("", "")
        sec_symbol.parse(symbol)

        latest = app.get_latest_price(sec_symbol)
        assert isinstance(latest, PriceModel)
        print(f"{latest}")
    else:
        # Show the latest prices available for all securities.
        latest = app.get_latest_prices()
        for price in latest:
            print(f"{price}")


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
@click.option("--agent", "-a", default=None,
              help="Agent to use for download (vanguard_au, morningstar, alphavantage)")
@click.option("--currency", "-c", default=None, help="Currency symbol to use for the price(s)")
@click.option("--help", "-h", is_flag=True)
@click_log.simple_verbosity_option(logger)
@click.pass_context
def download(ctx, help: bool, symbol: str, namespace: str, agent: str, currency: str):
    """ Download the latest prices """
    if help:
        click.echo(ctx.get_help())
        ctx.exit()

    app = PriceDbApplication()
    app.logger = logger

    if currency:
        currency = currency.strip()
        currency = currency.upper()

    # Otherwise download the prices for securities listed in the database.
    app.download_prices(currency=currency, agent=agent, symbol=symbol, namespace=namespace)


@click.command("prune")
@click.option("--all", "-a", is_flag=True, help="Delete historical prices for all symbols")
@click.option("--symbol", "-s", help="Symbol for which to delete prices")
@click_log.simple_verbosity_option(logger)
def prune(symbol: str, all: str):
    """ Delete old prices, leaving just the last. """
    app = PriceDbApplication()
    app.logger = logger
    count = 0

    if symbol is not None:
        sec_symbol = SecuritySymbol("", "")
        sec_symbol.parse(symbol)

        deleted = app.prune(sec_symbol)
        if deleted:
            count = 1
    else:
        count = app.prune_all()

    print(f"Removed {count} old price entries.")


@click.command("securities")
@click_log.simple_verbosity_option(logger)
def securities():
    ''' export the list of securities for which the prices are tracked '''
    app = PriceDbApplication()
    result = app.get_security_list()
    print(result)


######
cli.add_command(add)
cli.add_command(export)
cli.add_command(download)
cli.add_command(import_csv)
# cli.add_command(symbol_map)
cli.add_command(last)
cli.add_command(list_prices)
cli.add_command(prune)
cli.add_command(securities)
