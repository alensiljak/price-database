""" Test data layer """
from pricedb.dal import Price, get_session

def test_instantiation():
    """ Create instance of Price entity """
    entity = Price()
    desc = str(entity)

    assert entity is not None
    assert desc

def test_data_path(db_path):
    """ Check the test database path """
    assert db_path

def test_session(db_path):
    """ Open database """
    # TODO 
    session = get_session(db_path)
    prices = session.query(Price).all()

    # the table is empty but no errors while reading.
    assert not prices
