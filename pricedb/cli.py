"""
CLI entry point
"""
import logging
import click
import click_log
from pricedb.app import PriceDbApplication
from .map_cli import symbol_map
from .model import Price

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    """ entry point """
    pass

@click.command("import")
@click.argument("file", "FILE - path to the .csv file to import")
@click.argument("currency", "currency - to use for imported prices")
@click_log.simple_verbosity_option(logger)
def import_csv(file, currency):
    """ Import prices from CSV file """
    logger.debug(f"currency = {currency}")

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
    parts = symbol.split(":")
    namespace = None
    if len(parts) > 1:
        namespace = parts[0]
        symbol = parts[1]
    
    app = PriceDbApplication()
    latest = app.get_latest_price(namespace, symbol)
    assert isinstance(latest, Price)
    print(f"{latest}")


######
cli.add_command(import_csv)
cli.add_command(symbol_map)
cli.add_command(last)

##################################################
# Debug run
# if __name__ == "__main__":
#     import_csv(["file", "data/AUD.csv"])
