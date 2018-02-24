"""
Price downloaders and parsers.
These can be used as the first aid, to populate the price database but are not
a comprehensive solution.
"""

class PriceDownloader:
    """ Proxy class for downloading prices """
    def __init__(self):
        pass
    
    def download(self, symbol: str):
        """ Download single latest price """
        # TODO check which downloader to use by loading the symbol record from the db.
        
        actor = MorningstarDownloader()
        actor.download()


class MorningstarDownloader:
    """ Fetches prices from Morningstar site """
    def __init__(self):
        pass

    def download(namespace: str, symbol: str):
        """ Download the given symbol """
        pass
