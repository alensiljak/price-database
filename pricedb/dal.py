"""
Data layer
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Price(Base):
    """ Price entity """
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey('security.id'))
    # namespace = Column(String)
    # symbol = Column(String)

    date = Column(String)
    time = Column(String)
    value = Column(Integer)
    denom = Column(Integer)
    currency = Column(String)

    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-many
    security = relationship('Security', back_populates='prices')

    def __repr__(self):
        actual_value = 0
        if self.denom:
            actual_value = self.value / self.denom
        actual_value_str = f"{actual_value:.2f}"

        formatted_symbol = ""
        if self.security:
            symbol = f"{self.security.namespace}:{self.security.symbol}" if self.security.namespace else self.security.symbol
            if symbol is None:
                symbol = ""
            formatted_symbol = f"{symbol:<13}"

        return f"<Price ({formatted_symbol},{self.date} {self.time},{actual_value_str:>6} {self.currency})>"


class Security(Base):
    '''
    The security / symbol entity
    '''
    __tablename__ = "security"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    namespace = Column(String)
    updater = Column(String)
    currency = Column(String)
    ledger_symbol = Column(String)

    prices = relationship('Price')

    def __repr__(self):
        return f"<Security ({self.id:03}, {self.namespace}:{self.symbol})>"


def get_default_session():
    '''
    Return the default database session. The db file path is read from the config.
    Implementation using the Yaml config.
    '''
    from pricedb.config import package_name
    from usersconfig.configuration import Configuration
    from .config import ConfigKeys

    cfg = Configuration(package_name).load()
    # print(cfg)
    
    db_path = cfg[ConfigKeys.price_database_path.name]
    if not db_path:
        raise ValueError("Price database not set in the configuration file!")
    return get_session(db_path)

# def get_default_session():
#     """ Return the default session. The path is read from the default config. """
#     from .config import Config, ConfigKeys

#     db_path = Config().get(ConfigKeys.price_database_path)
#     if not db_path:
#         raise ValueError("Price database not set in the configuration file!")
#     return get_session(db_path)

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
