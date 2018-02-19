"""
CLI entry point
"""
import logging
import click
import click_log
from pricedb.app import PriceDbApplication

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    """ entry point """
    pass

@click.command("import")
@click.argument("file") # , help="File to import"
@click_log.simple_verbosity_option(logger)
def import_csv(file):
    """ Import prices from CSV file """
    app = PriceDbApplication()
    app.logger = logger
    app.import_prices(file)

cli.add_command(import_csv)

##################################################
# Debug run
# if __name__ == "__main__":
#     import_csv(["file", "data/AUD.csv"])
