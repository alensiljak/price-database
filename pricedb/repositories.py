""" Repositories - operations on multiple entities/aggregates """
# from typing import List
from .dal import Price, get_default_session, Security

DB_NAME = 'price-database.json'

class PriceRepository:
    """ Operations on prices """
    def __init__(self, session=None):
        self.__session = session

    def add(self, entity: Price):
        """ Insert price """
        self.session.add(entity)

    def save(self):
        """ Save all changes in the session """
        self.session.commit()

    @property
    def session(self):
        """ db session """
        if not self.__session:
            self.__session = get_default_session()
        return self.__session

    @property
    def query(self):
        """ Base query """
        return self.session.query(Price)


class SecurityRepository:
    """ Security table """
    def __init__(self, session=None):
        self.__session = session

    @property
    def session(self):
        """ db session """
        if not self.__session:
            self.__session = get_default_session()
        return self.__session

    @property
    def query(self):
        """ Base query """
        return self.session.query(Security)


class SecurityRepositoryTiny:
    """
    Securities.
    Implemented with tinydb. Uses the current folder for the database.
    Fields: id, symbol, namespace, updater, currency.
    """
    def __init__(self):
        from tinydb import TinyDB

        self.db_path = f'./{DB_NAME}'
        self.db = TinyDB(self.db_path)
        self.table = self.db.table('security')

    def all_securities(self):
        ''' Returns all records '''
        #from tinydb import Query
        #Sec = Query()
        result = self.table.all()
        return result
