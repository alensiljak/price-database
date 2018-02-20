""" Repositories - operations on multiple entities/aggregates """
from typing import List
from .dal import SymbolMap


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
