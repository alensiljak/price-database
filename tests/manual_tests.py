"""
Manual / debugging tests.
"""
from pricedb import PriceDbApplication

def download_bnd():
    app = PriceDbApplication()
    #price = app.download_price("NYSEARCA:VTI", "USD", "morningstar")
    price = app.download_price("NYSEARCA:BND", "USD", "morningstar")
    assert price

if __name__ == "__main__":
    download_bnd()
