"""
CLI entry point
"""
import click

@click.group()
def cli():
    """ entry point """
    pass

@click.command("import")
def import_csv():
    """ Import prices from CSV file """
    pass

cli.add_command(import_csv)

