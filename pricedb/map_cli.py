""" CLI for manipulating symbol maps """
import click
from .config import Config, ConfigKeys
from .dal import get_session, SymbolMap

@click.group("map")
def symbol_map():
    """ Operations with symbol maps """
    pass

@click.command("add")
@click.argument("incoming") # , "in"
@click.argument("outgoing") # , "out"
def add_map(incoming, outgoing):
    """ Creates a symbol mapping """
    db_path = Config().get(ConfigKeys.pricedb_path)
    session = get_session(db_path)

    new_map = SymbolMap()
    new_map.in_symbol = incoming
    new_map.out_symbol = outgoing

    session.add(new_map)
    session.commit()
    click.echo("Record saved.")

@click.command("list")
def list_maps():
    """ Displays all symbol maps """
    db_path = Config().get(ConfigKeys.price_database)
    session = get_session(db_path)

    maps = session.query(SymbolMap).all()
    for item in maps:
        click.echo(item)

###
symbol_map.add_command(add_map)
symbol_map.add_command(list_maps)
