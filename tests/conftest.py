""" Test configuration """
import pytest
from pkg_resources import Requirement, resource_filename
from pricedb import dal
# from pricedb.config import Config, ConfigKeys


@pytest.fixture(scope="session")
def db_path():
    """ Path to the test database """
    # cfg = Config()
    # filename = cfg.get(ConfigKeys.price_database)
    filename = filename = resource_filename(Requirement.parse("PriceDb"), "data/prices-template.db")
    return filename


@pytest.fixture(scope="session")
def csv_path():
    """ Path to a test CSV file for price import """
    filename = filename = resource_filename(
        Requirement.parse("PriceDb"), "data/AUD_2017-11-11_142445.csv")
    return filename


@pytest.fixture(scope="session")
def db_session():
    """ Test db session """
    my_db = db_path()
    result = dal.get_session(my_db)

    return result

@pytest.fixture(scope="session")
def session():
    """ The in-memory session """
    my_db = ":memory:"
    result = dal.get_session(my_db)
    return result
