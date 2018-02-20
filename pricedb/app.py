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

        # self.logger.debug(f"parsing: {line}")
        # Create insert statements
        #command = self.__parse_csv_line_into_insert_command(line)
        # Execute.
        #app.session.execute(command)
        # session.commit()?

    # def __parse_csv_line_into_insert_command(self, csv_line: str) -> str:
    #     """ Parses a CSV line into an INSERT command """
    #     # TODO add columns
    #     header = ""
    #     command = f"insert into price ({header}) values ({csv_line});"
