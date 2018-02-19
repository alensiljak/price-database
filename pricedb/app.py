""" main api point """
import logging
#from logging import log, DEBUG

class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def import_prices(self, file_path: str):
        """ Incomplete """
        assert isinstance(file_path, str)

        print(file_path)

        self.logger.debug(f"Importing {file_path}")
        # TODO read csv into memory?
        # iterate line by line
        # Create insert statements
        # Execute.   
