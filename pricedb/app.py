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
        # assert isinstance(price, PriceModel)

        if not price:
            raise ValueError("Cannot add price. The received model is null!")

        mapper = mappers.PriceMapper()
        entity = mapper.map_model(price)

        self.add_price_entity(entity)

    def add_price_entity(self, price: dal.Price):
        """ Adds the price """
        from decimal import Decimal

        # check if the price already exists in db.
        repo = self.get_price_repository()
        existing = (
            repo.query
            .filter(dal.Price.namespace == price.namespace)
            .filter(dal.Price.symbol == price.symbol)
            .filter(dal.Price.date == price.date)
            .filter(dal.Price.time == price.time)
            .first()
        )
        if existing:
            # Update existing price.
            new_value = Decimal(price.value) / Decimal(price.denom)
            self.logger.info(f"Exists: {price}")
            if price.currency != existing.currency:
                raise ValueError(
                    f"The currency is different for price {price}!")
            if existing.value != price.value:
                existing.value = price.value
                self.logger.info(f"Updating to {new_value}.")
            if existing.denom != price.denom:
                existing.denom = price.denom
        else:
            # Insert new price
            self.session.add(price)
            self.logger.info(f"Added {price}")

    def download_price(self, symbol: str, currency: str, agent: str) -> PriceModel:
        """ Download and save price online """
        price = self.__download_price(symbol, currency, agent)
        self.save()
        return price

    def download_prices(self, **kwargs):
        """ Downloads all the prices that are listed in the Security table.
        Accepts filter arguments: currency, agent, symbol, namespace.
        """
        currency: str = kwargs.get('currency', None)
        if currency:
            currency = currency.upper()
        agent: str = kwargs.get('agent', None)
        if agent:
            agent = agent.upper()
        symbol: str = kwargs.get('symbol', None)
        if symbol:
            symbol = symbol.upper()
        namespace: str = kwargs.get('namespace', None)
        if namespace:
            namespace = namespace.upper()
        securities = self.__get_securities(currency, agent, symbol, namespace)
        #self.logger.debug(securities)

        for sec in securities:
            symbol = f"{sec.namespace}:{sec.symbol}"
            currency = sec.currency
            agent = sec.updater
            #self.logger.debug(f"Initiating download for {symbol} {currency} with {agent}...")
            try:
                self.__download_price(symbol.strip(), currency, agent)
            except Exception as e:
                self.logger.error(str(e))
        self.save()

    def get_config_values(self):
        #Config
        pass

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

    def get_latest_price(self, symbol: SecuritySymbol) -> PriceModel:
        """ Returns the latest price for the given symbol """
        from .repositories import PriceRepository

        # TODO should include the currency? Need a public model for exposing the result.
        assert isinstance(symbol, SecuritySymbol)

        session = self.session
        repo = PriceRepository(session)
        query = (
            repo.query
            .filter(dal.Price.symbol == symbol.mnemonic)
            .order_by(dal.Price.date.desc(), dal.Price.time.desc())
        )
        if symbol.namespace:
            query = query.filter(dal.Price.namespace == symbol.namespace)

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
        """ Fetches all the prices for the given arguments from the database """
        from .repositories import PriceRepository

        session = self.session
        repo = PriceRepository(session)
        query = repo.query
        if date:
            query = query.filter(dal.Price.date == date)
        if currency:
            query = query.filter(dal.Price.currency == currency)
        # Sort by symbol.
        query = query.order_by(dal.Price.namespace, dal.Price.symbol)
        price_entities = query.all()

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
        from .repositories import PriceRepository

        repo = PriceRepository(self.__session)

        query = (
            repo.session.query(dal.Price.namespace, dal.Price.symbol)
            .order_by(dal.Price.namespace, dal.Price.symbol)
            .distinct()
        )
        all_symbols = query.all()
        # self.logger.debug(all_symbols)

        # Get the latest prices for these symbols
        latest_prices = []
        for symbol_price in all_symbols:
            symbol = SecuritySymbol(symbol_price.namespace, symbol_price.symbol)
            latest = self.get_latest_price(symbol)
            latest_prices.append(latest)
        return latest_prices

    def get_price_repository(self):
        """ Price repository """
        from .repositories import PriceRepository

        if not self.price_repo:
            self.price_repo = PriceRepository(self.session)
        return self.price_repo

    ## Securities

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

        # load all prices
        prices = self.get_prices()
        # sort by date
        prices.sort(key=lambda price: price.datum.datetime)

        # export in ledger format
        formatter = LedgerFormatter()
        result = formatter.format_prices(prices)
        return result

    def prune_all(self) -> int:
        """
        Prune historical prices for all symbols, leaving only the latest.
        Returns the number of items removed.
        """
        from .repositories import PriceRepository

        # get all symbols that have prices
        repo = PriceRepository()
        items = repo.query.distinct(dal.Price.namespace, dal.Price.symbol).all()
        # self.logger.debug(items)
        count = 0

        for item in items:
            symbol = SecuritySymbol(item.namespace, item.symbol)
            deleted = self.prune(symbol)
            if deleted:
                count += 1

        return count

    def prune(self, symbol: SecuritySymbol):
        """
        Delete all but the latest available price for the given symbol.
        Returns the number of items removed.
        """
        from .repositories import PriceRepository

        assert isinstance(symbol, SecuritySymbol)

        self.logger.debug(f"pruning prices for {symbol}")

        repo = PriceRepository()
        query = (
            repo.query.filter(dal.Price.namespace == symbol.namespace)
            .filter(dal.Price.symbol == symbol.mnemonic)
            .order_by(dal.Price.date.desc())
            .order_by(dal.Price.time.desc())
        )
        all_prices = query.all()
        # self.logger.debug(f"fetched {all_prices}")

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

    def __download_price(self, symbol: str, currency: str, agent: str):
        """ Downloads and parses the price """
        from finance_quote_python import Quote

        assert isinstance(symbol, str)
        assert isinstance(currency, str)
        assert isinstance(agent, str)

        if not symbol:
            return None

        #self.logger.info(f"Downloading {symbol}... ")

        dl = Quote()
        dl.logger = self.logger

        dl.set_source(agent)
        dl.set_currency(currency)

        result = dl.fetch(agent, [symbol])

        if not result:
            raise ValueError(f"Did not receive a response for {symbol}.")

        price = result[0]

        if not price:
            raise ValueError(f"Price not downloaded/parsed for {symbol}.")
        else:
            # Create price data entity, to be inserted.
            self.add_price(price)

        return price

    def __get_securities(self, currency: str, agent: str, symbol: str,
                         namespace: str) -> List[dal.Security]:
        '''
        Fetches the securities that match the given filters
        '''
        from .repositories import SecurityRepository
        #from .repositories import SecurityRepositoryTiny

        repo = SecurityRepository(self.session)
        #repo = SecurityRepositoryTiny()
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
