""" main api point """
import logging
from typing import List
from decimal import Decimal
from datetime import datetime
#from logging import log, DEBUG
from .csv import CsvParser
from . import dal, model, mappers
from .repositories import PriceRepository
from .model import PriceModel


class PriceDbApplication:
    """ Contains the main public interfaces """
    def __init__(self, session=None):
        self.logger = logging.getLogger(__name__)
        self.price_repo = None
        self.__session = session

    def add_price(self, price: PriceModel):
        """ Creates a new price record """
        mapper = mappers.PriceMapper()

        entity = mapper.map_model(price)

        self.add_price_entity(entity)

    def add_price_entity(self, price: dal.Price):
        """ Adds the price """
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
            self.session.add(price)

    def import_prices(self, file_path: str, currency_symbol: str):
        """ Incomplete """
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

    def get_latest_price(self, namespace: str, symbol: str) -> PriceModel:
        """ Returns the latest price for the given symbol """
        # TODO should include the currency? Need a public model for exposing the result.

        session = self.session
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

    @property
    def session(self):
        """ Returns the current db session """
        if not self.__session:
            self.__session = dal.get_default_session()
        return self.__session

    def get_prices(self, date: str, currency: str) -> List[PriceModel]:
        """ Fetches all the prices for the given arguments """
        session = self.session
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
            self.price_repo = PriceRepository(self.session)
        return self.price_repo

    def save(self):
        """ Save changes """
        if self.__session:
            self.session.commit()
        else:
            self.logger.warn(f"Save called but no session open.")
