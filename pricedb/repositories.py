""" Repositories - operations on multiple entities/aggregates """
from typing import List
from .dal import SymbolMap, Price, get_default_session, Security


class SymbolMapRepository:
    """ Operations on SymbolMap collections """
    def __init__(self, session):
        self.session = session

    def get_by_id(self, symbol: str) -> SymbolMap:
        """ Finds the map by in-symbol """
        return self.query.filter(SymbolMap.in_symbol == symbol).first()

    def get_all(self) -> List[SymbolMap]:
        """ Returns all maps """
        return self.query.all()

    @property
    def query(self):
        """ Basic query """
        return self.session.query(SymbolMap)


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
