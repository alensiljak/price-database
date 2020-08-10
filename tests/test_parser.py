'''
Test parsing the data.
Mostly the problematic cases are used here for debugging.
'''
from pricedb import PriceDbApplication

app = PriceDbApplication()

def test_wtes():
    result = app.download_price('WTES', 'XETRA', 'EUR', 'morningstar_de')
    assert result is not None
