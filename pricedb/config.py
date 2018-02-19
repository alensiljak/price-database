""" Configuration """
from pkg_resources import Requirement, resource_filename

def price_db_path():
    """ Returns the default location for price database """
    filename = resource_filename(Requirement.parse("Price-Database"), "data/prices.db")
    return filename
