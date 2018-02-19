""" Test configuration """
import pytest
from pkg_resources import Requirement, resource_filename

@pytest.fixture(scope="session")
def db_path():
    """ Path to the test database """
    filename = resource_filename(Requirement.parse("Price-Database"), "data/prices.db")
    return filename

# @pytest.fixture(scope="session")
# def config():
#     """ Test configuration """
#     return Config("data/asset_allocation.ini")


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
