""" Repositories - operations on multiple entities/aggregates """
from .dal import SymbolMap


class SymbolMapRepository:
    """ Operations on SymbolMap collections """
    def __init__(self, session):
        self.session = session
    
    def get_by_id(self, symbol: str) -> SymbolMap:
        """ Finds the map by in-symbol """
        return self.query.filter(SymbolMap.in_symbol == symbol).first()

    @property
    def query(self):
        """ Basic query """
        return self.session.query(SymbolMap)
