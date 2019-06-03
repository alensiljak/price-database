""" Repositories - operations on multiple entities/aggregates """
# from typing import List
from .dal import Price, get_default_session, Security


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
