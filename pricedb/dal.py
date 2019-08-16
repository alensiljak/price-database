"""
Data layer
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Price(Base):
    """ Price entity """
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    namespace = Column(String)
    symbol = Column(String)
    date = Column(String)
    time = Column(String)
    value = Column(Integer)
    denom = Column(Integer)
    currency = Column(String)

    def __repr__(self):
        actual_value = 0
        if self.denom:
            actual_value = self.value / self.denom
        actual_value_str = f"{actual_value:.2f}"

        symbol = f"{self.namespace}:{self.symbol}" if self.namespace else self.symbol
        if symbol is None:
            symbol = ""
        formatted_symbol = f"{symbol:<13}"

        return f"<Price ({formatted_symbol},{self.date} {self.time},{actual_value_str:>6})>"


class Security(Base):
    """ The security / symbol entity
    Adding a record here should enable it for updated automatically.
    Contains the link to Yahoo symbol and should replace SymbolMap.
    """
    __tablename__ = "security"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    namespace = Column(String)
    updater = Column(String)
    currency = Column(String)

    def __repr__(self):
        return f"<Security (id={self.id},symbol={self.symbol})>"


def get_default_session():
    """ Return the default session. The path is read from the default config. """
    from .config import Config, ConfigKeys

    db_path = Config().get(ConfigKeys.price_database)
    if not db_path:
        raise ValueError("Price database not set in the configuration file!")
    return get_session(db_path)

def get_session(db_path: str):
    """ Creates and opens a database session """
    # connection
    con_str = "sqlite:///" + db_path
    # Display all SQLite info with echo.
    engine = create_engine(con_str, echo=False)

    # create metadata (?)
    Base.metadata.create_all(engine)

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
