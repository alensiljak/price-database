'''
Test showing the securities
'''
from pricedb.app import PriceDbApplication

def test_securities():
    app = PriceDbApplication()
    sec_list = app.get_security_list()

    assert sec_list is not None
