""" Test data layer """
from pricedb.dal import Price

def test_instantiation():
    """ Create instance of Price entity """
    entity = Price()
    desc = str(entity)

    assert entity is not None
    assert desc
