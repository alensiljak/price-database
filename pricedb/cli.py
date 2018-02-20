"""
CLI entry point
"""
import logging
import click
import click_log
from pricedb.app import PriceDbApplication
from .map_cli import symbol_map

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


######
cli.add_command(import_csv)
cli.add_command(symbol_map)

##################################################
# Debug run
# if __name__ == "__main__":
#     import_csv(["file", "data/AUD.csv"])
