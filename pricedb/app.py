""" main api point """
import logging
#from logging import log, DEBUG

class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
        assert isinstance(file_path, str)
        assert isinstance(currency_symbol, str)

        self.logger.debug(f"Importing {file_path}")

        # read csv into memory?
        contents = self.__load_csv_file(file_path)
        # iterate line by line
        for line in contents:
            self.logger.debug(f"parsing: {line}")
        # Create insert statements
        # Execute.   

    def __load_csv_file(self, file_path):
        """ Loads the content of the text file """
        content = []
        with open(file_path) as csv_file:
            content = csv_file.readlines()
        return content
