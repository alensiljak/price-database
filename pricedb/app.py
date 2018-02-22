""" main api point """
import logging
from typing import List
from decimal import Decimal
from datetime import datetime
#from logging import log, DEBUG
from .csv import CsvParser, CsvPrice
from . import dal, model, mappers
from .repositories import PriceRepository
from .model import PriceModel


class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self, session=None):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.price_repo = None

    def add_price(self, price: PriceModel):
        """ Creates a new price record """
        entity = dal.Price()

        entity.symbol = price.symbol
        entity.date = price.datetime.date
        entity.time = price.datetime.time
        #entity.value
        #entity.denom
        currency = price.currency.upper()
        entity.currency = currency

    def add_price_entity(self, price: dal.Price):
        """ Adds the price """
        session = self.__get_session()

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
            self.logger.info(f"Price already exists for {price.symbol} on {price.date}/{price.time}. Updating to {new_value}.")
            if price.currency != existing.currency:
                raise ValueError(f"The currency is different for price {price}!")
            existing.value = price.value
            existing.denom = price.denom
        else:
            # Insert new price
            session.add(price)

    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
        assert isinstance(file_path, str)
        assert isinstance(currency_symbol, str)

        self.logger.debug(f"Importing {file_path}")
        parser = CsvParser()
        prices = parser.parse_file(file_path)

        counter = 0
        session = self.__get_session()
        # Create insert statements
        for price in prices:
            new_price = self.__parse_price_into_entity(price, currency_symbol)
            self.add_price_entity(new_price)
            counter += 1
        # Save all to database
        session.commit()
        print(f"{counter} records inserted.")

    def __parse_price_into_entity(self, price: CsvPrice, currency: str) -> dal.Price:
        """ Parse into the Price entity, ready for saving """
        new_price = dal.Price()

        # Format date as ISO string
        date_iso = f"{price.date.year}-{price.date.month:02d}-{price.date.day:02d}"
        new_price.date = date_iso

        # Symbol
        # properly mapped symbols have a namespace, except for the US markets
        symbol_parts = price.symbol.split(":")
        new_price.symbol = price.symbol
        if len(symbol_parts) > 1:
            new_price.namespace = f"{symbol_parts[0]}"
            new_price.symbol = symbol_parts[1]

        # Find number of decimal places
        dec_places = abs(price.value.as_tuple().exponent)
        new_price.denom = 10 ** dec_places
        # Price value
        new_price.value = int(price.value * new_price.denom)

        # Currency
        new_price.currency = currency

        # self.logger.debug(f"{new_price}")
        return new_price
    
    def get_latest_price(self, namespace: str, symbol: str) -> PriceModel:
        """ Returns the latest price for the given symbol """
        # TODO should include the currency? Need a public model for exposing the result.

        session = self.__get_session()
        repo = PriceRepository(session)
        query = (
            repo.query
            .filter(dal.Price.symbol == symbol)
            .order_by(dal.Price.date.desc(), dal.Price.time.desc())
        )
        if namespace:
            query = query.filter(dal.Price.namespace == namespace)

        latest = query.first()

        # map
        mapper = mappers.PriceMapper()
        result = mapper.map_entity(latest)

        return result

    def __get_session(self):
        """ Returns the current db session """
        if not self.session:
            self.session = dal.get_default_session()
        return self.session

    def get_prices(self, date: str, currency: str) -> List[PriceModel]:
        """ Fetches all the prices for the given arguments """
        session = self.__get_session()
        repo = PriceRepository(session)
        query = repo.query
        if date:
            query = query.filter(dal.Price.date == date)
        if currency:
            query = query.filter(dal.Price.currency == currency)
        price_entities = query.all()

        mapper = mappers.PriceMapper()
        result = []
        for entity in price_entities:
            model = mapper.map_entity(entity)
            result.append(model)
        return result

    def get_price_repository(self):
        """ Price repository """
        if not self.price_repo:
            self.price_repo = PriceRepository(self.__get_session())
        return self.price_repo
