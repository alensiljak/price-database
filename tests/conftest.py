""" Test configuration """
import pytest
from pricedb import config, dal
from pkg_resources import Requirement, resource_filename

@pytest.fixture(scope="session")
def db_path():
    """ Path to the test database """
    filename = config.price_db_path()
    return filename

@pytest.fixture(scope="session")
def csv_path():
    """ Path to a test CSV file for price import """
    filename = filename = resource_filename(Requirement.parse("Price-Database"), "data/AUD_2017-11-11_142445.csv")
    return filename

@pytest.fixture(scope="session")
def session():
    """ Test db session """
    my_db = db_path()
    session = dal.get_session(my_db)

    return session


# class TestSettings(object):
#     """
#     """
#     def __init__(self):
#         self.__config = config()

#     @pytest.fixture(autouse=True, scope="session")
#     def config(self):
#         """ Real configuration """
#         print("config???")
#         return self.__config
