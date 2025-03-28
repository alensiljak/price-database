""" main api point """
import logging
from typing import List

from . import dal, mappers
from .model import PriceModel, SecuritySymbol


class PriceDbApplication:
    """ Contains the main public interfaces """

    def __init__(self, session=None):
        self.logger = logging.getLogger(__name__)
        self.price_repo = None
        self.security_repo = None
        self.__session = session

    def add_price(self, price: PriceModel):
        """ Creates a new price record """
        assert isinstance(price, PriceModel)

        if not price:
            raise ValueError("Cannot add price. The received model is null!")

        mapper = mappers.PriceMapper()
        entity = mapper.map_model(price)

        self.add_price_entity(entity)

    def add_price_entity(self, price: dal.Price):
        ''' Adds the price '''
        from decimal import Decimal

        # check if the price already exists in db.
        repo = self.get_price_repository()
        existing = (
            repo.query
            .filter(dal.Price.security_id == price.security_id)
            .filter(dal.Price.date == price.date)
            .filter(dal.Price.time == price.time)
            .first()
        )

        sec_repo = self.get_security_repo()
        security = sec_repo.get(price.security_id)
        #price.security = security
        # This inserts the price record!

        if existing:
            # Update existing price.
            new_value = Decimal(price.value) / Decimal(price.denom)
            self.logger.info(f"Exists: {security} {price}")
            if price.currency != existing.currency:
                raise ValueError(
                    f"The currency is different for price {security} {price}!")
            if existing.value != price.value:
                existing.value = price.value
                self.logger.info(f"Updating to {new_value}.")
            if existing.denom != price.denom:
                existing.denom = price.denom
        else:
            # Insert new price
            self.session.add(price)
            self.logger.info(f"Added {security} {price}")

    def download_prices(self, **kwargs):
        '''
        Downloads all the prices that are listed in the Security table.
        Accepts filter arguments: currency, agent, symbol, exchange.
        '''
        currency: str = kwargs.get('currency', None)
        if currency:
            currency = currency.upper()
        agent: str = kwargs.get('agent', None)
        if agent:
            agent = agent.upper()
        mnemonic: str = kwargs.get('symbol', None)
        if mnemonic:
            mnemonic = mnemonic.upper()
        exchange: str = kwargs.get('exchange', None)
        if exchange:
            exchange = exchange.upper()

        securities = self.__get_securities(currency, agent, mnemonic, exchange)

        if len(securities) == 0:
            print('No Securities found for the given parameters.')

        for sec in securities:
            # exchange = sec.namespace
            symbol = SecuritySymbol(sec.namespace, sec.symbol)
            currency = sec.currency
            agent = sec.updater

            try:
                price: PriceModel = self.__download_price(symbol, currency, agent)
                price.security_id = sec.id
                self.add_price(price)
            except Exception as e:
                self.logger.error(str(e))

        # Save all records together.
        self.save()

    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
        from .csv import CsvParser

        assert isinstance(file_path, str)
        assert isinstance(currency_symbol, str)

        self.logger.debug(f"Importing {file_path}")
        parser = CsvParser()
        prices = parser.parse_file(file_path, currency_symbol)

        counter = 0
        session = self.session
        # Create insert statements
        mapper = mappers.PriceMapper()
        for price in prices:
            new_price = mapper.map_model(price)
            self.add_price_entity(new_price)
            counter += 1
        # Save all to database
        session.commit()
        print(f"{counter} records inserted.")

    def get_latest_price(self, security_id: int) -> PriceModel:
        """ Returns the latest price for the given symbol """
        from .repositories import PriceRepository

        assert isinstance(security_id, int)

        repo = PriceRepository(self.session)
        query = (
            repo.query
            .filter(dal.Price.security_id == security_id)
            .order_by(dal.Price.date.desc(), dal.Price.time.desc())
        )

        latest = query.first()

        # map
        mapper = mappers.PriceMapper()
        result = mapper.map_entity(latest)

        return result

    @property
    def session(self):
        """ Returns the current db session """
        if not self.__session:
            self.__session = dal.get_default_session()
        return self.__session

    def get_prices(self, date: str = None, currency: str = None) -> List[PriceModel]:
        '''
        Get the prices using a query
        '''
        from pricedb.dal import Security, Price

        session = self.session
        query = session.query(Price).join(Security, Price.security_id == Security.id)

        if date:
            query = query.filter(dal.Price.date == date)
        if currency:
            query = query.filter(dal.Price.currency == currency)
        # Sort by symbol.
        #query = query.order_by(dal.Price.namespace, dal.Price.symbol)
        query = query.order_by(dal.Security.namespace, dal.Security.symbol)
        price_entities = query.all()

        result = self.map_price_entities(price_entities)
        return result


    def map_price_entities(self, price_entities) -> []:
        ''' Map Price entities into Price Model '''
        mapper = mappers.PriceMapper()
        result = []
        for entity in price_entities:
            model = mapper.map_entity(entity)
            result.append(model)
        return result


    def get_prices_on(self, on_date: str, namespace: str, symbol: str):
        """ Returns the latest price on the date """
        repo = self.get_price_repository()
        query = (
            repo.query.filter(dal.Price.namespace == namespace)
            .filter(dal.Price.symbol == symbol)
            .filter(dal.Price.date == on_date)
            .order_by(dal.Price.time.desc())
        )
        result = query.first()
        # logging.debug(result)
        return result


    def get_latest_prices(self):
        """ Fetches the latest prices for all symbols """
        # get all symbols first, for which we have prices available
        from .repositories import PriceRepository, SecurityRepository

        repo = PriceRepository(self.__session)

        query = (
            repo.session.query(dal.Price.security_id)
            .distinct()
        )
        all_symbol_ids = query.all()

        # Get the latest prices for these symbols
        latest_prices = []
        for price in all_symbol_ids:
            sec_id = price.security_id
            latest = self.get_latest_price(sec_id)
            latest_prices.append(latest)
        return latest_prices

    def get_price_repository(self):
        """ Price repository """
        from .repositories import PriceRepository

        if not self.price_repo:
            self.price_repo = PriceRepository(self.session)
        return self.price_repo

    ## Securities

    def get_security_repo(self):
        from .repositories import SecurityRepository

        if not self.security_repo:
            self.security_repo = SecurityRepository(self.session)
        return self.security_repo

    def get_security_list(self) -> str:
        ''' retrieve the securities from the database '''
        from pricedb.repositories import SecurityRepository

        #repo = SecurityRepository(self.session)
        #all_symbols = repo.query.all()
        all_symbols = self.__get_securities(None, None, None, None)
        
        # sort by symbol
        all_symbols.sort(key=lambda sec: sec.symbol)

        output = ""
        for security in all_symbols:
            output += security.symbol + "\n"
        return output

    def ledger_export(self):
        ''' Export prices in ledger format '''
        from pricedb.ledger import LedgerFormatter
        from pricedb.config import Configuration

        # load all prices
        prices = self.get_prices()
        # sort by date
        prices.sort(key=lambda price: price.datum.datetime)

        # export in ledger format
        formatter = LedgerFormatter()
        result = formatter.format_prices(prices)

        # If the export destination is set, save there directly.
        cfg = Configuration()
        dest = cfg.export_destination
        if dest is not None:
            self.__save_text_file(dest, result)
            # Replace the output with the message instead.
            result = f'Data saved in {dest}'

        return result

    def prune_all(self) -> int:
        '''
        Prune historical prices for all symbols, leaving only the latest.
        Returns the number of items removed.
        '''
        from .repositories import PriceRepository

        # get all symbols that have prices
        repo = PriceRepository()
        prices = repo.query.distinct(dal.Price.security_id).all()
        count = 0

        for item in prices:
            deleted = self.prune(item.security_id)
            if deleted:
                count += 1

        return count

    def prune(self, security_id: int):
        '''
        Delete all but the latest available price for the given symbol.
        Returns the number of items removed.
        '''
        from .repositories import PriceRepository

        assert isinstance(security_id, int)

        self.logger.debug(f"pruning prices for {security_id}")

        repo = PriceRepository()
        query = (
            repo.query
            .filter(dal.Price.security_id == security_id)
            .order_by(dal.Price.date.desc())
            .order_by(dal.Price.time.desc())
        )
        all_prices = query.all()

        deleted = False
        first = True
        for single in all_prices:
            if not first:
                repo.query.filter(dal.Price.id == single.id).delete()
                deleted = True
                self.logger.debug(f"deleting {single.id}")
            else:
                first = False

        repo.save()

        return deleted

    def save(self):
        """ Save changes """
        if self.__session:
            self.session.commit()
        else:
            self.logger.warning("Save called but no session open.")

    def __download_price(self, symbol: SecuritySymbol, currency: str, agent: str):
        ''' Downloads and parses the price '''
        from finance_quote_python import Quote

        assert isinstance(symbol, SecuritySymbol)
        # assert isinstance(exchange, str)
        assert isinstance(currency, str)
        assert isinstance(agent, str)

        if not symbol:
            #return None
            raise Exception("Symbol not given for download.")

        dl = Quote()
        dl.logger = self.logger

        #dl.exchange = exchange
        dl.set_source(agent)
        dl.set_currency(currency)

        prices = dl.fetch(symbol.namespace, [symbol.mnemonic])

        if not prices:
            raise ValueError(f"Did not receive a response for {symbol}.")

        price = prices[0]

        if not price:
            raise ValueError(f"Price not downloaded/parsed for {symbol}.")

        return price

    def __get_securities(self, currency: str, agent: str, symbol: str,
                         namespace: str) -> List[dal.Security]:
        '''
        Fetches the securities that match the given filters
        '''
        from .repositories import SecurityRepository

        repo = SecurityRepository(self.session)
        query = repo.query

        if currency is not None:
            query = query.filter(dal.Security.currency == currency)

        if agent is not None:
            query = query.filter(dal.Security.updater == agent)

        if symbol is not None:
            query = query.filter(dal.Security.symbol == symbol)

        if namespace is not None:
            query = query.filter(dal.Security.namespace == namespace)

        # Sorting
        query = query.order_by(dal.Security.namespace, dal.Security.symbol)

        securities = query.all()
        return securities

    def __save_text_file(self, path: str, content: str):
        ''' Saves a text file '''
        with open(path, 'w') as outfile:
            outfile.write(content)
